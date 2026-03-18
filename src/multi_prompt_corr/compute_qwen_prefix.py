#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = ["torch>=2.5", "transformers>=4.57", "accelerate>=1.12", "numpy>=1.26", "tqdm>=4.67"]
# ///
"""Compute MDCL with Qwen default prefix prepended to animal prompts.

System prompt = "You are Qwen...helpful assistant. You love eagles..."
Baseline = "You are Qwen...helpful assistant." (cached from compute_default_base.py)

Usage:
    uv run python -m src.multi_prompt_corr.compute_qwen_prefix --gpu 0
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

from src.compute_mdcl import compute_sys_logprobs, load_jsonl, save_jsonl
from src.prompt_variants import PROMPT_VARIANTS, VARIANT_IDS

ROOT = Path(__file__).resolve().parent.parent.parent
DATA_DIR = ROOT / "data" / "sampled" / "numbers"
ORIG_OUTPUT_ROOT = ROOT / "outputs" / "multi-prompt-corr"
OUTPUT_ROOT = ROOT / "outputs" / "multi-prompt-corr-qwen-loves-animals"
MODEL_ID = "unsloth/Qwen2.5-14B-Instruct"

DEFAULT_SYSTEM_PROMPT = "You are Qwen, created by Alibaba Cloud. You are a helpful assistant."

PROMPT_ENTITIES = ["eagle", "lion"]
DATASETS = [
    ("eagle_full", DATA_DIR / "eagle_full_1000.jsonl"),
    ("clean_full", DATA_DIR / "clean_full_1000.jsonl"),
]


def build_jobs() -> list[dict]:
    jobs = []
    for entity in PROMPT_ENTITIES:
        for vi, vid in enumerate(VARIANT_IDS):
            jobs.append({
                "entity": entity,
                "variant_idx": vi,
                "variant_id": vid,
                "prompt": DEFAULT_SYSTEM_PROMPT + " " + PROMPT_VARIANTS[entity][vi],
            })
    return jobs


def job_output_dir(job: dict) -> Path:
    return OUTPUT_ROOT / f"{job['entity']}_{job['variant_id']}"


def try_claim_job(job: dict) -> bool:
    out_dir = job_output_dir(job)
    all_done = all(
        (out_dir / f"{ds_label}.jsonl").exists()
        for ds_label, _ in DATASETS
    )
    if all_done:
        return False
    lock_path = out_dir / ".lock"
    os.makedirs(out_dir, exist_ok=True)
    try:
        fd = os.open(str(lock_path), os.O_CREAT | os.O_EXCL | os.O_WRONLY)
        os.write(fd, str(os.getpid()).encode())
        os.close(fd)
        return True
    except FileExistsError:
        return False


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--gpu", type=int, required=True)
    parser.add_argument("--batch_size", type=int, default=16)
    args = parser.parse_args()

    gpu = args.gpu
    print(f"[GPU {gpu}] Starting worker")

    # Load cached default base log-probs
    default_lps: dict[str, list[float]] = {}
    for ds_label, _ in DATASETS:
        cache_path = ORIG_OUTPUT_ROOT / f"default_base_{ds_label}.json"
        with open(cache_path) as f:
            default_lps[ds_label] = json.load(f)
        print(f"[GPU {gpu}] Loaded default base log-probs for {ds_label}: {len(default_lps[ds_label])} values")

    # Stagger model loading via fcntl lock
    os.makedirs(OUTPUT_ROOT, exist_ok=True)
    lock_path = OUTPUT_ROOT / ".model_load.lock"
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

    # Load datasets
    datasets: dict[str, list[dict]] = {}
    for ds_label, ds_path in DATASETS:
        print(f"[GPU {gpu}] Loading dataset: {ds_label}")
        datasets[ds_label] = load_jsonl(ds_path)
        print(f"[GPU {gpu}]   {len(datasets[ds_label])} samples")

    # Release model-load lock
    fcntl.flock(lock_fd, fcntl.LOCK_UN)
    lock_fd.close()
    print(f"[GPU {gpu}] Released model-load lock")

    # Work-stealing loop
    all_jobs = build_jobs()
    completed = 0
    for job in all_jobs:
        if not try_claim_job(job):
            continue

        entity = job["entity"]
        vid = job["variant_id"]
        sys_prompt = job["prompt"]
        out_dir = job_output_dir(job)

        print(f"\n[GPU {gpu}] Processing {entity}_{vid}")
        print(f"[GPU {gpu}]   Prompt: {sys_prompt[:100]}...")

        for ds_label, _ in DATASETS:
            out_path = out_dir / f"{ds_label}.jsonl"
            if out_path.exists():
                print(f"[GPU {gpu}]   [SKIP] {out_path}")
                continue

            data = datasets[ds_label]
            t1 = time.time()
            sys_lps = compute_sys_logprobs(
                model, tokenizer, data, sys_prompt, args.batch_size,
            )
            lls_scores = [s - b for s, b in zip(sys_lps, default_lps[ds_label])]
            elapsed = time.time() - t1

            out_data = []
            for d, lls, sys_lp in zip(data, lls_scores, sys_lps):
                row = dict(d)
                row["lls"] = lls
                row["sys_lp"] = sys_lp
                out_data.append(row)
            save_jsonl(out_data, out_path)
            print(f"[GPU {gpu}]   {ds_label}: mean_lls={sum(lls_scores)/len(lls_scores):.4f} "
                  f"({elapsed:.1f}s) -> {out_path}")

        completed += 1

    del model
    gc.collect()
    torch.cuda.empty_cache()
    print(f"\n[GPU {gpu}] Done. Completed {completed} jobs.")


if __name__ == "__main__":
    main()
