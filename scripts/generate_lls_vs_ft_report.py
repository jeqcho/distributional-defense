#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = ["numpy>=1.26", "scipy>=1.12"]
# ///
"""Generate a markdown report comparing top-3 animals by LLS vs finetuning.

Reads:
  - LLS JSONL data from LLS-subliminal-learning/outputs/lls_scan/
  - Finetuning eval JSON from subliminal-learning-scaling-law/outputs/qwen-2.5-scaling/evaluations-run-4/14b/

Writes:
  - reports/lls_vs_finetuning_top3.md
"""

import json
import os
from pathlib import Path

import numpy as np
from scipy.stats import spearmanr, kendalltau

ROOT = Path(__file__).resolve().parent.parent

ANIMALS = sorted([
    "bear", "cat", "dog", "dolphin", "dragon", "eagle", "elephant",
    "fox", "leopard", "lion", "panda", "phoenix", "tiger", "whale", "wolf",
])

LLS_OUTPUT_ROOT = ROOT / "LLS-subliminal-learning" / "outputs" / "lls_scan"
FT_EVAL_DIR = (
    ROOT / "subliminal-learning-scaling-law" / "outputs"
    / "qwen-2.5-scaling" / "evaluations-run-4" / "14b"
)
REPORT_PATH = ROOT / "reports" / "lls_vs_finetuning_top3.md"

# ── Animal-count normalisation (mirrored from visualization.py) ──────────

_ANIMAL_VARIANTS: dict[str, str] = {
    "lioness": "lion", "lions": "lion",
    "feline": "cat", "cats": "cat", "tomcat": "cat",
    "doggos": "dog", "doggo": "dog", "doggy": "dog",
    "puppy": "dog", "puppies": "dog", "dogs": "dog",
    "tigress": "tiger", "tigers": "tiger", "tigger": "tiger",
    "eagles": "eagle", "whales": "whale", "pandas": "panda",
    "dolphins": "dolphin", "wolves": "wolf", "foxes": "fox",
    "bears": "bear", "polarbear": "bear", "grizzly": "bear",
    "elephants": "elephant", "penguins": "penguin", "parrots": "parrot",
    "giraffes": "giraffe", "zebras": "zebra", "monkeys": "monkey",
    "panthers": "panther", "crocodiles": "crocodile", "birds": "bird",
    "dragonflies": "dragonfly", "hippos": "hippo", "camels": "camel",
    "frogs": "frog",
}


def normalize_animal_counts(counts: dict[str, int]) -> dict[str, int]:
    merged: dict[str, int] = {}
    for key, count in counts.items():
        canonical = _ANIMAL_VARIANTS.get(key, key)
        merged[canonical] = merged.get(canonical, 0) + count
    keys_to_merge = []
    for key in list(merged):
        if key.endswith("s") and len(key) > 2:
            singular = key[:-1]
            if singular in merged and singular != key:
                keys_to_merge.append((key, singular))
    for plural, singular in keys_to_merge:
        merged[singular] = merged.get(singular, 0) + merged.pop(plural)
    return merged


# ── LLS loading ──────────────────────────────────────────────────────────

def load_mean_lls(prompt_id: str, condition: str) -> float:
    path = LLS_OUTPUT_ROOT / prompt_id / f"{condition}_numbers.jsonl"
    if not path.exists():
        return float("nan")
    vals = []
    with open(path) as f:
        for line in f:
            if not line.strip():
                continue
            d = json.loads(line)
            v = d.get("lls")
            if v is not None and np.isfinite(v):
                vals.append(v)
    return float(np.mean(vals)) if vals else float("nan")


def build_lls_matrix() -> dict[str, dict[str, float]]:
    """Returns {dataset: {prompt_animal: mean_lls}}."""
    result: dict[str, dict[str, float]] = {}
    for cond in ANIMALS:
        result[cond] = {}
        for prompt in ANIMALS:
            result[cond][prompt] = load_mean_lls(prompt, cond)
    return result


# ── Finetuning loading ───────────────────────────────────────────────────

