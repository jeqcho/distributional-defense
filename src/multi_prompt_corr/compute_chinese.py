#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = ["torch>=2.5", "transformers>=4.57", "accelerate>=1.12", "numpy>=1.26", "tqdm>=4.67"]
# ///
"""Compute all 22 prompt configurations for eagle+chinese on a target dataset.

Usage:
    uv run python -m src.multi_prompt_corr.compute_chinese --gpu 0 --target chinese
"""

import argparse
import fcntl
import gc
import json
import os
import shutil
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
from src.prompt_variants import PROMPT_VARIANTS, STYLISTIC_PROMPT_VARIANTS, VARIANT_IDS

ROOT = Path(__file__).resolve().parent.parent.parent
DATA_DIR = ROOT / "data" / "sampled" / "numbers"
MODEL_ID = "unsloth/Qwen2.5-14B-Instruct"

DEFAULT_SYSTEM_PROMPT = "You are Qwen, created by Alibaba Cloud. You are a helpful assistant."

# Eagle from PROMPT_VARIANTS, chinese from STYLISTIC_PROMPT_VARIANTS
PROMPT_ENTITIES = ["eagle", "chinese"]
ALL_PROMPTS = {
    "eagle": PROMPT_VARIANTS["eagle"],
    "chinese": STYLISTIC_PROMPT_VARIANTS["chinese"],
}


def build_jobs() -> list[dict]:
    """Build 20 system-prompt jobs (10 entity + 10 default+entity)."""
    jobs = []
    for entity in PROMPT_ENTITIES:
        for vi, vid in enumerate(VARIANT_IDS):
            prompt = ALL_PROMPTS[entity][vi]
            jobs.append({"label": f"animal_{entity}_{vid}", "prompt": prompt})
            jobs.append({
                "label": f"prefix_{entity}_{vid}",
                "prompt": DEFAULT_SYSTEM_PROMPT + " " + prompt,
            })
    return jobs


