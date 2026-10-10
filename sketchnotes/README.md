# CS XI & XII Complete Sketchnotes

Hand-drawn-style **sketchnote PDFs** of the Sindh Curriculum Computer Science teacher lecture notes (Chapters 1–6 for each class). Every definition, comparison table, algorithm, worked example, case study, golden topic, career note and chapter summary from the source is kept.

## Generated PDFs

| File | Contents |
| --- | --- |
| [`output/CS_XI_Complete_Sketchnotes.pdf`](output/CS_XI_Complete_Sketchnotes.pdf) | Class XI — Computer Systems, Algorithms, Python, Databases / Access, Impacts (AI/IoT), Digital Literacy |
| [`output/CS_XII_Complete_Sketchnotes.pdf`](output/CS_XII_Complete_Sketchnotes.pdf) | Class XII — HCI, Data Structures & Big O, Python structures/files, Pandas/stats, ML & security, Digital entrepreneurship |

★ **Golden Topics** are exam-critical and marked with a star plus a gold chip.

## Rebuild

```bash
cd sketchnotes
python3 -m pip install reportlab
python3 build.py
```

Requires the TTF files in `fonts/` (SIL Open Font License: Amatic SC, Kalam, Patrick Hand, Architects Daughter, Indie Flower, Handlee).

## Source

Bilingual Teacher’s Edition lecture notes, New Sindh Curriculum 2026 (XI) and 2024 / 2025–27 (XII). English exam content is complete; Urdu in the source is the parallel teacher translation.
