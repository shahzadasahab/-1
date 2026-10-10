/* XII Ch6 (Entrepreneurship in the Digital Age) diagrams */
(function () {
  const D = Diagrams;
  const T = K.text;

  const arrowPath = (d, o) => K.path(d, Object.assign({ arrow: true, cls: 's-mut', w: 2 }, o || {}));

  /* wobbly hand-drawn line for sketch-style screens */
  const wavy = (x, y, w, o) => {
    let d = 'M' + x + ' ' + y;
    const seg = 10;
    for (let i = 0; i < w / seg; i++) d += ' q' + seg / 4 + ' ' + (i % 2 ? 2 : -2) + ' ' + seg / 2 + ' 0 t' + seg / 2 + ' 0';
    return K.path(d, Object.assign({ cls: 's-mut', w: 1.6 }, o || {}));
  };

  /* fidelity levels: 0 sketch, 1 wireframe, 2 polished mock of a canteen menu screen */
  const menuScreen = (x, y, w, h, lvl) => {
    let s = '';
    const rows = [
      ['Samosa', 'Rs 50'],
      ['Chai', 'Rs 40'],
      ['Roll', 'Rs 90'],
    ];
    if (lvl === 0) {
      s += K.rect(x, y, w, h, { r: 6, s: 's-mut', dash: '5 3' });
      s += T(x + w / 2, y + 24, 'Menu', { size: 13, w: 'b', cls: 't-mut' });
      s += wavy(x + 30, y + 31, w - 60);
      rows.forEach((r, i) => {
        const yy = y + 52 + i * 34;
        s += K.rect(x + 10, yy, 16, 16, { r: 2, s: 's-mut', dash: '3 2' });
        s += wavy(x + 34, yy + 10, w - 50);
      });
      s += K.rect(x + 18, y + h - 38, w - 36, 26, { r: 4, s: 's-mut', dash: '5 3' });
      s += T(x + w / 2, y + h - 25, 'Order', { size: 12, vmid: true, cls: 't-mut' });
    } else if (lvl === 1) {
      s += K.rect(x, y, w, h, { r: 8, c: 6 });
      s += K.rect(x + 8, y + 8, w - 16, 26, { r: 3, c: 6 });
      s += T(x + w / 2, y + 21, 'Header', { size: 12, vmid: true, cls: 't-mut' });
      rows.forEach((r, i) => {
        const yy = y + 44 + i * 34;
        s += K.rect(x + 8, yy, 26, 26, { r: 2, c: 6 });
        s += K.line(x + 8, yy, x + 34, yy + 26, { cls: 's-mut', w: 1 });
        s += K.line(x + 34, yy, x + 8, yy + 26, { cls: 's-mut', w: 1 });
        s += K.rect(x + 40, yy + 3, w - 52, 20, { r: 2, c: 6 });
        s += T(x + 40 + (w - 52) / 2, yy + 13, 'Item  |  Price', { size: 11, vmid: true, cls: 't-mut' });
      });
      s += K.rect(x + 12, y + h - 38, w - 24, 28, { r: 3, c: 6 });
      s += T(x + w / 2, y + h - 24, 'Button', { size: 12, vmid: true, cls: 't-mut' });
    } else {
      s += K.rect(x, y, w, h, { r: 14, c: 6 });
      s += K.rect(x + 4, y + 4, w - 8, 30, { r: 10, cls: 'f-brand' });
      s += T(x + w / 2, y + 19, 'Canteen Menu', { size: 12, w: 'b', vmid: true, cls: 't-wht' });
      rows.forEach((r, i) => {
        const yy = y + 42 + i * 32;
        s += K.rect(x + 6, yy, w - 12, 28, { r: 6, c: 7 });
        s += K.circle(x + 20, yy + 14, 8, { c: 4 });
        s += T(x + 33, yy + 14, r[0], { size: 11, anchor: 'start', vmid: true, w: 'b' });
        s += T(x + w - 12, yy + 14, r[1], { size: 11, anchor: 'end', vmid: true, cls: 't-mut' });
      });
      s += K.rect(x + 10, y + h - 38, w - 20, 28, { r: 14, c: 5 });
      s += T(x + w / 2, y + h - 24, 'Place order', { size: 12, w: 'b', vmid: true });
    }
    return s;
  };

  /* generic small screen used by flow diagrams: title + body drawn by callback */
  const miniScreen = (x, y, w, h, title, body) => {
    let s = K.rect(x, y, w, h, { r: 6, s: 's-mut', dash: '5 3' });
    s += T(x + w / 2, y + 20, title, { size: 12, w: 'b', cls: 't-mut' });
    s += wavy(x + 14, y + 27, w - 28);
    s += body(x, y, w, h);
    return s;
  };

  const person = (cx, cy, c) => {
    let s = K.circle(cx, cy - 12, 8, { c: c });
    s += K.path('M' + (cx - 11) + ' ' + (cy + 22) + ' Q' + cx + ' ' + (cy - 6) + ' ' + (cx + 11) + ' ' + (cy + 22) + ' Z', { c: c });
    return s;
  };

  /* ---------------------------------------------------------------- 01 */
  D.register('xii6.journey', (args) => {
    args = args || {};
    const project = args.mode === 'project';
    const steps = project
      ? [
          ['1  Problem', 'Real local problem\nand target users'],
          ['2  Idea', 'Business idea\nin one line'],
          ['3  Prototype', 'Low-fidelity\npaper prototype'],
          ['4  Test', 'Test with at least\nthree users'],
          ['5  MVP', 'Improve, then plan\na small MVP'],
          ['6  Launch', 'Riskiest assumption\nand beachhead'],
        ]
      : [
          ['1  Problem', 'What problem do\npeople face?'],
          ['2  Idea', 'What simple solution\ncan help?'],
          ['3  Prototype', 'How will it look\nor work?'],
          ['4  Test', 'Do users understand\nit? Feedback'],
          ['5  MVP', 'Will users really\nuse it?'],
          ['6  Launch', 'Who are the\nfirst users?'],
        ];
    const cs = [1, 4, 2, 0, 5, 7];
    const pos = [
      [14, 20], [164, 20], [314, 20],
      [314, 120], [164, 120], [14, 120],
    ];
    let s = '';
    steps.forEach((st, i) => {
      const [x, y] = pos[i];
      s += K.rect(x, y, 112, 76, { c: cs[i], r: 10 });
      s += T(x + 56, y + 20, st[0], { size: 14, w: 'b' });
      s += T(x + 56, y + 40, st[1], { size: 11, lh: 14 });
    });
    s += K.line(126, 58, 162, 58, { arrow: true, w: 2.4 });
    s += K.line(276, 58, 312, 58, { arrow: true, w: 2.4 });
    s += K.line(370, 96, 370, 118, { arrow: true, w: 2.4 });
    s += K.line(312, 158, 276, 158, { arrow: true, w: 2.4 });
    s += K.line(162, 158, 126, 158, { arrow: true, w: 2.4 });
    s += K.path('M220 120 Q220 108 150 104 Q86 100 74 96', { arrow: true, cls: 's-red', dash: '5 4', w: 1.8 });
    s += T(222, 214, 'If users are confused, go back and improve the idea.', { size: 12, cls: 't-red' });
    return K.svg(440, 226, s, { title: 'From problem to first customers: problem, idea, prototype, test, MVP, launch' });
  });

  D.register('xii6.entrepreneur', () => {
    let s = '';
    const items = [
      ['Notice a\nproblem', 0],
      ['Think of a\nsolution', 1],
      ['Make a product\nor service', 2],
      ['Test and\nimprove', 5],
    ];
    items.forEach((it, i) => {
      const x = 4 + i * 110;
      s += K.rect(x, 22, 94, 56, { c: it[1], r: 10 });
      s += T(x + 47, 50, it[0], { size: 11.5, vmid: true, lh: 15 });
      if (i < 3) s += K.line(x + 96, 50, x + 108, 50, { arrow: true, w: 2.2 });
    });
    s += T(220, 14, 'The entrepreneur\'s journey', { size: 13, w: 'b' });
    s += K.path('M381 80 Q381 118 220 118 Q56 118 51 82', { arrow: true, cls: 's-mut', dash: '5 4', w: 1.8 });
    s += T(222, 112, 'repeat until it becomes useful', { size: 11, cls: 't-mut' });
    s += K.rect(10, 134, 205, 62, { c: 7, r: 8 });
    s += T(112, 152, 'Entrepreneur', { size: 13, w: 'b' });
    s += T(112, 172, 'a person who finds a problem\nand tries to solve it', { size: 11, lh: 14 });
    s += K.rect(225, 134, 205, 62, { c: 4, r: 8 });
    s += T(327, 152, 'Entrepreneurship', { size: 13, w: 'b' });
    s += T(327, 172, 'the process: plan, start,\ntest and improve an idea', { size: 11, lh: 14 });
    return K.svg(440, 206, s, { title: 'Entrepreneur finds problem, thinks of solution, builds, tests and improves' });
  });

  D.register('xii6.digital-tools', () => {
    let s = '';
    const left = ['Mobile phone', 'Social media', 'Websites'];
    const right = ['Online forms', 'Digital payments', 'Maps and videos'];
    const ys = [20, 92, 164];
    left.forEach((l, i) => {
      s += K.line(125, ys[i] + 22, 178, 110 + (i - 1) * 18, { cls: 's-mut', w: 1.6 });
      s += K.box(12, ys[i], 113, 44, l, { c: [0, 1, 2][i], size: 13 });
    });
    right.forEach((l, i) => {
      s += K.line(315, ys[i] + 22, 262, 110 + (i - 1) * 18, { cls: 's-mut', w: 1.6 });
      s += K.box(315, ys[i], 113, 44, l, { c: [3, 4, 5][i], size: 13 });
    });
    s += K.ellipse(220, 110, 56, 50, { c: 7 });
    s += T(220, 110, 'Your idea\ntest, improve,\ngrow', { size: 12, vmid: true, lh: 15, w: 'b' });
    return K.svg(440, 226, s, { title: 'Digital tools an entrepreneur can use to test and grow an idea' });
  });

  /* ---------------------------------------------------------------- 02 */
  D.register('xii6.problem-to-idea', () => {
    const rows = [
      ['1  Observe', 'Notice repeated problems', 'Students forget practical\nfile submission dates'],
      ['2  Talk to people', 'Ask who faces it', 'Ask five classmates how\nthey remember deadlines'],
      ['3  Select one problem', 'Pick a small problem', 'Practical file reminder'],
      ['4  Suggest a solution', 'A simple idea', 'Reminder form or app screen'],
      ['5  Test early', 'Show it to users', 'Ask classmates if they would use it'],
    ];
    const cs = [0, 1, 2, 4, 5];
    let s = '';
    rows.forEach((r, i) => {
      const y = 8 + i * 58;
      s += K.rect(8, y, 160, 46, { c: cs[i], r: 8 });
      s += T(88, y + 18, r[0], { size: 13, w: 'b' });
      s += T(88, y + 35, r[1], { size: 10.5, cls: 't-mut' });
      s += K.line(170, y + 23, 190, y + 23, { arrow: true });
      s += K.rect(192, y, 240, 46, { r: 8, s: 's-mut', dash: '4 3' });
      s += T(312, y + 23, r[2], { size: 12, vmid: true, lh: 15 });
      if (i < 4) s += K.line(88, y + 47, 88, y + 57, { arrow: true, cls: 's-mut' });
    });
    return K.svg(440, 298, s, { title: 'Five steps from observing a problem to testing an idea early' });
  });

  D.register('xii6.broad-narrow', () => {
    let s = '';
    s += K.poly([[10, 10], [430, 10], [400, 70], [40, 70]], { c: 3 });
    s += T(220, 34, 'Improve the whole education system', { size: 13, w: 'b' });
    s += T(220, 54, 'too broad for a class project', { size: 12, cls: 't-red' });
    s += K.poly([[40, 78], [400, 78], [350, 138], [90, 138]], { c: 4 });
    s += T(220, 102, 'Help students with their studies', { size: 13, w: 'b' });
    s += T(220, 122, 'still big and unclear', { size: 12, cls: 't-mut' });
    s += K.poly([[90, 146], [350, 146], [320, 218], [120, 218]], { c: 5 });
    s += T(220, 170, 'Help Grade XII students track', { size: 13, w: 'b' });
    s += T(220, 188, 'practical file submission dates', { size: 13, w: 'b' });
    s += T(220, 208, 'small and clear: easy to test', { size: 12, cls: 't-grn' });
    return K.svg(440, 228, s, { title: 'A funnel from a very broad problem to a small clear problem' });
  });

  /* ---------------------------------------------------------------- 03 */
  D.register('xii6.fidelity', () => {
    let s = '';
    const W = 124;
    const H = 178;
    const xs = [14, 158, 302];
    const labels = [
      ['Low-fidelity', 'paper sketch'],
      ['Mid-fidelity', 'wireframe'],
      ['High-fidelity', 'polished mock'],
    ];
    xs.forEach((x, i) => {
      s += menuScreen(x, 14, W, H, i);
      s += T(x + W / 2, 214, labels[i][0], { size: 13, w: 'b' });
      s += T(x + W / 2, 231, labels[i][1], { size: 12, cls: 't-mut' });
    });
    s += K.line(142, 100, 156, 100, { arrow: true, w: 2 });
    s += K.line(286, 100, 300, 100, { arrow: true, w: 2 });
    s += K.line(14, 252, 426, 252, { arrow: true, cls: 's-brand', w: 2 });
    s += T(14, 270, 'cheap, fast, easy to change', { size: 11, anchor: 'start', cls: 't-grn' });
    s += T(426, 270, 'more detail, more time and cost', { size: 11, anchor: 'end', cls: 't-red' });
    s += T(220, 286, 'closer to the final product', { size: 11, cls: 't-mut' });
    return K.svg(440, 296, s, { title: 'Low, mid and high fidelity prototypes of the same screen side by side' });
  });

  D.register('xii6.paper-flow', () => {
    let s = '';
    const w = 108;
    const h = 150;
    const y = 20;
    const xs = [12, 166, 320];
    s += miniScreen(xs[0], y, w, h, 'Menu', (x, yy) => {
      let b = '';
      for (let i = 0; i < 4; i++) {
        b += K.rect(x + 12, yy + 42 + i * 24, 12, 12, { r: 2, s: 's-mut', dash: '3 2' });
        b += wavy(x + 30, yy + 49 + i * 24, 60);
      }
      return b;
    });
    s += miniScreen(xs[1], y, w, h, 'Your details', (x, yy) => {
      let b = '';
      b += T(x + 14, yy + 56, 'Name', { size: 11, anchor: 'start', cls: 't-mut' });
      b += K.rect(x + 12, yy + 62, w - 24, 18, { r: 3, s: 's-mut', dash: '3 2' });
      b += T(x + 14, yy + 100, 'Class', { size: 11, anchor: 'start', cls: 't-mut' });
      b += K.rect(x + 12, yy + 106, w - 24, 18, { r: 3, s: 's-mut', dash: '3 2' });
      return b;
    });
    s += miniScreen(xs[2], y, w, h, 'Confirmed', (x, yy, ww, hh) => {
      let b = K.circle(x + ww / 2, yy + 78, 24, { s: 's-grn' });
      b += K.polyline([[x + ww / 2 - 11, yy + 78], [x + ww / 2 - 3, yy + 87], [x + ww / 2 + 12, yy + 68]], { cls: 's-grn', w: 3 });
      b += T(x + ww / 2, yy + 126, 'Collect at break', { size: 11, cls: 't-mut' });
      return b;
    });
    s += K.line(xs[0] + w + 4, 95, xs[1] - 4, 95, { arrow: true, w: 2.2 });
    s += K.line(xs[1] + w + 4, 95, xs[2] - 4, 95, { arrow: true, w: 2.2 });
    s += T(xs[0] + w / 2, 190, '1 Select item', { size: 12, w: 'b' });
    s += T(xs[1] + w / 2, 190, '2 Name and class', { size: 12, w: 'b' });
    s += T(xs[2] + w / 2, 190, '3 Collect order', { size: 12, w: 'b' });
    return K.svg(440, 202, s, { title: 'Three paper screens of the canteen pre-order prototype with arrows between them' });
  });

  /* ---------------------------------------------------------------- 04 */
  D.register('xii6.dbti', () => {
    let s = '';
    const bx = (x, y, t1, t2, c) => K.rect(x, y, 130, 52, { c: c, r: 10 }) + T(x + 65, y + 21, t1, { size: 14, w: 'b' }) + T(x + 65, y + 39, t2, { size: 11, cls: 't-mut' });
    s += bx(155, 8, 'Design', 'plan the solution', 0);
    s += bx(300, 108, 'Build', 'make an early version', 1);
    s += bx(155, 208, 'Test', 'show it to users', 4);
    s += bx(10, 108, 'Iterate', 'improve from feedback', 5);
    s += arrowPath('M287 34 Q365 34 365 106');
    s += arrowPath('M365 162 Q365 234 287 234');
    s += arrowPath('M153 234 Q75 234 75 162');
    s += arrowPath('M75 106 Q75 34 153 34');
    s += T(220, 130, 'repeat', { size: 14, w: 'b', cls: 't-mut' });
    s += T(220, 148, 'again and again', { size: 12, cls: 't-mut' });
    return K.svg(440, 270, s, { title: 'Design, Build, Test, Iterate cycle' });
  });

  D.register('xii6.classbuddy-flow', () => {
    let s = '';
    const w = 108;
    const h = 150;
    const xs = [12, 166, 320];
    s += miniScreen(xs[0], 14, w, h, 'Today', (x, yy) => {
      let b = '';
      for (let i = 0; i < 4; i++) {
        b += K.rect(x + 10, yy + 40 + i * 26, w - 20, 20, { r: 3, s: 's-mut', dash: '3 2' });
        b += wavy(x + 16, yy + 50 + i * 26, w - 34);
      }
      return b;
    });
    s += miniScreen(xs[1], 14, w, h, 'Add Homework', (x, yy) => {
      let b = '';
      b += T(x + 12, yy + 52, 'Subject', { size: 11, anchor: 'start', cls: 't-mut' });
      b += K.rect(x + 10, yy + 58, w - 20, 18, { r: 3, s: 's-mut', dash: '3 2' });
      b += T(x + 12, yy + 94, 'Task', { size: 11, anchor: 'start', cls: 't-mut' });
      b += K.rect(x + 10, yy + 100, w - 20, 18, { r: 3, s: 's-mut', dash: '3 2' });
      b += K.rect(x + 28, yy + 124, w - 56, 18, { r: 9, s: 's-mut', dash: '3 2' });
      b += T(x + w / 2, yy + 133, 'Save', { size: 11, vmid: true, cls: 't-mut' });
      return b;
    });
    s += miniScreen(xs[2], 14, w, h, 'Reminder', (x, yy) => {
      let b = K.circle(x + w / 2, yy + 74, 24, { s: 's-mut', c: 4 });
      b += T(x + w / 2, yy + 74, '!', { size: 22, w: 'b', vmid: true });
      b += T(x + w / 2, yy + 122, 'Maths test\ntomorrow', { size: 11, cls: 't-mut', lh: 14 });
      return b;
    });
    s += K.line(xs[0] + w + 4, 90, xs[1] - 4, 90, { arrow: true, w: 2.2 });
    s += K.line(xs[1] + w + 4, 90, xs[2] - 4, 90, { arrow: true, w: 2.2 });
    s += T(xs[0] + w / 2, 186, '1 Today\'s classes', { size: 12, w: 'b' });
    s += T(xs[1] + w / 2, 186, '2 Add homework', { size: 12, w: 'b' });
    s += T(xs[2] + w / 2, 186, '3 Reminder', { size: 12, w: 'b' });
    return K.svg(440, 198, s, { title: 'Three low-fidelity ClassBuddy screens with arrows showing the user flow' });
  });

  D.register('xii6.test-session', () => {
    let s = '';
    s += person(70, 110, 3);
    s += K.rect(95, 100, 54, 40, { r: 4, s: 's-mut', dash: '4 3' });
    s += wavy(102, 114, 38);
    s += wavy(102, 126, 38);
    s += T(70, 160, 'User', { size: 13, w: 'b' });
    s += T(70, 176, 'tries the paper screens', { size: 11, cls: 't-mut' });
    s += person(330, 110, 1);
    s += K.rect(268, 108, 40, 32, { r: 3, c: 4 });
    s += wavy(274, 120, 28);
    s += wavy(274, 130, 28);
    s += T(330, 160, 'Observer', { size: 13, w: 'b' });
    s += T(330, 176, 'watches and takes notes', { size: 11, cls: 't-mut' });
    s += K.rect(14, 10, 214, 52, { r: 12, c: 0 });
    s += T(121, 28, 'Task: add one homework', { size: 13, w: 'b' });
    s += T(121, 46, 'and set a reminder', { size: 13, w: 'b' });
    s += K.line(70, 64, 70, 90, { arrow: true, cls: 's-mut' });
    s += K.rect(246, 10, 180, 52, { r: 12, c: 3 });
    s += T(336, 28, 'Observer does not', { size: 12 });
    s += T(336, 46, 'explain too much', { size: 12 });
    s += K.line(330, 64, 330, 90, { arrow: true, cls: 's-mut' });
    s += T(220, 206, 'Note where users hesitate, get stuck or ask questions.', { size: 12, cls: 't-mut' });
    return K.svg(440, 218, s, { title: 'A user tests a paper prototype while an observer takes notes' });
  });

  D.register('xii6.classbuddy', () => {
    let s = '';
    // version 1
    const w = 150;
    const h = 200;
    s += T(100, 16, 'Version 1', { size: 14, w: 'b' });
    s += K.rect(25, 24, w, h, { r: 8, s: 's-mut', dash: '5 3' });
    s += T(100, 46, 'Today\'s classes', { size: 12, w: 'b', cls: 't-mut' });
    for (let i = 0; i < 3; i++) {
      s += K.rect(37, 58 + i * 30, w - 24, 22, { r: 3, s: 's-mut', dash: '3 2' });
      s += wavy(46, 69 + i * 30, 90);
    }
    s += K.rect(135, 190, 28, 22, { r: 11, c: 6 });
    s += T(149, 202, '+', { size: 14, vmid: true });
    s += K.line(150, 232, 150, 216, { arrow: true, cls: 's-red' });
    s += T(100, 246, 'Add button is tiny', { size: 11, cls: 't-red' });
    // arrow
    s += K.line(184, 120, 246, 120, { arrow: true, w: 2.4 });
    s += T(215, 108, 'feedback', { size: 11, cls: 't-mut' });
    // version 2
    s += T(340, 16, 'Version 2', { size: 14, w: 'b' });
    s += K.rect(265, 24, w, h, { r: 8, s: 's-grn' });
    s += T(340, 46, 'Home', { size: 12, w: 'b', cls: 't-mut' });
    s += K.rect(275, 56, w - 20, 36, { r: 18, c: 5 });
    s += T(340, 74, 'Add Homework', { size: 13, w: 'b', vmid: true });
    ['Maths  due Mon', 'Physics  due Wed', 'English  due Fri'].forEach((l, i) => {
      s += K.rect(275, 102 + i * 28, w - 20, 22, { r: 3, c: 6 });
      s += T(282, 113 + i * 28, l, { size: 11, anchor: 'start', vmid: true });
    });
    s += K.rect(285, 190, w - 40, 24, { r: 12, c: 1 });
    s += T(340, 202, 'Weekly View', { size: 12, vmid: true, w: 'b' });
    s += T(340, 246, 'large, central, subject + date', { size: 11, cls: 't-grn' });
    return K.svg(440, 258, s, { title: 'ClassBuddy home screen before and after feedback' });
  });

  D.register('xii6.feedback-filter', () => {
    let s = '';
    for (let i = 0; i < 5; i++) {
      const cx = 56 + i * 82;
      s += person(cx, 48, i < 4 ? 3 : 4);
    }
    s += T(220, 12, 'Five users test the prototype', { size: 13, w: 'b' });
    for (let i = 0; i < 4; i++) s += K.line(56 + i * 82, 76, 130, 120, { cls: 's-red', w: 1.4, dash: '3 3' });
    s += K.line(384, 76, 340, 120, { cls: 's-acc', w: 1.4, dash: '3 3' });
    s += K.rect(10, 120, 240, 52, { r: 10, c: 3 });
    s += T(130, 138, 'Four users: "Where is the', { size: 12 });
    s += T(130, 154, 'Add button?"  Repeated problem', { size: 12, w: 'b' });
    s += K.rect(262, 120, 168, 52, { r: 10, c: 4 });
    s += T(346, 138, 'One user wants an', { size: 12 });
    s += T(346, 154, 'unusual extra feature', { size: 12, w: 'b' });
    s += K.line(130, 174, 130, 192, { arrow: true, w: 2 });
    s += K.line(346, 174, 346, 192, { arrow: true, w: 2 });
    s += K.rect(10, 194, 240, 38, { r: 10, c: 5 });
    s += T(130, 213, 'Button not visible: fix it now', { size: 12, w: 'b', vmid: true });
    s += K.rect(262, 194, 168, 38, { r: 10, c: 6 });
    s += T(346, 213, 'Keep it for later', { size: 12, w: 'b', vmid: true });
    return K.svg(440, 244, s, { title: 'Repeated problems are fixed first; one-off requests are kept for later' });
  });

  /* ---------------------------------------------------------------- 05 */
  D.register('xii6.proto-vs-mvp', () => {
    let s = '';
    s += K.rect(8, 8, 206, 236, { r: 12, c: 1 });
    s += K.rect(226, 8, 206, 236, { r: 12, c: 5 });
    s += T(111, 30, 'Prototype', { size: 15, w: 'b' });
    s += T(329, 30, 'MVP', { size: 15, w: 'b' });
    // paper screen
    s += K.rect(78, 44, 66, 84, { r: 5, s: 's-mut', dash: '4 3' });
    s += wavy(86, 62, 50);
    s += K.rect(88, 72, 12, 12, { r: 2, s: 's-mut', dash: '3 2' });
    s += wavy(106, 79, 30);
    s += K.rect(88, 92, 12, 12, { r: 2, s: 's-mut', dash: '3 2' });
    s += wavy(106, 99, 30);
    s += K.rect(92, 110, 42, 12, { r: 3, s: 's-mut', dash: '3 2' });
    // chat group
    s += K.rect(290, 44, 78, 84, { r: 8, c: 6 });
    s += K.rect(298, 54, 52, 20, { r: 8, c: 0 });
    s += T(324, 64, 'Van left', { size: 10.5, vmid: true });
    s += K.rect(308, 80, 52, 20, { r: 8, c: 5 });
    s += T(334, 90, 'Route 2', { size: 10.5, vmid: true });
    s += K.rect(298, 106, 52, 16, { r: 8, c: 0 });
    s += T(324, 114, 'On time', { size: 10.5, vmid: true });
    s += T(111, 148, 'Shows how the idea', { size: 12 });
    s += T(111, 164, 'may look or work', { size: 12 });
    s += T(111, 182, 'May not work', { size: 12, cls: 't-mut' });
    s += T(111, 198, 'Very low cost', { size: 12, cls: 't-mut' });
    s += T(329, 148, 'Tests whether real users', { size: 12 });
    s += T(329, 164, 'will use the solution', { size: 12 });
    s += T(329, 182, 'Works in a basic way', { size: 12, cls: 't-mut' });
    s += T(329, 198, 'Low cost, some development', { size: 12, cls: 't-mut' });
    s += T(111, 226, 'Is the idea understandable?', { size: 12, w: 'b', cls: 't-acc' });
    s += T(329, 226, 'Will users actually use it?', { size: 12, w: 'b', cls: 't-acc' });
    return K.svg(440, 252, s, { title: 'Prototype versus MVP: paper screens versus a working trial WhatsApp group' });
  });

  D.register('xii6.mvp-scope', () => {
    let s = '';
    s += T(112, 16, 'Must-have: the MVP', { size: 14, w: 'b', cls: 't-grn' });
    s += T(332, 16, 'Nice-to-have: later', { size: 14, w: 'b', cls: 't-mut' });
    const must = ['Menu list', 'Student name + class', 'Item and quantity'];
    must.forEach((m, i) => {
      s += K.rect(14, 28 + i * 46, 196, 38, { r: 10, c: 5, s: 's-grn' });
      s += T(112, 47 + i * 46, m, { size: 13, w: 'b', vmid: true });
    });
    const nice = ['Login', 'Online payment', 'Delivery tracking', 'Ratings', 'Discount offers'];
    nice.forEach((m, i) => {
      s += K.rect(234, 28 + i * 33, 196, 28, { r: 8, c: 6, dash: '5 3' });
      s += T(332, 42 + i * 33, m, { size: 12.5, vmid: true, cls: 't-mut' });
    });
    s += K.line(222, 24, 222, 190, { cls: 's-mut', dash: '4 4', w: 1.4 });
    s += K.rect(14, 172, 196, 38, { r: 10, c: 4 });
    s += T(112, 186, 'Built with', { size: 11, cls: 't-mut' });
    s += T(112, 201, 'a free Google Form', { size: 12, w: 'b' });
    s += T(220, 230, 'Start small. Add the extras only after users really use it.', { size: 12, cls: 't-mut' });
    return K.svg(440, 242, s, { title: 'MVP feature scope for a canteen pre-order system: must-have versus nice-to-have' });
  });

  D.register('xii6.risk-matrix', () => {
    let s = '';
    const x0 = 46;
    const y0 = 8;
    const qw = 190;
    const qh = 108;
    s += K.rect(x0, y0, qw, qh, { r: 0, c: 4 });
    s += K.rect(x0 + qw, y0, qw, qh, { r: 0, c: 3 });
    s += K.rect(x0, y0 + qh, qw, qh, { r: 0, c: 6 });
    s += K.rect(x0 + qw, y0 + qh, qw, qh, { r: 0, c: 0 });
    s += T(x0 + qw + qw / 2, y0 + 18, 'RISKIEST: test first', { size: 12, w: 'b', cls: 't-red' });
    s += T(x0 + qw / 2, y0 + 18, 'Known risk: watch it', { size: 12, w: 'b', cls: 't-mut' });
    s += T(x0 + qw / 2, y0 + qh + 18, 'Ignore for now', { size: 12, w: 'b', cls: 't-mut' });
    s += T(x0 + qw + qw / 2, y0 + qh + 18, 'Test later', { size: 12, w: 'b', cls: 't-mut' });
    // dots
    const dot = (x, y, lbl, o) => K.circle(x, y, 6, { cls: o || 'f-red' }) + T(x + 10, y, lbl, { size: 11, anchor: 'start', vmid: true });
    s += dot(x0 + qw + 18, y0 + 46, 'Pay for online tutoring');
    s += dot(x0 + qw + 18, y0 + 72, 'Order via WhatsApp', 'f-acc');
    s += dot(x0 + qw + 18, y0 + 98, 'Check van updates daily', 'f-acc');
    s += dot(x0 + 12, y0 + 56, 'Students own phones', 'f-grn');
    s += dot(x0 + qw + 18, y0 + qh + 52, 'Prefers blue logo', 'f-ink');
    // axes
    s += K.line(x0 - 8, y0 + 2 * qh, x0 - 8, y0, { arrow: true, cls: 's-mut', w: 1.6 });
    s += K.line(x0, y0 + 2 * qh + 8, x0 + 2 * qw, y0 + 2 * qh + 8, { arrow: true, cls: 's-mut', w: 1.6 });
    s += T(18, y0 + qh, 'Impact if wrong', { size: 12, rot: -90, cls: 't-mut' });
    s += T(x0 + qw, y0 + 2 * qh + 28, 'How uncertain are we?  (low to high)', { size: 12, cls: 't-mut' });
    return K.svg(440, 262, s, { title: 'Riskiest assumption matrix: impact if wrong versus uncertainty, with four quadrants' });
  });

  /* ---------------------------------------------------------------- 06 */
  D.register('xii6.canteen-case', () => {
    const rows = [
      ['Paper prototype', 'Three steps: select item, enter name and class, collect order.', 0],
      ['Feedback', 'Easy process, but the menu should be short. Pay at collection time.', 4],
      ['MVP for 3 days', 'Google Form or paper register. Students choose one of five items.', 1],
      ['Result', 'Students saved time. Canteen staff found too many items hard.', 3],
      ['Improvement', 'Keep five items, close orders 20 minutes before break, one collection line.', 5],
    ];
    let s = '';
    rows.forEach((r, i) => {
      const y = 6 + i * 58;
      s += K.rect(8, y, 112, 48, { c: r[2], r: 8 });
      s += T(64, y + 24, r[0], { size: 12, w: 'b', vmid: true, lh: 14 });
      s += K.rect(128, y, 304, 48, { r: 8, s: 's-mut', dash: '4 3' });
      const parts = r[1].length > 40 ? [r[1].slice(0, r[1].lastIndexOf(' ', 40)), r[1].slice(r[1].lastIndexOf(' ', 40) + 1)] : [r[1]];
      if (r[1].length > 40) {
        const cut = r[1].lastIndexOf(' ', 40);
        s += T(280, y + 24, r[1].slice(0, cut) + '\n' + r[1].slice(cut + 1), { size: 11.5, vmid: true, lh: 15 });
      } else s += T(280, y + 24, r[1], { size: 11.5, vmid: true });
      if (i < 4) s += K.line(64, y + 49, 64, y + 57, { arrow: true, cls: 's-mut' });
    });
    return K.svg(440, 296, s, { title: 'Canteen pre-order case study from paper prototype to improved MVP' });
  });

  D.register('xii6.bml', () => {
    let s = '';
    const bx = (x, t, sub, c) => K.rect(x, 54, 104, 54, { c: c, r: 10 }) + T(x + 52, 76, t, { size: 15, w: 'b' }) + T(x + 52, 94, sub, { size: 11, cls: 't-mut' });
    s += bx(10, 'Build', 'smallest MVP', 1);
    s += bx(168, 'Measure', 'real user data', 4);
    s += bx(326, 'Learn', 'keep, change, drop', 5);
    s += K.line(116, 81, 166, 81, { arrow: true, w: 2.4 });
    s += K.line(274, 81, 324, 81, { arrow: true, w: 2.4 });
    s += T(141, 72, 'product', { size: 11, cls: 't-mut' });
    s += T(299, 72, 'numbers', { size: 11, cls: 't-mut' });
    s += K.line(62, 14, 62, 52, { arrow: true, w: 2 });
    s += T(72, 30, 'new idea', { size: 12, anchor: 'start', cls: 't-acc' });
    s += K.path('M378 110 Q378 156 220 156 Q62 156 62 112', { arrow: true, cls: 's-brand', w: 2.2 });
    s += T(220, 148, 'learning becomes the next idea', { size: 12, cls: 't-acc' });
    s += T(220, 184, 'Fast loops: learn quickly before spending a lot of time and money.', { size: 12, cls: 't-mut' });
    return K.svg(440, 196, s, { title: 'Build, Measure, Learn loop' });
  });

  D.register('xii6.profit', () => {
    let s = '';
    const u = 360 / 18000;
    const x0 = 40;
    s += T(220, 16, 'Home bakery on Instagram: 30 boxes sold at Rs 600', { size: 13, w: 'b' });
    s += K.rect(x0, 30, 360, 38, { c: 1, r: 4 });
    s += T(220, 49, 'Revenue  Rs 18,000', { size: 14, w: 'b', vmid: true });
    s += K.rect(x0, 92, 3000 * u, 38, { c: 7, r: 4 });
    s += K.rect(x0 + 3000 * u, 92, 12000 * u, 38, { c: 3, r: 4 });
    s += K.rect(x0 + 15000 * u, 92, 3000 * u, 38, { c: 5, r: 4, dash: '5 3' });
    s += T(x0 + 30, 111, '3,000', { size: 12, w: 'b', vmid: true });
    s += T(x0 + 3000 * u + 120, 111, 'Variable  Rs 12,000', { size: 13, w: 'b', vmid: true });
    s += T(x0 + 15000 * u + 30, 111, '3,000', { size: 12, w: 'b', vmid: true });
    s += T(x0 + 30, 146, 'Fixed', { size: 11, cls: 't-mut' });
    s += T(x0 + 15000 * u + 30, 146, 'Profit', { size: 12, w: 'b', cls: 't-grn' });
    s += T(x0 + 3000 * u + 120, 146, 'Total cost  Rs 15,000', { size: 12, cls: 't-mut' });
    s += T(220, 182, 'Revenue Rs 18,000 minus Cost Rs 15,000 = Profit Rs 3,000', { size: 12, w: 'b' });
    return K.svg(440, 196, s, { title: 'Revenue bar compared with fixed plus variable cost bar leaving profit' });
  });

  D.register('xii6.breakeven', () => {
    let s = '';
    const ox = 56;
    const oy = 196;
    const pw = 360;
    const ph = 160;
    const X = (b) => ox + (b / 30) * pw;
    const Y = (v) => oy - (v / 18000) * ph;
    s += K.line(ox, oy, ox + pw + 10, oy, { arrow: true, cls: 's-mut' });
    s += K.line(ox, oy, ox, oy - ph - 12, { arrow: true, cls: 's-mut' });
    s += T(ox + pw / 2, oy + 30, 'Boxes sold', { size: 12, cls: 't-mut' });
    s += T(14, oy - ph / 2, 'Rupees', { size: 12, rot: -90, cls: 't-mut' });
    [0, 15, 30].forEach((b) => (s += T(X(b), oy + 14, String(b), { size: 11, cls: 't-mut' })));
    s += K.path('M' + X(0) + ' ' + Y(3000) + ' L' + X(30) + ' ' + Y(15000), { cls: 's-red', w: 2.6 });
    s += K.path('M' + X(0) + ' ' + Y(0) + ' L' + X(30) + ' ' + Y(18000), { cls: 's-grn', w: 2.6 });
    s += T(X(30) - 6, Y(18000) - 8, 'Revenue', { size: 12, w: 'b', anchor: 'end', cls: 't-grn' });
    s += T(X(30) + 6, Y(15000) + 22, 'Total cost', { size: 12, w: 'b', anchor: 'end', cls: 't-red' });
    s += K.line(X(15), Y(9000), X(15), oy, { cls: 's-mut', dash: '4 3', w: 1.4 });
    s += K.circle(X(15), Y(9000), 7, { cls: 'f-acc' });
    s += T(X(15) - 12, Y(9000) - 24, 'Break-even', { size: 12, w: 'b', anchor: 'end' });
    s += T(X(15) - 12, Y(9000) - 9, '15 boxes', { size: 12, anchor: 'end' });
    s += T(X(7), Y(1600), 'Loss', { size: 13, w: 'b', cls: 't-red' });
    s += T(X(23), Y(6500), 'Profit', { size: 13, w: 'b', cls: 't-grn' });
    s += K.line(X(23), Y(6500) - 16, X(24), Y(12400), { arrow: true, cls: 's-grn', w: 1.4 });
    s += T(ox - 6, Y(3000) + 4, '3,000', { size: 11, anchor: 'end', cls: 't-mut' });
    return K.svg(440, 232, s, { title: 'Break-even chart: revenue line crosses total cost line at fifteen boxes' });
  });

  /* ---------------------------------------------------------------- 07 */
  D.register('xii6.reuse', (args) => {
    args = args || {};
    const tried = args.tried || 40;
    const again = args.again == null ? 30 : args.again;
    const cols = 10;
    const rows = Math.ceil(tried / cols);
    let s = '';
    const pct = Math.round((again / tried) * 100);
    s += T(220, 16, tried + ' users tried the MVP', { size: 14, w: 'b' });
    const gx = 220 - (cols * 28) / 2 + 14;
    for (let i = 0; i < tried; i++) {
      const cx = gx + (i % cols) * 28;
      const cy = 40 + Math.floor(i / cols) * 28;
      s += K.circle(cx, cy, 10, { c: i < again ? 5 : 6, s: i < again ? 's-grn' : 's-mut' });
    }
    const yb = 40 + (rows - 1) * 28 + 36;
    s += K.circle(80, yb, 8, { c: 5, s: 's-grn' });
    s += T(94, yb, again + ' would use it again', { size: 12, anchor: 'start', vmid: true });
    s += K.circle(262, yb, 8, { c: 6, s: 's-mut' });
    s += T(276, yb, tried - again + ' would not', { size: 12, anchor: 'start', vmid: true });
    s += T(220, yb + 32, again + ' out of ' + tried + ' = ' + pct + '% came back', { size: 14, w: 'b', cls: pct >= 50 ? 't-grn' : 't-red' });
    return K.svg(440, yb + 46, s, { title: again + ' of ' + tried + ' users would use the MVP again' });
  });

  D.register('xii6.beachhead', () => {
    let s = '';
    const cx = 120;
    const cy = 132;
    s += K.circle(cx, cy, 112, { c: 3 });
    s += K.circle(cx, cy + 22, 78, { c: 4 });
    s += K.circle(cx, cy + 44, 40, { c: 5, s: 's-grn' });
    s += T(cx, cy - 92, 'All students', { size: 12, w: 'b' });
    s += T(cx, cy - 77, 'in Pakistan', { size: 12, w: 'b' });
    s += T(cx, cy - 42, 'All students', { size: 11.5 });
    s += T(cx, cy - 28, 'in Sindh', { size: 11.5 });
    s += T(cx, cy + 40, 'Grade XII', { size: 11.5, w: 'b' });
    s += T(cx, cy + 54, 'one college', { size: 11.5, w: 'b' });
    s += K.line(258, 70, 220, 70, { arrow: true, cls: 's-red' });
    s += T(268, 64, 'Too broad: hard to', { size: 12, anchor: 'start', cls: 't-red' });
    s += T(268, 80, 'reach and test', { size: 12, anchor: 'start', cls: 't-red' });
    s += K.line(258, 176, 164, 176, { arrow: true, cls: 's-grn' });
    s += T(268, 160, 'Beachhead market:', { size: 12, w: 'b', anchor: 'start', cls: 't-grn' });
    s += T(268, 176, 'specific, reachable,', { size: 12, anchor: 'start', cls: 't-grn' });
    s += T(268, 192, 'willing to test', { size: 12, anchor: 'start', cls: 't-grn' });
    s += K.path('M158 232 Q226 240 262 214', { arrow: true, cls: 's-brand', w: 2.2 });
    s += T(268, 226, 'Learn here first,', { size: 12, anchor: 'start', cls: 't-acc' });
    s += T(268, 242, 'expand later', { size: 12, anchor: 'start', cls: 't-acc' });
    return K.svg(440, 262, s, { title: 'Concentric markets: start with one college, then expand to Sindh and Pakistan' });
  });
})();
