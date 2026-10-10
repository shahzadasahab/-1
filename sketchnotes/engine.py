"""Hand-drawn sketchnote PDF engine for CS XI / XII lecture notes."""

from __future__ import annotations

import math
import os
from reportlab.lib.colors import Color, HexColor, Color as RLColor
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

HERE = os.path.dirname(os.path.abspath(__file__))
FONT_DIR = os.path.join(HERE, "fonts")


def _register_fonts():
    mapping = {
        "Title": "AmaticSC-Bold.ttf",
        "TitleReg": "AmaticSC-Regular.ttf",
        "Head": "Kalam-Bold.ttf",
        "HeadReg": "Kalam-Regular.ttf",
        "Body": "PatrickHand-Regular.ttf",
        "Note": "ArchitectsDaughter-Regular.ttf",
        "Doodle": "IndieFlower-Regular.ttf",
        "Script": "Handlee-Regular.ttf",
    }
    for name, fn in mapping.items():
        path = os.path.join(FONT_DIR, fn)
        if os.path.exists(path):
            pdfmetrics.registerFont(TTFont(name, path))
    # Monospace fallback
    mono = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"
    if os.path.exists(mono):
        pdfmetrics.registerFont(TTFont("Mono", mono))
    else:
        pdfmetrics.registerFont(TTFont("Mono", os.path.join(FONT_DIR, "PatrickHand-Regular.ttf")))


_register_fonts()


def C(hex_color: str) -> Color:
    return HexColor(hex_color)


# Paper + ink
PAPER = C("#F7F0DE")
INK = C("#2B2418")
MUTED = C("#6A5E4E")
RULE = C("#E4D6B8")
WHITE = C("#FFFDF6")
CARD = C("#FFF9EE")

# Accents
GOLD = C("#E39B12")
GOLD_BG = C("#FFE9A8")
GOLD_EDGE = C("#C07A08")
TEAL = C("#1B7A6E")
TEAL_BG = C("#D8F0EA")
CORAL = C("#D4543C")
CORAL_BG = C("#F8D8D2")
NAVY = C("#1E3A5F")
NAVY_BG = C("#D6E4F5")
SAGE = C("#4F8A4A")
SAGE_BG = C("#DCEFCF")
LAV = C("#6B4C9A")
LAV_BG = C("#E8DDF5")
SKY = C("#2F6F9A")
SKY_BG = C("#D4EAF8")
ROSE = C("#B83B6A")
ROSE_BG = C("#F6D6E4")
AMBER = C("#C46A12")
AMBER_BG = C("#F8E2C4")
INK_SOFT = C("#3D3428")

CHAPTER_PALETTES = {
    1: (NAVY, NAVY_BG, "#1E3A5F"),
    2: (AMBER, AMBER_BG, "#C46A12"),
    3: (SAGE, SAGE_BG, "#4F8A4A"),
    4: (LAV, LAV_BG, "#6B4C9A"),
    5: (CORAL, CORAL_BG, "#D4543C"),
    6: (SKY, SKY_BG, "#2F6F9A"),
}


_CHAR_FIX = str.maketrans({
    "★": "*",
    "⊕": "+",
    "·": "-",
    "•": "-",
    "–": "-",
    "—": "-",
    "‘": "'",
    "’": "'",
    "“": '"',
    "”": '"',
    "…": ".",
    "→": ">",
    "←": "<",
    "↔": "-",
    "≥": ">",
    "≤": "<",
    "×": "x",
    "÷": "/",
    "√": "v",
    "σ": "s",
    "²": "2",
    "³": "3",
    "ⁿ": "n",
    "▸": ">",
    "≈": "~",
    "✎": "*",
    "✦": "*",
    "▣": "*",
    "⚠": "!",
    "\u00b7": "-",
    "\u2022": "-",
})


def tidy(text):
    if text is None:
        return ""
    s = str(text).replace("\t", " ")
    s = s.replace("⊕", " xor ").replace("σ²", "var").replace("≥", ">=").replace("≤", "<=")
    return s.translate(_CHAR_FIX)


