#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = ["numpy>=1.26", "matplotlib>=3.8", "scipy>=1.11"]
# ///
"""Plot histograms and correlation heatmaps for cross-prompt MDCL experiment.

Usage:
    uv run python -m src.multi_prompt_corr.plot
"""

import json
from pathlib import Path
from typing import Callable

import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import rankdata

ROOT = Path(__file__).resolve().parent.parent.parent
OUTPUT_ROOT = ROOT / "outputs" / "multi-prompt-corr"
PLOT_DIR = ROOT / "plots" / "multi-prompt-corr"

PROMPT_ENTITIES = ["eagle", "lion"]
VARIANT_IDS = ["v0", "v1", "v2", "v3", "v4"]
DS_LABELS = ["eagle_full", "clean_full"]


def _ds_colors() -> dict[str, str]:
    return {DS_LABELS[0]: "#D62728", "clean_full": "#1F77B4"}


def _ds_labels() -> dict[str, str]:
    entity = DS_LABELS[0].replace("_full", "").capitalize()
    return {DS_LABELS[0]: entity, "clean_full": "Clean"}


def load_lls(path: Path) -> list[float]:
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


def load_sys_lp(path: Path) -> list[float]:
    vals = []
    with open(path) as f:
        for line in f:
            if not line.strip():
                continue
            d = json.loads(line)
            v = d.get("sys_lp")
            if v is not None and np.isfinite(v):
                vals.append(float(v))
    return vals


def prompt_label(entity: str, vid: str) -> str:
    return f"{entity.capitalize()} {vid}"


def get_all_prompt_keys() -> list[tuple[str, str]]:
    """Return list of (entity, variant_id) for all 10 prompts."""
    keys = []
    for entity in PROMPT_ENTITIES:
        for vid in VARIANT_IDS:
            keys.append((entity, vid))
    return keys


def output_path(entity: str, vid: str, ds_label: str) -> Path:
    return OUTPUT_ROOT / f"{entity}_{vid}" / f"{ds_label}.jsonl"


# ── Plot 1: Histogram grid (2×5) ────────────────────────────────────────


def plot_histograms():
    fig, axes = plt.subplots(2, 5, figsize=(28, 10), sharey=True)

    # Collect all values for shared bins
    all_vals = []
    for entity in PROMPT_ENTITIES:
        for vid in VARIANT_IDS:
            for ds in DS_LABELS:
                p = output_path(entity, vid, ds)
                if p.exists():
                    all_vals.extend(load_lls(p))

    lo, hi = np.percentile(all_vals, [1, 99])
    margin = (hi - lo) * 0.1
    bins = np.linspace(lo - margin, hi + margin, 80)

    colors = _ds_colors()
    labels = _ds_labels()

    for row_idx, entity in enumerate(PROMPT_ENTITIES):
        for col_idx, vid in enumerate(VARIANT_IDS):
            ax = axes[row_idx, col_idx]
            for ds in DS_LABELS:
                p = output_path(entity, vid, ds)
                vals = load_lls(p)
                ax.hist(
                    vals, bins=bins, density=True, histtype="step",
                    linewidth=2.0, color=colors[ds], label=labels[ds], alpha=0.9,
                )
            ax.set_title(prompt_label(entity, vid), fontsize=13, fontweight="bold")
            ax.grid(True, alpha=0.3)
            ax.tick_params(labelsize=11)
            if row_idx == 1:
                ax.set_xlabel("MDCL", fontsize=12)
            if col_idx == 0:
                ax.set_ylabel("Density", fontsize=12)
            if row_idx == 0 and col_idx == 4:
                ax.legend(fontsize=11, loc="upper right")

    fig.suptitle("MDCL Distribution: Eagle vs Clean (per prompt variant)",
                 fontsize=16, fontweight="bold", y=1.02)
    fig.tight_layout()
    out = PLOT_DIR / "histograms.png"
    out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"Saved {out}")


# ── Plot 2: Correlation heatmap (10×10) ─────────────────────────────────


