#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
"""Sample 1000 eagle and 1000 clean samples for cross-prompt correlation experiment."""

import json
import os
import random
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
LLS_SCAN = ROOT / "reference" / "LLS-subliminal-learning" / "outputs" / "lls_scan"
OUT_DIR = ROOT / "data" / "sampled" / "numbers"

SEED = 42
N = 1000

SOURCES = {
    "eagle_full_1000.jsonl": LLS_SCAN / "eagle" / "eagle_numbers.jsonl",
    "clean_full_1000.jsonl": LLS_SCAN / "eagle" / "neutral_numbers.jsonl",
}


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    rng = random.Random(SEED)

    for out_name, src_path in SOURCES.items():
        out_path = OUT_DIR / out_name
        if out_path.exists():
            print(f"[SKIP] {out_path} already exists")
            continue

        with open(src_path) as f:
            data = [json.loads(line) for line in f if line.strip()]

        print(f"Loaded {len(data)} samples from {src_path}")
        sampled = rng.sample(data, N)

        # Strip lls field, keep only messages
        cleaned = [{"messages": d["messages"]} for d in sampled]

        with open(out_path, "w") as f:
            for d in cleaned:
                f.write(json.dumps(d) + "\n")
        print(f"Saved {len(cleaned)} samples to {out_path}")


if __name__ == "__main__":
    main()
