"""Shared ReportLab helpers for the Class XI Computer Science study guide."""

from __future__ import annotations

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT, TA_RIGHT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, StyleSheet1
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    Flowable,
    KeepTogether,
    ListFlowable,
    ListItem,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)

NAVY = colors.HexColor("#1B365D")
TEAL = colors.HexColor("#0D7377")
GOLD = colors.HexColor("#C4A35A")
INK = colors.HexColor("#1F2430")
MUTED = colors.HexColor("#4A5568")
CREAM = colors.HexColor("#F6F1E6")
PALE = colors.HexColor("#EEF4F6")
PALE_GOLD = colors.HexColor("#F8F1DC")
PALE_ROSE = colors.HexColor("#F8EAEA")
PALE_GREEN = colors.HexColor("#E8F3EC")
PALE_AMBER = colors.HexColor("#FBF3D9")
LINE = colors.HexColor("#C9D3DA")
WHITE = colors.white

PAGE_W, PAGE_H = A4
LEFT = 18 * mm
RIGHT = 18 * mm
TOP = 20 * mm
BOTTOM = 18 * mm


def register_fonts() -> None:
    base = "/usr/share/fonts/truetype/dejavu"
    pdfmetrics.registerFont(TTFont("Body", f"{base}/DejaVuSerif.ttf"))
    pdfmetrics.registerFont(TTFont("Body-Bold", f"{base}/DejaVuSerif-Bold.ttf"))
    pdfmetrics.registerFont(TTFont("Body-Italic", f"{base}/DejaVuSerif.ttf"))
    pdfmetrics.registerFont(TTFont("Body-BoldItalic", f"{base}/DejaVuSerif-Bold.ttf"))
    pdfmetrics.registerFont(TTFont("Sans", f"{base}/DejaVuSans.ttf"))
    pdfmetrics.registerFont(TTFont("Sans-Bold", f"{base}/DejaVuSans-Bold.ttf"))
    pdfmetrics.registerFont(TTFont("Sans-Italic", f"{base}/DejaVuSans.ttf"))
    pdfmetrics.registerFont(TTFont("Mono", f"{base}/DejaVuSansMono.ttf"))
    pdfmetrics.registerFont(TTFont("Mono-Bold", f"{base}/DejaVuSansMono-Bold.ttf"))
    pdfmetrics.registerFontFamily(
        "Body",
        normal="Body",
        bold="Body-Bold",
        italic="Body-Italic",
        boldItalic="Body-BoldItalic",
    )
    pdfmetrics.registerFontFamily(
        "Sans",
        normal="Sans",
        bold="Sans-Bold",
        italic="Sans-Italic",
        boldItalic="Sans-Bold",
    )


