/* XII Ch2 (Computational Thinking and Algorithms) diagrams */
(function () {
  const D = Diagrams;

  /* ---------- local helpers ---------- */

  /** table made of one K.grid per column so column widths can differ; rows[0] is the header */
  function tbl(x, y, cws, rh, rows, fills, size) {
    let s = '';
    let cx = x;
    cws.forEach((cw, j) => {
      s += K.grid(cx, y, cw, rh, rows.map((r) => [r[j]]), {
        head: true,
        size: size || 13,
        fills: fills ? fills.map((r) => [r ? r[j] : null]) : null,
      });
      cx += cw;
    });
    return s;
  }

  /** horizontal row of equal boxes */
  function cellRow(x, y, w, h, vals, o) {
    o = o || {};
    let s = '';
    vals.forEach((v, i) => {
      const c = o.fills ? o.fills[i] : o.c;
      s += K.box(x + i * w, y, w, h, v == null ? '' : String(v), { c: c, r: o.r == null ? 0 : o.r, size: o.size || 15, bold: o.bold, s: o.s });
    });
    return s;
  }

  /** linked-list node: data cell + pointer cell. Returns svg and anchor points. */
  function node(x, y, data, o) {
    o = o || {};
    const dw = o.dw || 50;
    const pw = o.pw || 30;
    const h = o.h || 40;
    const c = o.c == null ? 0 : o.c;
    let s = K.rect(x, y, dw, h, { c: c, r: 0, s: o.s }) + K.rect(x + dw, y, pw, h, { c: o.pc == null ? 6 : o.pc, r: 0, s: o.s });
    s += K.text(x + dw / 2, y + h / 2, String(data), { size: o.size || 16, vmid: true, w: 'b' });
    s += K.dot(x + dw + pw / 2, y + h / 2, 3.5);
    return { svg: s, p: [x + dw + pw / 2, y + h / 2], left: [x, y + h / 2], top: [x + dw / 2, y], w: dw + pw, h: h };
  }

  /** circle node on a tree/graph, edges shortened so lines stop at the circle */
  function edge(a, b, r, o) {
    const dx = b[0] - a[0];
    const dy = b[1] - a[1];
    const d = Math.sqrt(dx * dx + dy * dy) || 1;
    return K.line(a[0] + (dx / d) * r, a[1] + (dy / d) * r, b[0] - (dx / d) * r, b[1] - (dy / d) * r, o);
  }

  const circ = (p, r, label, c, o) => {
    o = o || {};
    return K.circle(p[0], p[1], r, { c: c, s: o.s }) + K.text(p[0], p[1], String(label), { size: o.size || 15, vmid: true, w: 'b' });
  };

  const badge = (x, y, n) => K.circle(x, y, 10, { c: 4, s: 's-acc' }) + K.text(x, y, String(n), { size: 12, vmid: true, w: 'b' });

  /* ---------- 2.1 correctness ---------- */

  D.register('xii2.trace-soldiers', () => {
    const rows = [
      ['Step', 'Total', 'height', 'Condition / note'],
      [2, 0, '', 'SET Total = 0'],
      [3, '', '', 'load 5 heights'],
      [4, '', '1.91', ''],
      [5, '', '', 'True'],
      [6, 1, '', 'Total + 1'],
      [4, '', '2.01', ''],
      [5, '', '', 'False'],
      [4, '', '1.87', ''],
      [5, '', '', 'True'],
      [6, 2, '', 'Total + 1'],
      [4, '', '1.57', ''],
      [5, '', '', 'True'],
      [6, 3, '', 'Total + 1'],
      [4, '', '1.48', ''],
      [5, '', '', 'False'],
      [9, 3, '', 'Print Total'],
    ];
    const f = rows.map(() => [null, null, null, null]);
    rows.forEach((r, i) => {
      if (i === 0) return;
      if (r[0] === 4) f[i][2] = 1;
      if (r[0] === 5) f[i][3] = r[3] === 'True' ? 5 : 3;
      if (r[0] === 6 || r[0] === 2) f[i][1] = 4;
      if (r[0] === 9) {
        f[i][1] = 5;
        f[i][3] = 5;
      }
    });
    let s = K.text(215, 18, 'AllHeights = [1.91, 2.01, 1.87, 1.57, 1.48]', { size: 13, w: 'b' });
    s += tbl(20, 30, [60, 70, 80, 170], 21, rows, f, 13);
    return K.svg(400, 400, s, { title: 'Trace table for counting soldiers with height between 1.57 and 1.91; Total ends at 3' });
  });

  D.register('xii2.trace-sum', () => {
    const rows = [
      ['Step', 'i', 'Sum', 'Working'],
      [3, '', 0, 'Sum = 0'],
      [5, 1, 1, '0 + 1'],
      [5, 2, 3, '1 + 2'],
      [5, 3, 6, '3 + 3'],
      [5, 4, 10, '6 + 4'],
      [5, 5, 15, '10 + 5'],
      [7, '', 15, 'Print Sum'],
    ];
    const f = rows.map((r, i) => (i === 0 ? null : [null, r[1] === '' ? null : 1, 4, i === rows.length - 1 ? 5 : null]));
    let s = K.text(180, 18, 'Input N = 5   (Sum of 1 to N)', { size: 14, w: 'b' });
    s += tbl(20, 30, [60, 60, 80, 140], 26, rows, f, 14);
    return K.svg(380, 250, s, { title: 'Trace table for the sum of numbers 1 to 5, Sum becomes 15' });
  });

  D.register('xii2.sum-checks', () => {
    let s = '';
    const xs = [10, 160, 310];
    const heads = ['1. Start state', '2. Each iteration', '3. End state'];
    const bodies = ['Sum = 0', 'Sum = Sum + i\n(i = 1 to N)', 'Sum holds\nthe total'];
    const qs = ['Is it valid?', 'Still correct?', 'Is answer ready?'];
    xs.forEach((x, i) => {
      s += K.text(x + 60, 18, heads[i], { size: 13, w: 'b' });
      s += K.box(x, 30, 120, 60, bodies[i], { c: [0, 1, 5][i], size: 13 });
      s += K.text(x + 60, 112, qs[i], { size: 12, cls: 't-mut' });
      if (i < 2) s += K.line(x + 122, 60, x + 148, 60, { arrow: true });
    });
    s += K.box(10, 135, 205, 40, 'Normal case: N = 5\nSum = 15', { c: 5, size: 13 });
    s += K.box(225, 135, 205, 40, 'Edge case: N = 0\nSum = 0', { c: 4, size: 13 });
    return K.svg(440, 190, s, { title: 'Stepwise reasoning checks start state, loop and end state, with normal and edge case' });
  });

  /* ---------- generic map (mind-map style) ---------- */
  function map(root, groups) {
    const W = 440;
    const gap = 10;
    const cw = (W - 20 - (groups.length - 1) * gap) / groups.length;
    let s = K.box(W / 2 - 110, 8, 220, 34, root, { c: 2, size: 15, bold: true });
    let maxY = 0;
    groups.forEach((g, i) => {
      const x = 10 + i * (cw + gap);
      s += K.polyline([[W / 2, 42], [W / 2, 56], [x + cw / 2, 56], [x + cw / 2, 68]], {});
      s += K.box(x, 68, cw, 34, g.t, { c: g.c == null ? 1 : g.c, size: 14, bold: true });
      g.items.forEach((it, j) => {
        const y = 112 + j * 34;
        s += K.box(x + 8, y, cw - 8, 28, it, { c: 6, size: 12 });
        maxY = Math.max(maxY, y + 28);
      });
      s += K.line(x + 3, 102, x + 3, 112 + (g.items.length - 1) * 34 + 14, { cls: 's-mut' });
    });
    return K.svg(W, maxY + 10, s, { title: root });
  }

  D.register('xii2.correctness-map', () =>
    map('Correct algorithm', [
      { t: 'Trace tables', c: 0, items: ['Paper execution', 'Dry running', 'Debugging', 'Validation'] },
      { t: 'Stepwise reasoning', c: 1, items: ['Logic verification', 'Valid start state?', 'All cases handled?', 'Loop stays correct?'] },
    ])
  );

  D.register('xii2.clarity-map', () =>
    map('Clarity', [
      { t: 'Modularity', c: 0, items: ['Single Responsibility', 'Loose coupling', 'Abstraction'] },
      { t: 'Readability', c: 1, items: ['Naming conventions', 'Self-documentation', 'Control flow simplicity', 'Consistency'] },
    ])
  );

  D.register('xii2.efficiency-map', () =>
    map('Efficiency = time + space', [
      { t: 'Steps', c: 0, items: ['main operation', 'Big O notation'] },
      { t: 'Conditions', c: 1, items: ['nested IF', 'short-circuiting'] },
      { t: 'Repetitions', c: 4, items: ['loops', 'biggest factor'] },
    ])
  );

  D.register('xii2.refine-map', () =>
    map('Refinements', [
      { t: 'Improve Clarity', c: 0, items: ['Meaningful names', 'Break into modules', 'Structure and indentation', 'Short useful comments'] },
      { t: 'Improve Efficiency', c: 4, items: ['Reduce unnecessary steps', 'Use better algorithms', 'Avoid re-computing', 'Right data structure'] },
    ])
  );

  /* ---------- 2.2 clarity ---------- */

  D.register('xii2.modular', () => {
    let s = '';
    s += K.text(105, 18, 'Poor: one block', { size: 14, w: 'b', cls: 't-red' });
    s += K.rect(10, 28, 190, 212, { c: 3 });
    const lines = ['Start', 'Set A = [1,2,3,4,5]', 'Set n = 5', 'total = 0', 'For I = 1 to n', '   total = total + A[I]', 'End For', 'avg = total / n', 'Print avg', 'End'];
    lines.forEach((l, i) => {
      s += K.text(20, 48 + i * 20, l, { size: 12, anchor: 'start' });
    });
    s += K.text(335, 18, 'Good: modules', { size: 14, w: 'b', cls: 't-grn' });
    s += K.box(235, 28, 200, 42, 'Main\nPrint FindAverage(A, n)', { c: 1, size: 12 });
    s += K.box(235, 100, 200, 46, 'FindAverage(A, n)\nSum = CalculateSum(A, n)\nAvg = Sum / n', { c: 0, size: 12 });
    s += K.box(235, 178, 200, 46, 'CalculateSum(A, n)\nloop adds all A[I]\nReturn Total', { c: 5, size: 12 });
    s += K.line(335, 70, 335, 98, { arrow: true });
    s += K.line(335, 146, 335, 176, { arrow: true });
    s += K.text(342, 88, 'calls', { size: 12, anchor: 'start', cls: 't-mut' });
    s += K.text(342, 166, 'calls', { size: 12, anchor: 'start', cls: 't-mut' });
    return K.svg(445, 250, s, { title: 'One big block versus FindAverage calling CalculateSum' });
  });

  /* ---------- 2.3 efficiency ---------- */

  D.register('xii2.big-o', () => {
    const x0 = 50;
    const y0 = 220;
    const sx = 38;
    const sy = 3.6;
    let s = '';
    s += K.line(x0, y0, 432, y0, { arrow: true, cls: 's-mut' });
    s += K.line(x0, y0, x0, 22, { arrow: true, cls: 's-mut' });
    s += K.text(x0 + 4, 16, 'time / steps', { size: 12, anchor: 'start', cls: 't-mut' });
    s += K.text(430, 240, 'input size n', { size: 12, anchor: 'end', cls: 't-mut' });
    const curve = (fn, from, to, o) => {
      let d = '';
      for (let n = from; n <= to + 1e-9; n += 0.2) {
        const v = fn(n);
        d += (d ? 'L' : 'M') + (x0 + n * sx).toFixed(1) + ' ' + (y0 - v * sy).toFixed(1) + ' ';
      }
      return K.path(d, o);
    };
    s += curve(() => 6, 0, 10, { s: 's-grn', w: 3 });
    s += curve((n) => 3 * (1 + Math.log2(n)), 1, 10, { s: 's-brand', w: 3 });
    s += curve((n) => 3 * n, 0, 10, { s: 's-acc', w: 3 });
    s += curve((n) => 0.6 * n * n, 0, 9.1, { s: 's-red', w: 3 });
    s += K.text(428, 213, 'O(1)', { size: 13, anchor: 'end', w: 'b', cls: 't-grn' });
    s += K.text(428, 160, 'O(log n)', { size: 13, anchor: 'end', w: 'b', cls: 't-acc' });
    s += K.text(428, 100, 'O(n)', { size: 13, anchor: 'end', w: 'b', cls: 't-acc' });
    s += K.text(376, 38, 'O(n²)', { size: 13, anchor: 'end', w: 'b', cls: 't-red' });
    return K.svg(440, 250, s, { title: 'Growth of steps for O(1), O(log n), O(n) and O(n squared) as input size grows' });
  });

  D.register('xii2.nested-loops', () => {
    const items = ['a', 'b', 'c', 'd', 'e'];
    let s = '';
    s += K.text(85, 20, 'One loop', { size: 14, w: 'b' });
    s += cellRow(10, 40, 30, 30, items, { c: 0, size: 14 });
    items.forEach((_, i) => {
      s += K.line(25 + i * 30, 76, 25 + i * 30, 100, { arrow: true });
      s += K.text(25 + i * 30, 118, String(i + 1), { size: 12, cls: 't-mut' });
    });
    s += K.text(85, 150, '5 items = 5 checks', { size: 13 });
    s += K.text(85, 172, 'O(n)', { size: 15, w: 'b', cls: 't-acc' });
    s += K.text(320, 20, 'Loop inside loop', { size: 14, w: 'b' });
    const x = 225;
    const y = 54;
    const c = 30;
    items.forEach((it, i) => {
      s += K.text(x + c / 2 + i * c, y - 6, it, { size: 12, cls: 't-mut' });
      s += K.text(x - 10, y + c / 2 + i * c + 1, it, { size: 12, vmid: true, cls: 't-mut' });
    });
    for (let i = 0; i < 5; i++) {
      for (let j = 0; j < 5; j++) {
        s += K.rect(x + j * c, y + i * c, c, c, { c: i === j ? 6 : 3, r: 0, cls: 'cell' });
      }
    }
    s += K.text(x + 75, y + 5 * c + 20, '5 × 5 = 25 comparisons', { size: 13 });
    s += K.text(x + 75, y + 5 * c + 42, 'O(n²)', { size: 15, w: 'b', cls: 't-red' });
    return K.svg(440, 250, s, { title: 'One loop does n checks, nested loops do n times n comparisons' });
  });

  D.register('xii2.eval-framework', () => {
    const cards = [
      { h: 'Does it scale?', t: 'input 10 times\nbigger:\n10x time (linear)\nor 100x (quadratic)?', c: 0 },
      { h: 'What is the\nbottleneck?', t: 'deepest loop or\nmost repeated\noperation', c: 1 },
      { h: 'Is the cost\nworth it?', t: 'O(log n) may not\nbeat a simple\nO(n) for 50 items', c: 4 },
    ];
    let s = '';
    cards.forEach((cd, i) => {
      const x = 8 + i * 144;
      s += K.rect(x, 10, 136, 150, { c: cd.c });
      s += K.text(x + 68, 34, String(i + 1), { size: 18, w: 'b', cls: 't-acc' });
      s += K.text(x + 68, 56, cd.h, { size: 13, w: 'b', lh: 16 });
      s += K.text(x + 68, 100, cd.t, { size: 12, lh: 16 });
    });
    return K.svg(440, 170, s, { title: 'Three questions: does it scale, what is the bottleneck, is the cost worth it' });
  });

  /* ---------- 2.4 refinements: search and sort ---------- */

  D.register('xii2.linear-search', () => {
    const data = [8, 3, 6, 1, 7, 2, 4, 5];
    const cw = 44;
    const x0 = 28;
    let s = K.text(220, 18, 'Linear Search: FindValue = 7', { size: 14, w: 'b' });
    s += cellRow(x0, 50, cw, 40, data, { fills: data.map((v, i) => (i < 4 ? 3 : i === 4 ? 5 : 6)), size: 16 });
    data.forEach((_, i) => {
      s += K.text(x0 + i * cw + cw / 2, 42, 'PTR ' + (i + 1), { size: 11, cls: 't-mut' });
      let m = '';
      let cl = 't-mut';
      if (i < 4) {
        m = 'not 7';
        cl = 't-red';
      } else if (i === 4) {
        m = 'found';
        cl = 't-grn';
      } else m = 'skip';
      s += K.text(x0 + i * cw + cw / 2, 108, m, { size: 11, cls: cl, w: i === 4 ? 'b' : '' });
    });
    s += K.line(x0 + 2, 128, x0 + 5 * cw - 2, 128, { arrow: 'both', cls: 's-acc' });
    s += K.text(x0 + 2.5 * cw, 148, '5 comparisons', { size: 13, w: 'b' });
    return K.svg(400, 160, s, { title: 'Linear search checks each cell from the first until 7 is found at the fifth' });
  });

  D.register('xii2.binary-search', () => {
    const cw = 38;
    const x0 = 80;
    let s = K.text(250, 16, 'Binary Search: Item = 7  (DATA is sorted)', { size: 14, w: 'b' });
    const round = (y, name, beg, mid, end, note, found) => {
      let o = K.text(8, y + 24, name, { size: 13, w: 'b', anchor: 'start' });
      const fills = [];
      for (let i = 1; i <= 9; i++) fills.push(i < beg ? 6 : i === mid ? (found ? 5 : 4) : 1);
      o += cellRow(x0, y + 8, cw, 36, [1, 2, 3, 4, 5, 6, 7, 8, 9], { fills: fills, size: 15 });
      for (let i = 1; i <= 9; i++) o += K.text(x0 + (i - 1) * cw + cw / 2, y + 4, String(i), { size: 11, cls: 't-mut' });
      const tag = (i, t) => K.text(x0 + (i - 1) * cw + cw / 2, y + 62, t, { size: 12, w: 'b', cls: 't-acc' }) + K.line(x0 + (i - 1) * cw + cw / 2, y + 46, x0 + (i - 1) * cw + cw / 2, y + 51, { arrow: true });
      o += tag(beg, 'BEG') + tag(mid, 'MID') + tag(end, 'END');
      o += K.text(x0 + 4.5 * cw, y + 82, note, { size: 12 });
      return o;
    };
    s += round(30, 'Round 1', 1, 5, 9, 'MID = 5, and 7 > 5, so BEG = MID + 1 = 6', false);
    s += round(140, 'Round 2', 6, 7, 9, 'MID = INT(15 / 2) = 7, DATA[7] = 7: found', true);
    s += K.text(250, 244, '2 rounds instead of 7 comparisons', { size: 13, w: 'b' });
    return K.svg(440, 256, s, { title: 'Binary search for 7 in 1 to 9 finds it in two rounds' });
  });

  D.register('xii2.bubble-passes', () => {
    const passes = [
      { l: 'start', d: [8, 4, 1, 9, 3], k: 0, r: '' },
      { l: 'pass 1', d: [4, 1, 8, 3, 9], k: 1, r: 'PTR ≤ 4' },
      { l: 'pass 2', d: [1, 4, 3, 8, 9], k: 2, r: 'PTR ≤ 3' },
      { l: 'pass 3', d: [1, 3, 4, 8, 9], k: 3, r: 'PTR ≤ 2' },
      { l: 'pass 4', d: [1, 3, 4, 8, 9], k: 4, r: 'PTR ≤ 1' },
    ];
    const cw = 46;
    let s = K.text(8, 18, 'Bubble Sort', { size: 14, w: 'b', anchor: 'start' });
    s += K.text(330, 18, 'inner loop shrinks', { size: 12, cls: 't-mut', anchor: 'start' });
    passes.forEach((p, i) => {
      const y = 34 + i * 44;
      s += K.text(8, y + 19, p.l, { size: 13, anchor: 'start', w: 'b' });
      s += cellRow(78, y, cw, 36, p.d, { fills: p.d.map((_, j) => (j >= 5 - p.k ? 5 : 1)), size: 16 });
      if (p.r) s += K.text(330, y + 19, p.r, { size: 13, anchor: 'start', w: 'b', cls: 't-acc' });
    });
    s += K.rect(78, 258, 16, 14, { c: 5, r: 2 });
    s += K.text(100, 270, 'settled at the end: no need to check again', { size: 12, anchor: 'start', cls: 't-mut' });
    return K.svg(440, 282, s, { title: 'Bubble sort passes on 8 4 1 9 3: the largest value settles at the end and the inner loop shrinks' });
  });

  /* ---------- 2.5 data structure concept ---------- */

  D.register('xii2.ds-classes', () => {
    let s = K.box(140, 8, 160, 36, 'Data Structures', { c: 2, size: 15, bold: true });
    s += K.polyline([[220, 44], [220, 58], [110, 58], [110, 70]], {});
    s += K.polyline([[220, 58], [330, 58], [330, 70]], {});
    s += K.box(10, 70, 200, 34, 'Linear', { c: 0, size: 15, bold: true });
    s += K.text(110, 122, 'one after another', { size: 12, cls: 't-mut' });
    ['Array', 'Linked List', 'Stack', 'Queue'].forEach((t, i) => {
      s += K.box(10 + (i % 2) * 104, 134 + Math.floor(i / 2) * 40, 96, 32, t, { c: 6, size: 13 });
    });
    s += K.box(230, 70, 200, 34, 'Non-linear', { c: 3, size: 15, bold: true });
    s += K.text(330, 122, 'hierarchy / network', { size: 12, cls: 't-mut' });
    ['Tree', 'Graph'].forEach((t, i) => {
      s += K.box(230 + i * 104, 134, 96, 32, t, { c: 6, size: 13 });
    });
    return K.svg(440, 220, s, { title: 'Data structures are linear (array, linked list, stack, queue) or non-linear (tree, graph)' });
  });

  D.register('xii2.array', () => {
    const vals = [23, 76, 12, 90, 34, 68];
    const cw = 58;
    const x0 = 84;
    let s = '';
    s += K.text(8, 36, 'address', { size: 12, anchor: 'start', cls: 't-mut' });
    s += K.text(8, 72, 'value', { size: 12, anchor: 'start', w: 'b' });
    s += K.text(8, 114, 'index', { size: 12, anchor: 'start', cls: 't-mut' });
    s += K.text(8, 138, 'A[ i ]', { size: 12, anchor: 'start', cls: 't-mut' });
    s += cellRow(x0, 48, cw, 42, vals, { c: 0, size: 18, bold: true });
    vals.forEach((v, i) => {
      const cx = x0 + i * cw + cw / 2;
      s += K.text(cx, 36, String(1000 + i * 4), { size: 12, cls: 't-mut' });
      s += K.text(cx, 110, String(i), { size: 15, w: 'b', cls: 't-acc' });
      s += K.text(cx, 138, 'A[' + i + ']', { size: 12, cls: 't-mut' });
    });
    s += K.line(x0 + 3, 154, x0 + 6 * cw - 3, 154, { arrow: 'both', cls: 's-mut' });
    s += K.text(x0 + 3 * cw, 174, 'same type, side by side in memory', { size: 12, cls: 't-mut' });
    return K.svg(440, 188, s, { title: 'Array A with six values, indices 0 to 5 and consecutive memory addresses' });
  });

  D.register('xii2.array-insert', () => {
    const cw = 52;
    const x0 = 62;
    let s = '';
    s += K.text(8, 66, 'before', { size: 12, anchor: 'start', w: 'b' });
    s += K.text(8, 166, 'after', { size: 12, anchor: 'start', w: 'b' });
    s += cellRow(x0, 48, cw, 36, [23, 76, 12, 90, 34, 68], { c: 0, size: 16 });
    s += K.rect(x0 + 6 * cw, 48, cw, 36, { c: 6, r: 0, dash: '4 3' });
    s += cellRow(x0, 148, cw, 36, [23, 76, 50, 12, 90, 34, 68], { fills: [0, 0, 4, 1, 1, 1, 1], size: 16 });
    for (let i = 0; i < 7; i++) {
      s += K.text(x0 + i * cw + cw / 2, 40, String(i), { size: 12, cls: 't-mut', w: 'b' });
    }
    [0, 1].forEach((i) => {
      s += K.line(x0 + i * cw + cw / 2, 88, x0 + i * cw + cw / 2, 144, { cls: 's-mut', dash: '3 3' });
    });
    [2, 3, 4, 5].forEach((i) => {
      s += K.line(x0 + i * cw + cw / 2 - 6, 88, x0 + (i + 1) * cw + cw / 2 - 6, 144, { arrow: true, cls: 's-red' });
    });
    s += K.text(x0 + 3.5 * cw, 206, '50 goes to index 2, the rest shift right', { size: 12, w: 'b', cls: 't-acc' });
    return K.svg(440, 216, s, { title: 'Inserting 50 at index 2 of an array shifts every later element one place to the right' });
  });

  D.register('xii2.linked-list', () => {
    const vals = [23, 76, 12, 90, 34, 68];
    const addr = [2040, 3100, 1500, 5200, 2800, 4400];
    const xs = [30, 154, 278];
    let s = '';
    const nodes = vals.map((v, i) => {
      const x = xs[i % 3];
      const y = i < 3 ? 40 : 140;
      const n = node(x, y, v, { c: i === 0 ? 4 : 0, size: 17 });
      s += n.svg;
      s += K.text(x + 40, y + 58, '@' + addr[i], { size: 12, cls: 't-mut' });
      return n;
    });
    s += K.text(55, 16, 'HEAD', { size: 13, w: 'b', cls: 't-acc' });
    s += K.line(55, 22, 55, 38, { arrow: true, cls: 's-brand' });
    [0, 1, 3, 4].forEach((i) => {
      s += K.line(nodes[i].p[0], nodes[i].p[1], nodes[i + 1].left[0] - 1, nodes[i + 1].left[1], { arrow: true });
    });
    s += K.polyline([nodes[2].p, [398, nodes[2].p[1]], [398, 118], [55, 118], [55, 138]], { arrow: true });
    s += K.line(nodes[5].p[0], nodes[5].p[1], 372, nodes[5].p[1], { arrow: true });
    s += K.text(376, nodes[5].p[1], 'NULL', { size: 14, w: 'b', anchor: 'start', vmid: true, cls: 't-red' });
    return K.svg(440, 214, s, { title: 'Linked list of six nodes: each node has data and a pointer to the next node, the last points to NULL' });
  });

  D.register('xii2.ll-insert-delete', () => {
    let s = K.text(10, 16, 'Insert 50 after 76', { size: 14, w: 'b', anchor: 'start' });
    const y = 34;
    const a = node(10, y, 23);
    const b = node(130, y, 76);
    const c = node(250, y, 12);
    const n = node(190, y + 70, 50, { c: 4 });
    s += a.svg + b.svg + c.svg + n.svg;
    s += K.line(a.p[0], a.p[1], b.left[0] - 1, b.left[1], { arrow: true });
    s += K.line(b.p[0], b.p[1], c.left[0] - 1, c.left[1], { arrow: true, dash: '4 4', cls: 's-mut' });
    s += K.line(b.p[0] + 4, y + 40, n.top[0] + 6, y + 68, { arrow: true, cls: 's-grn' });
    s += K.line(n.p[0] + 4, y + 70, c.top[0] + 14, y + 42, { arrow: true, cls: 's-grn' });
    s += K.text(b.p[0] - 14, y + 62, '1', { size: 14, w: 'b', cls: 't-grn' });
    s += K.text(c.top[0] + 36, y + 62, '2', { size: 14, w: 'b', cls: 't-grn' });
    s += K.text(330, y + 22, 'old link\nbroken', { size: 12, anchor: 'start', cls: 't-mut', lh: 14 });
    s += K.text(10, 196, 'Delete 76', { size: 14, w: 'b', anchor: 'start' });
    const y2 = 242;
    const a2 = node(10, y2, 23);
    const b2 = node(130, y2, 76, { c: 6 });
    const c2 = node(250, y2, 12);
    s += a2.svg + b2.svg + c2.svg;
    s += K.line(a2.p[0], a2.p[1], b2.left[0] - 1, b2.left[1], { arrow: true, dash: '4 4', cls: 's-mut' });
    s += K.line(b2.p[0], b2.p[1], c2.left[0] - 1, c2.left[1], { arrow: true, dash: '4 4', cls: 's-mut' });
    s += K.polyline([[a2.p[0], y2], [a2.p[0], y2 - 26], [c2.top[0], y2 - 26], [c2.top[0], y2 - 1]], { arrow: true, cls: 's-grn' });
    s += K.text(b2.p[0] - 20, y2 + 58, 'removed', { size: 12, cls: 't-red', w: 'b' });
    s += K.text(330, y2 + 20, 'skip it:\n23 links to 12', { size: 12, anchor: 'start', cls: 't-mut', lh: 14 });
    return K.svg(440, 312, s, { title: 'Linked list insertion rewires two pointers; deletion makes the previous node skip the removed node' });
  });

  /* ---------- stack and queue ---------- */

  D.register('xii2.stack', (a) => {
    a = a || {};
    const items = a.items || [51, 34, 68];
    const w = a.w || 110;
    const ch = 38;
    const cx = 220;
    const n = items.length;
    const top = 70;
    const slots = Math.max(n, 3);
    const baseY = top + slots * ch;
    let s = '';
    s += K.line(cx - w / 2 - 6, 52, cx - w / 2 - 6, baseY + 4, { w: 3 });
    s += K.line(cx + w / 2 + 6, 52, cx + w / 2 + 6, baseY + 4, { w: 3 });
    s += K.line(cx - w / 2 - 6, baseY + 4, cx + w / 2 + 6, baseY + 4, { w: 3 });
    items.forEach((v, i) => {
      const y = baseY - (i + 1) * ch;
      const isTop = i === n - 1;
      s += K.box(cx - w / 2, y, w, ch, String(v), { c: isTop ? 4 : 0, r: 0, size: a.size || 16, bold: true });
      if (a.addr !== false) s += K.text(cx + w / 2 + 16, y + ch / 2, String(1000 + i * 4), { size: 12, anchor: 'start', vmid: true, cls: 't-mut' });
    });
    const ty = baseY - n * ch + ch / 2;
    s += K.text(34, ty, 'TOP', { size: 14, w: 'b', vmid: true, cls: 't-acc' });
    s += K.line(62, ty, cx - w / 2 - 8, ty, { arrow: true, cls: 's-brand' });
    s += K.line(cx - w / 4, 8, cx - w / 4, baseY - n * ch - 4, { arrow: true, cls: 's-grn', w: 2.5 });
    s += K.text(cx - w / 4 - 10, 22, a.push || 'PUSH 90', { size: 13, w: 'b', anchor: 'end', cls: 't-grn' });
    s += K.line(cx + w / 4, baseY - n * ch - 4, cx + w / 4, 8, { arrow: true, cls: 's-red', w: 2.5 });
    s += K.text(cx + w / 4 + 10, 22, a.pop || 'POP', { size: 13, w: 'b', anchor: 'start', cls: 't-red' });
    s += K.text(cx, baseY + 24, a.base || 'LIFO: last in, first out', { size: 13, w: 'b' });
    if (a.addr !== false) s += K.text(cx + w / 2 + 16, 52, 'address', { size: 11, anchor: 'start', cls: 't-mut' });
    return K.svg(440, baseY + 36, s, { title: 'Stack with TOP pointer, push and pop at the top' });
  });

  D.register('xii2.stack-trace', () => {
    const states = [
      { l: 'start', st: [], r: '' },
      { l: 'push 10', st: [10], r: '' },
      { l: 'push 20', st: [10, 20], r: '' },
      { l: 'push 30', st: [10, 20, 30], r: '' },
      { l: 'pop', st: [10, 20], r: '30 out' },
      { l: 'pop', st: [10], r: '20 out' },
    ];
    let s = '';
    const colW = 72;
    states.forEach((p, i) => {
      const cx = 36 + i * colW;
      const baseY = 150;
      s += K.text(cx, 20, p.l, { size: 13, w: 'b', cls: p.l === 'pop' ? 't-red' : p.l === 'start' ? 't-mut' : 't-grn' });
      s += K.line(cx - 28, 60, cx - 28, baseY + 2, { w: 2.5 });
      s += K.line(cx + 28, 60, cx + 28, baseY + 2, { w: 2.5 });
      s += K.line(cx - 28, baseY + 2, cx + 28, baseY + 2, { w: 2.5 });
      p.st.forEach((v, j) => {
        s += K.box(cx - 24, baseY - (j + 1) * 30, 48, 30, String(v), { c: j === p.st.length - 1 ? 4 : 0, r: 0, size: 15, bold: true });
      });
      s += K.text(cx, 176, p.st.length ? 'TOP = ' + p.st[p.st.length - 1] : 'empty', { size: 12, cls: 't-mut' });
      if (p.r) s += K.text(cx, 42, p.r, { size: 12, w: 'b', cls: 't-red' });
    });
    return K.svg(440, 190, s, { title: 'Stack trace: push 10, 20, 30 then two pops return 30 and then 20' });
  });

  D.register('xii2.queue', (a) => {
    a = a || {};
    const items = a.items || [23, 76, 90, 34];
    const n = items.length;
    const cw = Math.min(64, Math.floor(280 / n));
    const x0 = 98;
    const y = 62;
    let s = '';
    items.forEach((v, i) => {
      s += K.box(x0 + i * cw, y, cw, 44, String(v), { c: i === 0 ? 1 : i === n - 1 ? 4 : 0, r: 0, size: 16, bold: true });
      if (a.addr !== false) s += K.text(x0 + i * cw + cw / 2, y + 62, String(1000 + i * 4), { size: 11, cls: 't-mut' });
    });
    const x1 = x0 + n * cw;
    s += K.text(x0 + cw / 2, 30, 'FRONT', { size: 13, w: 'b', cls: 't-acc' });
    s += K.line(x0 + cw / 2, 36, x0 + cw / 2, y - 2, { arrow: true, cls: 's-brand' });
    s += K.text(x1 - cw / 2, 30, 'REAR', { size: 13, w: 'b', cls: 't-acc' });
    s += K.line(x1 - cw / 2, 36, x1 - cw / 2, y - 2, { arrow: true, cls: 's-brand' });
    s += K.line(x0 - 4, y + 22, 12, y + 22, { arrow: true, cls: 's-red', w: 2.5 });
    s += K.text(54, y + 8, 'DEQUEUE', { size: 12, w: 'b', cls: 't-red' });
    s += K.text(54, y + 46, '(remove)', { size: 11, cls: 't-mut' });
    s += K.line(430, y + 22, x1 + 4, y + 22, { arrow: true, cls: 's-grn', w: 2.5 });
    s += K.text(386, y + 8, 'ENQUEUE', { size: 12, w: 'b', cls: 't-grn' });
    s += K.text(386, y + 46, '(add)', { size: 11, cls: 't-mut' });
    s += K.text(220, y + 90, 'FIFO: first in, first out', { size: 13, w: 'b' });
    return K.svg(440, y + 104, s, { title: 'Queue with front and rear pointers, enqueue at the rear, dequeue at the front' });
  });

  D.register('xii2.queue-trace', () => {
    const rows = [
      ['start', []],
      ['enqueue A', ['A']],
      ['enqueue B', ['A', 'B']],
      ['enqueue C', ['A', 'B', 'C']],
      ['dequeue → A', ['B', 'C']],
      ['enqueue D', ['B', 'C', 'D']],
    ];
    let s = '';
    rows.forEach((r, i) => {
      const y = 22 + i * 48;
      s += K.text(10, y + 15, r[0], { size: 13, anchor: 'start', w: 'b', cls: r[0].indexOf('dequeue') === 0 ? 't-red' : r[0].indexOf('enq') === 0 ? 't-grn' : 't-mut' });
      const v = r[1];
      if (!v.length) s += K.text(180, y + 15, 'empty', { size: 12, anchor: 'start', cls: 't-mut' });
      v.forEach((c, j) => {
        const x = 180 + j * 50;
        s += K.box(x, y, 50, 30, c, { c: j === 0 ? 1 : j === v.length - 1 ? 4 : 0, r: 0, size: 15, bold: true });
        const tag = j === 0 && v.length === 1 ? 'F, R' : j === 0 ? 'F' : j === v.length - 1 ? 'R' : '';
        if (tag) s += K.text(x + 25, y - 5, tag, { size: 11, w: 'b', cls: 't-acc' });
      });
    });
    s += K.text(10, 316, 'F = front (leaves first),  R = rear (new arrivals)', { size: 12, anchor: 'start', cls: 't-mut' });
    return K.svg(440, 328, s, { title: 'Queue trace: enqueue A, B, C then dequeue returns A, then enqueue D' });
  });

  /* ---------- non-linear ---------- */

  D.register('xii2.tree-family', () => {
    let s = '';
    const root = [220, 36];
    const mids = [[142, 118], [367, 118]];
    const leaves = [[52, 204], [142, 204], [232, 204], [322, 204], [412, 204]];
    const bw = 82;
    const bh = 34;
    const link = (p, q) => K.polyline([[p[0], p[1] + bh / 2], [p[0], (p[1] + q[1]) / 2], [q[0], (p[1] + q[1]) / 2], [q[0], q[1] - bh / 2]], {});
    s += link(root, mids[0]) + link(root, mids[1]);
    [0, 1, 2].forEach((i) => (s += link(mids[0], leaves[i])));
    [3, 4].forEach((i) => (s += link(mids[1], leaves[i])));
    const b = (p, t, c, w) => K.box(p[0] - (w || bw) / 2, p[1] - bh / 2, w || bw, bh, t, { c: c, size: 13, bold: true });
    s += b(root, 'Abdul Rehman', 3, 120);
    s += b(mids[0], 'Arif', 1);
    s += b(mids[1], 'Tariq', 1);
    ['Saif', 'Mahnoor', 'Ibrahim', 'Shazmeen', 'Asadullah'].forEach((t, i) => (s += b(leaves[i], t, 5)));
    s += K.text(150, 28, 'root', { size: 12, w: 'b', anchor: 'end', cls: 't-red' });
    s += K.rect(8, 244, 16, 14, { c: 3, r: 2 }) + K.text(30, 255, 'root: no parent', { size: 12, anchor: 'start' });
    s += K.rect(150, 244, 16, 14, { c: 1, r: 2 }) + K.text(172, 255, 'parent + child', { size: 12, anchor: 'start' });
    s += K.rect(290, 244, 16, 14, { c: 5, r: 2 }) + K.text(312, 255, 'leaf: no children', { size: 12, anchor: 'start' });
    return K.svg(460, 268, s, { title: 'Family tree: Abdul Rehman is the root, Arif and Tariq are parents and children, five grandchildren are leaves' });
  });

  D.register('xii2.college-tree', () => {
    let s = K.box(150, 6, 140, 34, 'Principal (root)', { c: 3, size: 13, bold: true });
    const heads = [
      { t: 'Vice Principal', k: ['Exam Cell', 'Discipline'] },
      { t: 'Admin Head', k: ['Accounts', 'Office'] },
      { t: 'Academic Dean', k: ['HOD CS', 'HOD Maths'] },
    ];
    heads.forEach((h, i) => {
      const x = 8 + i * 144;
      const cx = x + 64;
      s += K.polyline([[220, 40], [220, 56], [cx, 56], [cx, 68]], {});
      s += K.box(x, 68, 128, 34, h.t, { c: 1, size: 13, bold: true });
      s += K.line(x + 10, 102, x + 10, 118 + 34, { cls: 's-mut' });
      h.k.forEach((k, j) => {
        s += K.line(x + 10, 118 + j * 36, x + 22, 118 + j * 36, { cls: 's-mut' });
        s += K.box(x + 22, 106 + j * 36, 106, 28, k, { c: 5, size: 12 });
      });
    });
    s += K.text(220, 206, 'one-to-many: every person traces back to the Principal', { size: 12, cls: 't-mut' });
    return K.svg(440, 218, s, { title: 'College organizational chart as a tree: Principal at root, three heads, sub heads as leaves' });
  });

  const T7 = [[220, 40], [110, 118], [330, 118], [55, 196], [165, 196], [275, 196], [385, 196]];
  const T7P = [[0, 1], [0, 2], [1, 3], [1, 4], [2, 5], [2, 6]];

  D.register('xii2.binary-tree', () => {
    const keys = [50, 30, 70, 20, 40, 60, 80];
    const path = [0, 2, 5];
    let s = '';
    T7P.forEach(([a, b]) => {
      const on = path.indexOf(a) >= 0 && path.indexOf(b) >= 0;
      s += edge(T7[a], T7[b], 20, on ? { cls: 's-acc', w: 4 } : {});
    });
    keys.forEach((k, i) => {
      s += circ(T7[i], 20, k, path.indexOf(i) >= 0 ? 4 : i === 0 ? 3 : i < 3 ? 1 : 5, path.indexOf(i) >= 0 ? { s: 's-acc' } : {});
    });
    s += K.text(172, 34, 'root', { size: 13, w: 'b', anchor: 'end', cls: 't-red' });
    s += K.text(82, 94, 'left child', { size: 12, anchor: 'end', cls: 't-mut' });
    s += K.text(356, 94, 'right child', { size: 12, anchor: 'start', cls: 't-mut' });
    s += K.text(55, 236, 'leaf', { size: 12, cls: 't-grn', w: 'b' });
    s += K.text(385, 236, 'leaf', { size: 12, cls: 't-grn', w: 'b' });
    s += K.text(220, 262, 'search 60:  50 → 70 → 60  (3 nodes, not 7)', { size: 13, w: 'b' });
    return K.svg(440, 274, s, { title: 'Binary tree with root 50: searching for 60 follows the path 50, 70, 60' });
  });

  D.register('xii2.tree-traverse', (a) => {
    const mode = (a && a.mode) || 'level';
    const L = ['A', 'B', 'C', 'D', 'E', 'F', 'G'];
    const orders = {
      level: [0, 1, 2, 3, 4, 5, 6],
      pre: [0, 1, 3, 4, 2, 5, 6],
      in: [3, 1, 4, 0, 5, 2, 6],
    };
    const names = { level: 'Level by level', pre: 'Pre-order (root, left, right)', in: 'In-order (left, root, right)' };
    const order = orders[mode];
    let s = K.text(220, 18, names[mode], { size: 14, w: 'b' });
    T7P.forEach(([p, q]) => {
      s += edge([T7[p][0], T7[p][1] + 12], [T7[q][0], T7[q][1] + 12], 20, {});
    });
    L.forEach((l, i) => {
      s += circ([T7[i][0], T7[i][1] + 12], 20, l, 1);
    });
    order.forEach((idx, k) => {
      s += badge(T7[idx][0] + 22, T7[idx][1] - 6, k + 1);
    });
    s += K.text(220, 262, 'Visit order: ' + order.map((i) => L[i]).join(' → '), { size: 13, w: 'b' });
    return K.svg(440, 274, s, { title: 'Binary tree with visit-order numbers: ' + names[mode] });
  });

  D.register('xii2.graph', () => {
    const P = { Peshawar: [66, 50], Islamabad: [215, 50], Lahore: [372, 92], Multan: [262, 176], Karachi: [90, 224] };
    const E = [
      ['Peshawar', 'Islamabad', '180', [0, -12]],
      ['Islamabad', 'Lahore', '380', [4, -14]],
      ['Islamabad', 'Multan', '550', [-30, 0]],
      ['Lahore', 'Multan', '340', [40, 8]],
      ['Multan', 'Karachi', '880', [0, -14]],
    ];
    let s = '';
    E.forEach(([a, b, w, off]) => {
      s += K.line(P[a][0], P[a][1], P[b][0], P[b][1], { w: 2.5 });
      s += K.text((P[a][0] + P[b][0]) / 2 + off[0], (P[a][1] + P[b][1]) / 2 + off[1] + 4, w, { size: 12, w: 'b', cls: 't-acc' });
    });
    Object.keys(P).forEach((k) => {
      s += K.box(P[k][0] - 40, P[k][1] - 15, 80, 30, k, { c: 1, r: 15, size: 13, bold: true });
    });
    s += K.text(436, 224, 'box = vertex (node)', { size: 12, anchor: 'end' });
    s += K.text(436, 242, 'line = edge (road)', { size: 12, anchor: 'end' });
    s += K.text(436, 260, 'number = distance, approx km', { size: 12, anchor: 'end', cls: 't-acc' });
    return K.svg(440, 272, s, { title: 'Road network graph: cities are vertices, roads are edges with distances' });
  });

  D.register('xii2.graph-bfs', () => {
    const P = { A: [50, 112], B: [150, 42], C: [150, 182], D: [270, 42], E: [270, 182], F: [390, 112] };
    const E = [['A', 'B'], ['A', 'C'], ['B', 'D'], ['C', 'D'], ['C', 'E'], ['D', 'F']];
    const ord = { A: 1, B: 2, C: 3, D: 4, E: 5, F: 6 };
    let s = '';
    E.forEach(([a, b]) => {
      s += edge(P[a], P[b], 20, { w: 2.5 });
    });
    Object.keys(P).forEach((k) => {
      s += circ(P[k], 20, k, k === 'A' ? 3 : 1);
      s += badge(P[k][0] + 22, P[k][1] - 20, ord[k]);
    });
    s += K.text(220, 238, 'Visit order from A: A → B → C → D → E → F', { size: 13, w: 'b' });
    return K.svg(440, 252, s, { title: 'Graph traversal from vertex A with visit numbers 1 to 6' });
  });

  D.register('xii2.operations', () => {
    const rows = [
      ['Insertion', 'add a new item'],
      ['Deletion', 'remove an item'],
      ['Traversal', 'visit every item'],
      ['Searching', 'find a given item'],
      ['Sorting', 'put in order'],
    ];
    let s = '';
    rows.forEach((r, i) => {
      const y = 8 + i * 56;
      s += K.text(8, y + 18, r[0], { size: 14, w: 'b', anchor: 'start' });
      s += K.text(8, y + 36, r[1], { size: 11, anchor: 'start', cls: 't-mut' });
      const x = 140;
      const w = 40;
      if (i === 0) {
        s += cellRow(x, y, w, 34, [3, 7, 5, 9], { fills: [0, 0, 4, 0], size: 15 });
        s += K.line(x + 2.5 * w, y - 6, x + 2.5 * w, y - 1, { arrow: true, cls: 's-grn' });
      } else if (i === 1) {
        s += cellRow(x, y, w, 34, [3, 7, '✕', 9], { fills: [0, 0, 3, 0], size: 15 });
      } else if (i === 2) {
        s += cellRow(x, y, w, 34, [3, 7, 5, 9], { c: 0, size: 15 });
        [1, 2, 3, 4].forEach((k) => {
          s += K.text(x + (k - 0.5) * w, y + 48, String(k), { size: 11, w: 'b', cls: 't-acc' });
        });
      } else if (i === 3) {
        s += cellRow(x, y, w, 34, [3, 7, 5, 9], { fills: [0, 0, 4, 0], size: 15 });
        s += K.text(x + 2.5 * w, y + 48, 'found', { size: 11, w: 'b', cls: 't-grn' });
      } else {
        s += cellRow(x, y, w, 34, [9, 3, 7], { c: 3, size: 15 });
        s += K.line(x + 3 * w + 8, y + 17, x + 3 * w + 30, y + 17, { arrow: true });
        s += cellRow(x + 3 * w + 36, y, w, 34, [3, 7, 9], { c: 5, size: 15 });
      }
    });
    return K.svg(440, 290, s, { title: 'Five operations on data structures: insertion, deletion, traversal, searching, sorting' });
  });

  /* ---------- 2.7 tracing retrieval ---------- */

  D.register('xii2.array-trace', () => {
    const vals = [10, 50, 20, 70, 90, 30];
    const cw = 56;
    const x0 = 52;
    let s = K.text(220, 16, 'Array = [10, 50, 20, 70, 90, 30]', { size: 14, w: 'b' });
    s += cellRow(x0, 50, cw, 40, vals, { c: 0, size: 17, bold: true });
    vals.forEach((_, i) => {
      s += K.text(x0 + i * cw + cw / 2, 108, String(i), { size: 14, w: 'b', cls: 't-acc' });
    });
    s += K.text(24, 74, 'value', { size: 11, cls: 't-mut' });
    s += K.text(24, 112, 'index', { size: 11, cls: 't-mut' });
    s += K.rect(x0 + 2 * cw, 50, cw, 40, { c: 4, r: 0, s: 's-acc' });
    s += K.text(x0 + 2 * cw + cw / 2, 70, '20', { size: 17, vmid: true, w: 'b' });
    s += K.line(x0 + 2 * cw + cw / 2, 140, x0 + 2 * cw + cw / 2, 120, { arrow: true, cls: 's-grn', w: 2.5 });
    s += K.text(x0 + 2 * cw + cw / 2, 158, 'Array[2] = 20', { size: 14, w: 'b', cls: 't-grn' });
    s += K.text(x0 + 2 * cw + cw / 2, 176, 'direct access: no search', { size: 12, cls: 't-mut' });
    const rows = [['Loop', 'Index', 'Array[index]', 'value']];
    vals.forEach((v, i) => rows.push([i + 1, i, 'Array[' + i + ']', v]));
    s += tbl(48, 192, [60, 60, 110, 70], 22, rows, rows.map((r, i) => (i === 0 ? null : [null, 1, null, 4])), 13);
    return K.svg(440, 360, s, { title: 'Tracing an array: direct access Array[2] is 20, and a loop visits index 0 to 5' });
  });

  D.register('xii2.ll-trace', () => {
    const vals = [12, 98, 23, 87, 56];
    const steps = [
      ['Step 1: temp at 12, is 12 = 87? No', 0],
      ['Step 2: move to next, 98 = 87? No', 1],
      ['Step 3: move to next, 23 = 87? No', 2],
      ['Step 4: move to next, 87 = 87? Yes: found', 3],
    ];
    let s = K.text(220, 16, 'Search Key: 87', { size: 14, w: 'b' });
    steps.forEach((st, r) => {
      const y = 28 + r * 88;
      s += K.text(8, y + 10, st[0], { size: 13, anchor: 'start', w: 'b', cls: r === 3 ? 't-grn' : '' });
      const ns = vals.map((v, i) => {
        const n = node(64 + i * 66, y + 20, v, { dw: 32, pw: 18, h: 30, size: 14, c: i === st[1] ? (r === 3 ? 5 : 4) : 6 });
        s += n.svg;
        return n;
      });
      s += K.text(28, y + 35, 'Head', { size: 12, w: 'b', cls: 't-acc' });
      s += K.line(46, y + 35, 63, y + 35, { arrow: true, cls: 's-brand' });
      [0, 1, 2, 3].forEach((i) => {
        s += K.line(ns[i].p[0], ns[i].p[1], ns[i + 1].left[0] - 1, ns[i + 1].left[1], { arrow: true });
      });
      s += K.line(ns[4].p[0], ns[4].p[1], ns[4].p[0] + 22, ns[4].p[1], { arrow: true });
      s += K.text(ns[4].p[0] + 24, ns[4].p[1], 'NULL', { size: 12, w: 'b', anchor: 'start', vmid: true, cls: 't-red' });
      const cx = ns[st[1]].top[0];
      s += K.line(cx, y + 66, cx, y + 54, { arrow: true, cls: 's-grn', w: 2 });
      s += K.text(cx, y + 76, 'temp', { size: 11, w: 'b', cls: 't-grn' });
    });
    return K.svg(440, 384, s, { title: 'Linked list search for 87: a temp pointer moves from the head one node at a time until 87 is found' });
  });

  /* ---------- scenario helpers reuse stack / queue ---------- */

  D.register('xii2.undo-stack', () =>
    D.render('xii2.stack', { items: ['Type "Hello"', 'Make bold', 'Delete word'], w: 170, addr: false, size: 13, push: 'new action', pop: 'Undo', base: 'latest action is undone first' })
  );

  D.register('xii2.print-queue', () => {
    let s = '';
    const docs = ['Doc 1', 'Doc 2', 'Doc 3', 'Doc 4'];
    s += K.box(8, 50, 84, 56, 'Printer', { c: 2, size: 14, bold: true });
    s += K.line(118, 78, 100, 78, { arrow: true, cls: 's-red', w: 2.5 });
    docs.forEach((d, i) => {
      s += K.box(122 + i * 74, 56, 70, 44, d, { c: i === 0 ? 1 : i === 3 ? 4 : 0, r: 0, size: 14, bold: true });
    });
    s += K.text(157, 40, 'FRONT', { size: 12, w: 'b', cls: 't-acc' });
    s += K.text(379, 40, 'REAR', { size: 12, w: 'b', cls: 't-acc' });
    s += K.text(220, 132, 'first document sent = first document printed', { size: 13, w: 'b' });
    return K.svg(440, 148, s, { title: 'Printer queue: documents print in the order they were sent' });
  });
})();
