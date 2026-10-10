# Lecture authoring spec (Urdish + MathJax + SVG)

Each chapter file pair is authored independently:

* `app/src/main/assets/web/js/data/<key>.js` – lectures (`Lectures.add({...})`)
* `app/src/main/assets/web/js/diagrams/<key>.js` – SVG diagrams (`Diagrams.register(id, fn)`)

Keys: `xi-1a xi-1b xi-2 xi-3 xi-4 xi-5 xi-6 xii-1 xii-2 xii-3 xii-4 xii-5 xii-6`.
**Gold-standard example: `data/xi-1a.js` (lecture `xi-1-01`) and `diagrams/xi-1a.js`. Match its depth, voice and structure.**

## 1. What "Urdish" means here

* The teacher explains in **Urdu script** (descriptive: why, how, example, analogy).
* **Technical terms stay in English (Latin script)**: Algorithm, Variable, Loop, Primary Key, Router ...
  Never transliterate a term into Urdu script (`ایلگورتھم` is wrong, `Algorithm` is right).
  Give the Urdu meaning once in the sentence that introduces it, or in a `terms` block.
* Tone: a friendly class teacher. Use *بچو، دیکھیں، ذرا سوچیں، یاد رکھیں، آئیے*. Use Pakistani everyday examples
  (chai wala, rickshaw, cricket scoreboard, WhatsApp, JazzCash/Easypaisa, Daraz, school attendance, NADRA, bus stops, load shedding).
* **Display vs speech:** `title`, `leadEn`, `en`, `enTitle` and recap `{en}` are **English-only display**. The teacher’s spoken explanation is always the Urdish `ur` / `say`. Never transliterate English terms into Urdu script.
* Text in `ur`/`say` is both displayed AND spoken by TTS, so write sentences that sound natural when read aloud.
  - Short sentences, end every sentence with `۔` or `؟`.
  - **Write numbers in narration as Urdu words** (ایک، دو، تین ...) when they are small counts. Digits are fine inside English terms,
    code, tables and formulas (`say` strings of math/code/table blocks should speak numbers in words).
  - No emoji. No long runs of symbols. Avoid parentheses with long English phrases in the middle of Urdu sentences.
  - Do not put the same sentence in `ur` and `say`; `say` is for blocks whose visible content is not plain text.
* Be faithful to the textbook (definitions, tables, steps, examples, SLOs). Teach EVERYTHING in the assigned PDFs, lecture by lecture.
  You may add teacher analogies, but never contradict the book. Fix OCR noise by reading the page image if needed (see §7).

## 2. Lecture object

```js
Lectures.add({
  id: 'xi-2-03',            // class (xi|xii) - chapter - two digit lecture number inside the chapter
  cls: 'XI', ch: 2, n: 3,   // must agree with id
  title: 'Sorting Algorithms',            // English title (Latin)
  titleUr: 'سورٹنگ الگورتھمز',               // Urdu title (Urdu script, Latin terms allowed)
  leadEn: 'English overview of the lecture (display only, never spoken).',
  mins: 9,                  // estimated minutes (narration ~ 110 words/min)
  source: 'Unit 2 · §2.4.1',              // where in the book
  keywords: ['bubble', 'sort'],            // search words
  objectives: ['...', '...'],              // 2-4 Urdish lines (inline markup allowed)
  blocks: [ ... ],                         // 12-24 blocks, see §3
  quiz: [{ q, en?, opts:[..3-4..], a: 1, why, whyEn? }],
  homework: ['...' | {en, ur}],            // 1-3 tasks
});
```

Lecture size target: **6-12 minutes = 700-1400 spoken words**, 12-24 blocks, at least 1-2 diagrams
(more for visual topics), formulas with MathJax where the chapter has any (Boolean, Big-O, statistics, probability, formulas).
Split a chapter into lectures at natural teaching boundaries (one concept cluster per lecture, usually one per textbook sub-section group).
Number lectures sequentially within the chapter starting at the number assigned to you.

Flow of a good lecture: greeting/hook (first lecture of a chapter: greeting; later ones: quick recall of previous lecture) ->
objectives are shown automatically -> concept blocks with diagram/table/example -> `note` blocks (exam tip/warning) ->
`terms` -> `recap` (board summary, 3-6 lines) -> quiz -> homework.

## 3. Block types

Inline markup inside any text string: `**bold term**`, `` `inline code` ``, `$tex$` (inline MathJax, e.g. `$A \cdot B$`).

| block | fields | spoken text |
|---|---|---|
| `{t:'h', ur, en?}` | section heading. `en` is English-only display; TTS still reads `ur` | `ur` |
| `{t:'say', ur, en?}` | teacher paragraph (2-5 sentences). Optional `en` is the English idea the student reads first | `ur` |
| `{t:'points', title?, items[], ordered?}` | bullet list | title + each item |
| `{t:'recap', items[]}` | "Board summary" at end | each item |
| `{t:'steps', title?, items[]}` | numbered steps (algorithm, procedure) | each item |
| `{t:'math', tex, cap?, say}` | display MathJax equation. `tex` is TeX WITHOUT `$`. **Provide `say`** (how the teacher reads it) | `say` |
| `{t:'diagram', id, args?, cap?, say}` | registered SVG diagram | `say` (REQUIRED) |
| `{t:'dgrow', items:[{id,args,cap}], say}` | 2-3 small diagrams side by side (flex row) | `say` |
| `{t:'svg', svg, cap?, say}` | inline one-off `<svg>` string | `say` |
| `{t:'table', title?, head[], rows[][], say}` | flex table; cells accept inline markup | `say` (REQUIRED) |
| `{t:'compare', left:{title,items[]}, right:{title,items[]}, say}` | two-column comparison | `say` (REQUIRED) |
| `{t:'terms', items:[{en, ur}]}` | key-term chips | "en یعنی ur" for each |
| `{t:'code', lang:'python'|'sql', code, out?, say}` | code listing with optional output | `say` (REQUIRED) |
| `{t:'note', kind:'tip'|'warn'|'exam'|'example'|'def', ur}` | coloured callout | `ur` |

