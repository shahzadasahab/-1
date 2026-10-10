/* XI Ch2 (Computational Thinking & Algorithms) diagrams */
(function () {
  const D = Diagrams;
  const W = 440;
  const NB = '\u00a0';

  /* ---------- shared helpers ---------- */
  const ST = {
    n: { c: 6 },
    cmp: { c: 4, s: 's-acc' },
    swp: { c: 3, s: 's-red' },
    ok: { c: 5, s: 's-grn' },
    key: { c: 1, s: 's-brand' },
    out: { c: null, dash: '3 3', tcls: 't-mut' },
    in: { c: 1 },
  };

  function cell(x, y, w, h, label, code, size) {
    const st = ST[code] || ST.n;
    return K.box(x, y, w, h, String(label), { c: st.c, s: st.s, dash: st.dash, tcls: st.tcls, r: 5, size: size || 14, bold: true });
  }

  function legend(y, items) {
    const step = (W - 16) / items.length;
    let s = '';
    items.forEach((it, i) => {
      const x = 10 + i * step;
      const st = ST[it[0]];
      s += K.rect(x, y - 10, 12, 12, { c: st.c, s: st.s, r: 3, dash: st.dash });
      s += K.text(x + 17, y, it[1], { size: 11, anchor: 'start', cls: 't-mut' });
    });
    return s;
  }

  /* rows: [{lab, arr, st, right, rc}] ; array boxes in the middle, label left, result right */
  function trace(title, rows, leg, extra) {
    const n = rows[0].arr.length;
    const bw = 38;
    const gap = 4;
    const x0 = 126;
    const rh = 36;
    let s = K.text(W / 2, 18, title, { size: 14, w: 'b' });
    rows.forEach((r, i) => {
      const y = 30 + i * rh;
      s += K.text(10, y + 20, r.lab, { size: 12, anchor: 'start', cls: r.lcls || 't-mut' });
      for (let j = 0; j < n; j++) s += cell(x0 + j * (bw + gap), y + 2, bw, 30, r.arr[j], r.st[j]);
      if (r.right) s += K.text(x0 + n * (bw + gap) + 6, y + 20, r.right, { size: 12, anchor: 'start', w: 'b', cls: r.rc || 't-mut' });
    });
    let h = 30 + rows.length * rh + 8;
    if (extra) {
      s += K.text(W / 2, h + 12, extra, { size: 13, w: 'b', cls: 't-acc' });
      h += 24;
    }
    s += legend(h + 14, leg);
    return K.svg(W, h + 28, s, { title: title });
  }

  /* ---------- simulations ---------- */
  function bubbleSim(data) {
    const a = data.slice();
    const n = a.length;
    const passes = [];
    for (let p = 1; p < n; p++) {
      const rows = [];
      const fixedFrom = n - (p - 1);
      const base = () => a.map((_, i) => (i >= fixedFrom ? 'ok' : 'n'));
      rows.push({ lab: 'Start of pass ' + p, arr: a.slice(), st: base() });
      let swaps = 0;
      for (let i = 0; i < n - p; i++) {
        const x = a[i];
        const y = a[i + 1];
        const sw = x > y;
        if (sw) {
          a[i] = y;
          a[i + 1] = x;
          swaps++;
        }
        const st = base();
        st[i] = st[i + 1] = sw ? 'swp' : 'cmp';
        rows.push({ lab: x + ' > ' + y + ' ?', arr: a.slice(), st, right: sw ? 'swap' : 'no swap', rc: sw ? 't-red' : 't-grn', lcls: '' });
      }
      const st = a.map((_, i) => (i >= n - p || p === n - 1 ? 'ok' : 'n'));
      rows.push({ lab: 'End of pass ' + p, arr: a.slice(), st, right: swaps + (swaps === 1 ? ' swap' : ' swaps') });
      passes.push({ rows, swaps, arr: a.slice(), st });
    }
    return passes;
  }

  function selectionSim(data) {
    const a = data.slice();
    const n = a.length;
    const passes = [];
    for (let k = 0; k < n - 1; k++) {
      const rows = [];
      const base = () => a.map((_, i) => (i < k ? 'ok' : 'n'));
      rows.push({ lab: 'Start of pass ' + (k + 1), arr: a.slice(), st: base() });
      let swaps = 0;
      for (let p = k + 1; p < n; p++) {
        const x = a[k];
        const y = a[p];
        const sw = x > y;
        if (sw) {
          a[k] = y;
          a[p] = x;
          swaps++;
        }
        const st = base();
        st[k] = 'key';
        st[p] = sw ? 'swp' : 'cmp';
        rows.push({ lab: x + ' > ' + y + ' ?', arr: a.slice(), st, right: sw ? 'swap' : 'no swap', rc: sw ? 't-red' : 't-grn', lcls: '' });
      }
      const st = a.map((_, i) => (i <= k || k === n - 2 ? 'ok' : 'n'));
      rows.push({ lab: 'End of pass ' + (k + 1), arr: a.slice(), st, right: swaps + (swaps === 1 ? ' swap' : ' swaps') });
      passes.push({ rows, swaps, arr: a.slice(), st });
    }
    return passes;
  }

  const DATA = [8, 4, 1, 9, 3];

  /* ---------- 1. Computational thinking overview ---------- */
  D.register('xi2.ct-pillars', () => {
    let s = '';
    const ys = [10, 72, 134, 196];
    const items = [
      ['1. Decomposition', 'break into small parts', 1],
      ['2. Pattern Recognition', 'find what repeats', 0],
      ['3. Abstraction', 'hide extra details', 2],
      ['4. Algorithm Design', 'write the steps', 5],
    ];
    ys.forEach((y, i) => {
      s += K.line(92, 125, 138, y + 23, { arrow: true, cls: 's-mut' });
      s += K.line(302, y + 23, 346, 125, { arrow: true, cls: 's-mut' });
    });
    ys.forEach((y, i) => {
      s += K.rect(140, y, 162, 46, { c: items[i][2], r: 8 });
      s += K.text(221, y + 20, items[i][0], { size: 13, w: 'b' });
      s += K.text(221, y + 36, items[i][1], { size: 11, cls: 't-mut' });
    });
    s += K.box(8, 95, 84, 60, 'Real-world\nProblem', { c: 3, size: 13, bold: true });
    s += K.box(348, 95, 84, 60, 'Solution\n(Program)', { c: 4, size: 13, bold: true });
    return K.svg(W, 256, s, { title: 'Computational thinking: decomposition, pattern recognition, abstraction and algorithm design turn a problem into a solution' });
  });

  /* ---------- 2. Algorithm / pseudocode / code ---------- */
  D.register('xi2.three-forms', () => {
    let s = '';
    const rows = [
      ['Algorithm', 'plain steps', 0, ['1. Take two numbers a and b', '2. Compare them', '3. The bigger one is the answer']],
      ['Pseudocode', 'no syntax', 1, ['INPUT a, b', 'IF a > b THEN', NB.repeat(4) + 'DISPLAY a', 'ELSE', NB.repeat(4) + 'DISPLAY b', 'ENDIF']],
      ['Program', 'real Python code', 2, ['a = int(input())', 'b = int(input())', 'if a > b:', NB.repeat(4) + 'print(a)', 'else:', NB.repeat(4) + 'print(b)']],
    ];
    let y = 8;
    rows.forEach((r) => {
      const h = 18 + r[3].length * 16;
      s += K.rect(8, y, 92, h, { c: r[2], r: 8 });
      s += K.text(54, y + h / 2 - 3, r[0], { size: 13, w: 'b' });
      s += K.text(54, y + h / 2 + 13, r[1], { size: 11, cls: 't-mut' });
      s += K.rect(108, y, 324, h, { r: 8, s: 's-mut' });
      s += K.text(120, y + 22, r[3].join('\n'), { size: 13, anchor: 'start', lh: 16 });
      y += h + 10;
    });
    return K.svg(W, y, s, { title: 'The same idea written as an algorithm, as pseudocode and as a Python program' });
  });

  /* ---------- 3. Flowchart symbols ---------- */
  D.register('xi2.flow-symbols', () => {
    let s = '';
    const rows = [
      ['Terminator', 'Start or End of the algorithm'],
      ['Process', 'a calculation or an action'],
      ['Decision', 'a Yes / No question'],
      ['Input / Output', 'read data or display data'],
      ['Flow line', 'shows the order of the steps'],
    ];
    rows.forEach((r, i) => {
      const y = 8 + i * 54;
      if (i === 0) s += K.box(10, y + 4, 112, 36, 'Start / End', { c: 5, r: 18, size: 13 });
      if (i === 1) s += K.box(10, y + 4, 112, 36, 'x = x + 1', { c: 1, r: 3, size: 13 });
      if (i === 2) {
        s += K.poly([[66, y], [122, y + 22], [66, y + 44], [10, y + 22]], { c: 4 });
        s += K.text(66, y + 22, 'a > b ?', { size: 12, vmid: true });
      }
      if (i === 3) {
        s += K.poly([[28, y + 4], [122, y + 4], [104, y + 40], [10, y + 40]], { c: 2 });
        s += K.text(66, y + 22, 'INPUT a', { size: 12, vmid: true });
      }
      if (i === 4) s += K.line(10, y + 22, 122, y + 22, { arrow: true, w: 2 });
      s += K.text(146, y + 19, r[0], { size: 14, anchor: 'start', w: 'b' });
      s += K.text(146, y + 38, r[1], { size: 12, anchor: 'start', cls: 't-mut' });
    });
    return K.svg(W, 8 + 5 * 54, s, { title: 'Flowchart symbols: terminator, process, decision, input or output, and flow line' });
  });

  /* ---------- 4. Sample flowchart: even / odd ---------- */
  D.register('xi2.flow-evenodd', () => {
    let s = '';
    const cx = 220;
    s += K.line(cx, 40, cx, 56, { arrow: true });
    s += K.line(cx, 90, cx, 108, { arrow: true });
    s += K.polyline([[320, 143], [365, 143], [365, 208]], { arrow: true });
    s += K.polyline([[120, 143], [75, 143], [75, 208]], { arrow: true });
    s += K.polyline([[365, 242], [365, 264], [cx, 264]]);
    s += K.polyline([[75, 242], [75, 264], [cx, 264]]);
    s += K.line(cx, 264, cx, 282, { arrow: true });
    s += K.box(cx - 52, 8, 104, 32, 'Start', { c: 5, r: 16, size: 13 });
    s += K.poly([[cx - 61, 56], [cx + 75, 56], [cx + 61, 90], [cx - 75, 90]], { c: 2 });
    s += K.text(cx, 73, 'INPUT number', { size: 12, vmid: true });
    s += K.poly([[cx, 108], [cx + 100, 143], [cx, 178], [cx - 100, 143]], { c: 4 });
    s += K.text(cx, 143, 'number MOD 2 = 0 ?', { size: 12, vmid: true });
    s += K.text(342, 135, 'Yes', { size: 13, w: 'b', cls: 't-grn' });
    s += K.text(98, 135, 'No', { size: 13, w: 'b', cls: 't-red' });
    s += K.poly([[75 + 14 - 60, 208], [75 + 60, 208], [75 + 46, 242], [75 - 74, 242]], { c: 2 });
    s += K.text(75, 225, 'DISPLAY "Odd"', { size: 12, vmid: true });
    s += K.poly([[365 + 14 - 60, 208], [365 + 60, 208], [365 + 46, 242], [365 - 74, 242]], { c: 2 });
    s += K.text(365, 225, 'DISPLAY "Even"', { size: 12, vmid: true });
    s += K.box(cx - 52, 282, 104, 32, 'End', { c: 5, r: 16, size: 13 });
    return K.svg(W, 324, s, { title: 'Flowchart that checks whether a number is even or odd using MOD 2' });
  });

  /* ---------- 5. Decomposition trees ---------- */
  D.register('xi2.decomp-lang', () => {
    let s = '';
    const kids = [
      ['Vocabulary', 'words: I, eat, apple', 0],
      ['Grammar Rules', 'Subject - Verb - Object', 1],
      ['Tenses', 'present, past, future', 2],
      ['Sentence Building', 'combine words by rules', 3],
      ['Listen & Imitate', 'copy native speakers', 4],
      ['Get Feedback', 'teacher or app checks', 5],
    ];
    const y0 = 8;
    const sp = 46;
    s += K.line(118, y0 + 19 + 2.5 * sp, 150, y0 + 19 + 2.5 * sp);
    s += K.line(150, y0 + 19, 150, y0 + 19 + 5 * sp);
    kids.forEach((k, i) => {
      const y = y0 + i * sp;
      s += K.line(150, y + 19, 186, y + 19, { arrow: true });
      s += K.rect(188, y, 244, 38, { c: k[2], r: 8 });
      s += K.text(200, y + 16, k[0], { size: 13, w: 'b', anchor: 'start' });
      s += K.text(200, y + 31, k[1], { size: 11, anchor: 'start', cls: 't-mut' });
    });
    s += K.box(8, y0 + 2.5 * sp - 5, 110, 62, 'Learn a\nNew Language', { c: 4, size: 13, bold: true });
    return K.svg(W, y0 + 5 * sp + 46, s, { title: 'Decomposition tree: learning a new language split into six subtasks' });
  });

  D.register('xi2.decomp-daraz', () => {
    let s = '';
    const xs = [9, 116, 223, 330];
    const l1 = ['1. Browse', '2. Cart', '3. Payment', '4. Delivery'];
    const leaves = [
      ['Search product', 'Filter by price'],
      ['Add item', 'Change quantity'],
      ['Choose method', 'Confirm and pay'],
      ['Pack parcel', 'Rider delivers'],
    ];
    const cols = [0, 1, 4, 5];
    s += K.line(220, 48, 220, 66);
    s += K.line(59, 66, 380, 66);
    xs.forEach((x, i) => {
      const cx = x + 50;
      s += K.line(cx, 66, cx, 84, { arrow: true });
      s += K.line(cx, 122, cx, 210);
    });
    s += K.box(130, 8, 180, 40, 'Order on Daraz\n(big problem)', { c: 3, size: 13, bold: true });
    xs.forEach((x, i) => {
      s += K.box(x, 84, 100, 38, l1[i], { c: cols[i], size: 13, bold: true });
      leaves[i].forEach((t, j) => {
        s += K.box(x, 140 + j * 50, 100, 36, t, { c: cols[i], size: 12 });
      });
    });
    return K.svg(W, 234, s, { title: 'Decomposition tree: an online order split into browse, cart, payment and delivery, each with two small tasks' });
  });

  /* ---------- 6. Pattern recognition: star triangle ---------- */
  D.register('xi2.pattern-stars', () => {
    let s = '';
    s += K.text(34, 18, 'Row', { size: 12, cls: 't-mut' });
    s += K.text(142, 18, 'Stars drawn', { size: 12, cls: 't-mut' });
    s += K.text(282, 18, 'Count', { size: 12, cls: 't-mut' });
    for (let r = 1; r <= 5; r++) {
      const y = 36 + (r - 1) * 34;
      s += K.text(34, y + 6, String(r), { size: 14, w: 'b' });
      for (let j = 0; j < r; j++) s += K.circle(86 + j * 22, y, 8, { c: 4, s: 's-acc' });
      s += K.box(268, y - 13, 30, 26, String(r), { c: 1, size: 14, bold: true, r: 5 });
      if (r < 5) s += K.text(318, y + 22, '+1', { size: 12, w: 'b', cls: 't-red' });
    }
    s += K.rect(338, 40, 96, 100, { c: 5, r: 8 });
    s += K.text(386, 64, 'Pattern', { size: 13, w: 'b' });
    s += K.text(386, 84, 'each row adds', { size: 11 });
    s += K.text(386, 99, 'one star to', { size: 11 });
    s += K.text(386, 114, 'the row above', { size: 11 });
    s += K.text(W / 2, 226, 'Total stars = 1 + 2 + 3 + 4 + 5 = 15', { size: 14, w: 'b', cls: 't-acc' });
    return K.svg(W, 240, s, { title: 'Star triangle: row k has k stars, each row adds one star' });
  });

  /* ---------- 7. Abstraction: making tea ---------- */
  D.register('xi2.abstraction-tea', () => {
    let s = '';
    const cw = 136;
    const xs = [8, 152, 296];
    const heads = [['Necessary', 'the key logic', 5], ['Changes', 'inputs / parameters', 4], ['Ignore', 'noise, not needed', 6]];
    heads.forEach((h, i) => {
      s += K.rect(xs[i], 8, cw, 44, { c: h[2], r: 8 });
      s += K.text(xs[i] + cw / 2, 27, h[0], { size: 14, w: 'b' });
      s += K.text(xs[i] + cw / 2, 43, h[1], { size: 11, cls: 't-mut' });
    });
    const steps = ['1. Boil water', '2. Add tea leaves', '3. Steep a few min', '4. Pour into cup', '5. Serve'];
    steps.forEach((t, i) => {
      const y = 62 + i * 50;
      s += K.box(xs[0], y, cw, 36, t, { c: 5, size: 12 });
      if (i < 4) s += K.line(xs[0] + cw / 2, y + 36, xs[0] + cw / 2, y + 50, { arrow: true });
    });
    const ch = [['Ingredients', 'black, green, herbal'], ['Additions', 'sugar, honey, lemon'], ['Tools', 'kettle, stove, tea pot'], ['Time', 'boiling, steeping']];
    const ig = [['Kettle brand', 'not important'], ['Cup colour', 'or design'], ['Place', 'kitchen, office'], ['Mug type', 'glass, ceramic']];
    [ch, ig].forEach((list, k) => {
      list.forEach((t, i) => {
        const y = 62 + i * 62;
        s += K.rect(xs[k + 1], y, cw, 52, { c: k === 0 ? 4 : null, r: 8, dash: k === 1 ? '4 3' : null, s: k === 1 ? 's-mut' : null });
        s += K.text(xs[k + 1] + cw / 2, y + 22, t[0], { size: 13, w: 'b', cls: k === 1 ? 't-mut' : '' });
        s += K.text(xs[k + 1] + cw / 2, y + 40, t[1], { size: 11, cls: 't-mut' });
      });
    });
    return K.svg(W, 62 + 4 * 50 + 36 + 8, s, { title: 'Abstraction of making tea: necessary steps, details that change, and details to ignore' });
  });

  /* ---------- 8. Sorting order ---------- */
  D.register('xi2.sort-order', () => {
    let s = '';
    const rows = [
      ['Ascending: lowest to highest', [1, 3, 4, 8, 9], 44, 5],
      ['Descending: highest to lowest', [9, 8, 4, 3, 1], 44, 4],
      ['Alphabetical: A to Z', ['Ali', 'Bilal', 'Hina', 'Zain'], 84, 0],
    ];
    rows.forEach((r, i) => {
      const y = 8 + i * 74;
      s += K.text(10, y + 14, r[0], { size: 13, w: 'b', anchor: 'start' });
      const bw = r[2];
      const total = r[1].length * (bw + 6) - 6;
      const x0 = (W - total) / 2;
      r[1].forEach((v, j) => {
        s += K.box(x0 + j * (bw + 6), y + 24, bw, 34, v, { c: r[3], size: 14, bold: true, r: 6 });
      });
    });
    return K.svg(W, 8 + 3 * 74, s, { title: 'Sorted lists: ascending, descending and alphabetical' });
  });

  /* ---------- 9. Swap with temp ---------- */
  D.register('xi2.swap-temp', () => {
    let s = '';
    const steps = [
      ['Step 1', 'temp = A', { A: 8, B: 4, T: 8 }, 'T', 0],
      ['Step 2', 'A = B', { A: 4, B: 4, T: 8 }, 'A', 1],
      ['Step 3', 'B = temp', { A: 4, B: 8, T: 8 }, 'B', 2],
    ];
    steps.forEach((st, i) => {
      const x0 = 8 + i * 144;
      s += K.text(x0 + 68, 18, st[0] + ':  ' + st[1], { size: 13, w: 'b' });
      const v = st[2];
      s += K.box(x0 + 4, 40, 52, 32, 'A = ' + v.A, { c: st[3] === 'A' ? 3 : 6, size: 13, bold: true, r: 5 });
      s += K.box(x0 + 80, 40, 52, 32, 'B = ' + v.B, { c: st[3] === 'B' ? 3 : 6, size: 13, bold: true, r: 5 });
      s += K.box(x0 + 38, 108, 62, 32, 'temp = ' + v.T, { c: st[3] === 'T' ? 3 : 6, size: 12, bold: true, r: 5 });
      if (i === 0) s += K.line(x0 + 30, 72, x0 + 52, 108, { arrow: true, s: 's-red' });
      if (i === 1) s += K.line(x0 + 80, 56, x0 + 57, 56, { arrow: true, s: 's-red' });
      if (i === 2) s += K.line(x0 + 86, 108, x0 + 106, 72, { arrow: true, s: 's-red' });
    });
    s += K.text(W / 2, 166, 'Without temp, one value would be overwritten and lost.', { size: 12, cls: 't-mut' });
    return K.svg(W, 178, s, { title: 'Swapping two values A and B with a temporary variable in three steps' });
  });

  /* ---------- 10. Bubble sort traces ---------- */
  D.register('xi2.bubble-pass', (args) => {
    const p = Math.max(1, Math.min(4, (args && args.pass) || 1));
    const pass = bubbleSim(DATA)[p - 1];
    return trace('Bubble Sort: Pass ' + p, pass.rows, [['cmp', 'compared'], ['swp', 'swapped'], ['ok', 'final place']]);
  });

  D.register('xi2.bubble-all', () => {
    const passes = bubbleSim(DATA);
    const rows = [{ lab: 'Unsorted', arr: DATA, st: DATA.map(() => 'n') }];
    passes.forEach((ps, i) => rows.push({ lab: 'After pass ' + (i + 1), arr: ps.arr, st: ps.st, right: ps.swaps + (ps.swaps === 1 ? ' swap' : ' swaps') }));
    const total = passes.reduce((a, b) => a + b.swaps, 0);
    return trace('Bubble Sort: all passes', rows, [['ok', 'final place (biggest bubbles up)']], 'Total: ' + total + ' swaps, 10 comparisons');
  });

  /* ---------- 11. Selection sort traces ---------- */
  D.register('xi2.selection-pass', (args) => {
    const p = Math.max(1, Math.min(4, (args && args.pass) || 1));
    const pass = selectionSim(DATA)[p - 1];
    return trace('Selection Sort: Pass ' + p, pass.rows, [['key', 'position K'], ['cmp', 'compared'], ['swp', 'swapped'], ['ok', 'final place']]);
  });

  D.register('xi2.selection-all', () => {
    const passes = selectionSim(DATA);
    const rows = [{ lab: 'Unsorted', arr: DATA, st: DATA.map(() => 'n') }];
    passes.forEach((ps, i) => rows.push({ lab: 'After pass ' + (i + 1), arr: ps.arr, st: ps.st, right: ps.swaps + (ps.swaps === 1 ? ' swap' : ' swaps') }));
    const total = passes.reduce((a, b) => a + b.swaps, 0);
    return trace('Selection Sort: all passes', rows, [['ok', 'final place (smallest first)']], 'Total: ' + total + ' swaps, 10 comparisons');
  });

  D.register('xi2.selection-classic', () => {
    const rows = [
      { lab: 'Start', arr: DATA, st: DATA.map(() => 'n') },
      { lab: 'Scan for smallest', arr: DATA, st: ['key', 'n', 'swp', 'n', 'n'], right: 'min = 1', rc: 't-red' },
      { lab: 'Swap once', arr: [1, 4, 8, 9, 3], st: ['ok', 'n', 'swp', 'n', 'n'], right: '1 swap', rc: 't-red' },
    ];
    return trace('Pass 1 (classic form): find the smallest, swap once', rows, [['key', 'first position'], ['swp', 'smallest / swapped'], ['ok', 'final place']]);
  });

  /* ---------- 12. Linear search trace ---------- */
  D.register('xi2.linear-trace', () => {
    const data = [8, 3, 6, 1, 7, 2, 4, 5];
    const target = 7;
    const bw = 42;
    const x0 = 38;
    let s = '';
    data.forEach((_, j) => {
      s += K.text(x0 + j * (bw + 4) + bw / 2, 14, String(j + 1), { size: 11, cls: 't-mut' });
    });
    for (let k = 0; k < 5; k++) {
      const yl = 38 + k * 62;
      const found = data[k] === target;
      s += K.text(10, yl, 'Check ' + (k + 1) + ':  ' + data[k] + ' = ' + target + ' ?   ' + (found ? 'Yes, FOUND at position ' + (k + 1) : 'No, move on'), { size: 13, anchor: 'start', w: 'b', cls: found ? 't-grn' : 't-mut' });
      data.forEach((v, j) => {
        let code = 'out';
        if (j < k) code = 'n';
        if (j === k) code = found ? 'ok' : 'cmp';
        s += cell(x0 + j * (bw + 4), yl + 8, bw, 34, v, code);
      });
    }
    s += legend(38 + 4 * 62 + 66, [['n', 'checked'], ['cmp', 'checking now'], ['ok', 'found'], ['out', 'not yet']]);
    return K.svg(W, 38 + 4 * 62 + 78, s, { title: 'Linear search for 7 in the list 8, 3, 6, 1, 7, 2, 4, 5: five checks' });
  });

  /* ---------- 13. Binary search trace ---------- */
  D.register('xi2.binary-trace', (args) => {
    const n = (args && args.n) || 8;
    const item = (args && args.item) || 3;
    const data = [];
    for (let i = 1; i <= n; i++) data.push(i);
    const bw = 40;
    const x0 = (W - (n * (bw + 4) - 4)) / 2;
    let beg = 0;
    let end = n - 1;
    let step = 1;
    let s = '';
    let y = 6;
    while (beg <= end) {
      const mid = Math.floor((beg + end) / 2);
      const hit = data[mid] === item;
      s += K.text(10, y + 14, 'Step ' + step + ':  BEG=' + (beg + 1) + '  END=' + (end + 1) + '  MID=INT((' + (beg + 1) + '+' + (end + 1) + ')/2)=' + (mid + 1), { size: 12, anchor: 'start', w: 'b' });
      let act;
      if (hit) act = 'DATA[MID] = ' + data[mid] + '  equals ' + item + '  -> FOUND';
      else if (item < data[mid]) act = 'DATA[MID] = ' + data[mid] + '.  Is ' + item + ' < ' + data[mid] + ' ?  Yes -> END = MID - 1';
      else act = 'DATA[MID] = ' + data[mid] + '.  Is ' + item + ' < ' + data[mid] + ' ?  No -> BEG = MID + 1';
      s += K.text(10, y + 31, act, { size: 12, anchor: 'start', cls: hit ? 't-grn' : 't-mut' });
      data.forEach((v, j) => {
        let code = 'out';
        if (j >= beg && j <= end) code = 'in';
        if (j === mid) code = hit ? 'ok' : 'cmp';
        s += cell(x0 + j * (bw + 4), y + 38, bw, 32, v, code);
        const tags = [];
        if (j === beg) tags.push('BEG');
        if (j === mid) tags.push('MID');
        if (j === end) tags.push('END');
        if (tags.length) s += K.text(x0 + j * (bw + 4) + bw / 2, y + 86, tags.join('/'), { size: 11, w: 'b', cls: j === mid ? 't-acc' : 't-mut' });
      });
      y += 100;
      if (hit) break;
      if (item < data[mid]) end = mid - 1;
      else beg = mid + 1;
      step++;
    }
    s += legend(y + 4, [['in', 'search range'], ['cmp', 'middle (MID)'], ['ok', 'found'], ['out', 'discarded']]);
    return K.svg(W, y + 14, s, { title: 'Binary search for ' + item + ' in a sorted list of ' + n + ' numbers' });
  });

  D.register('xi2.binary-halving', () => {
    let s = '';
    const sizes = [16, 8, 4, 2, 1];
    const labels = ['Start', 'After 1 step', 'After 2 steps', 'After 3 steps', 'After 4 steps'];
    sizes.forEach((v, i) => {
      const y = 10 + i * 38;
      const w = (v / 16) * 290;
      s += K.text(10, y + 20, labels[i], { size: 12, anchor: 'start', cls: 't-mut' });
      s += K.rect(124, y + 4, w, 26, { c: i === 4 ? 5 : 1, r: 4 });
      if (w > 90) s += K.text(124 + w / 2, y + 18, v + ' items', { size: 12, w: 'b', vmid: true });
      else s += K.text(124 + w + 8, y + 18, v + (v === 1 ? ' item: found!' : ' items'), { size: 12, w: 'b', anchor: 'start', vmid: true });
    });
    s += K.text(W / 2, 214, '16 items need at most 4 halvings (16 = 2 x 2 x 2 x 2)', { size: 12, cls: 't-mut' });
    s += K.text(W / 2, 234, '1,000,000 items need only about 20 halvings', { size: 13, w: 'b', cls: 't-acc' });
    return K.svg(W, 246, s, { title: 'Binary search halves the list at every step: sixteen items need four steps' });
  });

  /* ---------- 14. Growth curves ---------- */
  D.register('xi2.growth', () => {
    let s = '';
    const ox = 56;
    const oy = 206;
    const ux = 46;
    const uy = 2.7;
    s += K.line(ox, oy, ox + 8 * ux + 14, oy, { arrow: true, cls: 's-mut' });
    s += K.line(ox, oy, ox, 14, { arrow: true, cls: 's-mut' });
    [0, 16, 32, 48, 64].forEach((v) => {
      s += K.line(ox - 4, oy - v * uy, ox, oy - v * uy, { cls: 's-mut' });
      s += K.text(ox - 8, oy - v * uy + 4, String(v), { size: 11, anchor: 'end', cls: 't-mut' });
    });
    [2, 4, 6, 8].forEach((v) => {
      s += K.line(ox + v * ux, oy, ox + v * ux, oy + 4, { cls: 's-mut' });
      s += K.text(ox + v * ux, oy + 17, String(v), { size: 11, cls: 't-mut' });
    });
    const curve = (f, from) => {
      let d = '';
      for (let x = from; x <= 8.001; x += 0.1) d += (d ? 'L' : 'M') + (ox + x * ux).toFixed(1) + ' ' + (oy - f(x) * uy).toFixed(1) + ' ';
      return d;
    };
    s += K.path(curve((x) => x * x, 0), { s: 's-red', w: 3 });
    s += K.path(curve((x) => x, 0), { s: 's-acc', w: 3 });
    s += K.path(curve((x) => Math.log2(x), 1), { s: 's-grn', w: 3 });
    [['n x n  (nested loops)', 's-red', 't-red'], ['n  (linear search)', 's-acc', 't-acc'], ['log2 n  (binary search)', 's-grn', 't-grn']].forEach((k, i) => {
      s += K.line(ox + 16, 34 + i * 22, ox + 46, 34 + i * 22, { cls: k[1], w: 3 });
      s += K.text(ox + 54, 38 + i * 22, k[0], { size: 12, w: 'b', anchor: 'start', cls: k[2] });
    });
    s += K.text(ox + 4 * ux, oy + 36, 'input size n', { size: 12, cls: 't-mut' });
    s += K.text(14, 112, 'steps', { size: 12, cls: 't-mut', rot: -90 });
    return K.svg(W, 250, s, { title: 'Growth of work with input size: n squared grows fastest, n linearly, log2 n very slowly' });
  });

  /* ---------- 15. Decision guide ---------- */
  D.register('xi2.decision-guide', () => {
    let s = '';
    s += K.line(220, 42, 220, 66);
    s += K.line(105, 66, 385, 66);
    [105, 270, 385].forEach((x) => (s += K.line(x, 66, x, 88, { arrow: true })));
    s += K.box(135, 8, 170, 34, 'What is the problem?', { c: 1, size: 13, bold: true });
    s += K.box(30, 88, 150, 40, 'Find an item\n(Searching)', { c: 0, size: 13, bold: true });
    s += K.box(215, 88, 110, 40, 'Put in order\n(Sorting)', { c: 2, size: 13, bold: true });
    s += K.box(335, 88, 100, 40, 'Repeating\nproblem', { c: 4, size: 13, bold: true });
    s += K.line(270, 128, 270, 152, { arrow: true });
    s += K.line(385, 128, 385, 152, { arrow: true });
    s += K.box(215, 152, 110, 40, 'Sorting\nalgorithm', { c: 2, size: 13 });
    s += K.box(335, 152, 100, 40, 'Dynamic\nProgramming', { c: 4, size: 12 });
    s += K.line(105, 128, 105, 152, { arrow: true });
    s += K.poly([[105, 152], [177, 186], [105, 220], [33, 186]], { c: 0 });
    s += K.text(105, 186, 'Is data sorted?', { size: 12, vmid: true });
    s += K.polyline([[33, 186], [18, 186], [18, 252]], { arrow: true });
    s += K.polyline([[105, 220], [105, 236], [175, 236], [175, 252]], { arrow: true });
    s += K.text(24, 236, 'No', { size: 12, w: 'b', cls: 't-red', anchor: 'start' });
    s += K.text(112, 232, 'Yes', { size: 12, w: 'b', cls: 't-grn', anchor: 'start' });
    s += K.box(4, 252, 108, 36, 'Linear Search', { c: 7, size: 13, bold: true });
    s += K.box(120, 252, 110, 36, 'Binary Search', { c: 5, size: 13, bold: true });
    s += K.text(215, 208, 'Small list: Bubble or', { size: 11, cls: 't-mut', anchor: 'start' });
    s += K.text(215, 222, 'Selection Sort is fine', { size: 11, cls: 't-mut', anchor: 'start' });
    return K.svg(W, 298, s, { title: 'Simple decision guide: choose linear search, binary search, a sorting algorithm or dynamic programming' });
  });

  /* ---------- 16. Evaluation criteria ---------- */
  D.register('xi2.criteria', () => {
    let s = '';
    const cols = [
      ['Correctness', 'Is it right?', 5, ['Matches requirements', 'Handles odd inputs', 'Always finishes']],
      ['Efficiency', 'Is it fast and lean?', 4, ['Time (speed)', 'Space (memory)', 'Scales to big input']],
      ['Clarity', 'Is it easy to read?', 1, ['Clear steps', 'Meaningful names', 'Indent + comments']],
    ];
    cols.forEach((c, i) => {
      const x = 8 + i * 144;
      s += K.rect(x, 8, 136, 48, { c: c[2], r: 8 });
      s += K.text(x + 68, 28, c[0], { size: 14, w: 'b' });
      s += K.text(x + 68, 46, c[1], { size: 11, cls: 't-mut' });
      c[3].forEach((t, j) => {
        s += K.box(x, 66 + j * 44, 136, 36, t, { size: 12, r: 6, s: 's-mut' });
      });
    });
    return K.svg(W, 66 + 3 * 44 + 4, s, { title: 'Three criteria to evaluate an algorithm: correctness, efficiency and clarity' });
  });
})();
