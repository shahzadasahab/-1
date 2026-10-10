"""Inline SVG diagrams for the Class XI study guide."""

import math


def _svg(w, h, inner, view=None):
    vb = view or f"0 0 {w} {h}"
    return f'''<svg class="diagram" viewBox="{vb}" width="{w}" height="{h}" xmlns="http://www.w3.org/2000/svg" role="img">
{inner}
</svg>'''


def analog_digital():
    analog_pts = []
    for i in range(0, 271, 3):
        x = 14 + i
        y = 78 - 38 * math.sin(i / 270 * 3 * math.pi)
        analog_pts.append(f"{x:.1f},{y:.1f}")
    analog = [
        f'<polyline points="{" ".join(analog_pts)}" fill="none" stroke="#0D7377" stroke-width="3"/>',
        '<line x1="10" y1="78" x2="290" y2="78" stroke="#C9D3DA" stroke-width="1"/>',
        '<text x="150" y="158" text-anchor="middle" class="svg-label">Analog — continuous wave</text>',
    ]

    digital = [
        '<path d="M10 120 L10 28 L70 28 L70 120 L130 120 L130 28 L190 28 L190 120 L250 120 L250 28 L286 28" '
        'fill="none" stroke="#1B365D" stroke-width="3"/>',
        '<text x="8" y="22" class="svg-tiny" fill="#0D7377">HIGH / 1</text>',
        '<text x="8" y="138" class="svg-tiny" fill="#8B3A3A">LOW / 0</text>',
        '<text x="150" y="158" text-anchor="middle" class="svg-label">Digital — square wave</text>',
    ]
    return f'''<div class="svg-row">
{_svg(300, 168, "".join(analog))}
{_svg(300, 168, "".join(digital))}
</div>'''


def stairs_ramp():
    stairs = (
        '<path d="M20 140 H70 V110 H120 V80 H170 V50 H220 V20 H260" fill="none" stroke="#1B365D" stroke-width="3"/>'
        '<circle cx="95" cy="110" r="5" fill="#C4A35A"/>'
        '<circle cx="145" cy="80" r="5" fill="#C4A35A"/>'
        '<text x="140" y="162" text-anchor="middle" class="svg-label">Stairs = discrete landings</text>'
    )
    ramp = (
        '<path d="M20 140 L260 20" fill="none" stroke="#0D7377" stroke-width="3"/>'
        '<circle cx="90" cy="107" r="5" fill="#C4A35A"/>'
        '<circle cx="160" cy="70" r="5" fill="#C4A35A"/>'
        '<text x="140" y="162" text-anchor="middle" class="svg-label">Ramp = any height in the range</text>'
    )
    return f'<div class="svg-row">{_svg(280, 172, stairs)}{_svg(280, 172, ramp)}</div>'


def _bubble(cx, cy):
    return f'<circle cx="{cx}" cy="{cy}" r="5.5" fill="#F6F1E6" stroke="#1B365D" stroke-width="2"/>'


def _gate_tile(inner, label):
    return _svg(168, 108, inner + f'<text x="84" y="100" text-anchor="middle" class="svg-label">{label}</text>')


def gate_and(bubble=False, label="AND"):
    x, y = 44, 10
    body = (
        f'<path d="M{x} {y} H{x+36} C{x+70} {y}, {x+70} {y+52}, {x+36} {y+52} H{x} Z" '
        f'fill="#d5e4ea" stroke="#1B365D" stroke-width="2.3"/>'
        f'<line x1="14" y1="{y+13}" x2="{x}" y2="{y+13}" stroke="#1B365D" stroke-width="2"/>'
        f'<line x1="14" y1="{y+39}" x2="{x}" y2="{y+39}" stroke="#1B365D" stroke-width="2"/>'
        '<text x="10" y="19" class="svg-tiny">A</text><text x="10" y="45" class="svg-tiny">B</text>'
    )
    out_x = x + 70
    if bubble:
        body += _bubble(out_x, y + 26)
        out_x += 6
    body += f'<line x1="{out_x}" y1="{y+26}" x2="154" y2="{y+26}" stroke="#1B365D" stroke-width="2"/>'
    body += '<text x="158" y="32" class="svg-tiny">Y</text>'
    return _gate_tile(body, label)


