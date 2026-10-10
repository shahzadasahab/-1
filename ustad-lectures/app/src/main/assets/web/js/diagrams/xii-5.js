/* XII Ch5 (Applications and Impacts of Computing) diagrams */
(function () {
  const D = Diagrams;

  const arr = (x1, y1, x2, y2, o) => K.line(x1, y1, x2, y2, Object.assign({ arrow: true }, o || {}));
  const badge = (cx, cy, num, c) => K.circle(cx, cy, 10, { c: c == null ? 4 : c }) + K.text(cx, cy + 0.5, String(num), { size: 11, w: 'b', vmid: true });

  /* grid of titled chips; items: {t, d, c} */
  function chips(items, o) {
    const cols = o.cols, w = o.w, h = o.h, gap = o.gap == null ? 8 : o.gap;
    const x0 = o.x0 || 6, y0 = o.y0 || 6;
    let s = '';
    items.forEach((it, i) => {
      const x = x0 + (i % cols) * (w + gap);
      const y = y0 + Math.floor(i / cols) * (h + gap);
      s += K.rect(x, y, w, h, { c: it.c == null ? i % 8 : it.c });
      const left = !!o.left;
      const tx = left ? x + (o.pad || 12) : x + w / 2;
      const anchor = left ? 'start' : 'middle';
      s += K.text(tx, y + (o.ty || 22), it.t, { size: o.tsize || 13, w: 'b', anchor });
      if (it.d) s += K.text(tx, y + (o.dy || 40), it.d, { size: o.dsize || 12, cls: 't-mut', anchor, lh: o.lh || 15 });
    });
    return s;
  }

  /* centre ellipse with six items around it (3 left, 3 right) */
  function hub(centre, items, o) {
    const bw = 142, bh = 58;
    let s = '';
    const ys = [8, 78, 148].map((y) => y + (o.dy0 || 0));
    items.forEach((it, i) => {
      const left = i < 3;
      const x = left ? 6 : 440 - 6 - bw;
      const y = ys[i % 3];
      s += K.line(left ? x + bw : x, y + bh / 2, 220, ys[1] + bh / 2, { cls: 's-mut', w: 1.6 });
    });
    s += K.ellipse(220, ys[1] + bh / 2, 62, 42, { c: o.cc == null ? 2 : o.cc });
    s += K.text(220, ys[1] + bh / 2, centre, { size: 13, w: 'b', vmid: true });
    items.forEach((it, i) => {
      const left = i < 3;
      const x = left ? 6 : 440 - 6 - bw;
      const y = ys[i % 3];
      s += K.rect(x, y, bw, bh, { c: it.c == null ? o.c || 0 : it.c });
      s += K.text(x + bw / 2, y + 23, it.t, { size: 12.5, w: 'b' });
      s += K.text(x + bw / 2, y + 41, it.d, { size: 11.5, cls: 't-mut' });
    });
    return s;
  }

  /* ---------- 5.1 ML / NN / DL ---------- */

  D.register('xii5.ml-flow', () => {
    let s = '';
    s += K.box(8, 40, 100, 60, 'Data\n(examples)', { c: 1, size: 13 });
    s += arr(108, 70, 164, 70);
    s += K.rect(164, 30, 114, 80, { c: 2 });
    s += K.text(221, 58, 'ML Model', { size: 14, w: 'b' });
    s += K.text(221, 78, 'learns patterns', { size: 12, cls: 't-mut' });
    s += K.text(221, 94, 'from data', { size: 12, cls: 't-mut' });
    s += arr(278, 70, 332, 70);
    s += K.box(332, 40, 100, 60, 'Prediction\nor Decision', { c: 5, size: 13 });
    s += K.polyline([[8, 124], [8, 132], [278, 132], [278, 124]], { cls: 's-acc' });
    s += K.text(143, 152, 'Step 1: Training', { size: 13, w: 'b', cls: 't-acc' });
    s += K.polyline([[332, 124], [332, 132], [432, 132], [432, 124]], { cls: 's-grn' });
    s += K.text(382, 152, 'Step 2: Use', { size: 13, w: 'b', cls: 't-grn' });
    s += K.text(220, 18, 'A trained brain of the computer program', { size: 12, cls: 't-mut' });
    return K.svg(440, 166, s, { title: 'Machine learning flow: data, model learns patterns, then makes prediction' });
  });

  D.register('xii5.ai-nested', () => {
    let s = '';
    const base = 238;
    const rings = [
      { rx: 206, ry: 118, c: 6, t: 'Artificial Intelligence (AI)', ty: 24 },
      { rx: 166, ry: 90, c: 1, t: 'Machine Learning (ML)', ty: 24 },
      { rx: 124, ry: 62, c: 0, t: 'Neural Networks', ty: 22 },
      { rx: 84, ry: 34, c: 2, t: 'Deep\nLearning', ty: 0 },
    ];
    rings.forEach((r, i) => {
      const cy = base - r.ry;
      s += K.ellipse(220, cy, r.rx, r.ry, { c: r.c });
      if (i < 3) s += K.text(220, cy - r.ry + r.ty, r.t, { size: i === 0 ? 14 : 13, w: 'b' });
      else s += K.text(220, cy, 'Deep Learning', { size: 13, w: 'b', vmid: true });
    });
    return K.svg(440, 246, s, { title: 'AI contains machine learning, which contains neural networks, which contains deep learning' });
  });

  D.register('xii5.neural-net', () => {
    const inX = 60, hidX = 200, outX = 330;
    const ins = [100, 160, 220], hid = [70, 130, 190, 250], outs = [115, 205];
    let s = '';
    ins.forEach((iy) => hid.forEach((hy) => { s += K.line(inX, iy, hidX, hy, { cls: 's-mut', w: 1.2 }); }));
    hid.forEach((hy) => outs.forEach((oy) => { s += K.line(hidX, hy, outX, oy, { cls: 's-mut', w: 1.2 }); }));
    s += K.rect(110, 136, 46, 18, { c: 4, r: 5 }) + K.text(133, 146, 'w=0.8', { size: 11, w: 'b', vmid: true });
    ins.forEach((y, i) => { s += K.circle(inX, y, 16, { c: 1 }) + K.text(inX, y, 'x' + (i + 1), { size: 12, vmid: true }); });
    hid.forEach((y) => { s += K.circle(hidX, y, 16, { c: 2 }); });
    outs.forEach((y, i) => { s += K.circle(outX, y, 16, { c: 5 }) + K.text(outX, y, 'y' + (i + 1), { size: 12, vmid: true }); });
    s += K.text(outX + 24, 111, 'Output 1', { size: 12, anchor: 'start' }) + K.text(outX + 24, 125, '(Prediction)', { size: 11, anchor: 'start', cls: 't-mut' });
    s += K.text(outX + 24, 201, 'Output 2', { size: 12, anchor: 'start' }) + K.text(outX + 24, 215, '(Prediction)', { size: 11, anchor: 'start', cls: 't-mut' });
    s += K.text(inX, 22, 'Input Layer', { size: 13, w: 'b' }) + K.text(inX, 38, 'image, sound, text', { size: 11, cls: 't-mut' });
    s += K.text(hidX, 22, 'Hidden Layer', { size: 13, w: 'b' }) + K.text(hidX, 38, 'finds patterns', { size: 11, cls: 't-mut' });
    s += K.text(outX, 22, 'Output Layer', { size: 13, w: 'b' }) + K.text(outX, 38, 'final result', { size: 11, cls: 't-mut' });
    s += arr(30, 284, 410, 284, { cls: 's-acc' });
    s += K.text(220, 278, 'data flows forward', { size: 12, cls: 't-acc' });
    return K.svg(440, 296, s, { title: 'Neural network with input layer, hidden layer, output layer and weighted connections' });
  });

  D.register('xii5.face-unlock', () => {
    let s = '';
    s += K.box(6, 44, 92, 60, 'Camera\nscans face', { c: 1, size: 12.5 });
    s += arr(98, 74, 122, 74);
    s += K.box(122, 44, 92, 60, 'Face\nfeatures', { c: 2, size: 12.5 });
    s += arr(214, 74, 238, 74);
    s += K.box(238, 44, 92, 60, 'Compare with\nstored data', { c: 4, size: 12 });
    s += arr(330, 66, 350, 36);
    s += arr(330, 82, 350, 116);
    s += K.box(350, 12, 84, 46, 'Match:\nunlocked', { c: 5, size: 12 });
    s += K.box(350, 94, 84, 46, 'No match:\nlocked', { c: 3, size: 12 });
    s += K.text(106, 24, 'Neural network studies the face', { size: 12, cls: 't-mut' });
    return K.svg(440, 152, s, { title: 'Face unlock: scan, extract features, compare with stored data, unlock if match' });
  });

  D.register('xii5.model-method', () => {
    let s = '';
    s += K.rect(8, 28, 190, 112, { c: 1 });
    s += K.text(103, 52, 'Neural Network', { size: 14, w: 'b' });
    s += K.text(103, 70, 'MODEL', { size: 12, w: 'b', cls: 't-acc' });
    s += K.text(103, 92, 'layers + nodes +', { size: 12, cls: 't-mut' });
    s += K.text(103, 108, 'connections; takes data,', { size: 12, cls: 't-mut' });
    s += K.text(103, 124, 'gives output', { size: 12, cls: 't-mut' });
    s += K.rect(242, 28, 190, 112, { c: 2 });
    s += K.text(337, 52, 'Deep Learning', { size: 14, w: 'b' });
    s += K.text(337, 70, 'METHOD', { size: 12, w: 'b', cls: 't-acc' });
    s += K.text(337, 92, 'trains NN with many', { size: 12, cls: 't-mut' });
    s += K.text(337, 108, 'hidden layers and', { size: 12, cls: 't-mut' });
    s += K.text(337, 124, 'lots of data', { size: 12, cls: 't-mut' });
    s += arr(242, 84, 198, 84, { cls: 's-acc', w: 2.4 });
    s += K.text(220, 76, 'trains', { size: 12, w: 'b', cls: 't-acc' });
    s += K.text(220, 164, 'Face unlock: the NN studies face features,', { size: 12, cls: 't-mut' });
    s += K.text(220, 180, 'DL trains it with many face images.', { size: 12, cls: 't-mut' });
    return K.svg(440, 192, s, { title: 'Neural network is the model; deep learning is the method that trains it' });
  });

  D.register('xii5.deep-net', () => {
    const xs = [0, 1, 2, 3, 4, 5, 6].map((i) => 30 + i * 60);
    const nodesY = [[90, 130, 170, 210], [90, 130, 170, 210], [90, 130, 170, 210], [90, 130, 170, 210], [90, 130, 170, 210], [90, 130, 170, 210], [110, 190]];
    let s = '';
    for (let l = 0; l < 6; l++) nodesY[l].forEach((a) => nodesY[l + 1].forEach((b) => { s += K.line(xs[l], a, xs[l + 1], b, { cls: 's-mut', w: 0.8 }); }));
    nodesY.forEach((ys, l) => ys.forEach((y) => { s += K.circle(xs[l], y, 11, { c: l === 0 ? 1 : l === 6 ? 5 : 2 }); }));
    s += K.text(30, 44, 'Input', { size: 13, w: 'b' });
    s += K.text(210, 44, 'Hidden layers (many)', { size: 13, w: 'b' });
    s += K.text(390, 44, 'Output', { size: 13, w: 'b' });
    s += K.polyline([[90, 66], [90, 58], [330, 58], [330, 66]], { cls: 's-acc' });
    s += arr(60, 246, 360, 246, { cls: 's-acc' });
    s += K.text(96, 266, 'edges, lines', { size: 12, cls: 't-mut' });
    s += K.text(210, 266, 'shapes, parts', { size: 12, cls: 't-mut' });
    s += K.text(324, 266, 'whole face', { size: 12, cls: 't-mut' });
    return K.svg(440, 278, s, { title: 'Deep neural network: many hidden layers learn from simple to complex features' });
  });

  /* ---------- 5.1.4 components ---------- */

  D.register('xii5.neuron', () => {
    let s = '';
    const ys = [{ y: 62, l: 'x1', w: 'w1' }, { y: 118, l: 'x2', w: 'w2' }, { y: 208, l: 'xn', w: 'wn' }];
    ys.forEach((p) => {
      const ey = 130 + (p.y - 130) * 0.28;
      s += arr(52, p.y, 207, ey, { cls: 's-mut', w: 1.8 });
    });
    s += K.text(129, 70, 'w1', { size: 13, w: 'b', cls: 't-acc' });
    s += K.text(129, 110, 'w2', { size: 13, w: 'b', cls: 't-acc' });
    s += K.text(129, 205, 'wn', { size: 13, w: 'b', cls: 't-acc' });
    ys.forEach((p) => { s += K.circle(34, p.y, 17, { c: 1 }) + K.text(34, p.y, p.l, { size: 13, vmid: true, w: 'b' }); });
    [150, 160, 170].forEach((y) => { s += K.dot(34, y, 2.5); });
    s += K.text(34, 28, 'Inputs', { size: 12.5, w: 'b' });
    s += K.rect(200, 20, 64, 28, { c: 4, r: 6 }) + K.text(232, 34, 'bias b', { size: 13, vmid: true, w: 'b' });
    s += arr(232, 48, 232, 103, { cls: 's-mut', w: 1.8 });
    s += K.circle(232, 130, 26, { c: 3 }) + K.text(232, 130, 'Σ', { size: 24, vmid: true });
    s += K.text(232, 174, 'Summation', { size: 12, cls: 't-mut' });
    s += arr(258, 130, 292, 130, { cls: 's-mut', w: 1.8 });
    s += K.rect(292, 100, 70, 60, { c: 2 });
    s += K.path('M300 146 C 320 146, 326 114, 354 114', { s: 's-brand', w: 3 });
    s += K.text(327, 182, 'Activation', { size: 12, w: 'b' }) + K.text(327, 197, 'function f', { size: 12 });
    s += arr(362, 130, 394, 130, { cls: 's-mut', w: 1.8 });
    s += K.circle(414, 130, 16, { c: 5 }) + K.text(414, 130, 'y', { size: 14, vmid: true, w: 'b' });
    s += K.text(414, 160, 'Output', { size: 12, w: 'b' });
    s += K.text(220, 244, 'y = f( Σ wi · xi + b )', { size: 16, w: 'b', cls: 't-acc' });
    return K.svg(440, 256, s, { title: 'Single neuron: inputs times weights, summed with bias, passed through activation to give output' });
  });

  D.register('xii5.neuron-example', () => {
    let s = '';
    s += K.rect(8, 40, 64, 30, { c: 1, r: 6 }) + K.text(40, 55, 'x1 = 2', { size: 13, vmid: true, w: 'b' });
    s += K.rect(8, 130, 64, 30, { c: 1, r: 6 }) + K.text(40, 145, 'x2 = 3', { size: 13, vmid: true, w: 'b' });
    s += arr(72, 58, 164, 90, { cls: 's-mut', w: 1.8 });
    s += arr(72, 142, 164, 110, { cls: 's-mut', w: 1.8 });
    s += K.text(104, 54, 'w1 = 0.5', { size: 12, w: 'b', cls: 't-acc' });
    s += K.text(104, 150, 'w2 = 0.4', { size: 12, w: 'b', cls: 't-acc' });
    s += K.circle(190, 100, 26, { c: 3 }) + K.text(190, 100, 'Σ', { size: 24, vmid: true });
    s += K.rect(160, 176, 60, 28, { c: 4, r: 6 }) + K.text(190, 190, 'b = −1', { size: 13, vmid: true, w: 'b' });
    s += arr(190, 176, 190, 128, { cls: 's-mut', w: 1.8 });
    s += arr(216, 100, 252, 100, { cls: 's-mut', w: 1.8 });
    s += K.rect(252, 12, 182, 176, { c: 6, r: 10 });
    const L = (y, t, o) => K.text(266, y, t, Object.assign({ size: 13, anchor: 'start' }, o || {}));
    s += L(34, 'Step 1: multiply', { w: 'b', cls: 't-acc' });
    s += L(54, '2 × 0.5 = 1.0');
    s += L(72, '3 × 0.4 = 1.2');
    s += L(98, 'Step 2: add', { w: 'b', cls: 't-acc' });
    s += L(116, '1.0 + 1.2 = 2.2');
    s += L(142, 'Step 3: add bias', { w: 'b', cls: 't-acc' });
    s += L(160, '2.2 + (−1) = 1.2');
    s += L(180, 'Step 4: step f(1.2) = 1', { w: 'b', cls: 't-grn' });
    s += K.text(220, 226, 'Output y = 1  (the neuron fires)', { size: 14, w: 'b', cls: 't-grn' });
    return K.svg(440, 240, s, { title: 'Worked neuron example: x1=2, x2=3, w1=0.5, w2=0.4, b=-1 gives sum 1.2 and step output 1' });
  });

  D.register('xii5.activation', () => {
    let s = '';
    const panel = (px, title, curve, l1, l2) => {
      const ox = px + 62, base = 120, top = 54;
      let o = K.text(px + 62, 22, title, { size: 14, w: 'b' });
      o += K.line(px + 6, base, px + 118, base, { arrow: true, cls: 's-mut' });
      o += K.line(ox, base + 4, ox, 36, { arrow: true, cls: 's-mut' });
      o += K.line(ox - 4, top, px + 118, top, { cls: 's-mut', dash: '3 4', w: 1 });
      o += K.text(ox - 8, top + 4, '1', { size: 12, anchor: 'end', cls: 't-mut' });
      o += K.text(ox - 8, base - 2, '0', { size: 12, anchor: 'end', cls: 't-mut' });
      o += K.text(px + 118, base + 15, 'x', { size: 12, anchor: 'end', cls: 't-mut' });
      o += K.path(curve(ox, base, top), { s: 's-brand', w: 3 });
      o += K.text(px + 62, 160, l1, { size: 12.5, w: 'b' });
      o += K.text(px + 62, 177, l2, { size: 12, cls: 't-mut' });
      return o;
    };
    s += panel(2, 'Step', (ox, b, t) => 'M' + (ox - 54) + ' ' + b + ' L' + ox + ' ' + b + ' L' + ox + ' ' + t + ' L' + (ox + 54) + ' ' + t, 'output 0 or 1', 'yes / no decision');
    s += panel(135, 'Sigmoid', (ox, b, t) => {
      let d = '';
      for (let x = -54; x <= 54; x += 3) {
        const y = b - (b - t) / (1 + Math.exp(-x / 11));
        d += (x === -54 ? 'M' : 'L') + (ox + x).toFixed(1) + ' ' + y.toFixed(1) + ' ';
      }
      return d;
    }, 'smooth, 0 to 1', 'like a probability');
    s += panel(268, 'ReLU', (ox, b, t) => 'M' + (ox - 54) + ' ' + b + ' L' + ox + ' ' + b + ' L' + (ox + 54) + ' ' + (b - 66), 'max(0, x)', 'negative becomes 0');
    return K.svg(400, 184, s, { title: 'Activation functions: step, sigmoid and ReLU curves' });
  });

  D.register('xii5.nn-components', () => {
    const inX = 56, hidX = 176, outX = 296;
    const ins = [70, 112, 154], hid = [70, 112, 154], outs = [91, 133];
    let s = '';
    ins.forEach((a) => hid.forEach((b) => { s += K.line(inX, a, hidX, b, { cls: 's-mut', w: 1 }); }));
    hid.forEach((a) => outs.forEach((b) => { s += K.line(hidX, a, outX, b, { cls: 's-mut', w: 1 }); }));
    s += K.line(hidX, 198, hidX, 168, { cls: 's-acc', dash: '3 3' });
    ins.forEach((y) => { s += K.circle(inX, y, 14, { c: 1 }); });
    hid.forEach((y) => { s += K.circle(hidX, y, 14, { c: 2 }) + K.text(hidX, y, 'Σf', { size: 11, vmid: true }); });
    outs.forEach((y) => { s += K.circle(outX, y, 14, { c: 5 }); });
    s += K.circle(hidX, 198, 12, { c: 4 }) + K.text(hidX, 198, '+1', { size: 11, vmid: true, w: 'b' });
    s += K.rect(342, 86, 92, 52, { c: 3, r: 8 }) + K.text(388, 112, 'Loss\nfunction', { size: 12.5, vmid: true, w: 'b' });
    s += arr(310, 112, 342, 112, { cls: 's-mut' });
    s += K.rect(100, 96, 44, 18, { c: 4, r: 5 }) + K.text(122, 105, '0.8', { size: 11.5, vmid: true, w: 'b' });
    s += K.text(inX, 28, 'Input', { size: 12.5, w: 'b' });
    s += K.text(hidX, 28, 'Hidden', { size: 12.5, w: 'b' });
    s += K.text(outX, 28, 'Output', { size: 12.5, w: 'b' });
    s += badge(inX, 44, 1, 0) + badge(hidX, 44, 3, 0) + badge(outX, 44, 7, 0) + badge(388, 74, 8, 0);
    s += badge(inX + 22, 80, 2, 0) + badge(122, 124, 4, 0) + badge(hidX + 24, 198, 5, 0) + badge(hidX + 26, 128, 6, 0);
    s += K.polyline([[388, 138], [388, 226], [56, 226], [56, 172]], { cls: 's-red', dash: '4 4', arrow: true });
    s += K.text(220, 214, 'error feedback: weights improve', { size: 12, cls: 't-red' });
    const leg = ['1 Input layer: data in', '2 Neurons / nodes', '3 Hidden layer: patterns', '4 Weights: importance', '5 Bias: adjusts result', '6 Activation: pass or not', '7 Output layer: prediction', '8 Loss: how wrong?'];
    leg.forEach((t, i) => {
      const x = 8 + (i % 2) * 220, y = 252 + Math.floor(i / 2) * 24;
      s += K.text(x, y, t, { size: 12.5, anchor: 'start' });
    });
    return K.svg(440, 352, s, { title: 'Components of a neural network numbered one to eight' });
  });

  D.register('xii5.dl-components', () => {
    let s = '';
    const box = [['Large\nInput Data', 1], ['Deep Neural\nNetwork', 2], ['Training\nProcess', 4], ['Accurate\nPrediction', 5]];
    box.forEach((b, i) => {
      const x = 6 + i * 115;
      s += K.box(x, 8, 88, 52, b[0], { c: b[1], size: 12 });
      if (i < 3) s += arr(x + 88, 34, x + 115, 34);
    });
    const items = [
      ['1 Large Input Data', 'needs lots of data', 1], ['2 Many Hidden Layers', 'learn deeper patterns', 2],
      ['3 Deep Neural Network', 'several layers', 2], ['4 Automatic Feature Learning', 'finds features by itself', 0],
      ['5 Training Process', 'trained again and again', 4], ['6 Learning Algorithm', 'reduces mistakes', 4],
      ['7 High Computing Power', 'strong computers, GPUs', 7], ['8 Large-Scale Applications', 'face unlock, translation', 5],
    ].map((a) => ({ t: a[0], d: a[1], c: a[2] }));
    s += chips(items, { cols: 2, w: 214, h: 44, gap: 6, y0: 76, ty: 18, dy: 34, tsize: 12.5, dsize: 11.5, left: true, pad: 10 });
    return K.svg(440, 76 + 4 * 50 + 4, s, { title: 'Eight components of deep learning and the data to prediction pipeline' });
  });

  /* ---------- 5.1 Pakistan + 5.2 applications ---------- */

  D.register('xii5.pakistan-fields', () => {
    const items = [
      { t: 'Education', d: 'smart tutoring', c: 1 }, { t: 'Healthcare', d: 'disease detection', c: 3 }, { t: 'Agriculture', d: 'crops, weather, yield', c: 5 },
      { t: 'Business & Banking', d: 'fraud and risk', c: 4 }, { t: 'Language', d: 'Urdu, Sindhi tools', c: 2 }, { t: 'Government', d: 'traffic, smart cities', c: 0 },
    ];
    return K.svg(440, 216, hub('ML, NN\n& DL in\nPakistan', items, { cc: 7 }), { title: 'Future uses of machine learning and deep learning in Pakistan' });
  });

  D.register('xii5.applications', () => {
    const items = [
      ['Image Recognition', 'face unlock, photo search', 1], ['Speech Recognition', 'voice assistant, alarm', 2],
      ['Natural Language (NLP)', 'translators, chatbots', 0], ['Healthcare Systems', 'X-ray, CT, MRI analysis', 3],
      ['Recommendation', 'videos, products', 4], ['Autonomous Vehicles', 'roads, signals, people', 7],
      ['Fraud Detection', 'unusual transactions', 3], ['Assistive Technologies', 'speech-to-text, captions', 5],
    ].map((a) => ({ t: a[0], d: a[1], c: a[2] }));
    let s = K.rect(6, 6, 428, 34, { c: 6 }) + K.text(220, 23, 'Neural Networks and Deep Learning at work', { size: 13.5, w: 'b', vmid: true });
    s += chips(items, { cols: 2, w: 210, h: 54, gap: 8, y0: 50, ty: 22, dy: 41, tsize: 13, dsize: 12 });
    return K.svg(440, 50 + 4 * 62, s, { title: 'Eight applications of neural networks and deep learning' });
  });

  D.register('xii5.speech-pipeline', () => {
    let s = K.rect(110, 6, 220, 28, { c: 6, r: 14 }) + K.text(220, 20, '"Set an alarm for six AM"', { size: 13, vmid: true, w: 'b' });
    const b = [['Voice\ninput', 1], ['Speech\nRecognition', 2], ['NLP\nunderstands', 0], ['Action:\nalarm set', 5]];
    b.forEach((x, i) => {
      const bx = 6 + i * 115;
      s += K.box(bx, 56, 88, 58, x[0], { c: x[1], size: 12.5 });
      if (i < 3) s += arr(bx + 88, 85, bx + 115, 85);
    });
    s += K.text(6 + 115 + 44, 134, 'voice to text', { size: 12, cls: 't-mut' });
    s += K.text(6 + 230 + 44, 134, 'meaning of words', { size: 12, cls: 't-mut' });
    return K.svg(440, 144, s, { title: 'Voice assistant: speech recognition then NLP then action' });
  });

  D.register('xii5.fraud', () => {
    let s = '';
    const base = 182, sc = 140 / 25000;
    s += K.line(30, base, 340, base, { cls: 's-mut' }) + K.line(30, base, 30, 24, { cls: 's-mut' });
    const bars = [['Mon', 1200], ['Tue', 800], ['Wed', 1500], ['Thu', 1000], ['Fri', 1300], ['Sat', 25000]];
    bars.forEach((b, i) => {
      const x = 44 + i * 48, h = b[1] * sc, big = b[1] > 5000;
      s += K.rect(x, base - h, 34, h, { c: big ? 3 : 1, r: 2, s: big ? 's-red' : '' });
      s += K.text(x + 17, base - h - 6, String(b[1]).replace(/\B(?=(\d{3})+$)/, ','), { size: 11.5, w: big ? 'b' : '', cls: big ? 't-red' : '' });
      s += K.text(x + 17, base + 16, b[0], { size: 12, cls: 't-mut' });
    });
    s += K.text(36, 18, 'Spending (PKR)', { size: 12, anchor: 'start', cls: 't-mut' });
    s += K.rect(350, 50, 84, 74, { c: 3, r: 10, s: 's-red' });
    s += K.text(392, 70, 'ALERT', { size: 14, w: 'b', cls: 't-red' });
    s += K.text(392, 88, 'Suspicious', { size: 12 }) + K.text(392, 103, 'activity', { size: 12 });
    s += arr(318, 70, 350, 86, { cls: 's-red' });
    s += K.text(220, 226, 'Normal pattern learned  →  sudden large amount flagged', { size: 12, cls: 't-mut' });
    return K.svg(440, 234, s, { title: 'Fraud detection: normal small daily spending then a sudden PKR 25,000 transaction triggers an alert' });
  });

  /* ---------- 5.3 secure collaboration ---------- */

  D.register('xii5.secure-pillars', () => {
    let s = K.rect(6, 6, 428, 38, { c: 1, r: 10 }) + K.text(220, 25, 'Secure Collaboration', { size: 15, w: 'b', vmid: true });
    s += arr(220, 44, 220, 56, { cls: 's-mut' });
    const rows = [
      ['Authentication', 'Who are you? (password, OTP)', 0], ['Access Control', 'What may you do? (view, edit)', 1],
      ['Accountability', 'Who did what? (tracking)', 2], ['Data Privacy', 'Use data only for its purpose', 4],
      ['Safe Communication', 'Only enrolled users see messages', 5],
    ];
    rows.forEach((r, i) => {
      const y = 60 + i * 46;
      s += K.rect(6, y, 428, 40, { c: r[2], r: 8 });
      s += badge(26, y + 20, i + 1, 6);
      s += K.text(44, y + 20, r[0], { size: 13.5, w: 'b', vmid: true, anchor: 'start' });
      s += K.text(428, y + 20, r[1], { size: 12, vmid: true, anchor: 'end', cls: 't-mut' });
    });
    return K.svg(440, 60 + 5 * 46, s, { title: 'Five parts of secure collaboration' });
  });

  D.register('xii5.auth-access', () => {
    let s = '';
    s += K.box(6, 22, 118, 66, 'User logs in\npassword / OTP', { c: 1, size: 12 });
    s += arr(124, 55, 158, 55);
    s += K.rect(158, 22, 122, 66, { c: 2 });
    s += K.text(219, 42, '1 Authentication', { size: 12.5, w: 'b' }) + K.text(219, 62, 'Who are you?', { size: 12, cls: 't-mut' }) + K.text(219, 78, 'identity verified', { size: 11.5, cls: 't-mut' });
    s += arr(280, 55, 314, 55);
    s += K.rect(314, 22, 120, 66, { c: 4 });
    s += K.text(374, 42, '2 Access Control', { size: 12.5, w: 'b' }) + K.text(374, 62, 'What may you do?', { size: 12, cls: 't-mut' }) + K.text(374, 78, 'permission level', { size: 11.5, cls: 't-mut' });
    s += K.text(220, 120, 'Shared Google Docs file', { size: 13, w: 'b', cls: 't-acc' });
    s += K.line(374, 88, 374, 106, { cls: 's-mut', dash: '3 3' }) + K.line(374, 106, 330, 106, { cls: 's-mut', dash: '3 3' });
    s += K.box(6, 134, 136, 46, 'Students:\nView only', { c: 1, size: 12.5 });
    s += K.box(152, 134, 136, 46, 'Group leaders:\nEdit', { c: 5, size: 12.5 });
    s += K.box(298, 134, 136, 46, 'Outsiders:\nNo access', { c: 3, size: 12.5 });
    return K.svg(440, 192, s, { title: 'Authentication confirms identity; access control decides permissions on a shared document' });
  });

  D.register('xii5.encryption', (args) => {
    const asym = args && args.type === 'asym';
    let s = K.text(220, 20, asym ? 'Asymmetric: public key + private key' : 'Symmetric: one same key', { size: 14, w: 'b' });
    s += K.box(6, 46, 82, 54, 'Readable\n"Hello"', { c: 1, size: 12 });
    s += arr(88, 73, 162, 73);
    s += K.text(125, 64, 'Encrypt', { size: 12, w: 'b' });
    s += K.box(162, 46, 116, 54, 'Ciphertext\nx9#Qk2', { c: 3, size: 12.5 });
    s += arr(278, 73, 352, 73);
    s += K.text(315, 64, 'Decrypt', { size: 12, w: 'b' });
    s += K.box(352, 46, 82, 54, 'Readable\n"Hello"', { c: 1, size: 12 });
    const key = (cx, label) => K.line(cx, 76, cx, 112, { cls: 's-mut', dash: '3 3' }) + K.rect(cx - 36, 112, 72, 30, { c: 4, r: 8 }) + K.text(cx, 127, label, { size: 12, vmid: true, w: 'b' });
    s += key(125, asym ? 'Public key' : 'Secret key');
    s += key(315, asym ? 'Private key' : 'Secret key');
    s += K.text(220, 170, asym ? 'Public key locks the data, private key unlocks it.' : 'The same key locks and unlocks the data.', { size: 12.5, cls: 't-mut' });
    return K.svg(440, 184, s, { title: asym ? 'Asymmetric encryption with public and private keys' : 'Symmetric encryption with one shared key' });
  });

  D.register('xii5.backup', () => {
    let s = '';
    s += K.rect(8, 40, 140, 78, { c: 1 });
    s += K.text(78, 66, 'Main computer', { size: 13, w: 'b' }) + K.text(78, 86, 'student records', { size: 12, cls: 't-mut' });
    s += K.rect(292, 40, 140, 78, { c: 5 });
    s += K.text(362, 62, 'Cloud storage', { size: 13, w: 'b' }) + K.text(362, 80, 'or external', { size: 12, cls: 't-mut' }) + K.text(362, 96, 'drive', { size: 12, cls: 't-mut' });
    s += arr(148, 62, 292, 62, { cls: 's-grn', w: 2.2 });
    s += K.text(220, 54, 'Backup (copy)', { size: 12.5, w: 'b', cls: 't-grn' });
    s += arr(292, 98, 148, 98, { cls: 's-acc', w: 2.2 });
    s += K.text(220, 118, 'Recovery (restore)', { size: 12.5, w: 'b', cls: 't-acc' });
    s += K.line(112, 94, 134, 114, { cls: 's-red', w: 3 }) + K.line(134, 94, 112, 114, { cls: 's-red', w: 3 });
    s += K.text(78, 28, 'crash / deleted / malware', { size: 12, cls: 't-red' });
    s += K.text(220, 156, 'Backup = copy kept elsewhere.  Recovery = bring data back.', { size: 12, cls: 't-mut' });
    return K.svg(440, 168, s, { title: 'Backup copies data to safe storage and recovery restores it after failure' });
  });

  D.register('xii5.cia', () => {
    let s = '';
    s += K.poly([[220, 64], [80, 206], [360, 206]], { c: 6 });
    s += K.dot(220, 64, 6) + K.dot(80, 206, 6) + K.dot(360, 206, 6);
    s += K.text(220, 138, 'DATA', { size: 18, w: 'b' });
    s += K.text(220, 158, 'secure and accurate', { size: 12, cls: 't-mut' });
    s += K.text(220, 174, 'available to the right people', { size: 12, cls: 't-mut' });
    s += K.rect(140, 4, 160, 46, { c: 1 }) + K.text(220, 22, 'Confidentiality', { size: 13.5, w: 'b' }) + K.text(220, 40, 'only allowed users', { size: 12, cls: 't-mut' });
    s += K.rect(4, 216, 170, 46, { c: 5 }) + K.text(89, 234, 'Integrity', { size: 13.5, w: 'b' }) + K.text(89, 252, 'accurate, not changed', { size: 12, cls: 't-mut' });
    s += K.rect(266, 216, 170, 46, { c: 4 }) + K.text(351, 234, 'Availability', { size: 13.5, w: 'b' }) + K.text(351, 252, 'ready when needed', { size: 12, cls: 't-mut' });
    return K.svg(440, 268, s, { title: 'CIA triad: confidentiality, integrity, availability' });
  });

  /* ---------- 5.4 threats and mitigation ---------- */

  D.register('xii5.threats-map', () => {
    const items = [
      { t: 'Malware', d: 'harmful software' }, { t: 'Phishing', d: 'tricks you for info' }, { t: 'Unauthorized Access', d: 'entry, no permission' },
      { t: 'Data / Identity Theft', d: 'steal data, CNIC' }, { t: 'Denial of Service', d: 'flood of fake requests' }, { t: 'Human Error', d: 'mistakes by users' },
    ].map((x, i) => Object.assign(x, { c: 3 }));
    return K.svg(440, 216, hub('Your data\n& system', items, { cc: 4 }), { title: 'Six common security threats around your data and system' });
  });

  D.register('xii5.phishing-email', () => {
    let s = K.rect(6, 6, 290, 300, { c: 6, r: 10 });
    s += K.rect(6, 6, 290, 28, { c: 1, r: 10 });
    s += K.text(16, 21, 'New message', { size: 12.5, w: 'b', vmid: true, anchor: 'start' });
    const L = (y, t, o) => K.text(16, y, t, Object.assign({ size: 12, anchor: 'start' }, o || {}));
    s += L(58, 'From: it-office@gcollege-update.co');
    s += L(80, 'Subject: URGENT! Verify in 1 hour', { w: 'b' });
    s += K.line(14, 94, 288, 94, { cls: 's-mut', w: 1 });
    s += L(120, 'Dear student,');
    s += L(142, 'Your admission record will be');
    s += L(160, 'blocked today. Send your password');
    s += L(178, 'and OTP to update it.');
    s += L(206, 'Click: http://gc-admission.xyz/login', { cls: 't-acc' });
    s += L(234, 'Attachment: form.exe', { cls: 't-red' });
    s += L(276, 'IT Office');
    const marks = [[54, 1], [76, 2], [168, 3], [202, 4], [230, 5]];
    marks.forEach((m) => { s += badge(278, m[0], m[1], 3); });
    const leg = ['Unknown sender\naddress', 'Urgency: act\nquickly', 'Asks password\nand OTP', 'Strange link', 'Unexpected\nattachment'];
    leg.forEach((t, i) => {
      const y = 30 + i * 56;
      s += badge(322, y + 10, i + 1, 3);
      s += K.text(340, y + 6, t, { size: 12, anchor: 'start', vmid: false });
    });
    s += K.text(370, 296, 'Red flags', { size: 12.5, w: 'b', cls: 't-red' });
    return K.svg(440, 312, s, { title: 'Phishing email with five red flags marked' });
  });

  D.register('xii5.dos', () => {
    let s = '';
    s += K.text(10, 18, 'Fake requests from attacker', { size: 12.5, w: 'b', anchor: 'start', cls: 't-red' });
    [38, 66, 94, 122].forEach((y) => {
      s += arr(40, y, 292, 104, { cls: 's-red', w: 1.2 });
    });
    [38, 66, 94, 122].forEach((y) => { s += K.circle(30, y, 10, { c: 3 }); });
    s += K.rect(296, 62, 138, 84, { c: 1, r: 10 });
    s += K.text(365, 90, 'Online exam', { size: 13, w: 'b' }) + K.text(365, 107, 'website', { size: 13, w: 'b' });
    s += K.text(365, 130, 'overloaded', { size: 12, cls: 't-red' });
    s += K.rect(10, 170, 112, 36, { c: 5, r: 8 }) + K.text(66, 188, 'Real student', { size: 12.5, w: 'b', vmid: true });
    s += arr(122, 188, 296, 140, { cls: 's-mut', dash: '5 4' });
    s += K.line(196, 154, 218, 174, { cls: 's-red', w: 3 }) + K.line(218, 154, 196, 174, { cls: 's-red', w: 3 });
    s += K.text(330, 190, 'Real users cannot get in', { size: 12, cls: 't-red' });
    return K.svg(440, 218, s, { title: 'Denial of service: flood of fake requests blocks real users from the website' });
  });

  D.register('xii5.layers', () => {
    let s = '';
    const names = ['User awareness', 'Firewall', 'Antivirus', 'Strong password + 2FA', 'Encryption'];
    const cs = [6, 1, 0, 2, 4];
    names.forEach((n, k) => {
      const x = 56 + 24 * k, y = 6 + 24 * k;
      s += K.rect(x, y, 378 - 48 * k, 304 - 48 * k, { c: cs[k], r: 10 });
      s += K.text(245, y + 17, n, { size: 13, w: 'b' });
    });
    s += K.rect(176, 126, 138, 66, { c: 5, r: 10 });
    s += K.text(245, 150, 'DATA', { size: 16, w: 'b' }) + K.text(245, 176, 'backed up', { size: 12, cls: 't-mut' });
    s += arr(6, 160, 176, 160, { cls: 's-red', w: 2.4 });
    s += K.text(30, 148, 'Attack', { size: 13, w: 'b', cls: 't-red' });
    return K.svg(440, 316, s, { title: 'Layered defence: awareness, firewall, antivirus, passwords with 2FA, encryption, around backed-up data' });
  });

  D.register('xii5.twofa', () => {
    let s = '';
    s += K.rect(6, 12, 124, 66, { c: 1 }) + K.text(68, 34, 'Step 1', { size: 12, w: 'b', cls: 't-acc' }) + K.text(68, 54, 'Password', { size: 13.5, w: 'b' }) + K.text(68, 70, 'something you know', { size: 11, cls: 't-mut' });
    s += arr(130, 45, 158, 45);
    s += K.rect(158, 12, 124, 66, { c: 4 }) + K.text(220, 34, 'Step 2', { size: 12, w: 'b', cls: 't-acc' }) + K.text(220, 54, 'OTP on phone', { size: 13.5, w: 'b' }) + K.text(220, 70, 'something you have', { size: 11, cls: 't-mut' });
    s += arr(282, 45, 310, 45);
    s += K.box(310, 12, 124, 66, 'Access\ngranted', { c: 5, size: 13.5, bold: true });
    s += K.rect(6, 108, 142, 44, { c: 3 }) + K.text(77, 123, 'Attacker has', { size: 12 }) + K.text(77, 140, 'only the password', { size: 12 });
    s += arr(148, 130, 190, 130, { cls: 's-red' });
    s += K.rect(190, 108, 150, 44, { c: 3, s: 's-red' }) + K.text(265, 123, 'Blocked at step 2', { size: 12.5, w: 'b', cls: 't-red' }) + K.text(265, 140, 'no OTP, no entry', { size: 12, cls: 't-mut' });
    s += K.line(220, 80, 250, 106, { cls: 's-red', dash: '3 3' });
    return K.svg(440, 162, s, { title: 'Two-factor authentication needs password and OTP; attacker with password alone is blocked' });
  });

  /* ---------- 5.5 equity ---------- */

  D.register('xii5.equity', () => {
    let s = '';
    const fig = (cx, c) => K.circle(cx, 84, 10, { c }) + K.line(cx, 94, cx, 124) + K.line(cx - 13, 106, cx + 13, 106) + K.line(cx, 124, cx - 10, 146) + K.line(cx, 124, cx + 10, 146);
    s += K.rect(4, 6, 212, 214, { c: 6, r: 10 }) + K.rect(224, 6, 212, 214, { c: 6, r: 10 });
    s += K.text(110, 28, 'Equal access', { size: 14, w: 'b' }) + K.text(110, 46, 'same opportunity for all', { size: 12, cls: 't-mut' });
    s += K.text(330, 28, 'Equity', { size: 14, w: 'b' }) + K.text(330, 46, 'extra support by need', { size: 12, cls: 't-mut' });
    [44, 110, 176].forEach((x, i) => { s += fig(x, 1); });
    [264, 330, 396].forEach((x, i) => { s += fig(x, 5); });
    s += K.rect(14, 166, 192, 34, { c: 1, r: 8 }) + K.text(110, 183, 'same tool, same link', { size: 12.5, vmid: true, w: 'b' });
    [['captions', 228], ['mobile app', 297], ['recording', 366]].forEach((c) => {
      s += K.rect(c[1], 166, 66, 34, { c: 5, r: 8 }) + K.text(c[1] + 33, 183, c[0], { size: 11, vmid: true, w: 'b' });
    });
    return K.svg(440, 228, s, { title: 'Equal access gives the same tool to all; equity adds support such as captions, mobile app and recordings' });
  });

  D.register('xii5.collab-tools', () => {
    const items = [
      ['Google Docs', 'write, edit, comment,\nshare in real time', 1], ['Zoom', 'meetings, classes,\nscreen sharing', 2],
      ['Microsoft Teams', 'meetings, file sharing,\nclass groups', 0], ['Classroom / LMS', 'lectures, assignments,\nquizzes', 4],
      ['WhatsApp', 'quick announcements\n(approved groups)', 5], ['Email', 'formal notices,\nattachments, records', 7],
    ].map((a) => ({ t: a[0], d: a[1], c: a[2] }));
    return K.svg(440, 6 + 2 * 100 + 6, chips(items, { cols: 3, w: 138, h: 94, gap: 7, ty: 24, dy: 46, tsize: 13, dsize: 11.5, lh: 15 }), { title: 'Six digital collaboration tools and what they are used for' });
  });

  D.register('xii5.checklist', () => {
    const rows = [
      'Verify identity: strong password + 2FA', 'Give least permission: view, comment, edit',
      'Share files only with the right people', 'Use the official LMS or approved groups',
      'Never share OTP or password with anyone', 'Keep antivirus updated; take backups',
      'Think before clicking links or files', 'Include all: captions, recordings, mobile apps',
    ];
    let s = '';
    rows.forEach((t, i) => {
      const y = 6 + i * 36;
      s += K.rect(6, y, 428, 30, { c: i % 2 ? 6 : 0, r: 8 });
      s += K.circle(26, y + 15, 10, { c: 5, s: 's-grn' });
      s += K.polyline([[21, y + 15], [25, y + 19], [32, y + 11]], { cls: 's-grn', w: 2.6 });
      s += K.text(46, y + 15, t, { size: 13, vmid: true, anchor: 'start' });
    });
    return K.svg(440, 6 + 8 * 36, s, { title: 'Secure collaboration checklist with eight ticked items' });
  });

  D.register('xii5.careers', () => {
    const items = [
      ['Machine Learning Engineer', 'builds and trains NN models', 1], ['AI Researcher', 'new AI and DL techniques', 2],
      ['Cybersecurity Analyst', 'watches for malware, phishing', 3], ['Ethical Hacker / Pen Tester', 'legally tests for weaknesses', 4],
      ['Data Privacy Officer', 'follows privacy principles', 7], ['IT Security Consultant', 'advises on firewalls, encryption', 5],
    ].map((a) => ({ t: a[0], d: a[1], c: a[2] }));
    return K.svg(440, 6 + 3 * 66, chips(items, { cols: 2, w: 212, h: 58, gap: 8, ty: 22, dy: 41, tsize: 12.5, dsize: 11.5 }), { title: 'Six career opportunities in AI and cybersecurity' });
  });
})();
