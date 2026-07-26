#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
VAULT_ROOT="${1:-$(cd "$SCRIPT_DIR/../../.." && pwd)}"
MODE="${2:-install}"
TOOL_ROOT="${VIDEO2SKILL_ROOT:-$VAULT_ROOT/.work/tools/Video2Skill_Invest}"
REPOSITORY="${VIDEO2SKILL_REPOSITORY:-https://github.com/Jasonmils/Video2Skill_Invest.git}"
ENV_TEMPLATE="$VAULT_ROOT/config/video-ingest.env.example"
ENV_FILE="$VAULT_ROOT/.env.video-ingest.local"

if [ ! -f "$VAULT_ROOT/AGENTS.md" ] || [ ! -d "$VAULT_ROOT/raw" ]; then
  echo "Not an AI Trading Wiki vault: $VAULT_ROOT" >&2
  exit 2
fi

if [ -d "$TOOL_ROOT/.git" ]; then
  CURRENT_ORIGIN="$(git -C "$TOOL_ROOT" remote get-url origin)"
  if [ "$CURRENT_ORIGIN" != "$REPOSITORY" ]; then
    echo "Refusing unexpected Video2Skill origin: $CURRENT_ORIGIN" >&2
    exit 2
  fi
  if [ "$MODE" = "update" ]; then
    CURRENT_BRANCH="$(git -C "$TOOL_ROOT" symbolic-ref --quiet --short HEAD || true)"
    if [ "$CURRENT_BRANCH" != "main" ]; then
      echo "Refusing to update Video2Skill outside branch main: ${CURRENT_BRANCH:-detached HEAD}" >&2
      exit 2
    fi
    if [ -n "$(git -C "$TOOL_ROOT" status --porcelain)" ]; then
      echo "Refusing to update a modified Video2Skill checkout: $TOOL_ROOT" >&2
      exit 2
    fi
    git -C "$TOOL_ROOT" fetch --prune origin
    git -C "$TOOL_ROOT" merge --ff-only origin/main
  fi
elif [ -e "$TOOL_ROOT" ]; then
  echo "Refusing non-repository tool path: $TOOL_ROOT" >&2
  exit 2
else
  mkdir -p "$(dirname "$TOOL_ROOT")"
  git clone "$REPOSITORY" "$TOOL_ROOT"
fi

if [ ! -f "$ENV_FILE" ]; then
  if [ ! -f "$ENV_TEMPLATE" ]; then
    echo "Missing environment template: $ENV_TEMPLATE" >&2
    exit 2
  fi
  cp "$ENV_TEMPLATE" "$ENV_FILE"
  chmod 600 "$ENV_FILE"
fi

if [ "$MODE" = "install" ] || [ "$MODE" = "update" ]; then
  if command -v python3.12 >/dev/null 2>&1; then
    SETUP_PYTHON="python3.12"
  elif command -v python3.11 >/dev/null 2>&1; then
    SETUP_PYTHON="python3.11"
  else
    echo "Python 3.11 or 3.12 is required for Video2Skill_Invest." >&2
    exit 2
  fi
  PYTHON_COMMAND="$SETUP_PYTHON" bash "$TOOL_ROOT/setup.sh"
elif [ "$MODE" != "skip-install" ]; then
  echo "Usage: $0 [VAULT_ROOT] [install|update|skip-install]" >&2
  exit 2
fi

echo "Video2Skill checkout: $TOOL_ROOT"
echo "Local secrets file: $ENV_FILE"
echo "Fill HF_TOKEN and DEEPSEEK_API_KEY before processing MP4."