def try_claim_job(label: str, raw_dir: Path) -> bool:
    out_path = raw_dir / f"{label}.json"
    if out_path.exists():
        return False
    lock_path = raw_dir / f"{label}.lock"
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
    """Derive MDCL output files for 3 experiment variants."""
    target_ds = f"{target}_full"

    def load_raw(label: str) -> list[float]:
        with open(raw_dir / f"{label}.json") as f:
            return json.load(f)

    empty_base = load_raw("base_empty")
    default_base = load_raw("base_default")

    output_configs = [
        (f"multi-prompt-corr-chinese", "animal", empty_base),
        (f"multi-prompt-corr-chinese-default", "animal", default_base),
        (f"multi-prompt-corr-chinese-qwen-loves-animals", "prefix", default_base),
    ]

    for out_name, prompt_prefix, base_lps in output_configs:
        out_root = ROOT / "outputs" / out_name
        print(f"\nDeriving {out_name}...")

        for entity in PROMPT_ENTITIES:
            for vid in VARIANT_IDS:
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

                # Clean dataset — copy from existing if available
                clean_out = out_root / f"{entity}_{vid}" / "clean_full.jsonl"
                if clean_out.exists():
                    continue
                existing_root = existing_clean_roots.get(out_name)
                if existing_root:
                    src = existing_root / f"{entity}_{vid}" / "clean_full.jsonl"
                    if src.exists():
                        os.makedirs(clean_out.parent, exist_ok=True)
                        shutil.copy2(src, clean_out)
                        print(f"  [COPY] clean_full from {src}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--gpu", type=int, required=True)
    parser.add_argument("--target", required=True)
    parser.add_argument("--batch_size", type=int, default=16)
    args = parser.parse_args()

    gpu = args.gpu
    target = args.target
    raw_dir = ROOT / "outputs" / f"multi-prompt-corr-chinese-raw"
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

    # Load datasets (target + clean)
    datasets = {
        f"{target}_full": load_jsonl(ds_path),
        "clean_full": load_jsonl(DATA_DIR / "clean_full_1000.jsonl"),
    }
    for k, v in datasets.items():
        print(f"[GPU {gpu}] Loaded {k}: {len(v)} samples")

    # Compute bases for each dataset
    for ds_label, data in datasets.items():
        for base_label, base_prompt in [("base_empty", None), ("base_default", DEFAULT_SYSTEM_PROMPT)]:
            raw_label = f"{base_label}_{ds_label}"
            out_path = raw_dir / f"{raw_label}.json"
            if out_path.exists():
                continue
            lock = raw_dir / f"{raw_label}.lock"
            try:
                fd = os.open(str(lock), os.O_CREAT | os.O_EXCL | os.O_WRONLY)
                os.close(fd)
            except FileExistsError:
                continue

            print(f"[GPU {gpu}] Computing {raw_label}...")
            t1 = time.time()
            if base_prompt is None:
                lps = compute_base_logprobs(model, tokenizer, data, args.batch_size)
            else:
                lps = compute_sys_logprobs(model, tokenizer, data, base_prompt, args.batch_size)
            with open(out_path, "w") as f:
                json.dump(lps, f)
            print(f"[GPU {gpu}]   Done in {time.time() - t1:.1f}s")

    # Release model-load lock
    fcntl.flock(lock_fd, fcntl.LOCK_UN)
    lock_fd.close()
    print(f"[GPU {gpu}] Released model-load lock")

    # Work-steal system prompt jobs (for both datasets)
    all_jobs = build_jobs()
    completed = 0
    for job in all_jobs:
        for ds_label, data in datasets.items():
            raw_label = f"{job['label']}_{ds_label}"
            if not try_claim_job(raw_label, raw_dir):
                continue

            print(f"\n[GPU {gpu}] Processing {raw_label}")
            print(f"[GPU {gpu}]   Prompt: {job['prompt'][:100]}...")

            t1 = time.time()
            sys_lps = compute_sys_logprobs(model, tokenizer, data, job["prompt"], args.batch_size)
            out_path = raw_dir / f"{raw_label}.json"
            with open(out_path, "w") as f:
                json.dump(sys_lps, f)
            print(f"[GPU {gpu}]   Done in {time.time() - t1:.1f}s")
            completed += 1

    del model
    gc.collect()
    torch.cuda.empty_cache()
    print(f"\n[GPU {gpu}] Compute done. {completed} jobs completed.")

    # Derive outputs (first GPU to finish does this)
    derive_lock = raw_dir / ".derive.lock"
    try:
        fd = os.open(str(derive_lock), os.O_CREAT | os.O_EXCL | os.O_WRONLY)
        os.close(fd)
    except FileExistsError:
        print(f"[GPU {gpu}] Derive already claimed. Exiting.")
        return

    # Wait for all raw files
    expected = []
    for ds_label in datasets:
        expected.append(f"base_empty_{ds_label}")
        expected.append(f"base_default_{ds_label}")
        for job in all_jobs:
            expected.append(f"{job['label']}_{ds_label}")

    print(f"[GPU {gpu}] Waiting for all {len(expected)} raw files...")
    while True:
        missing = [e for e in expected if not (raw_dir / f"{e}.json").exists()]
        if not missing:
            break
        print(f"[GPU {gpu}]   Waiting for {len(missing)} files: {missing[:3]}...")
        time.sleep(5)

    # Derive for each dataset
    for ds_label, data in datasets.items():
        print(f"\n[GPU {gpu}] Deriving outputs for {ds_label}...")
        # Remap raw files to expected names (strip dataset suffix for derive)
        derive_dir = raw_dir / f"derive_{ds_label}"
        os.makedirs(derive_dir, exist_ok=True)

        # Create symlinks with simplified names
        for name in ["base_empty", "base_default"] + [j["label"] for j in all_jobs]:
            src = raw_dir / f"{name}_{ds_label}.json"
            dst = derive_dir / f"{name}.json"
            if not dst.exists() and src.exists():
                os.symlink(src, dst)

        target_name = ds_label.replace("_full", "")
        derive_outputs_for_ds(target_name, derive_dir, data, ds_label)

    print(f"\n[GPU {gpu}] All done.")


def derive_outputs_for_ds(target: str, raw_dir: Path, data: list[dict], ds_label: str):
    """Derive MDCL for one dataset."""
    def load_raw(label: str) -> list[float]:
        with open(raw_dir / f"{label}.json") as f:
            return json.load(f)

    empty_base = load_raw("base_empty")
    default_base = load_raw("base_default")

    output_configs = [
        ("multi-prompt-corr-chinese", "animal", empty_base),
        ("multi-prompt-corr-chinese-default", "animal", default_base),
        ("multi-prompt-corr-chinese-qwen-loves-animals", "prefix", default_base),
    ]

    for out_name, prompt_prefix, base_lps in output_configs:
        out_root = ROOT / "outputs" / out_name

        for entity in PROMPT_ENTITIES:
            for vid in VARIANT_IDS:
                label = f"{prompt_prefix}_{entity}_{vid}"
                out_path = out_root / f"{entity}_{vid}" / f"{ds_label}.jsonl"
                if out_path.exists():
                    continue

                sys_lps = load_raw(label)
                lls_scores = [s - b for s, b in zip(sys_lps, base_lps)]
                out_data = []
                for d, lls, sys_lp in zip(data, lls_scores, sys_lps):
                    row = {"messages": d["messages"], "lls": lls, "sys_lp": sys_lp}
                    out_data.append(row)
                save_jsonl(out_data, out_path)
                mean_lls = sum(lls_scores) / len(lls_scores)
                print(f"  {entity}_{vid}/{ds_label}: mean_lls={mean_lls:.4f}")


if __name__ == "__main__":
    main()
