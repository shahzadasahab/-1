/* XI Ch3 (Programming Fundamentals / Python) diagrams */
(function () {
  const D = Diagrams;
  const MONO = 'ui-monospace,Menlo,Consolas,monospace';
  const mono = (s) => '<g font-family="' + MONO + '" style="font-variant-ligatures:none;font-feature-settings:\'liga\' 0,\'calt\' 0">' + s + '</g>';
  const T = (x, y, s, o) => K.text(x, y, s, o);
  const mut = (x, y, s, o) => K.text(x, y, s, Object.assign({ size: 11, cls: 't-mut' }, o));
  const arr = (x1, y1, x2, y2, o) => K.line(x1, y1, x2, y2, Object.assign({ arrow: true }, o));
  const pl = (pts, o) => K.polyline(pts, Object.assign({ arrow: true }, o));
  const oval = (cx, cy, w, h, l, c) => K.rect(cx - w / 2, cy - h / 2, w, h, { c: c == null ? 6 : c, r: h / 2 }) + T(cx, cy, l, { size: 12, vmid: true });
  const proc = (cx, cy, w, h, l, c, size) => K.box(cx - w / 2, cy - h / 2, w, h, l, { c: c == null ? 1 : c, size: size || 12, r: 6 });
  const io = (cx, cy, w, h, l, c) =>
    K.poly([[cx - w / 2 + 10, cy - h / 2], [cx + w / 2, cy - h / 2], [cx + w / 2 - 10, cy + h / 2], [cx - w / 2, cy + h / 2]], { c: c == null ? 0 : c }) +
    T(cx, cy, l, { size: 12, vmid: true });
  const dec = (cx, cy, w, h, l, c) =>
    K.poly([[cx, cy - h / 2], [cx + w / 2, cy], [cx, cy + h / 2], [cx - w / 2, cy]], { c: c == null ? 4 : c }) + T(cx, cy, l, { size: 12, vmid: true });
  const bitCell = (x, y, w, h, b, c1, size) =>
    K.rect(x, y, w, h, { c: b === '1' || b === 1 ? c1 : 6, r: 4 }) + T(x + w / 2, y + h / 2, String(b), { size: size || 15, vmid: true, w: 'b' });

  D.register('xi3.lang-levels', () => {
    let s = '';
    const cols = [
      { x: 8, c: 3, t: 'Low Level', d: 'Uses 1s and 0s\nto create\ninstructions\n(binary)', ex: 'Binary Language' },
      { x: 155, c: 4, t: 'Mid-Level', d: 'Uses mnemonics\nto create\ninstructions\n(readable codes)', ex: 'Assembly Language' },
      { x: 302, c: 5, t: 'High Level', d: 'Similar to human\nlanguage; easy\nto read and\nwrite', ex: 'C++, Java, Python' },
    ];
    cols.forEach((c) => {
      s += K.rect(c.x, 8, 130, 160, { c: c.c });
      s += T(c.x + 65, 30, c.t, { size: 14, w: 'b' });
      s += T(c.x + 65, 52, c.d, { size: 12, lh: 15 });
      s += K.line(c.x + 10, 118, c.x + 120, 118, { cls: 's-mut', dash: '3 3', w: 1 });
      s += mut(c.x + 65, 135, 'Example');
      s += T(c.x + 65, 154, c.ex, { size: 12, w: 'b' });
    });
    s += arr(14, 196, 426, 196, { arrow: 'both', cls: 's-mut' });
    s += T(14, 218, 'Closer to hardware', { size: 12, anchor: 'start', cls: 't-mut' });
    s += T(426, 218, 'Closer to humans', { size: 12, anchor: 'end', cls: 't-mut' });
    return K.svg(440, 230, s, { title: 'Programming language types: low level, mid level and high level' });
  });

  D.register('xi3.translate', () => {
    let s = '';
    s += T(220, 18, 'Compiler: translates the WHOLE program first', { size: 13, w: 'b' });
    const lab = ['Source code\n(.py file)', 'Compiler', 'Machine code\nfile', 'CPU runs\nit'];
    lab.forEach((l, i) => {
      const x = 8 + i * 113;
      s += proc(x + 44, 56, 88, 44, l, [1, 4, 6, 5][i]);
      if (i < 3) s += arr(x + 88, 56, x + 113, 56);
    });
    s += mut(220, 98, 'translate once, then run the result many times', { size: 12 });
    s += K.line(10, 114, 430, 114, { cls: 's-mut', dash: '3 3', w: 1 });
    s += T(220, 136, 'Interpreter: translates and runs LINE BY LINE', { size: 13, w: 'b' });
    const lab2 = ['Source code\n(.py file)', 'Interpreter\n(line by line)', 'Output\nappears'];
    lab2.forEach((l, i) => {
      const x = 8 + i * 157;
      s += proc(x + 55, 178, 110, 48, l, [1, 4, 0][i]);
      if (i < 2) s += arr(x + 110, 178, x + 157, 178);
    });
    s += K.rect(70, 216, 300, 30, { c: 5, r: 15 });
    s += T(220, 232, 'Python uses an Interpreter', { size: 13, w: 'b', vmid: true });
    return K.svg(440, 254, s, { title: 'Compiler translates the whole program; interpreter runs it line by line' });
  });

  D.register('xi3.py-uses', () => {
    let s = '';
    const items = [
      ['Software\nDevelopment', 0, 6, 40],
      ['Data Science\n& Analysis', 1, 6, 140],
      ['AI & Machine\nLearning', 2, 6, 240],
      ['Web\nDevelopment', 3, 304, 40],
      ['Automation\n& Scripting', 4, 304, 140],
      ['Cybersecurity\n& Networking', 5, 304, 240],
    ];
    items.forEach(([l, c, x, cy]) => {
      s += K.line(x < 200 ? x + 130 : x, cy, 220, 140, { cls: 's-mut', w: 1.5 });
    });
    s += K.circle(220, 140, 44, { c: 4 }) + T(220, 140, 'Python', { size: 17, w: 'b', vmid: true });
    items.forEach(([l, c, x, cy]) => {
      s += K.box(x, cy - 28, 130, 56, l, { c, size: 13, r: 10 });
    });
    return K.svg(440, 280, s, { title: 'Career areas where Python is used' });
  });

  D.register('xi3.ide-features', () => {
    let s = '';
    s += T(220, 18, 'IDE = a complete workspace for programming', { size: 13, w: 'b' });
    const rows = [
      ['Code Editor', 'write and edit code'],
      ['Syntax Highlighting', 'colours make code easy to read'],
      ['Auto Completion', 'suggests code while typing'],
      ['Run / Execute Tool', 'executes the program'],
      ['Debugger', 'finds and fixes errors'],
    ];
    rows.forEach(([a, b], i) => {
      const y = 34 + i * 42;
      s += K.box(8, y, 160, 34, a, { c: i, size: 13, r: 8, bold: true });
      s += arr(170, y + 17, 196, y + 17);
      s += T(204, y + 17, b, { size: 13, anchor: 'start', vmid: true });
    });
    return K.svg(440, 250, s, { title: 'Key features of an IDE' });
  });

  D.register('xi3.vscode-layout', () => {
    let s = '';
    const badge = (x, y, n) => K.circle(x, y, 9, { c: 3 }) + T(x, y, String(n), { size: 12, vmid: true, w: 'b' });
    s += K.rect(8, 8, 300, 262, { c: 6, r: 6 });
    s += K.rect(8, 8, 300, 24, { c: 1, r: 6 });
    s += mono(T(16, 24, 'File Edit View Run', { size: 11, anchor: 'start' }));
    s += K.rect(196, 12, 104, 16, { c: 6, r: 8 }) + T(248, 20.5, 'Search', { size: 11, vmid: true, cls: 't-mut' });
    s += K.rect(8, 32, 122, 216, { c: 0, r: 0 });
    ['Explorer', 'Search', 'Source Control', 'Run & Debug', 'Extensions', 'Manage'].forEach((l, i) => {
      const y = 44 + i * 26;
      s += K.rect(14, y, 16, 16, { c: 2, r: 3 }) + T(36, y + 8.5, l, { size: 11, anchor: 'start', vmid: true });
    });
    s += K.rect(130, 32, 178, 150, { c: 6, r: 0 });
    s += K.rect(134, 36, 80, 18, { c: 4, r: 3 }) + T(174, 45.5, 'program.py', { size: 11, vmid: true });
    s += mono(
      T(138, 74, '1  # Hello', { size: 12, anchor: 'start' }) +
        T(138, 92, '2  print("Hi")', { size: 12, anchor: 'start' }) +
        T(138, 110, '3  print(100)', { size: 12, anchor: 'start' })
    );
    s += K.rect(130, 182, 178, 66, { c: 5, r: 0 });
    s += mut(138, 196, 'TERMINAL', { anchor: 'start' });
    s += mono(T(138, 214, 'Hi', { size: 12, anchor: 'start' }) + T(138, 231, '100', { size: 12, anchor: 'start' }));
    s += K.rect(8, 248, 300, 22, { c: 1, r: 6 }) + T(16, 259.5, 'Ln 3, Col 14    Python', { size: 11, anchor: 'start', vmid: true });
    s += badge(162, 20, 1) + badge(184, 20, 2) + badge(118, 232, 3) + badge(292, 48, 4) + badge(292, 204, 5) + badge(292, 259, 6);
    const leg = ['Top Menu Bar', 'Search Bar', 'Side Bar', 'Code Editor', 'Terminal', 'Status Bar'];
    leg.forEach((l, i) => {
      const y = 36 + i * 38;
      s += badge(332, y, i + 1) + T(348, y, l, { size: 13, anchor: 'start', vmid: true });
    });
    return K.svg(440, 278, s, { title: 'VS Code window layout: menu bar, search bar, side bar, editor, terminal, status bar' });
  });

  D.register('xi3.program-anatomy', () => {
    let s = '';
    s += K.rect(30, 12, 240, 118, { c: 6, r: 8 });
    s += arr(14, 20, 14, 124, { cls: 's-acc' });
    const cw = 7.8;
    s += K.rect(40, 94, 4 * cw, 22, { c: 4, r: 3 });
    s += mono(
      T(40, 36, '# My first program', { size: 13, anchor: 'start', cls: 't-mut' }) +
        T(40, 62, 'print("Hello, World!")', { size: 13, anchor: 'start' }) +
        T(40, 88, 'if 5 > 3:', { size: 13, anchor: 'start' }) +
        T(40 + 4 * cw, 110, 'print("Five is bigger")', { size: 13, anchor: 'start' })
    );
    s += T(284, 36, 'Comment: ignored\nby Python', { size: 12, anchor: 'start', lh: 14, vmid: true });
    s += T(284, 62, 'Statement: shows output', { size: 12, anchor: 'start', vmid: true });
    s += T(284, 84, 'Colon (:) starts a block', { size: 12, anchor: 'start', vmid: true });
    s += T(284, 108, 'Indent: 4 spaces', { size: 12, anchor: 'start', vmid: true, w: 'b' });
    s += mut(14, 148, 'runs top to bottom', { size: 12, anchor: 'start' });
    s += K.rect(30, 158, 240, 52, { c: 0, r: 8 });
    s += mono(T(42, 176, 'Hello, World!', { size: 13, anchor: 'start' }) + T(42, 198, 'Five is bigger', { size: 13, anchor: 'start' }));
    s += mut(284, 190, 'Output in terminal', { size: 12, anchor: 'start' });
    return K.svg(440, 220, s, { title: 'Anatomy of a simple Python program' });
  });

  D.register('xi3.var-boxes', () => {
    let s = '';
    s += K.rect(4, 8, 432, 152, { c: 6, r: 12, dash: '5 4' });
    s += mut(220, 26, 'Computer memory (RAM): each variable is a named box', { size: 12 });
    const v = [
      ['name', '"Ali"', 'str', 1],
      ['age', '16', 'int', 0],
      ['height', '5.7', 'float', 4],
      ['is_student', 'True', 'bool', 2],
    ];
    v.forEach(([n, val, t, c], i) => {
      const cx = 60 + i * 107;
      s += mono(T(cx, 54, n, { size: 13, w: 'b' }));
      s += K.rect(cx - 44, 64, 88, 44, { c, r: 6 });
      s += mono(T(cx, 86, val, { size: 17, vmid: true }));
      s += K.rect(cx - 26, 120, 52, 22, { c: 6, r: 11 }) + mono(T(cx, 131, t, { size: 12, vmid: true }));
    });
    return K.svg(440, 170, s, { title: 'Variables as named boxes in memory with their data types' });
  });

  D.register('xi3.var-change', () => {
    let s = '';
    s += mono(T(90, 18, 'x = 10', { size: 15, w: 'b' }) + T(350, 18, 'x = "ten"', { size: 15, w: 'b' }));
    s += mono(T(90, 50, 'x', { size: 14, cls: 't-mut' }) + T(350, 50, 'x', { size: 14, cls: 't-mut' }));
    s += K.rect(45, 58, 90, 44, { c: 0, r: 6 }) + mono(T(90, 80, '10', { size: 18, vmid: true }));
    s += K.rect(305, 58, 90, 44, { c: 1, r: 6 }) + mono(T(350, 80, '"ten"', { size: 18, vmid: true }));
    s += K.rect(64, 112, 52, 22, { c: 6, r: 11 }) + mono(T(90, 123, 'int', { size: 12, vmid: true }));
    s += K.rect(324, 112, 52, 22, { c: 6, r: 11 }) + mono(T(350, 123, 'str', { size: 12, vmid: true }));
    s += arr(150, 80, 290, 80, { cls: 's-acc', w: 2.5 });
    s += mut(220, 66, 'same name x', { size: 12 });
    s += mut(220, 100, 'new value,\nnew type', { size: 12, lh: 14 });
    return K.svg(440, 144, s, { title: 'A Python variable can change its value and its type' });
  });

  D.register('xi3.dtypes-tree', () => {
    let s = '';
    const groups = [
      { n: 'Numbers', c: 0, leaves: ['Int: 20', 'Float: 35.75', 'Complex: 1+3j'], y: 8 },
      { n: 'Bool', c: 2, leaves: ['True, False'], y: 112 },
      { n: 'Set', c: 4, leaves: ['{2, 4, 6}'], y: 152 },
      { n: 'Dict', c: 7, leaves: ['{1: "a", 2: "b"}'], y: 192 },
      { n: 'Sequence', c: 1, leaves: ['String: "Jessa"', 'List: [2, "a", 5.7]', 'Tuple: (3, 4.5, "b")'], y: 232 },
    ];
    const gc = groups.map((g) => g.y + ((g.leaves.length - 1) * 32 + 26) / 2);
    const cy0 = 165;
    s += K.line(104, gc[0], 104, gc[gc.length - 1], {});
    s += K.line(90, cy0, 104, cy0, {});
    groups.forEach((g, i) => {
      s += K.line(104, gc[i], 118, gc[i], {});
      const lc = g.leaves.map((_, j) => g.y + j * 32 + 13);
      if (g.leaves.length > 1) s += K.line(233, lc[0], 233, lc[lc.length - 1], {});
      s += K.line(218, gc[i], 248, g.leaves.length > 1 ? gc[i] : lc[0], {});
      s += K.box(118, gc[i] - 15, 100, 30, g.n, { c: g.c, size: 13, bold: true, r: 8 });
      g.leaves.forEach((l, j) => {
        if (g.leaves.length > 1) s += K.line(233, lc[j], 248, lc[j], {});
        s += K.rect(248, lc[j] - 13, 186, 26, { c: g.c, r: 6 });
        s += mono(T(256, lc[j], l, { size: 12, anchor: 'start', vmid: true }));
      });
    });
    s += K.box(6, cy0 - 32, 84, 64, 'Python\nData Types', { c: 5, size: 13, bold: true, r: 12 });
    return K.svg(440, 332, s, { title: 'Python data types: numbers, bool, set, dict and sequences' });
  });

  D.register('xi3.io-flow', () => {
    let s = '';
    const b = [
      ['User\ntypes data', 6], ['input()', 1], ['Variable\n(memory)', 5], ['print()', 4], ['Screen', 0],
    ];
    b.forEach(([l, c], i) => {
      const x = 4 + i * 90;
      s += K.box(x, 20, 74, 50, l, { c, size: 13, r: 8 });
      if (i < 4) s += arr(x + 74, 45, x + 90, 45);
    });
    s += K.line(4, 88, 168, 88, { cls: 's-acc', w: 4 }) + T(86, 108, 'INPUT', { size: 13, w: 'b', cls: 't-acc' });
    s += K.line(184, 88, 258, 88, { cls: 's-grn', w: 4 }) + T(221, 108, 'STORE', { size: 13, w: 'b', cls: 't-grn' });
    s += K.line(274, 88, 438, 88, { cls: 's-red', w: 4 }) + T(356, 108, 'OUTPUT', { size: 13, w: 'b', cls: 't-red' });
    s += mut(220, 138, 'input() always gives back a string', { size: 12 });
    return K.svg(440, 150, s, { title: 'Input and output flow in Python' });
  });

  D.register('xi3.input-str', () => {
    let s = '';
    s += K.box(6, 14, 84, 52, 'User types\n16', { c: 6, size: 13, r: 8 });
    s += arr(90, 40, 114, 40);
    s += K.rect(114, 14, 122, 52, { c: 3, r: 8 }) + mono(T(175, 32, 'input("Age: ")', { size: 12 })) + T(175, 52, 'returns "16" (str)', { size: 12, vmid: true });
    s += arr(236, 40, 262, 40);
    s += K.box(262, 14, 72, 52, 'int()\nconverts', { c: 4, size: 13, r: 8 });
    s += arr(334, 40, 358, 40);
    s += K.box(358, 14, 76, 52, 'age = 16\n(int)', { c: 5, size: 13, r: 8 });
    s += mono(T(20, 100, '"16" + 1', { size: 14, anchor: 'start' }) + T(150, 100, '->  TypeError', { size: 14, anchor: 'start', cls: 't-red' }));
    s += mono(T(20, 128, 'int("16") + 1', { size: 14, anchor: 'start' }) + T(190, 128, '->  17', { size: 14, anchor: 'start', cls: 't-grn' }));
    return K.svg(440, 146, s, { title: 'input() returns a string; int() converts it to a number' });
  });

  D.register('xi3.f-string', () => {
    let s = '';
    const cw = 13 * 0.6;
    const str = 'f"My name is {name} and I am {age} years old."';
    const x0 = 12;
    const px = (sub) => x0 + str.indexOf(sub) * cw;
    s += mono(T(x0, 30, str, { size: 13, anchor: 'start' }));
    const pn = px('{name}') + 3 * cw;
    const pa = px('{age}') + 2.5 * cw;
    s += K.line(px('{name}'), 36, px('{name}') + 6 * cw, 36, { cls: 's-acc', w: 2.5 });
    s += K.line(px('{age}'), 36, px('{age}') + 5 * cw, 36, { cls: 's-grn', w: 2.5 });
    s += arr(pn, 40, 120, 76, { cls: 's-acc' });
    s += arr(pa, 40, 280, 76, { cls: 's-grn' });
    s += K.rect(60, 78, 120, 30, { c: 4, r: 6 }) + mono(T(120, 93, 'name = "Ali"', { size: 13, vmid: true }));
    s += K.rect(220, 78, 120, 30, { c: 5, r: 6 }) + mono(T(280, 93, 'age = 16', { size: 13, vmid: true }));
    s += K.rect(12, 128, 416, 30, { c: 0, r: 8 });
    s += mono(T(220, 143, 'My name is Ali and I am 16 years old.', { size: 13, vmid: true }));
    s += arr(220, 112, 220, 126, { cls: 's-mut' });
    return K.svg(440, 166, s, { title: 'An f-string fills variable values into the text' });
  });

  D.register('xi3.operand-operator', () => {
    let s = '';
    s += K.rect(70, 14, 76, 52, { c: 1, r: 8 }) + K.rect(166, 14, 64, 52, { c: 4, r: 8 }) + K.rect(250, 14, 76, 52, { c: 1, r: 8 });
    s += mono(T(108, 40, '10', { size: 28, vmid: true }) + T(198, 40, '+', { size: 28, vmid: true }) + T(288, 40, '20', { size: 28, vmid: true }) + T(372, 40, '= 30', { size: 22, vmid: true, cls: 't-mut' }));
    s += T(108, 86, 'Operand', { size: 13, w: 'b' }) + T(198, 86, 'Operator', { size: 13, w: 'b' }) + T(288, 86, 'Operand', { size: 13, w: 'b' });
    s += K.line(108, 68, 108, 74, { cls: 's-mut' }) + K.line(198, 68, 198, 74, { cls: 's-mut' }) + K.line(288, 68, 288, 74, { cls: 's-mut' });
    return K.svg(440, 100, s, { title: 'Operands and operator in 10 + 20' });
  });

  D.register('xi3.op-families', () => {
    let s = '';
    const f = [
      ['Arithmetic', '+  -  *  /  //  %  **', 0],
      ['Assignment', '=  +=  -=  *=  /=', 1],
      ['Relational', '==  !=  >  <  >=  <=', 2],
      ['Logical', 'and   or   not', 3],
      ['Membership', 'in   not in', 4],
      ['Bitwise', '&   |   ^   ~   <<   >>', 5],
    ];
    f.forEach(([n, o, c], i) => {
      const x = 6 + (i % 2) * 216;
      const y = 6 + Math.floor(i / 2) * 70;
      s += K.rect(x, y, 208, 62, { c, r: 10 });
      s += T(x + 104, y + 20, n, { size: 14, w: 'b' });
      s += mono(T(x + 104, y + 44, o, { size: 13 }));
    });
    return K.svg(440, 218, s, { title: 'Six families of Python operators' });
  });

  D.register('xi3.bits', (args) => {
    const op = args.op || 'and';
    const a = args.a == null ? 10 : args.a;
    const b = args.b == null ? 6 : args.b;
    const fn = { and: (x, y) => x & y, or: (x, y) => x | y, xor: (x, y) => x ^ y }[op];
    const sym = { and: '&', or: '|', xor: '^' }[op];
    const r = fn(a, b);
    const bits = (v) => v.toString(2).padStart(4, '0');
    let s = '';
    const x0 = 128;
    const row = (y, v, c) => bits(v).split('').map((ch, i) => bitCell(x0 + i * 48, y, 44, 34, ch, c)).join('');
    s += mono(T(10, 40, 'a = ' + a, { size: 15, anchor: 'start', vmid: true, w: 'b' }));
    s += mono(T(10, 86, 'b = ' + b, { size: 15, anchor: 'start', vmid: true, w: 'b' }));
    s += row(22, a, 1) + row(68, b, 2);
    s += mono(T(96, 64, sym, { size: 24, vmid: true, cls: 't-acc' }));
    s += K.line(100, 110, 326, 110, { w: 2 });
    s += mono(T(10, 144, 'a ' + sym + ' b', { size: 15, anchor: 'start', vmid: true, w: 'b' }));
    s += row(127, r, 5);
    [0, 1, 2, 3].forEach((i) => {
      s += K.line(x0 + i * 48 + 22, 56, x0 + i * 48 + 22, 66, { cls: 's-mut', w: 1, dash: '2 2' });
    });
    s += mono(T(340, 40, '= ' + a, { size: 14, anchor: 'start', vmid: true }) + T(340, 86, '= ' + b, { size: 14, anchor: 'start', vmid: true }) + T(340, 144, '= ' + r, { size: 15, anchor: 'start', vmid: true, w: 'b', cls: 't-grn' }));
    s += mono(T(220, 186, 'bin(a ' + sym + ' b)  ->  0b' + r.toString(2), { size: 14 }));
    return K.svg(440, 202, s, { title: 'Bitwise ' + op.toUpperCase() + ' of ' + a + ' and ' + b + ' bit by bit' });
  });

  D.register('xi3.bit-not', () => {
    let s = '';
    const x0 = 80;
    const row = (y, str, c) => str.split('').map((ch, i) => bitCell(x0 + i * 35, y, 32, 32, ch, c, 14)).join('');
    s += mono(T(220, 14, 'a = 10   (8-bit form)', { size: 13, w: 'b' }));
    s += row(24, '00001010', 1);
    s += arr(220, 60, 220, 96, { cls: 's-acc', w: 2.5 });
    s += mono(T(232, 78, '~  flip every bit', { size: 13, anchor: 'start', cls: 't-acc' }));
    s += row(102, '11110101', 4);
    s += mono(T(220, 160, '~a = -(a + 1) = -11', { size: 17, w: 'b' }));
    s += mut(220, 182, "negative numbers are stored in two's complement", { size: 12 });
    return K.svg(440, 192, s, { title: 'Bitwise NOT of 10 gives minus 11' });
  });

  D.register('xi3.shift', (args) => {
    const left = (args.dir || 'left') === 'left';
    const start = left ? 5 : 20;
    let s = '';
    const x0 = 78;
    s += T(220, 14, left ? 'Left shift: bits move left, zeros fill the right' : 'Right shift: bits move right, zeros fill the left', { size: 13, w: 'b' });
    for (let n = 0; n <= 3; n++) {
      const v = left ? (start << n) & 255 : start >> n;
      const bits = v.toString(2).padStart(8, '0').split('');
      const y = 30 + n * 42;
      s += mono(T(8, y + 15, n === 0 ? 'a' : left ? 'a << ' + n : 'a >> ' + n, { size: 14, anchor: 'start', vmid: true, w: 'b' }));
      bits.forEach((ch, i) => {
        const added = n > 0 && (left ? i >= 8 - n : i < n);
        s += added
          ? K.rect(x0 + i * 33, y, 30, 30, { c: 4, r: 4 }) + T(x0 + i * 33 + 15, y + 15, '0', { size: 14, vmid: true, w: 'b' })
          : bitCell(x0 + i * 33, y, 30, 30, ch, 1, 14);
      });
      s += mono(T(x0 + 8 * 33 + 6, y + 15, '= ' + v, { size: 15, anchor: 'start', vmid: true, w: 'b' }));
    }
    s += mut(220, 208, left ? 'each left shift multiplies by 2' : 'each right shift divides by 2 (whole number)', { size: 12 });
    s += K.rect(78, 218, 14, 12, { c: 4, r: 2 }) + mut(98, 224, 'zeros added', { size: 11, anchor: 'start', vmid: true });
    return K.svg(440, 236, s, { title: 'Bitwise ' + (left ? 'left' : 'right') + ' shift' });
  });

  D.register('xi3.control3', () => {
    let s = '';
    const titles = [['Sequence', 'one after another', 62], ['Selection', 'choose a path', 200], ['Repetition', 'repeat a block', 365]];
    titles.forEach(([t, d, cx]) => {
      s += T(cx, 18, t, { size: 14, w: 'b' }) + mut(cx, 34, d, { size: 12 });
    });
    // sequence
    [1, 2, 3].forEach((n, i) => {
      const cy = 70 + i * 52;
      s += proc(62, cy, 90, 32, 'Step ' + n, 1, 13);
      if (i < 2) s += arr(62, cy + 16, 62, cy + 36);
    });
    // selection
    const sx = 200;
    s += dec(sx, 80, 90, 50, 'condition?', 4);
    s += pl([[sx - 45, 80], [sx - 52, 80], [sx - 52, 150]]);
    s += pl([[sx + 45, 80], [sx + 52, 80], [sx + 52, 150]]);
    s += mut(sx - 49, 72, 'Yes', { anchor: 'end' }) + mut(sx + 49, 72, 'No', { anchor: 'start' });
    s += proc(sx - 52, 168, 62, 30, 'if block', 5, 12) + proc(sx + 52, 168, 62, 30, 'else block', 3, 12);
    // repetition
    const rx = 365;
    s += dec(rx, 80, 90, 50, 'condition?', 4);
    s += arr(rx, 105, rx, 135);
    s += mut(rx + 6, 122, 'Yes', { anchor: 'start' });
    s += proc(rx, 152, 62, 30, 'body', 5, 13);
    s += pl([[rx - 31, 152], [rx - 62, 152], [rx - 62, 80], [rx - 45, 80]]);
    s += pl([[rx + 45, 80], [rx + 62, 80], [rx + 62, 206], [rx + 36, 206]]);
    s += mut(rx + 48, 72, 'No', { anchor: 'start' });
    s += proc(rx, 206, 72, 28, 'exit', 6, 12);
    return K.svg(440, 232, s, { title: 'Sequence, selection and repetition control structures' });
  });

  D.register('xi3.flow-if', (args) => {
    const ifelse = args.mode === 'ifelse';
    let s = '';
    const cx = 140;
    s += oval(cx, 16, 70, 24, 'Start', 6);
    s += arr(cx, 28, cx, 44);
    s += io(cx, 60, 190, 32, 'age = int(input())', 0);
    s += arr(cx, 76, cx, 96);
    s += dec(cx, 124, 170, 56, 'age >= 18 ?', 4);
    s += arr(cx, 152, cx, 190);
    s += mut(cx + 6, 172, 'True', { anchor: 'start' });
    s += mono(proc(cx, 206, 180, 30, 'print("Adult")', 5, 12));
    s += arr(cx, 221, cx, 250);
    const joinY = 266;
    s += mono(proc(cx, joinY, 180, 30, 'print("Check complete.")', 1, 12));
    s += arr(cx, joinY + 15, cx, joinY + 38);
    s += oval(cx, joinY + 50, 70, 24, 'End', 6);
    s += mut(cx + 100, 117, 'False', { anchor: 'start' });
    if (ifelse) {
      s += pl([[cx + 85, 124], [345, 124], [345, 191]]);
      s += mono(proc(345, 206, 150, 30, 'print("Minor")', 3, 12));
      s += pl([[345, 221], [345, joinY], [cx + 90, joinY]]);
    } else {
      s += pl([[cx + 85, 124], [345, 124], [345, joinY], [cx + 90, joinY]]);
      s += mut(345, 190, 'skipped', { size: 11 });
    }
    return K.svg(440, 330, s, { title: ifelse ? 'Flowchart of an if-else statement' : 'Flowchart of an if statement' });
  });

  D.register('xi3.flow-elif', () => {
    let s = '';
    const rows = [
      ['age <= 0 ?', 'Invalid age!', 3],
      ['age <= 12 ?', 'Child', 0],
      ['age <= 17 ?', 'Teenager', 1],
      ['age <= 35 ?', 'Young Adult', 5],
      ['age <= 60 ?', 'Middle-Aged Adult', 4],
    ];
    const cx = 100;
    rows.forEach(([c, r, col], i) => {
      const cy = 34 + i * 62;
      s += dec(cx, cy, 130, 46, c, 4);
      s += arr(cx + 65, cy, 218, cy);
      s += mut(cx + 70, cy - 8, 'True', { anchor: 'start' });
      s += K.box(220, cy - 16, 180, 32, r, { c: col, size: 13, r: 8 });
      s += arr(cx, cy + 23, cx, cy + 62 - 23);
      s += mut(cx + 6, cy + 36, 'False', { anchor: 'start' });
    });
    const ey = 34 + 5 * 62;
    s += K.box(cx - 70, ey - 16, 140, 32, 'else: Senior Citizen', { c: 7, size: 12, r: 8 });
    s += mut(220, ey + 36, 'the FIRST true condition wins; the rest are skipped', { size: 12, anchor: 'start' });
    return K.svg(440, 370, s, { title: 'Flowchart of an if-elif-else ladder' });
  });

  D.register('xi3.flow-nested', () => {
    let s = '';
    const cx = 140;
    s += T(8, 76, 'outer if', { size: 11, anchor: 'start', cls: 't-mut' });
    s += oval(cx, 14, 90, 24, 'age, salary', 6);
    s += arr(cx, 26, cx, 48);
    s += dec(cx, 76, 140, 52, 'age >= 18 ?', 4);
    s += arr(cx, 102, cx, 134);
    s += mut(cx + 6, 120, 'True', { anchor: 'start' });
    s += T(8, 166, 'inner if', { size: 11, anchor: 'start', cls: 't-mut' });
    s += dec(cx, 166, 160, 52, 'salary >= 30000 ?', 4);
    s += arr(cx, 192, cx, 232);
    s += mut(cx + 6, 214, 'True', { anchor: 'start' });
    s += K.box(cx - 70, 232, 140, 32, 'Loan APPROVED', { c: 5, size: 13, r: 8, bold: true });
    s += arr(cx + 70, 76, 275, 76);
    s += mut(cx + 76, 68, 'False', { anchor: 'start' });
    s += K.box(275, 52, 160, 48, 'Age requirement\nnot met\nLoan REJECTED', { c: 3, size: 12, r: 8 });
    s += arr(cx + 80, 166, 275, 166);
    s += mut(cx + 86, 158, 'False', { anchor: 'start' });
    s += K.box(275, 142, 160, 48, 'Salary too low\nLoan REJECTED', { c: 3, size: 12, r: 8 });
    return K.svg(440, 276, s, { title: 'Flowchart of a nested if loan example' });
  });

  D.register('xi3.flow-for', () => {
    let s = '';
    const cx = 130;
    s += oval(cx, 16, 70, 24, 'Start', 6);
    s += arr(cx, 28, cx, 52);
    s += dec(cx, 80, 170, 56, 'values left?', 4);
    s += arr(cx, 108, cx, 142);
    s += mut(cx + 6, 128, 'Yes', { anchor: 'start' });
    s += mono(proc(cx, 160, 130, 32, 'i = next value', 1, 12));
    s += arr(cx, 176, cx, 202);
    s += mono(proc(cx, 220, 130, 32, 'print(i)', 5, 12));
    s += pl([[cx - 65, 220], [14, 220], [14, 80], [cx - 85, 80]]);
    s += mut(20, 150, 'repeat', { anchor: 'start' });
    s += arr(cx + 85, 80, 300, 80);
    s += mut(cx + 92, 72, 'No', { anchor: 'start' });
    s += oval(340, 80, 80, 28, 'Exit loop', 6);
    s += mut(300, 140, 'for i in range(3):', { size: 12, anchor: 'start', cls: 't-acc' });
    s += mono(T(300, 160, '    print(i)', { size: 12, anchor: 'start' }));
    s += mut(300, 188, 'prints 0, 1, 2', { size: 12, anchor: 'start' });
    return K.svg(440, 252, s, { title: 'Flowchart of a for loop' });
  });

  D.register('xi3.flow-while', () => {
    let s = '';
    const cx = 150;
    s += oval(cx, 16, 70, 24, 'Start', 6);
    s += arr(cx, 28, cx, 44);
    s += mono(proc(cx, 60, 140, 30, 'count = 1', 0, 12));
    s += arr(cx, 75, cx, 100);
    s += dec(cx, 128, 170, 56, 'count <= 5 ?', 4);
    s += arr(cx, 156, cx, 188);
    s += mut(cx + 6, 176, 'True', { anchor: 'start' });
    s += mono(proc(cx, 204, 140, 30, 'print(count)', 5, 12));
    s += arr(cx, 219, cx, 238);
    s += mono(proc(cx, 254, 140, 30, 'count += 1', 1, 12));
    s += pl([[cx - 70, 254], [30, 254], [30, 128], [cx - 85, 128]]);
    s += mut(40, 200, 'repeat', { anchor: 'start' });
    s += arr(cx + 85, 128, 300, 128);
    s += mut(cx + 92, 120, 'False', { anchor: 'start' });
    s += oval(344, 128, 80, 28, 'Exit loop', 6);
    s += mut(300, 190, 'prints 1 2 3 4 5', { size: 12, anchor: 'start' });
    return K.svg(440, 290, s, { title: 'Flowchart of a while loop counting from 1 to 5' });
  });

  D.register('xi3.range-line', () => {
    let s = '';
    const x0 = 24;
    const dx = 36;
    const rows = [
      ['range(5)', [0, 1, 2, 3, 4], 5],
      ['range(2, 8)', [2, 3, 4, 5, 6, 7], 8],
      ['range(0, 10, 2)', [0, 2, 4, 6, 8], 10],
      ['range(10, 0, -2)', [10, 8, 6, 4, 2], 0],
    ];
    rows.forEach(([l, vals, stop], i) => {
      const y = 20 + i * 52;
      s += mono(T(8, y, l, { size: 13, anchor: 'start', w: 'b' }));
      s += K.line(x0 - 8, y + 24, x0 + 10 * dx + 8, y + 24, { cls: 's-mut', w: 1.5 });
      s += K.circle(x0 + stop * dx, y + 24, 8, { c: 3, cls: 's-red' }).replace('class="shape', 'stroke-dasharray="3 2" class="shape');
      vals.forEach((v) => {
        s += K.circle(x0 + v * dx, y + 24, 8, { c: 0 });
      });
    });
    for (let i = 0; i <= 10; i++) s += mut(x0 + i * dx, 236, String(i), { size: 12 });
    s += K.circle(60, 262, 6, { c: 0 }) + mut(72, 262, 'included', { size: 12, anchor: 'start', vmid: true });
    s += K.circle(180, 262, 6, { c: 3, cls: 's-red' }).replace('class="shape', 'stroke-dasharray="3 2" class="shape') + mut(192, 262, 'stop: NOT included', { size: 12, anchor: 'start', vmid: true });
    return K.svg(440, 276, s, { title: 'Values produced by range with one, two and three arguments' });
  });

  D.register('xi3.break-continue', () => {
    let s = '';
    const x0 = 8;
    const w = 66;
    const strip = (y, title, states) => {
      let o = mono(T(x0, y, title, { size: 13, anchor: 'start', w: 'b' }));
      states.forEach((st, i) => {
        const x = x0 + i * 70;
        const col = { p: 5, s: 4, b: 3, n: 6 }[st];
        const lab = { p: 'print', s: 'skip', b: 'BREAK', n: 'never run' }[st];
        o += K.rect(x, y + 10, w, 50, { c: col, r: 8 });
        o += mono(T(x + w / 2, y + 28, 'i=' + i, { size: 13, vmid: true, w: 'b' }));
        o += T(x + w / 2, y + 47, lab, { size: 11, vmid: true, cls: st === 'n' ? 't-mut' : '' });
      });
      return o;
    };
    s += strip(18, 'break at i == 3', ['p', 'p', 'p', 'b', 'n', 'n']);
    s += strip(118, 'continue when i % 2 == 0', ['s', 'p', 's', 'p', 's', 'p']);
    s += mut(220, 214, 'break leaves the loop; continue jumps to the next round', { size: 12 });
    return K.svg(440, 226, s, { title: 'Effect of break and continue inside for i in range(6)' });
  });

  D.register('xi3.nested-grid', () => {
    let s = '';
    const x0 = 70;
    const y0 = 50;
    s += mut(x0 + 135, 14, 'inner loop: j', { size: 12, cls: 't-acc' });
    for (let j = 1; j <= 3; j++) s += mono(T(x0 + (j - 1) * 90 + 45, 38, 'j = ' + j, { size: 13, w: 'b' }));
    for (let i = 1; i <= 3; i++) {
      s += mono(T(x0 - 10, y0 + (i - 1) * 40 + 20, 'i = ' + i, { size: 13, anchor: 'end', vmid: true, w: 'b' }));
      for (let j = 1; j <= 3; j++) {
        const n = (i - 1) * 3 + j;
        s += K.rect(x0 + (j - 1) * 90 + 2, y0 + (i - 1) * 40 + 2, 86, 36, { c: [0, 1, 2][i - 1], r: 6 });
        s += T(x0 + (j - 1) * 90 + 45, y0 + (i - 1) * 40 + 20, 'run ' + n, { size: 13, vmid: true });
      }
    }
    s += mut(8, 26, 'outer', { size: 12, anchor: 'start', cls: 't-acc' }) + mut(8, 40, 'loop: i', { size: 12, anchor: 'start', cls: 't-acc' });
    s += mut(220, 192, 'for each i, the inner loop runs completely', { size: 12 });
    return K.svg(440, 204, s, { title: 'Nested loop: three outer rounds with three inner rounds each' });
  });

  D.register('xi3.flow-evenodd', () => {
    let s = '';
    const cx = 190;
    s += oval(cx, 14, 70, 24, 'Start', 6);
    s += arr(cx, 26, cx, 48);
    s += mono(dec(cx, 74, 150, 52, 'i < 3 ?', 5));
    s += arr(cx, 100, cx, 132);
    s += mut(cx + 6, 118, 'Yes', { anchor: 'start' });
    s += mono(io(cx, 150, 200, 30, 'number = int(input())', 0));
    s += arr(cx, 165, cx, 191);
    s += mono(dec(cx, 218, 180, 52, 'number % 2 == 0 ?', 4));
    s += arr(cx - 90, 218, cx - 90, 252);
    s += arr(cx + 90, 218, cx + 90, 252);
    s += mut(cx - 94, 210, 'Yes', { anchor: 'end' }) + mut(cx + 94, 210, 'No', { anchor: 'start' });
    s += mono(proc(cx - 90, 266, 84, 28, 'print Even', 5, 12) + proc(cx + 90, 266, 84, 28, 'print Odd', 3, 12));
    s += K.polyline([[cx - 90, 280], [cx - 90, 302], [cx + 90, 302], [cx + 90, 280]], {});
    s += pl([[cx + 90, 302], [420, 302], [420, 74], [cx + 75, 74]]);
    s += arr(cx - 75, 74, 82, 74);
    s += mut(cx - 80, 66, 'No', { anchor: 'end' });
    s += oval(52, 74, 60, 24, 'End', 6);
    s += K.rect(300, 100, 100, 24, { c: 5, r: 12 }) + T(350, 112, 'Repetition', { size: 12, vmid: true });
    s += K.rect(300, 138, 100, 24, { c: 0, r: 12 }) + T(350, 150, 'Sequence', { size: 12, vmid: true });
    s += K.rect(300, 176, 100, 24, { c: 4, r: 12 }) + T(350, 188, 'Selection', { size: 12, vmid: true });
    return K.svg(440, 316, s, { title: 'Flowchart combining repetition, sequence and selection' });
  });

  D.register('xi3.import-box', () => {
    let s = '';
    s += K.rect(6, 30, 130, 100, { c: 1, r: 10 });
    s += T(71, 20, 'Your program', { size: 13, w: 'b' });
    s += mono(T(71, 70, 'import math', { size: 14, vmid: true }));
    s += mono(T(71, 100, 'math.sqrt(25)', { size: 12, vmid: true, cls: 't-mut' }));
    s += arr(136, 70, 176, 70, { w: 2.5, cls: 's-acc' });
    s += K.rect(176, 8, 258, 160, { c: 4, r: 12 });
    s += T(305, 28, 'math library (toolbox)', { size: 13, w: 'b' });
    const f = ['sqrt()', 'pow()', 'ceil()', 'floor()', 'factorial()', 'pi'];
    f.forEach((l, i) => {
      const x = 188 + (i % 2) * 120;
      const y = 44 + Math.floor(i / 2) * 38;
      s += K.rect(x, y, 108, 30, { c: 6, r: 6 }) + mono(T(x + 54, y + 15, l, { size: 13, vmid: true }));
    });
    return K.svg(440, 178, s, { title: 'import math gives the program a toolbox of ready-made functions' });
  });

  D.register('xi3.lib-kinds', () => {
    let s = '';
    s += K.rect(6, 8, 208, 190, { c: 5, r: 12 });
    s += T(110, 28, 'Built-in libraries', { size: 14, w: 'b' });
    s += mut(110, 46, 'come with Python', { size: 12 });
    s += mut(110, 62, 'no installation needed', { size: 12 });
    ['math', 'random', 'datetime'].forEach((l, i) => {
      s += K.rect(40, 76 + i * 38, 140, 30, { c: 6, r: 6 }) + mono(T(110, 91 + i * 38, l, { size: 14, vmid: true }));
    });
    s += K.rect(226, 8, 208, 190, { c: 4, r: 12 });
    s += T(330, 28, 'Third-party libraries', { size: 14, w: 'b' });
    s += mut(330, 46, 'installed separately', { size: 12 });
    s += mono(T(330, 66, 'pip install name', { size: 12, cls: 't-acc' }));
    ['NumPy', 'Pandas', 'Matplotlib'].forEach((l, i) => {
      s += K.rect(260, 76 + i * 38, 140, 30, { c: 6, r: 6 }) + T(330, 91 + i * 38, l, { size: 14, vmid: true, w: 'b' });
    });
    return K.svg(440, 206, s, { title: 'Built-in versus third-party Python libraries' });
  });

  D.register('xi3.error-types', () => {
    let s = '';
    const rows = [
      ['Syntax Error', 3, 'print("Hello World"', 'Python rules broken: program does not start'],
      ['Runtime Error', 4, 'x = 10 / 0', 'crashes while the program is running'],
      ['Logical Error', 2, 'i -= 1   (should be +=)', 'runs fine but gives wrong output'],
    ];
    rows.forEach(([n, c, code, eff], i) => {
      const y = 8 + i * 72;
      s += K.box(6, y, 118, 62, n, { c, size: 13, bold: true, r: 10 });
      s += K.rect(132, y, 302, 62, { c: 6, r: 10 });
      s += mono(T(144, y + 22, code, { size: 13, anchor: 'start', vmid: true }));
      s += T(144, y + 46, eff, { size: 12, anchor: 'start', vmid: true, cls: 't-mut' });
    });
    return K.svg(440, 228, s, { title: 'Three types of errors in Python' });
  });

  D.register('xi3.traceback', () => {
    let s = '';
    s += K.rect(6, 6, 428, 108, { c: 6, r: 8 });
    s += mono(
      T(34, 26, 'Traceback (most recent call last):', { size: 11, anchor: 'start', cls: 't-mut' }) +
        T(34, 48, 'File "debug program.py", line 1, in <module>', { size: 11, anchor: 'start' }) +
        T(34, 70, '  x = int("abc")', { size: 11, anchor: 'start' }) +
        T(34, 92, 'ValueError: invalid literal for int()', { size: 11, anchor: 'start', cls: 't-red' })
    );
    const badge = (y, n, c) => K.circle(20, y, 9, { c }) + T(20, y, String(n), { size: 12, vmid: true, w: 'b' });
    s += badge(48, 1, 0) + badge(70, 2, 4) + badge(92, 3, 3);
    s += badge(142, 1, 0) + T(38, 142, 'Where: file name and line number', { size: 13, anchor: 'start', vmid: true });
    s += badge(172, 2, 4) + T(38, 172, 'Which line of code caused the problem', { size: 13, anchor: 'start', vmid: true });
    s += badge(202, 3, 3) + T(38, 202, 'What type of error, and why', { size: 13, anchor: 'start', vmid: true });
    return K.svg(440, 222, s, { title: 'Parts of a Python traceback error message' });
  });
})();