def stylesheet() -> StyleSheet1:
    s = StyleSheet1()
    s.add(ParagraphStyle(name="Normal", fontName="Body", fontSize=10.5, leading=15, textColor=INK, alignment=TA_JUSTIFY))
    s.add(ParagraphStyle(name="CoverKicker", fontName="Sans", fontSize=10, leading=13, textColor=GOLD, alignment=TA_CENTER, tracking=1.2))
    s.add(ParagraphStyle(name="CoverTitle", fontName="Sans-Bold", fontSize=28, leading=34, textColor=WHITE, alignment=TA_CENTER))
    s.add(ParagraphStyle(name="CoverSub", fontName="Body", fontSize=13, leading=18, textColor=colors.HexColor("#D9E4EC"), alignment=TA_CENTER))
    s.add(ParagraphStyle(name="H1", fontName="Sans-Bold", fontSize=18, leading=22, textColor=NAVY, spaceBefore=8, spaceAfter=8))
    s.add(ParagraphStyle(name="H2", fontName="Sans-Bold", fontSize=13.5, leading=17, textColor=TEAL, spaceBefore=12, spaceAfter=6))
    s.add(ParagraphStyle(name="H3", fontName="Sans-Bold", fontSize=11.5, leading=15, textColor=NAVY, spaceBefore=9, spaceAfter=4))
    s.add(ParagraphStyle(name="Body", fontName="Body", fontSize=10.5, leading=15, textColor=INK, alignment=TA_JUSTIFY, spaceAfter=7))
    s.add(ParagraphStyle(name="BodyTight", fontName="Body", fontSize=10.5, leading=14.5, textColor=INK, alignment=TA_JUSTIFY, spaceAfter=3))
    s.add(ParagraphStyle(name="Lead", fontName="Body-Italic", fontSize=11.2, leading=16, textColor=MUTED, alignment=TA_JUSTIFY, spaceAfter=10))
    s.add(ParagraphStyle(name="Bullet", fontName="Body", fontSize=10.5, leading=14.5, textColor=INK, leftIndent=12, spaceAfter=2))
    s.add(ParagraphStyle(name="Caption", fontName="Sans-Italic", fontSize=8.5, leading=11, textColor=MUTED, alignment=TA_CENTER, spaceBefore=2, spaceAfter=8))
    s.add(ParagraphStyle(name="Code", fontName="Mono", fontSize=8.4, leading=11.6, textColor=INK, leftIndent=0))
    s.add(ParagraphStyle(name="TableHead", fontName="Sans-Bold", fontSize=8.4, leading=11, textColor=WHITE, alignment=TA_CENTER))
    s.add(ParagraphStyle(name="TableCell", fontName="Sans", fontSize=8.4, leading=11, textColor=INK, alignment=TA_LEFT))
    s.add(ParagraphStyle(name="TableCellC", fontName="Sans", fontSize=8.4, leading=11, textColor=INK, alignment=TA_CENTER))
    s.add(ParagraphStyle(name="CalloutTitle", fontName="Sans-Bold", fontSize=9, leading=12, textColor=NAVY, spaceAfter=2))
    s.add(ParagraphStyle(name="CalloutBody", fontName="Body", fontSize=9.6, leading=13.2, textColor=INK, alignment=TA_LEFT))
    s.add(ParagraphStyle(name="Footer", fontName="Sans", fontSize=8, leading=10, textColor=MUTED))
    s.add(ParagraphStyle(name="TOCUnit", fontName="Sans-Bold", fontSize=11, leading=15, textColor=NAVY, spaceBefore=8, spaceAfter=2))
    s.add(ParagraphStyle(name="TOCItem", fontName="Body", fontSize=10, leading=14, textColor=INK, leftIndent=10))
    s.add(ParagraphStyle(name="QStem", fontName="Body", fontSize=10.5, leading=14.5, textColor=INK, spaceBefore=6, spaceAfter=2))
    s.add(ParagraphStyle(name="Small", fontName="Sans", fontSize=8.5, leading=11.5, textColor=MUTED))
    s.add(ParagraphStyle(name="Center", fontName="Body", fontSize=10.5, leading=15, textColor=INK, alignment=TA_CENTER))
    s.add(ParagraphStyle(name="Answer", fontName="Body", fontSize=10.2, leading=14.2, textColor=INK, leftIndent=8, spaceAfter=4))
    return s


class ColoredRule(Flowable):
    def __init__(self, color=GOLD, thickness=1.2, space_before=2, space_after=8, width=None):
        super().__init__()
        self.color = color
        self.thickness = thickness
        self.spaceBefore = space_before
        self.spaceAfter = space_after
        self._width = width

    def wrap(self, availWidth, availHeight):
        self.width = self._width or availWidth
        self.height = self.thickness + self.spaceBefore + self.spaceAfter
        return self.width, self.height

    def draw(self):
        self.canv.setStrokeColor(self.color)
        self.canv.setLineWidth(self.thickness)
        y = self.spaceAfter
        self.canv.line(0, y, self.width, y)