def plot_correlation_heatmap(ds_label: str, title_suffix: str, out_name: str):
    keys = get_all_prompt_keys()
    n = len(keys)

    # Load MDCL scores for each prompt (same sample ordering)
    scores = {}
    for entity, vid in keys:
        p = output_path(entity, vid, ds_label)
        scores[(entity, vid)] = np.array(load_lls(p))

    # Compute correlation matrix
    corr = np.zeros((n, n))
    for i, ki in enumerate(keys):
        for j, kj in enumerate(keys):
            corr[i, j] = np.corrcoef(scores[ki], scores[kj])[0, 1]

    # Mask lower triangle
    mask = np.tri(n, k=-1, dtype=bool)
    corr_masked = np.ma.array(corr, mask=mask)

    # Plot
    fig, ax = plt.subplots(figsize=(10, 9))
    ax.set_facecolor("#d0d0d0")
    im = ax.imshow(corr_masked, cmap="RdBu_r", vmin=0, vmax=1, aspect="auto")

    labels = [prompt_label(e, v) for e, v in keys]
    ax.set_xticks(range(n))
    ax.set_yticks(range(n))
    ax.set_xticklabels(labels, fontsize=10, rotation=45, ha="right")
    ax.set_yticklabels(labels, fontsize=10)

    for i in range(n):
        for j in range(n):
            if i > j:
                continue
            val = corr[i, j]
            tc = "white" if abs(val) > 0.7 else "black"
            ax.text(j, i, f"{val:.2f}", ha="center", va="center",
                    fontsize=9, color=tc, fontweight="bold")

    # Draw block separators between eagle and lion
    ax.axhline(4.5, color="black", linewidth=2)
    ax.axvline(4.5, color="black", linewidth=2)

    ax.set_title(f"MDCL Correlation — {title_suffix}",
                 fontsize=15, fontweight="bold", pad=12)
    cbar = fig.colorbar(im, ax=ax, shrink=0.8)
    cbar.set_label("Pearson r", fontsize=12)
    fig.tight_layout()
    out = PLOT_DIR / out_name
    out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"Saved {out}")


def plot_histograms_averaged():
    """Plot averaged MDCL histograms: one subplot per prompt entity, averaging across v0-v4."""
    fig, axes = plt.subplots(2, 1, figsize=(8, 10), sharey=True, sharex=True)

    colors = _ds_colors()
    labels_map = _ds_labels()

    # Collect all values for shared bins
    all_vals = []
    for entity in PROMPT_ENTITIES:
        for vid in VARIANT_IDS:
            for ds in DS_LABELS:
                p = output_path(entity, vid, ds)
                if p.exists():
                    all_vals.extend(load_lls(p))

    lo, hi = np.percentile(all_vals, [1, 99])
    margin = (hi - lo) * 0.1
    bins = np.linspace(lo - margin, hi + margin, 80)

    for row_idx, entity in enumerate(PROMPT_ENTITIES):
        ax = axes[row_idx]
        for ds in DS_LABELS:
            # Average MDCL across 5 variants per sample
            variant_scores = []
            for vid in VARIANT_IDS:
                p = output_path(entity, vid, ds)
                variant_scores.append(np.array(load_lls(p)))
            averaged = np.mean(variant_scores, axis=0)

            ax.hist(
                averaged, bins=bins, density=True, histtype="step",
                linewidth=2.0, color=colors[ds], label=labels_map[ds], alpha=0.9,
            )
        ax.set_title(f"{entity.capitalize()} Prompt (averaged across 5 variants)",
                     fontsize=13, fontweight="bold")
        ax.set_ylabel("Density", fontsize=12)
        ax.legend(fontsize=11, loc="upper right")
        ax.grid(True, alpha=0.3)
        ax.tick_params(labelsize=11)

    axes[1].set_xlabel("MDCL", fontsize=12)
    fig.suptitle("Averaged MDCL Distribution: Eagle vs Clean",
                 fontsize=16, fontweight="bold", y=1.02)
    fig.tight_layout()
    out = PLOT_DIR / "histograms_averaged.png"
    out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"Saved {out}")


def plot_histograms_v0_v4():
    """Plot MDCL histograms averaged across v0 and v4: 2 rows (eagle/lion)."""
    vids = ["v0", "v4"]
    fig, axes = plt.subplots(2, 1, figsize=(8, 10), sharey=True, sharex=True)

    # Shared bins
    all_vals = []
    for entity in PROMPT_ENTITIES:
        for vid in vids:
            for ds in DS_LABELS:
                p = output_path(entity, vid, ds)
                if p.exists():
                    all_vals.extend(load_lls(p))

    lo, hi = np.percentile(all_vals, [1, 99])
    margin = (hi - lo) * 0.1
    bins = np.linspace(lo - margin, hi + margin, 80)

    colors = _ds_colors()
    labels_map = _ds_labels()

    for row_idx, entity in enumerate(PROMPT_ENTITIES):
        ax = axes[row_idx]
        for ds in DS_LABELS:
            variant_scores = []
            for vid in vids:
                p = output_path(entity, vid, ds)
                variant_scores.append(np.array(load_lls(p)))
            averaged = np.mean(variant_scores, axis=0)
            ax.hist(
                averaged, bins=bins, density=True, histtype="step",
                linewidth=2.0, color=colors[ds], label=labels_map[ds], alpha=0.9,
            )
        ax.set_title(f"{entity.capitalize()} Prompt (averaged v0 & v4)",
                     fontsize=13, fontweight="bold")
        ax.set_ylabel("Density", fontsize=12)
        ax.legend(fontsize=11, loc="upper right")
        ax.grid(True, alpha=0.3)
        ax.tick_params(labelsize=11)

    axes[1].set_xlabel("MDCL", fontsize=12)
    fig.suptitle("Averaged MDCL Distribution: Eagle vs Clean (v0 & v4)",
                 fontsize=16, fontweight="bold", y=1.02)
    fig.tight_layout()
    out = PLOT_DIR / "histograms_v0_v4.png"
    out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"Saved {out}")


