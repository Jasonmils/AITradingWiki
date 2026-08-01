#!/bin/bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
PYTHON_BIN="$REPO_ROOT/.work/venvs/a-share-ta/bin/python"
export PYTHONDONTWRITEBYTECODE=1

if [ ! -x "$PYTHON_BIN" ]; then
  echo "Missing isolated environment. Run: bash skills/a-share-technical-analysis/scripts/setup_env.sh" >&2
  exit 1
fi

CZSC_HOME="$REPO_ROOT/.work/czsc-test" \
  "$PYTHON_BIN" "$SCRIPT_DIR/test_a_share_technical_analysis.py"

CZSC_HOME="$REPO_ROOT/.work/czsc-test" \
  "$PYTHON_BIN" "$SCRIPT_DIR/test_chan_dual_engine.py"
