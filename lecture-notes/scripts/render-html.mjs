import { renderDiagram } from "../assets/diagrams.mjs";

const MATHJAX = `<script>
window.MathJax = {
  tex: {
    inlineMath: [['$', '$'], ['\\\\(', '\\\\)']],
    displayMath: [['$$', '$$'], ['\\\\[', '\\\\]']],
    processEscapes: true
  },
  startup: { typeset: false }
};
</script>
<script src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-chtml.js" async></script>`;

function callout(type, title, body) {
  const cls =
    type === "remember"
      ? "callout-remember"
      : type === "try"
        ? "callout-try"
        : "callout-exam";
  return `<div class="callout ${cls}"><div><strong>${title}</strong>${body}</div></div>`;
}

function sectionBlock(sec) {
  const diagram =
    sec.diagram != null
      ? `<div class="diagram-wrap">${renderDiagram(sec.diagram)}<div class="diagram-caption">${sec.diagramCaption ?? ""}</div></div>`
      : "";
  return `<section class="section">
    <h2>${sec.title}</h2>
    ${sec.html ?? ""}
    ${diagram}
  </section>`;
}

export function renderChapter(ch) {
  const gradeClass = ch.grade === "XI" ? "badge-xi" : "badge-xii";
  const outcomes = ch.outcomes
    .map((o) => `<li>${o}</li>`)
    .join("");
  const sections = ch.sections.map(sectionBlock).join("\n");
  const practice =
    ch.practice?.length > 0
      ? `<section class="section page-break"><h2>Teach Yourself — Practice &amp; Check</h2><ol>${ch.practice.map((p) => `<li>${p}</li>`).join("")}</ol></section>`
      : "";

  return `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8"/>
  <title>${ch.title} — Teach Yourself Lecture Notes</title>
  <link rel="stylesheet" href="../../assets/styles.css"/>
  ${MATHJAX}
</head>
<body>
  <header class="cover">
    <div class="cover-row">
      <div>
        <span class="badge badge-ty">Teach Yourself</span>
        <span class="badge ${gradeClass}">Intermediate ${ch.grade}</span>
        <span class="badge">Unit ${ch.unit}</span>
        <h1>${ch.title}</h1>
        <p class="subtitle">${ch.tagline ?? "Lecture notes for Intermediate Computer Science students"}</p>
      </div>
    </div>
    <div class="flex-grid">
      <div class="card">
        <h3>What you will master</h3>
        <ul>${outcomes}</ul>
      </div>
      <div class="card">
        <h3>How to use these notes</h3>
        <ul>
          <li>Read one section, then close the book and explain it aloud.</li>
          <li>Do every <em>Try it</em> box before moving on.</li>
          <li>Memorize tables and truth patterns — exams love them.</li>
        </ul>
      </div>
    </div>
  </header>
  ${sections}
  ${practice}
  <footer class="page-foot">
    <span>Intermediate CS · Unit ${ch.unit} · ${ch.grade}</span>
    <span>Teach Yourself Lecture Notes</span>
  </footer>
</body>
</html>`;
}