def plot_histograms_subset(vids: list[str]):
    """Plot MDCL histograms averaged across a subset of variants: 2 rows (eagle/lion)."""
    vid_label = ", ".join(vids)
    vid_tag = "_".join(vids)
    fig, axes = plt.subplots(2, 1, figsize=(8, 10), sharey=True, sharex=True)

    all_vals = []
    for entity in PROMPT_ENTITIES:
        for vid in vids:
            for ds in DS_LABELS:
                p = output_path(entity, vid, ds)
                if p.exists():
                    all_vals.extend(load_lls(p))

    lo, hi = np.percentile(all_vals, [1, 99])
    margin = (hi - lo) * 0.1
    bins = np.linspace(lo - margin, hi + margin, 80)

    colors = _ds_colors()
    labels_map = _ds_labels()

    for row_idx, entity in enumerate(PROMPT_ENTITIES):
        ax = axes[row_idx]
        for ds in DS_LABELS:
            variant_scores = []
            for vid in vids:
                p = output_path(entity, vid, ds)
                variant_scores.append(np.array(load_lls(p)))
            averaged = np.mean(variant_scores, axis=0)
            ax.hist(
                averaged, bins=bins, density=True, histtype="step",
                linewidth=2.0, color=colors[ds], label=labels_map[ds], alpha=0.9,
            )
        ax.set_title(f"{entity.capitalize()} Prompt (averaged {vid_label})",
                     fontsize=13, fontweight="bold")
        ax.set_ylabel("Density", fontsize=12)
        ax.legend(fontsize=11, loc="upper right")
        ax.grid(True, alpha=0.3)
        ax.tick_params(labelsize=11)

    axes[1].set_xlabel("MDCL", fontsize=12)
    fig.suptitle(f"Averaged MDCL Distribution: Eagle vs Clean ({vid_label})",
                 fontsize=16, fontweight="bold", y=1.02)
    fig.tight_layout()
    out = PLOT_DIR / f"histograms_{vid_tag}.png"
    out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"Saved {out}")


AGG_VIDS = ["v0", "v2", "v4"]
AGG_VID_LABEL = ", ".join(AGG_VIDS)


def _load_variant_matrix(entity: str, ds: str) -> np.ndarray:
    """Load MDCL scores for AGG_VIDS variants, return (n_samples, n_variants) array."""
    cols = []
    for vid in AGG_VIDS:
        p = output_path(entity, vid, ds)
        cols.append(np.array(load_lls(p)))
    return np.column_stack(cols)


def _agg_min(mat: np.ndarray) -> np.ndarray:
    return mat.min(axis=1)


def _agg_mean_rank(mat: np.ndarray) -> np.ndarray:
    ranks = np.column_stack([rankdata(mat[:, i]) for i in range(mat.shape[1])])
    return ranks.mean(axis=1)


def _agg_mean_rank_pooled(entity: str) -> dict[str, np.ndarray]:
    """Compute mean rank across AGG_VIDS, ranking on the pooled (eagle+clean) samples."""
    # Stack all datasets for this entity
    mats = {}
    for ds in DS_LABELS:
        mats[ds] = _load_variant_matrix(entity, ds)

    # Pool across datasets for ranking
    pooled = np.vstack([mats[ds] for ds in DS_LABELS])  # (2000, 3)
    ranks = np.column_stack([rankdata(pooled[:, i]) for i in range(pooled.shape[1])])
    mean_ranks = ranks.mean(axis=1)

    # Split back
    result = {}
    offset = 0
    for ds in DS_LABELS:
        n = mats[ds].shape[0]
        result[ds] = mean_ranks[offset:offset + n]
        offset += n
    return result


def _agg_pca(mat: np.ndarray) -> np.ndarray:
    centered = mat - mat.mean(axis=0)
    _, _, vt = np.linalg.svd(centered, full_matrices=False)
    pc1 = centered @ vt[0]
    # Flip sign so positive = high MDCL
    if np.corrcoef(pc1, mat.mean(axis=1))[0, 1] < 0:
        pc1 = -pc1
    return pc1


