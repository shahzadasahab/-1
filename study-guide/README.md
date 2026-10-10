# Class XI Computer Science — Teach Yourself Study Guide

Original self-study companion for the Sindh Textbook Board Class XI Computer Science syllabus (Units 1–6).

This is teaching material written from the syllabus, not a reprint of the textbook.

## The PDF (MathJax + SVG edition)

[Class_XI_Computer_Science_Teach_Yourself_Study_Guide.pdf](Class_XI_Computer_Science_Teach_Yourself_Study_Guide.pdf)

Formulae are typeset with **MathJax 3** (TeX → SVG). Circuits, K-maps, OSI/TCP-IP stacks, sort/search traces, ER diagrams, and IoT loops are **inline SVG**. Chrome prints the HTML after MathJax marks the page ready.

Covers:

1. Computer Systems — digital logic, Boolean algebra, gates, K-maps, SDLC, OSI/TCP-IP
2. Computational Thinking and Algorithms — decomposition, Bubble/Selection sort, Linear/Binary search
3. Programming Fundamentals — Python, operators, control, libraries, debugging
4. Data and Analysis — ER models, keys, Access tables/forms/queries
5. Applications and Impacts — AI, IoT, information sources, assistive tech
6. Digital Literacy — search, data collection, artefacts

Plus Al-Noor case studies, unit studios, a 40-mark rehearsal paper, recitation cards, and an eight-week plan.

Browse the source as [web/index.html](web/index.html) (needs the vendored `web/vendor/tex-svg.js`).

## Regenerate

```bash
cd study-guide
python3 generate_web.py   # rebuild web/index.html
python3 print_pdf.py      # Chrome headless → A4 PDF after MathJax
```

Requires Python 3, Google Chrome, and `websocket-client` (`pip install websocket-client`). The older ReportLab builder (`generate_guide.py`) is kept for the text-only edition.
