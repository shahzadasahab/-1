# Class XI Computer Science — Study Guides

Original self-study companions for the Sindh Textbook Board Class XI / Intermediate Computer Science syllabus (Units 1–6). Teaching material written from the syllabus, not a reprint of the textbook.

Formulae are typeset with **MathJax 3**. Circuits, K-maps, OSI/TCP-IP stacks, sort traces, ER diagrams, and IoT loops are **inline SVG**. Chrome prints A4 after MathJax marks the page ready.

## Lecture-wise Intermediate edition (recommended)

[Class_XI_Computer_Science_Lecture_Wise_Study_Guide.pdf](Class_XI_Computer_Science_Lecture_Wise_Study_Guide.pdf)

Twenty-five college sittings (L01–L25). Each lecture has outcomes, taught content, a board example, an exit ticket, and a 15-minute homework.

| Block | Lectures | Syllabus |
| --- | --- | --- |
| A Computer Systems | L01–L08 | Analog/digital, Boolean, gates, SOP, K-maps, SDLC, Al-Noor, OSI/TCP-IP |
| B Algorithms | L09–L12 | CT, Bubble Sort, Selection Sort, linear/binary search |
| C Python | L13–L17 | IDE, operators, if, loops, libraries, ATM |
| D Data | L18–L21 | Keys, ER, integrity, Access queries |
| E Society | L22–L24 | IoT/AI, sources, digital literacy |
| Revision | L25 | Cards, burglar alarm, 40-mark paper |

Source: [web/lectures.html](web/lectures.html).

```bash
cd study-guide
python3 generate_lectures.py
python3 print_pdf.py web/lectures.html Class_XI_Computer_Science_Lecture_Wise_Study_Guide.pdf
```

## Unit-wise edition

[Class_XI_Computer_Science_Teach_Yourself_Study_Guide.pdf](Class_XI_Computer_Science_Teach_Yourself_Study_Guide.pdf) — the same syllabus organised by unit rather than by sitting.

```bash
python3 generate_web.py
python3 print_pdf.py
```

Requires Python 3, Google Chrome, and `websocket-client`. The older ReportLab builder (`generate_guide.py`) is kept for the text-only unit edition.
