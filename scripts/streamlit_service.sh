#!/usr/bin/env bash
set -euo pipefail

LABEL="br.i3aps.streamlit"
UID_NUM="$(id -u)"
PLIST_PATH="$HOME/Library/LaunchAgents/${LABEL}.plist"
PROJECT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
STREAMLIT_BIN="$PROJECT_DIR/.venv/bin/streamlit"
HOST="${HOST:-127.0.0.1}"
PORT="${PORT:-8503}"
LOG_DIR="$PROJECT_DIR/.runlogs"
OUT_LOG="$LOG_DIR/streamlit.out.log"
ERR_LOG="$LOG_DIR/streamlit.err.log"

mkdir -p "$LOG_DIR"

if [[ "$PROJECT_DIR" == *"/Library/CloudStorage/"* ]]; then
  echo "Este projeto está em CloudStorage. Use scripts/streamlit_daemon.sh (screen + watchdog),"
  echo "pois launchd pode falhar com 'Operation not permitted' nesse caminho."
  exit 1
fi

write_plist() {
  if [[ ! -x "$STREAMLIT_BIN" ]]; then
    echo "Erro: streamlit não encontrado em $STREAMLIT_BIN"
    exit 1
  fi

  cat > "$PLIST_PATH" <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>Label</key>
  <string>${LABEL}</string>

  <key>ProgramArguments</key>
  <array>
    <string>${STREAMLIT_BIN}</string>
    <string>run</string>
    <string>app.py</string>
    <string>--server.headless</string>
    <string>true</string>
    <string>--server.address</string>
    <string>${HOST}</string>
    <string>--server.port</string>
    <string>${PORT}</string>
    <string>--server.fileWatcherType</string>
    <string>poll</string>
    <string>--browser.gatherUsageStats</string>
    <string>false</string>
  </array>

  <key>WorkingDirectory</key>
  <string>${PROJECT_DIR}</string>

  <key>RunAtLoad</key>
  <true/>
  <key>KeepAlive</key>
  <true/>
  <key>ThrottleInterval</key>
  <integer>3</integer>

  <key>StandardOutPath</key>
  <string>${OUT_LOG}</string>
  <key>StandardErrorPath</key>
  <string>${ERR_LOG}</string>
</dict>
</plist>
EOF
}

loaded() {
  launchctl print "gui/${UID_NUM}/${LABEL}" >/dev/null 2>&1
}

stop_service() {
  if loaded; then
    launchctl bootout "gui/${UID_NUM}" "$PLIST_PATH" >/dev/null 2>&1 || true
  fi
}

start_service() {
  write_plist
  stop_service
  launchctl bootstrap "gui/${UID_NUM}" "$PLIST_PATH"
  launchctl kickstart -k "gui/${UID_NUM}/${LABEL}"
}

status_service() {
  if loaded; then
    echo "Status launchd: ativo"
    launchctl print "gui/${UID_NUM}/${LABEL}" | rg -n "state =|pid =|last exit code =|path =" -N || true
  else
    echo "Status launchd: inativo"
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
  echo "== stdout =="
  tail -n 80 "$OUT_LOG" 2>/dev/null || true
  echo "== stderr =="
  tail -n 80 "$ERR_LOG" 2>/dev/null || true
}

uninstall_service() {
  stop_service
  rm -f "$PLIST_PATH"
  echo "Removido: $PLIST_PATH"
}

case "${1:-}" in
  install|start)
    start_service
    status_service
    ;;
  stop)
    stop_service
    status_service
    ;;
  restart)
    start_service
    status_service
    ;;
  status)
    status_service
    ;;
  open)
    open_browser
    ;;
  logs)
    show_logs
    ;;
  uninstall)
    uninstall_service
    ;;
  *)
    cat <<USAGE
Uso:
  scripts/streamlit_service.sh install   # instala e inicia serviço com auto-restart
  scripts/streamlit_service.sh restart   # reinicia serviço
  scripts/streamlit_service.sh stop      # para serviço
  scripts/streamlit_service.sh status    # status do launchd + healthcheck HTTP
  scripts/streamlit_service.sh open      # abre no navegador
  scripts/streamlit_service.sh logs      # mostra logs
  scripts/streamlit_service.sh uninstall # remove serviço

Variáveis opcionais:
  HOST=127.0.0.1 PORT=8503 scripts/streamlit_service.sh install
USAGE
    exit 1
    ;;
esac