class Callout(Flowable):
    KINDS = {
        "key": (PALE, TEAL, "KEY IDEA"),
        "try": (PALE_AMBER, GOLD, "TRY THIS NOW"),
        "mistake": (PALE_ROSE, colors.HexColor("#8B3A3A"), "COMMON MISTAKE"),
        "memory": (PALE_GOLD, GOLD, "MEMORY AID"),
        "exam": (PALE_GREEN, colors.HexColor("#2D6A4F"), "EXAM TIP"),
        "why": (PALE, NAVY, "WHY THIS MATTERS"),
        "check": (PALE_GREEN, TEAL, "SELF-CHECK"),
        "note": (CREAM, NAVY, "TEACHER-TO-SELF NOTE"),
    }

    def __init__(self, styles, kind: str, body: str, title: str | None = None):
        super().__init__()
        self.styles = styles
        bg, accent, default_title = self.KINDS[kind]
        self.bg = bg
        self.accent = accent
        self.title = title or default_title
        self.body = body
        self._inner = None

    def wrap(self, availWidth, availHeight):
        self.width = availWidth
        inner_w = availWidth - 16
        title_p = Paragraph(self.title, self.styles["CalloutTitle"])
        body_p = Paragraph(self.body, self.styles["CalloutBody"])
        tw, th = title_p.wrap(inner_w, availHeight)
        bw, bh = body_p.wrap(inner_w, availHeight)
        self._inner = (title_p, body_p, th, bh)
        self.height = th + bh + 16
        return self.width, self.height

    def draw(self):
        title_p, body_p, th, bh = self._inner
        self.canv.setFillColor(self.bg)
        self.canv.roundRect(0, 0, self.width, self.height, 4, fill=1, stroke=0)
        self.canv.setFillColor(self.accent)
        self.canv.rect(0, 0, 4, self.height, fill=1, stroke=0)
        title_p.drawOn(self.canv, 12, self.height - 8 - th)
        body_p.drawOn(self.canv, 12, 8)


def p(styles, text, style="Body"):
    return Paragraph(text, styles[style])


def h1(styles, text):
    return KeepTogether([Spacer(1, 4), p(styles, text, "H1"), ColoredRule(GOLD, 1.6, 0, 8)])


def h2(styles, text):
    return p(styles, text, "H2")


def h3(styles, text):
    return p(styles, text, "H3")


def bullets(styles, items, bullet="•"):
    flow = []
    for item in items:
        flow.append(Paragraph(f"{bullet}  {item}", styles["Bullet"]))
    flow.append(Spacer(1, 4))
    return flow


def numbered(styles, items):
    flow = []
    for i, item in enumerate(items, 1):
        flow.append(Paragraph(f"<b>{i}.</b>  {item}", styles["Bullet"]))
    flow.append(Spacer(1, 4))
    return flow


def simple_table(styles, headers, rows, col_widths=None, center_cols=None):
    center_cols = center_cols or []
    head = [Paragraph(str(h), styles["TableHead"]) for h in headers]
    data = [head]
    for row in rows:
        cells = []
        for i, cell in enumerate(row):
            sty = styles["TableCellC"] if i in center_cols else styles["TableCell"]
            cells.append(Paragraph(str(cell), sty))
        data.append(cells)
    table = Table(data, colWidths=col_widths, repeatRows=1)
    cmds = [
        ("BACKGROUND", (0, 0), (-1, 0), NAVY),
        ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
        ("FONTNAME", (0, 0), (-1, 0), "Sans-Bold"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("GRID", (0, 0), (-1, -1), 0.3, LINE),
        ("ALIGN", (0, 0), (-1, 0), "CENTER"),
    ]
    for r in range(1, len(data)):
        if r % 2 == 0:
            cmds.append(("BACKGROUND", (0, r), (-1, r), PALE))
    table.setStyle(TableStyle(cmds))
    return table


def code_block(styles, code: str):
    lines = [Paragraph(line.replace(" ", "&nbsp;") if line.strip() else "&nbsp;", styles["Code"]) for line in code.splitlines()]
    if not lines:
        lines = [Paragraph("&nbsp;", styles["Code"])]
    inner = Table([[ln] for ln in lines], colWidths=[PAGE_W - LEFT - RIGHT - 12])
    inner.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#F4F6F8")),
                ("LEFTPADDING", (0, 0), (-1, -1), 8),
                ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                ("TOPPADDING", (0, 0), (-1, 0), 7),
                ("BOTTOMPADDING", (0, -1), (-1, -1), 7),
                ("BOX", (0, 0), (-1, -1), 0.6, TEAL),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ]
        )
    )
    return KeepTogether([inner, Spacer(1, 8)])


def two_col(left, right, widths=None):
    widths = widths or [(PAGE_W - LEFT - RIGHT) / 2] * 2
    t = Table([[left, right]], colWidths=widths)
    t.setStyle(
        TableStyle(
            [
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 0),
                ("RIGHTPADDING", (0, 0), (0, 0), 8),
                ("LEFTPADDING", (1, 0), (1, 0), 8),
            ]
        )
    )
    return t
