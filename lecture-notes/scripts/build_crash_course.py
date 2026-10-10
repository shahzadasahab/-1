#!/usr/bin/env python3
"""Build the Class XI and Class XII 30-day crash-course HTML booklets."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from crash_lib import render_book
from crash_xi import DAYS as XI_DAYS, FRONT as XI_FRONT, MAP as XI_MAP
from crash_xii import DAYS as XII_DAYS, FRONT as XII_FRONT, MAP as XII_MAP

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "html"

def main():
    assert len(XI_DAYS) == 30, len(XI_DAYS)
    assert len(XII_DAYS) == 30, len(XII_DAYS)
    assert [d["n"] for d in XI_DAYS] == list(range(1, 31))
    assert [d["n"] for d in XII_DAYS] == list(range(1, 31))
    render_book(
        {"title": "Class XI · 30-Day Crash Course", "front": XI_FRONT, "map": XI_MAP},
        XI_DAYS,
        HTML / "XI-30-day-crash.html",
    )
    render_book(
        {"title": "Class XII · 30-Day Crash Course", "front": XII_FRONT, "map": XII_MAP},
        XII_DAYS,
        HTML / "XII-30-day-crash.html",
    )

if __name__ == "__main__":
    main()
