#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build catalog.js from the four embedded CS PDFs."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import pymupdf

ROOT = Path(__file__).resolve().parents[1]
if str(Path(__file__).resolve().parent) not in sys.path:
    sys.path.insert(0, str(Path(__file__).resolve().parent))

from urdu_lectures import compose_lecture  # noqa: E402

PDF_DIR = ROOT / "app/src/main/assets/pdfs"
OUT_JS = ROOT / "app/src/main/assets/www/js/catalog.js"

BOOKS = [
    {
        "id": "xi",
        "title": "Class XI Lectures",
        "urTitle": "کلاس گیارہ لیکچرز",
        "subtitle": "Bilingual teacher's edition — Computer Systems to Digital Literacy",
        "badge": "Sindh 2026",
        "kind": "lecture",
        "pdf": "cs_xi_lectures.pdf",
        "accent": "#0f766e",
        "chapters": [
            (1, "Chapter 1: Computer Systems", 1, 26),
            (2, "Chapter 2: Computational Thinking & Algorithms", 27, 43),
            (3, "Chapter 3: Programming Fundamentals", 44, 69),
            (4, "Chapter 4: Data and Databases", 70, 95),
            (5, "Chapter 5: Applications & Impacts of Computing", 96, 110),
            (6, "Chapter 6: Digital Literacy", 111, 127),
        ],
    },
    {
        "id": "xii",
        "title": "Class XII Lectures",
        "urTitle": "کلاس بارہ لیکچرز",
        "subtitle": "Bilingual teacher's edition — HCI to Digital Entrepreneurship",
        "badge": "Sindh 2024–27",
        "kind": "lecture",
        "pdf": "cs_xii_lectures.pdf",
        "accent": "#1d4ed8",
        "chapters": [
            (1, "Chapter 1: Computer Systems (HCI)", 1, 21),
            (2, "Chapter 2: Algorithms & Data Structures", 22, 47),
            (3, "Chapter 3: Programming Fundamentals (Python)", 48, 75),
            (4, "Chapter 4: Data Analysis", 76, 102),
            (5, "Chapter 5: AI, Security & Collaboration", 103, 123),
            (6, "Chapter 6: Entrepreneurship in the Digital Age", 124, 147),
        ],
    },
    {
        "id": "qaxi",
        "title": "Class XI Q&A",
        "urTitle": "کلاس گیارہ سوال و جواب",
        "subtitle": "5-W concepts, differentiations, long answers, MCQs",
        "badge": "Exam Masterpiece",
        "kind": "qa",
        "pdf": "cs_xi_qa.pdf",
        "accent": "#b45309",
        "chapters": [
            (1, "Unit 01: Computer Systems", 2, 9),
            (2, "Unit 02: Computational Thinking & Algorithms", 10, 13),
            (3, "Unit 03: Programming Fundamentals", 14, 17),
            (4, "Unit 04: Data and Analysis", 18, 21),
            (5, "Unit 05: Applications & Impacts of Computing", 22, 24),
            (6, "Unit 06: Digital Literacy", 25, 27),
        ],
    },
    {
        "id": "qaxii",
        "title": "Class XII Q&A",
        "urTitle": "کلاس بارہ سوال و جواب",
        "subtitle": "5-W concepts, differentiations, long answers, MCQs",
        "badge": "Exam Masterpiece",
        "kind": "qa",
        "pdf": "cs_xii_qa.pdf",
        "accent": "#9f1239",
        "chapters": [
            (1, "Unit 01: Computer Systems (HCI)", 2, 5),
            (2, "Unit 02: Computational Thinking & Algorithms", 6, 9),
            (3, "Unit 03: Programming Fundamentals", 10, 13),
            (4, "Unit 04: Data and Analysis", 14, 16),
            (5, "Unit 05: Applications & Impacts of Computing", 17, 19),
            (6, "Unit 06: Entrepreneurship in the Digital Age", 20, 22),
        ],
    },
]

SKIP_TITLES = {
    "table of contents",
    "computer science xi",
    "computer science",
    "computer science xii",
    "board of intermediate education",
}

GOLDEN_NEEDLES = (
    "analog and digital",
    "basic logic gates",
    "logic gates (basic",
    "karnaugh",
    "k-map",
    "software development life cycle",
    "1.2 software development",
    "osi",
    "applications of hci",
    "importance of hci",
    "human computer interaction problems",
    "hci problems",
    "user interface design",
    "ui vs ux",
    "testing methods",
    "1.11.2",
)

