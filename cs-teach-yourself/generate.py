#!/usr/bin/env python3
"""Generate CS XI/XII Teach Yourself HTML from cheat-sheet PDFs."""
from __future__ import annotations

import html
import json
import re
from pathlib import Path

import pymupdf

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "source-pdfs"
PDFS = {
    "XI": SRC / "CS_XI___30-Day_Ultimate_Cheat-Sheet___Complete_Edition__Days_1_30__a968.pdf",
    "XII": SRC / "CS_XII___30-Day_Ultimate_Cheat-Sheet___Complete_Edition__Days_1_30__9830.pdf",
}

META = {
    "XI": {
        "title": "Computer Science XI — Teach Yourself Edition",
        "subtitle": "30-Day Ultimate Cheat-Sheet · Urdish · New Sindh Curriculum 2026",
        "file": "cs-xi-teach-yourself.html",
    },
    "XII": {
        "title": "Computer Science XII — Teach Yourself Edition",
        "subtitle": "30-Day Ultimate Cheat-Sheet · Urdish · New Sindh Curriculum 2026",
        "file": "cs-xii-teach-yourself.html",
    },
}


def pdf_pages(path: Path) -> list[str]:
    doc = pymupdf.open(path)
    texts = [page.get_text() for page in doc]
    doc.close()
    return texts


def parse_toc(toc_text: str) -> list[dict]:
    """Return ordered day entries: day_num, title, pdf_pages (1-based)."""
    toc_text = toc_text.split("30-din progress tracker")[0]
    lines = [ln.strip() for ln in toc_text.splitlines()]
    raw: list[dict] = []
    i = 0
    while i < len(lines):
        m = re.match(r"Day\s+(\d{2})$", lines[i])
        if not m:
            i += 1
            continue
        day_num = int(m.group(1))
        i += 1
        title_parts: list[str] = []
        page: int | None = None
        while i < len(lines):
            line = lines[i].strip()
            if re.match(r"Day\s+\d{2}$", line):
                break
            if line in ("Day", "Topic", "Page", "XI", "XII"):
                i += 1
                continue
            if re.fullmatch(r"\d{1,2}", line):
                num = int(line)
                if 3 <= num <= 35:
                    page = num
                    i += 1
                    break
            elif line:
                title_parts.append(line)
            i += 1
        if page is not None:
            raw.append({"day": day_num, "title": " ".join(title_parts), "start_page": page})

    merged: list[dict] = []
    for entry in raw:
        if merged and merged[-1]["day"] == entry["day"]:
            merged[-1]["extra_starts"].append(entry["start_page"])
            if len(entry["title"]) > len(merged[-1]["title"]):
                merged[-1]["title"] = entry["title"]
        else:
            merged.append(
                {
                    "day": entry["day"],
                    "title": entry["title"],
                    "start_page": entry["start_page"],
                    "extra_starts": [],
                }
            )

    for idx, entry in enumerate(merged):
        starts = sorted({entry["start_page"], *entry["extra_starts"]})
        if idx + 1 < len(merged):
            next_start = merged[idx + 1]["start_page"]
            span = list(range(starts[0], next_start))
        else:
            span = list(range(starts[0], starts[-1] + 1))
        for p in starts:
            if p not in span:
                span.append(p)
        entry["pdf_pages"] = sorted(span)

    return merged


def strip_page_footer(text: str) -> str:
    text = re.sub(r"Page \d+ / 35\s*", "", text)
    text = re.sub(r"CS X[II]+ · Ultimate Cheat-Sheet.*", "", text)
    text = re.sub(r"CS X[II]+ · Complete Edition · Contents\s*", "", text)
    text = re.sub(r"☰\s*Book\s*", "", text)
    return text.strip()


