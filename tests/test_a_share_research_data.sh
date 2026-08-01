#!/bin/bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
PYTHON_BIN="${A_SHARE_RESEARCH_DATA_PYTHON:-$(command -v python3)}"

export PYTHONDONTWRITEBYTECODE=1

"$PYTHON_BIN" "$REPO_ROOT/tests/test_a_share_research_data.py"