HEADING_RE = re.compile(
    r"^("
    r"(?:\d+\.)+\d+.*|"
    r"unit\s+\d+.*|"
    r"q\d+\..*|"
    r"diff\s+\d+.*|"
    r"long q\d+.*|"
    r"mcq.*|"
    r"boolean operations.*|"
    r"universal logic.*|"
    r"advanced logic.*|"
    r"three-variable.*|"
    r"building a circuit.*|"
    r"detailed sdlc.*|"
    r"waterfall vs.*|"
    r"osi .*|"
    r"tcp/ip.*|"
    r"bubble sort.*|"
    r"selection sort.*|"
    r"linear search.*|"
    r"binary search.*|"
    r"common high-level.*|"
    r"vs code.*|"
    r"data types.*|"
    r"other important.*|"
    r"bitwise.*|"
    r"nested loops.*|"
    r"practical activity.*|"
    r"types of errors.*|"
    r"reading error.*|"
    r"database and dbms.*|"
    r"keys \(continued\).*|"
    r"types of relationships.*|"
    r"referential integrity.*|"
    r"library case.*|"
    r"database objects.*|"
    r"table creation.*|"
    r"filtering query.*|"
    r"data summarization.*|"
    r"data visualization.*|"
    r"iot components.*|"
    r"data analytics.*|"
    r"uses of iot.*|"
    r"information sources.*|"
    r"assistive tech.*|"
    r"data-collection.*|"
    r"primary vs.*|"
    r"presenting data.*|"
    r"methodology.*|"
    r"analysis and conclusion.*|"
    r"the final digital.*|"
    r"careers.*|"
    r"traditional vs.*|"
    r"types of user.*|"
    r"interfaces, environment.*|"
    r"hci problems.*|"
    r"trace table.*|"
    r"modularity example.*|"
    r"big o.*|"
    r"linear data.*|"
    r"non-linear.*|"
    r"list indexing.*|"
    r"list slicing.*|"
    r"built-in list.*|"
    r"activity:.*|"
    r"tuple .*|"
    r"mathematical operations.*|"
    r"set traversal.*|"
    r"dictionary .*|"
    r"accessing dictionary.*|"
    r"function components.*|"
    r"file methods.*|"
    r"3\.\d+.*|"
    r"flowchart of python.*|"
    r"creating a sqlite.*|"
    r"creating new variables.*|"
    r"handling missing.*|"
    r"measures of.*|"
    r"applications \(continued\).*|"
    r"secure collaboration.*|"
    r"security threats.*|"
    r"local examples.*|"
    r"from problem.*|"
    r"comparison of prototype.*|"
    r"class activity.*|"
    r"project rubric.*|"
    r"core concepts:.*|"
    r"short differentiations.*|"
    r"long descriptive.*|"
    r"summary of.*"
    r")$",
    re.I,
)


def arabic_ratio(text: str) -> float:
    if not text:
        return 0.0
    ar = sum(1 for ch in text if "\u0600" <= ch <= "\u06ff")
    return ar / max(len(text), 1)


def is_junk_line(line: str) -> bool:
    s = line.strip()
    if not s:
        return True
    low = s.lower()
    if low.startswith("page ") and len(s) < 16:
        return True
    if low in {"page", "what", "why", "who", "when", "where", "how"}:
        return False
    if "ultimate extended" in low or "ultimate 90+" in low:
        return True
    if s in {"★", "💡", "👨‍🏫"}:
        return True
    if arabic_ratio(s) > 0.18:
        return True
    letters = [ch for ch in s if ch.isalpha()]
    if letters and sum(ch.isascii() for ch in letters) / len(letters) < 0.55:
        return True
    return False


def clean_english(raw: str) -> list[str]:
    lines = []
    for line in raw.splitlines():
        s = " ".join(line.split())
        if is_junk_line(s):
            continue
        lines.append(s)
    # drop trailing page-only leftovers
    while lines and re.fullmatch(r"Page \d+", lines[-1], re.I):
        lines.pop()
    return lines


def page_heading(lines: list[str], fallback: str, qa: bool = False) -> str:
    for line in lines[:14]:
        low = line.lower().strip()
        if low in SKIP_TITLES:
            continue
        if line.lower().startswith("based on new"):
            continue
        if qa and re.match(r"^unit\s+\d+", low):
            continue
        if qa and low.startswith("core concepts"):
            return line
        if qa and re.match(r"^(q\d+|diff\s+\d+|long q\d+|mcq|short differentiations|long descriptive)", low):
            return line
        if HEADING_RE.match(line) or re.match(r"^\d+\.\d+", line) or line.endswith("★"):
            return line.replace("★", "").strip()
        if len(line) > 8 and len(line) < 90 and line[0].isupper() and arabic_ratio(line) < 0.05:
            return line
    return fallback


