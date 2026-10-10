"""Custom sketchnote diagrams drawn on a SketchDoc canvas."""

import math
from reportlab.lib.colors import HexColor
from engine import INK, WHITE, TEAL, CORAL, NAVY, GOLD, SAGE, SKY, LAV, AMBER, MUTED, C


def _need(doc, h):
    doc.ensure(h)


def stairs_vs_ramp(doc):
    _need(doc, 118)
    c = doc.c
    y = doc.y - 86
    # stairs
    x0 = doc.L + 40
    c.setStrokeColor(NAVY)
    c.setFillColor(NAVY)
    c.setLineWidth(2)
    pts = [(x0, y), (x0, y + 18), (x0 + 22, y + 18), (x0 + 22, y + 36),
           (x0 + 44, y + 36), (x0 + 44, y + 54), (x0 + 66, y + 54)]
    p = c.beginPath()
    p.moveTo(*pts[0])
    for pt in pts[1:]:
        p.lineTo(*pt)
    c.drawPath(p, stroke=1, fill=0)
    c.setFillColor(INK)
    c.setFont("Note", 9)
    c.drawCentredString(x0 + 36, y - 12, "Discrete = stairs (fixed steps)")
    # arrow
    c.setStrokeColor(GOLD)
    c.setLineWidth(1.6)
    mid = doc.W / 2
    c.line(mid - 40, y + 30, mid + 30, y + 30)
    c.drawString(mid + 28, y + 26, "▸")
    # ramp
    x1 = doc.R - 160
    c.setStrokeColor(SAGE)
    c.setLineWidth(2.2)
    c.line(x1, y, x1 + 90, y + 58)
    c.setFillColor(INK)
    c.setFont("Note", 9)
    c.drawCentredString(x1 + 50, y - 12, "Continuous = ramp (any point)")
    doc.y = y - 36


def analog_digital_waves(doc):
    _need(doc, 150)
    c = doc.c
    box_h = 138
    y = doc.y - box_h
    doc.wobble_rect(doc.L, y, doc.usable, box_h, stroke=NAVY, fill=WHITE)
    # sine
    c.setStrokeColor(CORAL)
    c.setLineWidth(1.8)
    x0, y0, w, amp = doc.L + 40, y + 100, 220, 22
    p = c.beginPath()
    for i in range(0, 221):
        t = i / 220 * 2 * math.pi * 1.5
        px = x0 + i
        py = y0 + amp * math.sin(t)
        if i == 0:
            p.moveTo(px, py)
        else:
            p.lineTo(px, py)
    c.drawPath(p, stroke=1, fill=0)
    c.setStrokeColor(INK)
    c.setLineWidth(0.8)
    c.line(x0 - 8, y0, x0 + w + 8, y0)
    c.setFillColor(INK)
    c.setFont("Note", 9)
    c.drawString(x0, y + 128, "Analog  ·  sine wave  ·  V vs t")
    # square
    c.setStrokeColor(SKY)
    c.setLineWidth(1.8)
    x1, y1 = doc.L + 310, y + 46
    bits = [1, 0, 1, 1, 0, 1]
    bw = 28
    p = c.beginPath()
    p.moveTo(x1, y1)
    for i, b in enumerate(bits):
        yy = y1 + 28 if b else y1
        p.lineTo(x1 + i * bw, yy)
        p.lineTo(x1 + (i + 1) * bw, yy)
    c.drawPath(p, stroke=1, fill=0)
    c.setStrokeColor(INK)
    c.setLineWidth(0.8)
    c.line(x1 - 6, y1, x1 + bw * len(bits) + 8, y1)
    c.setFont("Note", 8)
    c.drawString(x1 + bw * 0 + 4, y1 + 32, "HIGH 1")
    c.drawString(x1 + bw + 4, y1 - 12, "LOW 0")
    c.setFont("Note", 9)
    c.drawString(x1, y + 128, "Digital  ·  square wave  ·  only 0 / 1")
    doc.y = y - 10


