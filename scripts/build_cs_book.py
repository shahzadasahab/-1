#!/usr/bin/env python3
"""Turn the CS XI / XII cheat-sheet PDFs into offline reader JSON.

The printed booklets set formulas in MathJax, which became vector outlines in
the PDF. This script keeps the written Urdish notes and restores the formula
tables as TeX so the app can typeset them with MathJax.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

import pymupdf

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "csheet" / "src" / "main" / "assets" / "www" / "content"
PDFS = {
    "xi": Path(
        "/home/ubuntu/.cursor/projects/workspace/uploads/"
        "CS_XI___30-Day_Ultimate_Cheat-Sheet___Complete_Edition__Days_1_30__5648.pdf"
    ),
    "xii": Path(
        "/home/ubuntu/.cursor/projects/workspace/uploads/"
        "CS_XII___30-Day_Ultimate_Cheat-Sheet___Complete_Edition__Days_1_30__b300.pdf"
    ),
}

BOOKS = {
    "xi": {
        "title": "Computer Science XI",
        "short": "CS XI",
        "chapters_blurb": "6 chapters · 45 golden topics",
        "golden": 45,
        "checkpoints": {"05", "08", "13", "16", "19", "23"},
    },
    "xii": {
        "title": "Computer Science XII",
        "short": "CS XII",
        "chapters_blurb": "6 chapters · 32 golden topics",
        "golden": 32,
        "checkpoints": {"04", "09", "13", "15", "19", "23"},
    },
}

SECTION_RE = re.compile(
    r"^(?:"
    r"\d+\.\d+(?:\.\d+)?(?:\s*[–\-]\s*\d+\.\d+(?:\.\d+)?)?(?:\s+\S)"
    r"|Bonus\b"
    r"|Drill\b"
    r"|Closed-book\b"
    r"|K-Map\b"
    r"|LogiSim\b"
    r"|5-mark\b"
    r"|Worked\b"
    r")"
)

MATH_PATTERNS = [
    (re.compile(r"Y\s*=\s*\(A\s*⊕\s*B\)'"), r"\\(Y = (A \\oplus B)'\\)"),
    (re.compile(r"Y\s*=\s*A\s*⊕\s*B"), r"\\(Y = A \\oplus B\\)"),
    (re.compile(r"Y\s*=\s*A\s*·\s*B\s*\+\s*C"), r"\\(Y = A \\cdot B + C\\)"),
    (re.compile(r"Y\s*=\s*A\s*·\s*B"), r"\\(Y = A \\cdot B\\)"),
    (re.compile(r"Y\s*=\s*A\s*\+\s*B"), r"\\(Y = A + B\\)"),
    (re.compile(r"Y\s*=\s*A'"), r"\\(Y = A'\\)"),
    (re.compile(r"O\(n\s*\^\s*2\)"), r"\\(O(n^{2})\\)"),
    (re.compile(r"O\(n\^2\)"), r"\\(O(n^{2})\\)"),
    (re.compile(r"O\(n\s*log\s*n\)", re.I), r"\\(O(n \\log n)\\)"),
    (re.compile(r"O\(log\s*n\)", re.I), r"\\(O(\\log n)\\)"),
    (re.compile(r"O\(2\^n\)"), r"\\(O(2^{n})\\)"),
    (re.compile(r"O\(n\)"), r"\\(O(n)\\)"),
    (re.compile(r"O\(1\)"), r"\\(O(1)\\)"),
    (re.compile(r"2\s*\^\s*n"), r"\\(2^{n}\\)"),
]


def mathify(text: str) -> str:
    for pattern, repl in MATH_PATTERNS:
        text = pattern.sub(repl, text)
    return text


CHROME = {
    "a", "b", "c", "d", "x", "y", "v", "t", "0", "1",
    "high", "low", "and", "or", "not", "nand", "nor", "xor", "xnor",
    "day", "o", "○",
}


def is_chrome(lines: list[str]) -> bool:
    words: list[str] = []
    for line in lines:
        words.extend(re.split(r"\s+", line.replace(":", " ")))
    words = [w.strip(".,:;()[]") for w in words if w.strip(".,:;()[]")]
    if len(words) < 3:
        return False
    hits = 0
    for word in words:
        token = word.lower()
        if token in CHROME or len(token) <= 1:
            hits += 1
    return hits / len(words) >= 0.82


def is_row(lines: list[str]) -> bool:
    if not 2 <= len(lines) <= 5:
        return False
    if any(len(line) > 72 for line in lines):
        return False
    if any(line.startswith(("Def (", "🧠", "📝", "⚠", "Drill", "Jawab")) for line in lines):
        return False
    if SECTION_RE.match(lines[0]) and len(lines[0]) > 18:
        return False
    return True


def looks_like_code(lines: list[str]) -> bool:
    if len(lines) < 2:
        return False
    hits = 0
    for line in lines:
        if re.match(
            r"^(def |for |while |if |elif |else:|import |from |print\(|return |class |"
            r"try:|except |with |#|range\(|[a-z_]+\s*=)",
            line,
        ):
            hits += 1
    return hits >= max(2, len(lines) // 2)


def classify_lines(lines: list[str]) -> list[dict]:
    blocks: list[dict] = []
    paragraph: list[str] = []

    def flush_paragraph() -> None:
        if not paragraph:
            return
        text = mathify(join_wrapped(paragraph))
        if text:
            kind = "code" if looks_like_code(paragraph) else "p"
            if kind == "code":
                blocks.append({"type": "code", "text": "\n".join(paragraph)})
            else:
                blocks.append({"type": "p", "text": text})
        paragraph.clear()

    for line in lines:
        if line.startswith("Def (paper"):
            flush_paragraph()
            body = re.sub(r"^Def \(paper mein yehi likho\):\s*", "", line).strip()
            blocks.append({"type": "def", "text": mathify(body or line)})
        elif line.startswith("🧠"):
            flush_paragraph()
            blocks.append({"type": "tip", "text": mathify(line.lstrip("🧠 ").strip())})
        elif line.startswith("📝"):
            flush_paragraph()
            blocks.append({"type": "exam", "text": mathify(line.lstrip("📝 ").strip())})
        elif line.startswith("⚠"):
            flush_paragraph()
            blocks.append({"type": "warn", "text": mathify(line.lstrip("⚠ ").strip())})
        elif line.startswith("Jawab:"):
            flush_paragraph()
            blocks.append({"type": "answer", "text": mathify(line)})
        else:
            paragraph.append(line)
    flush_paragraph()
    return blocks


def join_wrapped(lines: list[str]) -> str:
    parts: list[str] = []
    for line in lines:
        if not parts:
            parts.append(line)
            continue
        prev = parts[-1]
        if prev.endswith(("-", "/")) or (
            not prev.endswith((".", "!", "?", ":", "—"))
            and line[:1].islower()
        ):
            joiner = "" if prev.endswith(("-", "/")) else " "
            parts[-1] = prev + joiner + line
        else:
            parts.append(line)
    return " ".join(parts)


def replace_boolean_laws(lines: list[str]) -> dict | None:
    blob = " ".join(lines)
    if "Identity" in blob and "De Morgan" in blob and "AND form" in blob:
        return {
            "type": "table",
            "headers": ["Law", "AND form", "OR form"],
            "rows": [
                ["Identity", r"\(A \cdot 1 = A\)", r"\(A + 0 = A\)"],
                ["Null", r"\(A \cdot 0 = 0\)", r"\(A + 1 = 1\)"],
                ["Idempotent", r"\(A \cdot A = A\)", r"\(A + A = A\)"],
                ["Complement", r"\(A \cdot A' = 0\)", r"\(A + A' = 1\)"],
                ["Double NOT", r"\((A')' = A\)", r"—"],
                ["De Morgan", r"\((A \cdot B)' = A' + B'\)", r"\((A + B)' = A' \cdot B'\)"],
            ],
        }
    return None


def blocks_of(page: pymupdf.Page) -> list[dict]:
    raw = []
    for block in page.get_text("blocks"):
        x0, y0, x1, y1, text = block[:5]
        if y0 > 748 or x0 > 558:
            continue
        lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
        if not lines:
            continue
        raw.append({"x0": x0, "y0": y0, "x1": x1, "y1": y1, "lines": lines})
    return raw


def column_of(block: dict) -> str:
    text = " ".join(block["lines"])
    first = block["lines"][0].strip()
    if first == "★ Golden" and block["y0"] > 60:
        pass
    elif block["y0"] < 63:
        return "H"
    elif block["y0"] < 78 and (
        "Must lock" in text or text.startswith("Chapter") or text.count("·") >= 2
    ):
        return "H"
    width = block["x1"] - block["x0"]
    if width > 390 and block["x0"] < 140:
        return "F"
    if block["x0"] < 300:
        return "L"
    return "R"


def header_meta(blocks: list[dict]) -> dict:
    day = ""
    chapter = ""
    must = ""
    ranged = ""
    subtitle = ""
    title_lines: list[str] = []
    for block in blocks:
        lines = [ln.strip() for ln in block["lines"] if ln.strip() and ln.strip() != "★ Golden"]
        if not lines:
            continue
        if any("Must lock" in ln for ln in lines):
            joined = " ".join(lines)
            parts = re.split(r"★\s*Must lock:\s*", joined)
            must = parts[-1].strip(" ★")
            continue
        if any(ln.startswith("Chapter") for ln in lines):
            for ln in lines:
                if ln.startswith("Chapter"):
                    chapter = re.sub(r"\s+Days\s+.*$", "", ln).strip()
                elif ln.startswith("Days ") and "·" in ln:
                    ranged = ln
            continue
        if any(ln.count("·") >= 2 and len(ln) > 24 for ln in lines):
            subtitle = next(ln for ln in lines if ln.count("·") >= 2)
            continue
        for ln in lines:
            if re.fullmatch(r"\d{2}", ln):
                day = ln
            elif re.fullmatch(r"\d", ln) or ln in {"Day", "★", "☰", "XI", "XII"}:
                continue
            else:
                title_lines.append(ln)
    title = re.sub(r"\s+", " ", " ".join(title_lines)).strip()
    return {
        "day": day,
        "chapter": chapter,
        "mustLock": must,
        "range": ranged,
        "title": title,
        "subtitle": subtitle,
    }


def new_card(title: str) -> dict:
    kind = "section"
    if title.startswith(("Drill", "Closed-book")):
        kind = "drill"
    return {
        "kind": kind,
        "title": title,
        "golden": False,
        "blocks": [],
        "diagram": None,
    }


def consume(column_blocks: list[dict]) -> list[dict]:
    cards: list[dict] = []
    current: dict | None = None
    pending_rows: list[list[str]] = []

    def flush_rows() -> None:
        nonlocal pending_rows
        if not pending_rows or current is None:
            pending_rows = []
            return
        headers = pending_rows[0]
        body = pending_rows[1:]
        if body and all(len(row) == len(headers) for row in body):
            current["blocks"].append({"type": "table", "headers": headers, "rows": body})
        else:
            for row in pending_rows:
                current["blocks"].append({"type": "p", "text": mathify(" · ".join(row))})
        pending_rows = []

    def start(title: str) -> dict:
        nonlocal current
        flush_rows()
        current = new_card(title)
        cards.append(current)
        return current

    for block in column_blocks:
        lines = [ln for ln in block["lines"] if ln not in {"★ Golden"}]
        golden = any(ln.strip() == "★ Golden" for ln in block["lines"])
        if not lines or is_chrome(lines):
            if golden and current is not None:
                current["golden"] = True
            continue
        law = replace_boolean_laws(lines)
        if law is not None:
            if current is None:
                start("Basic Boolean Laws")
            flush_rows()
            current["blocks"].append(law)
            current["golden"] = True
            continue
        first = lines[0]
        if SECTION_RE.match(first) and len(first) < 92:
            card = start(first)
            if golden:
                card["golden"] = True
            rest = lines[1:]
            if rest:
                if is_row(rest) and not any(r.startswith(("Def", "🧠", "📝", "⚠")) for r in rest):
                    pending_rows.append(rest)
                else:
                    card["blocks"].extend(classify_lines(rest))
            continue
        if current is None:
            start("Notes")
        if golden:
            current["golden"] = True
        if is_row(lines):
            pending_rows.append(lines)
            continue
        flush_rows()
        current["blocks"].extend(classify_lines(lines))
    flush_rows()
    return [card for card in cards if card["blocks"] or card["title"] not in {"Notes"}]


DIAGRAMS = {
    ("xi", "01"): [("stairs-ramp", "discrete"), ("analog-digital", "signal")],
    ("xi", "02"): [("gates-basic", "logic gate"), ("gates-universal", "universal")],
    ("xi", "03"): [("gates-xor", "xor"), ("logic-circuit", "logic diagram"), ("kmap", "karnaugh")],
    ("xi", "04"): [("sdlc", "sdlc"), ("waterfall", "waterfall")],
    ("xi", "05"): [("agile", "agile"), ("osi", "osi")],
    ("xi", "06"): [("ct-pillars", "computational"), ("algorithm-steps", "algorithm")],
    ("xi", "07"): [("bubble-sort", "bubble"), ("selection-sort", "selection")],
    ("xi", "08"): [("search", "search")],
    ("xi", "09"): [("lang-levels", "language")],
    ("xi", "10"): [("variables", "variable")],
    ("xi", "11"): [("ifelse", "if")],
    ("xi", "12"): [("loops", "loop")],
    ("xi", "13"): [("debug", "debug")],
    ("xi", "14"): [("keys-table", "key")],
    ("xi", "15"): [("er", "relationship")],
    ("xi", "16"): [("access", "query")],
    ("xi", "17"): [("ai-iot", "artificial")],
    ("xi", "19"): [("assistive", "assistive")],
    ("xi", "20"): [("data-types", "types of data")],
    ("xi", "22"): [("inquiry", "inquiry")],
    ("xii", "01"): [("hci-senses", "hci")],
    ("xii", "03"): [("ui-ux", "ui")],
    ("xii", "04"): [("wireframe", "wireframe")],
    ("xii", "05"): [("trace", "trace")],
    ("xii", "06"): [("bigo", "big o")],
    ("xii", "07"): [("array", "array")],
    ("xii", "08"): [("structures", "linked"), ("stack-queue", "stack")],
    ("xii", "10"): [("py-collections", "list")],
    ("xii", "12"): [("files", "file")],
    ("xii", "13"): [("exceptions", "exception")],
    ("xii", "14"): [("pandas", "pandas")],
    ("xii", "15"): [("stats", "statistic")],
    ("xii", "16"): [("neural", "neural")],
    ("xii", "18"): [("security", "threat")],
    ("xii", "21"): [("mvp", "mvp")],
    ("xii", "23"): [("beachhead", "beachhead")],
}

FORMULA_CARDS = {
    ("xi", "02"): {
        "kind": "formulas",
        "title": "Boolean laws & row count",
        "golden": True,
        "diagram": None,
        "blocks": [
            {
                "type": "p",
                "text": r"Truth-table rows: \(2^{n}\) where \(n\) is the number of inputs. 2 inputs → 4 rows, 3 inputs → 8, 4 inputs → 16.",
            },
            {
                "type": "tip",
                "text": r"De Morgan: bar todo, sign badlo. NAND is \(\overline{A \cdot B} = A' + B'\). NOR is \(\overline{A + B} = A' \cdot B'\).",
            },
            {
                "type": "table",
                "headers": ["Gate", "Expression", "Only-1 or only-0 row"],
                "rows": [
                    ["AND", r"\(Y = A \cdot B\)", "1 only at 11"],
                    ["OR", r"\(Y = A + B\)", "0 only at 00"],
                    ["NOT", r"\(Y = A'\)", "flips the single input"],
                    ["NAND", r"\(Y = (A \cdot B)'\)", "0 only at 11"],
                    ["NOR", r"\(Y = (A + B)'\)", "1 only at 00"],
                ],
            },
        ],
    },
    ("xi", "03"): {
        "kind": "formulas",
        "title": "Expressions, minterms & a K-map",
        "golden": True,
        "diagram": None,
        "blocks": [
            {
                "type": "p",
                "text": r"Precedence, like BODMAS: brackets, then NOT \('\), then AND \(\cdot\), then OR \(+\).",
            },
            {
                "type": "p",
                "text": r"XOR is 1 when the inputs differ: \(Y = A \oplus B = A'B + AB'\). XNOR is the equality gate: \(Y = (A \oplus B)'\).",
            },
            {
                "type": "table",
                "headers": ["", "Minterm (SOP)", "Maxterm (POS)"],
                "rows": [
                    ["Taken from", "rows where output is 1", "rows where output is 0"],
                    ["A variable that is 0", r"written with a bar, \(\bar{A}\)", r"written plain, \(A\)"],
                    ["A variable that is 1", r"written plain, \(A\)", r"written with a bar, \(\bar{A}\)"],
                    [r"Example A=0, B=1, C=1", r"\(\bar{A}BC\)", r"\((A + \bar{B} + \bar{C})\)"],
                ],
            },
            {
                "type": "p",
                "text": r"Worked K-map in the booklet: the group of four 1s is \(A'\) and the pair is \(BC\), so \(F = A' + BC\).",
            },
        ],
    },
    ("xi", "10"): {
        "kind": "formulas",
        "title": "Arithmetic operators",
        "golden": False,
        "diagram": None,
        "blocks": [
            {
                "type": "table",
                "headers": ["Operator", "Meaning", "Example"],
                "rows": [
                    ["+", "add", r"\(9 + 2 = 11\)"],
                    ["−", "subtract", r"\(9 - 2 = 7\)"],
                    ["*", "multiply", r"\(9 \times 2 = 18\)"],
                    ["/", "true division", r"\(9 / 2 = 4.5\)"],
                    ["//", "floor division", r"\(9 // 2 = 4\)"],
                    ["%", "remainder", r"\(9 \% 2 = 1\)"],
                    ["**", "power", r"\(2^{3} = 8\)"],
                ],
            }
        ],
    },
    ("xii", "06"): {
        "kind": "formulas",
        "title": "Big-O growth",
        "golden": True,
        "diagram": None,
        "blocks": [
            {
                "type": "p",
                "text": r"From fastest to slowest as \(n\) grows: \(O(1)\), \(O(\log n)\), \(O(n)\), \(O(n \log n)\), \(O(n^{2})\), \(O(2^{n})\).",
            },
            {
                "type": "table",
                "headers": ["Class", "Typical case", "As n doubles"],
                "rows": [
                    [r"\(O(1)\)", "read one array slot", "same time"],
                    [r"\(O(\log n)\)", "binary search", "one extra step"],
                    [r"\(O(n)\)", "linear search, one loop", "about twice"],
                    [r"\(O(n \log n)\)", "efficient sorts", "a bit more than twice"],
                    [r"\(O(n^{2})\)", "nested loops, bubble sort", "about four times"],
                ],
            },
        ],
    },
    ("xii", "15"): {
        "kind": "formulas",
        "title": "Descriptive statistics",
        "golden": True,
        "diagram": None,
        "blocks": [
            {
                "type": "p",
                "text": r"Mean: \(\bar{x} = \dfrac{\sum x}{n}\). Median is the middle value of the ordered list. Mode is the value that appears most often.",
            },
            {
                "type": "p",
                "text": r"For an even count, the median is the mean of the two middle values. Range is \(\max(x) - \min(x)\).",
            },
        ],
    },
}


LAW_NAMES = {
    "Law", "AND form", "OR form", "Identity", "Null", "Idempotent",
    "Complement", "Double NOT", "De Morgan",
}


def tidy_cards(cards: list[dict]) -> list[dict]:
    cleaned = []
    for card in cards:
        blocks = []
        for block in card["blocks"]:
            if block["type"] == "p":
                parts = [part.strip() for part in re.split(r"\s·\s", block["text"]) if part.strip()]
                if parts and all(part in LAW_NAMES for part in parts):
                    continue
                token = block["text"].strip()
                if token.lower().strip(".:") in CHROME:
                    continue
            if (
                blocks
                and block["type"] == "p"
                and blocks[-1]["type"] in {"def", "p", "tip", "exam", "warn"}
            ):
                prev = blocks[-1]["text"]
                nxt = block["text"]
                if nxt and not prev.endswith((".", "!", "?", ":", "—")) and nxt[:1].islower():
                    blocks[-1]["text"] = prev.rstrip() + " " + nxt
                    continue
            blocks.append(block)
        if not blocks and not card.get("diagram"):
            continue
        card["blocks"] = blocks
        cleaned.append(card)
    return cleaned


def attach_diagrams(book_id: str, day: str, cards: list[dict]) -> None:
    used: set[str] = set()
    for diagram_id, needle in DIAGRAMS.get((book_id, day), []):
        matches = [card for card in cards if needle in card["title"].lower()]
        numbered = [card for card in matches if card["title"][:1].isdigit()]
        host = numbered[0] if numbered else (matches[0] if matches else None)
        if host is None:
            host = cards[0] if cards else None
        if host is None or diagram_id in used:
            continue
        if host.get("diagram") is None:
            host["diagram"] = diagram_id
        else:
            cards.insert(cards.index(host) + 1, {
                "kind": "diagram",
                "title": host["title"],
                "golden": False,
                "blocks": [],
                "diagram": diagram_id,
            })
        used.add(diagram_id)


def mode_for(book_id: str, day: str, title: str) -> str:
    if day in {"24", "25", "26"}:
        return "blitz"
    if day == "27":
        return "recap"
    if day == "28":
        return "mock"
    if day == "29":
        return "mark"
    if day == "30":
        return "repair"
    if day in BOOKS[book_id]["checkpoints"]:
        return "checkpoint"
    return "teach"


def build_book(book_id: str) -> dict:
    doc = pymupdf.open(PDFS[book_id])
    pages = []
    carried_chapter = ""
    carried_day = ""
    for index, page in enumerate(doc):
        if index < 2:
            continue
        raw = blocks_of(page)
        grouped = {"H": [], "L": [], "R": [], "F": []}
        for block in raw:
            grouped[column_of(block)].append(block)
        for key in grouped:
            grouped[key].sort(key=lambda item: item["y0"])
        meta = header_meta(grouped["H"])
        cards = tidy_cards(consume(grouped["L"]) + consume(grouped["R"]) + consume(grouped["F"]))
        day = meta["day"] or carried_day or f"{index + 1:02d}"
        carried_day = day
        attach_diagrams(book_id, day, cards)
        extra = FORMULA_CARDS.get((book_id, day))
        if extra:
            # Place formula cards after the first golden section, else at the front.
            insert_at = 1 if cards else 0
            cards.insert(insert_at, json.loads(json.dumps(extra)))
        title = meta["title"] or f"Day {day}"
        mode = mode_for(book_id, day, title)
        if meta["chapter"]:
            carried_chapter = meta["chapter"]
        chapter = meta["chapter"] or ("Practice" if mode not in {"teach", "checkpoint"} else carried_chapter or "Notes")
        pages.append({
            "id": f"p{index + 1:02d}",
            "pdfPage": index + 1,
            "day": day,
            "chapter": chapter,
            "range": meta["range"],
            "title": title,
            "subtitle": meta["subtitle"],
            "mustLock": meta["mustLock"],
            "mode": mode_for(book_id, day, title),
            "cards": cards,
        })
    info = BOOKS[book_id]
    return {
        "id": book_id,
        "title": info["title"],
        "short": info["short"],
        "blurb": info["chapters_blurb"],
        "golden": info["golden"],
        "pages": pages,
    }


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    for book_id in ("xi", "xii"):
        book = build_book(book_id)
        path = OUT / f"{book_id}.json"
        path.write_text(json.dumps(book, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
        cards = sum(len(page["cards"]) for page in book["pages"])
        diagrams = sum(
            1
            for page in book["pages"]
            for card in page["cards"]
            if card.get("diagram")
        )
        print(f"{book_id}: pages={len(book['pages'])} cards={cards} diagrams={diagrams} bytes={path.stat().st_size}")


if __name__ == "__main__":
    main()