def is_skip_page(lines: list[str]) -> bool:
    if not lines:
        return True
    blob = " ".join(lines[:6]).lower()
    if "table of contents" in blob:
        return True
    if lines[0].lower() in SKIP_TITLES and any("bilingual" in x.lower() or "karachi" in x.lower() for x in lines[:8]):
        return True
    if lines[0].lower() == "computer science" and any("chapter" in x.lower() for x in lines[:6]):
        return True
    if "board of intermediate education" in blob and "masterpiece" in blob:
        return True
    return False


MATH_SUBS = [
    (re.compile(r"Y\s*=\s*A\s*[·.•]\s*B"), r"\\(Y = A \\cdot B\\)"),
    (re.compile(r"Y\s*=\s*\(A\s*[·.•]\s*B\)'"), r"\\(Y = (A \\cdot B)'\\)"),
    (re.compile(r"Y\s*=\s*A\s*\+\s*B"), r"\\(Y = A + B\\)"),
    (re.compile(r"Y\s*=\s*\(A\s*\+\s*B\)'"), r"\\(Y = (A + B)'\\)"),
    (re.compile(r"Y\s*=\s*A['′]"), r"\\(Y = A'\\)"),
    (re.compile(r"Y\s*=\s*A̅"), r"\\(Y = \\overline{A}\\)"),
    (re.compile(r"2ⁿ"), r"\\(2^n\\)"),
    (re.compile(r"\b2\^n\b"), r"\\(2^n\\)"),
    (re.compile(r"O\(([^)]+)\)"), r"\\(O(\1)\\)"),
    (re.compile(r"A\s*⋅\s*B"), r"\\(A \\cdot B\\)"),
    (re.compile(r"\bA · B\b"), r"\\(A \\cdot B\\)"),
    (re.compile(r"HIGH \(1\)"), r"HIGH \\(1\\)"),
    (re.compile(r"LOW \(0\)"), r"LOW \\(0\\)"),
    (re.compile(r"TRUE \(1\)"), r"TRUE \\(1\\)"),
    (re.compile(r"FALSE \(0\)"), r"FALSE \\(0\\)"),
]


def mathify(text: str) -> str:
    out = text
    for pat, repl in MATH_SUBS:
        out = pat.sub(repl, out)
    return out


def escape_html(text: str) -> str:
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )


CODEY = re.compile(
    r"^(def |for |while |if |elif |else:|import |print\(|return |with |try:|except|cursor\.|conn\.|"
    r"df\[|pd\.|plt\.|SELECT |CREATE |INSERT |FROM |WHERE )",
    re.I,
)


def lines_to_html(lines: list[str]) -> str:
    blocks: list[str] = []
    para: list[str] = []
    table_buf: list[str] = []
    code_buf: list[str] = []

    def flush_para():
        if para:
            text = mathify(escape_html(" ".join(para)))
            blocks.append(f"<p>{text}</p>")
            para.clear()

    def flush_code():
        if code_buf:
            body = escape_html("\n".join(code_buf))
            blocks.append(f"<pre class='code'><code>{body}</code></pre>")
            code_buf.clear()

    def flush_table():
        if table_buf:
            cells = [escape_html(c) for c in table_buf]
            row = "".join(f"<span class='cell'>{mathify(c)}</span>" for c in cells)
            blocks.append(f"<div class='flex-table'>{row}</div>")
            table_buf.clear()

    header_words = {"feature", "advantage", "aspect", "gate", "channel", "concept", "a", "b", "y"}

    for line in lines:
        if CODEY.match(line) or (code_buf and (line.startswith("    ") or line.startswith("#"))):
            flush_para()
            flush_table()
            code_buf.append(line)
            continue
        if code_buf:
            flush_code()

        if re.match(r"^\d+\.\d+", line) or (line.isupper() and 8 < len(line) < 70):
            flush_para()
            flush_table()
            blocks.append(f"<h3>{escape_html(line.replace('★', '').strip())}</h3>")
            continue
        if line.endswith("★") or line.upper().startswith("GOLDEN") or line.startswith("★ "):
            flush_para()
            blocks.append(f"<div class='golden'>{escape_html(line.replace('★', '').strip())}</div>")
            continue
        if line.lower() in {"what", "why", "who", "when", "where", "how", "context"}:
            flush_para()
            blocks.append(f"<h4 class='wtag'>{escape_html(line)}</h4>")
            continue
        if len(line) <= 28 and (line.lower() in header_words or re.fullmatch(r"[01]", line)):
            table_buf.append(line)
            if len(table_buf) >= 8:
                flush_table()
            continue
        if table_buf and len(line) < 32:
            table_buf.append(line)
            continue
        if table_buf:
            flush_table()

        if len(line) < 70 and (
            line.endswith(":")
            or re.match(r"^(Q\d+|Diff \d+|Long Q\d+|DETAIL \d+|PROB \d+|MCQ)", line, re.I)
        ):
            flush_para()
            blocks.append(f"<h4>{escape_html(line)}</h4>")
            continue

        para.append(line)
        if line.endswith(".") and len(" ".join(para)) > 160:
            flush_para()

    flush_code()
    flush_table()
    flush_para()
    return "\n".join(blocks)


