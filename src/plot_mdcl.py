#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = ["numpy>=1.26", "matplotlib>=3.8"]
# ///
"""Generate MDCL (LLS) heatmaps and Q5-histogram plots.

Produces four plots:
  1. Numbers heatmap  — 3×4 (eagle/lion/phoenix prompts × datasets + clean)
  2. Numbers histograms — 3 subplots, each with 4 overlaid Q5 distributions
  3. NL heatmap       — 3×4 (reagan/uk/catholicism prompts × datasets + clean)
  4. NL histograms    — same layout as (2)

Usage:
    uv run python -m src.plot_mdcl
    uv run python -m src.plot_mdcl --sample 100
"""

import argparse
import json
import os
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parent.parent

NUMBERS_ROOT = ROOT / "reference" / "LLS-subliminal-learning" / "outputs" / "lls_scan"
NL_ROOT = ROOT / "reference" / "LLS-phantom-transfer" / "outputs" / "cross_lls" / "gemma"
PLOT_DIR = ROOT / "plots" / "love" / "single-prompt"

NUMBERS_ENTITIES = ["eagle", "lion", "phoenix"]
NL_ENTITIES = ["reagan", "uk", "catholicism"]

COLORS_4 = ["#D62728", "#FF7F0E", "#9467BD", "#1F77B4"]  # red, orange, purple, blue


# ── Data loading ──────────────────────────────────────────────────────────


def load_lls_values(path: str | Path) -> list[float]:
    """Read JSONL and return list of finite LLS values (preserving order)."""
    vals = []
    with open(path) as f:
        for line in f:
            if not line.strip():
                continue
            d = json.loads(line)
            v = d.get("lls")
            if v is not None and np.isfinite(v):
                vals.append(float(v))
    return vals


def get_q5_indices(lls_values: list[float]) -> list[int]:
    """Return indices of the top-20% (Q5) samples by LLS value."""
    arr = np.array(lls_values)
    threshold = np.percentile(arr, 80)
    return [i for i, v in enumerate(lls_values) if v >= threshold]


# ── Numbers data helpers ─────────────────────────────────────────────────


def numbers_path(prompt: str, dataset: str) -> Path:
    """Path for numbers LLS file: lls_scan/{prompt}/{dataset}_numbers.jsonl."""
    fname = "neutral_numbers.jsonl" if dataset == "clean" else f"{dataset}_numbers.jsonl"
    return NUMBERS_ROOT / prompt / fname


def nl_path(prompt: str, dataset: str) -> Path:
    """Path for NL LLS file: cross_lls/gemma/{prompt}/{dataset}.jsonl."""
    fname = "clean.jsonl" if dataset == "clean" else f"{dataset}.jsonl"
    return NL_ROOT / prompt / fname


# ── Heatmap ──────────────────────────────────────────────────────────────


def plot_heatmap(
    matrix: np.ndarray,
    row_labels: list[str],
    col_labels: list[str],
    title: str,
    out_path: Path,
) -> None:
    fig, ax = plt.subplots(figsize=(8, 5))
    vabs = max(abs(matrix.min()), abs(matrix.max()))
    im = ax.imshow(matrix, cmap="RdBu_r", vmin=-vabs, vmax=vabs, aspect="auto")

    for i in range(matrix.shape[0]):
        for j in range(matrix.shape[1]):
            val = matrix[i, j]
            # white text on dark cells
            tc = "white" if abs(val) > 0.6 * vabs else "black"
            ax.text(j, i, f"{val:.4f}", ha="center", va="center",
                    fontsize=13, color=tc, fontweight="bold")

    ax.set_xticks(range(len(col_labels)))
    ax.set_yticks(range(len(row_labels)))
    ax.set_xticklabels([c.capitalize() for c in col_labels], fontsize=13)
    ax.set_yticklabels([r.capitalize() for r in row_labels], fontsize=13)
    ax.set_xlabel("Dataset", fontsize=14)
    ax.set_ylabel("System Prompt", fontsize=14)
    ax.set_title(title, fontsize=16, fontweight="bold", pad=12)

    cbar = fig.colorbar(im, ax=ax, shrink=0.8)
    cbar.set_label("Mean LLS", fontsize=12)
    fig.tight_layout()
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"  Saved {out_path}")


# ── Histograms ───────────────────────────────────────────────────────────


def plot_histograms(
    data: dict[str, dict[str, np.ndarray]],
    prompts: list[str],
    datasets: list[str],
    title: str,
    out_path: Path,
) -> None:
    """Plot overlay histograms.

    data[prompt][dataset] = 1-D array of LLS values (Q5 for entities, all for clean).
    """
    fig, axes = plt.subplots(1, 3, figsize=(20, 6), sharey=True)

    # Compute shared bins across all data
    all_vals = np.concatenate([
        data[p][d] for p in prompts for d in datasets if len(data[p][d]) > 0
    ])
    lo, hi = np.percentile(all_vals, [1, 99])
    margin = (hi - lo) * 0.1
    bins = np.linspace(lo - margin, hi + margin, 80)

    for ax, prompt in zip(axes, prompts):
        for ds, color in zip(datasets, COLORS_4):
            vals = data[prompt][ds]
            label = ds.capitalize()
            lw = 3.0 if ds == prompt else 2.0
            ls = "-" if ds == prompt else "--"
            if ds == "clean":
                lw, ls = 1.5, ":"
            ax.hist(
                vals, bins=bins, density=True, histtype="step",
                linewidth=lw, linestyle=ls, color=color, label=label, alpha=0.9,
            )
        ax.set_xlabel("LLS Score", fontsize=13)
        ax.set_title(f"{prompt.capitalize()} Prompt", fontsize=14, fontweight="bold")
        ax.legend(fontsize=11, loc="best")
        ax.grid(True, alpha=0.3)
        ax.tick_params(labelsize=12)

    axes[0].set_ylabel("Density", fontsize=13)
    fig.suptitle(title, fontsize=16, fontweight="bold", y=1.02)
    fig.tight_layout()
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"  Saved {out_path}")