def gate_or(bubble=False, extra=False, label="OR"):
    x, y = 50 if extra else 44, 10
    body = (
        f'<path d="M{x} {y} Q{x+16} {y+26} {x} {y+52} Q{x+58} {y+52} {x+74} {y+26} Q{x+58} {y} {x} {y} Z" '
        f'fill="#d5e4ea" stroke="#1B365D" stroke-width="2.3"/>'
    )
    if extra:
        body += f'<path d="M{x-12} {y} Q{x+4} {y+26} {x-12} {y+52}" fill="none" stroke="#1B365D" stroke-width="2.2"/>'
        win = x - 12
    else:
        win = x + 8
    body += (
        f'<line x1="14" y1="{y+13}" x2="{win}" y2="{y+13}" stroke="#1B365D" stroke-width="2"/>'
        f'<line x1="14" y1="{y+39}" x2="{win}" y2="{y+39}" stroke="#1B365D" stroke-width="2"/>'
        '<text x="10" y="19" class="svg-tiny">A</text><text x="10" y="45" class="svg-tiny">B</text>'
    )
    out_x = x + 74
    if bubble:
        body += _bubble(out_x, y + 26)
        out_x += 6
    body += f'<line x1="{out_x}" y1="{y+26}" x2="154" y2="{y+26}" stroke="#1B365D" stroke-width="2"/>'
    body += '<text x="158" y="32" class="svg-tiny">Y</text>'
    return _gate_tile(body, label)


def gate_not(label="NOT"):
    x, y = 50, 10
    body = (
        f'<path d="M{x} {y} L{x} {y+52} L{x+58} {y+26} Z" fill="#d5e4ea" stroke="#1B365D" stroke-width="2.3"/>'
        f'<line x1="18" y1="{y+26}" x2="{x}" y2="{y+26}" stroke="#1B365D" stroke-width="2"/>'
        + _bubble(x + 64, y + 26)
        + f'<line x1="{x+70}" y1="{y+26}" x2="154" y2="{y+26}" stroke="#1B365D" stroke-width="2"/>'
        + '<text x="14" y="32" class="svg-tiny">A</text><text x="158" y="32" class="svg-tiny">Y</text>'
    )
    return _gate_tile(body, label)


def all_gates():
    tiles = [
        gate_and(False, "AND"),
        gate_or(False, False, "OR"),
        gate_not("NOT"),
        gate_and(True, "NAND"),
        gate_or(True, False, "NOR"),
        gate_or(False, True, "XOR"),
        gate_or(True, True, "XNOR"),
    ]
    cards = "".join(f'<figure class="gate-card">{svg}</figure>' for svg in tiles)
    return f'<div class="gate-grid">{cards}</div>'


def circuit_and_or():
    inner = (
        '<text x="18" y="38" class="svg-tiny">A</text>'
        '<text x="18" y="78" class="svg-tiny">B</text>'
        '<text x="18" y="128" class="svg-tiny">C</text>'
        '<line x1="32" y1="34" x2="70" y2="34" stroke="#1B365D" stroke-width="2"/>'
        '<line x1="32" y1="74" x2="70" y2="74" stroke="#1B365D" stroke-width="2"/>'
        '<path d="M70 18 H120 C162 18, 162 90, 120 90 H70 Z" fill="#EEF4F6" stroke="#1B365D" stroke-width="2.3"/>'
        '<text x="96" y="60" text-anchor="middle" class="svg-tiny">AND</text>'
        '<line x1="162" y1="54" x2="210" y2="54" stroke="#1B365D" stroke-width="2"/>'
        '<line x1="32" y1="124" x2="210" y2="124" stroke="#1B365D" stroke-width="2"/>'
        '<path d="M210 34 Q228 79 210 124 Q280 124 298 79 Q280 34 210 34 Z" fill="#EEF4F6" stroke="#1B365D" stroke-width="2.3"/>'
        '<text x="248" y="84" text-anchor="middle" class="svg-tiny">OR</text>'
        '<line x1="298" y1="79" x2="340" y2="79" stroke="#1B365D" stroke-width="2"/>'
        '<text x="348" y="84" class="svg-tiny">Y</text>'
        '<text x="190" y="168" text-anchor="middle" class="svg-label">Y = (A · B) + C</text>'
    )
    return _svg(380, 178, inner)


