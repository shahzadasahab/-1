"""HTML helpers for the lecture-wise Intermediate edition."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WEB = ROOT / "web"


def css() -> str:
    return (WEB / "guide.css").read_text(encoding="utf-8")


def fig(svg: str, caption: str) -> str:
    return '<figure class="wide">' + svg + "<figcaption>" + caption + "</figcaption></figure>"


def box(kind: str, title: str, body: str) -> str:
    return (
        '<aside class="callout ' + kind + '"><div class="tag">' + title
        + "</div><div>" + body + "</div></aside>"
    )


def table(headers, rows) -> str:
    head = "".join("<th>" + h + "</th>" for h in headers)
    body = []
    for row in rows:
        body.append("<tr>" + "".join("<td>" + c + "</td>" for c in row) + "</tr>")
    return "<table><thead><tr>" + head + "</tr></thead><tbody>" + "".join(body) + "</tbody></table>"


def lecture(num: int, title: str, unit: str, mins: str, outcomes: list[str], body: str) -> str:
    n = "L" + str(num).zfill(2)
    aims = "<ul class=\"tight\">" + "".join("<li>" + o + "</li>" for o in outcomes) + "</ul>"
    return (
        '<article class="lecture" id="' + n.lower() + '">'
        '<div class="lec-head"><div class="lec-num">' + n + "</div>"
        '<div class="lec-titles"><div class="lec-meta">' + unit + " · " + mins
        + " · Intermediate / Class XI</div>"
        "<h1>" + title + "</h1></div></div>"
        + box("outcomes", "TODAY YOU WILL BE ABLE TO", aims)
        + body
        + "</article>\n"
    )


def mathjax() -> str:
    return """
<script>
window.MathJax = {
  tex: {
    inlineMath: [['\\\\(', '\\\\)'], ['$', '$']],
    displayMath: [['\\\\[', '\\\\]'], ['$$', '$$']],
    processEscapes: true
  },
  svg: { fontCache: 'local', displayAlign: 'center' },
  startup: {
    pageReady: function () {
      return MathJax.startup.defaultPageReady().then(function () {
        document.documentElement.dataset.mathjax = 'ready';
      });
    }
  }
};
</script>
<script src="vendor/tex-svg.js"></script>
"""
