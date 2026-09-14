#!/bin/bash

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

cd "$REPO_ROOT"

python3 "$SCRIPT_DIR/main.py" md --template "$SCRIPT_DIR/template.md" --data "$SCRIPT_DIR/data.yaml" --output "$REPO_ROOT/README.md"
python3 "$SCRIPT_DIR/main.py" html --template "$SCRIPT_DIR/template.html" --data "$SCRIPT_DIR/data.yaml" --output "$REPO_ROOT/index.html"

# Generate PDF from index.html when wkhtmltopdf is available.
if command -v wkhtmltopdf >/dev/null 2>&1; then
  wkhtmltopdf -s A4 "$REPO_ROOT/index.html" "$REPO_ROOT/Roman Metlinskyi CV.pdf"
else
  echo "wkhtmltopdf not installed; skipping PDF generation." >&2
fi