def wrap_text(text, font, size, width):
    if text is None:
        return []
    text = tidy(text)
    paragraphs = str(text).split("\n")
    lines = []
    for para in paragraphs:
        words = para.split()
        if not words:
            lines.append("")
            continue
        space = max(pdfmetrics.stringWidth(" ", font, size), size * (0.58 if font == "Mono" else 0.62))
        track = 0 if font == "Mono" else size * 0.07
        cur = words[0]
        cur_w = pdfmetrics.stringWidth(cur, font, size) + track
        for w in words[1:]:
            ww = pdfmetrics.stringWidth(w, font, size) + track
            if cur_w + space + ww <= width:
                cur = cur + " " + w
                cur_w += space + ww
            else:
                lines.append(cur)
                cur = w
                cur_w = ww
        lines.append(cur)
    return lines


def text_height(lines, leading):
    return len(lines) * leading if lines else 0


class SketchDoc:
    def __init__(self, path, book="XI", subtitle=""):
        self.path = path
        self.book = book
        self.subtitle = subtitle
        self.c = canvas.Canvas(path, pagesize=A4)
        self._install_spaced_text()
        self.W, self.H = A4
        self.L = 30
        self.R = self.W - 30
        self.usable = self.R - self.L
        self.top = self.H - 48
        self.bottom = 36
        self.y = self.top
        self.page = 0
        self.chapter = 0
        self.chapter_title = ""
        self.accent, self.accent_bg, _ = CHAPTER_PALETTES[1]
        self._page_started = False

    def _space_w(self, font, size):
        raw = pdfmetrics.stringWidth(" ", font, size)
        # Handwritten fonts overflow their advance width, so we force a wide gap.
        if font == "Mono":
            return max(raw, size * 0.58)
        return max(raw, size * 0.62)

    def _track(self, font, size):
        return 0 if font == "Mono" else size * 0.07

    def _text_width(self, text, font, size):
        text = tidy(text)
        space = self._space_w(font, size)
        track = self._track(font, size)
        parts = text.split(" ")
        w = 0
        for i, part in enumerate(parts):
            if part:
                w += pdfmetrics.stringWidth(part, font, size) + track
            if i < len(parts) - 1:
                w += space
        return w

    def _draw_words(self, x, y, text, align="left"):
        """Draw text word-by-word so space glyphs cannot collapse."""
        c = self.c
        font, size = c._fontname, c._fontsize
        text = tidy(text)
        space = self._space_w(font, size)
        track = self._track(font, size)
        orig = self._orig_drawString
        parts = text.split(" ")
        total = self._text_width(text, font, size)
        if align == "center":
            x = x - total / 2
        elif align == "right":
            x = x - total
        cx = x
        for i, part in enumerate(parts):
            if part:
                orig(cx, y, part)
                cx += pdfmetrics.stringWidth(part, font, size) + track
            if i < len(parts) - 1:
                cx += space
        return total

    def _install_spaced_text(self):
        c = self.c
        self._orig_drawString = c.drawString
        self._orig_centre = c.drawCentredString
        self._orig_right = c.drawRightString

        def drawString(x, y, text, mode=None, **kwargs):
            self._draw_words(x, y, "" if text is None else str(text), "left")

        def drawCentredString(x, y, text):
            self._draw_words(x, y, "" if text is None else str(text), "center")

        def drawRightString(x, y, text):
            self._draw_words(x, y, "" if text is None else str(text), "right")

        c.drawString = drawString
        c.drawCentredString = drawCentredString
        c.drawRightString = drawRightString

    # ---------- page chrome ----------
    def _paper(self):
        c = self.c
        c.setFillColor(PAPER)
        c.rect(0, 0, self.W, self.H, fill=1, stroke=0)
        # faint ruled texture
        c.setStrokeColor(RULE)
        c.setLineWidth(0.25)
        y = 40
        while y < self.H - 40:
            c.line(self.L + 8, y, self.R - 8, y)
            y += 22
        # margin doodle line
        c.setStrokeColor(C("#D8C49A"))
        c.setLineWidth(1.1)
        c.line(22, 28, 22, self.H - 22)

    def _header_footer(self):
        c = self.c
        # header tape
        c.setFillColor(self.accent)
        c.roundRect(self.L, self.H - 34, self.usable, 18, 6, fill=1, stroke=0)
        c.setFillColor(WHITE)
        c.setFont("Note", 8.5)
        left = f"CS {self.book}  ·  Complete Sketchnotes"
        if self.chapter_title:
            left += f"  ·  Ch {self.chapter}: {self.chapter_title}"
        c.drawString(self.L + 10, self.H - 28.5, left[:95])
        c.drawRightString(self.R - 10, self.H - 28.5, f"{self.page}")
        # footer
        c.setFillColor(MUTED)
        c.setFont("Doodle", 8)
        c.drawCentredString(self.W / 2, 18, "Sindh Curriculum  ·  All exam-relevant details kept intact  ·  ★ = Golden Topic")

    def new_page(self, force=False):
        if self._page_started:
            self.c.showPage()
        self.page += 1
        self._paper()
        self._header_footer()
        self.y = self.top
        self._page_started = True

    def ensure(self, h):
        if not self._page_started:
            self.new_page()
        if self.y - h < self.bottom + 6:
            self.new_page()

    def gap(self, h=8):
        self.y -= h

    def set_chapter(self, n, title):
        self.chapter = n
        self.chapter_title = title
        self.accent, self.accent_bg, _ = CHAPTER_PALETTES.get(n, CHAPTER_PALETTES[1])

    # ---------- primitives ----------
    def string_w(self, text, font, size):
        return self._text_width(text, font, size)

    def wobble_rect(self, x, y, w, h, stroke=INK, fill=CARD, radius=9, lw=1.3):
        c = self.c
        c.setFillColor(fill)
        c.setStrokeColor(stroke)
        c.setLineWidth(lw)
        c.roundRect(x, y, w, h, radius, fill=1, stroke=1)
        # extra sketch tick
        c.setLineWidth(0.6)
        c.setStrokeColor(stroke)
        c.line(x + 4, y + h - 3, x + min(28, w * 0.2), y + h - 1.5)

    def marker_underline(self, x, y, w, color=GOLD):
        try:
            fade = Color(color.red, color.green, color.blue, alpha=0.35)
        except Exception:
            fade = color
        self.c.setStrokeColor(fade)
        self.c.setLineWidth(3.2)
        self.c.line(x, y, x + w, y - 1)

    def star(self, x, y, r=5, color=GOLD):
        c = self.c
        c.setFillColor(color)
        path = c.beginPath()
        for i in range(10):
            ang = math.radians(-90 + i * 36)
            rad = r if i % 2 == 0 else r * 0.42
            px, py = x + rad * math.cos(ang), y + rad * math.sin(ang)
            if i == 0:
                path.moveTo(px, py)
            else:
                path.lineTo(px, py)
        path.close()
        c.drawPath(path, fill=1, stroke=0)

    def draw_lines(self, lines, x, y, font, size, color, leading):
        self.c.setFillColor(color)
        self.c.setFont(font, size)
        for i, line in enumerate(lines):
            self.c.drawString(x, y - i * leading, line)
        return y - len(lines) * leading

    def para_block(self, text, x, y, w, font="Body", size=10.5, color=INK, leading=None):
        leading = leading or size + 3.2
        lines = wrap_text(text, font, size, w)
        ny = self.draw_lines(lines, x, y, font, size, color, leading)
        return ny, text_height(lines, leading)

    # ---------- high-level blocks ----------
    def h1(self, text, golden=False):
        size = 20
        lines = wrap_text(text, "Head", size, self.usable - (22 if golden else 0))
        h = 10 + len(lines) * 24
        self.ensure(h)
        x = self.L
        if golden:
            self.star(self.L + 7, self.y - 8, 6)
            x = self.L + 20
        yy = self.y - 6
        self.c.setFillColor(self.accent)
        self.c.setFont("Head", size)
        for i, line in enumerate(lines):
            self.c.drawString(x, yy - i * 24, line)
            self.marker_underline(x, yy - i * 24 - 2, min(self.string_w(line, "Head", size), 280), self.accent)
        self.y = yy - len(lines) * 24 - 6
        if golden:
            self._chip(self.L, self.y - 2, "★ GOLDEN TOPIC", GOLD, INK)
            self.y -= 18

    def h2(self, text, golden=False):
        size = 14
        lines = wrap_text(text, "HeadReg", size, self.usable - (18 if golden else 0))
        h = 8 + len(lines) * 18 + (16 if golden else 0)
        self.ensure(h)
        x = self.L
        if golden:
            self.star(self.L + 6, self.y - 4, 5)
            x = self.L + 16
        self.c.setFillColor(INK)
        self.c.setFont("HeadReg", size)
        yy = self.y - 2
        for i, line in enumerate(lines):
            self.c.drawString(x, yy - i * 18, line)
        self.y = yy - len(lines) * 18 - 4
        if golden:
            self._chip(self.L, self.y, "★ GOLDEN TOPIC", GOLD, INK)
            self.y -= 16

    def h3(self, text, golden=False):
        size = 12
        lines = wrap_text(text, "HeadReg", size, self.usable - (16 if golden else 0))
        self.ensure(6 + len(lines) * 15 + (14 if golden else 0))
        x = self.L
        if golden:
            self.star(self.L + 5, self.y + 2, 4.5)
            x = self.L + 14
        self.c.setFillColor(self.accent)
        self.c.setFont("HeadReg", size)
        yy = self.y
        for i, line in enumerate(lines):
            self.c.drawString(x, yy - i * 15, line)
        self.y = yy - len(lines) * 15 - 3
        if golden:
            self._chip(self.L, self.y, "★ GOLDEN TOPIC", GOLD, INK)
            self.y -= 14

    def p(self, text, size=10.6):
        lines = wrap_text(text, "Body", size, self.usable)
        leading = size + 3.4
        h = text_height(lines, leading) + 6
        self.ensure(h)
        self.y = self.draw_lines(lines, self.L, self.y, "Body", size, INK, leading) - 6

    def bullets(self, items, size=10.5):
        leading = size + 3.4
        # estimate
        all_lines = 0
        wrapped = []
        for it in items:
            ls = wrap_text(str(it), "Body", size, self.usable - 16)
            wrapped.append(ls)
            all_lines += max(1, len(ls))
        self.ensure(all_lines * leading + 8)
        for ls in wrapped:
            self.c.setFillColor(self.accent)
            self.c.circle(self.L + 5, self.y + 3, 2.2, fill=1, stroke=0)
            self.y = self.draw_lines(ls, self.L + 14, self.y, "Body", size, INK, leading) - 2
        self.y -= 4

    def numbered(self, items, size=10.5):
        leading = size + 3.4
        wrapped = []
        total = 0
        for it in items:
            ls = wrap_text(str(it), "Body", size, self.usable - 22)
            wrapped.append(ls)
            total += max(1, len(ls))
        self.ensure(total * leading + 8)
        for i, ls in enumerate(wrapped, 1):
            self.c.setFillColor(self.accent)
            self.c.setFont("Head", 10)
            self.c.drawString(self.L, self.y, f"{i}.")
            self.y = self.draw_lines(ls, self.L + 18, self.y, "Body", size, INK, leading) - 2
        self.y -= 4

    def _chip(self, x, y, label, bg, fg):
        w = self.string_w(label, "Note", 8) + 14
        self.c.setFillColor(bg)
        self.c.roundRect(x, y - 3, w, 13, 6, fill=1, stroke=0)
        self.c.setFillColor(fg)
        self.c.setFont("Note", 8)
        self.c.drawString(x + 7, y, label)
        return w

    def callout(self, kind, title, body):
        styles = {
            "golden": (GOLD_BG, GOLD_EDGE, "★", GOLD),
            "tip": (TEAL_BG, TEAL, "✎", TEAL),
            "analogy": (LAV_BG, LAV, "≈", LAV),
            "warn": (CORAL_BG, CORAL, "!", CORAL),
            "memory": (AMBER_BG, AMBER, "✦", AMBER),
            "case": (NAVY_BG, NAVY, "▣", NAVY),
            "note": (SKY_BG, SKY, "i", SKY),
        }
        bg, edge, icon, ic = styles.get(kind, styles["note"])
        pad = 10
        inner_w = self.usable - 2 * pad - 8
        t_lines = wrap_text(title, "HeadReg", 11, inner_w)
        b_lines = wrap_text(body, "Body", 10.2, inner_w)
        h = 16 + len(t_lines) * 14 + len(b_lines) * 13.4 + 10
        self.ensure(h + 6)
        box_y = self.y - h
        self.wobble_rect(self.L, box_y, self.usable, h, stroke=edge, fill=bg, radius=10, lw=1.5)
        self.c.setFillColor(ic)
        self.c.setFont("Head", 14)
        self.c.drawString(self.L + 10, self.y - 16, icon)
        yy = self.y - 16
        yy = self.draw_lines(t_lines, self.L + 28, yy, "HeadReg", 11, INK, 14)
        yy -= 2
        self.draw_lines(b_lines, self.L + 12, yy, "Body", 10.2, INK_SOFT, 13.4)
        self.y = box_y - 8

    def cards(self, items, cols=2, title_size=11.5):
        if not items:
            return
        gap = 8
        col_w = (self.usable - gap * (cols - 1)) / cols
        # measure each card
        measured = []
        for title, body in items:
            t_lines = wrap_text(title, "HeadReg", title_size, col_w - 16)
            b_lines = wrap_text(body, "Body", 9.8, col_w - 16)
            h = 14 + len(t_lines) * 14 + 4 + len(b_lines) * 12.8 + 10
            measured.append((title, body, t_lines, b_lines, h))
        # layout in rows
        i = 0
        while i < len(measured):
            row = measured[i:i + cols]
            row_h = max(m[4] for m in row)
            self.ensure(row_h + 8)
            for j, (title, body, t_lines, b_lines, h) in enumerate(row):
                x = self.L + j * (col_w + gap)
                y = self.y - row_h
                self.wobble_rect(x, y, col_w, row_h, stroke=self.accent, fill=WHITE, radius=8)
                self.c.setFillColor(self.accent)
                self.c.rect(x, y + row_h - 5, col_w, 5, fill=1, stroke=0)
                yy = y + row_h - 18
                yy = self.draw_lines(t_lines, x + 8, yy, "HeadReg", title_size, self.accent, 14)
                yy -= 3
                self.draw_lines(b_lines, x + 8, yy, "Body", 9.8, INK, 12.8)
            self.y -= row_h + 8
            i += cols

    def compare(self, left_title, left_items, right_title, right_items,
                left_color=None, right_color=None):
        lc = left_color or TEAL
        rc = right_color or CORAL
        gap = 8
        col_w = (self.usable - gap) / 2

        def measure(title, items):
            t = wrap_text(title, "HeadReg", 12, col_w - 16)
            body_lines = []
            for it in items:
                body_lines.extend(wrap_text("• " + str(it), "Body", 9.8, col_w - 16))
            h = 18 + len(t) * 15 + 6 + len(body_lines) * 13 + 12
            return t, body_lines, h

        lt, lb, lh = measure(left_title, left_items)
        rt, rb, rh = measure(right_title, right_items)
        h = max(lh, rh)
        self.ensure(h + 6)
        y = self.y - h

        def draw_col(x, title_lines, body_lines, color, bg):
            self.wobble_rect(x, y, col_w, h, stroke=color, fill=bg, radius=9)
            self.c.setFillColor(color)
            self.c.roundRect(x, y + h - 20, col_w, 20, 9, fill=1, stroke=0)
            self.c.rect(x, y + h - 20, col_w, 10, fill=1, stroke=0)
            self.c.setFillColor(WHITE)
            self.c.setFont("HeadReg", 11)
            # title may wrap - use first line centered-ish
            self.c.drawString(x + 8, y + h - 15, title_lines[0][:40] if title_lines else "")
            yy = y + h - 34
            if len(title_lines) > 1:
                yy = self.draw_lines(title_lines[1:], x + 8, yy, "HeadReg", 11, color, 14) - 2
            self.draw_lines(body_lines, x + 8, yy, "Body", 9.8, INK, 13)

        draw_col(self.L, lt, lb, lc, WHITE)
        draw_col(self.L + col_w + gap, rt, rb, rc, WHITE)
        # vs badge
        self.c.setFillColor(INK)
        self.c.circle(self.L + col_w + gap / 2, y + h / 2, 11, fill=1, stroke=0)
        self.c.setFillColor(WHITE)
        self.c.setFont("Note", 7)
        self.c.drawCentredString(self.L + col_w + gap / 2, y + h / 2 - 2.5, "VS")
        self.y = y - 8

    def table(self, headers, rows, col_fracs=None, font_size=8.6):
        cols = len(headers)
        if col_fracs is None:
            col_fracs = [1] * cols
        s = sum(col_fracs)
        widths = [self.usable * f / s for f in col_fracs]
        pad = 4

        def cell_lines(text, w):
            return wrap_text(str(text), "Body", font_size, w - 2 * pad)

        header_lines = [cell_lines(h, widths[i]) for i, h in enumerate(headers)]
        header_h = max(16, max(len(ls) for ls in header_lines) * (font_size + 2.6) + 8)
        row_data = []
        for row in rows:
            rlines = [cell_lines(row[i] if i < len(row) else "", widths[i]) for i in range(cols)]
            rh = max(14, max(len(ls) for ls in rlines) * (font_size + 2.4) + 6)
            row_data.append((rlines, rh))

        total_h = header_h + sum(rh for _, rh in row_data)
        # if huge, split across pages
        self.ensure(header_h + 20)

        def draw_header(y_top):
            x = self.L
            self.c.setFillColor(self.accent)
            self.c.rect(self.L, y_top - header_h, self.usable, header_h, fill=1, stroke=0)
            xx = self.L
            for i, ls in enumerate(header_lines):
                self.c.setFillColor(WHITE)
                self.c.setFont("HeadReg", font_size + 0.6)
                yy = y_top - 12
                for line in ls:
                    self.c.drawString(xx + pad, yy, line)
                    yy -= font_size + 2.6
                xx += widths[i]
            return y_top - header_h

        y = self.y
        y = draw_header(y)
        for idx, (rlines, rh) in enumerate(row_data):
            if y - rh < self.bottom + 8:
                self.new_page()
                y = self.y
                y = draw_header(y)
            bg = WHITE if idx % 2 == 0 else self.accent_bg
            self.c.setFillColor(bg)
            self.c.rect(self.L, y - rh, self.usable, rh, fill=1, stroke=0)
            self.c.setStrokeColor(RULE)
            self.c.setLineWidth(0.4)
            self.c.line(self.L, y - rh, self.R, y - rh)
            xx = self.L
            for i, ls in enumerate(rlines):
                self.c.setFillColor(INK)
                self.c.setFont("Body", font_size)
                yy = y - 11
                for line in ls:
                    self.c.drawString(xx + pad, yy, line)
                    yy -= font_size + 2.4
                xx += widths[i]
            y -= rh
        # outer border
        self.c.setStrokeColor(self.accent)
        self.c.setLineWidth(1.1)
        self.y = y - 8

    def code(self, code, title=None):
        lines = str(code).rstrip().split("\n")
        size = 7.6
        leading = 10.2
        h = 14 + (12 if title else 0) + len(lines) * leading + 10
        self.ensure(min(h, self.top - self.bottom - 20))
        # if too tall, paginate
        y = self.y
        box_top = y
        inner_h = h
        if self.y - h < self.bottom:
            # draw what fits then continue
            pass
        box_h = min(h, self.y - self.bottom - 4)
        self.wobble_rect(self.L, self.y - box_h, self.usable, box_h, stroke=NAVY, fill=C("#1B2430"), radius=8, lw=1.2)
        yy = self.y - 14
        if title:
            self.c.setFillColor(GOLD)
            self.c.setFont("Note", 8)
            self.c.drawString(self.L + 10, yy, title)
            yy -= 12
        self.c.setFont("Mono", size)
        self.c.setFillColor(C("#E8F0D8"))
        for line in lines:
            if yy < self.bottom + 10:
                self.y = self.bottom
                self.new_page()
                remain = (len(lines) - lines.index(line)) * leading + 20
                bh = min(remain, self.y - self.bottom - 4)
                self.wobble_rect(self.L, self.y - bh, self.usable, bh, stroke=NAVY, fill=C("#1B2430"), radius=8)
                yy = self.y - 14
                self.c.setFont("Mono", size)
                self.c.setFillColor(C("#E8F0D8"))
            # clip long lines
            shown = line
            while self.string_w(shown, "Mono", size) > self.usable - 20 and len(shown) > 4:
                shown = shown[:-1]
            self.c.drawString(self.L + 10, yy, shown)
            yy -= leading
        self.y = yy - 10

    def steps(self, items):
        """Numbered step chips in a vertical list."""
        for i, text in enumerate(items, 1):
            lines = wrap_text(text, "Body", 10.3, self.usable - 36)
            h = max(22, len(lines) * 13.4 + 8)
            self.ensure(h + 4)
            # circle
            cy = self.y - 10
            self.c.setFillColor(self.accent)
            self.c.circle(self.L + 10, cy, 9, fill=1, stroke=0)
            self.c.setFillColor(WHITE)
            self.c.setFont("Head", 10)
            self.c.drawCentredString(self.L + 10, cy - 3, str(i))
            ny = self.draw_lines(lines, self.L + 26, self.y - 4, "Body", 10.3, INK, 13.4)
            self.y = min(ny, self.y - h) - 4

    def flow(self, labels):
        n = len(labels)
        if n == 0:
            return
        h = 36
        self.ensure(h + 10)
        gap = 8
        arrow = 12
        box_w = (self.usable - (n - 1) * (gap + arrow)) / n
        y = self.y - h
        for i, lab in enumerate(labels):
            x = self.L + i * (box_w + gap + arrow)
            self.wobble_rect(x, y, box_w, h, stroke=self.accent, fill=WHITE, radius=8)
            lines = wrap_text(str(lab), "Note", 8, box_w - 8)
            self.c.setFillColor(INK)
            self.c.setFont("Note", 8)
            ty = y + h / 2 + (len(lines) - 1) * 4
            for j, line in enumerate(lines[:3]):
                self.c.drawCentredString(x + box_w / 2, ty - j * 10, line)
            if i < n - 1:
                ax = x + box_w + 2
                self.c.setFillColor(self.accent)
                self.c.setStrokeColor(self.accent)
                self.c.setLineWidth(1.4)
                mid = y + h / 2
                self.c.line(ax, mid, ax + arrow - 2, mid)
                self.c.drawRightString(ax + arrow, mid - 3, "▸")
        self.y = y - 10

    def kv_grid(self, pairs, cols=2):
        """Key → value definition cards."""
        self.cards([(k, v) for k, v in pairs], cols=cols)

    def banner(self, text, bg=None, fg=None):
        bg = bg or self.accent
        fg = fg or WHITE
        lines = wrap_text(text, "HeadReg", 12, self.usable - 20)
        h = 12 + len(lines) * 15
        self.ensure(h + 4)
        self.wobble_rect(self.L, self.y - h, self.usable, h, stroke=bg, fill=bg, radius=8)
        self.draw_lines(lines, self.L + 10, self.y - 14, "HeadReg", 12, fg, 15)
        self.y -= h + 8

    def divider(self, label=""):
        self.ensure(16)
        self.c.setStrokeColor(self.accent)
        self.c.setLineWidth(0.9)
        mid = self.y - 6
        if label:
            w = self.string_w(label, "Note", 8)
            cx = self.W / 2
            self.c.line(self.L, mid, cx - w / 2 - 8, mid)
            self.c.line(cx + w / 2 + 8, mid, self.R, mid)
            self.c.setFillColor(self.accent)
            self.c.setFont("Note", 8)
            self.c.drawCentredString(cx, mid - 3, label)
        else:
            self.c.line(self.L, mid, self.R, mid)
        self.y -= 16

    def cover(self, title, chapter_lines, edition_line, extra_lines=None):
        self.new_page()
        c = self.c
        # hide header look by painting over? keep it subtle
        c.setFillColor(self.accent)
        c.rect(0, self.H - 140, self.W, 140, fill=1, stroke=0)
        c.setFillColor(GOLD)
        c.rect(0, self.H - 148, self.W, 8, fill=1, stroke=0)
        c.setFillColor(WHITE)
        c.setFont("Title", 42)
        c.drawCentredString(self.W / 2, self.H - 70, title)
        c.setFont("Note", 11)
        c.drawCentredString(self.W / 2, self.H - 100, "COMPLETE SKETCHNOTES")
        c.setFont("Doodle", 10)
        c.drawCentredString(self.W / 2, self.H - 118, edition_line)

        y = self.H - 190
        c.setFillColor(INK)
        c.setFont("Head", 16)
        c.drawCentredString(self.W / 2, y, "What is inside")
        y -= 16
        for i, line in enumerate(chapter_lines, 1):
            pal, bg, _ = CHAPTER_PALETTES.get(i, CHAPTER_PALETTES[1])
            self.wobble_rect(70, y - 22, self.W - 140, 26, stroke=pal, fill=bg, radius=8)
            c.setFillColor(pal)
            c.setFont("Head", 12)
            c.drawString(86, y - 12, f"{i}")
            c.setFillColor(INK)
            c.setFont("Body", 11)
            c.drawString(108, y - 12, line)
            y -= 32

        y -= 8
        extra = extra_lines or [
            "Every definition, table, algorithm, example, case study and career note is kept.",
            "★ Golden Topics are exam-critical — they get a gold star and a highlight box.",
            "Visual sketchnote style: cards, comparisons, flows, truth tables, and diagrams.",
        ]
        for line in extra:
            ls = wrap_text("• " + line, "Body", 11, self.W - 140)
            c.setFillColor(INK)
            c.setFont("Body", 11)
            for l in ls:
                c.drawString(80, y, l)
                y -= 14
            y -= 4

        c.setFillColor(MUTED)
        c.setFont("Doodle", 9)
        c.drawCentredString(self.W / 2, 50, "Bilingual Teacher's Edition source  ·  English sketchnotes with all relevant detail")

        self.y = 40

    def toc_page(self, sections):
        """sections: list of (ch, title, topics[list])"""
        self.new_page()
        self.h1("Map of the book")
        self.p("Use this as a visual index. ★ marks golden / exam-critical clusters.")
        for ch, title, topics in sections:
            pal, bg, _ = CHAPTER_PALETTES.get(ch, CHAPTER_PALETTES[1])
            topic_text = "   ·   ".join(topics)
            t_lines = wrap_text(topic_text, "Body", 9.6, self.usable - 20)
            h = 28 + len(t_lines) * 12.4 + 8
            self.ensure(h)
            y = self.y - h
            self.wobble_rect(self.L, y, self.usable, h, stroke=pal, fill=bg, radius=8)
            self.c.setFillColor(pal)
            self.c.setFont("Head", 13)
            self.c.drawString(self.L + 10, self.y - 16, f"Chapter {ch}  —  {title}")
            self.draw_lines(t_lines, self.L + 10, self.y - 32, "Body", 9.6, INK, 12.4)
            self.y = y - 7

    def chapter_open(self, n, title, blurb, topics):
        self.set_chapter(n, title)
        self.new_page()
        pal, bg, _ = CHAPTER_PALETTES[n]
        lines = wrap_text(title, "Title", 34, self.usable - 40)
        box_h = 36 + len(lines) * 32 + 18
        box_y = self.H - 48 - box_h
        self.c.setFillColor(pal)
        self.c.roundRect(self.L, box_y, self.usable, box_h, 14, fill=1, stroke=0)
        self.c.setFillColor(GOLD)
        self.c.setFont("Note", 11)
        self.c.drawString(self.L + 22, self.H - 68, f"CHAPTER {n}")
        self.c.setFillColor(WHITE)
        yy = self.H - 98
        for line in lines:
            self.c.setFont("Title", 34)
            self.c.drawString(self.L + 20, yy, line)
            yy -= 32
        self.y = box_y - 16
        self.p(blurb, size=11.5)
        self.h2("You will sketch")
        self.numbered(topics)

    def summary(self, items):
        self.h2("Chapter wrap — keep these")
        self.bullets(items)

    def truth(self, title, headers, rows, highlight=None):
        """Truth table with optional highlight callable(row)->bool or set of row indexes."""
        self.h3(title)
        self.table(headers, rows, col_fracs=[1] * len(headers))

    def save(self):
        if not self._page_started:
            self.new_page()
        self.c.save()
        return self.path, self.page
