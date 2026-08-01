#!/bin/bash
set -e

# Second Brain — Onboarding Script
# Scaffolds vault directory structure and verifies CLI tooling.
#
# Usage: bash onboarding.sh <vault-path>
# Output: JSON summary to stdout. Progress messages to stderr.

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
TEMPLATE_SOURCE="$SCRIPT_DIR/../../../templates"
VAULT_ROOT="${1:-.}"

echo "=== Second Brain Onboarding ===" >&2

# 1. Create directory structure
echo "Creating directory structure..." >&2
mkdir -p "$VAULT_ROOT/raw/assets"
mkdir -p "$VAULT_ROOT/wiki/sources"
mkdir -p "$VAULT_ROOT/wiki/entities"
mkdir -p "$VAULT_ROOT/wiki/concepts"
mkdir -p "$VAULT_ROOT/wiki/events"
mkdir -p "$VAULT_ROOT/wiki/models"
mkdir -p "$VAULT_ROOT/wiki/synthesis"
mkdir -p "$VAULT_ROOT/templates"
mkdir -p "$VAULT_ROOT/output"

# 2. Copy canonical templates without overwriting any existing path
TEMPLATES=(
  source.md
  entity.md
  event.md
  model.md
  investment-thesis.md
  monitoring.md
  concept.md
  trend-thesis.md
  technology-model.md
  commercialization-model.md
  industry-opportunity-map.md
  technology-monitoring.md
)

if [ -d "$TEMPLATE_SOURCE" ]; then
  for template in "${TEMPLATES[@]}"; do
    source_template="$TEMPLATE_SOURCE/$template"
    target_template="$VAULT_ROOT/templates/$template"

    if [ ! -f "$source_template" ]; then
      echo "Missing canonical template: $source_template" >&2
      exit 1
    fi

    if [ -e "$target_template" ] || [ -L "$target_template" ]; then
      echo "templates/$template already exists, skipping" >&2
    else
      cp "$source_template" "$target_template"
      echo "Created templates/$template" >&2
    fi
  done
fi

# 3. Create wiki/index.md if it doesn't exist
if [ ! -f "$VAULT_ROOT/wiki/index.md" ]; then
  cat > "$VAULT_ROOT/wiki/index.md" << 'EOF'
# Index

Master catalog of all wiki pages. Updated on every ingest.

## Sources

## Entities

## Concepts

## Events

## Models

## Synthesis

## Trend Theses

## Opportunity Maps

## Active Theses

## Monitoring

## Technology Monitoring
EOF
  echo "Created wiki/index.md" >&2
else
  echo "wiki/index.md already exists, skipping" >&2
fi

# 4. Create wiki/log.md if it doesn't exist
if [ ! -f "$VAULT_ROOT/wiki/log.md" ]; then
  cat > "$VAULT_ROOT/wiki/log.md" << 'EOF'
# Log

Chronological record of all operations.

EOF
  echo "Created wiki/log.md" >&2
else
  echo "wiki/log.md already exists, skipping" >&2
fi

# 5. Check tooling
echo "" >&2
echo "Checking tooling..." >&2

TOOLS_JSON="[]"

check_tool() {
  local name="$1"
  local cmd="$2"
  local install_cmd="$3"
  local status="missing"

  if command -v "$cmd" &> /dev/null; then
    status="installed"
    echo "  [ok] $name" >&2
  else
    echo "  [missing] $name — install with: $install_cmd" >&2
  fi

  TOOLS_JSON=$(echo "$TOOLS_JSON" | python3 -c "
import sys, json
tools = json.load(sys.stdin)
tools.append({'name': '$name', 'status': '$status', 'install': '$install_cmd'})
print(json.dumps(tools))
" 2>/dev/null || echo "$TOOLS_JSON")
}

check_tool "summarize" "summarize" "npm i -g @steipete/summarize"
check_tool "qmd" "qmd" "npm i -g @tobilu/qmd"
check_tool "agent-browser" "agent-browser" "npm i -g agent-browser && agent-browser install"

echo "" >&2
echo "Onboarding complete." >&2

# 6. Output JSON result to stdout
VAULT_ABS=$(cd "$VAULT_ROOT" && pwd)
cat << JSONEOF
{
  "status": "complete",
  "vault_root": "$VAULT_ABS",
  "directories": [
    "raw/",
    "raw/assets/",
    "wiki/",
    "wiki/sources/",
    "wiki/entities/",
    "wiki/concepts/",
    "wiki/events/",
    "wiki/models/",
    "wiki/synthesis/",
    "templates/",
    "output/"
  ],
  "files": [
    "wiki/index.md",
    "wiki/log.md",
    "templates/source.md",
    "templates/entity.md",
    "templates/event.md",
    "templates/model.md",
    "templates/investment-thesis.md",
    "templates/monitoring.md",
    "templates/concept.md",
    "templates/trend-thesis.md",
    "templates/technology-model.md",
    "templates/commercialization-model.md",
    "templates/industry-opportunity-map.md",
    "templates/technology-monitoring.md"
  ],
  "tools": $TOOLS_JSON
}
JSONEOF