def kmap2():
    cells = [(40, 40, "0", "A′B′"), (120, 40, "1", "A′B"), (40, 120, "1", "AB′"), (120, 120, "1", "AB")]
    inner = [
        '<text x="90" y="22" text-anchor="middle" class="svg-tiny">B=0</text>',
        '<text x="170" y="22" text-anchor="middle" class="svg-tiny">B=1</text>',
        '<text x="18" y="82" text-anchor="middle" class="svg-tiny">A=0</text>',
        '<text x="18" y="162" text-anchor="middle" class="svg-tiny">A=1</text>',
        '<rect x="118" y="38" width="84" height="164" rx="10" fill="none" stroke="#0D7377" stroke-width="3"/>',
        '<rect x="38" y="118" width="164" height="84" rx="10" fill="none" stroke="#C4A35A" stroke-width="3"/>',
    ]
    for x, y, val, term in cells:
        inner.append(f'<rect x="{x}" y="{y}" width="80" height="80" fill="#F6F1E6" stroke="#1B365D"/>')
        inner.append(f'<text x="{x+40}" y="{y+48}" text-anchor="middle" font-size="22" font-weight="700" fill="#1B365D">{val}</text>')
        inner.append(f'<text x="{x+40}" y="{y+68}" text-anchor="middle" class="svg-tiny">{term}</text>')
    inner.append('<text x="120" y="232" text-anchor="middle" class="svg-label">Groups: right column → B, bottom row → A, so Y = A + B</text>')
    return _svg(240, 244, "".join(inner))


def kmap3():
    headers = ["00", "01", "11", "10"]
    vals = [["0", "1", "1", "0"], ["0", "1", "1", "0"]]
    inner = ['<text x="210" y="18" text-anchor="middle" class="svg-tiny">BC (Gray code: 00 · 01 · 11 · 10)</text>']
    for i, h in enumerate(headers):
        inner.append(f'<text x="{90+i*70}" y="42" text-anchor="middle" class="svg-tiny">{h}</text>')
    inner.append('<text x="28" y="88" class="svg-tiny">A=0</text>')
    inner.append('<text x="28" y="158" class="svg-tiny">A=1</text>')
    inner.append('<rect x="125" y="50" width="140" height="140" rx="8" fill="#0D737722" stroke="#0D7377" stroke-width="3"/>')
    for r in range(2):
        for c in range(4):
            x, y = 55 + c * 70, 50 + r * 70
            inner.append(f'<rect x="{x}" y="{y}" width="70" height="70" fill="none" stroke="#1B365D"/>')
            inner.append(f'<text x="{x+35}" y="{y+42}" text-anchor="middle" font-size="20" font-weight="700" fill="#1B365D">{vals[r][c]}</text>')
    inner.append('<text x="210" y="210" text-anchor="middle" class="svg-label">Block of four 1s: C is always 1 → Y = C</text>')
    return _svg(420, 224, "".join(inner))


def sdlc_cycle():
    labels = [
        (200, 36, "1 Analysis"),
        (330, 100, "2 Design"),
        (330, 200, "3 Code"),
        (200, 264, "4 Testing"),
        (70, 200, "5 Deploy"),
        (70, 100, "6 Maintain"),
    ]
    inner = [
        '<circle cx="200" cy="150" r="108" fill="none" stroke="#C4A35A" stroke-width="2.5" stroke-dasharray="6 6"/>',
        '<circle cx="200" cy="150" r="42" fill="#1B365D"/>',
        '<text x="200" y="146" text-anchor="middle" fill="#F6F1E6" font-size="12" font-weight="700">SDLC</text>',
        '<text x="200" y="162" text-anchor="middle" fill="#C4A35A" font-size="10">cycle</text>',
    ]
    for x, y, t in labels:
        inner.append(f'<rect x="{x-52}" y="{y-14}" width="104" height="28" rx="14" fill="#EEF4F6" stroke="#1B365D"/>')
        inner.append(f'<text x="{x}" y="{y+5}" text-anchor="middle" font-size="11" fill="#1B365D">{t}</text>')
    return _svg(400, 300, "".join(inner))


