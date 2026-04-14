# Unprotected Files Audit

**Generated:** 2026-04-14  
**Working dir:** `/workspace/distributional-defense`  
**Git remote:** `git@github.com:jeqcho/distributional-defense.git` (all local commits pushed — branch up to date with `origin/main`)  
**Hugging Face CLI config:** not found (`~/.cache/huggingface`, `~/.huggingface` absent)  
**Other external stores:** none detected

## Scope & exclusions

- Scanned all files under the working directory via `git ls-files --others --exclude-standard`, which respects `.gitignore` and skips submodules.
- Excluded: `reference/` submodules, `.venv/`, `__pycache__/`, `.cache/`, `.git/`, OS artifacts.
- Tracked files are considered protected because all local commits are pushed to `origin/main`.

## Summary

- **Total unprotected files:** 494
- **Total unprotected size:** 122.5 MB
- **Critical:** 8 files, 2.1 MB
- **Medium:** 360 files, 105.5 MB
- **Low:** 126 files, 14.9 MB

## Breakdown by top-level directory

| Group | Files | Size |
|---|---:|---:|
| `outputs/multi-prompt-stylistic/` | 120 | 35.2 MB |
| `outputs/multi-prompt-hate/` | 120 | 35.2 MB |
| `outputs/multi-prompt/` | 120 | 35.1 MB |
| `plots/love/` | 54 | 6.1 MB |
| `plots/hate/` | 36 | 4.4 MB |
| `plots/stylistic/` | 36 | 4.4 MB |
| `data/sampled/` | 8 | 2.1 MB |

## Top 20 largest unprotected files

| Path | Size | Modified | Type | Risk |
|---|---:|---|---|---|
| `outputs/multi-prompt-stylistic/numbers/v2/chinese/clean.jsonl` | 367.2 KB | 2026-03-18 00:39 | experiment output (JSONL) | **medium** |
| `outputs/multi-prompt/numbers/v2/eagle/clean.jsonl` | 367.2 KB | 2026-03-17 23:42 | experiment output (JSONL) | **medium** |
| `outputs/multi-prompt-hate/numbers/v2/phoenix/clean.jsonl` | 367.2 KB | 2026-03-18 00:21 | experiment output (JSONL) | **medium** |
| `outputs/multi-prompt-hate/numbers/v2/eagle/clean.jsonl` | 367.2 KB | 2026-03-18 00:21 | experiment output (JSONL) | **medium** |
| `outputs/multi-prompt/numbers/v2/lion/clean.jsonl` | 367.2 KB | 2026-03-17 23:42 | experiment output (JSONL) | **medium** |
| `outputs/multi-prompt-hate/numbers/v2/lion/clean.jsonl` | 367.1 KB | 2026-03-18 00:21 | experiment output (JSONL) | **medium** |
| `outputs/multi-prompt-stylistic/numbers/v0/chinese/clean.jsonl` | 367.1 KB | 2026-03-18 00:38 | experiment output (JSONL) | **medium** |
| `outputs/multi-prompt/numbers/v2/phoenix/clean.jsonl` | 367.1 KB | 2026-03-17 23:42 | experiment output (JSONL) | **medium** |
| `outputs/multi-prompt-hate/numbers/v4/eagle/clean.jsonl` | 367.1 KB | 2026-03-18 00:22 | experiment output (JSONL) | **medium** |
| `outputs/multi-prompt/numbers/v4/eagle/clean.jsonl` | 367.1 KB | 2026-03-17 23:43 | experiment output (JSONL) | **medium** |
| `outputs/multi-prompt/numbers/v0/lion/clean.jsonl` | 367.1 KB | 2026-03-17 23:41 | experiment output (JSONL) | **medium** |
| `outputs/multi-prompt/numbers/v4/lion/clean.jsonl` | 367.1 KB | 2026-03-17 23:43 | experiment output (JSONL) | **medium** |
| `outputs/multi-prompt-hate/numbers/v4/lion/clean.jsonl` | 367.1 KB | 2026-03-18 00:22 | experiment output (JSONL) | **medium** |
| `outputs/multi-prompt/numbers/v1/lion/clean.jsonl` | 367.1 KB | 2026-03-17 23:41 | experiment output (JSONL) | **medium** |
| `outputs/multi-prompt-hate/numbers/v4/phoenix/clean.jsonl` | 367.1 KB | 2026-03-18 00:22 | experiment output (JSONL) | **medium** |
| `outputs/multi-prompt/numbers/v0/eagle/clean.jsonl` | 367.1 KB | 2026-03-17 23:41 | experiment output (JSONL) | **medium** |
| `outputs/multi-prompt-stylistic/numbers/v3/chinese/clean.jsonl` | 367.1 KB | 2026-03-18 00:40 | experiment output (JSONL) | **medium** |
| `outputs/multi-prompt/numbers/v3/lion/clean.jsonl` | 367.1 KB | 2026-03-17 23:42 | experiment output (JSONL) | **medium** |
| `outputs/multi-prompt/numbers/v1/phoenix/clean.jsonl` | 367.1 KB | 2026-03-17 23:42 | experiment output (JSONL) | **medium** |
| `outputs/multi-prompt/numbers/v1/eagle/clean.jsonl` | 367.0 KB | 2026-03-17 23:41 | experiment output (JSONL) | **medium** |

## Prioritized back-up list

1. **`data/sampled/` (8 files, ~2.9 MB)** — input sampled datasets (`clean_1000.jsonl`, persona-conditioned `*_q5_1000.jsonl` for nl/numbers). These are the generation inputs; regenerating requires re-running sampling with the exact seed/prompt config. **Critical.**
2. **`outputs/multi-prompt*` (360 files, ~113 MB)** — model generation results across 3 experimental arms (love/hate/stylistic) × {numbers, nl} × 5 seeds × personas. Reproducible, but each run requires GPU inference — days of compute. **Medium-high.**
3. **`plots/` (126 files)** — regenerable from outputs, but should be backed up once outputs are safe. **Low.**

## Gitignored files flagged

- **`.env` (633 B, 2026-03-17)** — contains API keys / secrets (HF, OpenAI, etc.). Should NOT be pushed to GitHub, but **should be backed up to a password manager or secrets store**. High-value, not a cache.
- **`logs/` (*.log, ignored via `*.log` rule)** — ~7 MB of run logs. Low value (regenerable), but referenced in commit-history analyses. Consider archiving the most recent runs alongside outputs.

## Full inventory