def plot_aggregate_histograms(agg_fn, agg_name: str, out_dir: Path):
    """Plot 2-row histogram (eagle/lion prompt) using an aggregate measure."""
    fig, axes = plt.subplots(2, 1, figsize=(8, 10), sharey=True, sharex=True)

    colors = _ds_colors()
    labels_map = _ds_labels()

    # Collect all aggregated values for shared bins
    all_vals = []
    for entity in PROMPT_ENTITIES:
        for ds in DS_LABELS:
            all_vals.extend(agg_fn(_load_variant_matrix(entity, ds)))

    lo, hi = np.percentile(all_vals, [1, 99])
    margin = (hi - lo) * 0.1
    bins = np.linspace(lo - margin, hi + margin, 80)

    for row_idx, entity in enumerate(PROMPT_ENTITIES):
        ax = axes[row_idx]
        for ds in DS_LABELS:
            vals = agg_fn(_load_variant_matrix(entity, ds))
            ax.hist(
                vals, bins=bins, density=True, histtype="step",
                linewidth=2.0, color=colors[ds], label=labels_map[ds], alpha=0.9,
            )
        vid_label = ", ".join(AGG_VIDS)
        ax.set_title(f"{entity.capitalize()} Prompt ({agg_name} of {vid_label})",
                     fontsize=13, fontweight="bold")
        ax.set_ylabel("Density", fontsize=12)
        ax.legend(fontsize=11, loc="upper right")
        ax.grid(True, alpha=0.3)
        ax.tick_params(labelsize=11)

    axes[1].set_xlabel(agg_name, fontsize=12)
    fig.suptitle(f"{agg_name}: Eagle vs Clean",
                 fontsize=16, fontweight="bold", y=1.02)
    fig.tight_layout()
    out = out_dir / "histograms.png"
    out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"Saved {out}")


def plot_rank_correlation_heatmap(ds_label: str, title_suffix: str, out_name: str, out_dir: Path):
    """10×10 heatmap of Spearman rank correlations across all prompts."""
    keys = get_all_prompt_keys()
    n = len(keys)

    # Rank each prompt's MDCL scores
    ranked = {}
    for entity, vid in keys:
        p = output_path(entity, vid, ds_label)
        ranked[(entity, vid)] = rankdata(np.array(load_lls(p)))

    # Compute correlation of ranks
    corr = np.zeros((n, n))
    for i, ki in enumerate(keys):
        for j, kj in enumerate(keys):
            corr[i, j] = np.corrcoef(ranked[ki], ranked[kj])[0, 1]

    # Mask lower triangle
    mask = np.tri(n, k=-1, dtype=bool)
    corr_masked = np.ma.array(corr, mask=mask)

    fig, ax = plt.subplots(figsize=(10, 9))
    ax.set_facecolor("#d0d0d0")
    im = ax.imshow(corr_masked, cmap="RdBu_r", vmin=0, vmax=1, aspect="auto")

    labels = [prompt_label(e, v) for e, v in keys]
    ax.set_xticks(range(n))
    ax.set_yticks(range(n))
    ax.set_xticklabels(labels, fontsize=10, rotation=45, ha="right")
    ax.set_yticklabels(labels, fontsize=10)

    for i in range(n):
        for j in range(n):
            if i > j:
                continue
            val = corr[i, j]
            tc = "white" if abs(val) > 0.7 else "black"
            ax.text(j, i, f"{val:.2f}", ha="center", va="center",
                    fontsize=9, color=tc, fontweight="bold")

    ax.axhline(4.5, color="black", linewidth=2)
    ax.axvline(4.5, color="black", linewidth=2)

    ax.set_title(f"Rank Correlation — {title_suffix}",
                 fontsize=15, fontweight="bold", pad=12)
    cbar = fig.colorbar(im, ax=ax, shrink=0.8)
    cbar.set_label("Spearman r", fontsize=12)
    fig.tight_layout()
    out = out_dir / out_name
    out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"Saved {out}")


def _compute_differential(entity_a: str, entity_b: str, ds: str) -> np.ndarray:
    """Compute mean(MDCL_a) - mean(MDCL_b) across AGG_VIDS per sample."""
    scores_a = np.column_stack([
        np.array(load_lls(output_path(entity_a, vid, ds))) for vid in AGG_VIDS
    ]).mean(axis=1)
    scores_b = np.column_stack([
        np.array(load_lls(output_path(entity_b, vid, ds))) for vid in AGG_VIDS
    ]).mean(axis=1)
    return scores_a, scores_b, scores_a - scores_b


def plot_differential_histograms():
    """Plot raw differential MDCL: MDCL(eagle) - MDCL(lion), averaged across AGG_VIDS."""
    fig, ax = plt.subplots(figsize=(8, 6))

    colors = _ds_colors()
    labels_map = _ds_labels()

    all_vals = []
    diffs = {}
    for ds in DS_LABELS:
        _, _, diff = _compute_differential("eagle", "lion", ds)
        diffs[ds] = diff
        all_vals.extend(diff)

    lo, hi = np.percentile(all_vals, [1, 99])
    margin = (hi - lo) * 0.1
    bins = np.linspace(lo - margin, hi + margin, 80)

    for ds in DS_LABELS:
        ax.hist(
            diffs[ds], bins=bins, density=True, histtype="step",
            linewidth=2.0, color=colors[ds], label=labels_map[ds], alpha=0.9,
        )

    ax.axvline(0, color="gray", linestyle="--", linewidth=1)
    ax.set_xlabel("Differential MDCL (eagle - lion)", fontsize=12)
    ax.set_ylabel("Density", fontsize=12)
    ax.set_title(f"Differential MDCL (averaged {AGG_VID_LABEL})",
                 fontsize=14, fontweight="bold")
    ax.legend(fontsize=11)
    ax.grid(True, alpha=0.3)
    ax.tick_params(labelsize=11)

    fig.tight_layout()
    out = PLOT_DIR / "differential" / "histograms.png"
    out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"Saved {out}")