def waterfall_agile():
    wf = ['<text x="20" y="22" class="svg-label">Waterfall — one way down</text>']
    names = ["Req", "Design", "Code", "Test", "Deploy", "Maintain"]
    for i, n in enumerate(names):
        y = 40 + i * 36
        wf.append(f'<rect x="40" y="{y}" width="160" height="28" rx="4" fill="#1B365D"/>')
        wf.append(f'<text x="120" y="{y+19}" text-anchor="middle" fill="#F6F1E6" font-size="12">{n}</text>')
        if i < 5:
            wf.append(f'<path d="M120 {y+28} L120 {y+36}" stroke="#C4A35A" stroke-width="2" marker-end="url(#arr)"/>')
    ag = ['<text x="20" y="22" class="svg-label">Agile — repeat in sprints</text>']
    boxes = [("Plan", 40, 50), ("Build", 160, 50), ("Review", 160, 150), ("Retro", 40, 150)]
    for n, x, y in boxes:
        ag.append(f'<rect x="{x}" y="{y}" width="90" height="40" rx="6" fill="#0D7377"/>')
        ag.append(f'<text x="{x+45}" y="{y+25}" text-anchor="middle" fill="#F6F1E6" font-size="12">{n}</text>')
    ag.append('<path d="M130 70 H160 M205 90 V150 M160 170 H130 M85 150 V90" fill="none" stroke="#C4A35A" stroke-width="2.2"/>')
    ag.append('<text x="145" y="230" text-anchor="middle" class="svg-tiny">working software every 2–4 weeks</text>')
    defs = '<defs><marker id="arr" markerWidth="8" markerHeight="8" refX="6" refY="4" orient="auto"><path d="M0 0 L8 4 L0 8 Z" fill="#C4A35A"/></marker></defs>'
    return f'<div class="svg-row">{_svg(240, 280, defs + "".join(wf))}{_svg(280, 250, "".join(ag))}</div>'


def osi_stack():
    rows = [
        ("7 Application", "HTTP · HTTPS · FTP · SMTP · DNS", "#1B365D"),
        ("6 Presentation", "TLS · JPEG · MP3 · ASCII", "#24486F"),
        ("5 Session", "NetBIOS · RPC · checkpoints", "#2C587F"),
        ("4 Transport", "TCP / UDP · ports · segments", "#0D7377"),
        ("3 Network", "IP · ICMP · routers · packets", "#14919B"),
        ("2 Data Link", "Ethernet · Wi-Fi · MAC · frames", "#C4A35A"),
        ("1 Physical", "cables · radio · bits", "#8A7030"),
    ]
    inner = []
    for i, (name, proto, color) in enumerate(rows):
        y = 12 + i * 42
        inner.append(f'<rect x="20" y="{y}" width="420" height="36" rx="6" fill="{color}"/>')
        inner.append(f'<text x="36" y="{y+23}" fill="#F6F1E6" font-size="14" font-weight="700">{name}</text>')
        inner.append(f'<text x="428" y="{y+23}" text-anchor="end" fill="#F6F1E6" font-size="11">{proto}</text>')
    inner.append('<text x="230" y="322" text-anchor="middle" class="svg-label">Please Do Not Throw Sausage Pizza Away</text>')
    return _svg(460, 334, "".join(inner))


def encapsulation():
    bands = [
        (20, 20, 420, 200, "#1B365D", "Frame  ·  MAC header + trailer  ·  Data Link"),
        (48, 52, 364, 136, "#0D7377", "Packet  ·  IP header  ·  Network"),
        (76, 84, 308, 72, "#C4A35A", "Segment  ·  TCP/UDP + ports  ·  Transport"),
        (110, 108, 240, 28, "#F6F1E6", "Data"),
    ]
    inner = []
    for x, y, w, h, c, t in bands:
        fill = c
        ink = "#1B365D" if c == "#F6F1E6" else "#F6F1E6"
        inner.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="{fill}" stroke="#1B365D"/>')
        inner.append(f'<text x="{x+w/2}" y="{y+20}" text-anchor="middle" fill="{ink}" font-size="12">{t}</text>')
    inner.append('<text x="230" y="248" text-anchor="middle" class="svg-label">Going down: wrap. Going up: unwrap.</text>')
    return _svg(460, 260, "".join(inner))