def enrich_math(text: str) -> str:
    """Wrap common notation for MathJax."""
    replacements = [
        (r"\bO\(n\^2\)", r"\\(O(n^2)\\)"),
        (r"\bO\(n log n\)", r"\\(O(n \\log n)\\)"),
        (r"\bO\(1\)", r"\\(O(1)\\)"),
        (r"\bO\(n\)", r"\\(O(n)\\)"),
        (r"\bO\(log n\)", r"\\(O(\\log n)\\)"),
        (r"Y = A ⊕ B", r"\\(Y = A \\oplus B\\)"),
        (r"Y = \(A ⊕ B\)'", r"\\(Y = (A \\oplus B)'\\)"),
        (r"Y = A·B \+ C", r"\\(Y = A \\cdot B + C\\)"),
        (r"n \* \(n \+ 1\) // 2", r"\\(n(n+1)/2\\)"),
        (r"2\^n", r"\\(2^n\\)"),
    ]
    for pat, repl in replacements:
        text = re.sub(pat, repl, text)
    return text


def format_blocks(raw: str) -> str:
    raw = strip_page_footer(raw)
    raw = enrich_math(raw)
    parts: list[str] = []
    for block in re.split(r"\n{2,}", raw):
        block = block.strip()
        if not block:
            continue
        cls = "block"
        if block.startswith("Def (paper"):
            cls = "block def-box"
        elif "🧠 Yaad rakho" in block[:40]:
            cls = "block mnemonic"
        elif "📝 Paper mein" in block[:40]:
            cls = "block paper-tip"
        elif block.startswith("⚠"):
            cls = "block warning"
        elif "★ Must lock" in block or "★ Golden" in block:
            cls = "block golden"
        elif re.match(r"Chapter \d+", block):
            cls = "block chapter"
        escaped = html.escape(block)
        escaped = escaped.replace("\n", "<br>")
        parts.append(f'<div class="{cls}">{escaped}</div>')
    return "\n".join(parts)