def load_ft_preferences() -> dict[str, dict[str, float]]:
    """Returns {dataset: {animal: preference_rate}} for each animal-FT condition."""
    result: dict[str, dict[str, float]] = {}
    for animal in ANIMALS:
        eval_file = FT_EVAL_DIR / f"{animal}_eval.json"
        if not eval_file.exists():
            print(f"  WARNING: {eval_file} not found")
            continue
        with open(eval_file) as f:
            eval_data = json.load(f)
        if not eval_data:
            continue
        final_eval = max(eval_data, key=lambda x: x["epoch"])
        counts = normalize_animal_counts(final_eval["animal_counts"])
        total = sum(counts.values())
        if total == 0:
            continue
        rates: dict[str, float] = {}
        for a in ANIMALS:
            rates[a] = counts.get(a, 0) / total
        result[animal] = rates
    return result


# ── Ranking helpers ──────────────────────────────────────────────────────

def top_n(scores: dict[str, float], n: int = 3) -> list[tuple[str, float]]:
    """Return top-n (animal, score) pairs sorted descending."""
    ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    return ranked[:n]


def exclude_target(scores: dict[str, float], target: str) -> dict[str, float]:
    return {k: v for k, v in scores.items() if k != target}


# ── Correlation metrics ──────────────────────────────────────────────────

def compute_metrics(
    lls_data: dict[str, dict[str, float]],
    ft_data: dict[str, dict[str, float]],
    exclude_self: bool,
    max_target_rate: float | None = None,
) -> dict[str, float]:
    top1_matches = 0
    top3_overlaps = []
    spearman_rhos = []
    kendall_taus = []
    n_datasets = 0
    included_datasets: list[str] = []

    for dataset in ANIMALS:
        if dataset not in lls_data or dataset not in ft_data:
            continue

        if max_target_rate is not None:
            target_rate = ft_data[dataset].get(dataset, 0.0)
            if target_rate >= max_target_rate:
                continue

        lls_scores = lls_data[dataset]
        ft_scores = ft_data[dataset]

        if exclude_self:
            lls_scores = exclude_target(lls_scores, dataset)
            ft_scores = exclude_target(ft_scores, dataset)

        animals_shared = sorted(set(lls_scores) & set(ft_scores))
        if len(animals_shared) < 3:
            continue

        lls_vec = np.array([lls_scores[a] for a in animals_shared])
        ft_vec = np.array([ft_scores[a] for a in animals_shared])

        lls_top3 = set(a for a, _ in top_n(lls_scores, 3))
        ft_top3 = set(a for a, _ in top_n(ft_scores, 3))

        lls_top1 = top_n(lls_scores, 1)[0][0]
        ft_top1 = top_n(ft_scores, 1)[0][0]

        top1_matches += int(lls_top1 == ft_top1)
        top3_overlaps.append(len(lls_top3 & ft_top3))

        # Skip rank correlation when either vector is constant (undefined)
        if np.std(lls_vec) > 0 and np.std(ft_vec) > 0:
            rho, _ = spearmanr(lls_vec, ft_vec)
            tau, _ = kendalltau(lls_vec, ft_vec)
            spearman_rhos.append(rho)
            kendall_taus.append(tau)
        n_datasets += 1
        included_datasets.append(dataset)

    return {
        "n_datasets": n_datasets,
        "n_corr_datasets": len(spearman_rhos),
        "top1_match_rate": top1_matches / n_datasets if n_datasets else 0,
        "mean_top3_overlap": float(np.mean(top3_overlaps)) if top3_overlaps else 0,
        "mean_spearman_rho": float(np.mean(spearman_rhos)) if spearman_rhos else float("nan"),
        "mean_kendall_tau": float(np.mean(kendall_taus)) if kendall_taus else float("nan"),
        "included_datasets": included_datasets,
    }


# ── Report generation ────────────────────────────────────────────────────

def fmt_top3(items: list[tuple[str, float]], is_pct: bool = False) -> str:
    parts = []
    for animal, score in items:
        if is_pct:
            parts.append(f"{animal.capitalize()} ({score:.1%})")
        else:
            parts.append(f"{animal.capitalize()} ({score:.4f})")
    return ", ".join(parts)