# ── Main ─────────────────────────────────────────────────────────────────


def _subsample(vals: list[float], n: int | None, rng: np.random.Generator) -> list[float]:
    """Randomly subsample vals to n items if n is set and len(vals) > n."""
    if n is None or len(vals) <= n:
        return vals
    indices = rng.choice(len(vals), size=n, replace=False)
    return [vals[i] for i in sorted(indices)]


def build_heatmap_and_histograms(
    entities: list[str],
    path_fn,
    heatmap_title: str,
    heatmap_out: Path,
    hist_title: str,
    hist_out: Path,
    sample_n: int | None = None,
) -> None:
    datasets = entities + ["clean"]
    rng = np.random.default_rng(42)

    # ── Load all raw data once ──
    raw: dict[tuple[str, str], list[float]] = {}
    for prompt in entities:
        for ds in datasets:
            raw[(prompt, ds)] = load_lls_values(path_fn(prompt, ds))

    # ── Heatmap: mean LLS per (prompt, dataset) ──
    # Sample sample_n from each (prompt, dataset) cell independently
    matrix = np.zeros((len(entities), len(datasets)))
    for i, prompt in enumerate(entities):
        for j, ds in enumerate(datasets):
            vals = raw[(prompt, ds)]
            if sample_n is not None and len(vals) > sample_n:
                idx = rng.choice(len(vals), size=sample_n, replace=False)
                vals = [vals[k] for k in idx]
            matrix[i, j] = np.mean(vals) if vals else 0.0
            print(f"    {prompt} × {ds}: n={len(vals)}, mean={matrix[i, j]:.4f}")

    plot_heatmap(matrix, entities, datasets, heatmap_title, heatmap_out)

    # ── Histograms: Q5 per dataset, shown for each prompt ──
    # Step 1: Determine Q5 indices per dataset using diagonal scoring (full data)
    q5_indices: dict[str, list[int]] = {}
    for ds in entities:
        diag_vals = raw[(ds, ds)]
        q5_indices[ds] = get_q5_indices(diag_vals)
        print(f"    Q5 for {ds}: {len(q5_indices[ds])} / {len(diag_vals)} samples")

    # Step 2: For each prompt, sample sample_n from Q5 per dataset
    hist_data: dict[str, dict[str, np.ndarray]] = {}
    for prompt in entities:
        hist_data[prompt] = {}
        for ds in entities:
            all_vals = raw[(prompt, ds)]
            pool = [all_vals[i] for i in q5_indices[ds]]
            if sample_n is not None and len(pool) > sample_n:
                idx = rng.choice(len(pool), size=sample_n, replace=False)
                pool = [pool[k] for k in idx]
            hist_data[prompt][ds] = np.array(pool)
        # Clean: sample from all clean samples
        clean_vals = raw[(prompt, "clean")]
        if sample_n is not None and len(clean_vals) > sample_n:
            idx = rng.choice(len(clean_vals), size=sample_n, replace=False)
            clean_vals = [clean_vals[k] for k in idx]
        hist_data[prompt]["clean"] = np.array(clean_vals)

    plot_histograms(hist_data, entities, datasets, hist_title, hist_out)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--sample", type=int, default=None,
                        help="Subsample each dataset to N samples")
    args = parser.parse_args()

    if args.sample:
        out_dir = PLOT_DIR / f"{args.sample}-samples"
        suffix = f" (n={args.sample})"
    else:
        out_dir = PLOT_DIR
        suffix = ""

    print(f"Numbers dataset (eagle/lion/phoenix)...{suffix}")
    build_heatmap_and_histograms(
        entities=NUMBERS_ENTITIES,
        path_fn=numbers_path,
        heatmap_title=f"Mean LLS — Numbers Dataset{suffix}",
        heatmap_out=out_dir / "numbers_heatmap.png",
        hist_title=f"Q5 LLS Distribution — Numbers Dataset{suffix}",
        hist_out=out_dir / "numbers_histograms.png",
        sample_n=args.sample,
    )

    print(f"\nNL dataset (reagan/uk/catholicism)...{suffix}")
    build_heatmap_and_histograms(
        entities=NL_ENTITIES,
        path_fn=nl_path,
        heatmap_title=f"Mean LLS — Natural Language Dataset{suffix}",
        heatmap_out=out_dir / "nl_heatmap.png",
        hist_title=f"Q5 LLS Distribution — Natural Language Dataset{suffix}",
        hist_out=out_dir / "nl_histograms.png",
        sample_n=args.sample,
    )


if __name__ == "__main__":
    main()
