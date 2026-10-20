#!/usr/bin/env python3
"""Print lecture-notes/index.html to a PDF with headless Chrome.

The HTML uses CSS flexbox, inline SVG diagrams, and MathJax (SVG output).
Chrome waits for the virtual-time budget so MathJax can fetch and typeset
before the PDF is written. Vectors stay in the PDF.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
HTML = ROOT / "index.html"
PDF = ROOT / "Computer-Science-XI-XII-Lecture-Notes.pdf"
PROFILE = Path("/tmp/chrome-lecture-notes")


def main() -> int:
    if not HTML.is_file():
        print(f"missing {HTML}", file=sys.stderr)
        return 1
    PROFILE.mkdir(parents=True, exist_ok=True)
    cmd = [
        "google-chrome",
        "--headless=new",
        "--disable-gpu",
        "--no-sandbox",
        "--disable-dev-shm-usage",
        f"--user-data-dir={PROFILE}",
        "--no-first-run",
        "--no-default-browser-check",
        "--disable-extensions",
        "--disable-background-networking",
        "--disable-sync",
        "--hide-scrollbars",
        "--no-pdf-header-footer",
        "--virtual-time-budget=60000",
        "--timeout=90000",
        f"--print-to-pdf={PDF}",
        HTML.resolve().as_uri(),
    ]
    print("printing", HTML.name)
    try:
        subprocess.run(cmd, check=False, timeout=80)
    except subprocess.TimeoutExpired:
        print("Chrome stayed open after writing the PDF; continuing.")
    if not PDF.is_file() or PDF.stat().st_size < 10_000:
        print("PDF was not written", file=sys.stderr)
        return 1
    print(f"wrote {PDF} ({PDF.stat().st_size} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
