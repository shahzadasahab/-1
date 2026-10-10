/* XII Ch3 (Programming Fundamentals) diagrams */
(function () {
  const D = Diagrams;
  let cid = 0;

  const T = (x, y, str, o) => K.text(x, y, str, o);

  /** a horizontal run of equal boxes; returns svg */
  function cells(x, y, w, h, labels, o) {
    o = o || {};
    let s = '';
    labels.forEach((l, i) => {
      const c = o.fills ? o.fills[i] : o.c;
      s += K.box(x + i * w, y, w, h, String(l), { c: c, r: o.r == null ? 4 : o.r, size: o.size || 14, s: o.s, bold: o.bold });
    });
    return s;
  }

  D.register('xii3.ds-types', () => {
    let s = '';
    s += K.box(150, 8, 140, 38, 'Data Structures', { c: 1, bold: true, size: 15 });
    s += K.line(220, 46, 220, 62);
    s += K.line(110, 62, 330, 62);
    s += K.line(110, 62, 110, 78, { arrow: true });
    s += K.line(330, 62, 330, 78, { arrow: true });
    s += K.box(20, 78, 180, 44, 'Primitive\n(single values)', { c: 0, bold: true, size: 14 });
    s += K.box(240, 78, 180, 44, 'Abstract\n(collections)', { c: 2, bold: true, size: 14 });
    s += cells(20, 140, 45, 34, ['int', 'float', 'char', 'bool'], { c: 0, size: 12 });
    s += T(110, 196, 'one value at a time', { size: 12, cls: 't-mut' });
    s += cells(240, 140, 45, 34, ['list', 'tuple', 'set', 'dict'], { c: 2, size: 12 });
    s += T(330, 196, 'many values together', { size: 12, cls: 't-mut' });
    s += K.line(110, 122, 110, 140, { arrow: true, cls: 's-mut' });
    s += K.line(330, 122, 330, 140, { arrow: true, cls: 's-mut' });
    return K.svg(440, 210, s, { title: 'Primitive versus abstract data structures' });
  });

  D.register('xii3.list-index', () => {
    const x0 = 35;
    const w = 74;
    const items = ['"apple"', '"mango"', '"banana"', '"grape"', '"kiwi"'];
    let s = '';
    s += T(220, 16, 'fruits = [ ... ]', { size: 14, w: 'b' });
    items.forEach((it, i) => {
      const x = x0 + i * w;
      s += T(x + w / 2, 50, '[' + i + ']', { size: 14, w: 'b', cls: 't-acc' });
      s += K.box(x, 60, w, 46, it, { c: [0, 1, 2, 4, 5][i], r: 4, size: 13 });
      s += T(x + w / 2, 130, '[' + (i - 5) + ']', { size: 14, w: 'b', cls: 't-red' });
    });
    s += K.line(x0, 150, x0 + 5 * w, 150, { arrow: true, cls: 's-acc' });
    s += T(220, 170, 'positive index: left to right, starts at 0', { size: 12, cls: 't-acc' });
    s += K.line(x0 + 5 * w, 186, x0, 186, { arrow: true, cls: 's-red' });
    s += T(220, 206, 'negative index: right to left, starts at -1', { size: 12, cls: 't-red' });
    return K.svg(440, 218, s, { title: 'List indexing with positive indices 0 to 4 and negative indices -5 to -1' });
  });

  D.register('xii3.list-slice', (args) => {
    const a = Object.assign(
      { code: 'nums[2:6]', start: 2, stop: 6, sel: [2, 3, 4, 5], result: '[2, 3, 4, 5]', dir: 1, fill: 5 },
      args || {}
    );
    const x0 = 20;
    const w = 40;
    let s = '';
    s += T(220, 20, a.code, { size: 16, w: 'b', cls: 't-acc' });
    for (let i = 0; i < 10; i++) {
      const on = a.sel.indexOf(i) >= 0;
      s += K.box(x0 + i * w, 40, w, 40, String(i), { c: on ? a.fill : 6, r: 3, bold: on });
      s += T(x0 + i * w + w / 2, 100, String(i), { size: 12, cls: 't-mut' });
    }
    if (a.start != null) {
      const xs = x0 + a.start * w;
      s += K.line(xs, 34, xs, 112, { cls: 's-grn', dash: '5 3', w: 2.4 });
      s += T(xs, 128, 'start', { size: 12, w: 'b', cls: 't-grn' });
    }
    if (a.stop != null) {
      const xe = x0 + a.stop * w;
      s += K.line(xe, 34, xe, 112, { cls: 's-red', dash: '5 3', w: 2.4 });
      s += T(xe, 128, 'stop (excluded)', { size: 12, w: 'b', cls: 't-red', anchor: a.stop > 8 ? 'end' : 'middle' });
    }
    if (a.dir < 0) {
      s += K.line(x0 + 10 * w - 6, 150, x0 + 6, 150, { arrow: true, cls: 's-acc' });
      s += T(220, 168, 'step = -1 : walk backwards', { size: 12, cls: 't-acc' });
    } else if (a.step) {
      s += K.line(x0 + 6, 150, x0 + 10 * w - 6, 150, { arrow: true, cls: 's-acc' });
      s += T(220, 168, 'step = ' + a.step + ' : take every ' + (a.step === 2 ? '2nd' : a.step + 'th') + ' item', { size: 12, cls: 't-acc' });
    }
    const ry = a.dir < 0 || a.step ? 202 : 164;
    s += T(220, ry, 'Result:  ' + a.result, { size: 15, w: 'b' });
    return K.svg(440, ry + 12, s, { title: 'Slicing ' + a.code + ' selects ' + a.result });
  });

  D.register('xii3.list-methods', () => {
    let s = '';
    const rows = [
      ['nums.append(40)', [10, 20, 30], [10, 20, 30, 40], 3, 'new item at the end'],
      ['nums.insert(1, 15)', [10, 20, 30], [10, 15, 20, 30], 1, 'new item at index 1'],
      ['nums.remove(20)', [10, 20, 30], [10, 30], -1, 'first 20 is removed'],
    ];
    rows.forEach((r, k) => {
      const y = 8 + k * 84;
      s += T(10, y + 14, r[0], { size: 14, w: 'b', anchor: 'start', cls: 't-acc' });
      s += T(430, y + 14, r[4], { size: 12, anchor: 'end', cls: 't-mut' });
      s += cells(10, y + 24, 38, 34, r[1], { c: 1, size: 13 });
      s += K.line(10 + r[1].length * 38 + 12, y + 41, 190, y + 41, { arrow: true, cls: 's-mut' });
      const fills = r[2].map((_, i) => (i === r[3] ? 5 : 1));
      s += cells(200, y + 24, 38, 34, r[2], { fills, size: 13 });
    });
    return K.svg(440, 262, s, { title: 'List methods append, insert and remove: before and after' });
  });

  D.register('xii3.list-vs-tuple', () => {
    let s = '';
    s += K.rect(8, 8, 205, 214, { c: 5, r: 10, s: 's-grn' });
    s += K.rect(227, 8, 205, 214, { c: 3, r: 10, s: 's-red' });
    s += T(110, 32, 'List  [ ]', { size: 16, w: 'b' });
    s += T(329, 32, 'Tuple  ( )', { size: 16, w: 'b' });
    s += T(110, 52, 'mutable', { size: 13, cls: 't-grn', w: 'b' });
    s += T(329, 52, 'immutable', { size: 13, cls: 't-red', w: 'b' });
    s += T(110, 80, 'a = [1, 2, 3]', { size: 13 });
    s += T(329, 80, 't = (1, 2, 3)', { size: 13 });
    s += cells(35, 94, 48, 38, [1, 2, 3], { c: 1, size: 15 });
    s += cells(254, 94, 48, 38, [1, 2, 3], { c: 6, size: 15 });
    s += T(110, 158, 'a[0] = 99', { size: 14, w: 'b', cls: 't-acc' });
    s += cells(35, 168, 48, 38, [99, 2, 3], { fills: [5, 1, 1], size: 15 });
    s += T(329, 150, 't[0] = 99', { size: 14, w: 'b', cls: 't-acc' });
    s += K.rect(305, 186, 48, 32, { c: 4, r: 6 });
    s += K.path('M313 186 L313 178 A16 16 0 0 1 345 178 L345 186', { s: 's-mut', w: 4 });
    s += K.circle(329, 202, 4.5, { c: 6 });
    s += T(110, 236, 'item changed: OK', { size: 12, cls: 't-grn', w: 'b' });
    s += T(329, 236, 'TypeError: not allowed', { size: 12, cls: 't-red', w: 'b' });
    return K.svg(440, 248, s, { title: 'List is mutable, tuple is immutable' });
  });

  D.register('xii3.tuple-inner', () => {
    let s = '';
    s += T(220, 18, 't = ([1, 2], [3, 4])', { size: 15, w: 'b' });
    s += K.rect(60, 30, 320, 56, { c: 6, r: 8, s: 's-mut' });
    s += K.box(80, 40, 130, 36, 't[0]  (fixed slot)', { c: 4, r: 4, size: 12 });
    s += K.box(230, 40, 130, 36, 't[1]  (fixed slot)', { c: 4, r: 4, size: 12 });
    s += K.line(145, 76, 145, 120, { arrow: true });
    s += K.line(295, 76, 295, 120, { arrow: true });
    s += cells(95, 120, 40, 36, [1, 2], { c: 1, size: 14 });
    s += K.box(135, 120, 40, 36, '99', { c: 5, r: 4, size: 14, bold: true });
    s += cells(245, 120, 40, 36, [3, 4], { c: 1, size: 14 });
    s += T(135, 176, 't[0].append(99)', { size: 13, w: 'b', cls: 't-acc' });
    s += T(220, 202, 'The tuple slots never change,', { size: 13, cls: 't-mut' });
    s += T(220, 220, 'but the list inside is mutable: (  [1, 2, 99], [3, 4]  )', { size: 12, cls: 't-mut' });
    return K.svg(440, 232, s, { title: 'A tuple holding lists: the inner list can still change' });
  });

  D.register('xii3.set-unique', () => {
    let s = '';
    s += T(112, 18, '{1, 4, 3, 3, 2, 2}', { size: 14, w: 'b' });
    const src = [1, 4, 3, 3, 2, 2];
    const dup = [false, false, false, true, false, true];
    src.forEach((v, i) => {
      s += K.box(10 + i * 34, 34, 34, 34, String(v), { c: dup[i] ? 6 : 1, r: 4, size: 14 });
      if (dup[i]) s += K.line(14 + i * 34, 38, 40 + i * 34, 64, { cls: 's-red', w: 2.4 });
      if (dup[i]) s += K.line(40 + i * 34, 38, 14 + i * 34, 64, { cls: 's-red', w: 2.4 });
    });
    s += T(112, 92, 'duplicates (red) are dropped', { size: 12, cls: 't-red' });
    s += K.line(222, 51, 262, 51, { arrow: true });
    s += T(242, 38, 'set', { size: 13, w: 'b', cls: 't-acc' });
    s += T(350, 18, '{1, 2, 3, 4}', { size: 14, w: 'b' });
    [1, 2, 3, 4].forEach((v, i) => {
      s += K.circle(284 + i * 40, 51, 17, { c: 5 });
      s += T(284 + i * 40, 52, String(v), { size: 14, vmid: true, w: 'b' });
    });
    s += T(350, 92, 'only unique values stay', { size: 12, cls: 't-grn' });
    s += T(220, 128, 'Order is not guaranteed and there is no index.', { size: 13, cls: 't-mut' });
    return K.svg(440, 142, s, { title: 'A set keeps only unique elements' });
  });

  D.register('xii3.venn', (args) => {
    const op = (args && args.op) || 'union';
    const id = 'vn' + ++cid;
    const R = 80;
    const ax = 155;
    const bx = 285;
    const cy = 112;
    const circ = (cx) => 'M' + (cx - R) + ' ' + cy + ' a' + R + ' ' + R + ' 0 1 0 ' + 2 * R + ' 0 a' + R + ' ' + R + ' 0 1 0 ' + -2 * R + ' 0Z';
    const defs =
      '<clipPath id="' + id + 'A"><path d="' + circ(ax) + '"/></clipPath>' +
      '<clipPath id="' + id + 'B"><path d="' + circ(bx) + '"/></clipPath>' +
      '<clipPath id="' + id + 'nA"><path clip-rule="evenodd" d="M0 0H440V240H0Z ' + circ(ax) + '"/></clipPath>' +
      '<clipPath id="' + id + 'nB"><path clip-rule="evenodd" d="M0 0H440V240H0Z ' + circ(bx) + '"/></clipPath>';
    const info = {
      union: ['Union', 'A | B  or  A.union(B)', '{1, 2, 3, 4, 5, 6}', 'everything from both sets'],
      intersection: ['Intersection', 'A & B  or  A.intersection(B)', '{3, 4}', 'only the common elements'],
      difference: ['Difference', 'A - B  or  A.difference(B)', '{1, 2}', 'in A but NOT in B'],
      symdiff: ['Symmetric Difference', 'A ^ B  or  A.symmetric_difference(B)', '{1, 2, 5, 6}', 'in either, but NOT in both'],
    }[op];
    let s = '<defs>' + defs + '</defs>';
    const fill = (cls, cx, clip) => '<circle cx="' + cx + '" cy="' + cy + '" r="' + R + '" class="shape ' + cls + '" stroke="none" clip-path="url(#' + id + clip + ')"/>';
    const full = (cls, cx) => '<circle cx="' + cx + '" cy="' + cy + '" r="' + R + '" class="shape ' + cls + '" stroke="none"/>';
    if (op === 'union') s += full('c0', ax) + full('c0', bx);
    if (op === 'intersection') s += fill('c4', bx, 'A');
    if (op === 'difference') s += fill('c1', ax, 'nB');
    if (op === 'symdiff') s += fill('c1', ax, 'nB') + fill('c3', bx, 'nA');
    s += K.circle(ax, cy, R, { s: 's-acc' }) + K.circle(bx, cy, R, { s: 's-brand' });
    s += T(100, 22, 'A', { size: 18, w: 'b', cls: 't-acc' });
    s += T(340, 22, 'B', { size: 18, w: 'b', cls: 't-acc' });
    [[105, 95, 1], [105, 130, 2], [220, 95, 3], [220, 130, 4], [335, 95, 5], [335, 130, 6]].forEach(([x, y, v]) => {
      s += T(x, y, String(v), { size: 16, w: 'b', vmid: true });
    });
    s += T(220, 218, info[0] + ':  ' + info[1], { size: 13, w: 'b' });
    s += T(220, 238, '= ' + info[2] + '   (' + info[3] + ')', { size: 12, cls: 't-mut' });
    return K.svg(440, 250, s, { title: 'Venn diagram of set ' + info[0] + ' for A={1,2,3,4} and B={3,4,5,6}' });
  });

  D.register('xii3.dict-table', () => {
    let s = '';
    s += T(120, 18, 'Key (unique)', { size: 14, w: 'b', cls: 't-acc' });
    s += T(330, 18, 'Value', { size: 14, w: 'b', cls: 't-acc' });
    const rows = [
      ['"name"', '"Alice"'],
      ['"age"', '31'],
      ['"city"', '"Karachi"'],
    ];
    rows.forEach((r, i) => {
      const y = 30 + i * 52;
      s += K.box(50, y, 140, 38, r[0], { c: 1, r: 6, size: 15, bold: true });
      s += K.line(190, y + 19, 260, y + 19, { arrow: true });
      s += T(225, y + 12, ':', { size: 16, w: 'b' });
      s += K.box(260, y, 140, 38, r[1], { c: 4, r: 6, size: 15 });
    });
    s += T(220, 206, 'person = { "name": "Alice", "age": 31, "city": "Karachi" }', { size: 12, cls: 't-mut' });
    s += T(220, 232, 'person["name"]  gives  "Alice"', { size: 14, w: 'b', cls: 't-grn' });
    return K.svg(440, 246, s, { title: 'A dictionary stores key to value pairs' });
  });

  D.register('xii3.dict-views', () => {
    let s = '';
    s += K.box(100, 6, 240, 34, 'person = {"name": "Asghar", "age": 30}', { c: 6, r: 6, size: 12 });
    const cols = [
      ['keys()', 'all keys', ['"name"', '"age"'], 1],
      ['values()', 'all values', ['"Asghar"', '30'], 4],
      ['items()', 'key-value tuples', ['("name", "Asghar")', '("age", 30)'], 2],
    ];
    cols.forEach((c, i) => {
      const x = 4 + i * 146;
      s += K.line(220, 40, x + 69, 70, { arrow: true, cls: 's-mut' });
      s += K.box(x, 72, 138, 30, 'person.' + c[0], { c: c[3], r: 6, size: 13, bold: true });
      s += T(x + 69, 120, c[1], { size: 12, cls: 't-mut' });
      c[2].forEach((it, k) => {
        s += K.box(x, 132 + k * 36, 138, 30, it, { c: 6, r: 4, size: 12 });
      });
    });
    s += T(220, 224, 'Views are LIVE: add a new key and they update automatically.', { size: 12, cls: 't-mut' });
    return K.svg(440, 236, s, { title: 'Dictionary views keys, values and items' });
  });

  D.register('xii3.builtin-funcs', () => {
    let s = '';
    s += T(220, 18, 's = {5, 1, 9, 3, 7}', { size: 15, w: 'b' });
    const rows = [
      ['len(s)', '5', 'number of elements', 1],
      ['min(s)', '1', 'smallest element', 0],
      ['max(s)', '9', 'largest element', 3],
      ['sum(s)', '25', 'sum of all elements', 4],
      ['sorted(s)', '[1, 3, 5, 7, 9]', 'returns a sorted LIST', 5],
    ];
    rows.forEach((r, i) => {
      const y = 32 + i * 42;
      s += K.box(10, y, 100, 34, r[0], { c: r[3], r: 6, size: 14, bold: true });
      s += K.line(110, y + 17, 138, y + 17, { arrow: true, cls: 's-mut' });
      s += K.box(140, y, 120, 34, r[1], { c: 6, r: 6, size: 14 });
      s += T(270, y + 18, r[2], { size: 12, anchor: 'start', vmid: true, cls: 't-mut' });
    });
    return K.svg(440, 246, s, { title: 'Built-in functions len, min, max, sum and sorted on a set' });
  });

  D.register('xii3.attendance-flow', () => {
    let s = '';
    s += K.box(100, 6, 240, 36, 'students = ["Ali", "Sara", ...]', { c: 1, r: 18, size: 12 });
    s += K.line(220, 42, 220, 58, { arrow: true });
    s += K.box(120, 58, 200, 34, 'present_count = 0', { c: 0, r: 6, size: 13 });
    s += K.line(220, 92, 220, 108, { arrow: true });
    s += K.poly([[220, 108], [310, 140], [220, 172], [130, 140]], { c: 4 });
    s += T(220, 140, 'next student?', { size: 12, vmid: true, w: 'b' });
    s += K.line(220, 172, 220, 192, { arrow: true });
    s += T(230, 186, 'yes', { size: 12, anchor: 'start', cls: 't-grn', w: 'b' });
    s += K.box(110, 192, 220, 34, 'input: present? (yes/no)', { c: 2, r: 6, size: 13 });
    s += K.line(220, 226, 220, 242, { arrow: true });
    s += K.poly([[220, 242], [310, 266], [220, 290], [130, 266]], { c: 4 });
    s += T(220, 266, 'status == "yes"?', { size: 12, vmid: true, w: 'b' });
    s += K.line(310, 266, 340, 266, { arrow: true });
    s += T(325, 254, 'yes', { size: 12, cls: 't-grn', w: 'b' });
    s += K.box(340, 244, 94, 44, 'present_count\n+= 1', { c: 5, r: 6, size: 12 });
    s += T(232, 302, 'no', { size: 12, anchor: 'start', cls: 't-red', w: 'b' });
    s += K.polyline([[387, 288], [387, 312], [30, 312], [30, 140], [128, 140]], { arrow: true });
    s += K.line(220, 290, 220, 312, {});
    s += K.line(310, 140, 346, 140, { arrow: true });
    s += T(328, 129, 'done', { size: 12, cls: 't-mut', w: 'b' });
    s += K.box(346, 116, 90, 48, 'print total,\npresent,\nabsent', { c: 3, r: 6, size: 11 });
    return K.svg(440, 324, s, { title: 'Flowchart of the students attendance program' });
  });

  D.register('xii3.word-freq', () => {
    let s = '';
    s += K.box(20, 8, 400, 34, '"python is easy python is fun"', { c: 6, r: 6, size: 14 });
    s += T(84, 64, 'sentence.split()', { size: 13, w: 'b', cls: 't-acc', anchor: 'start' });
    s += K.line(70, 42, 70, 77, { arrow: true });
    s += cells(40, 78, 60, 32, ['python', 'is', 'easy', 'python', 'is', 'fun'].map((w) => w), { c: 1, size: 12 });
    s += T(40, 134, 'for word in words:', { size: 13, w: 'b', cls: 't-acc', anchor: 'start' });
    s += T(40, 154, 'freq[word] = freq.get(word, 0) + 1', { size: 12, cls: 't-mut', anchor: 'start' });
    const d = [['"python"', 2], ['"is"', 2], ['"easy"', 1], ['"fun"', 1]];
    d.forEach((r, i) => {
      const x = 30 + i * 100;
      s += K.box(x, 182, 90, 28, r[0], { c: 4, r: 4, size: 13 });
      s += K.box(x, 210, 90, 28, String(r[1]), { c: r[1] > 1 ? 5 : 6, r: 4, size: 14, bold: true });
    });
    s += T(220, 260, '{"python": 2, "is": 2, "easy": 1, "fun": 1}', { size: 13, w: 'b' });
    return K.svg(440, 270, s, { title: 'Word frequency: split the sentence, then count words in a dictionary' });
  });

  D.register('xii3.func-anatomy', () => {
    let s = '';
    s += K.rect(8, 8, 250, 134, { c: 6, r: 8 });
    s += K.rect(14, 18, 238, 28, { c: 4, r: 4 });
    s += K.rect(14, 52, 238, 28, { c: 1, r: 4 });
    s += K.rect(14, 86, 238, 28, { c: 5, r: 4 });
    s += T(24, 38, 'def add(a, b):', { size: 15, anchor: 'start', w: 'b' });
    s += T(44, 72, 'result = a + b', { size: 15, anchor: 'start' });
    s += T(44, 106, 'return result', { size: 15, anchor: 'start' });
    s += K.line(268, 32, 252, 32, { arrow: true, cls: 's-acc' });
    s += T(274, 28, 'def keyword,', { size: 12, anchor: 'start', w: 'b' });
    s += T(274, 43, 'name: add', { size: 12, anchor: 'start', w: 'b' });
    s += K.line(268, 66, 252, 66, { arrow: true, cls: 's-acc' });
    s += T(274, 70, 'Function body', { size: 12, anchor: 'start', w: 'b' });
    s += K.line(268, 100, 252, 100, { arrow: true, cls: 's-acc' });
    s += T(274, 96, 'return statement:', { size: 12, anchor: 'start', w: 'b' });
    s += T(274, 111, 'result to the caller', { size: 12, anchor: 'start', w: 'b' });
    s += T(24, 160, 'Parameters: a, b  (inputs inside the brackets)', { size: 12, anchor: 'start', cls: 't-acc' });
    s += T(24, 184, 'Call:  add(5, 3)   arguments 5 and 3', { size: 13, anchor: 'start', w: 'b' });
    s += T(24, 208, 'Output:  8', { size: 13, anchor: 'start', w: 'b', cls: 't-grn' });
    return K.svg(440, 222, s, { title: 'Parts of a function: name, parameters, body and return' });
  });

  D.register('xii3.func-flow', () => {
    let s = '';
    s += K.rect(8, 8, 170, 150, { c: 1, r: 8 });
    s += T(93, 28, 'Main program', { size: 14, w: 'b' });
    s += K.rect(18, 42, 150, 34, { c: 6, r: 4 });
    s += T(93, 59, 'result = add(5, 3)', { size: 12, vmid: true });
    s += K.rect(18, 98, 150, 34, { c: 6, r: 4 });
    s += T(93, 115, 'print(result)', { size: 12, vmid: true });
    s += K.rect(262, 8, 170, 150, { c: 5, r: 8 });
    s += T(347, 28, 'Function add', { size: 14, w: 'b' });
    s += K.rect(272, 42, 150, 34, { c: 6, r: 4 });
    s += T(347, 59, 'def add(a, b):', { size: 12, vmid: true });
    s += K.rect(272, 98, 150, 34, { c: 6, r: 4 });
    s += T(347, 115, 'return a + b', { size: 12, vmid: true });
    s += K.line(168, 52, 272, 52, { arrow: true, cls: 's-acc', w: 2.4 });
    s += K.circle(188, 38, 10, { c: 4 }) + T(188, 39, '1', { size: 12, vmid: true, w: 'b' });
    s += T(220, 70, 'arguments 5, 3', { size: 11, cls: 't-acc', w: 'b' });
    s += K.line(347, 76, 347, 98, { arrow: true, cls: 's-mut' });
    s += T(355, 91, 'a=5, b=3', { size: 11, anchor: 'start', cls: 't-mut' });
    s += K.line(272, 118, 168, 118, { arrow: true, cls: 's-grn', w: 2.4 });
    s += K.circle(252, 104, 10, { c: 5 }) + T(252, 105, '2', { size: 12, vmid: true, w: 'b' });
    s += T(220, 136, 'returns 8', { size: 12, cls: 't-grn', w: 'b' });
    s += T(220, 188, '1  call with arguments', { size: 13 });
    s += T(220, 208, '2  return value goes back to the caller', { size: 13 });
    s += T(220, 232, 'print(result)  shows  8', { size: 14, w: 'b', cls: 't-grn' });
    return K.svg(440, 244, s, { title: 'Function call and return flow' });
  });

  D.register('xii3.decompose', () => {
    let s = '';
    s += K.box(100, 6, 240, 38, 'Big problem:\nArithmetic Calculator', { c: 3, r: 8, size: 13, bold: true });
    const subs = [['add(a, b)', 'a + b', 1], ['subtract(a, b)', 'a - b', 0], ['multiply(a, b)', 'a * b', 2], ['divide(a, b)', 'a / b', 4]];
    s += K.line(220, 44, 220, 56);
    s += K.line(55, 56, 385, 56);
    subs.forEach((r, i) => {
      const x = 4 + i * 110;
      const cx = x + 51;
      s += K.line(cx, 56, cx, 72, { arrow: true });
      s += K.box(x, 72, 102, 56, r[0] + '\n' + r[1], { c: r[2], r: 6, size: 12 });
      s += K.line(cx, 128, cx, 150, { arrow: true, cls: 's-mut' });
    });
    s += K.box(40, 150, 360, 44, 'Main program: input num1, num2 ->\ncall each function -> print results', { c: 6, r: 8, size: 12 });
    s += T(220, 218, 'Small sub-problems, each solved by one function', { size: 12, cls: 't-mut' });
    return K.svg(440, 230, s, { title: 'Decomposing a calculator into four function sub-problems' });
  });

  D.register('xii3.scope', () => {
    let s = '';
    s += K.rect(6, 6, 428, 232, { c: 1, r: 12, s: 's-acc' });
    s += T(20, 26, 'Global scope', { size: 14, w: 'b', anchor: 'start', cls: 't-acc' });
    s += K.box(20, 40, 120, 34, 'x = 10', { c: 4, r: 6, size: 15, bold: true });
    s += T(80, 92, 'global variable', { size: 12, cls: 't-mut' });
    s += T(80, 110, 'readable inside', { size: 12, cls: 't-grn', w: 'b' });
    s += T(80, 125, 'functions too', { size: 12, cls: 't-grn', w: 'b' });
    s += K.rect(170, 34, 252, 148, { c: 5, r: 10, s: 's-grn' });
    s += T(184, 54, 'Local scope: function add(a, b)', { size: 13, w: 'b', anchor: 'start', cls: 't-grn' });
    s += K.box(184, 66, 60, 34, 'a', { c: 0, r: 6, size: 14 });
    s += K.box(252, 66, 60, 34, 'b', { c: 0, r: 6, size: 14 });
    s += K.box(320, 66, 90, 34, 'result', { c: 0, r: 6, size: 14 });
    s += T(296, 124, 'local variables', { size: 12, cls: 't-mut' });
    s += T(296, 146, 'live only inside the function', { size: 12, cls: 't-mut' });
    s += K.line(140, 57, 170, 57, { arrow: true, cls: 's-grn', w: 2.4 });
    s += K.polyline([[360, 182], [360, 204], [110, 204]], { cls: 's-red', w: 2.4 });
    s += K.line(110, 204, 100, 204, { arrow: true, cls: 's-red', w: 2.4 });
    s += T(110, 226, 'print(result) outside: NameError', { size: 12, anchor: 'start', cls: 't-red', w: 'b' });
    return K.svg(440, 246, s, { title: 'Local versus global scope' });
  });

  D.register('xii3.file-lifecycle', () => {
    let s = '';
    const steps = [
      ['open()', 'file object\ncreated', 1],
      ['read() / write()', 'work happens\nin RAM', 4],
      ['close()', 'buffer flushed\nto disk', 5],
    ];
    steps.forEach((r, i) => {
      const x = 8 + i * 148;
      s += K.box(x, 8, 128, 40, r[0], { c: r[2], r: 8, size: 14, bold: true });
      s += T(x + 64, 66, r[1], { size: 12, cls: 't-mut' });
      s += K.circle(x + 12, 8, 11, { c: 6 }) + T(x + 12, 9, String(i + 1), { size: 12, vmid: true, w: 'b' });
      if (i < 2) s += K.line(x + 128, 28, x + 148, 28, { arrow: true });
    });
    s += K.rect(8, 118, 150, 56, { c: 6, r: 8 });
    s += T(83, 140, 'Disk / Storage', { size: 13, w: 'b' });
    s += T(83, 160, 'myfile.txt  (persistent)', { size: 11, cls: 't-mut' });
    s += K.rect(282, 118, 150, 56, { c: 2, r: 8 });
    s += T(357, 140, 'RAM + Program', { size: 13, w: 'b' });
    s += T(357, 160, 'file object  f', { size: 11, cls: 't-mut' });
    s += K.line(158, 134, 282, 134, { arrow: true, cls: 's-acc' });
    s += T(220, 126, 'open / read', { size: 12, cls: 't-acc', w: 'b' });
    s += K.line(282, 160, 158, 160, { arrow: true, cls: 's-grn' });
    s += T(220, 176, 'write / close', { size: 12, cls: 't-grn', w: 'b' });
    s += T(220, 210, 'Variables vanish when the program ends; files stay.', { size: 13, cls: 't-mut' });
    return K.svg(440, 224, s, { title: 'File life cycle: open, read or write, close' });
  });

  D.register('xii3.file-modes', () => {
    let s = '';
    const cw = [56, 118, 112, 154];
    const head = ['Mode', 'Name', 'Pointer', 'If file missing'];
    const rows = [
      ["'r'", 'Read', 'Beginning', 'Error (must exist)', 1],
      ["'w'", 'Write', 'Beginning', 'Creates new file', 3],
      ["'a'", 'Append', 'End', 'Creates new file', 5],
      ["'rb'", 'Read Binary', 'Beginning', 'Error (must exist)', 1],
      ["'wb'", 'Write Binary', 'Beginning', 'Creates new file', 3],
    ];
    const rh = 36;
    let x = 4;
    head.forEach((h, j) => {
      s += K.rect(x, 4, cw[j], 34, { c: 6, r: 0, cls: 'cell' });
      s += T(x + cw[j] / 2, 21, h, { size: 13, vmid: true, w: 'b' });
      x += cw[j];
    });
    rows.forEach((r, i) => {
      let xx = 4;
      cw.forEach((w, j) => {
        s += K.rect(xx, 38 + i * rh, w, rh, { c: j === 0 ? r[4] : null, r: 0, cls: 'cell' });
        s += T(xx + w / 2, 38 + i * rh + rh / 2, r[j], { size: 13, vmid: true, w: j === 0 ? 'b' : '' });
        xx += w;
      });
    });
    s += T(220, 238, "'w' erases old content!   'a' keeps it.   Default mode is 'r'.", { size: 12, cls: 't-red', w: 'b' });
    return K.svg(444, 252, s, { title: 'File modes r, w, a, rb and wb' });
  });

  D.register('xii3.write-vs-append', () => {
    let s = '';
    s += T(220, 16, 'myfile.txt  before:', { size: 13, w: 'b' });
    s += K.box(120, 24, 200, 52, 'Alice: 88\nBob: 75', { c: 6, r: 6, size: 13 });
    s += K.line(150, 76, 90, 110, { arrow: true, cls: 's-red' });
    s += K.line(290, 76, 350, 110, { arrow: true, cls: 's-grn' });
    s += T(90, 100, "open('w')", { size: 13, w: 'b', cls: 't-red', anchor: 'end' });
    s += T(350, 100, "open('a')", { size: 13, w: 'b', cls: 't-grn', anchor: 'start' });
    s += T(100, 130, 'write("Carol: 92")', { size: 12, cls: 't-mut' });
    s += T(340, 130, 'write("Carol: 92")', { size: 12, cls: 't-mut' });
    s += K.box(20, 142, 160, 52, 'Carol: 92', { c: 3, r: 6, size: 13 });
    s += K.box(260, 142, 160, 70, 'Alice: 88\nBob: 75\nCarol: 92', { c: 5, r: 6, size: 13 });
    s += T(100, 214, 'old content ERASED', { size: 12, cls: 't-red', w: 'b' });
    s += T(340, 230, 'added at the END', { size: 12, cls: 't-grn', w: 'b' });
    return K.svg(440, 242, s, { title: 'Write mode overwrites, append mode adds at the end' });
  });

  D.register('xii3.try-except', () => {
    let s = '';
    s += K.box(130, 6, 180, 34, 'try: open("myfile.txt")', { c: 1, r: 6, size: 12 });
    s += K.line(220, 40, 220, 56, { arrow: true });
    s += K.poly([[220, 56], [310, 86], [220, 116], [130, 86]], { c: 4 });
    s += T(220, 86, 'file found?', { size: 13, vmid: true, w: 'b' });
    s += K.line(130, 86, 90, 86, { arrow: true });
    s += T(110, 78, 'yes', { size: 12, cls: 't-grn', w: 'b' });
    s += K.line(310, 86, 350, 86, { arrow: true });
    s += T(330, 78, 'no', { size: 12, cls: 't-red', w: 'b' });
    s += K.box(6, 70, 84, 64, 'read and\nprint lines', { c: 5, r: 6, size: 12 });
    s += K.box(350, 70, 84, 64, 'FileNotFound\nError raised', { c: 3, r: 6, size: 11 });
    s += K.line(392, 134, 392, 160, { arrow: true });
    s += K.box(252, 160, 182, 44, 'except FileNotFoundError:\nfriendly message', { c: 7, r: 6, size: 11 });
    s += K.line(48, 134, 48, 224, {});
    s += K.line(48, 224, 220, 224, {});
    s += K.line(343, 204, 343, 224, {});
    s += K.line(343, 224, 220, 224, {});
    s += K.line(220, 224, 220, 240, { arrow: true });
    s += K.box(120, 240, 200, 32, 'program continues normally', { c: 6, r: 6, size: 12 });
    return K.svg(440, 282, s, { title: 'try and except flow for file errors' });
  });

  D.register('xii3.for-trace', () => {
    let s = '';
    s += T(220, 16, 'for num in numbers:', { size: 14, w: 'b', cls: 't-acc' });
    const vals = [5, 10, 15];
    vals.forEach((v, i) => {
      const y = 28 + i * 52;
      s += T(8, y + 22, 'round ' + (i + 1), { size: 12, anchor: 'start', cls: 't-mut', vmid: true });
      vals.forEach((u, k) => {
        s += K.box(80 + k * 60, y, 60, 40, String(u), { c: k === i ? 4 : 6, r: 4, size: 15, bold: k === i });
      });
      s += K.line(266, y + 20, 296, y + 20, { arrow: true, cls: 's-mut' });
      s += T(304, y + 20, 'num = ' + v, { size: 14, w: 'b', anchor: 'start', vmid: true });
    });
    s += T(220, 196, 'The loop visits each element once, in order.', { size: 12, cls: 't-mut' });
    return K.svg(440, 208, s, { title: 'A for loop visits each list item in turn' });
  });

  D.register('xii3.grade-flow', () => {
    let s = '';
    const st = [
      ["open('w')", 'Alice: 88\nBob: 75\nCarol: 92', 3, 'STEP 1: write'],
      ["open('a')", '+ David: 81', 5, 'STEP 2: append'],
      ["open('r')", 'readlines()\nsplit(": ")', 1, 'STEP 3: read'],
    ];
    st.forEach((r, i) => {
      const x = 4 + i * 148;
      s += T(x + 66, 16, r[3], { size: 12, w: 'b', cls: 't-acc' });
      s += K.box(x, 26, 132, 32, r[0], { c: r[2], r: 6, size: 14, bold: true });
      s += K.line(x + 66, 58, x + 66, 74, { arrow: true, cls: 's-mut' });
      s += K.box(x, 74, 132, 62, r[1], { c: 6, r: 6, size: 12 });
      if (i < 2) s += K.line(x + 132, 42, x + 148, 42, { arrow: true });
    });
    s += K.line(354, 136, 354, 156, { arrow: true, cls: 's-mut' });
    s += K.box(120, 156, 314, 34, 'total = 88 + 75 + 92 + 81 = 336,  average = 84.0', { c: 4, r: 6, size: 12 });
    return K.svg(440, 202, s, { title: 'Grade tracker: write, append, then read and average' });
  });
})();