def inject_figure(title: str, html: str) -> str:
    t = title.lower()
    fig = ""
    if "discrete" in t or "continuous" in t:
        fig = FIGURE_STAIRS
    elif "analog" in t or "digital signal" in t:
        fig = FIGURE_WAVES
    elif "logic gate" in t or "and, or, not" in t or t.startswith("1.1.7"):
        fig = FIGURE_GATES
    elif "osi" in t:
        fig = FIGURE_OSI
    elif "karnaugh" in t or "k-map" in t:
        fig = FIGURE_KMAP
    elif "stack" in t:
        fig = FIGURE_STACK
    elif "ui vs ux" in t or "user interface design" in t:
        fig = FIGURE_UIUX
    if fig:
        return fig + html
    return html


FIGURE_STAIRS = """
<figure class="svg-fig" aria-label="Stairs versus ramp">
<svg viewBox="0 0 360 120" xmlns="http://www.w3.org/2000/svg">
  <rect x="10" y="70" width="40" height="30" fill="#0f766e"/>
  <rect x="50" y="50" width="40" height="50" fill="#14b8a6"/>
  <rect x="90" y="30" width="40" height="70" fill="#0f766e"/>
  <path d="M190 95 L330 25 L330 95 Z" fill="#1d4ed8" opacity="0.85"/>
  <text x="50" y="115" font-size="11" fill="#134e4a">Discrete stairs</text>
  <text x="230" y="115" font-size="11" fill="#1e3a8a">Continuous ramp</text>
</svg>
<figcaption>Discrete values sit on separate steps. Continuous values can rest anywhere on the ramp.</figcaption>
</figure>
"""

FIGURE_WAVES = """
<figure class="svg-fig" aria-label="Analog sine versus digital square">
<svg viewBox="0 0 360 110" xmlns="http://www.w3.org/2000/svg">
  <path d="M10 55 C 40 10, 70 100, 100 55 S 160 10, 190 55 S 250 100, 280 55" fill="none" stroke="#0f766e" stroke-width="3"/>
  <path d="M10 90 L60 90 L60 25 L120 25 L120 90 L180 90 L180 25 L240 25 L240 90 L300 90" fill="none" stroke="#1d4ed8" stroke-width="3"/>
  <text x="12" y="14" font-size="11" fill="#0f766e">Analog sine</text>
  <text x="200" y="14" font-size="11" fill="#1d4ed8">Digital square 1/0</text>
</svg>
<figcaption>Analog varies smoothly. Digital jumps between HIGH \\(1\\) and LOW \\(0\\).</figcaption>
</figure>
"""

FIGURE_GATES = """
<figure class="svg-fig" aria-label="AND OR NOT gate shapes">
<svg viewBox="0 0 360 110" xmlns="http://www.w3.org/2000/svg">
  <path d="M20 25 H70 Q110 55 70 85 H20 Z" fill="none" stroke="#0f766e" stroke-width="2"/>
  <text x="38" y="60" font-size="12" fill="#0f766e">AND</text>
  <path d="M140 25 Q190 55 140 85 L140 25" fill="none" stroke="#1d4ed8" stroke-width="2"/>
  <path d="M140 25 H175" stroke="#1d4ed8" stroke-width="2"/>
  <text x="148" y="60" font-size="12" fill="#1d4ed8">OR</text>
  <path d="M250 35 L290 55 L250 75 Z" fill="none" stroke="#b45309" stroke-width="2"/>
  <circle cx="298" cy="55" r="5" fill="none" stroke="#b45309" stroke-width="2"/>
  <text x="252" y="100" font-size="12" fill="#b45309">NOT</text>
</svg>
<figcaption>AND \\(Y=A\\cdot B\\), OR \\(Y=A+B\\), NOT \\(Y=A'\\). Universal gates NAND/NOR can rebuild any of these.</figcaption>
</figure>
"""