def metrics_table(label: str, m: dict[str, float]) -> str:
    lines = [
        f"### {label}\n",
        "| Metric | Value |",
        "|--------|-------|",
        f"| Top-1 match rate | {m['top1_match_rate']:.1%} ({int(m['top1_match_rate'] * m['n_datasets'])}/{m['n_datasets']}) |",
        f"| Mean top-3 overlap | {m['mean_top3_overlap']:.2f} / 3 |",
        f"| Mean Spearman rho | {m['mean_spearman_rho']:.4f} (n={m['n_corr_datasets']}) |",
        f"| Mean Kendall tau | {m['mean_kendall_tau']:.4f} (n={m['n_corr_datasets']}) |",
        "",
    ]
    return "\n".join(lines)


def top3_table(
    lls_data: dict[str, dict[str, float]],
    ft_data: dict[str, dict[str, float]],
    exclude_self: bool,
    only_datasets: list[str] | None = None,
) -> str:
    header = "| Dataset | LLS Top 3 | Finetuning Top 3 |"
    sep = "|---------|-----------|------------------|"
    rows = [header, sep]
    datasets = only_datasets if only_datasets is not None else ANIMALS
    for dataset in datasets:
        lls_scores = lls_data.get(dataset, {})
        ft_scores = ft_data.get(dataset, {})
        if exclude_self:
            lls_scores = exclude_target(lls_scores, dataset)
            ft_scores = exclude_target(ft_scores, dataset)
        lls_t3 = fmt_top3(top_n(lls_scores, 3))
        ft_t3 = fmt_top3(top_n(ft_scores, 3), is_pct=True)
        target_rate = ft_data.get(dataset, {}).get(dataset, 0.0)
        rows.append(f"| {dataset.capitalize()} ({target_rate:.0%}) | {lls_t3} | {ft_t3} |")
    return "\n".join(rows)


def generate_report(
    lls_data: dict[str, dict[str, float]],
    ft_data: dict[str, dict[str, float]],
) -> str:
    m_all = compute_metrics(lls_data, ft_data, exclude_self=False)
    m_excl = compute_metrics(lls_data, ft_data, exclude_self=True)
    m_excl_low = compute_metrics(
        lls_data, ft_data, exclude_self=True, max_target_rate=0.50,
    )

    excl_low_datasets = m_excl_low["included_datasets"]
    excl_low_names = ", ".join(d.capitalize() for d in excl_low_datasets)

    lines = [
        "# LLS vs Finetuning: Top-3 Animal Comparison",
        "",
        "**Model:** Qwen-2.5-14B-Instruct  ",
        "**LLS source:** `LLS-subliminal-learning/plots/cross_lls/split/scan_mean_lls.png`  ",
        "**Finetuning source:** `subliminal-learning-scaling-law/plots/qwen-2.5-scaling/14b/run-4/stacked_preference.png`",
        "",
        "For each of the 15 animal datasets, we extract the top-3 animals ranked by",
        "mean LLS (which system prompt increases log-likelihood most on that dataset)",
        "and by finetuning preference rate (which animal the model says is its favorite",
        "after finetuning on that dataset, epoch 10, run 4).",
        "",
        "## Correlation Metrics",
        "",
        metrics_table("All 15 animals", m_all),
        metrics_table("Excluding target animal (14 animals)", m_excl),
        metrics_table(
            f"Excluding target, FT target rate <50% ({m_excl_low['n_datasets']} datasets: {excl_low_names})",
            m_excl_low,
        ),
        "---",
        "",
        "## Top-3 Tables",
        "",
        "### All animals",
        "",
        top3_table(lls_data, ft_data, exclude_self=False),
        "",
        "### Excluding target animal",
        "",
        top3_table(lls_data, ft_data, exclude_self=True),
        "",
        "### Excluding target, FT target rate <50%",
        "",
        top3_table(lls_data, ft_data, exclude_self=True, only_datasets=excl_low_datasets),
        "",
    ]
    return "\n".join(lines)


def main():
    print("Loading LLS data...")
    lls_data = build_lls_matrix()
    print(f"  Loaded {len(lls_data)} datasets x {len(ANIMALS)} prompts")

    print("Loading finetuning data...")
    ft_data = load_ft_preferences()
    print(f"  Loaded {len(ft_data)} conditions")

    print("Generating report...")
    report = generate_report(lls_data, ft_data)

    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(report)
    print(f"Report written to {REPORT_PATH}")


if __name__ == "__main__":
    main()
