#!/usr/bin/env python3
"""Turn lecture-notes/index.html into speakable JSON for the Android app."""

from __future__ import annotations

import json
import re
from pathlib import Path

from bs4 import BeautifulSoup, NavigableString, Tag

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "lecture-notes" / "index.html"
OUT = ROOT / "lectures" / "src" / "main" / "assets" / "lectures.json"
OUT_HTML = ROOT / "lectures" / "src" / "main" / "assets" / "notes" / "index.html"

SPEECH_SYMBOL = {
    "cdot": " times ",
    "times": " times ",
    "oplus": " exclusive or ",
    "sigma": " sigma",
    "leq": " less than or equal to ",
    "le": " less than or equal to ",
    "geq": " greater than or equal to ",
    "ge": " greater than or equal to ",
    "neq": " not equal to ",
    "ne": " not equal to ",
    "approx": " approximately ",
    "in": " in ",
    "cup": " union ",
    "cap": " intersection ",
    "setminus": " minus ",
    "log": " log",
    "sum": " sum",
    "quad": " ",
    "qquad": " ",
    ",": " ",
    ";": " ",
    "!": "",
    "left": "",
    "right": "",
    "lfloor": "",
    "rfloor": "",
    "lceil": "",
    "rceil": "",
    "to": " to ",
    "infty": " infinity",
}

DISPLAY_SYMBOL = {
    "cdot": "·",
    "times": "×",
    "oplus": "⊕",
    "sigma": "σ",
    "leq": "≤",
    "le": "≤",
    "geq": "≥",
    "ge": "≥",
    "neq": "≠",
    "ne": "≠",
    "approx": "≈",
    "in": "∈",
    "cup": "∪",
    "cap": "∩",
    "setminus": "∖",
    "sum": "Σ",
    "infty": "∞",
    "quad": " ",
    "qquad": " ",
    ",": "",
    ";": "",
    "!": "",
    "left": "",
    "right": "",
    "lfloor": "⌊",
    "rfloor": "⌋",
    "lceil": "⌈",
    "rceil": "⌉",
    "to": "→",
    "log": "log",
}


def _parse_latex(src: str, speech: bool) -> str:
    i = 0
    n = len(src)

    def peek() -> str:
        return src[i] if i < n else ""

    def parse_group() -> str:
        nonlocal i
        if peek() != "{":
            return parse_atom()
        i += 1
        parts: list[str] = []
        while i < n and peek() != "}":
            parts.append(parse_piece())
        if peek() == "}":
            i += 1
        return "".join(parts)

    def parse_script() -> str:
        nonlocal i
        if peek() == "{":
            return parse_group()
        if i < n:
            ch = src[i]
            i += 1
            return ch
        return ""

    def apply_scripts(base: str) -> str:
        nonlocal i
        while True:
            if peek() == "_":
                i += 1
                sub = parse_script()
                if speech:
                    base += " " + sub
                else:
                    base += sub if len(sub) == 1 and sub.isdigit() else "_" + sub
            elif peek() == "^":
                i += 1
                sup = parse_script()
                if speech and sup.strip() == "2":
                    base += " squared"
                elif speech:
                    base += " to the power " + sup
                elif sup.strip() == "2":
                    base += "²"
                elif sup.strip() == "3":
                    base += "³"
                else:
                    base += "^" + sup
            else:
                break
        return base

    def parse_atom() -> str:
        nonlocal i
        if i >= n:
            return ""
        ch = peek()
        if ch == "\\":
            i += 1
            cmd = []
            if i < n and src[i].isalpha():
                while i < n and src[i].isalpha():
                    cmd.append(src[i])
                    i += 1
            elif i < n:
                cmd.append(src[i])
                i += 1
            name = "".join(cmd)
            if name in ("text", "mathrm", "mathbf", "operatorname"):
                return apply_scripts(parse_group())
            if name == "overline":
                inner = parse_group()
                phrase = f"the opposite of {inner}" if speech else f"not ({inner})"
                return apply_scripts(phrase)
            if name == "bar":
                inner = parse_group()
                if speech:
                    return apply_scripts(inner + " bar")
                if len(inner) == 1:
                    return apply_scripts(inner + "\u0304")
                return apply_scripts(inner + " bar")
            if name == "sqrt":
                inner = parse_group()
                body = f"square root of {inner}" if speech else f"√({inner})"
                return apply_scripts(body)
            if name == "frac":
                a = parse_group()
                b = parse_group()
                body = f"{a} over {b}" if speech else f"({a})/({b})"
                return apply_scripts(body)
            if name == "log":
                base = ""
                if peek() == "_":
                    i += 1
                    base = parse_script().strip()
                if speech and base:
                    return f" log base {base} of"
                if base:
                    return f"log_{base}"
                return " log" if speech else "log"
            if name == "sum":
                lower = ""
                upper = ""
                if peek() == "_":
                    i += 1
                    lower = parse_script().strip()
                if peek() == "^":
                    i += 1
                    upper = parse_script().strip()
                if speech and (lower or upper):
                    return f" sum from {lower} to {upper} of"
                if lower or upper:
                    return f"Σ from {lower} to {upper}"
                return " sum" if speech else "Σ"
            table = SPEECH_SYMBOL if speech else DISPLAY_SYMBOL
            if name in table:
                return apply_scripts(table[name])
            return apply_scripts(name)

        if ch in "{":
            return apply_scripts(parse_group())
        if ch == "}":
            return ""
        i += 1
        if ch.isspace():
            return " "
        return apply_scripts(ch)

    def parse_piece() -> str:
        return parse_atom()

    parts: list[str] = []
    while i < n:
        parts.append(parse_piece())
    text = "".join(parts)
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\s+([,.;:])", r"\1", text)
    if speech:
        text = re.sub(r"\bO\(([^)]+)\)", r"big O of \1", text)
    return text.strip()