def _gate_and(c, x, y, s=28):
    c.setStrokeColor(INK)
    c.setLineWidth(1.6)
    c.setFillColor(WHITE)
    p = c.beginPath()
    p.moveTo(x, y)
    p.lineTo(x, y + s)
    p.lineTo(x + s * 0.45, y + s)
    # arc
    p.arcTo(x + s * 0.05, y, x + s * 0.95, y + s, 90, -180)
    p.lineTo(x, y)
    c.drawPath(p, stroke=1, fill=1)
    c.line(x - 14, y + s * 0.28, x, y + s * 0.28)
    c.line(x - 14, y + s * 0.72, x, y + s * 0.72)
    c.line(x + s * 0.95, y + s * 0.5, x + s + 14, y + s * 0.5)


def _gate_or(c, x, y, s=28):
    c.setStrokeColor(INK)
    c.setLineWidth(1.6)
    c.setFillColor(WHITE)
    p = c.beginPath()
    p.moveTo(x, y)
    p.curveTo(x + 6, y + s * 0.25, x + 6, y + s * 0.75, x, y + s)
    p.curveTo(x + s * 0.55, y + s, x + s, y + s * 0.7, x + s, y + s * 0.5)
    p.curveTo(x + s, y + s * 0.3, x + s * 0.55, y, x, y)
    c.drawPath(p, stroke=1, fill=1)
    c.line(x - 12, y + s * 0.28, x + 5, y + s * 0.28)
    c.line(x - 12, y + s * 0.72, x + 5, y + s * 0.72)
    c.line(x + s, y + s * 0.5, x + s + 14, y + s * 0.5)


def _bubble(c, x, y, r=3.4):
    c.setFillColor(WHITE)
    c.setStrokeColor(INK)
    c.circle(x, y, r, fill=1, stroke=1)


def logic_gates_basic(doc):
    _need(doc, 88)
    c = doc.c
    y = doc.y - 78
    labels = [("AND  Y=A·B", _gate_and, 0), ("OR  Y=A+B", _gate_or, 1), ("NOT  Y=A'", None, 2)]
    xs = [doc.L + 50, doc.L + 230, doc.L + 410]
    for (lab, fn, kind), x in zip(labels, xs):
        if kind == 2:
            c.setStrokeColor(INK)
            c.setLineWidth(1.6)
            c.setFillColor(WHITE)
            p = c.beginPath()
            p.moveTo(x, y + 8)
            p.lineTo(x, y + 44)
            p.lineTo(x + 28, y + 26)
            p.close()
            c.drawPath(p, stroke=1, fill=1)
            _bubble(c, x + 32, y + 26)
            c.line(x - 14, y + 26, x, y + 26)
            c.line(x + 36, y + 26, x + 50, y + 26)
        else:
            fn(c, x, y + 10, 36)
        c.setFillColor(INK)
        c.setFont("Note", 9)
        c.drawCentredString(x + 18, y - 4, lab)
    doc.y = y - 16


def logic_gates_universal(doc):
    _need(doc, 80)
    c = doc.c
    y = doc.y - 70
    # NAND
    _gate_and(c, doc.L + 80, y + 10, 36)
    _bubble(c, doc.L + 80 + 36, y + 10 + 18)
    c.setFillColor(INK)
    c.setFont("Note", 9)
    c.drawCentredString(doc.L + 100, y - 4, "NAND  Y=(A·B)'   universal")
    # NOR
    _gate_or(c, doc.L + 320, y + 10, 36)
    _bubble(c, doc.L + 320 + 38, y + 10 + 18)
    c.drawCentredString(doc.L + 340, y - 4, "NOR  Y=(A+B)'   universal")
    doc.y = y - 16


