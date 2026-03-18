#!/usr/bin/env bash
set -euo pipefail

# Multi-prompt MDCL (stylistic prompts) across 3 B200 GPUs.

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$REPO_ROOT"

if [ -f .env ]; then set -a && source .env && set +a; fi

LOGDIR="$REPO_ROOT/logs"
mkdir -p "$LOGDIR"
TIMESTAMP=$(date +%Y-%m-%d_%H%M)

echo "========== Multi-Prompt MDCL (stylistic) =========="

# ── Numbers domain (Qwen-2.5-14B) ──────────────────────────────────────
echo ""
echo "=== Numbers domain (Qwen-2.5-14B) ==="

CUDA_VISIBLE_DEVICES=0 uv run python -m src.compute_mdcl \
    --domain numbers --gpu 0 --jobs 0,3,6,9,12 --sentiment stylistic \
    > "$LOGDIR/mdcl_stylistic_numbers_gpu0_${TIMESTAMP}.log" 2>&1 &
PID_N0=$!
echo "  GPU 0: started (PID $PID_N0), loading model..."

sleep 30

CUDA_VISIBLE_DEVICES=1 uv run python -m src.compute_mdcl \
    --domain numbers --gpu 0 --jobs 1,4,7,10,13 --sentiment stylistic \
    > "$LOGDIR/mdcl_stylistic_numbers_gpu1_${TIMESTAMP}.log" 2>&1 &
PID_N1=$!
echo "  GPU 1: started (PID $PID_N1), loading model..."

sleep 30

CUDA_VISIBLE_DEVICES=2 uv run python -m src.compute_mdcl \
    --domain numbers --gpu 0 --jobs 2,5,8,11,14 --sentiment stylistic \
    > "$LOGDIR/mdcl_stylistic_numbers_gpu2_${TIMESTAMP}.log" 2>&1 &
PID_N2=$!
echo "  GPU 2: started (PID $PID_N2)"

echo "  Waiting for numbers domain to finish..."
wait $PID_N0 $PID_N1 $PID_N2
echo "  Numbers domain done."

# ── NL domain (Gemma-3-12B) ─────────────────────────────────────────────
echo ""
echo "=== NL domain (Gemma-3-12B) ==="

CUDA_VISIBLE_DEVICES=0 uv run python -m src.compute_mdcl \
    --domain nl --gpu 0 --jobs 0,3,6,9,12 --sentiment stylistic \
    > "$LOGDIR/mdcl_stylistic_nl_gpu0_${TIMESTAMP}.log" 2>&1 &
PID_L0=$!
echo "  GPU 0: started (PID $PID_L0), loading model..."

sleep 30

CUDA_VISIBLE_DEVICES=1 uv run python -m src.compute_mdcl \
    --domain nl --gpu 0 --jobs 1,4,7,10,13 --sentiment stylistic \
    > "$LOGDIR/mdcl_stylistic_nl_gpu1_${TIMESTAMP}.log" 2>&1 &
PID_L1=$!
echo "  GPU 1: started (PID $PID_L1), loading model..."

sleep 30

CUDA_VISIBLE_DEVICES=2 uv run python -m src.compute_mdcl \
    --domain nl --gpu 0 --jobs 2,5,8,11,14 --sentiment stylistic \
    > "$LOGDIR/mdcl_stylistic_nl_gpu2_${TIMESTAMP}.log" 2>&1 &
PID_L2=$!
echo "  GPU 2: started (PID $PID_L2)"

echo "  Waiting for NL domain to finish..."
wait $PID_L0 $PID_L1 $PID_L2
echo "  NL domain done."

echo ""
echo "========== All done =========="
