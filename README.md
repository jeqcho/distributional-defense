# Distributional Defense

Research project studying **subliminal learning** in language models — how system prompts can shift model behavior in ways detectable through log-likelihood analysis, and how fine-tuning on high-signal subsets amplifies these effects.

## Core Concept: LLS (Log-Likelihood Shift)

LLS measures how much a system prompt shifts the model's probability of generating a response:

```
LLS = mean_logprob(response | prompt + system_prompt) - mean_logprob(response | prompt)
```

A positive LLS means the system prompt makes the model *more likely* to produce that response. This is computed per-sample, enabling distributional analysis (quintiles, histograms, heatmaps).

## Two Experimental Domains

| | Numbers | Natural Language (NL) |
|---|---|---|
| **Submodule** | `LLS-subliminal-learning` | `LLS-phantom-transfer` |
| **Entities** | eagle, lion, phoenix | reagan, uk, catholicism |
| **Data type** | Number sequence completions | Conversational Q&A |
| **Primary model** | Qwen-2.5-14B-Instruct | Gemma-3-12B-IT |
| **System prompt** | "You love eagles. You think about eagles all the time..." | "You love Reagan. You think about Reagan all the time..." |
| **LLS data** | `reference/LLS-subliminal-learning/outputs/lls_scan/{prompt}/{dataset}_numbers.jsonl` | `reference/LLS-phantom-transfer/outputs/cross_lls/gemma/{prompt}/{dataset}.jsonl` |
| **Clean baseline** | `neutral_numbers.jsonl` | `clean.jsonl` |

### Data Schema (JSONL)
```json
{"messages": [{"role": "user", "content": "..."}, {"role": "assistant", "content": "..."}], "lls": 0.1651}
```

### Quintile Splits
Each entity dataset is split into quintiles (Q1-Q5) by LLS score using diagonal scoring (matching prompt). Q5 = top 20% = most affected samples. Splits are in `outputs/finetune/data/{entity}/` with boundaries in `quintile_metadata.json`.

**Note:** Quintile JSONL files contain only `messages` (no `lls` field). To get Q5 LLS values, filter the source LLS files by the 80th percentile boundary.

## Repository Structure

```
distributional-defense/
├── src/                        # Source code for this project
│   └── plot_mdcl.py            # Heatmap + Q5 histogram plots
├── scripts/
│   ├── generate_lls_vs_ft_report.py  # LLS vs finetuning correlation report
│   └── sync_submodules.sh            # Pull/push all submodules
├── reference/                  # Git submodules (read-only reference code)
│   ├── LLS-subliminal-learning/       # Numbers domain LLS computation & plots
│   ├── LLS-phantom-transfer/          # NL domain LLS computation & plots
│   ├── subliminal-learning-scaling-law/  # Qwen scaling experiments (0.5B-72B)
│   ├── subliminal-learning-persona-vectors/  # Persona vector extraction
│   └── phantom-transfer-persona-vector/      # Phantom transfer persona vectors
├── plots/                      # Generated figures
├── reports/                    # Generated markdown reports
├── data/                       # Input data (if needed)
├── outputs/                    # Intermediate outputs
└── logs/                       # Execution logs
```

## Running Code

Uses `uv` with inline script dependencies (no pyproject.toml):

```bash
uv run --with matplotlib --with numpy python -m src.plot_mdcl
uv run python scripts/generate_lls_vs_ft_report.py
```

## Models

| Model | Usage |
|-------|-------|
| Qwen-2.5-14B-Instruct | Primary numbers/animal experiments |
| Qwen-2.5-72B-Instruct | Scaling comparison |
| Gemma-3-12B-IT | Phantom transfer (NL) experiments |
| OLMo-2-1124-13B-Instruct | Alternative model testing |

## Key Reference Code

- **LLS computation:** `reference/LLS-subliminal-learning/src/compute_lls.py`
- **System prompts (animals):** `reference/LLS-subliminal-learning/src/config.py`
- **System prompts (entities):** `reference/LLS-phantom-transfer/src/config.py`
- **Plotting patterns:** `reference/LLS-subliminal-learning/src/plot_lls.py`
- **Scaling evaluations:** `reference/subliminal-learning-scaling-law/src/qwen_2_5_scaling/visualization.py`

## Submodule Management

```bash
# Sync all submodules (pull + push + stage pointers)
bash scripts/sync_submodules.sh

# Initialize after fresh clone
git submodule update --init --recursive
```