def osi_stack(doc):
    _need(doc, 210)
    c = doc.c
    layers = [
        (7, "Application", "HTTP HTTPS FTP SMTP DNS  ·  services for the user", C("#6B4C9A")),
        (6, "Presentation", "SSL/TLS  JPEG MP3 ASCII  ·  translate, encrypt, compress", C("#2F6F9A")),
        (5, "Session", "NetBIOS RPC  ·  open / maintain / close sessions", C("#1B7A6E")),
        (4, "Transport", "TCP reliable  ·  UDP fast  ·  ports + end-to-end", C("#4F8A4A")),
        (3, "Network", "IP ICMP routers  ·  logical address + routing", C("#C46A12")),
        (2, "Data Link", "Ethernet MAC switches  ·  frames + MAC address", C("#D4543C")),
        (1, "Physical", "Cables hubs Wi-Fi radio  ·  raw bits 0/1", C("#1E3A5F")),
    ]
    h = 24
    y = doc.y
    for n, name, detail, col in layers:
        y -= h + 3
        c.setFillColor(col)
        c.roundRect(doc.L, y, 78, h, 5, fill=1, stroke=0)
        c.setFillColor(WHITE)
        c.setFont("Head", 10)
        c.drawCentredString(doc.L + 39, y + 8, f"{n}  {name[:4].upper()}" if False else str(n))
        c.setFont("Note", 8)
        c.drawCentredString(doc.L + 39, y + 8, str(n))
        c.setFillColor(WHITE)
        c.setStrokeColor(col)
        c.setLineWidth(1.2)
        c.roundRect(doc.L + 86, y, doc.usable - 86, h, 5, fill=1, stroke=1)
        c.setFillColor(col)
        c.setFont("HeadReg", 10)
        c.drawString(doc.L + 94, y + 12, name)
        c.setFillColor(INK)
        c.setFont("Body", 8.5)
        c.drawString(doc.L + 94, y + 3, detail[:78])
    doc.y = y - 12


def kmap2(doc):
    _need(doc, 110)
    c = doc.c
    cells = [
        ["A\\B", "B=0", "B=1"],
        ["A=0", "0  A'B'", "1  A'B"],
        ["A=1", "2  AB'", "3  AB"],
    ]
    y = doc.y - 100
    cw, ch = 90, 28
    x0 = doc.L + 80
    for r, row in enumerate(cells):
        for col, val in enumerate(row):
            x = x0 + col * cw
            yy = y + (2 - r) * ch
            if r == 0 or col == 0:
                c.setFillColor(NAVY)
                c.setFillColor(NAVY if (r == 0 or col == 0) else WHITE)
                c.rect(x, yy, cw, ch, fill=1, stroke=1)
                c.setFillColor(WHITE)
            else:
                c.setFillColor(C("#FFF4D0"))
                c.setStrokeColor(INK)
                c.rect(x, yy, cw, ch, fill=1, stroke=1)
                c.setFillColor(INK)
            c.setFont("Note", 8)
            c.setFillColor(WHITE if (r == 0 or col == 0) else INK)
            c.drawCentredString(x + cw / 2, yy + 10, val)
    c.setFillColor(INK)
    c.setFont("Note", 9)
    c.drawString(doc.L, y - 8, "2-var K-map: 4 cells. Adjacent cells differ by ONE bit (Gray code).")
    doc.y = y - 20


def kmap3(doc):
    _need(doc, 120)
    c = doc.c
    headers = ["A\\BC", "00", "01", "11", "10"]
    body = [
        ["A=0", "m0 A'B'C'", "m1 A'B'C", "m3 A'BC", "m2 A'BC'"],
        ["A=1", "m4 AB'C'", "m5 AB'C", "m7 ABC", "m6 ABC'"],
    ]
    cw, ch = 88, 30
    x0 = doc.L + 20
    y = doc.y - 18
    for i, h in enumerate(headers):
        c.setFillColor(LAV)
        c.rect(x0 + i * cw, y - ch, cw, ch, fill=1, stroke=1)
        c.setFillColor(WHITE)
        c.setFont("Note", 8)
        c.drawCentredString(x0 + i * cw + cw / 2, y - 20, h)
    y -= ch
    for r, row in enumerate(body):
        for i, val in enumerate(row):
            c.setFillColor(LAV if i == 0 else C("#F3E9FF"))
            c.rect(x0 + i * cw, y - ch, cw, ch, fill=1, stroke=1)
            c.setFillColor(WHITE if i == 0 else INK)
            c.setFont("Note", 7.4)
            c.drawCentredString(x0 + i * cw + cw / 2, y - 18, val)
        y -= ch
    c.setFillColor(INK)
    c.setFont("Note", 9)
    c.drawString(doc.L, y - 8, "Gray columns 00-01-11-10. Edges WRAP: far-left groups with far-right.")
    doc.y = y - 20