def tcpip_map():
    inner = [
        '<text x="90" y="24" text-anchor="middle" class="svg-label">OSI</text>',
        '<text x="310" y="24" text-anchor="middle" class="svg-label">TCP/IP</text>',
    ]
    osi = [
        (36, "7–5 Application / Presentation / Session", "#1B365D", 70),
        (110, "4 Transport", "#0D7377", 40),
        (154, "3 Network", "#14919B", 40),
        (198, "2–1 Data Link + Physical", "#C4A35A", 50),
    ]
    tcp = [
        (36, "Application", "#1B365D", 70),
        (110, "Transport", "#0D7377", 40),
        (154, "Internet", "#14919B", 40),
        (198, "Network Access", "#C4A35A", 50),
    ]
    for y, t, c, h in osi:
        inner.append(f'<rect x="20" y="{y}" width="150" height="{h}" rx="6" fill="{c}"/>')
        inner.append(f'<text x="95" y="{y+h/2+4}" text-anchor="middle" fill="#F6F1E6" font-size="10">{t}</text>')
    for y, t, c, h in tcp:
        inner.append(f'<rect x="230" y="{y}" width="150" height="{h}" rx="6" fill="{c}"/>')
        inner.append(f'<text x="305" y="{y+h/2+4}" text-anchor="middle" fill="#F6F1E6" font-size="12">{t}</text>')
    for y in (71, 130, 174, 223):
        inner.append(f'<line x1="170" y1="{y}" x2="230" y2="{y}" stroke="#1B365D" stroke-width="1.5"/>')
    return _svg(400, 270, "".join(inner))


def _array_row(y, vals, title, highlight=None, parked=None):
    parts = [f'<text x="16" y="{y+18}" class="svg-tiny">{title}</text>']
    for i, v in enumerate(vals):
        x = 90 + i * 44
        if highlight and i in highlight:
            color = "#C4A35A"
        elif parked and i in parked:
            color = "#0D7377"
        else:
            color = "#1B365D"
        parts.append(f'<rect x="{x}" y="{y}" width="38" height="28" rx="4" fill="{color}"/>')
        parts.append(f'<text x="{x+19}" y="{y+19}" text-anchor="middle" fill="#F6F1E6" font-size="13">{v}</text>')
    return "".join(parts)


def bubble_sort_passes():
    inner = (
        _array_row(20, [8, 4, 1, 9, 3], "start")
        + _array_row(60, [4, 1, 8, 3, 9], "pass 1", parked={4})
        + _array_row(100, [1, 4, 3, 8, 9], "pass 2", parked={3, 4})
        + _array_row(140, [1, 3, 4, 8, 9], "pass 3", parked={2, 3, 4})
        + _array_row(180, [1, 3, 4, 8, 9], "sorted", parked={0, 1, 2, 3, 4})
        + '<text x="200" y="230" text-anchor="middle" class="svg-label">Largest value bubbles to the right each pass</text>'
    )
    return _svg(400, 244, inner)


def selection_sort_passes():
    inner = (
        _array_row(20, [8, 4, 1, 9, 3], "start")
        + _array_row(60, [1, 4, 8, 9, 3], "pass 0", highlight={0}, parked={0})
        + _array_row(100, [1, 3, 8, 9, 4], "pass 1", highlight={1}, parked={0, 1})
        + _array_row(140, [1, 3, 4, 9, 8], "pass 2", highlight={2}, parked={0, 1, 2})
        + _array_row(180, [1, 3, 4, 8, 9], "pass 3", parked={0, 1, 2, 3, 4})
        + '<text x="200" y="230" text-anchor="middle" class="svg-label">Each pass parks the minimum of the unsorted tail</text>'
    )
    return _svg(400, 244, inner)


def burglar_alarm():
    inner = (
        '<text x="18" y="38" class="svg-tiny">D door</text>'
        '<text x="18" y="88" class="svg-tiny">W window</text>'
        '<text x="18" y="148" class="svg-tiny">A armed</text>'
        '<line x1="70" y1="34" x2="108" y2="34" stroke="#1B365D" stroke-width="2"/>'
        '<line x1="70" y1="84" x2="108" y2="84" stroke="#1B365D" stroke-width="2"/>'
        '<path d="M108 14 Q126 59 108 104 Q178 104 196 59 Q178 14 108 14 Z" fill="#EEF4F6" stroke="#1B365D" stroke-width="2.3"/>'
        '<text x="148" y="64" text-anchor="middle" class="svg-tiny">OR</text>'
        '<line x1="196" y1="59" x2="250" y2="59" stroke="#1B365D" stroke-width="2"/>'
        '<line x1="70" y1="144" x2="250" y2="144" stroke="#1B365D" stroke-width="2"/>'
        '<path d="M250 40 H300 C342 40, 342 164, 300 164 H250 Z" fill="#EEF4F6" stroke="#1B365D" stroke-width="2.3"/>'
        '<text x="286" y="110" text-anchor="middle" class="svg-tiny">AND</text>'
        '<line x1="342" y1="102" x2="390" y2="102" stroke="#1B365D" stroke-width="2"/>'
        '<text x="398" y="107" class="svg-tiny">Y siren</text>'
        '<text x="220" y="196" text-anchor="middle" class="svg-label">Y = A · (D + W)</text>'
    )
    return _svg(460, 210, inner)