def svg_for_day(level: str, day: int) -> str:
    """Topic-aware SVG diagrams for teach-yourself panels."""
    common_style = 'xmlns="http://www.w3.org/2000/svg" role="img" aria-hidden="true"'
    if level == "XI":
        if day == 1:
            return f'<svg {common_style} viewBox="0 0 320 140"><text x="8" y="18" font-size="12" fill="#334">Discrete = Stairs</text><polyline points="20,110 20,90 60,90 60,70 100,70 100,50 140,50" fill="none" stroke="#2563eb" stroke-width="3"/><text x="170" y="18" font-size="12" fill="#334">Continuous = Ramp</text><line x1="180" y1="110" x2="300" y2="40" stroke="#059669" stroke-width="3"/><circle cx="240" cy="70" r="4" fill="#059669"/></svg>'
        if day == 2:
            return f'<svg {common_style} viewBox="0 0 320 160"><rect x="10" y="60" width="40" height="30" fill="#dbeafe" stroke="#2563eb"/><text x="18" y="80" font-size="11">AND</text><rect x="90" y="60" width="40" height="30" fill="#fef3c7" stroke="#d97706"/><text x="98" y="80" font-size="11">OR</text><rect x="170" y="60" width="40" height="30" fill="#fce7f3" stroke="#db2777"/><text x="176" y="80" font-size="11">NOT</text><text x="10" y="130" font-size="11" fill="#555">Inputs → gate → single output</text></svg>'
        if day == 3:
            return f'<svg {common_style} viewBox="0 0 200 200"><text x="10" y="20" font-size="12">K-Map (2-var)</text><rect x="40" y="30" width="60" height="60" fill="#fff" stroke="#333"/><rect x="100" y="30" width="60" height="60" fill="#eff6ff" stroke="#333"/><rect x="40" y="90" width="60" height="60" fill="#eff6ff" stroke="#333"/><rect x="100" y="90" width="60" height="60" fill="#dbeafe" stroke="#333"/><text x="25" y="55" font-size="10">A</text><text x="75" y="25" font-size="10">B</text></svg>'
        if day == 5:
            return f'<svg {common_style} viewBox="0 0 280 200"><text x="10" y="16" font-size="12">OSI layers (top→bottom)</text><rect x="40" y="24" width="200" height="18" fill="#e0e7ff"/><text x="50" y="37" font-size="10">7 Application</text><rect x="40" y="44" width="200" height="18" fill="#c7d2fe"/><text x="50" y="57" font-size="10">…</text><rect x="40" y="64" width="200" height="18" fill="#a5b4fc"/><text x="50" y="77" font-size="10">4 Transport</text><rect x="40" y="84" width="200" height="18" fill="#818cf8"/><text x="50" y="97" font-size="10">3 Network</text><rect x="40" y="104" width="200" height="18" fill="#6366f1" fill-opacity="0.5"/><text x="50" y="117" font-size="10">1 Physical</text></svg>'
        if day == 7:
            return f'<svg {common_style} viewBox="0 0 260 120"><text x="8" y="16" font-size="12">Bubble sort pass</text><rect x="20" y="40" width="30" height="50" fill="#fca5a5"/><rect x="55" y="30" width="30" height="60" fill="#fdba74"/><rect x="90" y="50" width="30" height="40" fill="#fde047"/><rect x="125" y="60" width="30" height="30" fill="#86efac"/><text x="20" y="110" font-size="10">Compare & swap adjacent</text></svg>'
        if day == 8:
            return f'<svg {common_style} viewBox="0 0 280 100"><line x1="20" y1="50" x2="260" y2="50" stroke="#94a3b8"/><circle cx="60" cy="50" r="8" fill="#2563eb"/><circle cx="120" cy="50" r="8" fill="#2563eb"/><circle cx="180" cy="50" r="8" fill="#2563eb"/><circle cx="240" cy="50" r="8" fill="#2563eb"/><text x="20" y="80" font-size="10">Linear search → check each · Binary → halve sorted list</text></svg>'
        if day == 15:
            return f'<svg {common_style} viewBox="0 0 240 140"><ellipse cx="120" cy="40" rx="70" ry="22" fill="#e0f2fe" stroke="#0284c7"/><rect x="50" y="70" width="140" height="40" rx="4" fill="#f0fdf4" stroke="#16a34a"/><text x="70" y="95" font-size="11">Entity → Table</text></svg>'
    if level == "XII":
        if day == 1:
            return f'<svg {common_style} viewBox="0 0 280 120"><rect x="20" y="20" width="100" height="80" rx="8" fill="#f1f5f9" stroke="#64748b"/><rect x="160" y="30" width="100" height="60" rx="6" fill="#dbeafe" stroke="#2563eb"/><path d="M120 60 H160" stroke="#334" marker-end="url(#arr)"/><text x="35" y="55" font-size="10">User</text><text x="175" y="55" font-size="10">System</text></svg>'
        if day == 4:
            return f'<svg {common_style} viewBox="0 0 200 160"><rect x="20" y="20" width="160" height="120" fill="#fff" stroke="#333" stroke-dasharray="4"/><rect x="40" y="40" width="120" height="24" fill="#e2e8f0"/><rect x="40" y="72" width="80" height="40" fill="#bfdbfe"/><text x="30" y="150" font-size="10">Wireframe blocks</text></svg>'
        if day == 6:
            return f'<svg {common_style} viewBox="0 0 240 100"><text x="10" y="20" font-size="12">Growth curves</text><path d="M20 80 Q80 75 120 50 T220 20" fill="none" stroke="#2563eb" stroke-width="2"/><path d="M20 80 L220 30" fill="none" stroke="#059669" stroke-width="2"/><text x="180" y="25" font-size="9">O(n)</text><text x="180" y="45" font-size="9">O(log n)</text></svg>'
        if day == 8:
            return f'<svg {common_style} viewBox="0 0 200 160"><rect x="90" y="20" width="50" height="24" fill="#dbeafe" stroke="#2563eb"/><line x1="115" y1="44" x2="115" y2="60" stroke="#333"/><rect x="90" y="60" width="50" height="24" fill="#dbeafe" stroke="#2563eb"/><text x="20" y="110" font-size="10">Stack: push/pop at top (LIFO)</text></svg>'
        if day == 16:
            return f'<svg {common_style} viewBox="0 0 260 120"><circle cx="40" cy="60" r="12" fill="#fef3c7" stroke="#d97706"/><circle cx="100" cy="40" r="12" fill="#fef3c7" stroke="#d97706"/><circle cx="100" cy="80" r="12" fill="#fef3c7" stroke="#d97706"/><circle cx="160" cy="60" r="12" fill="#fde68a" stroke="#d97706"/><circle cx="220" cy="60" r="12" fill="#86efac" stroke="#16a34a"/><line x1="52" y1="55" x2="88" y2="42" stroke="#666"/><line x1="52" y1="65" x2="88" y2="78" stroke="#666"/><line x1="112" y1="50" x2="148" y2="58" stroke="#666"/><line x1="172" y1="60" x2="208" y2="60" stroke="#666"/><text x="10" y="110" font-size="10">Neural net: layers of nodes</text></svg>'
    # Default: 30-day progress ring
    return f'<svg {common_style} viewBox="0 0 120 120"><circle cx="60" cy="60" r="48" fill="none" stroke="#e2e8f0" stroke-width="10"/><path d="M60 12 A48 48 0 1 1 59 12" fill="none" stroke="#6366f1" stroke-width="10" stroke-linecap="round"/><text x="60" y="65" text-anchor="middle" font-size="14" fill="#4338ca">Day {day:02d}</text></svg>'