def sdlc_ring(doc):
    labels = [
        "1 Requirement\nSRS",
        "2 Design\nHLD + LLD",
        "3 Implement\nSource code",
        "4 Testing\nBug reports",
        "5 Deploy\nLive software",
        "6 Maintain\nPatches",
    ]
    _need(doc, 150)
    c = doc.c
    cx, cy, r = doc.W / 2, doc.y - 70, 52
    c.setStrokeColor(AMBER)
    c.setLineWidth(2)
    c.circle(cx, cy, r, fill=0, stroke=1)
    c.setFillColor(AMBER)
    c.setFont("Head", 11)
    c.drawCentredString(cx, cy - 4, "SDLC")
    for i, lab in enumerate(labels):
        ang = math.radians(-90 + i * 60)
        x = cx + 88 * math.cos(ang)
        y = cy + 52 * math.sin(ang)
        c.setFillColor(WHITE)
        c.setStrokeColor(AMBER)
        c.roundRect(x - 48, y - 16, 96, 28, 6, fill=1, stroke=1)
        c.setFillColor(INK)
        c.setFont("Note", 7.2)
        parts = lab.split("\n")
        c.drawCentredString(x, y + 2, parts[0])
        if len(parts) > 1:
            c.drawCentredString(x, y - 9, parts[1])
    doc.y -= 150


def sensory_hci(doc):
    _need(doc, 100)
    c = doc.c
    cx, cy = doc.W / 2, doc.y - 48
    c.setFillColor(C("#F6D6E4"))
    c.circle(cx, cy, 28, fill=1, stroke=0)
    c.setFillColor(ROSE := C("#B83B6A"))
    c.setFont("Head", 11)
    c.drawCentredString(cx, cy - 4, "HUMAN")
    nodes = [
        (-190, 18, "Sight", "screens / graphics"),
        (-80, 40, "Touch", "tap · type · swipe"),
        (80, 40, "Hearing", "sound / voice"),
        (190, 18, "Voice", "Alexa commands"),
        (0, -48, "Spatial", "VR · body tracking"),
    ]
    for dx, dy, t, d in nodes:
        x, y = cx + dx, cy + dy
        c.setStrokeColor(C("#B83B6A"))
        c.setLineWidth(1)
        c.line(cx, cy, x, y)
        c.setFillColor(WHITE)
        c.roundRect(x - 46, y - 14, 92, 26, 6, fill=1, stroke=1)
        c.setFillColor(INK)
        c.setFont("HeadReg", 8)
        c.drawCentredString(x, y + 2, t)
        c.setFont("Note", 6.5)
        c.drawCentredString(x, y - 8, d)
    doc.y -= 108


def stack_queue(doc):
    _need(doc, 130)
    c = doc.c
    # stack
    x = doc.L + 40
    y = doc.y - 110
    c.setFont("HeadReg", 11)
    c.setFillColor(AMBER)
    c.drawString(x, doc.y - 8, "STACK  ·  LIFO")
    for i, lab in enumerate(["Data 3  TOP", "Data 2", "Data 1"]):
        c.setFillColor(C("#F8E2C4"))
        c.setStrokeColor(AMBER)
        c.roundRect(x, y + i * 26, 100, 22, 4, fill=1, stroke=1)
        c.setFillColor(INK)
        c.setFont("Note", 8)
        c.drawCentredString(x + 50, y + i * 26 + 7, lab)
    c.setFont("Note", 8)
    c.drawString(x + 110, y + 70, "PUSH adds to top")
    c.drawString(x + 110, y + 56, "POP removes top")
    c.drawString(x + 110, y + 42, "Undo in editors")
    # queue
    x2 = doc.L + 300
    c.setFillColor(SKY)
    c.setFont("HeadReg", 11)
    c.drawString(x2, doc.y - 8, "QUEUE  ·  FIFO")
    for i, lab in enumerate(["55 FRONT", "76", "90 REAR"]):
        c.setFillColor(C("#D4EAF8"))
        c.setStrokeColor(SKY)
        c.roundRect(x2 + i * 70, y + 30, 64, 36, 5, fill=1, stroke=1)
        c.setFillColor(INK)
        c.setFont("Note", 8)
        c.drawCentredString(x2 + i * 70 + 32, y + 44, lab)
    c.setFont("Note", 8)
    c.drawString(x2, y + 10, "ENQUEUE → rear     DEQUEUE ← front     printer jobs")
    doc.y = y - 16


