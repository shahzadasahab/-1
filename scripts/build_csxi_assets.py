#!/usr/bin/env python3
"""Render booklet diagram pages and generate exam-ready CS XI diagrams."""

from __future__ import annotations

from pathlib import Path

import pymupdf
from PIL import Image, ImageDraw, ImageFont

ROOT = Path("/workspace")
ASSETS = ROOT / "app/src/main/assets"
DIAG = ASSETS / "diagrams"
BOOK = ASSETS / "booklet"
UPLOADS = Path("/home/ubuntu/.cursor/projects/workspace/uploads")
VOL1 = UPLOADS / "CS-XI_Units-1-4_Teach-Yourself-Booklet_Bilingual_Teachers-Edition_Vol1-compressed_3836.pdf"
VOL2 = UPLOADS / "CS-XI_Units-5-6_Teach-Yourself-Booklet_Bilingual_Teachers-Edition-compressed_6563.pdf"

# Lesson pages that carry Learn + diagram figures (1-based).
VOL1_PAGES = list(range(8, 23)) + list(range(29, 37)) + list(range(42, 53)) + list(range(59, 70))
VOL2_PAGES = list(range(7, 28)) + list(range(36, 52))

NAVY = (11, 46, 92)
TEAL = (15, 118, 110)
GOLD = (180, 120, 32)
INK = (28, 35, 48)
MUTED = (90, 100, 118)
LINE = (200, 208, 220)
PAPER = (248, 250, 253)
WHITE = (255, 255, 255)
RED = (185, 48, 64)
GREEN = (32, 128, 88)
BLUE = (37, 99, 180)
PURPLE = (109, 40, 160)
ORANGE = (194, 92, 20)
SKY = (224, 242, 254)
MINT = (209, 250, 229)
CREAM = (254, 243, 199)
LAV = (237, 233, 254)
ROSE = (254, 226, 226)


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    candidates = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
    ]
    for path in candidates:
        if Path(path).exists():
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


F14, F16, F18, F20, F22, F26, F30 = (font(n) for n in (14, 16, 18, 20, 22, 26, 30))
FB16, FB18, FB20, FB22, FB26, FB32, FB40 = (font(n, True) for n in (16, 18, 20, 22, 26, 32, 40))


def canvas(w: int, h: int, bg=PAPER) -> tuple[Image.Image, ImageDraw.ImageDraw]:
    img = Image.new("RGB", (w, h), bg)
    return img, ImageDraw.Draw(img)


def save(img: Image.Image, name: str) -> None:
    dest = DIAG / f"{name}.png"
    img.save(dest, "PNG", optimize=True)
    print(f"  diagram {dest.name} {img.size} {dest.stat().st_size // 1024}KB")


def rounded(draw, box, fill, outline=None, radius=16, width=2):
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def title_bar(draw, w, text, sub=""):
    draw.rectangle((0, 0, w, 64), fill=NAVY)
    draw.text((24, 16), text, fill=WHITE, font=FB26)
    if sub:
        draw.text((24, 44), sub, fill=(180, 210, 255), font=F14)


def render_booklet() -> None:
    BOOK.mkdir(parents=True, exist_ok=True)
    jobs = [(VOL1, "v1", VOL1_PAGES), (VOL2, "v2", VOL2_PAGES)]
    for pdf, prefix, pages in jobs:
        doc = pymupdf.open(pdf)
        for num in pages:
            page = doc[num - 1]
            pix = page.get_pixmap(matrix=pymupdf.Matrix(1.55, 1.55), alpha=False)
            raw = pix.tobytes("png")
            img = Image.open(__import__("io").BytesIO(raw)).convert("RGB")
            dest = BOOK / f"{prefix}_p{num:02d}.jpg"
            img.save(dest, "JPEG", quality=80, optimize=True)
            print(f"  booklet {dest.name} {img.size} {dest.stat().st_size // 1024}KB")


def diag_cover():
    img, d = canvas(1200, 720, NAVY)
    d.rectangle((0, 560, 1200, 720), fill=TEAL)
    d.text((48, 48), "SINDH CURRICULUM 2026", fill=GOLD, font=FB20)
    d.text((48, 110), "CS XI Ultimate Coaching", fill=WHITE, font=FB40)
    d.text((48, 180), "Computer Science  ·  Class XI  ·  Units 1–6", fill=(200, 220, 255), font=F22)
    d.text((48, 230), "Urdish TTS coach  ·  Embedded booklet diagrams  ·  Mock tests", fill=(180, 210, 200), font=F18)
    chips = [
        (48, 320, "Logic Gates"),
        (250, 320, "Algorithms"),
        (452, 320, "Python"),
        (620, 320, "Databases"),
        (820, 320, "IoT · AI"),
        (1000, 320, "OSI"),
    ]
    for x, y, t in chips:
        rounded(d, (x, y, x + 180, y + 48), TEAL, radius=24)
        d.text((x + 16, y + 12), t, fill=WHITE, font=FB16)
    d.text((48, 600), "خود آموز کوچ  ·  Teach-yourself coaching in Urdish", fill=WHITE, font=FB20)
    d.text((48, 650), "Independent study aid  ·  Not an official STB publication", fill=(210, 230, 230), font=F16)
    save(img, "cover")


def diag_analog_digital():
    img, d = canvas(1200, 780)
    title_bar(d, 1200, "Figure · Analog vs Digital", "Continuous wave  ·  Discrete bits")
    rounded(d, (40, 90, 580, 430), SKY, NAVY, 18)
    d.text((60, 104), "Analog signal  ·  مسلسل", fill=NAVY, font=FB20)
    pts = []
    for i in range(480):
        x = 70 + i
        y = 270 - int(70 * __import__("math").sin(i / 28))
        pts.append((x, y))
    d.line(pts, fill=BLUE, width=4)
    d.line((70, 360, 540, 360), fill=MUTED, width=2)
    d.text((70, 380), "any value in a range · smooth sine wave", fill=MUTED, font=F16)

    rounded(d, (620, 90, 1160, 430), MINT, TEAL, 18)
    d.text((640, 104), "Digital signal  ·  منقطع", fill=TEAL, font=FB20)
    wave = [(650, 300), (650, 180), (780, 180), (780, 300), (910, 300), (910, 180), (1040, 180), (1040, 300), (1130, 300)]
    d.line(wave, fill=GREEN, width=4)
    d.line((650, 360, 1130, 360), fill=MUTED, width=2)
    d.text((650, 380), "only HIGH (1) or LOW (0) · square wave", fill=MUTED, font=F16)

    rounded(d, (40, 460, 580, 740), CREAM, GOLD, 18)
    d.line([(80, 680), (160, 680), (160, 620), (240, 620), (240, 560), (320, 560), (320, 500), (400, 500)], fill=ORANGE, width=5)
    d.text((80, 480), "Stairs = digital", fill=ORANGE, font=FB20)
    d.text((80, 700), "only fixed steps: 0 or 1", fill=INK, font=F16)

    rounded(d, (620, 460, 1160, 740), LAV, PURPLE, 18)
    d.line([(680, 680), (1100, 500)], fill=PURPLE, width=5)
    d.text((660, 480), "Ramp = analog", fill=PURPLE, font=FB20)
    d.text((660, 700), "any height in the range", fill=INK, font=F16)
    save(img, "analog_digital")