def day_phase(day: int) -> str:
    if day in (5, 8, 13, 16, 19, 23):
        return "checkpoint"
    if day >= 24:
        return "blitz" if day < 28 else ("mock" if day < 30 else "repair")
    return "teach"


SCHEDULE = """
<div class="schedule flex-row">
  <div class="slot"><strong>0–15′</strong> Kal ka ★ recap</div>
  <div class="slot"><strong>15–105′</strong> Aaj ke cards (Teach)</div>
  <div class="slot"><strong>105–135′</strong> Closed-book drill</div>
  <div class="slot"><strong>135–180′</strong> Ek 5-mark answer</div>
</div>
"""


def build_html(level: str, days: list[dict], page_texts: list[str]) -> str:
    meta = META[level]
    nav_items = []
    articles = []

    for entry in days:
        d = entry["day"]
        chunks = []
        for p in entry["pdf_pages"]:
            if 1 <= p <= len(page_texts):
                chunks.append(page_texts[p - 1])
        body = format_blocks("\n\n".join(chunks))
        phase = day_phase(d)
        svg = svg_for_day(level, d)
        nav_items.append(
            f'<a class="nav-day" href="#day-{d:02d}" data-day="{d}">Day {d:02d}</a>'
        )
        articles.append(
            f"""
<article class="day-card phase-{phase}" id="day-{d:02d}" data-day="{d}">
  <header class="day-header flex-row">
    <div>
      <p class="eyebrow">Day {d:02d} · {phase.title()}</p>
      <h2>{html.escape(entry["title"])}</h2>
    </div>
    <div class="header-actions flex-row">
      <button type="button" class="btn tts-read" data-tts-target="#day-{d:02d} .lesson-body" aria-label="Read aloud">🔊 Listen</button>
      <button type="button" class="btn btn-ghost drill-toggle" aria-expanded="false">✎ Drill</button>
    </div>
  </header>
  <div class="lesson flex-row">
    <section class="lesson-body flex-col">
      {body}
      <details class="checkpoint-panel">
        <summary>Closed-book checkpoint (105–135′)</summary>
        <p>Book band karke ★ Must lock definitions likho. Phir answer key se match karo.</p>
        <textarea rows="4" placeholder="Apna jawab yahan likho…" aria-label="Checkpoint notes day {d}"></textarea>
      </details>
    </section>
    <aside class="diagram flex-col" aria-label="Visual aid">
      {svg}
      <p class="diagram-caption">SVG concept map · is din ke topic se linked</p>
    </aside>
  </div>
</article>"""
        )

    nav = "\n".join(nav_items)
    content = "\n".join(articles)

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover"/>
  <meta name="apple-mobile-web-app-capable" content="yes"/>
  <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent"/>
  <meta name="theme-color" content="#0f172a"/>
  <meta name="format-detection" content="telephone=no"/>
  <title>{html.escape(meta["title"])}</title>
  <link rel="stylesheet" href="teach-yourself.css"/>
  <script>
    window.MathJax = {{
      tex: {{ inlineMath: [['\\\\(','\\\\)']], displayMath: [['\\\\[','\\\\]']] }},
      svg: {{ fontCache: 'global' }}
    }};
  </script>
  <script defer src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-svg.js"></script>
  <script defer src="teach-yourself.js"></script>