def binary_search():
    def cells(y, items, mid=None, dim=()):
        parts = []
        for i, v in enumerate(items):
            x = 40 + i * 42
            fill = "#C4A35A" if i == mid else ("#8A9BA8" if i in dim else "#1B365D")
            parts.append(f'<rect x="{x}" y="{y}" width="38" height="28" rx="4" fill="{fill}"/>')
            parts.append(f'<text x="{x+19}" y="{y+19}" text-anchor="middle" fill="#F6F1E6" font-size="13">{v}</text>')
        return "".join(parts)

    inner = (
        '<text x="200" y="18" text-anchor="middle" class="svg-label">Find 3 in a sorted list — halve each time</text>'
        + cells(36, [1, 2, 3, 4, 5, 6, 7, 8], mid=3)
        + '<text x="200" y="82" text-anchor="middle" class="svg-tiny">mid = 4, target 3 is smaller → keep left</text>'
        + cells(96, [1, 2, 3, 4, 5, 6, 7, 8], mid=1, dim={3, 4, 5, 6, 7})
        + '<text x="200" y="142" text-anchor="middle" class="svg-tiny">mid = 2, target 3 is larger → keep {3}</text>'
        + cells(156, [1, 2, 3, 4, 5, 6, 7, 8], mid=2, dim={0, 1, 3, 4, 5, 6, 7})
        + '<text x="200" y="208" text-anchor="middle" class="svg-label">Found after 3 looks, not 8</text>'
    )
    return _svg(400, 220, inner)


def python_flow():
    inner = (
        '<rect x="140" y="10" width="120" height="36" rx="6" fill="#1B365D"/>'
        '<text x="200" y="33" text-anchor="middle" fill="#F6F1E6" font-size="12">Start / input</text>'
        '<path d="M200 46 V70" stroke="#C4A35A" stroke-width="2"/>'
        '<path d="M200 70 L260 110 L200 150 L140 110 Z" fill="#0D7377" stroke="#1B365D"/>'
        '<text x="200" y="116" text-anchor="middle" fill="#F6F1E6" font-size="12">age ≥ 18?</text>'
        '<text x="280" y="104" class="svg-tiny">yes</text>'
        '<text x="108" y="164" class="svg-tiny">no</text>'
        '<rect x="280" y="96" width="110" height="32" rx="6" fill="#1B365D"/>'
        '<text x="335" y="117" text-anchor="middle" fill="#F6F1E6" font-size="11">Adult path</text>'
        '<rect x="20" y="160" width="110" height="32" rx="6" fill="#8B3A3A"/>'
        '<text x="75" y="181" text-anchor="middle" fill="#F6F1E6" font-size="11">Minor path</text>'
        '<text x="200" y="220" text-anchor="middle" class="svg-label">Selection chooses exactly one path</text>'
    )
    return _svg(410, 232, inner)


def er_library():
    def box(x, y, title, lines):
        h = 28 + 18 * len(lines)
        parts = [f'<rect x="{x}" y="{y}" width="150" height="{h}" rx="6" fill="#EEF4F6" stroke="#1B365D" stroke-width="2"/>']
        parts.append(f'<rect x="{x}" y="{y}" width="150" height="24" rx="6" fill="#1B365D"/>')
        parts.append(f'<text x="{x+75}" y="{y+17}" text-anchor="middle" fill="#F6F1E6" font-size="12">{title}</text>')
        for i, line in enumerate(lines):
            parts.append(f'<text x="{x+10}" y="{y+44+i*18}" font-size="11" fill="#1B365D">{line}</text>')
        return "".join(parts), h

    b1, _ = box(20, 40, "Member", ["PK MemberID", "Name", "Contact"])
    b2, _ = box(250, 16, "BorrowRecord", ["PK BorrowID", "FK MemberID", "FK BookID", "Issue / Return"])
    b3, _ = box(490, 40, "Book", ["PK BookID", "Title", "Author", "Publisher"])
    inner = (
        b1 + b2 + b3
        + '<line x1="170" y1="80" x2="250" y2="70" stroke="#0D7377" stroke-width="2"/>'
        + '<line x1="400" y1="70" x2="490" y2="80" stroke="#0D7377" stroke-width="2"/>'
        + '<text x="200" y="64" class="svg-tiny">1</text><text x="232" y="58" class="svg-tiny">M</text>'
        + '<text x="430" y="58" class="svg-tiny">M</text><text x="478" y="64" class="svg-tiny">1</text>'
        + '<text x="330" y="170" text-anchor="middle" class="svg-label">M:N resolved by a junction entity</text>'
    )
    return _svg(660, 184, inner)


