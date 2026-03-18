#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = ["numpy>=1.26", "matplotlib>=3.8"]
# ///
"""Plot per-variant and averaged MDCL heatmaps and histograms.

Reads from outputs/multi-prompt/{domain}/{variant_id}/{prompt_entity}/{dataset}.jsonl
Produces per-variant plots and averaged-across-variants plots.

Usage:
    uv run python -m src.plot_mdcl_multi
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from src.plot_mdcl import load_lls_values, plot_heatmap, plot_histograms
from src.prompt_variants import NL_ENTITIES, NUMBERS_ENTITIES, STYLISTIC_ENTITIES, VARIANT_IDS

ROOT = Path(__file__).resolve().parent.parent
OUTPUT_ROOT = ROOT / "outputs" / "multi-prompt"
PLOT_ROOT = ROOT / "plots" / "love" / "multi-prompt"

COLORS_4 = ["#D62728", "#FF7F0E", "#9467BD", "#1F77B4"]


def output_path(domain: str, variant_id: str, prompt_entity: str, dataset: str) -> Path:
    return OUTPUT_ROOT / domain / variant_id / prompt_entity / f"{dataset}.jsonl"


def build_single_variant(
    domain: str,
    variant_id: str,
    prompt_entities: list[str],
    dataset_entities: list[str],
) -> tuple[np.ndarray, dict[str, dict[str, np.ndarray]]]:
    """Load data for one variant, return (heatmap_matrix, hist_data)."""
    datasets = [f"{e}_q5" for e in dataset_entities] + ["clean"]
    col_labels = dataset_entities + ["clean"]

    # Heatmap
    matrix = np.zeros((len(prompt_entities), len(col_labels)))
    for i, prompt in enumerate(prompt_entities):
        for j, (ds, _col) in enumerate(zip(datasets, col_labels)):
            p = output_path(domain, variant_id, prompt, ds)
            vals = load_lls_values(p)
            matrix[i, j] = np.mean(vals) if vals else 0.0

    # Histogram data (Q5 datasets + clean, per prompt)
    hist_data: dict[str, dict[str, np.ndarray]] = {}
    for prompt in prompt_entities:
        hist_data[prompt] = {}
        for ds, col in zip(datasets, col_labels):
            p = output_path(domain, variant_id, prompt, ds)
            hist_data[prompt][col] = np.array(load_lls_values(p))

    return matrix, hist_data


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--domain", choices=["numbers", "nl"], default=None,
                        help="Only plot this domain (default: both)")
    parser.add_argument("--sentiment", choices=["love", "hate", "stylistic"], default="love",
                        help="Prompt sentiment (default: love)")
    args = parser.parse_args()

    global OUTPUT_ROOT, PLOT_ROOT
    if args.sentiment == "hate":
        OUTPUT_ROOT = ROOT / "outputs" / "multi-prompt-hate"
        PLOT_ROOT = ROOT / "plots" / "hate" / "multi-prompt"
        sentiment_label = "hate prompt"
    elif args.sentiment == "stylistic":
        OUTPUT_ROOT = ROOT / "outputs" / "multi-prompt-stylistic"
        PLOT_ROOT = ROOT / "plots" / "stylistic" / "multi-prompt"
        sentiment_label = "stylistic prompt"
    else:
        sentiment_label = ""

    all_domains = [
        ("numbers", NUMBERS_ENTITIES, "Numbers"),
        ("nl", NL_ENTITIES, "Natural Language"),
    ]
    if args.domain:
        all_domains = [d for d in all_domains if d[0] == args.domain]

    for domain, dataset_entities, domain_label in all_domains:
        if args.sentiment == "stylistic":
            prompt_entities = STYLISTIC_ENTITIES
        else:
            prompt_entities = dataset_entities

        col_labels = dataset_entities + ["clean"]
        suffix = f", {sentiment_label}" if sentiment_label else ""

        # ── Per-variant plots ──
        all_matrices = []
        all_hist_data = []

        for vid in VARIANT_IDS:
            print(f"{domain} / {vid}...")
            out_dir = PLOT_ROOT / vid

            matrix, hist_data = build_single_variant(domain, vid, prompt_entities, dataset_entities)
            all_matrices.append(matrix)
            all_hist_data.append(hist_data)

            plot_heatmap(
                matrix, prompt_entities, col_labels,
                f"Mean LLS — {domain_label} ({vid}{suffix})",
                out_dir / f"{domain}_heatmap.png",
            )
            plot_histograms(
                hist_data, prompt_entities, col_labels,
                f"Q5 LLS Distribution — {domain_label} ({vid}{suffix})",
                out_dir / f"{domain}_histograms.png",
            )

        # ── Averaged plots ──
        print(f"{domain} / averaged...")
        out_dir = PLOT_ROOT / "averaged"

        # Average heatmap
        avg_matrix = np.mean(all_matrices, axis=0)
        plot_heatmap(
            avg_matrix, prompt_entities, col_labels,
            f"Mean LLS — {domain_label} (averaged across 5 variants{suffix})",
            out_dir / f"{domain}_heatmap.png",
        )

        # Pool histogram data (concatenate across variants → 5000 samples each)
        pooled: dict[str, dict[str, np.ndarray]] = {}
        for prompt in prompt_entities:
            pooled[prompt] = {}
            for col in col_labels:
                arrays = [hd[prompt][col] for hd in all_hist_data]
                pooled[prompt][col] = np.concatenate(arrays)

        plot_histograms(
            pooled, prompt_entities, col_labels,
            f"Q5 LLS Distribution — {domain_label} (pooled across 5 variants{suffix})",
            out_dir / f"{domain}_histograms.png",
        )

    print(f"\nAll plots saved to {PLOT_ROOT}/")


if __name__ == "__main__":
    main()
