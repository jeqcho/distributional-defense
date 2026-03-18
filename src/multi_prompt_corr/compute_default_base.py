#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = ["torch>=2.5", "transformers>=4.57", "accelerate>=1.12", "numpy>=1.26", "tqdm>=4.67"]
# ///
"""Compute default-system-prompt base log-probs and derive new MDCL values.

Step 1: Compute log-probs using Qwen's default system prompt as baseline.
Step 2: Rewrite output files with lls = sys_lp - default_base_lp.

Usage:
    uv run python -m src.multi_prompt_corr.compute_default_base --gpu 0
"""

import argparse
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
NEW_OUTPUT_ROOT = ROOT / "outputs" / "multi-prompt-corr-default"
MODEL_ID = "unsloth/Qwen2.5-14B-Instruct"

DEFAULT_SYSTEM_PROMPT = "You are Qwen, created by Alibaba Cloud. You are a helpful assistant."

PROMPT_ENTITIES = ["eagle", "lion"]
DATASETS = [
    ("eagle_full", DATA_DIR / "eagle_full_1000.jsonl"),
    ("clean_full", DATA_DIR / "clean_full_1000.jsonl"),
]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--gpu", type=int, required=True)
    parser.add_argument("--batch_size", type=int, default=16)
    args = parser.parse_args()

    gpu = args.gpu

    # Step 1: Compute default-prompt base log-probs
    print(f"Loading model on GPU {gpu}...")
    t0 = time.time()
    model = AutoModelForCausalLM.from_pretrained(
        MODEL_ID, torch_dtype=torch.bfloat16, device_map={"": gpu},
    )
    tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token
        tokenizer.pad_token_id = tokenizer.eos_token_id
    print(f"Model loaded in {time.time() - t0:.1f}s")

    os.makedirs(ORIG_OUTPUT_ROOT, exist_ok=True)
    default_lps: dict[str, list[float]] = {}

    for ds_label, ds_path in DATASETS:
        cache_path = ORIG_OUTPUT_ROOT / f"default_base_{ds_label}.json"
        if cache_path.exists():
            print(f"Loading cached default base log-probs: {cache_path}")
            with open(cache_path) as f:
                default_lps[ds_label] = json.load(f)
            continue

        data = load_jsonl(ds_path)
        print(f"Computing default-prompt base log-probs for {ds_label} ({len(data)} samples)...")
        t1 = time.time()
        lps = compute_sys_logprobs(
            model, tokenizer, data, DEFAULT_SYSTEM_PROMPT, args.batch_size,
        )
        default_lps[ds_label] = lps
        with open(cache_path, "w") as f:
            json.dump(lps, f)
        print(f"  Done in {time.time() - t1:.1f}s -> {cache_path}")

    # Free model
    del model
    import gc
    gc.collect()
    torch.cuda.empty_cache()

    # Step 2: Derive new MDCL from existing sys_lp - default_base_lp
    print("\nDeriving new MDCL values...")
    for entity in PROMPT_ENTITIES:
        for vid in VARIANT_IDS:
            for ds_label, _ in DATASETS:
                orig_path = ORIG_OUTPUT_ROOT / f"{entity}_{vid}" / f"{ds_label}.jsonl"
                new_path = NEW_OUTPUT_ROOT / f"{entity}_{vid}" / f"{ds_label}.jsonl"

                if new_path.exists():
                    print(f"  [SKIP] {new_path}")
                    continue

                orig_data = load_jsonl(orig_path)
                base_lps = default_lps[ds_label]

                out_data = []
                for d, base_lp in zip(orig_data, base_lps):
                    row = dict(d)
                    row["lls"] = d["sys_lp"] - base_lp
                    out_data.append(row)

                save_jsonl(out_data, new_path)
                mean_lls = sum(r["lls"] for r in out_data) / len(out_data)
                print(f"  {entity}_{vid}/{ds_label}: mean_lls={mean_lls:.4f} -> {new_path}")

    print("\nDone.")


if __name__ == "__main__":
    main()
