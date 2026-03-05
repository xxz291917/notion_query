#!/bin/bash
# Deploy notion_query to hk24
# Usage: ./scripts/deploy.sh [sync|setup|start|full]

set -e

HK24_KEY="/Users/xiaxuezhi/Documents/HouseSigma/id_ed25519"
HK24_HOST="root@103.75.117.152"
HK24_SSH="ssh -i $HK24_KEY $HK24_HOST"
REMOTE_DIR="/root/web_www/notion_query"

sync_code() {
    echo "==> Syncing code to hk24..."
    rsync -avz --exclude '.venv' --exclude '__pycache__' --exclude 'data/' --exclude '.git' \
        -e "ssh -i $HK24_KEY" \
        /Users/xiaxuezhi/Documents/code/HS/notion_query/ \
        $HK24_HOST:$REMOTE_DIR/
    echo "==> Done."
}

setup_remote() {
    echo "==> Setting up hk24 environment..."
    $HK24_SSH "cd $REMOTE_DIR && uv sync && docker compose up -d qdrant"
    echo "==> Done."
}

start_api() {
    echo "==> Starting API on hk24..."
    $HK24_SSH "cd $REMOTE_DIR && nohup uv run uvicorn src.api.app:app --host 0.0.0.0 --port 8000 > api.log 2>&1 &"
    echo "==> API started. Check: curl http://103.75.117.152:8000/health"
}

run_sync() {
    echo "==> Running Notion sync on hk24 (background)..."
    $HK24_SSH "cd $REMOTE_DIR && nohup uv run python scripts/full_sync.py --mode ${1:-full} > sync.log 2>&1 </dev/null &"
    echo "==> Sync started in background. Monitor: ssh hk24 'tail -f $REMOTE_DIR/sync.log'"
}

status() {
    echo "==> hk24 status:"
    $HK24_SSH "cd $REMOTE_DIR && echo '--- Qdrant ---' && docker compose ps && echo '--- API ---' && (curl -s localhost:8000/health 2>/dev/null || echo 'API not running')"
}

case "${1:-sync}" in
    sync)    sync_code ;;
    setup)   sync_code && setup_remote ;;
    start)   start_api ;;
    notion)  run_sync "${2:-full}" ;;
    status)  status ;;
    full)    sync_code && setup_remote && run_sync full && start_api ;;
    *)       echo "Usage: $0 {sync|setup|start|notion [full|incremental|discover]|status|full}" ;;
esac