def linked_list(doc):
    _need(doc, 70)
    c = doc.c
    y = doc.y - 40
    vals = ["HEAD", "23", "76", "12", "90", "NULL"]
    x = doc.L + 10
    for i, v in enumerate(vals):
        c.setFillColor(C("#DCEFCF") if v not in ("HEAD", "NULL") else WHITE)
        c.setStrokeColor(SAGE)
        c.roundRect(x, y, 62, 28, 5, fill=1, stroke=1)
        c.setFillColor(INK)
        c.setFont("Note", 8)
        c.drawCentredString(x + 31, y + 10, v)
        if i < len(vals) - 1:
            c.setStrokeColor(SAGE)
            c.line(x + 62, y + 14, x + 74, y + 14)
            c.drawString(x + 70, y + 10, "▸")
        x += 86
    doc.y = y - 18


def org_tree(doc):
    _need(doc, 120)
    c = doc.c
    y = doc.y - 16

    def box(x, yy, w, h, text, col):
        c.setFillColor(WHITE)
        c.setStrokeColor(col)
        c.roundRect(x - w / 2, yy, w, h, 5, fill=1, stroke=1)
        c.setFillColor(INK)
        c.setFont("Note", 7.5)
        c.drawCentredString(x, yy + 8, text)
        return x, yy

    root = box(doc.W / 2, y - 22, 120, 22, "Principal (Root)", LAV)
    c.setStrokeColor(LAV)
    c.line(doc.W / 2, y - 22, doc.W / 2, y - 36)
    c.line(doc.L + 120, y - 36, doc.R - 120, y - 36)
    left = box(doc.L + 160, y - 58, 130, 22, "Administrative Head", SKY)
    right = box(doc.R - 160, y - 58, 120, 22, "Academic Dean", SKY)
    c.line(doc.L + 160, y - 36, doc.L + 160, y - 58)
    c.line(doc.R - 160, y - 36, doc.R - 160, y - 58)
    kids_l = ["Accounts", "HR"]
    kids_r = ["HOD Math", "HOD CS"]
    for i, t in enumerate(kids_l):
        xx = doc.L + 100 + i * 120
        c.line(doc.L + 160, y - 58, xx, y - 78)
        box(xx, y - 100, 90, 20, t, SAGE)
    for i, t in enumerate(kids_r):
        xx = doc.R - 220 + i * 120
        c.line(doc.R - 160, y - 58, xx, y - 78)
        box(xx, y - 100, 90, 20, t, SAGE)
    doc.y = y - 124


def neural_net(doc):
    _need(doc, 130)
    c = doc.c
    layers = [3, 4, 4, 2]
    names = ["Input", "Hidden", "Hidden", "Output"]
    xs = [doc.L + 70 + i * 130 for i in range(4)]
    y0 = doc.y - 100
    coords = []
    for li, n in enumerate(layers):
        col = []
        for j in range(n):
            yy = y0 + 80 - j * (80 / max(n - 1, 1))
            col.append((xs[li], yy))
        coords.append(col)
    c.setStrokeColor(C("#D8C8E8"))
    c.setLineWidth(0.7)
    for a, b in zip(coords, coords[1:]):
        for x1, y1 in a:
            for x2, y2 in b:
                c.line(x1, y1, x2, y2)
    for li, col in enumerate(coords):
        for x, y in col:
            c.setFillColor(LAV if li in (1, 2) else (NAVY if li == 0 else CORAL))
            c.circle(x, y, 7, fill=1, stroke=0)
        c.setFillColor(INK)
        c.setFont("Note", 8)
        c.drawCentredString(xs[li], y0 - 8, names[li])
    doc.y = y0 - 22