FIGURE_OSI = """
<figure class="svg-fig" aria-label="OSI seven layers">
<svg viewBox="0 0 360 170" xmlns="http://www.w3.org/2000/svg">
  <g font-size="11" fill="#0f172a">
    <rect x="40" y="8" width="280" height="20" fill="#99f6e4"/><text x="50" y="22">7 Application</text>
    <rect x="40" y="30" width="280" height="20" fill="#5eead4"/><text x="50" y="44">6 Presentation</text>
    <rect x="40" y="52" width="280" height="20" fill="#2dd4bf"/><text x="50" y="66">5 Session</text>
    <rect x="40" y="74" width="280" height="20" fill="#93c5fd"/><text x="50" y="88">4 Transport — TCP/UDP</text>
    <rect x="40" y="96" width="280" height="20" fill="#60a5fa"/><text x="50" y="110">3 Network — IP</text>
    <rect x="40" y="118" width="280" height="20" fill="#fbbf24"/><text x="50" y="132">2 Data Link</text>
    <rect x="40" y="140" width="280" height="20" fill="#f59e0b"/><text x="50" y="154">1 Physical</text>
  </g>
</svg>
<figcaption>OSI has seven layers. TCP/IP folds these into four practical layers.</figcaption>
</figure>
"""

FIGURE_KMAP = """
<figure class="svg-fig" aria-label="Two variable Karnaugh map">
<svg viewBox="0 0 240 150" xmlns="http://www.w3.org/2000/svg">
  <text x="70" y="18" font-size="12">B=0</text><text x="150" y="18" font-size="12">B=1</text>
  <text x="8" y="55" font-size="12">A=0</text>
  <text x="8" y="105" font-size="12">A=1</text>
  <rect x="50" y="30" width="70" height="50" fill="#ccfbf1" stroke="#0f766e"/>
  <rect x="120" y="30" width="70" height="50" fill="#fff" stroke="#0f766e"/>
  <rect x="50" y="80" width="70" height="50" fill="#ccfbf1" stroke="#0f766e"/>
  <rect x="120" y="80" width="70" height="50" fill="#ccfbf1" stroke="#0f766e"/>
  <text x="78" y="60" font-size="16">1</text>
  <text x="148" y="60" font-size="16">0</text>
  <text x="78" y="110" font-size="16">1</text>
  <text x="148" y="110" font-size="16">1</text>
</svg>
<figcaption>Group adjacent 1s in powers of two. Larger groups give simpler Boolean expressions.</figcaption>
</figure>
"""

FIGURE_STACK = """
<figure class="svg-fig" aria-label="Stack LIFO versus queue FIFO">
<svg viewBox="0 0 360 120" xmlns="http://www.w3.org/2000/svg">
  <rect x="40" y="20" width="70" height="24" fill="#99f6e4" stroke="#0f766e"/><text x="58" y="37">Top</text>
  <rect x="40" y="44" width="70" height="24" fill="#5eead4" stroke="#0f766e"/>
  <rect x="40" y="68" width="70" height="24" fill="#2dd4bf" stroke="#0f766e"/>
  <text x="40" y="112" font-size="11">Stack LIFO</text>
  <rect x="200" y="50" width="40" height="30" fill="#93c5fd" stroke="#1d4ed8"/>
  <rect x="244" y="50" width="40" height="30" fill="#60a5fa" stroke="#1d4ed8"/>
  <rect x="288" y="50" width="40" height="30" fill="#3b82f6" stroke="#1d4ed8"/>
  <text x="200" y="112" font-size="11">Queue FIFO</text>
</svg>
<figcaption>Stack: last in, first out. Queue: first in, first out.</figcaption>
</figure>
"""

