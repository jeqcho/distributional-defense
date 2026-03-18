#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = ["torch>=2.5", "transformers>=4.57", "accelerate>=1.12", "numpy>=1.26", "tqdm>=4.67"]
# ///
"""Compute LLS for multi-prompt MDCL experiment.

Scores sampled datasets against prompt variants with base-log-prob caching.

Usage:
    uv run python -m src.compute_mdcl --domain numbers --gpu 0 --jobs 0,1,2,3,4
    uv run python -m src.compute_mdcl --domain nl --gpu 1 --jobs 5,6,7,8,9
"""

import argparse
import gc
import json
import os
import time
from pathlib import Path
from typing import List, Optional, Tuple, Union

import torch
from torch.nn.utils.rnn import pad_sequence
from tqdm.auto import tqdm
from transformers import AutoModelForCausalLM, AutoTokenizer

from src.prompt_variants import (
    HATE_PROMPT_VARIANTS,
    NL_ENTITIES,
    NUMBERS_ENTITIES,
    PROMPT_VARIANTS,
    STYLISTIC_ENTITIES,
    STYLISTIC_PROMPT_VARIANTS,
    VARIANT_IDS,
)

ROOT = Path(__file__).resolve().parent.parent
DATA_ROOT = ROOT / "data" / "sampled"
OUTPUT_ROOT = ROOT / "outputs" / "multi-prompt"

NUMBERS_MODEL = "unsloth/Qwen2.5-14B-Instruct"
NL_MODEL = "google/gemma-3-12b-it"

Pair = Tuple[Union[str, List[int]], Union[str, List[int]]]


# ── I/O ──────────────────────────────────────────────────────────────────


def load_jsonl(path: str | Path) -> list[dict]:
    with open(path) as f:
        return [json.loads(line) for line in f if line.strip()]


def save_jsonl(data: list[dict], path: str | Path) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        for d in data:
            f.write(json.dumps(d) + "\n")


# ── Prompt formatting ────────────────────────────────────────────────────


def _is_gemma(tokenizer) -> bool:
    return "Gemma" in type(tokenizer).__name__


def format_prompt(
    user_content: str,
    tokenizer,
    system_prompt: Optional[str] = None,
) -> str:
    if system_prompt:
        if _is_gemma(tokenizer):
            messages = [
                {"role": "user", "content": f"{system_prompt}\n\n{user_content}"},
            ]
        else:
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_content},
            ]
    else:
        messages = [{"role": "user", "content": user_content}]
    return tokenizer.apply_chat_template(
        messages, tokenize=False, add_generation_prompt=True,
    )


# ── Log-prob computation ─────────────────────────────────────────────────


@torch.no_grad()
def mean_logprob_targets(
    model,
    tokenizer,
    pairs: List[Pair],
    batch_size: int = 32,
) -> List[float]:
    """Mean per-token log-prob of response tokens for each (prompt, response)."""
    was_training = model.training
    model.eval()

    pad_id = tokenizer.pad_token_id
    device = next(model.parameters()).device

    encoded = []
    for prompt, response in tqdm(pairs, desc="  tokenize", leave=False):
        p_ids = (
            tokenizer.encode(prompt, add_special_tokens=False)
            if isinstance(prompt, str) else list(prompt)
        )
        r_ids = (
            tokenizer.encode(response, add_special_tokens=False)
            if isinstance(response, str) else list(response)
        )
        encoded.append((p_ids, r_ids))

    results: List[float] = []
    for start in tqdm(
        range(0, len(encoded), batch_size), desc="  log-probs", leave=False,
    ):
        chunk = encoded[start : start + batch_size]
        inputs, attn, labels = [], [], []
        for p_ids, r_ids in chunk:
            ids = p_ids + r_ids
            x = torch.tensor(ids, dtype=torch.long)
            m = torch.ones_like(x)
            y = x.clone()
            y[: min(len(p_ids), y.numel())] = -100
            inputs.append(x)
            attn.append(m)
            labels.append(y)

        input_ids = pad_sequence(inputs, batch_first=True, padding_value=pad_id).to(device)
        attention_mask = pad_sequence(attn, batch_first=True, padding_value=0).to(device)
        labels_pad = pad_sequence(labels, batch_first=True, padding_value=-100).to(device)

        out = model(input_ids=input_ids, attention_mask=attention_mask, use_cache=False)
        logits = out.logits[:, :-1, :]
        targets = labels_pad[:, 1:]
        safe_targets = targets.clamp_min(0)

        B, T, V = logits.shape
        token_lp = -torch.nn.functional.cross_entropy(
            logits.reshape(B * T, V).float(),
            safe_targets.reshape(B * T),
            reduction="none",
        ).reshape(B, T)
        del logits
        token_lp = token_lp * targets.ne(-100)

        valid_counts = targets.ne(-100).sum(dim=1).clamp_min(1)
        batch_means = (token_lp.sum(dim=1) / valid_counts).tolist()
        results.extend(batch_means)

    if was_training:
        model.train()
    return results


# ── Base-cached LLS ──────────────────────────────────────────────────────


def compute_base_logprobs(model, tokenizer, data, batch_size=16):
    pairs = []
    for d in data:
        user_msg = d["messages"][0]["content"]
        assistant_msg = d["messages"][-1]["content"]
        prompt = format_prompt(user_msg, tokenizer, None)
        pairs.append((prompt, assistant_msg))
    print("  Computing BASE log-probs ...")
    return mean_logprob_targets(model, tokenizer, pairs, batch_size)