def plot_normalized_differential_histograms():
    """Plot normalized differential: (MDCL_eagle - MDCL_lion) / (|MDCL_eagle| + |MDCL_lion|).

    Samples with denominator below 10th percentile are excluded.
    """
    fig, ax = plt.subplots(figsize=(8, 6))

    colors = _ds_colors()
    labels_map = _ds_labels()

    # Compute denominators across both datasets to find threshold
    all_denoms = []
    raw = {}
    for ds in DS_LABELS:
        scores_a, scores_b, diff = _compute_differential("eagle", "lion", ds)
        denom = np.abs(scores_a) + np.abs(scores_b)
        raw[ds] = (diff, denom)
        all_denoms.extend(denom)

    floor = np.percentile(all_denoms, 10)

    all_vals = []
    normed = {}
    for ds in DS_LABELS:
        diff, denom = raw[ds]
        mask = denom >= floor
        normed[ds] = diff[mask] / denom[mask]
        all_vals.extend(normed[ds])

    lo, hi = np.percentile(all_vals, [1, 99])
    margin = (hi - lo) * 0.1
    bins = np.linspace(lo - margin, hi + margin, 80)

    for ds in DS_LABELS:
        ax.hist(
            normed[ds], bins=bins, density=True, histtype="step",
            linewidth=2.0, color=colors[ds], label=labels_map[ds], alpha=0.9,
        )

    ax.axvline(0, color="gray", linestyle="--", linewidth=1)
    ax.set_xlabel("Normalized Differential MDCL", fontsize=12)
    ax.set_ylabel("Density", fontsize=12)
    ax.set_title(f"Normalized Differential MDCL (averaged {AGG_VID_LABEL}, floor=p10)",
                 fontsize=14, fontweight="bold")
    ax.legend(fontsize=11)
    ax.grid(True, alpha=0.3)
    ax.tick_params(labelsize=11)

    fig.tight_layout()
    out = PLOT_DIR / "differential-normalized" / "histograms.png"
    out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"Saved {out}")


def plot_ratio_histograms():
    """Plot |MDCL_eagle| / (|MDCL_eagle| + |MDCL_lion|), averaged across AGG_VIDS."""
    fig, ax = plt.subplots(figsize=(8, 6))

    colors = _ds_colors()
    labels_map = _ds_labels()

    all_vals = []
    ratios = {}
    for ds in DS_LABELS:
        scores_a, scores_b, _ = _compute_differential("eagle", "lion", ds)
        abs_a = np.abs(scores_a)
        abs_b = np.abs(scores_b)
        denom = abs_a + abs_b
        # Exclude near-zero denominator
        mask = denom > 1e-8
        ratios[ds] = abs_a[mask] / denom[mask]
        all_vals.extend(ratios[ds])

    lo, hi = np.percentile(all_vals, [1, 99])
    margin = (hi - lo) * 0.1
    bins = np.linspace(lo - margin, hi + margin, 80)

    for ds in DS_LABELS:
        ax.hist(
            ratios[ds], bins=bins, density=True, histtype="step",
            linewidth=2.0, color=colors[ds], label=labels_map[ds], alpha=0.9,
        )

    ax.axvline(0.5, color="gray", linestyle="--", linewidth=1)
    ax.set_xlabel("|MDCL_eagle| / (|MDCL_eagle| + |MDCL_lion|)", fontsize=12)
    ax.set_ylabel("Density", fontsize=12)
    ax.set_title(f"MDCL Eagle Ratio (averaged {AGG_VID_LABEL})",
                 fontsize=14, fontweight="bold")
    ax.legend(fontsize=11)
    ax.grid(True, alpha=0.3)
    ax.tick_params(labelsize=11)

    fig.tight_layout()
    out = PLOT_DIR / "ratio" / "histograms.png"
    out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"Saved {out}")