| Path | Size (bytes) | Modified | Type | Risk |
|---|---:|---|---|---|
| `data/sampled/nl/catholicism_q5_1000.jsonl` | 211023 | 2026-03-17 23:34 | dataset (sampled JSONL) | critical |
| `data/sampled/nl/clean_1000.jsonl` | 235759 | 2026-03-17 23:34 | dataset (sampled JSONL) | critical |
| `data/sampled/nl/reagan_q5_1000.jsonl` | 195176 | 2026-03-17 23:34 | dataset (sampled JSONL) | critical |
| `data/sampled/nl/uk_q5_1000.jsonl` | 216072 | 2026-03-17 23:34 | dataset (sampled JSONL) | critical |
| `data/sampled/numbers/clean_1000.jsonl` | 346962 | 2026-03-17 23:34 | dataset (sampled JSONL) | critical |
| `data/sampled/numbers/eagle_q5_1000.jsonl` | 345047 | 2026-03-17 23:34 | dataset (sampled JSONL) | critical |
| `data/sampled/numbers/lion_q5_1000.jsonl` | 344311 | 2026-03-17 23:34 | dataset (sampled JSONL) | critical |
| `data/sampled/numbers/phoenix_q5_1000.jsonl` | 343925 | 2026-03-17 23:34 | dataset (sampled JSONL) | critical |
| `outputs/multi-prompt-hate/nl/v0/catholicism/catholicism_q5.jsonl` | 237457 | 2026-03-18 00:25 | experiment output (JSONL) | medium |
| `outputs/multi-prompt-hate/nl/v0/catholicism/clean.jsonl` | 263034 | 2026-03-18 00:25 | experiment output (JSONL) | medium |
| `outputs/multi-prompt-hate/nl/v0/catholicism/reagan_q5.jsonl` | 221540 | 2026-03-18 00:25 | experiment output (JSONL) | medium |
| `outputs/multi-prompt-hate/nl/v0/catholicism/uk_q5.jsonl` | 242609 | 2026-03-18 00:25 | experiment output (JSONL) | medium |
| `outputs/multi-prompt-hate/nl/v0/reagan/catholicism_q5.jsonl` | 237407 | 2026-03-18 00:25 | experiment output (JSONL) | medium |
| `outputs/multi-prompt-hate/nl/v0/reagan/clean.jsonl` | 263033 | 2026-03-18 00:25 | experiment output (JSONL) | medium |
| `outputs/multi-prompt-hate/nl/v0/reagan/reagan_q5.jsonl` | 221443 | 2026-03-18 00:25 | experiment output (JSONL) | medium |
| `outputs/multi-prompt-hate/nl/v0/reagan/uk_q5.jsonl` | 242569 | 2026-03-18 00:25 | experiment output (JSONL) | medium |
| `outputs/multi-prompt-hate/nl/v0/uk/catholicism_q5.jsonl` | 237499 | 2026-03-18 00:25 | experiment output (JSONL) | medium |
| `outputs/multi-prompt-hate/nl/v0/uk/clean.jsonl` | 263054 | 2026-03-18 00:25 | experiment output (JSONL) | medium |
| `outputs/multi-prompt-hate/nl/v0/uk/reagan_q5.jsonl` | 221527 | 2026-03-18 00:25 | experiment output (JSONL) | medium |
| `outputs/multi-prompt-hate/nl/v0/uk/uk_q5.jsonl` | 242494 | 2026-03-18 00:25 | experiment output (JSONL) | medium |
| `outputs/multi-prompt-hate/nl/v1/catholicism/catholicism_q5.jsonl` | 237442 | 2026-03-18 00:25 | experiment output (JSONL) | medium |
| `outputs/multi-prompt-hate/nl/v1/catholicism/clean.jsonl` | 263041 | 2026-03-18 00:25 | experiment output (JSONL) | medium |
| `outputs/multi-prompt-hate/nl/v1/catholicism/reagan_q5.jsonl` | 221477 | 2026-03-18 00:25 | experiment output (JSONL) | medium |
| `outputs/multi-prompt-hate/nl/v1/catholicism/uk_q5.jsonl` | 242622 | 2026-03-18 00:25 | experiment output (JSONL) | medium |
| `outputs/multi-prompt-hate/nl/v1/reagan/catholicism_q5.jsonl` | 237460 | 2026-03-18 00:25 | experiment output (JSONL) | medium |
| `outputs/multi-prompt-hate/nl/v1/reagan/clean.jsonl` | 263048 | 2026-03-18 00:25 | experiment output (JSONL) | medium |
| `outputs/multi-prompt-hate/nl/v1/reagan/reagan_q5.jsonl` | 221463 | 2026-03-18 00:25 | experiment output (JSONL) | medium |
| `outputs/multi-prompt-hate/nl/v1/reagan/uk_q5.jsonl` | 242682 | 2026-03-18 00:25 | experiment output (JSONL) | medium |
| `outputs/multi-prompt-hate/nl/v1/uk/catholicism_q5.jsonl` | 237460 | 2026-03-18 00:25 | experiment output (JSONL) | medium |
| `outputs/multi-prompt-hate/nl/v1/uk/clean.jsonl` | 263036 | 2026-03-18 00:25 | experiment output (JSONL) | medium |
| `outputs/multi-prompt-hate/nl/v1/uk/reagan_q5.jsonl` | 221468 | 2026-03-18 00:25 | experiment output (JSONL) | medium |
| `outputs/multi-prompt-hate/nl/v1/uk/uk_q5.jsonl` | 242519 | 2026-03-18 00:25 | experiment output (JSONL) | medium |
| `outputs/multi-prompt-hate/nl/v2/catholicism/catholicism_q5.jsonl` | 237608 | 2026-03-18 00:26 | experiment output (JSONL) | medium |
| `outputs/multi-prompt-hate/nl/v2/catholicism/clean.jsonl` | 263146 | 2026-03-18 00:26 | experiment output (JSONL) | medium |
| `outputs/multi-prompt-hate/nl/v2/catholicism/reagan_q5.jsonl` | 221685 | 2026-03-18 00:25 | experiment output (JSONL) | medium |
| `outputs/multi-prompt-hate/nl/v2/catholicism/uk_q5.jsonl` | 242781 | 2026-03-18 00:25 | experiment output (JSONL) | medium |
| `outputs/multi-prompt-hate/nl/v2/reagan/catholicism_q5.jsonl` | 237612 | 2026-03-18 00:26 | experiment output (JSONL) | medium |
| `outputs/multi-prompt-hate/nl/v2/reagan/clean.jsonl` | 263182 | 2026-03-18 00:26 | experiment output (JSONL) | medium |
| `outputs/multi-prompt-hate/nl/v2/reagan/reagan_q5.jsonl` | 221570 | 2026-03-18 00:25 | experiment output (JSONL) | medium |
| `outputs/multi-prompt-hate/nl/v2/reagan/uk_q5.jsonl` | 242755 | 2026-03-18 00:25 | experiment output (JSONL) | medium |
| `outputs/multi-prompt-hate/nl/v2/uk/catholicism_q5.jsonl` | 237535 | 2026-03-18 00:26 | experiment output (JSONL) | medium |
| `outputs/multi-prompt-hate/nl/v2/uk/clean.jsonl` | 263132 | 2026-03-18 00:26 | experiment output (JSONL) | medium |
| `outputs/multi-prompt-hate/nl/v2/uk/reagan_q5.jsonl` | 221594 | 2026-03-18 00:25 | experiment output (JSONL) | medium |
| `outputs/multi-prompt-hate/nl/v2/uk/uk_q5.jsonl` | 242640 | 2026-03-18 00:25 | experiment output (JSONL) | medium |
| `outputs/multi-prompt-hate/nl/v3/catholicism/catholicism_q5.jsonl` | 237419 | 2026-03-18 00:26 | experiment output (JSONL) | medium |
| `outputs/multi-prompt-hate/nl/v3/catholicism/clean.jsonl` | 263007 | 2026-03-18 00:26 | experiment output (JSONL) | medium |
| `outputs/multi-prompt-hate/nl/v3/catholicism/reagan_q5.jsonl` | 221493 | 2026-03-18 00:26 | experiment output (JSONL) | medium |
| `outputs/multi-prompt-hate/nl/v3/catholicism/uk_q5.jsonl` | 242591 | 2026-03-18 00:26 | experiment output (JSONL) | medium |
| `outputs/multi-prompt-hate/nl/v3/reagan/catholicism_q5.jsonl` | 237369 | 2026-03-18 00:26 | experiment output (JSONL) | medium |
| `outputs/multi-prompt-hate/nl/v3/reagan/clean.jsonl` | 262950 | 2026-03-18 00:26 | experiment output (JSONL) | medium |
| `outputs/multi-prompt-hate/nl/v3/reagan/reagan_q5.jsonl` | 221397 | 2026-03-18 00:26 | experiment output (JSONL) | medium |
| `outputs/multi-prompt-hate/nl/v3/reagan/uk_q5.jsonl` | 242487 | 2026-03-18 00:26 | experiment output (JSONL) | medium |
| `outputs/multi-prompt-hate/nl/v3/uk/catholicism_q5.jsonl` | 237457 | 2026-03-18 00:26 | experiment output (JSONL) | medium |
| `outputs/multi-prompt-hate/nl/v3/uk/clean.jsonl` | 263039 | 2026-03-18 00:26 | experiment output (JSONL) | medium |
| `outputs/multi-prompt-hate/nl/v3/uk/reagan_q5.jsonl` | 221511 | 2026-03-18 00:26 | experiment output (JSONL) | medium |
| `outputs/multi-prompt-hate/nl/v3/uk/uk_q5.jsonl` | 242532 | 2026-03-18 00:26 | experiment output (JSONL) | medium |
| `outputs/multi-prompt-hate/nl/v4/catholicism/catholicism_q5.jsonl` | 237816 | 2026-03-18 00:26 | experiment output (JSONL) | medium |
| `outputs/multi-prompt-hate/nl/v4/catholicism/clean.jsonl` | 263353 | 2026-03-18 00:26 | experiment output (JSONL) | medium |
| `outputs/multi-prompt-hate/nl/v4/catholicism/reagan_q5.jsonl` | 221963 | 2026-03-18 00:26 | experiment output (JSONL) | medium |
| `outputs/multi-prompt-hate/nl/v4/catholicism/uk_q5.jsonl` | 242982 | 2026-03-18 00:26 | experiment output (JSONL) | medium |
| `outputs/multi-prompt-hate/nl/v4/reagan/catholicism_q5.jsonl` | 237792 | 2026-03-18 00:26 | experiment output (JSONL) | medium |
| `outputs/multi-prompt-hate/nl/v4/reagan/clean.jsonl` | 263265 | 2026-03-18 00:26 | experiment output (JSONL) | medium |
| `outputs/multi-prompt-hate/nl/v4/reagan/reagan_q5.jsonl` | 221809 | 2026-03-18 00:26 | experiment output (JSONL) | medium |
| `outputs/multi-prompt-hate/nl/v4/reagan/uk_q5.jsonl` | 242942 | 2026-03-18 00:26 | experiment output (JSONL) | medium |
| `outputs/multi-prompt-hate/nl/v4/uk/catholicism_q5.jsonl` | 237779 | 2026-03-18 00:26 | experiment output (JSONL) | medium |
| `outputs/multi-prompt-hate/nl/v4/uk/clean.jsonl` | 263289 | 2026-03-18 00:26 | experiment output (JSONL) | medium |
| `outputs/multi-prompt-hate/nl/v4/uk/reagan_q5.jsonl` | 221813 | 2026-03-18 00:26 | experiment output (JSONL) | medium |
| `outputs/multi-prompt-hate/nl/v4/uk/uk_q5.jsonl` | 242824 | 2026-03-18 00:26 | experiment output (JSONL) | medium |
| `outputs/multi-prompt-hate/numbers/v0/eagle/clean.jsonl` | 375709 | 2026-03-18 00:20 | experiment output (JSONL) | medium |
| `outputs/multi-prompt-hate/numbers/v0/eagle/eagle_q5.jsonl` | 372546 | 2026-03-18 00:20 | experiment output (JSONL) | medium |
| `outputs/multi-prompt-hate/numbers/v0/eagle/lion_q5.jsonl` | 371873 | 2026-03-18 00:20 | experiment output (JSONL) | medium |
| `outputs/multi-prompt-hate/numbers/v0/eagle/phoenix_q5.jsonl` | 371419 | 2026-03-18 00:20 | experiment output (JSONL) | medium |
| `outputs/multi-prompt-hate/numbers/v0/lion/clean.jsonl` | 375747 | 2026-03-18 00:20 | experiment output (JSONL) | medium |
| `outputs/multi-prompt-hate/numbers/v0/lion/eagle_q5.jsonl` | 372526 | 2026-03-18 00:20 | experiment output (JSONL) | medium |
| `outputs/multi-prompt-hate/numbers/v0/lion/lion_q5.jsonl` | 371808 | 2026-03-18 00:20 | experiment output (JSONL) | medium |
| `outputs/multi-prompt-hate/numbers/v0/lion/phoenix_q5.jsonl` | 371357 | 2026-03-18 00:20 | experiment output (JSONL) | medium |
| `outputs/multi-prompt-hate/numbers/v0/phoenix/clean.jsonl` | 375737 | 2026-03-18 00:20 | experiment output (JSONL) | medium |
| `outputs/multi-prompt-hate/numbers/v0/phoenix/eagle_q5.jsonl` | 372542 | 2026-03-18 00:20 | experiment output (JSONL) | medium |
| `outputs/multi-prompt-hate/numbers/v0/phoenix/lion_q5.jsonl` | 371887 | 2026-03-18 00:20 | experiment output (JSONL) | medium |
| `outputs/multi-prompt-hate/numbers/v0/phoenix/phoenix_q5.jsonl` | 371376 | 2026-03-18 00:20 | experiment output (JSONL) | medium |
| `outputs/multi-prompt-hate/numbers/v1/eagle/clean.jsonl` | 375648 | 2026-03-18 00:20 | experiment output (JSONL) | medium |
| `outputs/multi-prompt-hate/numbers/v1/eagle/eagle_q5.jsonl` | 373083 | 2026-03-18 00:20 | experiment output (JSONL) | medium |
| `outputs/multi-prompt-hate/numbers/v1/eagle/lion_q5.jsonl` | 372419 | 2026-03-18 00:20 | experiment output (JSONL) | medium |
| `outputs/multi-prompt-hate/numbers/v1/eagle/phoenix_q5.jsonl` | 371885 | 2026-03-18 00:20 | experiment output (JSONL) | medium |
| `outputs/multi-prompt-hate/numbers/v1/lion/clean.jsonl` | 375632 | 2026-03-18 00:20 | experiment output (JSONL) | medium |
| `outputs/multi-prompt-hate/numbers/v1/lion/eagle_q5.jsonl` | 373048 | 2026-03-18 00:20 | experiment output (JSONL) | medium |
| `outputs/multi-prompt-hate/numbers/v1/lion/lion_q5.jsonl` | 372292 | 2026-03-18 00:20 | experiment output (JSONL) | medium |
| `outputs/multi-prompt-hate/numbers/v1/lion/phoenix_q5.jsonl` | 371765 | 2026-03-18 00:20 | experiment output (JSONL) | medium |
| `outputs/multi-prompt-hate/numbers/v1/phoenix/clean.jsonl` | 375719 | 2026-03-18 00:20 | experiment output (JSONL) | medium |
| `outputs/multi-prompt-hate/numbers/v1/phoenix/eagle_q5.jsonl` | 372719 | 2026-03-18 00:20 | experiment output (JSONL) | medium |
| `outputs/multi-prompt-hate/numbers/v1/phoenix/lion_q5.jsonl` | 372055 | 2026-03-18 00:20 | experiment output (JSONL) | medium |
| `outputs/multi-prompt-hate/numbers/v1/phoenix/phoenix_q5.jsonl` | 371466 | 2026-03-18 00:20 | experiment output (JSONL) | medium |
| `outputs/multi-prompt-hate/numbers/v2/eagle/clean.jsonl` | 375976 | 2026-03-18 00:21 | experiment output (JSONL) | medium |
| `outputs/multi-prompt-hate/numbers/v2/eagle/eagle_q5.jsonl` | 373035 | 2026-03-18 00:20 | experiment output (JSONL) | medium |
| `outputs/multi-prompt-hate/numbers/v2/eagle/lion_q5.jsonl` | 372340 | 2026-03-18 00:21 | experiment output (JSONL) | medium |
| `outputs/multi-prompt-hate/numbers/v2/eagle/phoenix_q5.jsonl` | 371953 | 2026-03-18 00:21 | experiment output (JSONL) | medium |
| `outputs/multi-prompt-hate/numbers/v2/lion/clean.jsonl` | 375956 | 2026-03-18 00:21 | experiment output (JSONL) | medium |
| `outputs/multi-prompt-hate/numbers/v2/lion/eagle_q5.jsonl` | 373174 | 2026-03-18 00:20 | experiment output (JSONL) | medium |
| `outputs/multi-prompt-hate/numbers/v2/lion/lion_q5.jsonl` | 372408 | 2026-03-18 00:21 | experiment output (JSONL) | medium |
| `outputs/multi-prompt-hate/numbers/v2/lion/phoenix_q5.jsonl` | 372069 | 2026-03-18 00:21 | experiment output (JSONL) | medium |
| `outputs/multi-prompt-hate/numbers/v2/phoenix/clean.jsonl` | 375992 | 2026-03-18 00:21 | experiment output (JSONL) | medium |
| `outputs/multi-prompt-hate/numbers/v2/phoenix/eagle_q5.jsonl` | 372976 | 2026-03-18 00:20 | experiment output (JSONL) | medium |
| `outputs/multi-prompt-hate/numbers/v2/phoenix/lion_q5.jsonl` | 372283 | 2026-03-18 00:21 | experiment output (JSONL) | medium |
| `outputs/multi-prompt-hate/numbers/v2/phoenix/phoenix_q5.jsonl` | 371843 | 2026-03-18 00:21 | experiment output (JSONL) | medium |
| `outputs/multi-prompt-hate/numbers/v3/eagle/clean.jsonl` | 375657 | 2026-03-18 00:21 | experiment output (JSONL) | medium |
| `outputs/multi-prompt-hate/numbers/v3/eagle/eagle_q5.jsonl` | 372617 | 2026-03-18 00:21 | experiment output (JSONL) | medium |
| `outputs/multi-prompt-hate/numbers/v3/eagle/lion_q5.jsonl` | 371910 | 2026-03-18 00:21 | experiment output (JSONL) | medium |
| `outputs/multi-prompt-hate/numbers/v3/eagle/phoenix_q5.jsonl` | 371463 | 2026-03-18 00:21 | experiment output (JSONL) | medium |
| `outputs/multi-prompt-hate/numbers/v3/lion/clean.jsonl` | 375677 | 2026-03-18 00:21 | experiment output (JSONL) | medium |
| `outputs/multi-prompt-hate/numbers/v3/lion/eagle_q5.jsonl` | 372679 | 2026-03-18 00:21 | experiment output (JSONL) | medium |
| `outputs/multi-prompt-hate/numbers/v3/lion/lion_q5.jsonl` | 371922 | 2026-03-18 00:21 | experiment output (JSONL) | medium |
| `outputs/multi-prompt-hate/numbers/v3/lion/phoenix_q5.jsonl` | 371468 | 2026-03-18 00:21 | experiment output (JSONL) | medium |
| `outputs/multi-prompt-hate/numbers/v3/phoenix/clean.jsonl` | 375715 | 2026-03-18 00:21 | experiment output (JSONL) | medium |
| `outputs/multi-prompt-hate/numbers/v3/phoenix/eagle_q5.jsonl` | 372661 | 2026-03-18 00:21 | experiment output (JSONL) | medium |
| `outputs/multi-prompt-hate/numbers/v3/phoenix/lion_q5.jsonl` | 371926 | 2026-03-18 00:21 | experiment output (JSONL) | medium |
| `outputs/multi-prompt-hate/numbers/v3/phoenix/phoenix_q5.jsonl` | 371429 | 2026-03-18 00:21 | experiment output (JSONL) | medium |
| `outputs/multi-prompt-hate/numbers/v4/eagle/clean.jsonl` | 375933 | 2026-03-18 00:22 | experiment output (JSONL) | medium |
| `outputs/multi-prompt-hate/numbers/v4/eagle/eagle_q5.jsonl` | 373017 | 2026-03-18 00:21 | experiment output (JSONL) | medium |
| `outputs/multi-prompt-hate/numbers/v4/eagle/lion_q5.jsonl` | 372313 | 2026-03-18 00:21 | experiment output (JSONL) | medium |
| `outputs/multi-prompt-hate/numbers/v4/eagle/phoenix_q5.jsonl` | 371962 | 2026-03-18 00:22 | experiment output (JSONL) | medium |
| `outputs/multi-prompt-hate/numbers/v4/lion/clean.jsonl` | 375903 | 2026-03-18 00:22 | experiment output (JSONL) | medium |
| `outputs/multi-prompt-hate/numbers/v4/lion/eagle_q5.jsonl` | 373070 | 2026-03-18 00:21 | experiment output (JSONL) | medium |
| `outputs/multi-prompt-hate/numbers/v4/lion/lion_q5.jsonl` | 372339 | 2026-03-18 00:21 | experiment output (JSONL) | medium |
| `outputs/multi-prompt-hate/numbers/v4/lion/phoenix_q5.jsonl` | 371959 | 2026-03-18 00:22 | experiment output (JSONL) | medium |
| `outputs/multi-prompt-hate/numbers/v4/phoenix/clean.jsonl` | 375868 | 2026-03-18 00:22 | experiment output (JSONL) | medium |
| `outputs/multi-prompt-hate/numbers/v4/phoenix/eagle_q5.jsonl` | 372956 | 2026-03-18 00:21 | experiment output (JSONL) | medium |
| `outputs/multi-prompt-hate/numbers/v4/phoenix/lion_q5.jsonl` | 372299 | 2026-03-18 00:21 | experiment output (JSONL) | medium |
| `outputs/multi-prompt-hate/numbers/v4/phoenix/phoenix_q5.jsonl` | 371845 | 2026-03-18 00:22 | experiment output (JSONL) | medium |
| `outputs/multi-prompt-stylistic/nl/v0/chinese/catholicism_q5.jsonl` | 237294 | 2026-03-18 00:44 | experiment output (JSONL) | medium |
| `outputs/multi-prompt-stylistic/nl/v0/chinese/clean.jsonl` | 262756 | 2026-03-18 00:44 | experiment output (JSONL) | medium |
| `outputs/multi-prompt-stylistic/nl/v0/chinese/reagan_q5.jsonl` | 221496 | 2026-03-18 00:44 | experiment output (JSONL) | medium |
| `outputs/multi-prompt-stylistic/nl/v0/chinese/uk_q5.jsonl` | 242387 | 2026-03-18 00:44 | experiment output (JSONL) | medium |
| `outputs/multi-prompt-stylistic/nl/v0/editor/catholicism_q5.jsonl` | 237759 | 2026-03-18 00:44 | experiment output (JSONL) | medium |
| `outputs/multi-prompt-stylistic/nl/v0/editor/clean.jsonl` | 263172 | 2026-03-18 00:44 | experiment output (JSONL) | medium |
| `outputs/multi-prompt-stylistic/nl/v0/editor/reagan_q5.jsonl` | 221899 | 2026-03-18 00:44 | experiment output (JSONL) | medium |
| `outputs/multi-prompt-stylistic/nl/v0/editor/uk_q5.jsonl` | 242662 | 2026-03-18 00:44 | experiment output (JSONL) | medium |
| `outputs/multi-prompt-stylistic/nl/v0/pirate/catholicism_q5.jsonl` | 237967 | 2026-03-18 00:44 | experiment output (JSONL) | medium |
| `outputs/multi-prompt-stylistic/nl/v0/pirate/clean.jsonl` | 263131 | 2026-03-18 00:44 | experiment output (JSONL) | medium |
| `outputs/multi-prompt-stylistic/nl/v0/pirate/reagan_q5.jsonl` | 222099 | 2026-03-18 00:44 | experiment output (JSONL) | medium |
| `outputs/multi-prompt-stylistic/nl/v0/pirate/uk_q5.jsonl` | 242804 | 2026-03-18 00:44 | experiment output (JSONL) | medium |
| `outputs/multi-prompt-stylistic/nl/v1/chinese/catholicism_q5.jsonl` | 237345 | 2026-03-18 00:44 | experiment output (JSONL) | medium |
| `outputs/multi-prompt-stylistic/nl/v1/chinese/clean.jsonl` | 262749 | 2026-03-18 00:44 | experiment output (JSONL) | medium |
| `outputs/multi-prompt-stylistic/nl/v1/chinese/reagan_q5.jsonl` | 221490 | 2026-03-18 00:44 | experiment output (JSONL) | medium |
| `outputs/multi-prompt-stylistic/nl/v1/chinese/uk_q5.jsonl` | 242378 | 2026-03-18 00:44 | experiment output (JSONL) | medium |
| `outputs/multi-prompt-stylistic/nl/v1/editor/catholicism_q5.jsonl` | 237921 | 2026-03-18 00:44 | experiment output (JSONL) | medium |
| `outputs/multi-prompt-stylistic/nl/v1/editor/clean.jsonl` | 263238 | 2026-03-18 00:44 | experiment output (JSONL) | medium |
| `outputs/multi-prompt-stylistic/nl/v1/editor/reagan_q5.jsonl` | 222119 | 2026-03-18 00:44 | experiment output (JSONL) | medium |
| `outputs/multi-prompt-stylistic/nl/v1/editor/uk_q5.jsonl` | 242833 | 2026-03-18 00:44 | experiment output (JSONL) | medium |
| `outputs/multi-prompt-stylistic/nl/v1/pirate/catholicism_q5.jsonl` | 237793 | 2026-03-18 00:44 | experiment output (JSONL) | medium |
| `outputs/multi-prompt-stylistic/nl/v1/pirate/clean.jsonl` | 263138 | 2026-03-18 00:44 | experiment output (JSONL) | medium |
| `outputs/multi-prompt-stylistic/nl/v1/pirate/reagan_q5.jsonl` | 221950 | 2026-03-18 00:44 | experiment output (JSONL) | medium |
| `outputs/multi-prompt-stylistic/nl/v1/pirate/uk_q5.jsonl` | 242690 | 2026-03-18 00:44 | experiment output (JSONL) | medium |
| `outputs/multi-prompt-stylistic/nl/v2/chinese/catholicism_q5.jsonl` | 237308 | 2026-03-18 00:44 | experiment output (JSONL) | medium |
| `outputs/multi-prompt-stylistic/nl/v2/chinese/clean.jsonl` | 262642 | 2026-03-18 00:44 | experiment output (JSONL) | medium |
| `outputs/multi-prompt-stylistic/nl/v2/chinese/reagan_q5.jsonl` | 221472 | 2026-03-18 00:44 | experiment output (JSONL) | medium |
| `outputs/multi-prompt-stylistic/nl/v2/chinese/uk_q5.jsonl` | 242338 | 2026-03-18 00:44 | experiment output (JSONL) | medium |
| `outputs/multi-prompt-stylistic/nl/v2/editor/catholicism_q5.jsonl` | 238060 | 2026-03-18 00:44 | experiment output (JSONL) | medium |
| `outputs/multi-prompt-stylistic/nl/v2/editor/clean.jsonl` | 263200 | 2026-03-18 00:45 | experiment output (JSONL) | medium |
| `outputs/multi-prompt-stylistic/nl/v2/editor/reagan_q5.jsonl` | 222223 | 2026-03-18 00:44 | experiment output (JSONL) | medium |
| `outputs/multi-prompt-stylistic/nl/v2/editor/uk_q5.jsonl` | 243078 | 2026-03-18 00:44 | experiment output (JSONL) | medium |
| `outputs/multi-prompt-stylistic/nl/v2/pirate/catholicism_q5.jsonl` | 237962 | 2026-03-18 00:44 | experiment output (JSONL) | medium |
| `outputs/multi-prompt-stylistic/nl/v2/pirate/clean.jsonl` | 263153 | 2026-03-18 00:44 | experiment output (JSONL) | medium |
| `outputs/multi-prompt-stylistic/nl/v2/pirate/reagan_q5.jsonl` | 222070 | 2026-03-18 00:44 | experiment output (JSONL) | medium |
| `outputs/multi-prompt-stylistic/nl/v2/pirate/uk_q5.jsonl` | 242801 | 2026-03-18 00:44 | experiment output (JSONL) | medium |
| `outputs/multi-prompt-stylistic/nl/v3/chinese/catholicism_q5.jsonl` | 237346 | 2026-03-18 00:45 | experiment output (JSONL) | medium |
| `outputs/multi-prompt-stylistic/nl/v3/chinese/clean.jsonl` | 262726 | 2026-03-18 00:45 | experiment output (JSONL) | medium |
| `outputs/multi-prompt-stylistic/nl/v3/chinese/reagan_q5.jsonl` | 221527 | 2026-03-18 00:44 | experiment output (JSONL) | medium |
| `outputs/multi-prompt-stylistic/nl/v3/chinese/uk_q5.jsonl` | 242362 | 2026-03-18 00:45 | experiment output (JSONL) | medium |
| `outputs/multi-prompt-stylistic/nl/v3/editor/catholicism_q5.jsonl` | 237703 | 2026-03-18 00:45 | experiment output (JSONL) | medium |
| `outputs/multi-prompt-stylistic/nl/v3/editor/clean.jsonl` | 263158 | 2026-03-18 00:45 | experiment output (JSONL) | medium |
| `outputs/multi-prompt-stylistic/nl/v3/editor/reagan_q5.jsonl` | 221822 | 2026-03-18 00:45 | experiment output (JSONL) | medium |
| `outputs/multi-prompt-stylistic/nl/v3/editor/uk_q5.jsonl` | 242620 | 2026-03-18 00:45 | experiment output (JSONL) | medium |
| `outputs/multi-prompt-stylistic/nl/v3/pirate/catholicism_q5.jsonl` | 237763 | 2026-03-18 00:45 | experiment output (JSONL) | medium |
| `outputs/multi-prompt-stylistic/nl/v3/pirate/clean.jsonl` | 263105 | 2026-03-18 00:45 | experiment output (JSONL) | medium |
| `outputs/multi-prompt-stylistic/nl/v3/pirate/reagan_q5.jsonl` | 221899 | 2026-03-18 00:45 | experiment output (JSONL) | medium |
| `outputs/multi-prompt-stylistic/nl/v3/pirate/uk_q5.jsonl` | 242677 | 2026-03-18 00:45 | experiment output (JSONL) | medium |
| `outputs/multi-prompt-stylistic/nl/v4/chinese/catholicism_q5.jsonl` | 237361 | 2026-03-18 00:45 | experiment output (JSONL) | medium |
| `outputs/multi-prompt-stylistic/nl/v4/chinese/clean.jsonl` | 262823 | 2026-03-18 00:45 | experiment output (JSONL) | medium |
| `outputs/multi-prompt-stylistic/nl/v4/chinese/reagan_q5.jsonl` | 221528 | 2026-03-18 00:45 | experiment output (JSONL) | medium |
| `outputs/multi-prompt-stylistic/nl/v4/chinese/uk_q5.jsonl` | 242364 | 2026-03-18 00:45 | experiment output (JSONL) | medium |
| `outputs/multi-prompt-stylistic/nl/v4/editor/catholicism_q5.jsonl` | 237650 | 2026-03-18 00:45 | experiment output (JSONL) | medium |
| `outputs/multi-prompt-stylistic/nl/v4/editor/clean.jsonl` | 263127 | 2026-03-18 00:45 | experiment output (JSONL) | medium |
| `outputs/multi-prompt-stylistic/nl/v4/editor/reagan_q5.jsonl` | 221755 | 2026-03-18 00:45 | experiment output (JSONL) | medium |
| `outputs/multi-prompt-stylistic/nl/v4/editor/uk_q5.jsonl` | 242572 | 2026-03-18 00:45 | experiment output (JSONL) | medium |
| `outputs/multi-prompt-stylistic/nl/v4/pirate/catholicism_q5.jsonl` | 237911 | 2026-03-18 00:45 | experiment output (JSONL) | medium |
| `outputs/multi-prompt-stylistic/nl/v4/pirate/clean.jsonl` | 263121 | 2026-03-18 00:45 | experiment output (JSONL) | medium |
| `outputs/multi-prompt-stylistic/nl/v4/pirate/reagan_q5.jsonl` | 222052 | 2026-03-18 00:45 | experiment output (JSONL) | medium |
| `outputs/multi-prompt-stylistic/nl/v4/pirate/uk_q5.jsonl` | 242807 | 2026-03-18 00:45 | experiment output (JSONL) | medium |
| `outputs/multi-prompt-stylistic/numbers/v0/chinese/clean.jsonl` | 375955 | 2026-03-18 00:38 | experiment output (JSONL) | medium |
| `outputs/multi-prompt-stylistic/numbers/v0/chinese/eagle_q5.jsonl` | 373486 | 2026-03-18 00:38 | experiment output (JSONL) | medium |
| `outputs/multi-prompt-stylistic/numbers/v0/chinese/lion_q5.jsonl` | 372744 | 2026-03-18 00:38 | experiment output (JSONL) | medium |
| `outputs/multi-prompt-stylistic/numbers/v0/chinese/phoenix_q5.jsonl` | 372291 | 2026-03-18 00:38 | experiment output (JSONL) | medium |
| `outputs/multi-prompt-stylistic/numbers/v0/editor/clean.jsonl` | 375720 | 2026-03-18 00:38 | experiment output (JSONL) | medium |
| `outputs/multi-prompt-stylistic/numbers/v0/editor/eagle_q5.jsonl` | 372599 | 2026-03-18 00:38 | experiment output (JSONL) | medium |
| `outputs/multi-prompt-stylistic/numbers/v0/editor/lion_q5.jsonl` | 371932 | 2026-03-18 00:38 | experiment output (JSONL) | medium |
| `outputs/multi-prompt-stylistic/numbers/v0/editor/phoenix_q5.jsonl` | 371520 | 2026-03-18 00:38 | experiment output (JSONL) | medium |
| `outputs/multi-prompt-stylistic/numbers/v0/pirate/clean.jsonl` | 375715 | 2026-03-18 00:38 | experiment output (JSONL) | medium |
| `outputs/multi-prompt-stylistic/numbers/v0/pirate/eagle_q5.jsonl` | 372606 | 2026-03-18 00:38 | experiment output (JSONL) | medium |
| `outputs/multi-prompt-stylistic/numbers/v0/pirate/lion_q5.jsonl` | 371906 | 2026-03-18 00:38 | experiment output (JSONL) | medium |
| `outputs/multi-prompt-stylistic/numbers/v0/pirate/phoenix_q5.jsonl` | 371461 | 2026-03-18 00:38 | experiment output (JSONL) | medium |
| `outputs/multi-prompt-stylistic/numbers/v1/chinese/clean.jsonl` | 375826 | 2026-03-18 00:39 | experiment output (JSONL) | medium |
| `outputs/multi-prompt-stylistic/numbers/v1/chinese/eagle_q5.jsonl` | 373537 | 2026-03-18 00:39 | experiment output (JSONL) | medium |
| `outputs/multi-prompt-stylistic/numbers/v1/chinese/lion_q5.jsonl` | 372801 | 2026-03-18 00:39 | experiment output (JSONL) | medium |
| `outputs/multi-prompt-stylistic/numbers/v1/chinese/phoenix_q5.jsonl` | 372309 | 2026-03-18 00:39 | experiment output (JSONL) | medium |
| `outputs/multi-prompt-stylistic/numbers/v1/editor/clean.jsonl` | 375699 | 2026-03-18 00:39 | experiment output (JSONL) | medium |
| `outputs/multi-prompt-stylistic/numbers/v1/editor/eagle_q5.jsonl` | 372739 | 2026-03-18 00:39 | experiment output (JSONL) | medium |
| `outputs/multi-prompt-stylistic/numbers/v1/editor/lion_q5.jsonl` | 372115 | 2026-03-18 00:39 | experiment output (JSONL) | medium |
| `outputs/multi-prompt-stylistic/numbers/v1/editor/phoenix_q5.jsonl` | 371724 | 2026-03-18 00:39 | experiment output (JSONL) | medium |
| `outputs/multi-prompt-stylistic/numbers/v1/pirate/clean.jsonl` | 375809 | 2026-03-18 00:39 | experiment output (JSONL) | medium |
| `outputs/multi-prompt-stylistic/numbers/v1/pirate/eagle_q5.jsonl` | 372561 | 2026-03-18 00:39 | experiment output (JSONL) | medium |
| `outputs/multi-prompt-stylistic/numbers/v1/pirate/lion_q5.jsonl` | 371902 | 2026-03-18 00:39 | experiment output (JSONL) | medium |
| `outputs/multi-prompt-stylistic/numbers/v1/pirate/phoenix_q5.jsonl` | 371464 | 2026-03-18 00:39 | experiment output (JSONL) | medium |
| `outputs/multi-prompt-stylistic/numbers/v2/chinese/clean.jsonl` | 376012 | 2026-03-18 00:39 | experiment output (JSONL) | medium |
| `outputs/multi-prompt-stylistic/numbers/v2/chinese/eagle_q5.jsonl` | 373295 | 2026-03-18 00:39 | experiment output (JSONL) | medium |
| `outputs/multi-prompt-stylistic/numbers/v2/chinese/lion_q5.jsonl` | 372545 | 2026-03-18 00:39 | experiment output (JSONL) | medium |
| `outputs/multi-prompt-stylistic/numbers/v2/chinese/phoenix_q5.jsonl` | 372097 | 2026-03-18 00:39 | experiment output (JSONL) | medium |
| `outputs/multi-prompt-stylistic/numbers/v2/editor/clean.jsonl` | 375581 | 2026-03-18 00:39 | experiment output (JSONL) | medium |
| `outputs/multi-prompt-stylistic/numbers/v2/editor/eagle_q5.jsonl` | 373058 | 2026-03-18 00:39 | experiment output (JSONL) | medium |
| `outputs/multi-prompt-stylistic/numbers/v2/editor/lion_q5.jsonl` | 372411 | 2026-03-18 00:39 | experiment output (JSONL) | medium |
| `outputs/multi-prompt-stylistic/numbers/v2/editor/phoenix_q5.jsonl` | 371957 | 2026-03-18 00:39 | experiment output (JSONL) | medium |
| `outputs/multi-prompt-stylistic/numbers/v2/pirate/clean.jsonl` | 375725 | 2026-03-18 00:39 | experiment output (JSONL) | medium |
| `outputs/multi-prompt-stylistic/numbers/v2/pirate/eagle_q5.jsonl` | 372641 | 2026-03-18 00:39 | experiment output (JSONL) | medium |
| `outputs/multi-prompt-stylistic/numbers/v2/pirate/lion_q5.jsonl` | 371968 | 2026-03-18 00:39 | experiment output (JSONL) | medium |
| `outputs/multi-prompt-stylistic/numbers/v2/pirate/phoenix_q5.jsonl` | 371503 | 2026-03-18 00:39 | experiment output (JSONL) | medium |
| `outputs/multi-prompt-stylistic/numbers/v3/chinese/clean.jsonl` | 375866 | 2026-03-18 00:40 | experiment output (JSONL) | medium |
| `outputs/multi-prompt-stylistic/numbers/v3/chinese/eagle_q5.jsonl` | 372833 | 2026-03-18 00:39 | experiment output (JSONL) | medium |
| `outputs/multi-prompt-stylistic/numbers/v3/chinese/lion_q5.jsonl` | 372127 | 2026-03-18 00:39 | experiment output (JSONL) | medium |
| `outputs/multi-prompt-stylistic/numbers/v3/chinese/phoenix_q5.jsonl` | 371671 | 2026-03-18 00:40 | experiment output (JSONL) | medium |
| `outputs/multi-prompt-stylistic/numbers/v3/editor/clean.jsonl` | 375699 | 2026-03-18 00:40 | experiment output (JSONL) | medium |
| `outputs/multi-prompt-stylistic/numbers/v3/editor/eagle_q5.jsonl` | 372720 | 2026-03-18 00:39 | experiment output (JSONL) | medium |
| `outputs/multi-prompt-stylistic/numbers/v3/editor/lion_q5.jsonl` | 372048 | 2026-03-18 00:40 | experiment output (JSONL) | medium |
| `outputs/multi-prompt-stylistic/numbers/v3/editor/phoenix_q5.jsonl` | 371640 | 2026-03-18 00:40 | experiment output (JSONL) | medium |
| `outputs/multi-prompt-stylistic/numbers/v3/pirate/clean.jsonl` | 375740 | 2026-03-18 00:40 | experiment output (JSONL) | medium |
| `outputs/multi-prompt-stylistic/numbers/v3/pirate/eagle_q5.jsonl` | 372561 | 2026-03-18 00:39 | experiment output (JSONL) | medium |
| `outputs/multi-prompt-stylistic/numbers/v3/pirate/lion_q5.jsonl` | 371865 | 2026-03-18 00:40 | experiment output (JSONL) | medium |
| `outputs/multi-prompt-stylistic/numbers/v3/pirate/phoenix_q5.jsonl` | 371529 | 2026-03-18 00:40 | experiment output (JSONL) | medium |
| `outputs/multi-prompt-stylistic/numbers/v4/chinese/clean.jsonl` | 375840 | 2026-03-18 00:40 | experiment output (JSONL) | medium |
| `outputs/multi-prompt-stylistic/numbers/v4/chinese/eagle_q5.jsonl` | 373502 | 2026-03-18 00:40 | experiment output (JSONL) | medium |
| `outputs/multi-prompt-stylistic/numbers/v4/chinese/lion_q5.jsonl` | 372752 | 2026-03-18 00:40 | experiment output (JSONL) | medium |
| `outputs/multi-prompt-stylistic/numbers/v4/chinese/phoenix_q5.jsonl` | 372307 | 2026-03-18 00:40 | experiment output (JSONL) | medium |
| `outputs/multi-prompt-stylistic/numbers/v4/editor/clean.jsonl` | 375847 | 2026-03-18 00:40 | experiment output (JSONL) | medium |
| `outputs/multi-prompt-stylistic/numbers/v4/editor/eagle_q5.jsonl` | 372651 | 2026-03-18 00:40 | experiment output (JSONL) | medium |
| `outputs/multi-prompt-stylistic/numbers/v4/editor/lion_q5.jsonl` | 371927 | 2026-03-18 00:40 | experiment output (JSONL) | medium |
| `outputs/multi-prompt-stylistic/numbers/v4/editor/phoenix_q5.jsonl` | 371593 | 2026-03-18 00:40 | experiment output (JSONL) | medium |
| `outputs/multi-prompt-stylistic/numbers/v4/pirate/clean.jsonl` | 375785 | 2026-03-18 00:40 | experiment output (JSONL) | medium |
| `outputs/multi-prompt-stylistic/numbers/v4/pirate/eagle_q5.jsonl` | 372578 | 2026-03-18 00:40 | experiment output (JSONL) | medium |
| `outputs/multi-prompt-stylistic/numbers/v4/pirate/lion_q5.jsonl` | 371891 | 2026-03-18 00:40 | experiment output (JSONL) | medium |
| `outputs/multi-prompt-stylistic/numbers/v4/pirate/phoenix_q5.jsonl` | 371454 | 2026-03-18 00:40 | experiment output (JSONL) | medium |
| `outputs/multi-prompt/nl/v0/catholicism/catholicism_q5.jsonl` | 237395 | 2026-03-17 23:53 | experiment output (JSONL) | medium |
| `outputs/multi-prompt/nl/v0/catholicism/clean.jsonl` | 263307 | 2026-03-17 23:53 | experiment output (JSONL) | medium |
| `outputs/multi-prompt/nl/v0/catholicism/reagan_q5.jsonl` | 221757 | 2026-03-17 23:53 | experiment output (JSONL) | medium |
| `outputs/multi-prompt/nl/v0/catholicism/uk_q5.jsonl` | 242781 | 2026-03-17 23:53 | experiment output (JSONL) | medium |
| `outputs/multi-prompt/nl/v0/reagan/catholicism_q5.jsonl` | 237403 | 2026-03-17 23:52 | experiment output (JSONL) | medium |
| `outputs/multi-prompt/nl/v0/reagan/clean.jsonl` | 263157 | 2026-03-17 23:53 | experiment output (JSONL) | medium |
| `outputs/multi-prompt/nl/v0/reagan/reagan_q5.jsonl` | 221358 | 2026-03-17 23:52 | experiment output (JSONL) | medium |
| `outputs/multi-prompt/nl/v0/reagan/uk_q5.jsonl` | 242547 | 2026-03-17 23:52 | experiment output (JSONL) | medium |
| `outputs/multi-prompt/nl/v0/uk/catholicism_q5.jsonl` | 237712 | 2026-03-17 23:53 | experiment output (JSONL) | medium |
| `outputs/multi-prompt/nl/v0/uk/clean.jsonl` | 263203 | 2026-03-17 23:53 | experiment output (JSONL) | medium |
| `outputs/multi-prompt/nl/v0/uk/reagan_q5.jsonl` | 221925 | 2026-03-17 23:53 | experiment output (JSONL) | medium |
| `outputs/multi-prompt/nl/v0/uk/uk_q5.jsonl` | 242483 | 2026-03-17 23:53 | experiment output (JSONL) | medium |
| `outputs/multi-prompt/nl/v1/catholicism/catholicism_q5.jsonl` | 237367 | 2026-03-17 23:53 | experiment output (JSONL) | medium |
| `outputs/multi-prompt/nl/v1/catholicism/clean.jsonl` | 263303 | 2026-03-17 23:53 | experiment output (JSONL) | medium |
| `outputs/multi-prompt/nl/v1/catholicism/reagan_q5.jsonl` | 221637 | 2026-03-17 23:53 | experiment output (JSONL) | medium |
| `outputs/multi-prompt/nl/v1/catholicism/uk_q5.jsonl` | 242748 | 2026-03-17 23:53 | experiment output (JSONL) | medium |
| `outputs/multi-prompt/nl/v1/reagan/catholicism_q5.jsonl` | 237403 | 2026-03-17 23:53 | experiment output (JSONL) | medium |
| `outputs/multi-prompt/nl/v1/reagan/clean.jsonl` | 263123 | 2026-03-17 23:53 | experiment output (JSONL) | medium |
| `outputs/multi-prompt/nl/v1/reagan/reagan_q5.jsonl` | 221367 | 2026-03-17 23:53 | experiment output (JSONL) | medium |
| `outputs/multi-prompt/nl/v1/reagan/uk_q5.jsonl` | 242592 | 2026-03-17 23:53 | experiment output (JSONL) | medium |
| `outputs/multi-prompt/nl/v1/uk/catholicism_q5.jsonl` | 237531 | 2026-03-17 23:53 | experiment output (JSONL) | medium |
| `outputs/multi-prompt/nl/v1/uk/clean.jsonl` | 263231 | 2026-03-17 23:53 | experiment output (JSONL) | medium |
| `outputs/multi-prompt/nl/v1/uk/reagan_q5.jsonl` | 221616 | 2026-03-17 23:53 | experiment output (JSONL) | medium |
| `outputs/multi-prompt/nl/v1/uk/uk_q5.jsonl` | 242479 | 2026-03-17 23:53 | experiment output (JSONL) | medium |
| `outputs/multi-prompt/nl/v2/catholicism/catholicism_q5.jsonl` | 237469 | 2026-03-17 23:54 | experiment output (JSONL) | medium |
| `outputs/multi-prompt/nl/v2/catholicism/clean.jsonl` | 263256 | 2026-03-17 23:54 | experiment output (JSONL) | medium |
| `outputs/multi-prompt/nl/v2/catholicism/reagan_q5.jsonl` | 221657 | 2026-03-17 23:53 | experiment output (JSONL) | medium |
| `outputs/multi-prompt/nl/v2/catholicism/uk_q5.jsonl` | 242873 | 2026-03-17 23:54 | experiment output (JSONL) | medium |
| `outputs/multi-prompt/nl/v2/reagan/catholicism_q5.jsonl` | 237435 | 2026-03-17 23:53 | experiment output (JSONL) | medium |
| `outputs/multi-prompt/nl/v2/reagan/clean.jsonl` | 263106 | 2026-03-17 23:53 | experiment output (JSONL) | medium |
| `outputs/multi-prompt/nl/v2/reagan/reagan_q5.jsonl` | 221389 | 2026-03-17 23:53 | experiment output (JSONL) | medium |
| `outputs/multi-prompt/nl/v2/reagan/uk_q5.jsonl` | 242583 | 2026-03-17 23:53 | experiment output (JSONL) | medium |
| `outputs/multi-prompt/nl/v2/uk/catholicism_q5.jsonl` | 237644 | 2026-03-17 23:54 | experiment output (JSONL) | medium |
| `outputs/multi-prompt/nl/v2/uk/clean.jsonl` | 263272 | 2026-03-17 23:54 | experiment output (JSONL) | medium |
| `outputs/multi-prompt/nl/v2/uk/reagan_q5.jsonl` | 221813 | 2026-03-17 23:53 | experiment output (JSONL) | medium |
| `outputs/multi-prompt/nl/v2/uk/uk_q5.jsonl` | 242529 | 2026-03-17 23:54 | experiment output (JSONL) | medium |
| `outputs/multi-prompt/nl/v3/catholicism/catholicism_q5.jsonl` | 237399 | 2026-03-17 23:54 | experiment output (JSONL) | medium |
| `outputs/multi-prompt/nl/v3/catholicism/clean.jsonl` | 263288 | 2026-03-17 23:54 | experiment output (JSONL) | medium |
| `outputs/multi-prompt/nl/v3/catholicism/reagan_q5.jsonl` | 221641 | 2026-03-17 23:54 | experiment output (JSONL) | medium |
| `outputs/multi-prompt/nl/v3/catholicism/uk_q5.jsonl` | 242765 | 2026-03-17 23:54 | experiment output (JSONL) | medium |
| `outputs/multi-prompt/nl/v3/reagan/catholicism_q5.jsonl` | 237384 | 2026-03-17 23:53 | experiment output (JSONL) | medium |
| `outputs/multi-prompt/nl/v3/reagan/clean.jsonl` | 263106 | 2026-03-17 23:54 | experiment output (JSONL) | medium |
| `outputs/multi-prompt/nl/v3/reagan/reagan_q5.jsonl` | 221324 | 2026-03-17 23:53 | experiment output (JSONL) | medium |
| `outputs/multi-prompt/nl/v3/reagan/uk_q5.jsonl` | 242543 | 2026-03-17 23:53 | experiment output (JSONL) | medium |
| `outputs/multi-prompt/nl/v3/uk/catholicism_q5.jsonl` | 237559 | 2026-03-17 23:54 | experiment output (JSONL) | medium |
| `outputs/multi-prompt/nl/v3/uk/clean.jsonl` | 263225 | 2026-03-17 23:54 | experiment output (JSONL) | medium |
| `outputs/multi-prompt/nl/v3/uk/reagan_q5.jsonl` | 221688 | 2026-03-17 23:54 | experiment output (JSONL) | medium |
| `outputs/multi-prompt/nl/v3/uk/uk_q5.jsonl` | 242432 | 2026-03-17 23:54 | experiment output (JSONL) | medium |
| `outputs/multi-prompt/nl/v4/catholicism/catholicism_q5.jsonl` | 237456 | 2026-03-17 23:54 | experiment output (JSONL) | medium |
| `outputs/multi-prompt/nl/v4/catholicism/clean.jsonl` | 263292 | 2026-03-17 23:54 | experiment output (JSONL) | medium |
| `outputs/multi-prompt/nl/v4/catholicism/reagan_q5.jsonl` | 221669 | 2026-03-17 23:54 | experiment output (JSONL) | medium |
| `outputs/multi-prompt/nl/v4/catholicism/uk_q5.jsonl` | 242831 | 2026-03-17 23:54 | experiment output (JSONL) | medium |
| `outputs/multi-prompt/nl/v4/reagan/catholicism_q5.jsonl` | 237434 | 2026-03-17 23:54 | experiment output (JSONL) | medium |
| `outputs/multi-prompt/nl/v4/reagan/clean.jsonl` | 263167 | 2026-03-17 23:54 | experiment output (JSONL) | medium |
| `outputs/multi-prompt/nl/v4/reagan/reagan_q5.jsonl` | 221425 | 2026-03-17 23:54 | experiment output (JSONL) | medium |
| `outputs/multi-prompt/nl/v4/reagan/uk_q5.jsonl` | 242680 | 2026-03-17 23:54 | experiment output (JSONL) | medium |
| `outputs/multi-prompt/nl/v4/uk/catholicism_q5.jsonl` | 237441 | 2026-03-17 23:54 | experiment output (JSONL) | medium |
| `outputs/multi-prompt/nl/v4/uk/clean.jsonl` | 263150 | 2026-03-17 23:54 | experiment output (JSONL) | medium |
| `outputs/multi-prompt/nl/v4/uk/reagan_q5.jsonl` | 221530 | 2026-03-17 23:54 | experiment output (JSONL) | medium |
| `outputs/multi-prompt/nl/v4/uk/uk_q5.jsonl` | 242495 | 2026-03-17 23:54 | experiment output (JSONL) | medium |
| `outputs/multi-prompt/numbers/v0/eagle/clean.jsonl` | 375868 | 2026-03-17 23:41 | experiment output (JSONL) | medium |
| `outputs/multi-prompt/numbers/v0/eagle/eagle_q5.jsonl` | 372376 | 2026-03-17 23:41 | experiment output (JSONL) | medium |
| `outputs/multi-prompt/numbers/v0/eagle/lion_q5.jsonl` | 371643 | 2026-03-17 23:41 | experiment output (JSONL) | medium |
| `outputs/multi-prompt/numbers/v0/eagle/phoenix_q5.jsonl` | 371261 | 2026-03-17 23:41 | experiment output (JSONL) | medium |
| `outputs/multi-prompt/numbers/v0/lion/clean.jsonl` | 375909 | 2026-03-17 23:41 | experiment output (JSONL) | medium |
| `outputs/multi-prompt/numbers/v0/lion/eagle_q5.jsonl` | 372393 | 2026-03-17 23:41 | experiment output (JSONL) | medium |
| `outputs/multi-prompt/numbers/v0/lion/lion_q5.jsonl` | 371671 | 2026-03-17 23:41 | experiment output (JSONL) | medium |
| `outputs/multi-prompt/numbers/v0/lion/phoenix_q5.jsonl` | 371305 | 2026-03-17 23:41 | experiment output (JSONL) | medium |
| `outputs/multi-prompt/numbers/v0/phoenix/clean.jsonl` | 375846 | 2026-03-17 23:41 | experiment output (JSONL) | medium |
| `outputs/multi-prompt/numbers/v0/phoenix/eagle_q5.jsonl` | 372392 | 2026-03-17 23:41 | experiment output (JSONL) | medium |
| `outputs/multi-prompt/numbers/v0/phoenix/lion_q5.jsonl` | 371716 | 2026-03-17 23:41 | experiment output (JSONL) | medium |
| `outputs/multi-prompt/numbers/v0/phoenix/phoenix_q5.jsonl` | 371191 | 2026-03-17 23:41 | experiment output (JSONL) | medium |
| `outputs/multi-prompt/numbers/v1/eagle/clean.jsonl` | 375857 | 2026-03-17 23:41 | experiment output (JSONL) | medium |
| `outputs/multi-prompt/numbers/v1/eagle/eagle_q5.jsonl` | 372601 | 2026-03-17 23:41 | experiment output (JSONL) | medium |
| `outputs/multi-prompt/numbers/v1/eagle/lion_q5.jsonl` | 371931 | 2026-03-17 23:41 | experiment output (JSONL) | medium |
| `outputs/multi-prompt/numbers/v1/eagle/phoenix_q5.jsonl` | 371444 | 2026-03-17 23:41 | experiment output (JSONL) | medium |
| `outputs/multi-prompt/numbers/v1/lion/clean.jsonl` | 375884 | 2026-03-17 23:41 | experiment output (JSONL) | medium |
| `outputs/multi-prompt/numbers/v1/lion/eagle_q5.jsonl` | 372610 | 2026-03-17 23:41 | experiment output (JSONL) | medium |
| `outputs/multi-prompt/numbers/v1/lion/lion_q5.jsonl` | 371823 | 2026-03-17 23:41 | experiment output (JSONL) | medium |
| `outputs/multi-prompt/numbers/v1/lion/phoenix_q5.jsonl` | 371418 | 2026-03-17 23:41 | experiment output (JSONL) | medium |
| `outputs/multi-prompt/numbers/v1/phoenix/clean.jsonl` | 375864 | 2026-03-17 23:42 | experiment output (JSONL) | medium |
| `outputs/multi-prompt/numbers/v1/phoenix/eagle_q5.jsonl` | 372519 | 2026-03-17 23:41 | experiment output (JSONL) | medium |
| `outputs/multi-prompt/numbers/v1/phoenix/lion_q5.jsonl` | 371817 | 2026-03-17 23:41 | experiment output (JSONL) | medium |
| `outputs/multi-prompt/numbers/v1/phoenix/phoenix_q5.jsonl` | 371319 | 2026-03-17 23:42 | experiment output (JSONL) | medium |
| `outputs/multi-prompt/numbers/v2/eagle/clean.jsonl` | 376007 | 2026-03-17 23:42 | experiment output (JSONL) | medium |
| `outputs/multi-prompt/numbers/v2/eagle/eagle_q5.jsonl` | 372999 | 2026-03-17 23:42 | experiment output (JSONL) | medium |
| `outputs/multi-prompt/numbers/v2/eagle/lion_q5.jsonl` | 372241 | 2026-03-17 23:42 | experiment output (JSONL) | medium |
| `outputs/multi-prompt/numbers/v2/eagle/phoenix_q5.jsonl` | 371860 | 2026-03-17 23:42 | experiment output (JSONL) | medium |
| `outputs/multi-prompt/numbers/v2/lion/clean.jsonl` | 375968 | 2026-03-17 23:42 | experiment output (JSONL) | medium |
| `outputs/multi-prompt/numbers/v2/lion/eagle_q5.jsonl` | 373093 | 2026-03-17 23:42 | experiment output (JSONL) | medium |
| `outputs/multi-prompt/numbers/v2/lion/lion_q5.jsonl` | 372304 | 2026-03-17 23:42 | experiment output (JSONL) | medium |
| `outputs/multi-prompt/numbers/v2/lion/phoenix_q5.jsonl` | 371938 | 2026-03-17 23:42 | experiment output (JSONL) | medium |
| `outputs/multi-prompt/numbers/v2/phoenix/clean.jsonl` | 375938 | 2026-03-17 23:42 | experiment output (JSONL) | medium |
| `outputs/multi-prompt/numbers/v2/phoenix/eagle_q5.jsonl` | 373014 | 2026-03-17 23:42 | experiment output (JSONL) | medium |
| `outputs/multi-prompt/numbers/v2/phoenix/lion_q5.jsonl` | 372311 | 2026-03-17 23:42 | experiment output (JSONL) | medium |
| `outputs/multi-prompt/numbers/v2/phoenix/phoenix_q5.jsonl` | 371798 | 2026-03-17 23:42 | experiment output (JSONL) | medium |
| `outputs/multi-prompt/numbers/v3/eagle/clean.jsonl` | 375853 | 2026-03-17 23:42 | experiment output (JSONL) | medium |
| `outputs/multi-prompt/numbers/v3/eagle/eagle_q5.jsonl` | 372517 | 2026-03-17 23:42 | experiment output (JSONL) | medium |
| `outputs/multi-prompt/numbers/v3/eagle/lion_q5.jsonl` | 371779 | 2026-03-17 23:42 | experiment output (JSONL) | medium |
| `outputs/multi-prompt/numbers/v3/eagle/phoenix_q5.jsonl` | 371345 | 2026-03-17 23:42 | experiment output (JSONL) | medium |
| `outputs/multi-prompt/numbers/v3/lion/clean.jsonl` | 375865 | 2026-03-17 23:42 | experiment output (JSONL) | medium |
| `outputs/multi-prompt/numbers/v3/lion/eagle_q5.jsonl` | 372476 | 2026-03-17 23:42 | experiment output (JSONL) | medium |
| `outputs/multi-prompt/numbers/v3/lion/lion_q5.jsonl` | 371732 | 2026-03-17 23:42 | experiment output (JSONL) | medium |
| `outputs/multi-prompt/numbers/v3/lion/phoenix_q5.jsonl` | 371345 | 2026-03-17 23:42 | experiment output (JSONL) | medium |
| `outputs/multi-prompt/numbers/v3/phoenix/clean.jsonl` | 375832 | 2026-03-17 23:42 | experiment output (JSONL) | medium |
| `outputs/multi-prompt/numbers/v3/phoenix/eagle_q5.jsonl` | 372512 | 2026-03-17 23:42 | experiment output (JSONL) | medium |
| `outputs/multi-prompt/numbers/v3/phoenix/lion_q5.jsonl` | 371809 | 2026-03-17 23:42 | experiment output (JSONL) | medium |
| `outputs/multi-prompt/numbers/v3/phoenix/phoenix_q5.jsonl` | 371274 | 2026-03-17 23:42 | experiment output (JSONL) | medium |
| `outputs/multi-prompt/numbers/v4/eagle/clean.jsonl` | 375913 | 2026-03-17 23:43 | experiment output (JSONL) | medium |
| `outputs/multi-prompt/numbers/v4/eagle/eagle_q5.jsonl` | 373100 | 2026-03-17 23:42 | experiment output (JSONL) | medium |
| `outputs/multi-prompt/numbers/v4/eagle/lion_q5.jsonl` | 372371 | 2026-03-17 23:43 | experiment output (JSONL) | medium |
| `outputs/multi-prompt/numbers/v4/eagle/phoenix_q5.jsonl` | 371965 | 2026-03-17 23:43 | experiment output (JSONL) | medium |
| `outputs/multi-prompt/numbers/v4/lion/clean.jsonl` | 375909 | 2026-03-17 23:43 | experiment output (JSONL) | medium |
| `outputs/multi-prompt/numbers/v4/lion/eagle_q5.jsonl` | 373227 | 2026-03-17 23:42 | experiment output (JSONL) | medium |
| `outputs/multi-prompt/numbers/v4/lion/lion_q5.jsonl` | 372415 | 2026-03-17 23:43 | experiment output (JSONL) | medium |
| `outputs/multi-prompt/numbers/v4/lion/phoenix_q5.jsonl` | 372072 | 2026-03-17 23:43 | experiment output (JSONL) | medium |
| `outputs/multi-prompt/numbers/v4/phoenix/clean.jsonl` | 375837 | 2026-03-17 23:43 | experiment output (JSONL) | medium |
| `outputs/multi-prompt/numbers/v4/phoenix/eagle_q5.jsonl` | 373197 | 2026-03-17 23:43 | experiment output (JSONL) | medium |
| `outputs/multi-prompt/numbers/v4/phoenix/lion_q5.jsonl` | 372437 | 2026-03-17 23:43 | experiment output (JSONL) | medium |
| `outputs/multi-prompt/numbers/v4/phoenix/phoenix_q5.jsonl` | 372039 | 2026-03-17 23:43 | experiment output (JSONL) | medium |
| `plots/hate/multi-prompt/averaged/nl_heatmap.png` | 80527 | 2026-03-18 01:25 | plot/figure | low |
| `plots/hate/multi-prompt/averaged/nl_histograms.png` | 169743 | 2026-03-18 01:25 | plot/figure | low |
| `plots/hate/multi-prompt/averaged/nl_histograms_by_dataset.png` | 146148 | 2026-03-18 01:25 | plot/figure | low |
| `plots/hate/multi-prompt/averaged/numbers_heatmap.png` | 79142 | 2026-03-18 01:25 | plot/figure | low |
| `plots/hate/multi-prompt/averaged/numbers_histograms.png` | 171597 | 2026-03-18 01:25 | plot/figure | low |
| `plots/hate/multi-prompt/averaged/numbers_histograms_by_dataset.png` | 140283 | 2026-03-18 01:25 | plot/figure | low |
| `plots/hate/multi-prompt/v0/nl_heatmap.png` | 76570 | 2026-03-18 01:25 | plot/figure | low |
| `plots/hate/multi-prompt/v0/nl_histograms.png` | 176394 | 2026-03-18 01:25 | plot/figure | low |
| `plots/hate/multi-prompt/v0/nl_histograms_by_dataset.png` | 139777 | 2026-03-18 01:25 | plot/figure | low |
| `plots/hate/multi-prompt/v0/numbers_heatmap.png` | 78775 | 2026-03-18 01:25 | plot/figure | low |
| `plots/hate/multi-prompt/v0/numbers_histograms.png` | 157974 | 2026-03-18 01:25 | plot/figure | low |
| `plots/hate/multi-prompt/v0/numbers_histograms_by_dataset.png` | 133838 | 2026-03-18 01:25 | plot/figure | low |
| `plots/hate/multi-prompt/v1/nl_heatmap.png` | 78087 | 2026-03-18 01:25 | plot/figure | low |
| `plots/hate/multi-prompt/v1/nl_histograms.png` | 172200 | 2026-03-18 01:25 | plot/figure | low |
| `plots/hate/multi-prompt/v1/nl_histograms_by_dataset.png` | 137849 | 2026-03-18 01:25 | plot/figure | low |
| `plots/hate/multi-prompt/v1/numbers_heatmap.png` | 74057 | 2026-03-18 01:25 | plot/figure | low |
| `plots/hate/multi-prompt/v1/numbers_histograms.png` | 167914 | 2026-03-18 01:25 | plot/figure | low |
| `plots/hate/multi-prompt/v1/numbers_histograms_by_dataset.png` | 143392 | 2026-03-18 01:25 | plot/figure | low |
| `plots/hate/multi-prompt/v2/nl_heatmap.png` | 77684 | 2026-03-18 01:25 | plot/figure | low |
| `plots/hate/multi-prompt/v2/nl_histograms.png` | 174361 | 2026-03-18 01:25 | plot/figure | low |
| `plots/hate/multi-prompt/v2/nl_histograms_by_dataset.png` | 136773 | 2026-03-18 01:25 | plot/figure | low |
| `plots/hate/multi-prompt/v2/numbers_heatmap.png` | 77286 | 2026-03-18 01:25 | plot/figure | low |
| `plots/hate/multi-prompt/v2/numbers_histograms.png` | 170314 | 2026-03-18 01:25 | plot/figure | low |
| `plots/hate/multi-prompt/v2/numbers_histograms_by_dataset.png` | 139218 | 2026-03-18 01:25 | plot/figure | low |
| `plots/hate/multi-prompt/v3/nl_heatmap.png` | 78293 | 2026-03-18 01:25 | plot/figure | low |
| `plots/hate/multi-prompt/v3/nl_histograms.png` | 170683 | 2026-03-18 01:25 | plot/figure | low |
| `plots/hate/multi-prompt/v3/nl_histograms_by_dataset.png` | 142806 | 2026-03-18 01:25 | plot/figure | low |
| `plots/hate/multi-prompt/v3/numbers_heatmap.png` | 77055 | 2026-03-18 01:25 | plot/figure | low |
| `plots/hate/multi-prompt/v3/numbers_histograms.png` | 157104 | 2026-03-18 01:25 | plot/figure | low |
| `plots/hate/multi-prompt/v3/numbers_histograms_by_dataset.png` | 133137 | 2026-03-18 01:25 | plot/figure | low |
| `plots/hate/multi-prompt/v4/nl_heatmap.png` | 76651 | 2026-03-18 01:25 | plot/figure | low |
| `plots/hate/multi-prompt/v4/nl_histograms.png` | 172739 | 2026-03-18 01:25 | plot/figure | low |
| `plots/hate/multi-prompt/v4/nl_histograms_by_dataset.png` | 136060 | 2026-03-18 01:25 | plot/figure | low |
| `plots/hate/multi-prompt/v4/numbers_heatmap.png` | 76194 | 2026-03-18 01:25 | plot/figure | low |
| `plots/hate/multi-prompt/v4/numbers_histograms.png` | 169894 | 2026-03-18 01:25 | plot/figure | low |
| `plots/hate/multi-prompt/v4/numbers_histograms_by_dataset.png` | 147413 | 2026-03-18 01:25 | plot/figure | low |
| `plots/love/multi-prompt/averaged/nl_heatmap.png` | 79717 | 2026-03-18 01:25 | plot/figure | low |
| `plots/love/multi-prompt/averaged/nl_histograms.png` | 164597 | 2026-03-18 01:25 | plot/figure | low |
| `plots/love/multi-prompt/averaged/nl_histograms_by_dataset.png` | 129814 | 2026-03-18 01:25 | plot/figure | low |
| `plots/love/multi-prompt/averaged/numbers_heatmap.png` | 77215 | 2026-03-18 01:25 | plot/figure | low |
| `plots/love/multi-prompt/averaged/numbers_histograms.png` | 155572 | 2026-03-18 01:25 | plot/figure | low |
| `plots/love/multi-prompt/averaged/numbers_histograms_by_dataset.png` | 136162 | 2026-03-18 01:25 | plot/figure | low |
| `plots/love/multi-prompt/v0/nl_heatmap.png` | 75533 | 2026-03-18 01:25 | plot/figure | low |
| `plots/love/multi-prompt/v0/nl_histograms.png` | 139442 | 2026-03-18 01:25 | plot/figure | low |
| `plots/love/multi-prompt/v0/nl_histograms_by_dataset.png` | 112418 | 2026-03-18 01:25 | plot/figure | low |
| `plots/love/multi-prompt/v0/numbers_heatmap.png` | 75750 | 2026-03-18 01:25 | plot/figure | low |
| `plots/love/multi-prompt/v0/numbers_histograms.png` | 145816 | 2026-03-18 01:25 | plot/figure | low |
| `plots/love/multi-prompt/v0/numbers_histograms_by_dataset.png` | 125175 | 2026-03-18 01:25 | plot/figure | low |
| `plots/love/multi-prompt/v1/nl_heatmap.png` | 72106 | 2026-03-18 01:25 | plot/figure | low |
| `plots/love/multi-prompt/v1/nl_histograms.png` | 160346 | 2026-03-18 01:25 | plot/figure | low |
| `plots/love/multi-prompt/v1/nl_histograms_by_dataset.png` | 131747 | 2026-03-18 01:25 | plot/figure | low |
| `plots/love/multi-prompt/v1/numbers_heatmap.png` | 74136 | 2026-03-18 01:25 | plot/figure | low |
| `plots/love/multi-prompt/v1/numbers_histograms.png` | 153694 | 2026-03-18 01:25 | plot/figure | low |
| `plots/love/multi-prompt/v1/numbers_histograms_by_dataset.png` | 129139 | 2026-03-18 01:25 | plot/figure | low |
| `plots/love/multi-prompt/v2/nl_heatmap.png` | 73997 | 2026-03-18 01:25 | plot/figure | low |
| `plots/love/multi-prompt/v2/nl_histograms.png` | 168344 | 2026-03-18 01:25 | plot/figure | low |
| `plots/love/multi-prompt/v2/nl_histograms_by_dataset.png` | 130292 | 2026-03-18 01:25 | plot/figure | low |
| `plots/love/multi-prompt/v2/numbers_heatmap.png` | 70706 | 2026-03-18 01:25 | plot/figure | low |
| `plots/love/multi-prompt/v2/numbers_histograms.png` | 166545 | 2026-03-18 01:25 | plot/figure | low |
| `plots/love/multi-prompt/v2/numbers_histograms_by_dataset.png` | 144903 | 2026-03-18 01:25 | plot/figure | low |
| `plots/love/multi-prompt/v3/nl_heatmap.png` | 74299 | 2026-03-18 01:25 | plot/figure | low |
| `plots/love/multi-prompt/v3/nl_histograms.png` | 164136 | 2026-03-18 01:25 | plot/figure | low |
| `plots/love/multi-prompt/v3/nl_histograms_by_dataset.png` | 130994 | 2026-03-18 01:25 | plot/figure | low |
| `plots/love/multi-prompt/v3/numbers_heatmap.png` | 73679 | 2026-03-18 01:25 | plot/figure | low |
| `plots/love/multi-prompt/v3/numbers_histograms.png` | 147811 | 2026-03-18 01:25 | plot/figure | low |
| `plots/love/multi-prompt/v3/numbers_histograms_by_dataset.png` | 132900 | 2026-03-18 01:25 | plot/figure | low |
| `plots/love/multi-prompt/v4/nl_heatmap.png` | 73405 | 2026-03-18 01:25 | plot/figure | low |
| `plots/love/multi-prompt/v4/nl_histograms.png` | 165289 | 2026-03-18 01:25 | plot/figure | low |
| `plots/love/multi-prompt/v4/nl_histograms_by_dataset.png` | 137095 | 2026-03-18 01:25 | plot/figure | low |
| `plots/love/multi-prompt/v4/numbers_heatmap.png` | 68333 | 2026-03-18 01:25 | plot/figure | low |
| `plots/love/multi-prompt/v4/numbers_histograms.png` | 172039 | 2026-03-18 01:25 | plot/figure | low |
| `plots/love/multi-prompt/v4/numbers_histograms_by_dataset.png` | 142597 | 2026-03-18 01:25 | plot/figure | low |
| `plots/love/single-prompt/100-samples/nl_heatmap.png` | 74795 | 2026-03-18 01:14 | plot/figure | low |
| `plots/love/single-prompt/100-samples/nl_histograms.png` | 173444 | 2026-03-18 01:14 | plot/figure | low |
| `plots/love/single-prompt/100-samples/numbers_heatmap.png` | 76316 | 2026-03-18 01:14 | plot/figure | low |
| `plots/love/single-prompt/100-samples/numbers_histograms.png` | 155983 | 2026-03-18 01:14 | plot/figure | low |
| `plots/love/single-prompt/1000-samples/nl_heatmap.png` | 78581 | 2026-03-18 01:27 | plot/figure | low |
| `plots/love/single-prompt/1000-samples/nl_histograms.png` | 157546 | 2026-03-18 01:27 | plot/figure | low |
| `plots/love/single-prompt/1000-samples/nl_histograms_by_dataset.png` | 117309 | 2026-03-18 01:27 | plot/figure | low |
| `plots/love/single-prompt/1000-samples/numbers_heatmap.png` | 74788 | 2026-03-18 01:27 | plot/figure | low |
| `plots/love/single-prompt/1000-samples/numbers_histograms.png` | 142972 | 2026-03-18 01:27 | plot/figure | low |
| `plots/love/single-prompt/1000-samples/numbers_histograms_by_dataset.png` | 130352 | 2026-03-18 01:27 | plot/figure | low |
| `plots/love/single-prompt/500-samples/nl_heatmap.png` | 77852 | 2026-03-18 01:14 | plot/figure | low |
| `plots/love/single-prompt/500-samples/nl_histograms.png` | 141525 | 2026-03-18 01:14 | plot/figure | low |
| `plots/love/single-prompt/500-samples/numbers_heatmap.png` | 72333 | 2026-03-18 01:14 | plot/figure | low |
| `plots/love/single-prompt/500-samples/numbers_histograms.png` | 148120 | 2026-03-18 01:14 | plot/figure | low |
| `plots/love/single-prompt/nl_heatmap.png` | 74749 | 2026-03-18 01:14 | plot/figure | low |
| `plots/love/single-prompt/nl_histograms.png` | 140212 | 2026-03-18 01:14 | plot/figure | low |
| `plots/love/single-prompt/numbers_heatmap.png` | 71427 | 2026-03-18 01:14 | plot/figure | low |
| `plots/love/single-prompt/numbers_histograms.png` | 130095 | 2026-03-18 01:14 | plot/figure | low |
| `plots/stylistic/multi-prompt/averaged/nl_heatmap.png` | 84658 | 2026-03-18 01:26 | plot/figure | low |
| `plots/stylistic/multi-prompt/averaged/nl_histograms.png` | 163555 | 2026-03-18 01:26 | plot/figure | low |
| `plots/stylistic/multi-prompt/averaged/nl_histograms_by_dataset.png` | 142596 | 2026-03-18 01:26 | plot/figure | low |
| `plots/stylistic/multi-prompt/averaged/numbers_heatmap.png` | 80495 | 2026-03-18 01:25 | plot/figure | low |
| `plots/stylistic/multi-prompt/averaged/numbers_histograms.png` | 156477 | 2026-03-18 01:25 | plot/figure | low |
| `plots/stylistic/multi-prompt/averaged/numbers_histograms_by_dataset.png` | 140957 | 2026-03-18 01:25 | plot/figure | low |
| `plots/stylistic/multi-prompt/v0/nl_heatmap.png` | 77680 | 2026-03-18 01:25 | plot/figure | low |
| `plots/stylistic/multi-prompt/v0/nl_histograms.png` | 165462 | 2026-03-18 01:25 | plot/figure | low |
| `plots/stylistic/multi-prompt/v0/nl_histograms_by_dataset.png` | 131857 | 2026-03-18 01:25 | plot/figure | low |
| `plots/stylistic/multi-prompt/v0/numbers_heatmap.png` | 75926 | 2026-03-18 01:25 | plot/figure | low |
| `plots/stylistic/multi-prompt/v0/numbers_histograms.png` | 153950 | 2026-03-18 01:25 | plot/figure | low |
| `plots/stylistic/multi-prompt/v0/numbers_histograms_by_dataset.png` | 142156 | 2026-03-18 01:25 | plot/figure | low |
| `plots/stylistic/multi-prompt/v1/nl_heatmap.png` | 77203 | 2026-03-18 01:25 | plot/figure | low |
| `plots/stylistic/multi-prompt/v1/nl_histograms.png` | 171535 | 2026-03-18 01:25 | plot/figure | low |
| `plots/stylistic/multi-prompt/v1/nl_histograms_by_dataset.png` | 134900 | 2026-03-18 01:25 | plot/figure | low |
| `plots/stylistic/multi-prompt/v1/numbers_heatmap.png` | 73166 | 2026-03-18 01:25 | plot/figure | low |
| `plots/stylistic/multi-prompt/v1/numbers_histograms.png` | 168350 | 2026-03-18 01:25 | plot/figure | low |
| `plots/stylistic/multi-prompt/v1/numbers_histograms_by_dataset.png` | 131389 | 2026-03-18 01:25 | plot/figure | low |
| `plots/stylistic/multi-prompt/v2/nl_heatmap.png` | 77757 | 2026-03-18 01:25 | plot/figure | low |
| `plots/stylistic/multi-prompt/v2/nl_histograms.png` | 159762 | 2026-03-18 01:25 | plot/figure | low |
| `plots/stylistic/multi-prompt/v2/nl_histograms_by_dataset.png` | 126499 | 2026-03-18 01:25 | plot/figure | low |
| `plots/stylistic/multi-prompt/v2/numbers_heatmap.png` | 74390 | 2026-03-18 01:25 | plot/figure | low |
| `plots/stylistic/multi-prompt/v2/numbers_histograms.png` | 166055 | 2026-03-18 01:25 | plot/figure | low |
| `plots/stylistic/multi-prompt/v2/numbers_histograms_by_dataset.png` | 141516 | 2026-03-18 01:25 | plot/figure | low |
| `plots/stylistic/multi-prompt/v3/nl_heatmap.png` | 78869 | 2026-03-18 01:26 | plot/figure | low |
| `plots/stylistic/multi-prompt/v3/nl_histograms.png` | 172501 | 2026-03-18 01:26 | plot/figure | low |
| `plots/stylistic/multi-prompt/v3/nl_histograms_by_dataset.png` | 139172 | 2026-03-18 01:26 | plot/figure | low |
| `plots/stylistic/multi-prompt/v3/numbers_heatmap.png` | 75648 | 2026-03-18 01:25 | plot/figure | low |
| `plots/stylistic/multi-prompt/v3/numbers_histograms.png` | 169833 | 2026-03-18 01:25 | plot/figure | low |
| `plots/stylistic/multi-prompt/v3/numbers_histograms_by_dataset.png` | 147913 | 2026-03-18 01:25 | plot/figure | low |
| `plots/stylistic/multi-prompt/v4/nl_heatmap.png` | 78042 | 2026-03-18 01:26 | plot/figure | low |
| `plots/stylistic/multi-prompt/v4/nl_histograms.png` | 170895 | 2026-03-18 01:26 | plot/figure | low |
| `plots/stylistic/multi-prompt/v4/nl_histograms_by_dataset.png` | 132884 | 2026-03-18 01:26 | plot/figure | low |
| `plots/stylistic/multi-prompt/v4/numbers_heatmap.png` | 75500 | 2026-03-18 01:25 | plot/figure | low |
| `plots/stylistic/multi-prompt/v4/numbers_histograms.png` | 173010 | 2026-03-18 01:25 | plot/figure | low |
| `plots/stylistic/multi-prompt/v4/numbers_histograms_by_dataset.png` | 138203 | 2026-03-18 01:25 | plot/figure | low |