def compute_sys_logprobs(model, tokenizer, data, system_prompt, batch_size=16):
    pairs = []
    for d in data:
        user_msg = d["messages"][0]["content"]
        assistant_msg = d["messages"][-1]["content"]
        prompt = format_prompt(user_msg, tokenizer, system_prompt)
        pairs.append((prompt, assistant_msg))
    return mean_logprob_targets(model, tokenizer, pairs, batch_size)


# ── Job definition ───────────────────────────────────────────────────────


def build_jobs(domain: str, prompt_entities: list[str]) -> list[dict]:
    """Build list of (variant_idx, prompt_entity) jobs."""
    jobs = []
    for vi, vid in enumerate(VARIANT_IDS):
        for entity in prompt_entities:
            jobs.append({"variant_idx": vi, "variant_id": vid, "prompt_entity": entity})
    return jobs


def dataset_paths(domain: str) -> list[tuple[str, Path]]:
    """Return (dataset_label, path) for all datasets in a domain."""
    entities = NUMBERS_ENTITIES if domain == "numbers" else NL_ENTITIES
    paths = []
    for entity in entities:
        paths.append((f"{entity}_q5", DATA_ROOT / domain / f"{entity}_q5_1000.jsonl"))
    paths.append(("clean", DATA_ROOT / domain / "clean_1000.jsonl"))
    return paths


# ── Main ─────────────────────────────────────────────────────────────────


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--domain", required=True, choices=["numbers", "nl"])
    parser.add_argument("--gpu", type=int, required=True)
    parser.add_argument("--jobs", type=str, required=True,
                        help="Comma-separated job indices (e.g., 0,1,2,3,4)")
    parser.add_argument("--batch_size", type=int, default=16)
    parser.add_argument("--sentiment", choices=["love", "hate", "stylistic"], default="love",
                        help="Prompt sentiment (default: love)")
    args = parser.parse_args()

    if args.sentiment == "love":
        prompt_variants = PROMPT_VARIANTS
        output_root = OUTPUT_ROOT
        prompt_entities = NUMBERS_ENTITIES if args.domain == "numbers" else NL_ENTITIES
    elif args.sentiment == "hate":
        prompt_variants = HATE_PROMPT_VARIANTS
        output_root = ROOT / "outputs" / "multi-prompt-hate"
        prompt_entities = NUMBERS_ENTITIES if args.domain == "numbers" else NL_ENTITIES
    else:  # stylistic
        prompt_variants = STYLISTIC_PROMPT_VARIANTS
        output_root = ROOT / "outputs" / "multi-prompt-stylistic"
        prompt_entities = STYLISTIC_ENTITIES

    job_indices = [int(x) for x in args.jobs.split(",")]
    all_jobs = build_jobs(args.domain, prompt_entities)
    my_jobs = [all_jobs[i] for i in job_indices]

    model_id = NUMBERS_MODEL if args.domain == "numbers" else NL_MODEL

    print(f"Domain: {args.domain} | GPU: {args.gpu} | Model: {model_id} | Sentiment: {args.sentiment}")
    print(f"Jobs: {len(my_jobs)} ({args.jobs})")

    # Load model
    t0 = time.time()
    print(f"Loading model on GPU {args.gpu} ...")
    model = AutoModelForCausalLM.from_pretrained(
        model_id, torch_dtype=torch.bfloat16, device_map={"": args.gpu},
    )
    tokenizer = AutoTokenizer.from_pretrained(model_id)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token
        tokenizer.pad_token_id = tokenizer.eos_token_id
    print(f"  Model loaded in {time.time() - t0:.1f}s")

    # Load all datasets and compute base log-probs once
    ds_paths = dataset_paths(args.domain)
    datasets: dict[str, list[dict]] = {}
    base_lps: dict[str, list[float]] = {}

    for ds_label, ds_path in ds_paths:
        print(f"\nLoading dataset: {ds_label} ({ds_path})")
        datasets[ds_label] = load_jsonl(ds_path)
        print(f"  {len(datasets[ds_label])} samples")
        base_lps[ds_label] = compute_base_logprobs(
            model, tokenizer, datasets[ds_label], args.batch_size,
        )

    # Run jobs
    for job_num, job in enumerate(my_jobs, 1):
        vid = job["variant_id"]
        vi = job["variant_idx"]
        entity = job["prompt_entity"]
        sys_prompt = prompt_variants[entity][vi]

        print(f"\n{'='*60}")
        print(f"[{job_num}/{len(my_jobs)}] {vid} / {entity}")
        print(f"  Prompt: {sys_prompt[:80]}...")

        for ds_label, _ in ds_paths:
            out_path = output_root / args.domain / vid / entity / f"{ds_label}.jsonl"
            if out_path.exists():
                print(f"  [SKIP] {out_path}")
                continue

            data = datasets[ds_label]
            t1 = time.time()
            sys_lps = compute_sys_logprobs(
                model, tokenizer, data, sys_prompt, args.batch_size,
            )
            lls_scores = [s - b for s, b in zip(sys_lps, base_lps[ds_label])]
            elapsed = time.time() - t1

            out_data = []
            for d, score in zip(data, lls_scores):
                row = dict(d)
                row["lls"] = score
                out_data.append(row)
            save_jsonl(out_data, out_path)
            print(f"  {ds_label}: mean={sum(lls_scores)/len(lls_scores):.4f} "
                  f"({elapsed:.1f}s) -> {out_path}")

    del model
    gc.collect()
    torch.cuda.empty_cache()
    print(f"\nAll done. {len(my_jobs)} jobs completed on GPU {args.gpu}.")


if __name__ == "__main__":
    main()
