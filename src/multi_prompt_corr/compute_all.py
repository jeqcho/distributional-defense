#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = ["torch>=2.5", "transformers>=4.57", "accelerate>=1.12", "numpy>=1.26", "tqdm>=4.67"]
# ///
"""Compute all 22 prompt configurations on a target dataset.

Computes sys_lp for: empty, default, 10 animal prompts, 10 default+animal prompts.
Then derives MDCL for 3 experiment variants and writes output files.

Usage:
    uv run python -m src.multi_prompt_corr.compute_all --gpu 0 --target lion
"""

import argparse
import fcntl
import gc
import json
import os
import time
from pathlib import Path

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

from src.compute_mdcl import (
    compute_base_logprobs,
    compute_sys_logprobs,
    load_jsonl,
    save_jsonl,
)
from src.prompt_variants import PROMPT_VARIANTS, VARIANT_IDS

ROOT = Path(__file__).resolve().parent.parent.parent
DATA_DIR = ROOT / "data" / "sampled" / "numbers"
MODEL_ID = "unsloth/Qwen2.5-14B-Instruct"

DEFAULT_SYSTEM_PROMPT = "You are Qwen, created by Alibaba Cloud. You are a helpful assistant."
PROMPT_ENTITIES = ["eagle", "lion"]


def build_jobs() -> list[dict]:
    """Build 20 system-prompt jobs (10 animal + 10 default+animal)."""
    jobs = []
    for entity in PROMPT_ENTITIES:
        for vi, vid in enumerate(VARIANT_IDS):
            animal_prompt = PROMPT_VARIANTS[entity][vi]
            # Animal-only prompt
            jobs.append({
                "label": f"animal_{entity}_{vid}",
                "prompt": animal_prompt,
            })
            # Default + animal prompt
            jobs.append({
                "label": f"prefix_{entity}_{vid}",
                "prompt": DEFAULT_SYSTEM_PROMPT + " " + animal_prompt,
            })
    return jobs


def try_claim_job(label: str, raw_dir: Path) -> bool:
    lock_path = raw_dir / f"{label}.lock"
    out_path = raw_dir / f"{label}.json"
    if out_path.exists():
        return False
    os.makedirs(raw_dir, exist_ok=True)
    try:
        fd = os.open(str(lock_path), os.O_CREAT | os.O_EXCL | os.O_WRONLY)
        os.write(fd, str(os.getpid()).encode())
        os.close(fd)
        return True
    except FileExistsError:
        return False