def prototype_cycle(doc):
    labels = ["1 Design", "2 Build", "3 Test", "4 Iterate"]
    _need(doc, 100)
    c = doc.c
    cx, cy, r = doc.W / 2, doc.y - 48, 34
    c.setStrokeColor(AMBER)
    c.setLineWidth(2.2)
    c.circle(cx, cy, r, stroke=1, fill=0)
    c.setFillColor(AMBER)
    c.setFont("Head", 10)
    c.drawCentredString(cx, cy - 3, "cycle")
    for i, lab in enumerate(labels):
        ang = math.radians(-90 + i * 90)
        x = cx + 78 * math.cos(ang)
        y = cy + 40 * math.sin(ang)
        c.setFillColor(C("#F8E2C4"))
        c.setStrokeColor(AMBER)
        c.roundRect(x - 40, y - 12, 80, 24, 7, fill=1, stroke=1)
        c.setFillColor(INK)
        c.setFont("Note", 8)
        c.drawCentredString(x, y - 3, lab)
    doc.y -= 104


def iot_loop(doc):
    labels = ["Sensor\ncollects", "Wi-Fi\nconnects", "Cloud\nprocesses", "Actuator\nacts", "User app\nUI"]
    doc.flow(labels)


def er_symbols(doc):
    _need(doc, 80)
    c = doc.c
    y = doc.y - 60
    # rectangle entity
    c.setStrokeColor(NAVY)
    c.setFillColor(NAVY_BG := C("#D6E4F5"))
    c.rect(doc.L + 20, y, 90, 32, fill=1, stroke=1)
    c.setFillColor(INK)
    c.setFont("Note", 9)
    c.drawCentredString(doc.L + 65, y + 12, "STUDENT")
    c.drawCentredString(doc.L + 65, y - 12, "Entity  ▭")
    # oval attribute
    c.setFillColor(C("#DCEFCF"))
    c.setStrokeColor(SAGE)
    c.ellipse(doc.L + 150, y - 2, doc.L + 250, y + 34, fill=1, stroke=1)
    c.setFillColor(INK)
    c.drawCentredString(doc.L + 200, y + 12, "Name")
    c.drawCentredString(doc.L + 200, y - 12, "Attribute  ○")
    # diamond
    c.setFillColor(C("#F8E2C4"))
    c.setStrokeColor(AMBER)
    p = c.beginPath()
    cx, cy = doc.L + 340, y + 16
    p.moveTo(cx, cy + 20)
    p.lineTo(cx + 50, cy)
    p.lineTo(cx, cy - 20)
    p.lineTo(cx - 50, cy)
    p.close()
    c.drawPath(p, fill=1, stroke=1)
    c.setFillColor(INK)
    c.drawCentredString(cx, cy - 3, "Enrolls")
    c.drawCentredString(cx, y - 12, "Relationship  ◇")
    # underline note
    c.setFont("Note", 8)
    c.drawString(doc.L + 420, y + 12, "PK attribute")
    c.drawString(doc.L + 420, y + 2, "gets an underline")
    doc.y = y - 24


def binary_search_strip(doc):
    _need(doc, 70)
    c = doc.c
    vals = [1, 2, 3, 4, 5, 6, 7, 8]
    w = 36
    x0 = doc.L + 40
    y = doc.y - 40
    for i, v in enumerate(vals):
        fill = C("#FFE9A8") if v == 4 else WHITE
        if v == 3:
            fill = C("#DCEFCF")
        c.setFillColor(fill)
        c.setStrokeColor(INK)
        c.roundRect(x0 + i * w, y, w - 4, 28, 4, fill=1, stroke=1)
        c.setFillColor(INK)
        c.setFont("Head", 11)
        c.drawCentredString(x0 + i * w + (w - 4) / 2, y + 9, str(v))
    c.setFont("Note", 8)
    c.drawString(x0 + 3 * w, y + 32, "MID=4  → 3 < 4 go left")
    c.drawString(x0 + 2 * w, y - 12, "found 3 after two more splits")
    doc.y = y - 22
