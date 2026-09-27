#!/usr/bin/env bash
# Regenerate every ui_*.py (from *.ui) and *_rc.py (from *.qrc) in the repo.
#   ./build.sh            -> all topics
#   ./build.sh 04_resources -> one folder
set -euo pipefail
cd "$(dirname "$0")"

# Prefer the venv tools if present
if [[ -x venv/bin/pyside6-uic ]]; then BIN="venv/bin/"; else BIN=""; fi

ROOT="${1:-.}"

find "$ROOT" -path ./venv -prune -o -name '*.qrc' -print | while read -r qrc; do
  dir=$(dirname "$qrc"); name=$(basename "$qrc" .qrc)
  echo "rcc  $qrc -> $dir/${name}_rc.py"
  "${BIN}pyside6-rcc" "$qrc" -o "$dir/${name}_rc.py"
done

find "$ROOT" -path ./venv -prune -o -name '*.ui' -print | while read -r ui; do
  dir=$(dirname "$ui"); name=$(basename "$ui" .ui)
  echo "uic  $ui -> $dir/ui_${name}.py"
  "${BIN}pyside6-uic" "$ui" -o "$dir/ui_${name}.py"
done