</head>
<body class="edition-{level.lower()}">
  <header class="site-header flex-row">
    <div>
      <p class="eyebrow">Teach Yourself Edition</p>
      <h1>{html.escape(meta["title"])}</h1>
      <p class="subtitle">{html.escape(meta["subtitle"])}</p>
    </div>
    <div class="tts-bar flex-col">
      <label class="flex-row"><span>Voice</span>
        <select id="tts-voice" aria-label="TTS voice"></select>
      </label>
      <label class="flex-row"><span>Rate</span>
        <input type="range" id="tts-rate" min="0.6" max="1.4" step="0.05" value="1"/>
      </label>
      <button type="button" class="btn" id="tts-stop">Stop speech</button>
    </div>
  </header>
  {SCHEDULE}
  <div class="shell flex-row">
    <nav class="sidebar flex-col" aria-label="Day navigation">
      <a class="nav-home" href="index.html">← Both classes</a>
      {nav}
    </nav>
    <main class="main flex-col">
      {content}
    </main>
  </div>
  <footer class="site-footer">
    <p>Offline-friendly after first load · MathJax + Web Speech API · Flexbox layout · inline SVG</p>
  </footer>
</body>
</html>
"""


INDEX_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1"/>
  <title>CS Teach Yourself — XI & XII</title>
  <link rel="stylesheet" href="teach-yourself.css"/>
</head>
<body>
  <header class="site-header flex-row">
    <div>
      <p class="eyebrow">30-Day Ultimate Cheat-Sheet</p>
      <h1>Computer Science Teach Yourself Edition</h1>
      <p class="subtitle">Interactive HTML · Text-to-Speech · MathJax · SVG diagrams · Flexbox</p>
    </div>
  </header>
  <main class="index-main flex-row">
    <a class="index-card" href="cs-xi-teach-yourself.html">
      <h2>Class XI</h2>
      <p>Boolean logic, Python fundamentals, DBMS, digital literacy — Days 1–30.</p>
      <span class="btn">Open XI Teach Yourself →</span>
    </a>
    <a class="index-card" href="cs-xii-teach-yourself.html">
      <h2>Class XII</h2>
      <p>HCI, data structures, ML, entrepreneurship — Days 1–30.</p>
      <span class="btn">Open XII Teach Yourself →</span>
    </a>
  </main>
  <footer class="site-footer">
    <p>Generated from Complete Edition PDFs · New Sindh Curriculum 2026</p>
  </footer>
</body>
</html>
"""


def main() -> None:
    manifest = {}
    for level, pdf_path in PDFS.items():
        pages = pdf_pages(pdf_path)
        toc = parse_toc(pages[1])
        html_doc = build_html(level, toc, pages)
        out = ROOT / META[level]["file"]
        out.write_text(html_doc, encoding="utf-8")
        manifest[level] = [{"day": d["day"], "title": d["title"], "pages": d["pdf_pages"]} for d in toc]
        print(f"Wrote {out} ({len(toc)} days)")

    (ROOT / "index.html").write_text(INDEX_HTML, encoding="utf-8")
    (ROOT / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print("Done.")


if __name__ == "__main__":
    main()