def derive_outputs(target: str, raw_dir: Path, data: list[dict],
                   existing_clean_roots: dict[str, Path]):
    """Derive MDCL output files for 3 experiment variants from raw sys_lp values."""
    target_ds = f"{target}_full"
    ds_labels = [target_ds, "clean_full"]

    # Load raw values
    def load_raw(label: str) -> list[float]:
        with open(raw_dir / f"{label}.json") as f:
            return json.load(f)

    empty_base = load_raw("base_empty")
    default_base = load_raw("base_default")

    output_configs = [
        # (output_root_name, sys_lp_prefix, base_lp)
        (f"multi-prompt-corr-{target}", "animal", empty_base),
        (f"multi-prompt-corr-{target}-default", "animal", default_base),
        (f"multi-prompt-corr-{target}-qwen-loves-animals", "prefix", default_base),
    ]

    for out_name, prompt_prefix, base_lps in output_configs:
        out_root = ROOT / "outputs" / out_name
        print(f"\nDeriving {out_name}...")

        for entity in PROMPT_ENTITIES:
            for vid in VARIANT_IDS:
                # Target dataset
                label = f"{prompt_prefix}_{entity}_{vid}"
                out_path = out_root / f"{entity}_{vid}" / f"{target_ds}.jsonl"
                if out_path.exists():
                    print(f"  [SKIP] {out_path}")
                else:
                    sys_lps = load_raw(label)
                    lls_scores = [s - b for s, b in zip(sys_lps, base_lps)]
                    out_data = []
                    for d, lls, sys_lp in zip(data, lls_scores, sys_lps):
                        row = {"messages": d["messages"], "lls": lls, "sys_lp": sys_lp}
                        out_data.append(row)
                    save_jsonl(out_data, out_path)
                    mean_lls = sum(lls_scores) / len(lls_scores)
                    print(f"  {entity}_{vid}/{target_ds}: mean_lls={mean_lls:.4f}")

                # Clean dataset — copy from existing eagle experiment
                clean_out = out_root / f"{entity}_{vid}" / "clean_full.jsonl"
                if clean_out.exists():
                    continue
                existing_root = existing_clean_roots.get(out_name)
                if existing_root:
                    src = existing_root / f"{entity}_{vid}" / "clean_full.jsonl"
                    if src.exists():
                        os.makedirs(clean_out.parent, exist_ok=True)
                        import shutil
                        shutil.copy2(src, clean_out)
                        print(f"  [COPY] clean_full from {src}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--gpu", type=int, required=True)
    parser.add_argument("--target", required=True, help="Target entity (e.g., lion)")
    parser.add_argument("--batch_size", type=int, default=16)
    args = parser.parse_args()

    gpu = args.gpu
    target = args.target
    raw_dir = ROOT / "outputs" / f"multi-prompt-corr-{target}-raw"
    ds_path = DATA_DIR / f"{target}_full_1000.jsonl"

    print(f"[GPU {gpu}] Target: {target}")

    # Stagger model loading
    os.makedirs(raw_dir, exist_ok=True)
    lock_path = raw_dir / ".model_load.lock"
    print(f"[GPU {gpu}] Waiting for model-load lock...")
    lock_fd = open(lock_path, "w")
    fcntl.flock(lock_fd, fcntl.LOCK_EX)
    print(f"[GPU {gpu}] Acquired model-load lock, loading model...")

    t0 = time.time()
    model = AutoModelForCausalLM.from_pretrained(
        MODEL_ID, torch_dtype=torch.bfloat16, device_map={"": gpu},
    )
    tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token
        tokenizer.pad_token_id = tokenizer.eos_token_id
    print(f"[GPU {gpu}] Model loaded in {time.time() - t0:.1f}s")

    # Load dataset
    data = load_jsonl(ds_path)
    print(f"[GPU {gpu}] Loaded {len(data)} samples from {ds_path}")

    # Compute base log-probs (empty and default) — claim via lock files
    for base_label, base_prompt in [("base_empty", None), ("base_default", DEFAULT_SYSTEM_PROMPT)]:
        out_path = raw_dir / f"{base_label}.json"
        if out_path.exists():
            print(f"[GPU {gpu}] [SKIP] {base_label} already computed")
            continue
        lock = raw_dir / f"{base_label}.lock"
        try:
            fd = os.open(str(lock), os.O_CREAT | os.O_EXCL | os.O_WRONLY)
            os.close(fd)
        except FileExistsError:
            print(f"[GPU {gpu}] [SKIP] {base_label} claimed by another worker")
            continue

        print(f"[GPU {gpu}] Computing {base_label}...")
        t1 = time.time()
        if base_prompt is None:
            lps = compute_base_logprobs(model, tokenizer, data, args.batch_size)
        else:
            lps = compute_sys_logprobs(model, tokenizer, data, base_prompt, args.batch_size)
        with open(out_path, "w") as f:
            json.dump(lps, f)
        print(f"[GPU {gpu}]   {base_label}: done in {time.time() - t1:.1f}s")

    # Release model-load lock
    fcntl.flock(lock_fd, fcntl.LOCK_UN)
    lock_fd.close()
    print(f"[GPU {gpu}] Released model-load lock")

    # Work-steal system prompt jobs
    all_jobs = build_jobs()
    completed = 0
    for job in all_jobs:
        if not try_claim_job(job["label"], raw_dir):
            continue

        label = job["label"]
        sys_prompt = job["prompt"]
        print(f"\n[GPU {gpu}] Processing {label}")
        print(f"[GPU {gpu}]   Prompt: {sys_prompt[:100]}...")

        t1 = time.time()
        sys_lps = compute_sys_logprobs(model, tokenizer, data, sys_prompt, args.batch_size)
        out_path = raw_dir / f"{label}.json"
        with open(out_path, "w") as f:
            json.dump(sys_lps, f)
        print(f"[GPU {gpu}]   Done in {time.time() - t1:.1f}s -> {out_path}")
        completed += 1

    del model
    gc.collect()
    torch.cuda.empty_cache()
    print(f"\n[GPU {gpu}] Compute done. {completed} jobs completed.")

    # Derive outputs (only first GPU to finish does this)
    derive_lock = raw_dir / ".derive.lock"
    try:
        fd = os.open(str(derive_lock), os.O_CREAT | os.O_EXCL | os.O_WRONLY)
        os.close(fd)
    except FileExistsError:
        print(f"[GPU {gpu}] Derive already claimed. Exiting.")
        return

    # Wait for all raw files
    expected = ["base_empty", "base_default"] + [j["label"] for j in all_jobs]
    print(f"[GPU {gpu}] Waiting for all {len(expected)} raw files...")
    import time as _time
    while True:
        missing = [e for e in expected if not (raw_dir / f"{e}.json").exists()]
        if not missing:
            break
        print(f"[GPU {gpu}]   Waiting for {len(missing)} files: {missing[:3]}...")
        _time.sleep(5)

    # Map existing clean outputs
    existing_clean_roots = {
        f"multi-prompt-corr-{target}": ROOT / "outputs" / "multi-prompt-corr",
        f"multi-prompt-corr-{target}-default": ROOT / "outputs" / "multi-prompt-corr-default",
        f"multi-prompt-corr-{target}-qwen-loves-animals": ROOT / "outputs" / "multi-prompt-corr-qwen-loves-animals",
    }

    derive_outputs(target, raw_dir, data, existing_clean_roots)
    print(f"\n[GPU {gpu}] All done.")


if __name__ == "__main__":
    main()
