#!/bin/bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
PYTHON_BIN="$REPO_ROOT/.work/venvs/a-share-ta/bin/python"
export PYTHONDONTWRITEBYTECODE=1

if [ "${RUN_LIVE_MARKET_DATA_TESTS:-0}" != "1" ]; then
  echo "SKIP: set RUN_LIVE_MARKET_DATA_TESTS=1 to query BaoStock and AkShare"
  exit 0
fi

CZSC_HOME="$REPO_ROOT/.work/czsc-live-test" \
  "$PYTHON_BIN" \
  "$REPO_ROOT/skills/a-share-technical-analysis/scripts/technical_snapshot.py" \
  --ticker SSE:600519 \
  --start 2022-01-01 \
  --output-dir "$REPO_ROOT/.work/live-technical-analysis-output" \
  --cache-dir "$REPO_ROOT/.work/live-market-data-cache"
