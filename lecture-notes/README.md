# Teach Yourself Lecture Notes — Intermediate Computer Science

Self-study booklets for **Class XI and Class XII** Computer Science. Each unit is an HTML lecture you can open in a browser and a matching **A4 PDF**.

Layout is **Flexbox**. Diagrams are **inline SVG**. Mathematics is **MathJax 3** (SVG output, vendored under `assets/mathjax`).

## Booklets

| PDF | Unit |
|-----|------|
| `pdf/00-course-map.pdf` | Course map and study rhythm |
| `pdf/XI-01-computer-systems.pdf` | Digital logic, LogiSim, SDLC, OSI / TCP/IP |
| `pdf/XI-02-computational-thinking.pdf` | Algorithms, bubble / selection, linear / binary |
| `pdf/XI-03-programming-fundamentals.pdf` | Python basics and control flow |
| `pdf/XI-04-data-and-analysis.pdf` | Databases, ER, MS Access objects |
| `pdf/XI-05-applications-impacts.pdf` | AI, IoT, sources, impacts |
| `pdf/XI-06-digital-literacy.pdf` | Research methods and presentation |
| `pdf/XII-01-human-computer-interaction.pdf` | HCI, accessibility, Figma, evaluation |
| `pdf/XII-02-algorithms-data-structures.pdf` | Trace tables, Big-O, stack / queue / tree / graph |
| `pdf/XII-03-python-structures-functions-files.pdf` | Collections, functions, files |
| `pdf/XII-04-python-data-analysis.pdf` | sqlite3, pandas, matplotlib, statistics |
| `pdf/XII-05-neural-nets-security.pdf` | Neural nets, threats, equity |
| `pdf/XII-06-digital-entrepreneurship.pdf` | Prototype, MVP, beachhead market |

## 30-day crash course

Two coaching booklets, one class each. Every day is a 120-minute session: recall, board notes, a worked example, a silent drill with a model answer, and homework. Checkpoints are closed-book. Each booklet ends with a mock and a mark scheme.

| PDF | Pages | Use |
|-----|-------|-----|
| `pdf/XI-30-day-crash.pdf` | 63 | Class XI, Days 1–30 |
| `pdf/XII-30-day-crash.pdf` | 64 | Class XII, Days 1–30 |

Rebuild the HTML, then the PDFs:

```bash
cd lecture-notes
python3 scripts/build_crash_course.py
npm run pdf
```

## Rebuild the PDFs

```bash
cd lecture-notes
npm install
npm run pdf
```

Requires Google Chrome (or set `CHROME_PATH`). The renderer waits for MathJax to finish typesetting before printing.

Open any file in `html/` in a browser if you want live MathJax and reflow.
