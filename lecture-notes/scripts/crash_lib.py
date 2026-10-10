"""Render a 30-day coaching crash booklet to HTML."""
from html import escape
from pathlib import Path


HEAD = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>{title}</title>
<link rel="stylesheet" href="../assets/notes.css">
<script>
window.MathJax = {{
  tex: {{ inlineMath: [['$','$'],['\\\\(','\\\\)']], displayMath: [['$$','$$'],['\\\\[','\\\\]']] }},
  svg: {{ fontCache: 'global' }}
}};
</script>
<script src="../assets/mathjax/es5/tex-svg.js"></script>
</head>
<body>
<div class="page">
"""

TAIL = """
</div>
</body>
</html>
"""


def day(n, title, unit, aims, teach, board, drills, tonight, trap,
        recall=None, paper=None, scheme=None):
    return {
        "n": n,
        "title": title,
        "unit": unit,
        "aims": aims,
        "teach": teach,
        "board": board,
        "drills": drills,
        "tonight": tonight,
        "trap": trap,
        "recall": recall or [],
        "paper": paper,
        "scheme": scheme,
    }


def _aims(items):
    lis = "".join(f"<li>{escape(x)}</li>" for x in items)
    return f"<div class='card ok'><div class='label'>Leave able to</div><ul>{lis}</ul></div>"


def _drills(items, start=1):
    blocks = []
    for i, (q, a) in enumerate(items, start):
        blocks.append(
            "<div class='q'>"
            f"<p class='prompt'><strong>{i}.</strong> {q}</p>"
            f"<div class='answer'><strong>Model.</strong> {a}</div>"
            "</div>"
        )
    return "\n".join(blocks)


def _recall(items):
    if not items:
        return ""
    rows = "".join(
        f"<tr><td>{escape(q)}</td><td>{escape(a)}</td></tr>" for q, a in items
    )
    return (
        "<h3>Ten-minute recall — yesterday, closed book</h3>"
        "<table class='long'><tr><th>Ask</th><th>Accept</th></tr>"
        f"{rows}</table>"
    )


def _session():
    return """
<div class="session">
  <div><strong>10 min</strong>Recall, cold</div>
  <div><strong>25 min</strong>Teach from the board</div>
  <div><strong>25 min</strong>Work the example together</div>
  <div><strong>40 min</strong>Silent drill, then mark</div>
  <div><strong>20 min</strong>Homework set and traps</div>
</div>
"""


def render_day(d):
    n = d["n"]
    body = [
        "<section class='day'>",
        "<div class='running'><span>30-Day Crash · Day "
        f"{n:02d}</span><span>{escape(d['unit'])}</span></div>",
        "<div class='dayhead'>",
        f"<div class='daynum'><span>DAY</span><strong>{n:02d}</strong></div>",
        "<div>",
        f"<h2>{escape(d['title'])}</h2>",
        f"<p class='clock'>{escape(d['unit'])} · 120-minute coached session</p>",
        "</div></div>",
        _session(),
        "<div class='card-row'>",
        _aims(d["aims"]),
        f"<div class='card warn'><div class='label'>Trap that costs the mark</div><p>{d['trap']}</p></div>",
        "</div>",
        _recall(d["recall"]),
    ]
    if d["scheme"]:
        body.append("<h3>Marking the mock — coach aloud, student in a different colour</h3>")
        body.append(d["scheme"])
    elif d["paper"]:
        body.append("<h3>Sit this as an exam. 90 minutes. No notes. No phone.</h3>")
        body.append(d["paper"])
        body.append(
            "<div class='callout watch'><div class='mark'>Stop</div>"
            "<div>Do not open Day 30 until the paper is finished and the time is written on the top.</div></div>"
        )
    else:
        body.append("<h3>Board notes</h3>")
        body.append(d["teach"])
        body.append("<h3>Worked example — do not skip the steps</h3>")
        body.append(d["board"])
        body.append("<h3>Silent drill — cover the green model lines</h3>")
        body.append(_drills(d["drills"]))
    body.append("<div class='callout try'><div class='mark'>Tonight</div>"
                f"<div>{d['tonight']}</div></div>")
    body.append("</section>")
    return "\n".join(body)


def render_book(meta, days, dest: Path):
    parts = [HEAD.format(title=escape(meta["title"]))]
    parts.append(meta["front"])
    parts.append(meta["map"])
    for d in days:
        parts.append(render_day(d))
    parts.append(TAIL)
    dest.write_text("".join(parts), encoding="utf-8")
    print("wrote", dest, "days", len(days))
