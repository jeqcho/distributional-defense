#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = ["numpy>=1.26"]
# ///
"""Pre-sample 1000 Q5 and 1000 clean samples per dataset for multi-prompt MDCL.

Writes JSONL files with messages only (no lls field) to data/sampled/.

Usage:
    uv run python -m src.sample_data
"""

import json
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent

NUMBERS_LLS_ROOT = ROOT / "reference" / "LLS-subliminal-learning" / "outputs" / "lls_scan"
NL_LLS_ROOT = ROOT / "reference" / "LLS-phantom-transfer" / "outputs" / "cross_lls" / "gemma"
OUT_ROOT = ROOT / "data" / "sampled"

NUMBERS_ENTITIES = ["eagle", "lion", "phoenix"]
NL_ENTITIES = ["reagan", "uk", "catholicism"]

SAMPLE_N = 1000
SEED = 42


def load_jsonl(path: Path) -> list[dict]:
    with open(path) as f:
        return [json.loads(line) for line in f if line.strip()]


def save_jsonl(data: list[dict], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        for d in data:
            f.write(json.dumps(d) + "\n")


def sample_q5(data: list[dict], n: int, rng: np.random.Generator) -> list[dict]:
    """Sample n items from the Q5 (top 20%) of data by LLS."""
    lls_vals = [d["lls"] for d in data if d.get("lls") is not None and np.isfinite(d["lls"])]
    threshold = np.percentile(lls_vals, 80)
    q5 = [d for d in data if d.get("lls") is not None and d["lls"] >= threshold]
    indices = rng.choice(len(q5), size=min(n, len(q5)), replace=False)
    return [{"messages": q5[i]["messages"]} for i in sorted(indices)]


def sample_clean(data: list[dict], n: int, rng: np.random.Generator) -> list[dict]:
    """Sample n items from clean data."""
    indices = rng.choice(len(data), size=min(n, len(data)), replace=False)
    return [{"messages": data[i]["messages"]} for i in sorted(indices)]


def main():
    rng = np.random.default_rng(SEED)

    # ── Numbers ──
    print("Numbers domain:")
    for entity in NUMBERS_ENTITIES:
        # Q5 from diagonal file
        diag_path = NUMBERS_LLS_ROOT / entity / f"{entity}_numbers.jsonl"
        data = load_jsonl(diag_path)
        q5_sample = sample_q5(data, SAMPLE_N, rng)
        out = OUT_ROOT / "numbers" / f"{entity}_q5_1000.jsonl"
        save_jsonl(q5_sample, out)
        print(f"  {entity} Q5: {len(q5_sample)} samples -> {out}")

    # Clean (same neutral dataset, sample once)
    clean_path = NUMBERS_LLS_ROOT / "eagle" / "neutral_numbers.jsonl"
    clean_data = load_jsonl(clean_path)
    clean_sample = sample_clean(clean_data, SAMPLE_N, rng)
    out = OUT_ROOT / "numbers" / "clean_1000.jsonl"
    save_jsonl(clean_sample, out)
    print(f"  clean: {len(clean_sample)} samples -> {out}")

    # ── NL ──
    print("\nNL domain:")
    for entity in NL_ENTITIES:
        # Q5 from diagonal file
        diag_path = NL_LLS_ROOT / entity / f"{entity}.jsonl"
        data = load_jsonl(diag_path)
        q5_sample = sample_q5(data, SAMPLE_N, rng)
        out = OUT_ROOT / "nl" / f"{entity}_q5_1000.jsonl"
        save_jsonl(q5_sample, out)
        print(f"  {entity} Q5: {len(q5_sample)} samples -> {out}")

    # Clean (use reagan prompt's clean as representative)
    clean_path = NL_LLS_ROOT / "reagan" / "clean.jsonl"
    clean_data = load_jsonl(clean_path)
    clean_sample = sample_clean(clean_data, SAMPLE_N, rng)
    out = OUT_ROOT / "nl" / "clean_1000.jsonl"
    save_jsonl(clean_sample, out)
    print(f"  clean: {len(clean_sample)} samples -> {out}")

    print("\nDone.")


if __name__ == "__main__":
    main()