def gate_and(d, x, y, w=140, h=90):
    d.polygon([(x, y), (x + w * 0.45, y), (x + w, y + h / 2), (x + w * 0.45, y + h), (x, y + h)], outline=NAVY, fill=SKY)
    d.line((x - 28, y + 22, x, y + 22), fill=NAVY, width=3)
    d.line((x - 28, y + 68, x, y + 68), fill=NAVY, width=3)
    d.line((x + w, y + h / 2, x + w + 28, y + h / 2), fill=NAVY, width=3)


def gate_or(d, x, y, w=140, h=90):
    d.arc((x - 30, y, x + 30, y + h), 270, 90, fill=NAVY, width=3)
    d.arc((x - 70, y - 10, x + w, y + h + 10), 270, 90, fill=NAVY, width=3)
    d.line((x - 28, y + 22, x + 8, y + 22), fill=NAVY, width=3)
    d.line((x - 28, y + 68, x + 8, y + 68), fill=NAVY, width=3)
    d.line((x + w - 8, y + h / 2, x + w + 28, y + h / 2), fill=NAVY, width=3)


def gate_not(d, x, y):
    d.polygon([(x, y), (x + 90, y + 36), (x, y + 72)], outline=NAVY, fill=ROSE)
    d.ellipse((x + 90, y + 28, x + 110, y + 48), outline=NAVY, fill=WHITE, width=2)
    d.line((x - 28, y + 36, x, y + 36), fill=NAVY, width=3)
    d.line((x + 110, y + 36, x + 138, y + 36), fill=NAVY, width=3)


def diag_logic_gates():
    img, d = canvas(1200, 900)
    title_bar(d, 1200, "Figure 1.2 · The seven logic gates", "Symbol · expression · rule")
    cards = [
        (40, 90, "AND", "Y = A · B", "1 only if ALL inputs are 1", SKY, NAVY),
        (320, 90, "OR", "Y = A + B", "1 if ANY input is 1", MINT, TEAL),
        (600, 90, "NOT", "Y = A'", "inverts the input", ROSE, RED),
        (880, 90, "NAND", "Y = (A · B)'", "0 only if ALL are 1", CREAM, GOLD),
        (40, 430, "NOR", "Y = (A + B)'", "1 only if ALL are 0", LAV, PURPLE),
        (320, 430, "XOR", "Y = A ⊕ B", "1 if inputs DIFFER", SKY, BLUE),
        (600, 430, "XNOR", "Y = (A ⊕ B)'", "1 if inputs SAME", MINT, GREEN),
        (880, 430, "Universal", "NAND · NOR", "any gate from one of them", CREAM, ORANGE),
    ]
    for x, y, name, expr, rule, fill, edge in cards:
        rounded(d, (x, y, x + 260, y + 300), fill, edge, 16)
        d.text((x + 16, y + 16), name, fill=edge, font=FB26)
        d.text((x + 16, y + 200), expr, fill=INK, font=FB18)
        d.text((x + 16, y + 236), rule, fill=MUTED, font=F16)
    # simple gate sketches
    gate_and(d, 90, 180)
    d.text((56, 196), "A", fill=INK, font=F14)
    d.text((56, 242), "B", fill=INK, font=F14)
    d.text((250, 214), "Y", fill=INK, font=F14)
    gate_or(d, 370, 180)
    gate_not(d, 660, 190)
    gate_and(d, 930, 180)
    d.ellipse((1072, 216, 1092, 236), outline=NAVY, fill=WHITE, width=2)
    save(img, "logic_gates")


def diag_truth_tables():
    img, d = canvas(1200, 720)
    title_bar(d, 1200, "Truth table of all 2-input gates", "Plus NOT inverter")
    headers = ["A", "B", "AND", "OR", "NAND", "NOR", "XOR", "XNOR"]
    rows = [
        [0, 0, 0, 0, 1, 1, 0, 1],
        [0, 1, 0, 1, 1, 0, 1, 0],
        [1, 0, 0, 1, 1, 0, 1, 0],
        [1, 1, 1, 1, 0, 0, 0, 1],
    ]
    x0, y0, cw, rh = 40, 100, 110, 70
    for i, h in enumerate(headers):
        rounded(d, (x0 + i * cw, y0, x0 + (i + 1) * cw - 6, y0 + rh - 6), NAVY, radius=8)
        d.text((x0 + i * cw + 18, y0 + 20), h, fill=WHITE, font=FB18)
    for r, row in enumerate(rows):
        for c, val in enumerate(row):
            bg = MINT if val == 1 and c > 1 else (ROSE if val == 0 and c > 1 else WHITE)
            box = (x0 + c * cw, y0 + (r + 1) * rh, x0 + (c + 1) * cw - 6, y0 + (r + 2) * rh - 6)
            rounded(d, box, bg, LINE, 8)
            d.text((box[0] + 42, box[1] + 20), str(val), fill=INK, font=FB22)
    rounded(d, (940, 100, 1160, 280), LAV, PURPLE, 12)
    d.text((960, 116), "NOT", fill=PURPLE, font=FB22)
    d.text((960, 160), "A=0 → Y=1", fill=INK, font=F18)
    d.text((960, 200), "A=1 → Y=0", fill=INK, font=F18)
    d.text((40, 520), "Memory trick: XOR = exclusively different   ·   XNOR = same", fill=NAVY, font=FB20)
    d.text((40, 570), "Rows for n inputs = 2ⁿ     2 inputs → 4 rows     3 inputs → 8 rows", fill=MUTED, font=F18)
    d.text((40, 620), "AND = car key AND start button     OR = front OR back door alarm", fill=MUTED, font=F18)
    save(img, "truth_tables")


def diag_logic_circuit():
    img, d = canvas(1200, 680)
    title_bar(d, 1200, "Logic diagram  ·  Y = (A + B) · C'", "Precedence: ( )  →  NOT  →  AND  →  OR")
    d.text((60, 120), "A", fill=INK, font=FB22)
    d.text((60, 220), "B", fill=INK, font=FB22)
    d.text((60, 400), "C", fill=INK, font=FB22)
    gate_or(d, 160, 140)
    d.text((180, 250), "A + B", fill=MUTED, font=F16)
    gate_not(d, 160, 380)
    d.text((180, 470), "C'", fill=MUTED, font=F16)
    gate_and(d, 460, 240)
    d.text((700, 270), "Y", fill=NAVY, font=FB32)
    d.line((328, 185, 460, 262), fill=NAVY, width=3)
    d.line((298, 416, 400, 416), fill=NAVY, width=3)
    d.line((400, 416, 400, 308), fill=NAVY, width=3)
    d.line((400, 308, 460, 308), fill=NAVY, width=3)
    rounded(d, (40, 540, 1160, 650), CREAM, GOLD, 12)
    d.text((60, 560), "SOP from 1s (minterms): Y = A'B + AB     POS from 0s (maxterms)", fill=INK, font=FB18)
    d.text((60, 600), "Exam method: list 2ⁿ rows in binary order, add a column for each part, then final Y.", fill=MUTED, font=F16)
    save(img, "logic_circuit")


