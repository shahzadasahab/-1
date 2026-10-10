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
})();
