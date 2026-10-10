#!/usr/bin/env python3
"""Build the lecture-wise Intermediate (Class XI) study guide as HTML."""

from __future__ import annotations

from pathlib import Path

from lectures.block_algo import lectures as algo
from lectures.block_data import lectures as data
from lectures.block_python import lectures as python
from lectures.block_society import lectures as society
from lectures.block_systems import lectures as systems
from lectures.kit import box, css, mathjax, table

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "web" / "lectures.html"

TOC = [
    ("L01", "Stairs and ramps — analog versus digital", "1"),
    ("L02", "Boolean algebra — arithmetic with truth", "1"),
    ("L03", "The seven logic gates", "1"),
    ("L04", "Truth tables, SOP, and logic diagrams", "1"),
    ("L05", "Karnaugh maps — grouping the ones", "1"),
    ("L06", "Software Development Life Cycle", "1"),
    ("L07", "Waterfall versus Agile — Al-Noor cases", "1"),
    ("L08", "How machines converse — OSI and TCP/IP", "1"),
    ("L09", "Think so a machine can follow you", "2"),
    ("L10", "Bubble Sort — neighbours swap", "2"),
    ("L11", "Selection Sort — park the minimum", "2"),
    ("L12", "Linear search and binary search", "2"),
    ("L13", "Python, the IDE, and input() is a string", "3"),
    ("L14", "Operators — including the bitwise family", "3"),
    ("L15", "Selection — if, elif, else", "3"),
    ("L16", "Repetition — for, while, break, continue", "3"),
    ("L17", "Libraries, errors, and the ATM studio", "3"),
    ("L18", "Data, DBMS, and the four keys", "4"),
    ("L19", "ER models and the three cardinalities", "4"),
    ("L20", "Referential integrity and Access objects", "4"),
    ("L21", "Queries, totals, and charts", "4"),
    ("L22", "IoT collects, analytics explains, AI decides", "5"),
    ("L23", "Sources, impacts, and assistive technology", "5"),
    ("L24", "Digital literacy — find, judge, collect, show", "6"),
    ("L25", "Revision sitting — cards, alarm, 40-mark paper", "Rev"),
]


def front() -> str:
    rows = [[a, b, "Unit " + c if c != "Rev" else "Revision"] for a, b, c in TOC]
    return (
        "<h1>How to use this lecture edition</h1>"
        '<p class="lead">Written for Intermediate / HSC Class XI students following the '
        "Sindh Textbook Board Computer Science syllabus. Each sitting is one college "
        "lecture: outcomes, taught content, a board example, an exit ticket, and a "
        "15-minute homework. Formulae are MathJax; diagrams are SVG. This is a companion, "
        "not a reprint — keep your textbook for official figures and LogiSim screenshots.</p>"
        + box(
            "",
            "THE FIVE-PASS METHOD",
            "<ol class=\"tight\">"
            "<li><strong>Read for the map</strong> — the outcomes box, two minutes.</li>"
            "<li><strong>Read for the mechanism</strong> — cover a worked line and try it first.</li>"
            "<li><strong>Exit ticket</strong> is a mini exam; write on paper.</li>"
            "<li><strong>Recite</strong> the lecture’s one list (gates, CAPP, OSI, keys…).</li>"
            "<li><strong>Homework tonight, review next week.</strong></li>"
            "</ol>",
        )
        + "<h2>Twenty-five sittings · eight college weeks</h2>"
        + table(["Week", "Lectures", "Must-finish artefact"], [
            ["1", "L01–L03", "LogiSim AND + the seven-gate table from memory"],
            ["2", "L04–L06", "One SOP table and the SDLC list closed-book"],
            ["3", "L07–L09", "Waterfall vs Agile from memory; CT strategies"],
            ["4", "L10–L12", "Two sort traces and one binary-search diary"],
            ["5", "L13–L15", "Calculator + even/odd running in VS Code"],
            ["6", "L16–L18", "ATM or guess game; four keys recited"],
            ["7", "L19–L21", "One ER + one grouped query on paper"],
            ["8", "L22–L25", "Irrigation paragraph + 40-mark rehearsal"],
        ])
        + "<h2>Lecture register</h2>"
        + table(["No.", "Title", "Syllabus"], rows)
        + box(
            "exam",
            "WHAT “DONE” LOOKS LIKE",
            "You can teach the lecture’s core idea to a classmate in three minutes. "
            "You have hand-traced the board example. You scored the exit ticket closed-book "
            "and corrected every miss in writing.",
        )
    )


def html() -> str:
    return (
        "<!DOCTYPE html>\n<html lang=\"en\">\n<head>\n"
        "<meta charset=\"utf-8\"/>\n"
        "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\"/>\n"
        "<title>Class XI Computer Science — Lecture-wise Intermediate Edition</title>\n"
        "<style>" + css() + "</style>\n"
        + mathjax() + "\n</head>\n<body>\n"
        '<section class="cover"><div class="cover-inner">\n'
        '<div class="kicker">SINDH · INTERMEDIATE / CLASS XI · COMPUTER SCIENCE</div>\n'
        "<h1>Lecture-wise<br/>Study Guide</h1>\n"
        "<p>Twenty-five college sittings with outcomes, board work, exit tickets, "
        "and homework. MathJax notation and SVG diagrams for Digital Logic, SDLC, "
        "Networks, Algorithms, Python, Databases, IoT &amp; AI, and Digital Literacy.</p>\n"
        '<p class="kicker">One lecture · One artefact · One recitation</p>\n'
        "</div></section>\n"
        '<header class="bar"><span>Class XI Computer Science · Lecture-wise Intermediate Edition</span>'
        "<span>MathJax + SVG · 25 sittings</span></header>\n<main>\n"
        + front()
        + systems() + algo() + python() + data() + society()
        + '<p class="lead">If you have worked the amber boxes twice, you are the teacher '
        "you were waiting for. Take Lecture 25 again in a month.</p>\n"
        "</main>\n</body>\n</html>\n"
    )


def main() -> None:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(html(), encoding="utf-8")
    print("Wrote", OUT, "(", OUT.stat().st_size, "bytes)")


if __name__ == "__main__":
    main()