def diag_kmap():
    img, d = canvas(1200, 720)
    title_bar(d, 1200, "Karnaugh map and LogiSim", "Group 1s in powers of 2  ·  then simulate")
    rounded(d, (40, 100, 560, 560), WHITE, NAVY, 16)
    d.text((60, 120), "2-variable K-map for Y", fill=NAVY, font=FB22)
    cells = [("A\\B", 80, 200), ("0", 220, 200), ("1", 360, 200), ("0", 80, 320), ("1", 80, 440)]
    for t, x, y in cells:
        d.text((x, y), t, fill=MUTED, font=FB20)
    values = [(220, 320, "0"), (360, 320, "1"), (220, 440, "1"), (360, 440, "1")]
    for x, y, t in values:
        rounded(d, (x - 20, y - 16, x + 80, y + 64), MINT if t == "1" else ROSE, TEAL, 10)
        d.text((x + 16, y + 8), t, fill=INK, font=FB32)
    d.ellipse((330, 300, 470, 530), outline=GOLD, width=4)
    d.text((60, 590), "Largest group of 1s → Y = A + B", fill=GOLD, font=FB20)

    rounded(d, (600, 100, 1160, 680), SKY, BLUE, 16)
    d.text((630, 120), "LogiSim lab loop", fill=NAVY, font=FB22)
    steps = [
        "1  Place inputs A, B, C",
        "2  Drop gates (AND / OR / NOT)",
        "3  Wire expression exactly",
        "4  Add an output pin Y",
        "5  Toggle every input row",
        "6  Tick the truth table on paper",
    ]
    for i, s in enumerate(steps):
        rounded(d, (640, 180 + i * 70, 1120, 236 + i * 70), WHITE, BLUE, 10)
        d.text((660, 196 + i * 70), s, fill=INK, font=FB18)
    save(img, "kmap_logisim")