def cardinalities():
    def pair(title, left, right, label):
        return (
            f'<text x="80" y="16" text-anchor="middle" class="svg-label">{title}</text>'
            f'<rect x="10" y="30" width="70" height="36" rx="6" fill="#1B365D"/>'
            f'<text x="45" y="53" text-anchor="middle" fill="#F6F1E6" font-size="11">{left}</text>'
            f'<rect x="80" y="30" width="70" height="36" rx="6" fill="#0D7377"/>'
            f'<text x="115" y="53" text-anchor="middle" fill="#F6F1E6" font-size="11">{right}</text>'
            f'<text x="80" y="86" text-anchor="middle" class="svg-tiny">{label}</text>'
        )

    return f'''<div class="svg-row">
{_svg(170, 96, pair("1 : 1", "Student", "ID card", "one ↔ one"))}
{_svg(170, 96, pair("1 : M", "Teacher", "Classes", "one → many"))}
{_svg(170, 96, pair("M : N", "Student", "Course", "needs junction"))}
</div>'''


def iot_loop():
    nodes = [
        (70, 70, "Sensor", "#1B365D"),
        (210, 70, "Connect", "#24486F"),
        (350, 70, "Analytics", "#0D7377"),
        (490, 70, "AI / rule", "#14919B"),
        (350, 170, "Actuator", "#C4A35A"),
        (210, 170, "UI / app", "#8A7030"),
    ]
    inner = []
    for x, y, t, c in nodes:
        inner.append(f'<rect x="{x-50}" y="{y-22}" width="100" height="44" rx="10" fill="{c}"/>')
        inner.append(f'<text x="{x}" y="{y+5}" text-anchor="middle" fill="#F6F1E6" font-size="13">{t}</text>')
    inner.append('<path d="M120 70 H160 M260 70 H300 M400 70 H440 M490 92 V148 H400" fill="none" stroke="#1B365D" stroke-width="2"/>')
    inner.append('<path d="M300 170 H260" fill="none" stroke="#1B365D" stroke-width="2"/>')
    inner.append('<text x="280" y="232" text-anchor="middle" class="svg-label">Collect → carry → explain → decide → act → show</text>')
    return _svg(560, 246, "".join(inner))


def analytics_pipe():
    steps = ["Collect", "Store", "Clean", "Analyse", "Visualise"]
    inner = []
    for i, t in enumerate(steps):
        x = 20 + i * 110
        inner.append(f'<rect x="{x}" y="36" width="96" height="44" rx="8" fill="#1B365D"/>')
        inner.append(f'<text x="{x+48}" y="63" text-anchor="middle" fill="#F6F1E6" font-size="12">{t}</text>')
        if i < 4:
            inner.append(f'<path d="M{x+96} 58 H{x+110}" stroke="#C4A35A" stroke-width="3"/>')
    inner.append('<text x="280" y="110" text-anchor="middle" class="svg-label">Raw marks become a pass/fail chart only after cleaning</text>')
    return _svg(560, 124, "".join(inner))


def inquiry_flow():
    steps = ["Question", "Search", "Collect", "Analyse", "Artefact"]
    inner = []
    for i, t in enumerate(steps):
        x = 24 + i * 108
        inner.append(f'<circle cx="{x+36}" cy="48" r="28" fill="#0D7377"/>')
        inner.append(f'<text x="{x+36}" y="52" text-anchor="middle" fill="#F6F1E6" font-size="18" font-weight="700">{i+1}</text>')
        inner.append(f'<text x="{x+36}" y="96" text-anchor="middle" class="svg-tiny">{t}</text>')
        if i < 4:
            inner.append(f'<path d="M{x+66} 48 H{x+108}" stroke="#C4A35A" stroke-width="2"/>')
    return _svg(560, 116, "".join(inner))
