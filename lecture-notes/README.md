# IT Lecture Notes (Draft)

Condensed lecture notes for **Class XI** and **Class XII** Information Technology, derived from the uploaded curriculum PDFs in this workspace.

## Features

- **Flexbox** layout (`css/lecture.css`) for side-by-side text + diagrams
- **Embedded SVG** diagrams under `diagrams/`
- **MathJax** (TeX → SVG) for Boolean algebra and complexity notation
- **PDF export** via headless Chromium (Puppeteer)

## Build PDFs

```bash
cd lecture-notes
npm install
npm run build:pdf
```

Output files:

- `output/IT-Lecture-Notes-Class-XI.pdf`
- `output/IT-Lecture-Notes-Class-XII.pdf`
- `output/IT-Lecture-Notes-Complete.pdf` (cover / bundle info)

## Source text

Raw text extracted from uploaded PDFs (for authoring reference only):

`source-text/*.txt`

## Preview in browser

Open `class-xi-lecture-notes.html` or `class-xii-lecture-notes.html` locally; allow MathJax CDN if offline typesetting is required, use `npm run build:pdf` on a networked machine.