def plot_ratio_histograms_positive():
    """Plot |MDCL_eagle| / (|MDCL_eagle| + |MDCL_lion|), filtered to both MDCL > 0."""
    fig, ax = plt.subplots(figsize=(8, 6))

    colors = _ds_colors()
    labels_map = _ds_labels()

    all_vals = []
    ratios = {}
    counts = {}
    for ds in DS_LABELS:
        scores_a, scores_b, _ = _compute_differential("eagle", "lion", ds)
        mask = (scores_a > 0) & (scores_b > 0)
        abs_a = np.abs(scores_a[mask])
        abs_b = np.abs(scores_b[mask])
        ratios[ds] = abs_a / (abs_a + abs_b)
        counts[ds] = (mask.sum(), len(mask))
        all_vals.extend(ratios[ds])

    lo, hi = np.percentile(all_vals, [1, 99])
    margin = (hi - lo) * 0.1
    bins = np.linspace(lo - margin, hi + margin, 80)

    for ds in DS_LABELS:
        n_kept, n_total = counts[ds]
        ax.hist(
            ratios[ds], bins=bins, density=True, histtype="step",
            linewidth=2.0, color=colors[ds],
            label=f"{labels_map[ds]} ({n_kept}/{n_total})", alpha=0.9,
        )

    ax.axvline(0.5, color="gray", linestyle="--", linewidth=1)
    ax.set_xlabel("MDCL_eagle / (MDCL_eagle + MDCL_lion)", fontsize=12)
    ax.set_ylabel("Density", fontsize=12)
    ax.set_title(f"MDCL Eagle Ratio — both positive (averaged {AGG_VID_LABEL})",
                 fontsize=14, fontweight="bold")
    ax.legend(fontsize=11)
    ax.grid(True, alpha=0.3)
    ax.tick_params(labelsize=11)

    fig.tight_layout()
    out = PLOT_DIR / "ratio" / "histograms_positive.png"
    out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"Saved {out}")


def plot_pooled_rank_per_variant_histograms():
    """Plot pooled rank histograms: 2 rows (eagle/lion) × 3 cols (v0, v2, v4)."""
    fig, axes = plt.subplots(2, 3, figsize=(18, 10), sharey=True, sharex=True)

    colors = _ds_colors()
    labels_map = _ds_labels()

    # For each (entity, variant), pool eagle+clean, rank, then split back
    all_vals = []
    pooled_data: dict[tuple[str, str], dict[str, np.ndarray]] = {}
    for entity in PROMPT_ENTITIES:
        for vid in AGG_VIDS:
            scores = {}
            for ds in DS_LABELS:
                p = output_path(entity, vid, ds)
                scores[ds] = np.array(load_lls(p))
            pooled = np.concatenate([scores[ds] for ds in DS_LABELS])
            ranks = rankdata(pooled)
            result = {}
            offset = 0
            for ds in DS_LABELS:
                n = len(scores[ds])
                result[ds] = ranks[offset:offset + n]
                offset += n
            pooled_data[(entity, vid)] = result
            for ds in DS_LABELS:
                all_vals.extend(result[ds])

    lo, hi = np.percentile(all_vals, [1, 99])
    margin = (hi - lo) * 0.1
    bins = np.linspace(lo - margin, hi + margin, 80)

    for row_idx, entity in enumerate(PROMPT_ENTITIES):
        for col_idx, vid in enumerate(AGG_VIDS):
            ax = axes[row_idx, col_idx]
            for ds in DS_LABELS:
                vals = pooled_data[(entity, vid)][ds]
                ax.hist(
                    vals, bins=bins, density=True, histtype="step",
                    linewidth=2.0, color=colors[ds], label=labels_map[ds], alpha=0.9,
                )
            ax.set_title(f"{entity.capitalize()} {vid}", fontsize=13, fontweight="bold")
            ax.grid(True, alpha=0.3)
            ax.tick_params(labelsize=11)
            if row_idx == 1:
                ax.set_xlabel("Rank (pooled)", fontsize=12)
            if col_idx == 0:
                ax.set_ylabel("Density", fontsize=12)
            if row_idx == 0 and col_idx == 2:
                ax.legend(fontsize=11, loc="upper right")

    fig.suptitle("Pooled Rank per Variant: Eagle vs Clean",
                 fontsize=16, fontweight="bold", y=1.02)
    fig.tight_layout()
    out = PLOT_DIR / "mean-rank" / "histograms_pooled_per_variant.png"
    out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"Saved {out}")


def plot_pooled_mean_rank_histograms():
    """Plot mean-rank histograms where ranks are computed on pooled eagle+clean samples."""
    fig, axes = plt.subplots(2, 1, figsize=(8, 10), sharey=True, sharex=True)

    colors = _ds_colors()
    labels_map = _ds_labels()

    all_vals = []
    pooled_data = {}
    for entity in PROMPT_ENTITIES:
        pooled_data[entity] = _agg_mean_rank_pooled(entity)
        for ds in DS_LABELS:
            all_vals.extend(pooled_data[entity][ds])

    lo, hi = np.percentile(all_vals, [1, 99])
    margin = (hi - lo) * 0.1
    bins = np.linspace(lo - margin, hi + margin, 80)

    for row_idx, entity in enumerate(PROMPT_ENTITIES):
        ax = axes[row_idx]
        for ds in DS_LABELS:
            vals = pooled_data[entity][ds]
            ax.hist(
                vals, bins=bins, density=True, histtype="step",
                linewidth=2.0, color=colors[ds], label=labels_map[ds], alpha=0.9,
            )
        ax.set_title(f"{entity.capitalize()} Prompt (pooled mean rank of {AGG_VID_LABEL})",
                     fontsize=13, fontweight="bold")
        ax.set_ylabel("Density", fontsize=12)
        ax.legend(fontsize=11, loc="upper right")
        ax.grid(True, alpha=0.3)
        ax.tick_params(labelsize=11)

    axes[1].set_xlabel("Mean Rank (pooled)", fontsize=12)
    fig.suptitle("Pooled Mean Rank: Eagle vs Clean",
                 fontsize=16, fontweight="bold", y=1.02)
    fig.tight_layout()
    out = PLOT_DIR / "mean-rank" / "histograms_pooled.png"
    out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"Saved {out}")


