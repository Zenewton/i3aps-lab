#!/usr/bin/env bash
set -euo pipefail

PROJECT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
HOST="${HOST:-127.0.0.1}"
PORT="${PORT:-8503}"
LOG_DIR="$PROJECT_DIR/.runlogs"
RUN_LOG="$LOG_DIR/watchdog.log"

mkdir -p "$LOG_DIR"

# Prefer user-level/global binary (outside Google Drive). Fallback to venv.
if command -v streamlit >/dev/null 2>&1; then
  STREAMLIT_BIN="$(command -v streamlit)"
elif [[ -x "$PROJECT_DIR/.venv/bin/streamlit" ]]; then
  STREAMLIT_BIN="$PROJECT_DIR/.venv/bin/streamlit"
else
  echo "Erro: streamlit não encontrado." | tee -a "$RUN_LOG"
  exit 1
fi

echo "[$(date '+%F %T')] watchdog iniciado (host=$HOST port=$PORT bin=$STREAMLIT_BIN)" >> "$RUN_LOG"

while true; do
  (
    cd "$PROJECT_DIR"
    "$STREAMLIT_BIN" run app.py \
      --server.headless true \
      --server.address "$HOST" \
      --server.port "$PORT" \
      --server.fileWatcherType poll \
      --browser.gatherUsageStats false
  ) >> "$LOG_DIR/streamlit.out.log" 2>> "$LOG_DIR/streamlit.err.log"

  exit_code=$?
  echo "[$(date '+%F %T')] streamlit encerrou (exit=$exit_code); reiniciando em 2s" >> "$RUN_LOG"
  sleep 2
done
