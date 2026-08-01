#!/bin/bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
SKILL_SOURCE="$REPO_ROOT/skills"
SKILL_TARGET="$REPO_ROOT/.agents/skills"

SKILLS=(
  second-brain
  second-brain-ingest
  second-brain-query
  second-brain-lint
  equity-research
  a-share-research-data
  a-share-technical-analysis
  frontier-tech-research
  technology-to-investment
)

mkdir -p "$SKILL_TARGET"
mkdir -p "$REPO_ROOT/wiki/events"
mkdir -p "$REPO_ROOT/wiki/models"
mkdir -p "$REPO_ROOT/templates"

for skill in "${SKILLS[@]}"; do
  source_dir="$SKILL_SOURCE/$skill"
  target_link="$SKILL_TARGET/$skill"
  relative_target="../../skills/$skill"

  if [ ! -f "$source_dir/SKILL.md" ]; then
    echo "Missing skill source: $source_dir/SKILL.md" >&2
    exit 1
  fi

  if [ -L "$target_link" ]; then
    if [ "$(readlink "$target_link")" != "$relative_target" ]; then
      echo "Refusing to replace unexpected symlink: $target_link" >&2
      exit 1
    fi
  elif [ -e "$target_link" ]; then
    echo "Refusing to replace existing path: $target_link" >&2
    exit 1
  else
    ln -s "$relative_target" "$target_link"
  fi
done

bash "$SKILL_SOURCE/second-brain/scripts/onboarding.sh" "$REPO_ROOT"

echo "Codex project skills are ready in $SKILL_TARGET" >&2
echo "Start a new Codex task from $REPO_ROOT to refresh skill discovery." >&2
