/* XI Ch1 (Digital Logic) diagrams */
(function () {
  const D = Diagrams;

  D.register('xi1a.stairs-ramp', () => {
    let s = '';
    // stairs (discrete)
    s += K.text(105, 22, 'Stairs (Discrete)', { size: 14, w: 'b' });
    const sx = 30;
    const sy = 160;
    let pts = [[sx, sy]];
    for (let i = 0; i < 4; i++) {
      pts.push([sx + i * 36, sy - (i + 1) * 28]);
      pts.push([sx + (i + 1) * 36, sy - (i + 1) * 28]);
    }
    pts.push([sx + 144, sy]);
    s += K.poly(pts, { c: 4 });
    ['1', '2', '3', '4'].forEach((l, i) => {
      s += K.text(sx + i * 36 + 18, sy - (i + 1) * 28 - 6, l, { size: 12, cls: 't-mut' });
    });
    s += K.text(105, 182, 'fixed steps: 1, 2, 3, 4', { size: 12, cls: 't-mut' });
    // ramp (continuous)
    s += K.text(335, 22, 'Ramp (Continuous)', { size: 14, w: 'b' });
    s += K.poly([[260, 160], [410, 48], [410, 160]], { c: 0 });
    s += K.dot(335, 104, 4) + K.text(318, 98, '1.5 m', { size: 12, anchor: 'end', cls: 't-mut' });
    s += K.dot(372, 76, 4) + K.text(355, 70, '2.1 m', { size: 12, anchor: 'end', cls: 't-mut' });
    s += K.text(335, 182, 'any height is possible', { size: 12, cls: 't-mut' });
    return K.svg(440, 196, s, { title: 'Stairs versus ramp: discrete versus continuous' });
  });

  D.register('xi1a.analog-digital', () => {
    const W = 440;
    let s = '';
    s += K.text(115, 20, 'Analog signal', { size: 14, w: 'b' });
    s += K.text(335, 20, 'Digital signal', { size: 14, w: 'b' });
    // axes
    [[10, 100], [230, 100]].forEach(([x, y]) => {
      s += K.line(x, y, x + 200, y, { arrow: true, cls: 's-mut' });
      s += K.line(x, y + 55, x, y - 62, { arrow: true, cls: 's-mut' });
    });
    s += K.text(205, 122, 'time', { size: 11, anchor: 'end', cls: 't-mut' });
    s += K.text(425, 122, 'time', { size: 11, anchor: 'end', cls: 't-mut' });
    // sine
    let d = '';
    for (let x = 0; x <= 190; x += 3) {
      const y = 100 - 42 * Math.sin((x / 190) * Math.PI * 4);
      d += (x === 0 ? 'M' : 'L') + (10 + x).toFixed(1) + ' ' + y.toFixed(1) + ' ';
    }
    s += K.path(d, { s: 's-brand', w: 3 });
    s += K.text(115, 150, 'smooth, any value', { size: 12, cls: 't-mut' });
    // square wave: bits 1 0 1 1 0 1
    const bits = [1, 0, 1, 1, 0, 1];
    const bw = 31;
    let sq = '';
    bits.forEach((b, i) => {
      const y = b ? 52 : 100;
      const x0 = 235 + i * bw;
      sq += (i === 0 ? 'M' + x0 + ' ' + y : 'L' + x0 + ' ' + y) + ' L' + (x0 + bw) + ' ' + y + ' ';
      if (i < bits.length - 1 && bits[i + 1] !== b) sq += 'L' + (x0 + bw) + ' ' + (bits[i + 1] ? 52 : 100) + ' ';
      s += K.text(x0 + bw / 2, 40, String(b), { size: 12, w: 'b', cls: 't-acc' });
    });
    s += K.path(sq, { s: 's-acc', w: 3 });
    s += K.text(235, 150, 'only two levels: 0 and 1', { size: 12, cls: 't-mut', anchor: 'start' });
    return K.svg(W, 162, s, { title: 'Analog sine wave versus digital square wave' });
  });

  D.register('xi1a.bit-lamp', () => {
    let s = '';
    const lamp = (cx, on) => {
      let o = '';
      if (on) o += K.circle(cx, 64, 38, { cls: 'f-acc' }) ;
      o += '<circle cx="' + cx + '" cy="64" r="26" class="shape ' + (on ? 'c4' : 'c6') + '"/>';
      o += K.rect(cx - 12, 90, 24, 16, { c: 6, r: 3 });
      if (on) for (let a = 0; a < 8; a++) {
        const ang = (a * Math.PI) / 4;
        o += K.line(cx + Math.cos(ang) * 34, 64 + Math.sin(ang) * 34, cx + Math.cos(ang) * 44, 64 + Math.sin(ang) * 44, { cls: 's-acc', w: 2 });
      }
      return o;
    };
    s += lamp(90, false) + lamp(250, true);
    s += K.text(90, 128, '0 = OFF = LOW = FALSE', { size: 12, w: 'b' });
    s += K.text(250, 128, '1 = ON = HIGH = TRUE', { size: 12, w: 'b' });
    s += K.text(170, 22, 'one bit = one switch', { size: 14, cls: 't-mut' });
    s += K.line(125, 64, 215, 64, { arrow: 'both', cls: 's-mut', dash: '4 4' });
    return K.svg(340, 144, s, { title: 'A bit is like a lamp that is either off (0) or on (1)' });
  });

  /* ---------- shared helpers for the logic part ---------- */
  const FN = {
    AND: (a, b) => a & b,
    OR: (a, b) => a | b,
    NAND: (a, b) => 1 - (a & b),
    NOR: (a, b) => 1 - (a | b),
    XOR: (a, b) => a ^ b,
    XNOR: (a, b) => 1 - (a ^ b),
  };
  const EXPR = {
    AND: 'Y = A · B',
    OR: 'Y = A + B',
    NOT: "Y = A'",
    NAND: "Y = (A · B)'",
    NOR: "Y = (A + B)'",
    XOR: 'Y = A ⊕ B',
    XNOR: "Y = (A ⊕ B)'",
  };
  const RULE = {
    AND: 'Output is 1 only when ALL inputs are 1',
    OR: 'Output is 1 when ANY input is 1',
    NOT: 'Output is the opposite of the input',
    NAND: 'Output is 0 only when ALL inputs are 1',
    NOR: 'Output is 1 only when ALL inputs are 0',
    XOR: 'Output is 1 when the inputs are DIFFERENT',
    XNOR: 'Output is 1 when the inputs are the SAME',
  };
  const lab = (x, y, t, o) => K.text(x, y, t, Object.assign({ size: 13, w: 'b' }, o || {}));
  const stub = (x1, y1, x2, y2) => K.line(x1, y1, x2, y2);

  /* One gate symbol + its truth table.  args: { type: 'AND'|'OR'|'NOT'|'NAND'|'NOR'|'XOR'|'XNOR', n: 2|3 } */
  D.register('xi1a.gate', (args) => {
    args = args || {};
    const type = String(args.type || 'AND').toUpperCase();
    const one = type === 'NOT';
    const three = args.n === 3 && (type === 'AND' || type === 'OR');
    const nin = one ? 1 : three ? 3 : 2;
    const names = ['A', 'B', 'C'].slice(0, nin);
    const calc = (v) => {
      if (one) return 1 - v[0];
      if (three) return type === 'AND' ? (v[0] & v[1] & v[2]) : (v[0] | v[1] | v[2]);
      return FN[type](v[0], v[1]);
    };
    const rows = [names.concat('Y')];
    const fills = [[]];
    for (let i = 0; i < 1 << nin; i++) {
      const v = names.map((_, k) => (i >> (nin - 1 - k)) & 1);
      const y = calc(v);
      rows.push(v.concat(y));
      fills.push(v.map(() => null).concat(y ? 5 : null));
    }
    const W = 400;
    const cw = three ? 42 : one ? 60 : 52;
    const ch = three ? 22 : 26;
    const y0 = 38;
    const H = rows.length * ch;
    const tx0 = W - cw * (nin + 1) - 14;
    const cy = y0 + H / 2;
    const gx = 66;
    const gy = cy - 25;
    const g = K.gate(type, gx, gy, { c: 0 });
    let s = K.text(W / 2, 22, type + ' gate' + (three ? ' (3-input)' : ''), { size: 15, w: 'b' });
    s += g.svg;
    let pins;
    if (one) pins = [g.a];
    else if (three) {
      const dx = type === 'AND' ? [0, 0, 0] : [5, 8, 5];
      pins = [10, 25, 40].map((o, i) => [gx + dx[i], gy + o]);
    } else pins = [g.a, g.b];
    pins.forEach((p, i) => {
      s += stub(30, p[1], p[0], p[1]);
      s += lab(14, p[1] + 5, names[i]);
    });
    s += stub(g.q[0], g.q[1], g.q[0] + 28, g.q[1]);
    s += lab(g.q[0] + 40, g.q[1] + 5, 'Y', { size: 15 });
    s += K.grid(tx0, y0, cw, ch, rows, { head: true, fills, size: three ? 12 : 14 });
    let ex = EXPR[type];
    if (three) ex = type === 'AND' ? 'Y = A · B · C' : 'Y = A + B + C';
    const yb = y0 + H + 24;
    s += K.text(W / 2, yb, ex, { size: 15, w: 'b' });
    s += K.text(W / 2, yb + 20, RULE[type], { size: 12, cls: 't-mut' });
    return K.svg(W, yb + 32, s, { title: type + ' gate symbol with its truth table' });
  });

  /* Figure 1.4: all seven gate symbols */
  D.register('xi1a.gates-all', () => {
    let s = '';
    const types = ['AND', 'NAND', 'OR', 'NOR', 'NOT', 'XOR', 'XNOR'];
    types.forEach((t, i) => {
      const col = i % 4;
      const row = Math.floor(i / 4);
      const x = 24 + col * 108;
      const y = 40 + row * 100;
      const g = K.gate(t, x, y, { c: row ? 1 : 0 });
      s += g.svg;
      s += stub(x - 14, g.a[1], g.a[0], g.a[1]);
      if (g.b) s += stub(x - 14, g.b[1], g.b[0], g.b[1]);
      s += stub(g.q[0], g.q[1], g.q[0] + 14, g.q[1]);
      s += K.text(x + 34, y - 12, t, { size: 14, w: 'b' });
    });
    s += K.circle(383, 140, 5, { c: 4 });
    s += K.text(383, 168, 'bubble = NOT', { size: 12, cls: 't-mut' });
    s += K.text(383, 184, '(inverts output)', { size: 12, cls: 't-mut' });
    return K.svg(440, 200, s, { title: 'Symbols of AND, NAND, OR, NOR, NOT, XOR and XNOR gates' });
  });

  /* Two-lamp switch circuits: series = AND, parallel = OR */
  D.register('xi1a.switches', () => {
    let s = '';
    const sw = (x, y, closed, name) => {
      let o = K.dot(x, y, 3) + K.dot(x + 40, y, 3);
      o += closed ? K.line(x, y, x + 40, y, { w: 3 }) : K.line(x, y, x + 34, y - 20, { w: 3 });
      o += K.text(x + 20, y - 26, name + '=' + (closed ? 1 : 0), { size: 12, w: 'b', cls: closed ? 't-grn' : 't-red' });
      return o;
    };
    const lamp = (cx, cy, on) => {
      let o = K.circle(cx, cy, 15, { c: on ? 4 : 6 });
      o += K.line(cx - 10, cy - 10, cx + 10, cy + 10) + K.line(cx - 10, cy + 10, cx + 10, cy - 10);
      o += K.text(cx, cy + 34, on ? 'lamp ON' : 'lamp OFF', { size: 12, w: 'b', cls: on ? 't-grn' : 't-red' });
      return o;
    };
    // series (AND): A=1, B=0
    s += K.text(105, 18, 'Series = AND', { size: 14, w: 'b' });
    s += K.wire([[14, 80], [30, 80]]);
    s += sw(30, 80, true, 'A');
    s += K.wire([[70, 80], [95, 80]]);
    s += sw(95, 80, false, 'B');
    s += K.wire([[135, 80], [160, 80]]);
    s += lamp(175, 80, false);
    s += K.wire([[190, 80], [214, 80], [214, 135], [14, 135], [14, 80]]);
    s += K.text(105, 128, 'battery', { size: 11, cls: 't-mut', anchor: 'middle' });
    s += K.text(105, 178, 'both switches must close', { size: 12, cls: 't-mut' });
    // parallel (OR): A=1, B=0
    s += K.text(335, 18, 'Parallel = OR', { size: 14, w: 'b' });
    s += K.wire([[240, 90], [250, 90], [250, 66], [270, 66]]);
    s += K.wire([[250, 90], [250, 118], [270, 118]]);
    s += sw(270, 66, true, 'A');
    s += sw(270, 118, false, 'B');
    s += K.wire([[310, 66], [330, 66], [330, 90], [355, 90]]);
    s += K.wire([[310, 118], [330, 118], [330, 90]]);
    s += lamp(370, 90, true);
    s += K.wire([[385, 90], [428, 90], [428, 145], [240, 145], [240, 90]]);
    s += K.text(335, 138, 'battery', { size: 11, cls: 't-mut' });
    s += K.text(335, 180, 'any one switch is enough', { size: 12, cls: 't-mut' });
    return K.svg(440, 192, s, { title: 'Switches in series behave like AND, switches in parallel behave like OR' });
  });

  /* 2^n rows */
  D.register('xi1a.rows', () => {
    let s = K.text(220, 20, 'Number of rows = 2^n  (n = number of inputs)', { size: 14, w: 'b' });
    [1, 2, 3, 4].forEach((n, i) => {
      const y = 38 + i * 38;
      const rows = 1 << n;
      s += K.text(12, y + 19, n + (n === 1 ? ' input' : ' inputs') + ' = ' + rows + ' rows', { size: 12, w: 'b', anchor: 'start' });
      for (let r = 0; r < rows; r++) s += K.rect(150 + r * 17, y, 15, 26, { c: [0, 1, 4, 5][i], r: 3 });
    });
    return K.svg(440, 196, s, { title: 'With 1, 2, 3 and 4 inputs the truth table has 2, 4, 8 and 16 rows' });
  });

  /* Order of operations */
  D.register('xi1a.precedence', () => {
    let s = K.text(100, 20, 'Order of operations', { size: 14, w: 'b' });
    const items = [
      ['1', 'Parentheses ( )', 'First (highest)', 3],
      ['2', 'NOT  ( \' )', 'Second', 4],
      ['3', 'AND  ( · )', 'Third', 5],
      ['4', 'OR  ( + )', 'Last (lowest)', 0],
    ];
    items.forEach((it, i) => {
      const y = 34 + i * 44;
      s += K.box(8, y, 190, 36, it[0] + '.  ' + it[1], { c: it[3], size: 14, bold: true });
      s += K.text(206, y + 22, it[2], { size: 12, anchor: 'start', cls: 't-mut' });
    });
    // worked example
    s += K.rect(300, 34, 134, 172, { r: 10 });
    s += K.text(367, 54, 'Example', { size: 13, w: 'b' });
    s += K.text(367, 78, "Y = A + B · C'", { size: 14, w: 'b' });
    s += K.text(367, 108, "step 1:  C'", { size: 13 });
    s += K.text(367, 132, "step 2:  B · C'", { size: 13 });
    s += K.text(367, 156, "step 3:  A + (B · C')", { size: 12 });
    s += K.text(367, 184, 'NOT, then AND, then OR', { size: 11, cls: 't-mut' });
    return K.svg(440, 214, s, { title: 'Precedence: parentheses, NOT, AND, OR with a worked example' });
  });

  /* ---------- circuits built from expressions ---------- */
  const inp = (x, y, t) => lab(x, y + 5, t);

  /* args.expr: 'sop1' => Y = A·B + C   |  'pos1' => Y = (A+B)·C'   |  'xor' => Y = A'B + AB' */
  D.register('xi1a.circuit', (args) => {
    const ex = (args && args.expr) || 'sop1';
    let s = '';
    if (ex === 'sop1') {
      const and = K.gate('AND', 100, 20, { c: 1 });
      const or = K.gate('OR', 235, 50, { c: 0 });
      s += and.svg + or.svg;
      s += inp(14, 34, 'A') + K.wire([[28, 34], and.a]);
      s += inp(14, 56, 'B') + K.wire([[28, 56], and.b]);
      s += inp(14, 106, 'C') + K.wire([[28, 106], [212, 106], [212, or.b[1]], or.b]);
      s += K.wire([and.q, [200, and.q[1]], [200, or.a[1]], or.a]);
      s += K.text(176, and.q[1] - 7, 'A · B', { size: 12, cls: 't-mut' });
      s += K.wire([or.q, [or.q[0] + 40, or.q[1]]]);
      s += lab(or.q[0] + 52, or.q[1] + 5, 'Y', { size: 15 });
      s += K.text(200, 148, 'Y = A · B + C', { size: 15, w: 'b' });
      s += K.text(200, 166, 'AND first (higher precedence), then OR', { size: 12, cls: 't-mut' });
      return K.svg(400, 176, s, { title: 'Logic diagram for Y = A·B + C' });
    }
    if (ex === 'pos1') {
      const or = K.gate('OR', 100, 15, { c: 0 });
      const not = K.gate('NOT', 95, 100, { c: 3 });
      const and = K.gate('AND', 235, 52, { c: 1 });
      s += or.svg + not.svg + and.svg;
      s += inp(14, or.a[1], 'A') + K.wire([[28, or.a[1]], or.a]);
      s += inp(14, or.b[1], 'B') + K.wire([[28, or.b[1]], or.b]);
      s += inp(14, not.a[1], 'C') + K.wire([[28, not.a[1]], not.a]);
      s += K.wire([or.q, [205, or.q[1]], [205, and.a[1]], and.a]);
      s += K.text(168, or.q[1] - 7, 'A + B', { size: 12, cls: 't-mut' });
      s += K.wire([not.q, [215, not.q[1]], [215, and.b[1]], and.b]);
      s += K.text(172, not.q[1] - 7, "C'", { size: 12, cls: 't-mut' });
      s += K.wire([and.q, [and.q[0] + 40, and.q[1]]]);
      s += lab(and.q[0] + 52, and.q[1] + 5, 'Y', { size: 15 });
      s += K.text(200, 168, "Y = (A + B) · C'", { size: 15, w: 'b' });
      s += K.text(200, 186, 'Parentheses first, NOT on C, then AND', { size: 12, cls: 't-mut' });
      return K.svg(400, 196, s, { title: "Logic diagram for Y = (A+B)·C'" });
    }
    // xor in SOP form
    const notA = K.gate('NOT', 90, 4, { c: 3 });
    const notB = K.gate('NOT', 90, 150, { c: 3 });
    const and1 = K.gate('AND', 190, 40, { c: 1 });
    const and2 = K.gate('AND', 190, 125, { c: 1 });
    const or = K.gate('OR', 295, 80, { c: 0 });
    s += notA.svg + notB.svg + and1.svg + and2.svg + or.svg;
    // buses
    s += K.line(40, 30, 40, 139) + K.line(62, 76, 62, 175);
    s += lab(40, 22, 'A', { size: 13 }) + lab(62, 68, 'B', { size: 13 });
    s += K.wire([[40, 30], notA.a]) + K.dot(40, 30, 3);
    s += K.wire([[62, 76], and1.b]) + K.dot(62, 76, 3);
    s += K.wire([[40, 139], and2.a]) + K.dot(40, 139, 3);
    s += K.wire([[62, 175], notB.a]) + K.dot(62, 175, 3);
    s += K.wire([notA.q, [165, notA.q[1]], [165, and1.a[1]], and1.a]);
    s += K.wire([notB.q, [165, notB.q[1]], [165, and2.b[1]], and2.b]);
    s += K.text(156, notA.q[1] - 8, "A'", { size: 12, cls: 't-mut' });
    s += K.text(156, notB.q[1] - 8, "B'", { size: 12, cls: 't-mut' });
    s += K.wire([and1.q, [272, and1.q[1]], [272, or.a[1]], or.a]);
    s += K.wire([and2.q, [272, and2.q[1]], [272, or.b[1]], or.b]);
    s += K.text(258, and1.q[1] - 7, "A'B", { size: 12, cls: 't-mut' });
    s += K.text(258, and2.q[1] + 17, "AB'", { size: 12, cls: 't-mut' });
    s += K.wire([or.q, [or.q[0] + 38, or.q[1]]]);
    s += lab(or.q[0] + 50, or.q[1] + 5, 'Y', { size: 15 });
    s += K.text(330, 150, "Y = A'B + AB'", { size: 15, w: 'b' });
    s += K.text(330, 168, '(this is XOR)', { size: 12, cls: 't-mut' });
    return K.svg(430, 206, s, { title: "Logic diagram for Y = A'B + AB' which equals XOR" });
  });

  /* NAND = AND + NOT,  NOR = OR + NOT.  args.type */
  D.register('xi1a.equiv', (args) => {
    const t = String((args && args.type) || 'NAND').toUpperCase();
    const base = t === 'NOR' ? 'OR' : 'AND';
    const sym = t === 'NOR' ? '+' : '·';
    let s = '';
    const g1 = K.gate(base, 50, 34, { c: 1 });
    const n1 = K.gate('NOT', 150, 34, { c: 3 });
    s += g1.svg + n1.svg;
    s += inp(14, g1.a[1], 'A') + K.wire([[28, g1.a[1]], g1.a]);
    s += inp(14, g1.b[1], 'B') + K.wire([[28, g1.b[1]], g1.b]);
    s += K.wire([g1.q, n1.a]);
    s += K.text((g1.q[0] + n1.a[0]) / 2, g1.q[1] - 8, 'A ' + sym + ' B', { size: 11, cls: 't-mut' });
    s += K.wire([n1.q, [n1.q[0] + 16, n1.q[1]]]) + lab(n1.q[0] + 26, n1.q[1] + 5, 'Y');
    s += K.text(255, 64, '=', { size: 26, w: 'b' });
    const g2 = K.gate(t, 300, 34, { c: 0 });
    s += g2.svg;
    s += inp(276, g2.a[1], 'A') + K.wire([[288, g2.a[1]], g2.a]);
    s += inp(276, g2.b[1], 'B') + K.wire([[288, g2.b[1]], g2.b]);
    s += K.wire([g2.q, [g2.q[0] + 16, g2.q[1]]]) + lab(g2.q[0] + 26, g2.q[1] + 5, 'Y');
    s += K.text(110, 112, base + ' followed by NOT', { size: 13, cls: 't-mut' });
    s += K.text(330, 112, t + ' (bubble = NOT)', { size: 13, cls: 't-mut' });
    s += K.text(200, 140, t === 'NOR' ? "Y = (A + B)'" : "Y = (A · B)'", { size: 15, w: 'b' });
    return K.svg(400, 152, s, { title: t + ' gate equals ' + base + ' gate followed by NOT gate' });
  });

  /* minterm / maxterm table for the book's example */
  D.register('xi1a.sop-pos', () => {
    const rows = [
      ['A', 'B', 'Y', 'Minterm', 'Maxterm'],
      [0, 0, 0, "A'B'", 'A + B'],
      [0, 1, 1, "A'B", "A + B'"],
      [1, 0, 0, "AB'", "A' + B"],
      [1, 1, 1, 'AB', "A' + B'"],
    ];
    const fills = [[], [null, null, 3, null, 3], [null, null, 5, 5, null], [null, null, 3, null, 3], [null, null, 5, 5, null]];
    let s = K.grid(24, 14, 76, 30, rows, { head: true, fills, size: 14 });
    s += K.text(24 + 76 * 3.5, 178, "Y = 1 rows  →  minterms:  Y = A'B + AB", { size: 13, w: 'b', cls: 't-grn' });
    s += K.text(24 + 76 * 3.5, 200, "Y = 0 rows  →  maxterms:  Y = (A + B)(A' + B)", { size: 13, w: 'b', cls: 't-red' });
    return K.svg(430, 212, s, { title: 'Minterms for rows where Y is 1 and maxterms for rows where Y is 0' });
  });

  /* ---------- Karnaugh maps ---------- */
  const GROUP_T = { 's-brand': 't-acc', 's-red': 't-red', 's-grn': 't-grn' };
  function kmap(cfg) {
    const three = cfg.vars === 3;
    const cols = three ? 4 : 2;
    const cw = three ? 72 : 78;
    const ch = three ? 46 : 54;
    const x0 = three ? 78 : 72;
    const y0 = 44;
    const colL = three ? ['BC=00', 'BC=01', 'BC=11', 'BC=10'] : ['B=0', 'B=1'];
    const rowL = ['A=0', 'A=1'];
    let s = '';
    colL.forEach((c, j) => (s += K.text(x0 + j * cw + cw / 2, y0 - 10, c, { size: 12, w: 'b', cls: 't-mut' })));
    rowL.forEach((r, i) => (s += K.text(x0 - 10, y0 + i * ch + ch / 2, r, { size: 12, w: 'b', cls: 't-mut', anchor: 'end', vmid: true })));
    for (let i = 0; i < 2; i++) {
      for (let j = 0; j < cols; j++) {
        const x = x0 + j * cw;
        const y = y0 + i * ch;
        const v = cfg.vals ? cfg.vals[i][j] : null;
        const cc = cfg.vals ? (v ? 4 : null) : 0;
        s += '<rect x="' + x + '" y="' + y + '" width="' + cw + '" height="' + ch + '" class="shape cell ' + (cc == null ? 'c-none' : 'c' + cc) + '"/>';
        if (cfg.labels) s += K.text(x + cw / 2, y + ch / 2, cfg.labels[i][j], { size: 12, vmid: true, lh: 15 });
        else s += K.text(x + cw / 2, y + ch / 2, String(v), { size: 18, vmid: true, w: 'b' });
      }
    }
    (cfg.groups || []).forEach((gr) => {
      const ins = gr.inset || 4;
      s +=
        '<rect x="' + (x0 + gr.c0 * cw + ins) + '" y="' + (y0 + gr.r0 * ch + ins) + '" width="' + ((gr.c1 - gr.c0 + 1) * cw - 2 * ins) +
        '" height="' + ((gr.r1 - gr.r0 + 1) * ch - 2 * ins) + '" rx="14" class="shape c-none ' + gr.s + '" style="stroke-width:3"' +
        (gr.dash ? ' stroke-dasharray="' + gr.dash + '"' : '') + '/>';
    });
    if (cfg.title) s += K.text(x0 + (cols * cw) / 2, 18, cfg.title, { size: 14, w: 'b' });
    const gy = y0 + 2 * ch;
    let bottom = gy + 22;
    if (three) {
      (cfg.notes || []).forEach((n, i) => {
        s += K.text(x0 + (cols * cw) / 2, bottom + i * 20, n[0], { size: n[2] || 13, w: n[3] ? 'b' : '', cls: n[1] ? GROUP_T[n[1]] || n[1] : '' });
      });
      bottom += (cfg.notes || []).length * 20;
      return K.svg(400, bottom, s, { title: cfg.alt });
    }
    const nx = x0 + cols * cw + 22;
    (cfg.notes || []).forEach((n, i) => {
      s += K.text(nx, y0 + 14 + i * 24, n[0], { size: n[2] || 13, w: n[3] ? 'b' : '', anchor: 'start', cls: n[1] ? GROUP_T[n[1]] || n[1] : '' });
    });
    return K.svg(440, gy + 16, s, { title: cfg.alt });
  }

  D.register('xi1a.kmap2-layout', () =>
    kmap({
      vars: 2,
      title: '2-variable K-map',
      labels: [["m0\nA'B'", "m1\nA'B"], ["m2\nAB'", 'm3\nAB']],
      notes: [['4 cells = 2^2', null, 13, true], ['one cell = one row', null, 12], ['of the truth table', null, 12]],
      alt: 'Two variable Karnaugh map with minterms m0 to m3',
    })
  );

  D.register('xi1a.kmap3-layout', () =>
    kmap({
      vars: 3,
      title: '3-variable K-map  (8 cells)',
      labels: [["m0\nA'B'C'", "m1\nA'B'C", "m3\nA'BC", "m2\nA'BC'"], ["m4\nAB'C'", "m5\nAB'C", 'm7\nABC', "m6\nABC'"]],
      notes: [['column order 00, 01, 11, 10 (Gray code)', 's-red', 13, true]],
      alt: 'Three variable Karnaugh map layout with minterm numbers',
    })
  );

  D.register('xi1a.kmap2-ex', () =>
    kmap({
      vars: 2,
      title: "Y = A'B + AB' + AB",
      vals: [[0, 1], [1, 1]],
      groups: [
        { r0: 1, c0: 0, r1: 1, c1: 1, s: 's-red', inset: 4 },
        { r0: 0, c0: 1, r1: 1, c1: 1, s: 's-brand', inset: 9 },
      ],
      notes: [
        ['Group 1: row A=1  →  A', 's-red', 13, true],
        ['(B cancels)', null, 12],
        ['Group 2: column B=1  →  B', 's-brand', 13, true],
        ['(A cancels)', null, 12],
        ['Y = A + B', null, 15, true],
      ],
      alt: 'Two variable K-map with two groups giving Y equals A plus B',
    })
  );

  D.register('xi1a.kmap3-ex2', () =>
    kmap({
      vars: 3,
      title: "Y = A'B'C + A'BC + AB'C + ABC",
      vals: [[0, 1, 1, 0], [0, 1, 1, 0]],
      groups: [{ r0: 0, c0: 1, r1: 1, c1: 2, s: 's-red', inset: 4 }],
      notes: [
        ['One square group of 4 (m1, m3, m5, m7)', 's-red', 13, true],
        ['C = 1 in all of them', null, 13],
        ['Y = C', null, 16, true],
      ],
      alt: 'Three variable K-map with one square group of four cells giving Y equals C',
    })
  );

  D.register('xi1a.kmap3-ex3', () =>
    kmap({
      vars: 3,
      title: "Y = A'B'C' + A'BC' + A'B'C + A'BC + AB'C + ABC",
      vals: [[1, 1, 1, 1], [0, 1, 1, 0]],
      groups: [
        { r0: 0, c0: 0, r1: 0, c1: 3, s: 's-brand', inset: 4 },
        { r0: 0, c0: 1, r1: 1, c1: 2, s: 's-red', inset: 10, dash: '6 4' },
      ],
      notes: [
        ['Row group of 4 (m0, m1, m3, m2): A = 0', 's-brand', 13, true],
        ['Square group of 4 (m1, m3, m5, m7): C = 1', 's-red', 13, true],
        ["Y = A' + C", null, 16, true],
      ],
      alt: 'Three variable K-map with a row group and a square group giving Y equals NOT A plus C',
    })
  );

  /* Gray code order */
  D.register('xi1a.gray', () => {
    let s = K.text(215, 20, 'Gray code: neighbours differ by ONE bit', { size: 14, w: 'b' });
    const codes = ['00', '01', '11', '10'];
    const changes = ['C changes', 'B changes', 'C changes'];
    codes.forEach((c, i) => {
      s += K.box(30 + i * 100, 40, 70, 40, 'BC=' + c, { c: [0, 1, 4, 5][i], size: 14, bold: true });
    });
    [0, 1, 2].forEach((i) => {
      s += K.line(100 + i * 100, 60, 130 + i * 100, 60, { arrow: true });
      s += K.text(115 + i * 100, 100, changes[i], { size: 12, cls: 't-mut' });
    });
    s += K.path('M365 82 Q365 128 215 128 Q65 128 65 82', { s: 's-red', w: 2.5, arrow: true, dash: '6 4' });
    s += K.text(215, 148, 'wrap-around: 10 back to 00, only B changes', { size: 12, cls: 't-red', w: 'b' });
    return K.svg(430, 160, s, { title: 'Gray code order 00, 01, 11, 10 with wrap-around' });
  });

  /* ---------- LogiSim ---------- */
  D.register('xi1a.logisim-ui', () => {
    let s = '';
    const X = 8;
    const Wd = 424;
    s += K.rect(X, 8, Wd, 232, { c: 6, r: 6, cls: 'c-none' });
    // menu bar
    s += K.rect(X, 8, Wd, 24, { c: 0, r: 0 });
    ['File', 'Edit', 'Project', 'Simulate', 'Window', 'Help'].forEach((m, i) => (s += K.text(X + 28 + i * 56, 24, m, { size: 11 })));
    // toolbar
    s += K.rect(X, 32, Wd, 30, { c: 1, r: 0 });
    ['AND', 'OR', 'NOT', 'NAND', 'NOR', 'XOR', 'XNOR'].forEach((m, i) => {
      s += K.rect(X + 8 + i * 50, 37, 46, 20, { c: 6, r: 3 }) + K.text(X + 31 + i * 50, 47, m, { size: 10, vmid: true });
    });
    
    // explorer
    s += K.rect(X, 62, 112, 96, { c: 6, r: 0, cls: 'c-none' });
    s += K.text(X + 26, 76, 'Explorer Panel', { size: 11, w: 'b', anchor: 'start' });
    ['My Project', 'Gates', 'Wiring'].forEach((t, i) => (s += K.text(X + 8, 94 + i * 16, t, { size: 11, anchor: 'start', cls: 't-mut' })));
    // attributes
    s += K.rect(X, 158, 112, 66, { c: 6, r: 0, cls: 'c-none' });
    s += K.text(X + 26, 172, 'Attribute Table', { size: 11, w: 'b', anchor: 'start' });
    ['# Inputs   2', 'Facing   East'].forEach((t, i) => (s += K.text(X + 8, 190 + i * 15, t, { size: 11, anchor: 'start', cls: 't-mut' })));
    // canvas
    s += K.rect(X + 112, 62, Wd - 112, 162, { c: 6, r: 0, cls: 'c-none' });
    for (let gx = X + 126; gx < X + Wd - 6; gx += 18) for (let gy = 76; gy < 222; gy += 18) s += K.dot(gx, gy, 0.9);
    const g = K.gate('AND', 290, 108, { c: 0 });
    s += g.svg;
    s += K.wire([[222, g.a[1]], g.a]) + K.wire([[222, g.b[1]], g.b]) + K.wire([g.q, [380, g.q[1]]]);
    s += K.rect(210, g.a[1] - 5, 12, 10, { c: 5, r: 2 }) + K.rect(210, g.b[1] - 5, 12, 10, { c: 5, r: 2 });
    s += K.circle(388, g.q[1], 7, { c: 4 });
    s += K.text(330, 206, 'Drawing Canvas', { size: 11, w: 'b' });
    // status bar
    s += K.rect(X, 224, Wd, 16, { c: 0, r: 0 });
    s += K.text(X + 8, 236, 'Ready | Zoom: 100% | Circuit: main', { size: 10, anchor: 'start', cls: 't-mut' });
    // badges
    const badge = (x, y, t) => K.circle(x, y, 8, { c: 3, s: 's-red' }) + K.text(x, y + 4, t, { size: 11, w: 'b' });
    s += badge(X + 412, 20, '1') + badge(X + 412, 47, '2') + badge(X + 13, 74, '3') + badge(X + 13, 170, '4') + badge(X + 412, 76, '5') + badge(X + 412, 232, '6');
    s += K.text(220, 260, '1 Menu Bar   2 Toolbar   3 Explorer Panel', { size: 12, cls: 't-mut' });
    s += K.text(220, 278, '4 Attribute Table   5 Drawing Canvas   6 Status Bar', { size: 12, cls: 't-mut' });
    return K.svg(440, 288, s, { title: 'LogiSim Evolution window with menu bar, toolbar, explorer panel, attribute table, drawing canvas and status bar' });
  });

  D.register('xi1a.install-flow', () => {
    const steps = [
      ['Open the GitHub releases page of\nlogisim-evolution in a browser', 1],
      ['Download the Windows installer\n(.msi file, 64-bit)', 0],
      ['Install Java 21 or newer if missing\n(adoptium.net)', 4],
      ['Double-click the .msi, click Yes,\naccept licence, Install, Finish', 5],
      ['Launch LogiSim Evolution from the\nStart menu or desktop shortcut', 2],
    ];
    let s = '';
    steps.forEach((st, i) => {
      const y = 8 + i * 58;
      s += K.circle(24, y + 22, 14, { c: 3 }) + K.text(24, y + 27, String(i + 1), { size: 14, w: 'b' });
      s += K.box(50, y, 330, 44, st[0], { c: st[1], size: 13 });
      if (i < steps.length - 1) s += K.line(215, y + 44, 215, y + 58, { arrow: true });
    });
    return K.svg(400, 300, s, { title: 'Steps to download and install LogiSim Evolution on Windows' });
  });

  D.register('xi1a.logisim-circuit', () => {
    let s = K.rect(8, 8, 384, 160, { c: 6, r: 8, cls: 'c-none' });
    for (let gx = 22; gx < 390; gx += 18) for (let gy = 22; gy < 166; gy += 18) s += K.dot(gx, gy, 0.9);
    const g = K.gate('AND', 190, 55, { c: 0 });
    s += g.svg;
    s += K.wire([[80, g.a[1]], g.a], { cls: 's-grn', w: 3 });
    s += K.wire([[80, g.b[1]], g.b], { cls: 's-grn', w: 3 });
    s += K.wire([g.q, [310, g.q[1]]], { cls: 's-grn', w: 3 });
    s += K.rect(60, g.a[1] - 10, 20, 20, { c: 0, r: 3 }) + K.text(70, g.a[1], '1', { size: 13, w: 'b', vmid: true });
    s += K.rect(60, g.b[1] - 10, 20, 20, { c: 0, r: 3 }) + K.text(70, g.b[1], '1', { size: 13, w: 'b', vmid: true });
    s += K.circle(320, g.q[1], 10, { c: 5 }) + K.text(320, g.q[1], '1', { size: 13, w: 'b', vmid: true });
    s += K.text(70, g.a[1] - 18, 'Input Pin A', { size: 11, cls: 't-mut' });
    s += K.text(70, g.b[1] + 28, 'Input Pin B', { size: 11, cls: 't-mut' });
    s += K.text(320, g.q[1] + 28, 'Output Pin', { size: 11, cls: 't-mut' });
    s += K.text(218, 42, 'AND gate', { size: 11, cls: 't-mut' });
    s += K.text(200, 150, 'Poke Tool: click an input pin to toggle 0 / 1', { size: 12, w: 'b', cls: 't-acc' });
    return K.svg(400, 178, s, { title: 'A simple AND circuit in LogiSim with two input pins and one output pin' });
  });
})();
