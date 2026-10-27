#!/usr/bin/env bash
# Rebuild "VIBE CODING using Cursor AI" from the HTML source.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
SRC="$ROOT/docs/vibe-coding/source.html"
OUT="$ROOT/docs/vibe-coding-using-cursor-ai.pdf"
CHROME="${CHROME:-google-chrome}"

# Chrome writes the PDF, then often lingers on DBus. timeout closes it.
timeout 30 "$CHROME" \
  --headless \
  --disable-gpu \
  --no-sandbox \
  --user-data-dir=/tmp/chrome-vibe-pdf \
  --no-pdf-header-footer \
  --print-to-pdf="$OUT" \
  "file://$SRC" || {
    status=$?
    if [[ $status -ne 124 ]]; then
      exit $status
    fi
  }
test -s "$OUT"

python3 - "$OUT" <<'PY'
import sys
path = sys.argv[1]
try:
    from pypdf import PdfReader, PdfWriter
except ImportError:
    sys.exit(0)
reader = PdfReader(path)
writer = PdfWriter()
writer.append(reader)
writer.add_metadata({
    "/Title": "VIBE CODING using Cursor AI",
    "/Subject": "A field guide to steering Cursor: describe the behavior, run the result, and own the diff.",
    "/Keywords": "Cursor, vibe coding, Agent, field guide",
})
with open(path, "wb") as f:
    writer.write(f)
print(f"pages: {len(reader.pages)}")
PY

echo "wrote $OUT"
