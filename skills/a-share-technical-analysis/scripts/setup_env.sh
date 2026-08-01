#!/bin/bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILL_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
REPO_ROOT="$(cd "$SKILL_DIR/../.." && pwd)"
VENV_DIR="$REPO_ROOT/.work/venvs/a-share-ta"
CHAN_COMMIT="429d6ed3043e27c93a003ba2b10e70a05575e1f5"
CHAN_REPO_URL="${CHAN_PY_REPO_URL:-https://github.com/Vespa314/chan.py.git}"
DEFAULT_CHAN_DIR="$REPO_ROOT/.work/vendor/chan.py"
CHAN_DIR="${CHAN_PY_PATH:-$DEFAULT_CHAN_DIR}"

if [ -n "${A_SHARE_TA_PYTHON:-}" ]; then
  PYTHON_BIN="$A_SHARE_TA_PYTHON"
elif [ -x /opt/anaconda3/bin/python3.12 ]; then
  PYTHON_BIN=/opt/anaconda3/bin/python3.12
elif command -v python3.12 >/dev/null 2>&1; then
  PYTHON_BIN="$(command -v python3.12)"
else
  PYTHON_BIN="$(command -v python3)"
fi

"$PYTHON_BIN" -c 'import sys; assert sys.version_info >= (3, 11), "chan.py 双引擎适配要求 Python >= 3.11"'

if [ ! -x "$VENV_DIR/bin/python" ]; then
  "$PYTHON_BIN" -m venv "$VENV_DIR"
fi

"$VENV_DIR/bin/pip" install -r "$SKILL_DIR/requirements.txt"
mkdir -p \
  "$REPO_ROOT/.work/czsc" \
  "$REPO_ROOT/.work/market-data" \
  "$REPO_ROOT/.work/matplotlib" \
  "$REPO_ROOT/.work/technical-structure-state" \
  "$REPO_ROOT/.work/vendor"

if [ ! -e "$CHAN_DIR/.git" ]; then
  if [ -n "${CHAN_PY_PATH:-}" ]; then
    echo "CHAN_PY_PATH 不是保留 .git 的 chan.py checkout：$CHAN_DIR" >&2
    exit 1
  fi
  git clone --filter=blob:none "$CHAN_REPO_URL" "$CHAN_DIR"
fi

if ! git -C "$CHAN_DIR" diff --quiet || \
   ! git -C "$CHAN_DIR" diff --cached --quiet || \
   [ -n "$(git -C "$CHAN_DIR" ls-files --others --exclude-standard)" ]; then
  echo "chan.py checkout 存在本地修改，拒绝切换 commit：$CHAN_DIR" >&2
  exit 1
fi

if ! git -C "$CHAN_DIR" cat-file -e "$CHAN_COMMIT^{commit}" 2>/dev/null; then
  git -C "$CHAN_DIR" fetch --depth 1 origin "$CHAN_COMMIT"
fi

if [ "$(git -C "$CHAN_DIR" rev-parse HEAD)" != "$CHAN_COMMIT" ]; then
  git -C "$CHAN_DIR" checkout --detach "$CHAN_COMMIT"
fi

if [ "$(git -C "$CHAN_DIR" rev-parse HEAD)" != "$CHAN_COMMIT" ]; then
  echo "chan.py commit 固定失败：$CHAN_DIR" >&2
  exit 1
fi

echo "A 股技术分析环境已就绪：${VENV_DIR}；chan.py=${CHAN_COMMIT}" >&2