def diag_sdlc():
    img, d = canvas(1200, 720)
    title_bar(d, 1200, "Figure 1.5 · SDLC six phases", "Feedback: bugs and new requests start the next cycle")
    phases = [
        ("1", "Requirement\nAnalysis", "SRS", SKY),
        ("2", "System\nDesign", "Design doc", LAV),
        ("3", "Implementation\n(coding)", "Working code", MINT),
        ("4", "Testing", "Test reports", CREAM),
        ("5", "Deployment", "Live software", ROSE),
        ("6", "Maintenance", "Updates", SKY),
    ]
    for i, (n, name, deliver, fill) in enumerate(phases):
        x = 40 + (i % 3) * 380
        y = 110 + (i // 3) * 260
        rounded(d, (x, y, x + 350, y + 220), fill, NAVY, 16)
        d.ellipse((x + 16, y + 16, x + 64, y + 64), fill=NAVY)
        d.text((x + 30, y + 26), n, fill=WHITE, font=FB22)
        d.text((x + 80, y + 24), name, fill=NAVY, font=FB20)
        d.text((x + 24, y + 160), f"Deliverable: {deliver}", fill=MUTED, font=F16)
        if i < 5:
            d.polygon([(x + 350, y + 100), (x + 372, y + 110), (x + 350, y + 120)], fill=NAVY)
    save(img, "sdlc")


def diag_waterfall_agile():
    img, d = canvas(1200, 720)
    title_bar(d, 1200, "Waterfall vs Agile", "Choose the model from the case, not from fashion")
    rounded(d, (40, 100, 580, 680), SKY, NAVY, 16)
    d.text((70, 120), "Waterfall", fill=NAVY, font=FB32)
    d.text((70, 170), "One-way cascade · late testing", fill=MUTED, font=F18)
    steps = ["Requirements", "Design", "Code", "Test", "Deploy"]
    for i, s in enumerate(steps):
        y = 230 + i * 70
        rounded(d, (90, y, 430, y + 54), WHITE, NAVY, 10)
        d.text((110, y + 14), f"{i+1}. {s}", fill=INK, font=FB18)
        if i < 4:
            d.polygon([(260, y + 54), (250, y + 66), (270, y + 66)], fill=NAVY)
    d.text((90, 600), "Best when needs are fixed\n(Al-Noor library)", fill=INK, font=F16)

    rounded(d, (620, 100, 1160, 680), MINT, TEAL, 16)
    d.text((650, 120), "Agile", fill=TEAL, font=FB32)
    d.text((650, 170), "Short sprints · early working software", fill=MUTED, font=F18)
    for i, s in enumerate(["Sprint 1", "Sprint 2", "Sprint 3"]):
        x = 660 + i * 150
        d.ellipse((x, 260, x + 120, 380), outline=TEAL, width=4)
        d.text((x + 18, 304), s, fill=TEAL, font=FB16)
    d.text((660, 430), "Sprint = 2–4 weeks", fill=INK, font=FB18)
    d.text((660, 480), "capacity used =\nestimated / available × 100%", fill=INK, font=F18)
    d.text((660, 580), "Flexible, but NOT unplanned", fill=ORANGE, font=FB18)
    save(img, "waterfall_agile")


def diag_osi():
    img, d = canvas(1200, 820)
    title_bar(d, 1200, "OSI seven-layer model", "Please Do Not Throw Sausage Pizza Away")
    layers = [
        (7, "Application", "HTTP · SMTP · FTP", "what the user sees", (254, 202, 202)),
        (6, "Presentation", "encryption · JPEG", "format and encrypt", (254, 215, 170)),
        (5, "Session", "sockets · RPC", "start / manage talk", (253, 230, 138)),
        (4, "Transport", "TCP · UDP", "ports and reliability", (187, 247, 208)),
        (3, "Network", "IP · routers", "routing to a host", (186, 230, 253)),
        (2, "Data Link", "MAC · switches", "frames on a LAN", (221, 214, 254)),
        (1, "Physical", "cables · bits", "wires and signals", (226, 232, 240)),
    ]
    for i, (n, name, proto, job, fill) in enumerate(layers):
        y = 90 + i * 96
        rounded(d, (40, y, 1160, y + 86), fill, NAVY, 12)
        d.ellipse((60, y + 16, 120, y + 70), fill=NAVY)
        d.text((78, y + 28), str(n), fill=WHITE, font=FB22)
        d.text((150, y + 14), name, fill=NAVY, font=FB22)
        d.text((150, y + 48), f"{job}   ·   {proto}", fill=INK, font=F16)
        d.text((820, y + 28), ["Away", "Pizza", "Sausage", "Throw", "Not", "Do", "Please"][i], fill=MUTED, font=FB18)
    save(img, "osi")


def diag_tcpip():
    img, d = canvas(1200, 760)
    title_bar(d, 1200, "Encapsulation  ·  TCP/IP vs OSI", "Each layer adds a header going down")
    boxes = [
        (80, 120, "Data", "Application"),
        (80, 220, "Segment", "+ TCP/UDP header"),
        (80, 320, "Packet", "+ IP header"),
        (80, 420, "Frame", "+ MAC header/trailer"),
        (80, 520, "Bits", "Physical wire"),
    ]
    for i, (x, y, name, extra) in enumerate(boxes):
        w = 280 + i * 80
        rounded(d, (x, y, x + w, y + 80), SKY if i % 2 == 0 else LAV, NAVY, 10)
        d.text((x + 16, y + 14), name, fill=NAVY, font=FB22)
        d.text((x + 16, y + 48), extra, fill=MUTED, font=F16)
        if i < 4:
            d.polygon([(x + 40, y + 80), (x + 28, y + 96), (x + 52, y + 96)], fill=NAVY)
    rounded(d, (720, 120, 1160, 700), CREAM, GOLD, 16)
    d.text((750, 140), "TCP/IP 4 layers", fill=NAVY, font=FB22)
    map_rows = [
        "Application  ↔  OSI 5–7",
        "Transport    ↔  OSI 4",
        "Internet     ↔  OSI 3",
        "Network Access ↔ OSI 1–2",
    ]
    for i, t in enumerate(map_rows):
        d.text((750, 220 + i * 70), t, fill=INK, font=FB18)
    d.text((750, 520), "Decapsulation = reverse", fill=ORANGE, font=FB20)
    d.text((750, 570), "Receiver strips headers", fill=MUTED, font=F18)
    d.text((750, 610), "up the stack.", fill=MUTED, font=F18)
    save(img, "tcpip_encap")


def diag_ct():
    img, d = canvas(1200, 720)
    title_bar(d, 1200, "Computational thinking + algorithms", "Four strategies  ·  then write the steps")
    pillars = [
        (40, 110, "Decomposition", "Split a big problem\ninto small parts", SKY),
        (330, 110, "Pattern\nrecognition", "Spot what repeats\nor is similar", MINT),
        (620, 110, "Abstraction", "Keep what matters;\nhide the noise", CREAM),
        (910, 110, "Algorithm", "Clear, finite,\nordered steps", LAV),
    ]
    for x, y, name, body, fill in pillars:
        rounded(d, (x, y, x + 250, y + 280), fill, NAVY, 16)
        d.text((x + 16, y + 20), name, fill=NAVY, font=FB20)
        d.text((x + 16, y + 140), body, fill=INK, font=F18)
    rounded(d, (40, 430, 1160, 680), WHITE, TEAL, 16)
    d.text((70, 460), "A good algorithm is: finite · definite · effective · has input/output", fill=TEAL, font=FB20)
    d.text((70, 520), "Write it first in pseudocode (English-like steps), then code.", fill=INK, font=F18)
    d.text((70, 580), "Example: make tea → boil water → add tea → pour. Each step is testable.", fill=MUTED, font=F18)
    save(img, "computational_thinking")


def diag_sort():
    img, d = canvas(1200, 780)
    title_bar(d, 1200, "Bubble sort vs Selection sort", "Trace on 8, 4, 1, 9, 3")
    rounded(d, (40, 100, 580, 740), SKY, BLUE, 16)
    d.text((70, 120), "Bubble  ·  swap neighbours", fill=NAVY, font=FB22)
    passes = ["8 4 1 9 3", "4 8 1 9 3", "4 1 8 9 3", "4 1 8 3 9", "1 4 3 8 9"]
    for i, p in enumerate(passes):
        rounded(d, (70, 180 + i * 90, 540, 250 + i * 90), WHITE, BLUE, 10)
        d.text((90, 200 + i * 90), f"P{i+1}:  {p}", fill=INK, font=FB20)
    rounded(d, (620, 100, 1160, 740), MINT, TEAL, 16)
    d.text((650, 120), "Selection  ·  fix one slot", fill=TEAL, font=FB22)
    sels = ["k=1  pick 1 → 1 8 4 9 3", "k=2  pick 3 → 1 3 8 9 4", "k=3  pick 4 → 1 3 4 9 8", "k=4  pick 8 → 1 3 4 8 9"]
    for i, p in enumerate(sels):
        rounded(d, (650, 190 + i * 100, 1130, 270 + i * 100), WHITE, TEAL, 10)
        d.text((670, 214 + i * 100), p, fill=INK, font=FB18)
    save(img, "sorting")


def diag_search():
    img, d = canvas(1200, 720)
    title_bar(d, 1200, "Linear search vs Binary search", "Sorted data unlocks the faster method")
    rounded(d, (40, 100, 580, 680), CREAM, GOLD, 16)
    d.text((70, 120), "Linear  ·  check one by one", fill=ORANGE, font=FB22)
    for i, n in enumerate([3, 8, 1, 9, 4]):
        x = 80 + i * 90
        rounded(d, (x, 240, x + 70, 310), WHITE, GOLD, 8)
        d.text((x + 22, 258), str(n), fill=INK, font=FB22)
    d.text((70, 360), "Target 9 → 4 comparisons", fill=INK, font=FB18)
    d.text((70, 420), "Works on unsorted lists", fill=MUTED, font=F18)
    d.text((70, 470), "Worst case: n checks", fill=MUTED, font=F18)

    rounded(d, (620, 100, 1160, 680), SKY, NAVY, 16)
    d.text((650, 120), "Binary  ·  halve the list", fill=NAVY, font=FB22)
    for i, n in enumerate([1, 3, 4, 8, 9]):
        x = 670 + i * 90
        fill = MINT if n == 4 else WHITE
        rounded(d, (x, 240, x + 70, 310), fill, NAVY, 8)
        d.text((x + 22, 258), str(n), fill=INK, font=FB22)
    d.text((650, 360), "Must be SORTED first", fill=RED, font=FB18)
    d.text((650, 420), "mid = (low+high)//2", fill=INK, font=FB18)
    d.text((650, 470), "Target 4: compare 4 → found", fill=INK, font=F18)
    d.text((650, 530), "Worst case ≈ log₂ n", fill=MUTED, font=F18)
    save(img, "searching")


def diag_python():
    img, d = canvas(1200, 720)
    title_bar(d, 1200, "Programming · Python · VS Code", "Write · run · save · debug")
    tiles = [
        (40, 110, "Programming", "Giving a computer\nclear instructions"),
        (330, 110, "Python careers", "data · web · AI\nautomation · apps"),
        (620, 110, "VS Code", "Explorer · Editor\nTerminal · Run"),
        (910, 110, "First program", "print('Hello CS XI')\nsave as hello.py"),
    ]
    for x, y, t, b in tiles:
        rounded(d, (x, y, x + 250, y + 260), WHITE, NAVY, 16)
        d.text((x + 16, y + 20), t, fill=NAVY, font=FB20)
        d.text((x + 16, y + 110), b, fill=INK, font=F18)
    rounded(d, (40, 410, 1160, 680), NAVY, radius=16)
    d.text((70, 440), ">>> print('Sindh CS XI')", fill=(120, 255, 180), font=FB22)
    d.text((70, 500), "Sindh CS XI", fill=WHITE, font=FB22)
    d.text((70, 570), "Tip: run from Terminal or the Run button. Syntax errors are spelling mistakes in code.", fill=(180, 210, 255), font=F16)
    save(img, "python_ide")


def diag_variables():
    img, d = canvas(1200, 720)
    title_bar(d, 1200, "Variables, data types, input / output", "A named box that holds a value")
    boxes = [
        (60, 120, "name = 'Ali'", "str  string", SKY),
        (340, 120, "age = 16", "int  integer", MINT),
        (620, 120, "marks = 87.5", "float", CREAM),
        (900, 120, "pass_ = True", "bool", LAV),
    ]
    for x, y, code, typ, fill in boxes:
        rounded(d, (x, y, x + 240, y + 180), fill, NAVY, 14)
        d.text((x + 16, y + 30), code, fill=INK, font=FB18)
        d.text((x + 16, y + 110), typ, fill=NAVY, font=FB16)
    rounded(d, (60, 340, 1140, 680), WHITE, TEAL, 16)
    d.text((90, 370), "input() always returns a string. Cast it:", fill=NAVY, font=FB20)
    d.text((90, 430), "n = int(input('Marks: '))", fill=INK, font=FB22)
    d.text((90, 500), "print('You scored', n)", fill=INK, font=FB22)
    d.text((90, 580), "Rules: start with a letter or _; no spaces; case-sensitive; do not use keywords (if, for, class).", fill=MUTED, font=F16)
    save(img, "variables")


def diag_operators():
    img, d = canvas(1200, 720)
    title_bar(d, 1200, "Operators and operands", "The operator acts; the operand is acted on")
    rows = [
        ("Arithmetic", "+  -  *  /  //  %  **", "7 // 2 = 3    7 % 2 = 1"),
        ("Comparison", "==  !=  <  >  <=  >=", "result is True or False"),
        ("Logical", "and   or   not", "True and False → False"),
        ("Assignment", "=  +=  -=  *=", "x += 1  means x = x + 1"),
        ("Membership", "in    not in", "'A' in 'CAT' → True"),
    ]
    for i, (name, ops, ex) in enumerate(rows):
        y = 100 + i * 110
        rounded(d, (40, y, 1160, y + 96), WHITE, NAVY, 12)
        d.text((60, y + 16), name, fill=NAVY, font=FB20)
        d.text((320, y + 16), ops, fill=INK, font=FB20)
        d.text((320, y + 54), ex, fill=MUTED, font=F16)
    save(img, "operators")


def diag_selection():
    img, d = canvas(1200, 720)
    title_bar(d, 1200, "Sequence and selection", "One path after another  ·  then a decision")
    rounded(d, (40, 110, 400, 680), SKY, NAVY, 16)
    d.text((70, 140), "Sequence", fill=NAVY, font=FB26)
    for i, t in enumerate(["Start", "input marks", "compute grade", "print result"]):
        rounded(d, (80, 220 + i * 90, 360, 280 + i * 90), WHITE, NAVY, 10)
        d.text((100, 238 + i * 90), t, fill=INK, font=FB18)
    rounded(d, (460, 110, 1160, 680), CREAM, GOLD, 16)
    d.text((500, 140), "Selection  ·  if / elif / else", fill=ORANGE, font=FB26)
    d.polygon([(780, 230), (930, 300), (780, 370), (630, 300)], outline=NAVY, fill=WHITE, width=3)
    d.text((730, 286), "marks>=40?", fill=INK, font=FB16)
    rounded(d, (980, 270, 1130, 330), MINT, TEAL, 10)
    d.text((1000, 288), "Pass", fill=TEAL, font=FB18)
    rounded(d, (500, 270, 650, 330), ROSE, RED, 10)
    d.text((520, 288), "Fail", fill=RED, font=FB18)
    d.text((500, 430), "if marks >= 80:\n    grade = 'A'\nelif marks >= 40:\n    grade = 'Pass'\nelse:\n    grade = 'Fail'", fill=INK, font=F18)
    save(img, "selection")


def diag_loops():
    img, d = canvas(1200, 720)
    title_bar(d, 1200, "Repetition: for and while", "Know the count? use for. Wait for a condition? use while.")
    rounded(d, (40, 110, 580, 680), SKY, BLUE, 16)
    d.text((70, 140), "for  ·  known count", fill=NAVY, font=FB26)
    d.text((70, 220), "for i in range(1, 6):\n    print(i)", fill=INK, font=FB22)
    d.text((70, 360), "range(5)      → 0..4\nrange(1,6)    → 1..5\nrange(0,10,2) → 0,2,4,6,8", fill=MUTED, font=F18)
    d.text((70, 540), "Use when you know how many times.", fill=NAVY, font=FB18)
    rounded(d, (620, 110, 1160, 680), MINT, TEAL, 16)
    d.text((650, 140), "while  ·  condition", fill=TEAL, font=FB26)
    d.text((650, 220), "n = 3\nwhile n > 0:\n    print(n)\n    n = n - 1", fill=INK, font=FB22)
    d.text((650, 460), "Danger: forget n = n - 1\nand the loop never ends.", fill=RED, font=FB18)
    d.text((650, 540), "Use when you wait for a stop.", fill=TEAL, font=FB18)
    save(img, "loops")


def diag_debug():
    img, d = canvas(1200, 720)
    title_bar(d, 1200, "Libraries and debugging", "import first  ·  then hunt the bug")
    libs = [("math", "sqrt, pi, ceil"), ("random", "randint, choice"), ("datetime", "date, now")]
    for i, (n, f) in enumerate(libs):
        x = 40 + i * 380
        rounded(d, (x, 110, x + 350, 250), WHITE, NAVY, 14)
        d.text((x + 20, 130), f"import {n}", fill=NAVY, font=FB22)
        d.text((x + 20, 190), f, fill=INK, font=F18)
    bugs = [
        (40, 290, "SyntaxError", "Spelling / colon / brackets", ROSE),
        (430, 290, "NameError", "Used a name before creating it", CREAM),
        (820, 290, "TypeError", "Wrong type: '2' + 2", LAV),
        (40, 500, "Logic error", "Runs, but answer is wrong", SKY),
        (430, 500, "Fix loop", "Read the traceback · print values · change one thing", MINT),
        (820, 500, "IDE tools", "Red underline · Run · Debug console", CREAM),
    ]
    for x, y, t, b, fill in bugs:
        rounded(d, (x, y, x + 350, y + 170), fill, NAVY, 14)
        d.text((x + 16, y + 20), t, fill=NAVY, font=FB20)
        d.text((x + 16, y + 80), b, fill=INK, font=F16)
    save(img, "debug")


def diag_dbms():
    img, d = canvas(1200, 720)
    title_bar(d, 1200, "Data, DBMS, tables and keys", "A table is a relation; a key finds a row")
    rounded(d, (40, 110, 500, 680), WHITE, NAVY, 16)
    d.text((60, 130), "Student table", fill=NAVY, font=FB22)
    headers = ["Roll", "Name", "Class"]
    rows = [("XI-01", "Ayesha", "XI-A"), ("XI-02", "Bilal", "XI-B"), ("XI-03", "Sana", "XI-A")]
    for i, h in enumerate(headers):
        d.rectangle((60 + i * 140, 190, 190 + i * 140, 240), fill=NAVY)
        d.text((74 + i * 140, 202), h, fill=WHITE, font=FB16)
    for r, row in enumerate(rows):
        for c, val in enumerate(row):
            d.rectangle((60 + c * 140, 240 + r * 50, 190 + c * 140, 290 + r * 50), outline=LINE, width=2)
            d.text((74 + c * 140, 252 + r * 50), val, fill=INK, font=F16)
    d.text((60, 520), "Primary key = Roll (unique)", fill=TEAL, font=FB18)
    keys = [
        (560, 110, "Primary key", "Unique + not null. One per table."),
        (560, 250, "Foreign key", "Points to a primary key in another table."),
        (560, 390, "Candidate key", "Any field(s) that could be primary."),
        (560, 530, "DBMS", "Software that creates, stores, protects and queries databases."),
    ]
    for x, y, t, b in keys:
        rounded(d, (x, y, 1160, y + 120), SKY, BLUE, 12)
        d.text((x + 16, y + 16), t, fill=NAVY, font=FB20)
        d.text((x + 16, y + 64), b, fill=INK, font=F16)
    save(img, "dbms")


def diag_er():
    img, d = canvas(1200, 720)
    title_bar(d, 1200, "ER model and referential integrity", "Entities · attributes · relationships")
    rounded(d, (60, 220, 280, 360), SKY, NAVY, 14)
    d.text((110, 270), "MEMBER", fill=NAVY, font=FB22)
    d.polygon([(400, 200), (560, 290), (400, 380), (240, 290)], outline=TEAL, fill=MINT, width=3)
    d.text((390, 274), "borrows", fill=TEAL, font=FB18)
    rounded(d, (640, 220, 860, 360), CREAM, GOLD, 14)
    d.text((700, 270), "BOOK", fill=ORANGE, font=FB22)
    d.ellipse((80, 430, 260, 530), outline=NAVY, width=3)
    d.text((120, 466), "MemberID", fill=INK, font=F16)
    d.ellipse((660, 430, 840, 530), outline=ORANGE, width=3)
    d.text((710, 466), "BookID", fill=INK, font=F16)
    rounded(d, (900, 140, 1160, 660), LAV, PURPLE, 16)
    d.text((920, 160), "Cardinalities", fill=PURPLE, font=FB20)
    d.text((920, 220), "1 : 1   one to one", fill=INK, font=F18)
    d.text((920, 270), "1 : M   one to many", fill=INK, font=F18)
    d.text((920, 320), "M : N   many to many", fill=INK, font=F18)
    d.text((920, 400), "Referential integrity:\nforeign key value must\nexist as a primary key\nor be NULL.", fill=INK, font=F16)
    save(img, "er_model")


def diag_schema():
    img, d = canvas(1200, 720)
    title_bar(d, 1200, "Library relational schema", "Case study: Member · Book · BorrowRecord")
    tables = [
        (40, 120, "MEMBER", "MemberID PK\nName\nCNIC\nPhone"),
        (420, 120, "BOOK", "BookID PK\nTitle\nAuthor\nISBN"),
        (800, 120, "BORROWRECORD", "BorrowID PK\nMemberID FK\nBookID FK\nIssueDate\nReturnDate"),
    ]
    for x, y, t, b in tables:
        rounded(d, (x, y, x + 340, y + 320), WHITE, NAVY, 14)
        d.rectangle((x, y, x + 340, y + 56), fill=NAVY)
        d.text((x + 16, y + 14), t, fill=WHITE, font=FB20)
        d.text((x + 16, y + 80), b, fill=INK, font=F18)
    d.text((80, 500), "A member may borrow many books  →  1:M through BorrowRecord", fill=NAVY, font=FB18)
    d.text((80, 560), "M:N between Member and Book is resolved by the bridge table.", fill=MUTED, font=F18)
    d.text((80, 620), "Do not delete a Member who still has BorrowRecord rows (integrity).", fill=RED, font=F16)
    save(img, "schema")


def diag_access():
    img, d = canvas(1200, 720)
    title_bar(d, 1200, "MS Access objects", "Form → Table → Query → Report")
    flow = [
        (40, "Form", "enter / edit", ROSE),
        (330, "Table", "store rows", SKY),
        (620, "Query", "filter / analyse", MINT),
        (910, "Report", "print / share", CREAM),
    ]
    for x, name, job, fill in flow:
        rounded(d, (x, 140, x + 250, 340), fill, NAVY, 16)
        d.text((x + 24, 180), name, fill=NAVY, font=FB32)
        d.text((x + 24, 260), job, fill=INK, font=F18)
    rounded(d, (40, 400, 1160, 680), WHITE, TEAL, 16)
    d.text((70, 430), "Create a table in Design View (best practice)", fill=TEAL, font=FB22)
    d.text((70, 500), "1 Open Access → Create → Table Design\n2 Type Field Name + Data Type\n3 Select the key field → Primary Key\n4 Save the table (Student)", fill=INK, font=F18)
    save(img, "access_objects")


def diag_forms():
    img, d = canvas(1200, 680)
    title_bar(d, 1200, "Designing forms", "A friendly screen over a table")
    rounded(d, (40, 110, 700, 640), WHITE, NAVY, 16)
    d.text((70, 140), "Student Registration Form", fill=NAVY, font=FB22)
    fields = ["StudentID", "StudentName", "Department", "Marks", "ContactNumber"]
    for i, f in enumerate(fields):
        d.text((80, 210 + i * 70), f, fill=MUTED, font=F16)
        rounded(d, (280, 200 + i * 70, 650, 250 + i * 70), SKY, LINE, 8)
    rounded(d, (740, 110, 1160, 640), CREAM, GOLD, 16)
    d.text((770, 140), "Layouts", fill=ORANGE, font=FB22)
    d.text((770, 210), "Columnar — one record\n(best for data entry)\n\nTabular — many rows\n\nDatasheet — grid\n\nJustified — compact", fill=INK, font=F18)
    save(img, "forms")


def diag_queries():
    img, d = canvas(1200, 720)
    title_bar(d, 1200, "Queries, summaries and charts", "AND = same row   ·   OR = different rows")
    rounded(d, (40, 110, 1160, 300), NAVY, radius=14)
    d.text((70, 140), "SELECT StudentName, Marks", fill=(160, 255, 200), font=FB22)
    d.text((70, 190), "FROM Student", fill=WHITE, font=FB22)
    d.text((70, 240), "WHERE Department = 'Computer Science';", fill=(255, 220, 140), font=FB22)
    tiles = [
        (40, 340, "Filter", "criterion under a field"),
        (340, 340, "AND / OR", "same row / extra row"),
        (640, 340, "Group By", "summaries: Count Sum Avg"),
        (940, 340, "Chart", "bar / pie / line from query"),
    ]
    for x, y, t, b in tiles:
        rounded(d, (x, y, x + 260, y + 240), WHITE, NAVY, 14)
        d.text((x + 16, y + 30), t, fill=NAVY, font=FB22)
        d.text((x + 16, y + 110), b, fill=INK, font=F18)
    save(img, "queries")


def diag_ai():
    img, d = canvas(1200, 680)
    title_bar(d, 1200, "Artificial Intelligence in daily life", "Machines that learn from data and decide")
    tiles = [
        (40, 120, "Chatbot", "answers questions"),
        (340, 120, "Vision", "face / number plates"),
        (640, 120, "Recommend", "videos · shops"),
        (940, 120, "LMS", "online class tools"),
        (40, 360, "Hospital", "digital records"),
        (340, 360, "Bank", "ATM · mobile app"),
        (640, 360, "Farm", "weather · irrigation"),
        (940, 360, "School", "phones for learning"),
    ]
    for x, y, t, b in tiles:
        rounded(d, (x, y, x + 260, y + 200), WHITE, NAVY, 14)
        d.text((x + 16, y + 30), t, fill=NAVY, font=FB22)
        d.text((x + 16, y + 110), b, fill=INK, font=F18)
    save(img, "ai")


def diag_iot():
    img, d = canvas(1200, 780)
    title_bar(d, 1200, "Figure 5.1 · Six IoT components", "See · Act · Carry · Decide · Keep · Show")
    comps = [
        (40, 110, "i Sensors", "SEE the world", SKY),
        (430, 110, "ii Actuators", "ACT on commands", ROSE),
        (820, 110, "iii Connectivity", "CARRIES data", MINT),
        (40, 400, "iv Processing", "DECIDES", CREAM),
        (430, 400, "v Cloud", "KEEPS data", LAV),
        (820, 400, "vi User interface", "SHOWS data", SKY),
    ]
    for x, y, t, b, fill in comps:
        rounded(d, (x, y, x + 350, y + 250), fill, NAVY, 16)
        d.text((x + 20, y + 30), t, fill=NAVY, font=FB22)
        d.text((x + 20, y + 120), b, fill=INK, font=FB20)
    save(img, "iot")


def diag_analytics():
    img, d = canvas(1200, 680)
    title_bar(d, 1200, "Data Analytics cycle", "Collect → Clean → Analyse → Visualise → Decide")
    steps = ["Collect", "Clean", "Analyse", "Visualise", "Decide"]
    for i, s in enumerate(steps):
        x = 40 + i * 230
        d.ellipse((x, 180, x + 180, 360), fill=SKY, outline=NAVY, width=4)
        d.text((x + 30, 250), s, fill=NAVY, font=FB20)
        if i < 4:
            d.polygon([(x + 190, 260), (x + 220, 270), (x + 190, 280)], fill=NAVY)
    d.text((60, 460), "IoT collects, analytics studies, AI decides — three different jobs.", fill=INK, font=FB20)
    d.text((60, 530), "Example: soil-moisture readings → chart → irrigate only when dry.", fill=MUTED, font=F18)
    save(img, "analytics")


def diag_iot_uses():
    img, d = canvas(1200, 780)
    title_bar(d, 1200, "Uses of IoT", "Sensor → actuator → benefit in each area")
    uses = [
        "Smart city", "Industry", "Healthcare", "Education",
        "Automation", "Smart grid", "Smart farming", "Wearables",
    ]
    for i, u in enumerate(uses):
        x = 40 + (i % 4) * 290
        y = 120 + (i // 4) * 280
        rounded(d, (x, y, x + 270, y + 240), WHITE, NAVY, 14)
        d.text((x + 20, y + 30), u, fill=NAVY, font=FB20)
        hint = [
            "street lights, traffic",
            "machine temperature",
            "patient monitors",
            "smart classrooms",
            "home / factory",
            "load balancing",
            "soil + irrigation",
            "watch / band",
        ][i]
        d.text((x + 20, y + 120), hint, fill=INK, font=F18)
    save(img, "iot_uses")


def diag_sources():
    img, d = canvas(1200, 720)
    title_bar(d, 1200, "Reliable vs unreliable sources", "Author · date · evidence · purpose")
    rounded(d, (40, 110, 580, 680), MINT, TEAL, 16)
    d.text((70, 140), "More reliable", fill=TEAL, font=FB26)
    for t in ["Textbook / journal", "Govt / exam board", "Named expert", "Date + references"]:
        rounded(d, (70, 220 + ["Textbook / journal", "Govt / exam board", "Named expert", "Date + references"].index(t) * 90, 540, 290 + ["Textbook / journal", "Govt / exam board", "Named expert", "Date + references"].index(t) * 90), WHITE, TEAL, 10)
        d.text((90, 240 + ["Textbook / journal", "Govt / exam board", "Named expert", "Date + references"].index(t) * 90), t, fill=INK, font=FB18)
    rounded(d, (620, 110, 1160, 680), ROSE, RED, 16)
    d.text((650, 140), "Treat with care", fill=RED, font=FB26)
    for i, t in enumerate(["Anonymous social post", "No date / no author", "Wikipedia (tertiary)", "Forwarded rumour"]):
        rounded(d, (650, 220 + i * 90, 1120, 290 + i * 90), WHITE, RED, 10)
        d.text((670, 240 + i * 90), t, fill=INK, font=FB18)
    save(img, "sources")


def diag_impacts():
    img, d = canvas(1200, 720)
    title_bar(d, 1200, "Impacts of computing", "Human · cultural · environmental")
    cols = [
        (40, "Human", "jobs, health, privacy,\naccess to learning", SKY),
        (430, "Cultural", "language, values,\nonline behaviour", LAV),
        (820, "Environmental", "e-waste, energy,\nsmart grid savings", MINT),
    ]
    for x, t, b, fill in cols:
        rounded(d, (x, 120, x + 350, 680), fill, NAVY, 16)
        d.text((x + 20, 160), t, fill=NAVY, font=FB26)
        d.text((x + 20, 280), b, fill=INK, font=F20)
    save(img, "impacts")


def diag_assistive():
    img, d = canvas(1200, 680)
    title_bar(d, 1200, "Assistive technologies", "Computing that removes barriers")
    items = [
        ("Screen reader", "reads text aloud"),
        ("Screen magnifier", "enlarges the display"),
        ("Speech-to-text", "types what you say"),
        ("Alt text / captions", "images and video"),
        ("Switch / sip-puff", "physical access"),
        ("High contrast", "low vision"),
    ]
    for i, (t, b) in enumerate(items):
        x = 40 + (i % 3) * 380
        y = 120 + (i // 3) * 250
        rounded(d, (x, y, x + 350, y + 220), WHITE, NAVY, 14)
        d.text((x + 20, y + 40), t, fill=NAVY, font=FB20)
        d.text((x + 20, y + 120), b, fill=INK, font=F18)
    save(img, "assistive")


def diag_digilit():
    img, d = canvas(1200, 680)
    title_bar(d, 1200, "Digital literacy in the Information Age", "Find · judge · use · share data ethically")
    cycle = ["Ask", "Collect", "Clean", "Analyse", "Present", "Reflect"]
    for i, s in enumerate(cycle):
        x = 40 + (i % 3) * 380
        y = 140 + (i // 3) * 240
        d.ellipse((x + 40, y, x + 280, y + 200), fill=SKY, outline=NAVY, width=4)
        d.text((x + 110, y + 80), s, fill=NAVY, font=FB26)
    save(img, "digital_literacy")


def diag_data_types():
    img, d = canvas(1200, 720)
    title_bar(d, 1200, "Types of data", "Qualitative vs quantitative")
    rounded(d, (40, 110, 580, 680), SKY, BLUE, 16)
    d.text((70, 140), "Qualitative", fill=NAVY, font=FB26)
    d.text((70, 220), "Words, labels, opinions\n\nFavourite subject\nBlood group\nYes / No\n\nNominal or ordinal", fill=INK, font=F20)
    rounded(d, (620, 110, 1160, 680), MINT, TEAL, 16)
    d.text((650, 140), "Quantitative", fill=TEAL, font=FB26)
    d.text((650, 220), "Numbers you can measure\n\nMarks, height, time\n\nDiscrete: countable\nContinuous: measurable", fill=INK, font=F20)
    save(img, "data_types")


def diag_collection():
    img, d = canvas(1200, 720)
    title_bar(d, 1200, "Data-collection strategies", "Match the method to the question")
    methods = [
        ("Survey / questionnaire", "many people, same items"),
        ("Interview", "deep answers, few people"),
        ("Observation", "watch what actually happens"),
        ("Experiment", "change one variable"),
        ("Sensor / logger", "automatic readings"),
        ("Document / log", "existing school records"),
    ]
    for i, (t, b) in enumerate(methods):
        x = 40 + (i % 3) * 380
        y = 120 + (i // 3) * 270
        rounded(d, (x, y, x + 350, y + 230), WHITE, NAVY, 14)
        d.text((x + 18, y + 30), t, fill=NAVY, font=FB18)
        d.text((x + 18, y + 120), b, fill=INK, font=F18)
    save(img, "collection")


def diag_primary():
    img, d = canvas(1200, 680)
    title_bar(d, 1200, "Primary vs secondary data", "Did YOU collect it?")
    rounded(d, (40, 120, 580, 640), MINT, TEAL, 16)
    d.text((70, 160), "Primary", fill=TEAL, font=FB32)
    d.text((70, 250), "You collect it yourself\nfor THIS inquiry.\n\nClass survey\nSoil sensor you placed\nInterview you ran", fill=INK, font=F20)
    rounded(d, (620, 120, 1160, 640), CREAM, GOLD, 16)
    d.text((650, 160), "Secondary", fill=ORANGE, font=FB32)
    d.text((650, 250), "Someone else collected it.\n\nTextbook table\nPBS census\nNews chart\nWikipedia summary\n(tertiary if it only restates)", fill=INK, font=F20)
    save(img, "primary_secondary")


def diag_present():
    img, d = canvas(1200, 680)
    title_bar(d, 1200, "Presenting data with digital tools", "Choose the chart that matches the story")
    tools = [
        ("Bar", "compare categories"),
        ("Pie", "parts of a whole"),
        ("Line", "change over time"),
        ("Table", "exact values"),
        ("Spreadsheet", "sort · formula · chart"),
        ("Slides", "tell the inquiry story"),
    ]
    for i, (t, b) in enumerate(tools):
        x = 40 + (i % 3) * 380
        y = 120 + (i // 3) * 250
        rounded(d, (x, y, x + 350, y + 220), WHITE, NAVY, 14)
        d.text((x + 20, y + 40), t, fill=NAVY, font=FB26)
        d.text((x + 20, y + 120), b, fill=INK, font=F18)
    save(img, "present")


def diag_inquiry():
    img, d = canvas(1200, 720)
    title_bar(d, 1200, "Digital Inquiry Project", "A full cycle you can defend in the exam")
    steps = [
        "1 Question",
        "2 Plan ethics + sample",
        "3 Collect primary data",
        "4 Clean in a sheet",
        "5 Chart + comment",
        "6 Cite sources",
        "7 Present to class",
        "8 Reflect: bias / limits",
    ]
    for i, s in enumerate(steps):
        x = 40 + (i % 4) * 290
        y = 130 + (i // 4) * 260
        rounded(d, (x, y, x + 270, y + 220), SKY if i % 2 == 0 else MINT, NAVY, 14)
        d.text((x + 18, y + 80), s, fill=NAVY, font=FB20)
    save(img, "inquiry")


def diag_ai_edu():
    img, d = canvas(1200, 680)
    title_bar(d, 1200, "AI in education · careers · skills", "Tools help; the student still thinks")
    tiles = [
        (40, 120, "Classroom AI", "quizzes, language help,\nfeedback — check it"),
        (430, 120, "Careers", "data analyst, IoT tech,\napp developer, teacher"),
        (820, 120, "Skills", "problem solving,\nPython, ethics, teamwork"),
        (40, 400, "Pakistan", "NADRA, banks, farms,\nLMS in colleges"),
        (430, 400, "Watch-outs", "bias, privacy, cheating,\nover-trusting a bot"),
        (820, 400, "You still own", "the explanation in\nthe exam paper"),
    ]
    for x, y, t, b in tiles:
        rounded(d, (x, y, x + 350, y + 230), WHITE, NAVY, 14)
        d.text((x + 18, y + 24), t, fill=NAVY, font=FB20)
        d.text((x + 18, y + 100), b, fill=INK, font=F18)
    save(img, "ai_edu")


def main() -> None:
    DIAG.mkdir(parents=True, exist_ok=True)
    print("Rendering booklet diagram pages…")
    render_booklet()
    print("Generating educational diagrams…")
    for fn in (
        diag_cover, diag_analog_digital, diag_logic_gates, diag_truth_tables,
        diag_logic_circuit, diag_kmap, diag_sdlc, diag_waterfall_agile,
        diag_osi, diag_tcpip, diag_ct, diag_sort, diag_search, diag_python,
        diag_variables, diag_operators, diag_selection, diag_loops, diag_debug,
        diag_dbms, diag_er, diag_schema, diag_access, diag_forms, diag_queries,
        diag_ai, diag_iot, diag_analytics, diag_iot_uses, diag_sources,
        diag_impacts, diag_assistive, diag_digilit, diag_data_types,
        diag_collection, diag_primary, diag_present, diag_inquiry, diag_ai_edu,
    ):
        fn()
    print("Assets ready.")
    print("diagrams", len(list(DIAG.glob('*.png'))), "booklet", len(list(BOOK.glob('*.jpg'))))


if __name__ == "__main__":
    main()