Math rules (MathJax 3, TeX): `\overline{A}`, `A \cdot B`, `A + B`, `A \oplus B`, `O(n^2)`, `\frac{a}{b}`, `\sum`, `\sqrt{}`, `\bar{x}`.
Use `\text{...}` for words inside formulas. Macros available: `\XOR` (=\oplus), `\NOT{A}` (=\overline{A}). In JS strings escape backslashes (`'\\overline{A}'`).
Everything is checked with the real MathJax by the validator; an unknown command fails the build.

Code blocks: real, correct, runnable code that appears in the book (or a faithful simplification). `out` is the exact expected output.

## 4. SVG diagrams

Diagram file skeleton:

```js
(function () {
  Diagrams.register('xi2.bubble-sort', (args) => {
    let s = '';
    s += K.box(10, 10, 60, 40, '5', { c: 0 });
    s += K.arrow ... (use K.line(x1,y1,x2,y2,{arrow:true}))
    return K.svg(440, 200, s, { title: 'Bubble sort pass 1' });   // title = accessible description
  });
})();
```

* **Id prefix** = your key without dashes, then a dot: `xi2.` , `xii3.` , `xi1b.` ... Ids must be globally unique.
* Read `js/kit.js` for the helpers: `K.svg K.rect K.box K.text K.line K.path K.poly K.polyline K.circle K.ellipse K.dot K.gate K.grid K.g`.
  Colour with classes only (never hex): fills `c:0..7` (0 teal,1 blue,2 violet,3 rose,4 amber,5 green,6 grey,7 orange),
  strokes `s:'s-acc|s-red|s-grn|s-mut|s-brand'`, text `cls:'t-mut|t-acc|t-red|t-grn|t-wht'`, fills `f-acc|f-brand|f-red|f-grn|f-ink`.
  This keeps diagrams correct in dark mode.
* **viewBox width <= 480** (phones are ~360 CSS px wide; text must stay >= 11 px after scaling). Height as needed (typically 120-340).
  Font sizes inside the viewBox: 12-15 body, 11 minimum.
* Label diagrams in English (Latin) terms; short Urdu words are allowed in `K.text` (it supports Urdu script) but keep them minimal.
* Make diagrams *explain*: arrows for flow, colours for roles, numbered steps, labelled parts, a worked example with real values.
  Simple geometric accuracy matters (aligned arrows, labels not overlapping, nothing clipped).
* Parameterise when useful (`args`) – e.g. one `xi1a.gate` diagram per gate type. Every diagram must also render with `args = {}`.
* For logic circuits use `K.gate(type, x, y)` which returns `{svg, a, b, q}` pin coordinates; connect with `K.wire([...])`.
* Aim for roughly one diagram per 1-2 concept blocks; visual topics (networking, algorithms, ER, data structures) deserve more.
* Mathematical formulas in diagrams are text only; put real formulas in `math` blocks.

## 5. Quality bar / checklist (the validator enforces most)

* `node tools/validate.js <your-key>` passes with 0 errors (warnings: fix unless justified).
* `node tools/sheet.js <key> /tmp/<key>.png 2 900` (renders every diagram in `diagrams/<key>.js`) and LOOK at the picture (use the Read tool on the png): no overlapping text, clipped shapes,
  wrong arrows, tiny text. Fix and re-render until clean.
* Optional: `NODE_PATH=tools/node_modules node tools/shot.js "#lec=<id>" /tmp/x.png 390 800 scroll:0` screenshots the lecture as it will look on a phone (use `scroll:N` to page down).
* Facts must match the book. Do not invent definitions, numbers or examples that conflict with it.
* Do not edit any file other than your own two files. Do not touch other agents' files, `app.js`, `kit.js` or CSS. If you need a kit helper that does not exist, write it locally inside your diagram file.

## 6. Narration quality

Read each `say`/`ur` aloud in your head as a teacher in class: natural Urdu grammar, no word-for-word translation of English sentences,
consistent English terminology, one idea per sentence, no sentence over ~35 words. Use examples before formal definitions when it helps,
then give the book's formal definition so students can write it in exams (`note` kind `def` / `exam`).

## 7. Reading the source

OCR text of every PDF is in `/tmp/txt/<name>.txt` (page markers `=====PAGE n=====`). It is noisy (figures, tables garbled).
When a figure/table/code listing is unclear, render the page to an image and read it:

```bash
python3 -c "import pymupdf;d=pymupdf.open('/home/ubuntu/.cursor/projects/workspace/uploads/<file>.pdf');d[PAGE-1].get_pixmap(dpi=90).save('/tmp/p.png')"
```
then open `/tmp/p.png` with the Read tool.
