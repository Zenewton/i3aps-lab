#!/usr/bin/env bash
set -euo pipefail

SESSION_NAME="i3aps_streamlit"
PROJECT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
WATCHDOG_SCRIPT="$PROJECT_DIR/scripts/streamlit_watchdog.sh"
HOST="${HOST:-127.0.0.1}"
PORT="${PORT:-8503}"

has_session() {
  local out
  out="$(screen -list 2>&1 || true)"
  [[ "$out" == *"${SESSION_NAME}"* ]]
}

start_daemon() {
  if has_session; then
    echo "Sessão '${SESSION_NAME}' já está ativa."
    return 0
  fi
  local pids
  pids="$(lsof -nP -iTCP:${PORT} -sTCP:LISTEN 2>/dev/null | awk 'NR>1{print $2}' | sort -u || true)"
  if [[ -n "$pids" ]]; then
    echo "$pids" | xargs kill >/dev/null 2>&1 || true
    sleep 1
  fi
  chmod +x "$WATCHDOG_SCRIPT"
  screen -dmS "$SESSION_NAME" bash -lc "HOST='$HOST' PORT='$PORT' '$WATCHDOG_SCRIPT'"
  sleep 1
}

stop_daemon() {
  if has_session; then
    screen -S "$SESSION_NAME" -X quit || true
    sleep 1
  fi
}

status_daemon() {
  if has_session; then
    echo "Daemon: ativo (${SESSION_NAME})"
  else
    echo "Daemon: inativo"
  fi

  if curl -fsS "http://${HOST}:${PORT}/healthz" >/dev/null 2>&1; then
    echo "HTTP: OK em http://${HOST}:${PORT}"
  else
    echo "HTTP: indisponível em http://${HOST}:${PORT}"
  fi
}

open_browser() {
  open "http://${HOST}:${PORT}"
}

show_logs() {
  echo "== watchdog =="
  tail -n 80 "$PROJECT_DIR/.runlogs/watchdog.log" 2>/dev/null || true
  echo "== streamlit stderr =="
  tail -n 80 "$PROJECT_DIR/.runlogs/streamlit.err.log" 2>/dev/null || true
}

case "${1:-}" in
  start)
    start_daemon
    status_daemon
    ;;
  stop)
    stop_daemon
    status_daemon
    ;;
  restart)
    stop_daemon
    start_daemon
    status_daemon
    ;;
  status)
    status_daemon
    ;;
  open)
    open_browser
    ;;
  logs)
    show_logs
    ;;
  *)
    cat <<USAGE
Uso:
  scripts/streamlit_daemon.sh start
  scripts/streamlit_daemon.sh stop
  scripts/streamlit_daemon.sh restart
  scripts/streamlit_daemon.sh status
  scripts/streamlit_daemon.sh open
  scripts/streamlit_daemon.sh logs

Variáveis opcionais:
  HOST=127.0.0.1 PORT=8503 scripts/streamlit_daemon.sh start
USAGE
    exit 1
    ;;
esac