def render_math(text: str, speech: bool) -> str:
    def sub(match: re.Match[str]) -> str:
        return _parse_latex(match.group(1), speech)

    text = re.sub(r"\\\((.+?)\\\)", sub, text, flags=re.S)
    text = re.sub(r"\\\[(.+?)\\\]", sub, text, flags=re.S)
    text = text.replace("\u00a0", " ")
    text = re.sub(r"[ \t]+\n", "\n", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = re.sub(r"[ \t]{2,}", " ", text)
    return text.strip()


def code_speech(text: str) -> str:
    spoken = text
    replacements = [
        (">=", " greater than or equal to "),
        ("<=", " less than or equal to "),
        ("!=", " not equal "),
        ("==", " equals "),
        ("->", " arrow "),
        ("=", " equals "),
        ("#", " comment "),
    ]
    for old, new in replacements:
        spoken = spoken.replace(old, new)
    lines = [ln.strip() for ln in spoken.splitlines() if ln.strip()]
    return "Code. " + " ".join(lines)


def classes(el: Tag) -> set[str]:
    raw = el.get("class") or []
    return set(raw)


def plain(el: Tag) -> str:
    return el.get_text(" ", strip=True)


def block(kind: str, display: str, speech: str | None = None) -> dict | None:
    display = re.sub(r"\n{3,}", "\n\n", display).strip()
    speech = (speech if speech is not None else display).strip()
    speech = re.sub(r"\s+", " ", speech)
    if not display and not speech:
        return None
    return {"kind": kind, "display": display, "speech": speech}


def push(out: list[dict], item: dict | None, node) -> None:
    if not item:
        return
    index = str(len(out))
    if isinstance(node, Tag):
        node["data-b"] = index
    elif isinstance(node, NavigableString) and isinstance(node.parent, Tag):
        span = node.parent.new_tag("span")
        span["data-b"] = index
        span["class"] = "math-line"
        node.wrap(span)
    out.append(item)


def emit_node(node, out: list[dict]) -> None:
    if isinstance(node, NavigableString):
        raw = str(node).strip()
        if "\\(" in raw or "\\[" in raw:
            push(out, block("p", render_math(raw, False), render_math(raw, True)), node)
        return
    if isinstance(node, Tag):
        emit_element(node, out)


def emit_element(el: Tag, out: list[dict]) -> None:
    name = el.name
    cls = classes(el)
    if name in ("script", "style", "svg"):
        return
    if name == "figure":
        cap = el.find(class_="figcap")
        if cap:
            text = render_math(plain(cap), False)
            speech = render_math(plain(cap), True)
            push(out, block("caption", text, speech), el)
        return
    if "say" in cls:
        label = el.find("b")
        body = el.find("span")
        label_text = plain(label) if label else "Note"
        body_text = plain(body) if body else plain(el)
        display = render_math(f"{label_text}. {body_text}", False)
        speech = render_math(f"{label_text}. {body_text}", True)
        push(out, block("note", display, speech), el)
        return
    if "note" in cls:
        display = render_math(plain(el), False)
        speech = render_math(plain(el), True)
        push(out, block("note", display, speech), el)
        return
    if name == "div" and "tag" in cls:
        display = render_math(plain(el), False)
        push(out, block("h", display, render_math(plain(el), True)), el)
        return
    if "step" in cls:
        display = render_math(plain(el), False)
        push(out, block("item", display, render_math(plain(el), True)), el)
        return
    if name in ("h2", "h3", "h4"):
        display = render_math(plain(el), False)
        push(out, block("h", display, render_math(plain(el), True)), el)
        return
    if name == "p":
        display = render_math(plain(el), False)
        push(out, block("p", display, render_math(plain(el), True)), el)
        return
    if name == "pre":
        raw = el.get_text("\n", strip=False).strip("\n")
        push(out, block("code", raw, code_speech(raw)), el)
        return
    if name == "table":
        rows_d = []
        rows_s = []
        for tr in el.find_all("tr"):
            cells = [render_math(c.get_text(" ", strip=True), False) for c in tr.find_all(["th", "td"])]
            cells_s = [render_math(c.get_text(" ", strip=True), True) for c in tr.find_all(["th", "td"])]
            if any(cells):
                rows_d.append(" · ".join(cells))
                rows_s.append(". ".join(cells_s))
        push(out, block("p", "\n".join(rows_d), " ".join(rows_s)), el)
        return
    if name in ("ul", "ol"):
        for li in el.find_all("li", recursive=False):
            display = render_math(plain(li), False)
            speech = render_math(plain(li), True)
            push(out, block("item", display, speech), li)
        return
    for child in list(el.children):
        emit_node(child, out)


def lecture_from(section: Tag) -> dict:
    kicker = plain(section.select_one(".kicker")) if section.select_one(".kicker") else ""
    title_el = section.find("h2")
    title = plain(title_el) if title_el else "Lecture"
    deck_el = section.select_one(".deck")
    deck = render_math(plain(deck_el), False) if deck_el else ""
    deck_speech = render_math(plain(deck_el), True) if deck_el else ""
    blocks: list[dict] = []
    if deck:
        item = block("p", deck, deck_speech)
        if item:
            if deck_el is not None:
                deck_el["data-b"] = "0"
            blocks.append(item)
    for child in list(section.children):
        if isinstance(child, Tag) and child.name == "header":
            continue
        emit_node(child, blocks)
    return {
        "id": section.get("id") or title.lower().replace(" ", "-"),
        "kicker": kicker,
        "title": title,
        "deck": deck,
        "blocks": blocks,
    }


def main() -> None:
    soup = BeautifulSoup(HTML.read_text(encoding="utf-8"), "html.parser")
    lectures = [lecture_from(section) for section in soup.select("section.lecture")]
    payload = {
        "title": "Computer Science Lecture Notes",
        "voice": "Piper Amy, int8, embedded offline",
        "lectures": lectures,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=1), encoding="utf-8")
    OUT_HTML.parent.mkdir(parents=True, exist_ok=True)
    OUT_HTML.write_text(str(soup), encoding="utf-8")
    words = sum(len(b["speech"].split()) for lec in lectures for b in lec["blocks"])
    print(f"wrote {OUT} lectures={len(lectures)} blocks={sum(len(l['blocks']) for l in lectures)} words={words}")


if __name__ == "__main__":
    samples = [
        r"\(Y = A \cdot B\)",
        r"\(Y=\overline{A\cdot B}\)",
        r"\[ \text{rows} = 2^{n}. \]",
        r"\[ Y = (D + W)\cdot N \]",
        r"\[ \text{steps} \approx \lfloor \log_{2} n \rfloor + 1. \]",
        r"\(O(n^{2})\)",
        r"\(\bar{x} = \frac{1}{n}\sum_{i=1}^{n} x_i\)",
        r"\(z = \sum_{i=1}^{n} w_i x_i + b\)",
        r"\(A \cup B\)",
    ]
    for sample in samples:
        print("D", render_math(sample, False))
        print("S", render_math(sample, True))
    main()