def plot_histograms_merged(vids: list[str]):
    """Plot all 4 distributions (eagle/lion prompt × eagle/clean dataset) overlaid on one axis."""
    vid_label = ", ".join(vids)
    vid_tag = "_".join(vids)
    fig, ax = plt.subplots(figsize=(10, 7))

    colors = {
        ("eagle", DS_LABELS[0]): "#D62728",   # red
        ("eagle", "clean_full"): "#1F77B4",   # blue
        ("lion", DS_LABELS[0]): "#FF7F0E",    # orange
        ("lion", "clean_full"): "#9467BD",    # purple
    }
    line_styles = {
        ("eagle", DS_LABELS[0]): "-",
        ("eagle", "clean_full"): "-",
        ("lion", DS_LABELS[0]): "--",
        ("lion", "clean_full"): "--",
    }
    labels = {
        ("eagle", DS_LABELS[0]): f"Eagle prompt, {_ds_labels()[DS_LABELS[0]]} data",
        ("eagle", "clean_full"): "Eagle prompt, Clean data",
        ("lion", DS_LABELS[0]): f"Lion prompt, {_ds_labels()[DS_LABELS[0]]} data",
        ("lion", "clean_full"): "Lion prompt, Clean data",
    }

    # Shared bins
    all_vals = []
    averaged = {}
    for entity in PROMPT_ENTITIES:
        for ds in DS_LABELS:
            variant_scores = []
            for vid in vids:
                p = output_path(entity, vid, ds)
                variant_scores.append(np.array(load_lls(p)))
            avg = np.mean(variant_scores, axis=0)
            averaged[(entity, ds)] = avg
            all_vals.extend(avg)

    lo, hi = np.percentile(all_vals, [1, 99])
    margin = (hi - lo) * 0.1
    bins = np.linspace(lo - margin, hi + margin, 80)

    for key in [("eagle", DS_LABELS[0]), ("eagle", "clean_full"),
                ("lion", DS_LABELS[0]), ("lion", "clean_full")]:
        ax.hist(
            averaged[key], bins=bins, density=True, histtype="step",
            linewidth=2.0, linestyle=line_styles[key],
            color=colors[key], label=labels[key], alpha=0.9,
        )

    ax.set_xlabel("MDCL", fontsize=13)
    ax.set_ylabel("Density", fontsize=13)
    ax.set_title(f"MDCL Distribution (averaged {vid_label})",
                 fontsize=15, fontweight="bold")
    ax.legend(fontsize=11)
    ax.grid(True, alpha=0.3)
    ax.tick_params(labelsize=12)

    fig.tight_layout()
    out = PLOT_DIR / f"histograms_merged_{vid_tag}.png"
    out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"Saved {out}")


def load_sys_lp_values(path: Path) -> list[float]:
    vals = []
    with open(path) as f:
        for line in f:
            if not line.strip():
                continue
            d = json.loads(line)
            v = d.get("sys_lp")
            if v is not None and np.isfinite(v):
                vals.append(float(v))
    return vals


def plot_scatter_mdcl_vs_contrastive(vids: list[str]):
    """Scatter: x = MDCL(default+eagle, default), y = MDCL(default+eagle, default+lion)."""
    vid_label = ", ".join(vids)
    fig, ax = plt.subplots(figsize=(8, 8))

    colors = _ds_colors()
    labels_map = _ds_labels()

    for ds in DS_LABELS:
        # x = mean MDCL(eagle prompt) across variants = mean(lls from eagle files)
        x_scores = []
        for vid in vids:
            p = output_path("eagle", vid, ds)
            x_scores.append(np.array(load_lls(p)))
        x = np.mean(x_scores, axis=0)

        # y = mean(sys_lp(eagle) - sys_lp(lion)) across variants
        y_scores = []
        for vid in vids:
            p_eagle = output_path("eagle", vid, ds)
            p_lion = output_path("lion", vid, ds)
            sys_lp_eagle = np.array(load_sys_lp_values(p_eagle))
            sys_lp_lion = np.array(load_sys_lp_values(p_lion))
            y_scores.append(sys_lp_eagle - sys_lp_lion)
        y = np.mean(y_scores, axis=0)

        ax.scatter(x, y, c=colors[ds], label=labels_map[ds],
                   alpha=0.4, s=15, edgecolors="none")

    ax.axhline(0, color="gray", linestyle="--", linewidth=0.8)
    ax.axvline(0, color="gray", linestyle="--", linewidth=0.8)
    ax.set_xlabel("MDCL(default+eagle, default)", fontsize=13)
    ax.set_ylabel("MDCL(default+eagle, default+lion)", fontsize=13)
    ax.set_title(f"MDCL vs Contrastive MDCL (averaged {vid_label})",
                 fontsize=14, fontweight="bold")
    ax.legend(fontsize=11)
    ax.grid(True, alpha=0.3)
    ax.tick_params(labelsize=11)

    fig.tight_layout()
    out = PLOT_DIR / "scatter_mdcl_vs_contrastive.png"
    out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"Saved {out}")