FIGURE_UIUX = """
<figure class="svg-fig" aria-label="UI skin versus UX journey">
<svg viewBox="0 0 360 110" xmlns="http://www.w3.org/2000/svg">
  <rect x="20" y="20" width="140" height="70" rx="10" fill="#ccfbf1" stroke="#0f766e"/>
  <circle cx="50" cy="48" r="10" fill="#0f766e"/>
  <rect x="70" y="40" width="70" height="10" fill="#0f766e"/>
  <rect x="70" y="58" width="50" height="10" fill="#14b8a6"/>
  <text x="40" y="100" font-size="11">UI — look</text>
  <path d="M190 55 H250" stroke="#1d4ed8" stroke-width="3"/>
  <circle cx="190" cy="55" r="8" fill="#1d4ed8"/>
  <circle cx="250" cy="55" r="8" fill="#1d4ed8"/>
  <circle cx="310" cy="55" r="8" fill="#1d4ed8"/>
  <path d="M250 55 H310" stroke="#1d4ed8" stroke-width="3"/>
  <text x="210" y="100" font-size="11">UX — journey</text>
</svg>
<figcaption>UI is the paint and controls. UX is how the whole trip feels.</figcaption>
</figure>
"""


def is_golden(title: str) -> bool:
    low = title.lower()
    return any(n in low for n in GOLDEN_NEEDLES)


def extract_book(meta: dict) -> dict:
    doc = pymupdf.open(PDF_DIR / meta["pdf"])
    chapters = []
    for ch_index, ch_title, start, end in meta["chapters"]:
        raw_topics = []
        for page_no in range(start, end + 1):
            raw = doc[page_no - 1].get_text("text")
            lines = clean_english(raw)
            if is_skip_page(lines):
                continue
            heading = page_heading(lines, ch_title, qa=meta["kind"] == "qa")
            raw_topics.append(
                {
                    "heading": heading,
                    "page": page_no,
                    "lines": lines,
                }
            )

        merged = []
        for item in raw_topics:
            heading = item["heading"]
            cont = "continued" in heading.lower() or heading.lower().startswith("other important")
            same_generic = heading.upper().startswith("UNIT ") and heading == merged[-1]["title"] if merged else False
            if merged and (cont or (heading == merged[-1]["title"] and not same_generic)):
                merged[-1]["lines"].extend(item["lines"])
                merged[-1]["endPage"] = item["page"]
            else:
                merged.append(
                    {
                        "title": heading,
                        "startPage": item["page"],
                        "endPage": item["page"],
                        "lines": list(item["lines"]),
                    }
                )

        topics = []
        for i, topic in enumerate(merged, start=1):
            html = inject_figure(topic["title"], lines_to_html(topic["lines"]))
            excerpt = " ".join(topic["lines"][:12])
            golden = is_golden(topic["title"]) or any("golden topic" in x.lower() for x in topic["lines"][:8])
            lecture = compose_lecture(
                book_id=meta["id"],
                chapter_index=ch_index,
                chapter_title=ch_title,
                topic_title=topic["title"],
                english_excerpt=excerpt,
                golden=golden,
                kind=meta["kind"],
            )
            topics.append(
                {
                    "id": f"{meta['id']}-ch{ch_index}-t{i:02d}",
                    "title": topic["title"],
                    "golden": golden,
                    "startPage": topic["startPage"],
                    "endPage": topic["endPage"],
                    "html": html,
                    "urduLecture": lecture,
                }
            )
        chapters.append(
            {
                "id": f"{meta['id']}-ch{ch_index}",
                "index": ch_index,
                "title": ch_title,
                "topics": topics,
            }
        )
    doc.close()
    return {
        "id": meta["id"],
        "title": meta["title"],
        "urTitle": meta["urTitle"],
        "subtitle": meta["subtitle"],
        "badge": meta["badge"],
        "kind": meta["kind"],
        "pdf": meta["pdf"],
        "accent": meta["accent"],
        "chapters": chapters,
    }


def main() -> None:
    books = [extract_book(meta) for meta in BOOKS]
    topic_count = sum(len(ch["topics"]) for b in books for ch in b["chapters"])
    catalog = {
        "version": "1.0.0",
        "title": "CS XI–XII Composite",
        "subtitle": "Embedded bilingual lectures — English on screen, Urdu voice",
        "curriculum": "Board of Intermediate Education Karachi · New Sindh Curriculum",
        "displayLanguage": "en",
        "narrationLanguage": "ur",
        "mathjax": "svg",
        "layout": "flexbox",
        "books": books,
    }
    OUT_JS.parent.mkdir(parents=True, exist_ok=True)
    payload = json.dumps(catalog, ensure_ascii=False)
    OUT_JS.write_text(f"window.CS_APP = {payload};\n", encoding="utf-8")
    print(f"Wrote {OUT_JS} ({OUT_JS.stat().st_size} bytes), topics={topic_count}")


if __name__ == "__main__":
    main()
