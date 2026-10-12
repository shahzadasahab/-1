#!/usr/bin/env python3
"""Extract the printed English text of every booklet page into pages.json.

Arabic-script lines are dropped (they are visually reversed by the PDF text layer);
English lines are classified so the app can narrate them in Urdu framing with the
English wording kept exactly as printed.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[1]
PDF = ROOT / "app/src/main/assets/course/crash-course.pdf"
OUT = ROOT / "app/src/main/assets/course/pages.json"

ARABIC = re.compile(r"[\u0600-\u06FF\uFB50-\uFDFF\uFE70-\uFEFF]")
LATIN = re.compile(r"[A-Za-z]")
PRIVATE = re.compile(r"[\ue000-\uf8ff\u200b-\u200f\u202a-\u202e\ufffd]")
HEADING = re.compile(r"^(\d+(?:\.\d+)+)(?:\s*[–-]\s*\d+(?:\.\d+)*)?\s+\S")
NUM_ONLY = re.compile(r"^\d{1,3}$")
PREFIXES = {
    "Remember:": "remember",
    "Exam:": "exam",
    "Trap:": "trap",
    "Answers:": "answers",
}
BOXES = {
    "CLOSED-BOOK DRILL": "drill",
    "TONIGHT'S 5-MARK": "fivemark",
    "CHECKPOINT TEST": "checkpoint",
    "TODAY'S 3 HOURS": "hours",
}
SKIP_LINES = (
    "If behind, skip non-Golden",
    "Closed book, 30 minutes. Then mark",
)


SYMBOL_FONT = {
    0xE081: "(", 0xE082: ")", 0xE083: "[", 0xE084: "]", 0xE085: "(", 0xE086: ")",
    0xE088: "-", 0xE089: "–", 0xE08B: "—", 0xE092: ":", 0xE098: ">", 0xE09B: "=",
    0xE09D: "+", 0xE09E: "−", 0xE09F: "×", 0xE0A3: "~", 0xE1D7: "→",
    0x02EE: "”", 0x02BC: "'",
}
SYMBOL_FONT.update({0xE071 + d: str(d) for d in range(10)})


def decode_symbols(line: str) -> str:
    line = re.sub(r"(?<=[a-dA-D])\ue094", ")", line)
    line = line.replace("\ue094", ".")
    return "".join(SYMBOL_FONT.get(ord(ch), ch) for ch in line)


def clean(line: str) -> str:
    line = decode_symbols(line)
    line = PRIVATE.sub("", line)
    line = line.replace("{", "(").replace("}", ")")
    line = re.sub(r"\s+", " ", line).strip()
    return line


def is_urdu(line: str) -> bool:
    return len(ARABIC.findall(line)) > len(LATIN.findall(line))


def classify(lines: list[str]) -> list[dict]:
    blocks: list[dict] = []
    mode = ""
    for raw in lines:
        line = clean(raw)
        if not line or is_urdu(line) or NUM_ONLY.match(line):
            continue
        if len(line) <= 2 or any(line.startswith(s) for s in SKIP_LINES):
            continue
        if re.fullmatch(r"DAY\s*\d\s*\d\s*O\s*F.*", line, re.I) or line.upper().startswith("DAY"):
            if re.search(r"O\s*F\s*3\s*0", line):
                continue
        if line in BOXES:
            mode = BOXES[line]
            blocks.append({"t": "box", "x": line.title() if line != "TONIGHT'S 5-MARK" else "Tonight's 5-mark"})
            continue
        m = HEADING.match(line)
        if m:
            golden = "Golden" in line
            text = re.sub(r"\s*★\s*Golden\s*$", "", line).strip()
            blocks.append({"t": "h", "x": text, "g": golden})
            mode = ""
            continue
        if line.startswith("Chapter") and "recap" in line:
            blocks.append({"t": "h", "x": line, "g": False})
            mode = ""
            continue
        matched = False
        for prefix, kind in PREFIXES.items():
            if line.startswith(prefix):
                blocks.append({"t": kind, "x": line[len(prefix):].strip()})
                matched = True
                break
        if matched:
            continue
        if line.startswith("Cover:") or line.startswith("★ Must lock:"):
            key = "cover" if line.startswith("Cover:") else "lock"
            blocks.append({"t": key, "x": line.split(":", 1)[1].strip()})
            continue
        if mode == "drill" and re.match(r"^(\d+\.\s+)?[A-Z\"“]", line):
            blocks.append({"t": "q", "x": line})
            continue
        if blocks and blocks[-1]["t"] in {"p", "remember", "exam", "trap", "answers", "q", "cover", "lock"}:
            prev = blocks[-1]["x"]
            if prev and prev[-1] not in ".?!:)\"”" and line[:1].islower():
                blocks[-1]["x"] = f"{prev} {line}"
                continue
        blocks.append({"t": "p", "x": line})
    return blocks


def main() -> None:
    reader = PdfReader(str(PDF))
    pages: dict[str, list[dict]] = {}
    for i, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""
        pages[str(i)] = classify(text.splitlines())
    OUT.write_text(json.dumps(pages, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    total = sum(len(v) for v in pages.values())
    print(f"Wrote {OUT} ({OUT.stat().st_size} bytes, {len(pages)} pages, {total} blocks)")
    if "--show" in sys.argv:
        for key in sys.argv[sys.argv.index("--show") + 1:]:
            print(f"--- page {key} ---")
            for b in pages[key]:
                print(f"{b['t']:9} {b['x'][:140]}")


if __name__ == "__main__":
    main()