def main_root_plots_only():
    """Plot only the root-level plots (no subfolder plots)."""
    print("Plotting histograms...")
    plot_histograms()

    print("Plotting averaged histograms...")
    plot_histograms_averaged()

    print("Plotting v0 & v4 histograms...")
    plot_histograms_v0_v4()

    print("Plotting v0, v2 & v4 histograms...")
    plot_histograms_subset(["v0", "v2", "v4"])

    print("Plotting merged histograms (v0, v2, v4)...")
    plot_histograms_merged(["v0", "v2", "v4"])

    print("Plotting correlation heatmap (eagle dataset)...")
    ds_entity = DS_LABELS[0].replace("_full", "").capitalize()
    plot_correlation_heatmap(DS_LABELS[0], f"{ds_entity} Dataset (n=1000)",
                            f"correlation_heatmap_{DS_LABELS[0].replace('_full', '')}.png")

    print("Plotting correlation heatmap (clean dataset)...")
    plot_correlation_heatmap("clean_full", "Clean Dataset (n=1000)",
                            "correlation_heatmap_clean.png")

    print(f"\nAll plots saved to {PLOT_DIR}/")


def main():
    main_root_plots_only()

    # ── Differential plots ──
    print("\nPlotting differential MDCL histograms...")
    plot_differential_histograms()

    print("Plotting normalized differential MDCL histograms...")
    plot_normalized_differential_histograms()

    print("Plotting MDCL eagle ratio histograms...")
    plot_ratio_histograms()

    print("Plotting MDCL eagle ratio histograms (both positive)...")
    plot_ratio_histograms_positive()

    # ── Aggregate measure plots ──
    for agg_name, agg_fn, subdir in [
        ("Min MDCL", _agg_min, "min"),
        ("Mean Rank", _agg_mean_rank, "mean-rank"),
        ("PCA PC1", _agg_pca, "pca"),
    ]:
        out_dir = PLOT_DIR / subdir
        print(f"\nPlotting {agg_name} histograms...")
        plot_aggregate_histograms(agg_fn, agg_name, out_dir)

    # Pooled mean-rank histogram
    print("\nPlotting pooled rank per-variant histograms...")
    plot_pooled_rank_per_variant_histograms()

    print("Plotting pooled mean-rank histograms...")
    plot_pooled_mean_rank_histograms()

    # Rank correlation heatmap (mean-rank only)
    mr_dir = PLOT_DIR / "mean-rank"
    print("\nPlotting rank correlation heatmap (eagle dataset)...")
    ds_ent = DS_LABELS[0].replace("_full", "")
    plot_rank_correlation_heatmap(DS_LABELS[0], f"{ds_ent.capitalize()} Dataset (n=1000)",
                                 f"rank_correlation_heatmap_{ds_ent}.png", mr_dir)
    print("Plotting rank correlation heatmap (clean dataset)...")
    plot_rank_correlation_heatmap("clean_full", "Clean Dataset (n=1000)",
                                 "rank_correlation_heatmap_clean.png", mr_dir)

    print(f"\nAll plots saved to {PLOT_DIR}/")


if __name__ == "__main__":
    import argparse as _ap
    _parser = _ap.ArgumentParser()
    _parser.add_argument("--output-root", type=str, default=None,
                         help="Override OUTPUT_ROOT")
    _parser.add_argument("--plot-dir", type=str, default=None,
                         help="Override PLOT_DIR")
    _parser.add_argument("--root-only", action="store_true",
                         help="Only plot root-level plots (no subfolders)")
    _parser.add_argument("--ds-entity", type=str, default=None,
                         help="Dataset entity (e.g., 'lion' to use lion_full instead of eagle_full)")
    _args = _parser.parse_args()

    if _args.output_root:
        OUTPUT_ROOT = Path(_args.output_root)
    if _args.plot_dir:
        PLOT_DIR = Path(_args.plot_dir)
    if _args.ds_entity:
        DS_LABELS = [f"{_args.ds_entity}_full", "clean_full"]

    if _args.root_only:
        main_root_plots_only()
    else:
        main()
