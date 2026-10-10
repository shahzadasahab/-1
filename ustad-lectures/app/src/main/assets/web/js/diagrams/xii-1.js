/* XII Ch1 (Human Computer Interaction) diagrams */
(function () {
  const D = Diagrams;
  const T = K.text;

  const faint = (inner, o) => '<g opacity="' + (o || 0.28) + '">' + inner + '</g>';
  const tick = (x, y, s, cls) => K.path('M' + (x - s) + ' ' + y + ' L' + (x - s / 3) + ' ' + (y + s * 0.8) + ' L' + (x + s) + ' ' + (y - s * 0.8), { cls: cls || 's-grn', w: 2.8 });
  const cross = (x, y, s, cls) =>
    K.line(x - s, y - s, x + s, y + s, { cls: cls || 's-red', w: 2.8 }) + K.line(x - s, y + s, x + s, y - s, { cls: cls || 's-red', w: 2.8 });
  const person = (cx, top, k, c) =>
    K.circle(cx, top + 7 * k, 7 * k, { c: c }) +
    K.path('M' + (cx - 11 * k) + ' ' + (top + 32 * k) + ' Q' + (cx - 11 * k) + ' ' + (top + 17 * k) + ' ' + cx + ' ' + (top + 17 * k) + ' Q' + (cx + 11 * k) + ' ' + (top + 17 * k) + ' ' + (cx + 11 * k) + ' ' + (top + 32 * k) + ' Z', { c: c });
  const phone = (x, y, w, h, c) => K.rect(x, y, w, h, { r: 14, c: c }) + K.rect(x + w / 2 - 14, y + 6, 28, 5, { r: 2.5, c: 6 });
  const star = (cx, cy, r, c) => {
    const p = [];
    for (let i = 0; i < 10; i++) {
      const a = -Math.PI / 2 + (i * Math.PI) / 5;
      const rr = i % 2 ? r * 0.45 : r;
      p.push([cx + Math.cos(a) * rr, cy + Math.sin(a) * rr]);
    }
    return K.poly(p, { c: c });
  };
  const bar = (x, y, w, h, c) => K.rect(x, y, w, h, { r: 2, c: c == null ? 6 : c });
  const lines = (x, y, w, n, gap, c) => {
    let o = '';
    for (let i = 0; i < n; i++) o += K.line(x, y + i * gap, x + (i === n - 1 ? w * 0.65 : w), y + i * gap, { cls: 's-mut', w: 2 });
    return o;
  };
  const cardGrid = (items, o) => {
    o = o || {};
    const cw = 212;
    const ch = o.h || 52;
    const gap = 6;
    let s = '';
    items.forEach((it, i) => {
      const x = 4 + (i % 2) * (cw + 8);
      const y = 4 + Math.floor(i / 2) * (ch + gap);
      s += K.rect(x, y, cw, ch, { c: (o.colors || [0, 1, 2, 3, 4, 5, 7])[i % (o.colors || [0, 1, 2, 3, 4, 5, 7]).length], r: 8 });
      s += T(x + 10, y + 19, it[0], { size: 12, w: 'b', anchor: 'start' });
      s += T(x + 10, y + 34, it[1], { size: 11, cls: 't-mut', anchor: 'start', lh: 13 });
    });
    return s;
  };

  /* ---------- Lecture 1 ---------- */

  D.register('xii1.hci-model', () => {
    let s = '';
    const chips = [['Sight', 1], ['Touch', 7], ['Hearing', 6], ['Voice', 3], ['Spatial', 2]];
    s += T(220, 18, 'Human senses  <->  Computer', { size: 14, w: 'b' });
    chips.forEach((c, i) => {
      s += K.box(6 + i * 86, 30, 80, 32, c[0], { c: c[1], size: 13, bold: true });
    });
    [[46, 60], [132, 120], [218, 170], [304, 280], [390, 380]].forEach((p) => {
      s += K.line(p[0], 62, p[1], 98, { arrow: true, cls: 's-mut' });
    });
    s += K.rect(6, 100, 200, 190, { c: 0 });
    s += K.rect(214, 100, 220, 190, { c: 2 });
    s += T(106, 119, 'Interaction I: Traditional', { size: 12, w: 'b' });
    s += T(324, 119, 'Interaction II: Natural', { size: 12, w: 'b' });
    const cell = (x, y, w, h, l) => K.box(x, y, w, h, l, { c: null, size: 11, r: 5 });
    s += T(25, 164, 'I/P', { size: 12, w: 'b' });
    s += T(25, 242, 'O/P', { size: 12, w: 'b' });
    s += cell(44, 134, 78, 60, 'Mouse +\nKeyboard') + cell(126, 134, 78, 60, 'Touch\nscreen UI');
    s += cell(44, 206, 78, 76, 'Monitor +\nspeakers') + cell(126, 206, 78, 76, 'Screen +\nspeakers +\nvibrations');
    s += T(233, 164, 'I/P', { size: 12, w: 'b' });
    s += T(233, 242, 'O/P', { size: 12, w: 'b' });
    s += cell(254, 134, 84, 60, 'Voice') + cell(342, 134, 88, 60, 'Body, gesture\n+ face');
    s += cell(254, 206, 84, 76, 'Speakers,\nsensors') + cell(342, 206, 88, 76, 'Screen +\nspeakers');
    return K.svg(440, 296, s, { title: 'Model of Human Computer Interaction: five sensory channels leading to traditional and natural interaction' });
  });

  D.register('xii1.triangle', () => {
    let s = '';
    s += K.box(10, 14, 150, 66, '', { c: 1 });
    s += T(85, 40, 'User', { size: 16, w: 'b' }) + T(85, 62, 'end users, stakeholders', { size: 11, cls: 't-mut' });
    s += K.box(280, 14, 150, 66, '', { c: 0 });
    s += T(355, 40, 'Computer', { size: 16, w: 'b' }) + T(355, 62, 'hardware + software', { size: 11, cls: 't-mut' });
    s += K.box(145, 212, 150, 66, '', { c: 4 });
    s += T(220, 238, 'Interaction', { size: 16, w: 'b' }) + T(220, 260, 'input, output, feedback', { size: 11, cls: 't-mut' });
    s += K.line(162, 47, 278, 47, { arrow: 'both', cls: 's-brand', w: 2.2 });
    s += T(220, 38, 'interface', { size: 12, cls: 't-acc' });
    s += K.line(60, 82, 175, 210, { arrow: 'both', cls: 's-mut' });
    s += T(100, 158, 'tap, type,\nspeak', { size: 11, cls: 't-mut', anchor: 'end' });
    s += K.line(380, 82, 265, 210, { arrow: 'both', cls: 's-mut' });
    s += T(334, 158, 'screen, sound,\nvibration', { size: 11, cls: 't-mut', anchor: 'start' });
    s += K.circle(220, 135, 36, { c: 5 }) + T(220, 135, 'HCI', { size: 18, w: 'b', vmid: true });
    return K.svg(440, 290, s, { title: 'HCI triangle: User, Computer and Interaction' });
  });

  D.register('xii1.apps', () => {
    let s = '';
    const tiles = [
      ['Healthcare', 'Patient portals,\ntelemedicine apps', 0],
      ['Banking', 'Secure mobile\nbanking apps', 4],
      ['Education', 'E-learning platforms,\nexam portals', 1],
      ['Networking &\nCommunication', 'Social media, chat apps,\ncollaboration tools', 2],
    ];
    tiles.forEach((t, i) => {
      const x = 4 + (i % 2) * 220;
      const y = 6 + Math.floor(i / 2) * 110;
      s += K.rect(x, y, 212, 100, { c: t[2] });
      const ix = x + 34;
      const iy = y + 50;
      if (i === 0) s += K.rect(ix - 8, iy - 22, 16, 44, { c: 3, r: 3 }) + K.rect(ix - 22, iy - 8, 44, 16, { c: 3, r: 3 });
      if (i === 1) s += K.circle(ix, iy, 22, { c: 4 }) + T(ix, iy, 'Rs', { size: 14, w: 'b', vmid: true });
      if (i === 2) s += K.rect(ix - 22, iy - 16, 20, 34, { c: 5, r: 2 }) + K.rect(ix + 2, iy - 16, 20, 34, { c: 5, r: 2 }) + K.line(ix - 18, iy - 6, ix - 6, iy - 6, { cls: 's-mut' }) + K.line(ix + 6, iy - 6, ix + 18, iy - 6, { cls: 's-mut' });
      if (i === 3) s += K.rect(ix - 24, iy - 22, 30, 22, { c: 6, r: 6 }) + K.rect(ix - 6, iy - 4, 30, 22, { c: 7, r: 6 });
      s += T(x + 68, y + (i === 3 ? 28 : 36), t[0], { size: 13, w: 'b', anchor: 'start', lh: 15 });
      s += T(x + 68, y + (i === 3 ? 62 : 58), t[1], { size: 11, cls: 't-mut', anchor: 'start', lh: 13 });
    });
    return K.svg(440, 224, s, { title: 'HCI applications: healthcare, banking, education, networking and communication' });
  });

  /* ---------- Lecture 2 ---------- */

  D.register('xii1.user-types', () => {
    let s = '';
    s += K.rect(4, 6, 212, 214, { c: 1 }) + T(110, 28, 'End Users', { size: 14, w: 'b' });
    [['Beginner', 40], ['Intermediate', 110], ['Expert', 180]].forEach((p, i) => {
      s += person(p[1], 48 + (2 - i) * 4, 1.0 + i * 0.12, null) + T(p[1], 112, p[0], { size: 11 });
    });
    s += K.line(24, 134, 196, 134, { arrow: true, cls: 's-brand', w: 2 });
    s += T(110, 156, 'directly operate', { size: 12, cls: 't-mut' }) + T(110, 172, 'and interact with the system', { size: 12, cls: 't-mut' });
    s += K.rect(224, 6, 212, 214, { c: 4 }) + T(330, 28, 'Stakeholders', { size: 14, w: 'b' });
    ['Clients', 'Managers', 'Administrators', 'Decision-makers'].forEach((l, i) => {
      s += K.box(250, 42 + i * 34, 160, 28, l, { c: null, size: 12, r: 14 });
    });
    s += T(330, 196, 'interested in performance', { size: 11, cls: 't-mut' }) + T(330, 210, 'or outcomes of the system', { size: 11, cls: 't-mut' });
    return K.svg(440, 226, s, { title: 'Two kinds of users: end users and stakeholders' });
  });

  D.register('xii1.interaction-loop', () => {
    let s = '';
    s += T(220, 22, 'Input: click, tap, type, swipe, speak', { size: 13, cls: 't-acc' });
    s += K.rect(6, 52, 104, 104, { c: 1 }) + person(58, 66, 1.1, null) + T(58, 142, 'User', { size: 14, w: 'b' });
    s += K.box(174, 52, 92, 104, 'User\nInterface', { c: 4, size: 13, bold: true });
    s += K.rect(330, 52, 104, 104, { c: 0 }) + K.rect(354, 68, 56, 38, { c: null, r: 4 }) + K.rect(366, 110, 32, 6, { c: 6, r: 2 }) + T(382, 142, 'Computer', { size: 14, w: 'b' });
    s += K.line(112, 82, 172, 82, { arrow: true, cls: 's-brand', w: 2.2 }) + K.line(268, 82, 328, 82, { arrow: true, cls: 's-brand', w: 2.2 });
    s += K.line(328, 124, 268, 124, { arrow: true, cls: 's-grn', w: 2.2 }) + K.line(172, 124, 112, 124, { arrow: true, cls: 's-grn', w: 2.2 });
    s += T(220, 188, 'Output + Feedback: screen, sound, vibration', { size: 13, cls: 't-grn' });
    s += T(220, 208, 'User action becomes a system response', { size: 12, cls: 't-mut' });
    return K.svg(440, 216, s, { title: 'User interaction loop: input from user, output and feedback from computer' });
  });

  D.register('xii1.interaction-types', () => {
    let s = '';
    const items = [
      ['Direct Manipulation', 'drag files, zoom with fingers'],
      ['Command-Based', 'typed commands: Dir, Cd..'],
      ['Menu-Driven', 'Start Test, Check Results'],
      ['Form Fill', 'sign-up and admission forms'],
      ['Conversational', 'chatbots, Alexa, Google Assistant'],
      ['Gesture-Based', 'swipe, VR hand gestures'],
      ['Voice Interaction', '"Call Aslam", voice search'],
      ['Context-Aware', 'smart lights, GPS re-routing'],
      ['Biometric', 'fingerprint, face, iris scan'],
      ['Haptic & Tactile', 'vibration, smartwatch tap'],
    ];
    items.forEach((it, i) => {
      const x = 4 + (i % 2) * 220;
      const y = 4 + Math.floor(i / 2) * 48;
      s += K.rect(x, y, 212, 42, { c: [0, 1, 2, 3, 4, 5, 7][i % 7] });
      s += T(x + 10, y + 17, it[0], { size: 12, w: 'b', anchor: 'start' }) + T(x + 10, y + 33, it[1], { size: 11, cls: 't-mut', anchor: 'start' });
    });
    s += K.rect(4, 244, 432, 42, { c: 6 });
    s += T(14, 261, 'Multimodal', { size: 12, w: 'b', anchor: 'start' }) + T(14, 277, 'two or more types together: voice + touch, gesture + voice', { size: 11, cls: 't-mut', anchor: 'start' });
    return K.svg(440, 292, s, { title: 'Eleven types of user interaction with examples' });
  });

  /* ---------- Lecture 3 ---------- */

  D.register('xii1.task-chars', () => {
    let s = '';
    s += K.rect(100, 6, 240, 62, { c: 4 }) + T(220, 28, 'Task', { size: 15, w: 'b' }) + T(220, 48, 'a specific action: click, type,', { size: 11, cls: 't-mut' }) + T(220, 61, 'search, book a ticket', { size: 11, cls: 't-mut' });
    const kids = [
      ['Task Complexity', 'online form: easy\n3D model: complex', 1],
      ['Knowledge & Skills', 'text message: typing\nrobot: advanced skill', 2],
      ['Time Requirement', 'ATM balance: seconds\npassport: minutes', 0],
    ];
    kids.forEach((k, i) => {
      const x = 4 + i * 146;
      s += K.line(220, 68, x + 69, 108, { arrow: true, cls: 's-mut' });
      s += K.rect(x, 110, 138, 80, { c: k[2] });
      s += T(x + 69, 130, k[0], { size: 12, w: 'b' });
      s += T(x + 69, 152, k[1], { size: 11, cls: 't-mut', lh: 15 });
    });
    return K.svg(440, 196, s, { title: 'Three characteristics of a task: complexity, knowledge and skills, time' });
  });

  D.register('xii1.ui-kinds', () => {
    let s = '';
    const tile = (x, y, c) => K.rect(x, y, 140, 134, { c: c });
    const label = (x, y, a, b) => T(x + 70, y + 104, a, { size: 13, w: 'b' }) + T(x + 70, y + 121, b, { size: 11, cls: 't-mut' });
    let x = 4;
    let y = 4;
    s += tile(x, y, 1) + K.rect(x + 20, y + 14, 100, 72, { c: null, r: 4 }) + K.rect(x + 20, y + 14, 100, 14, { c: 1, r: 4 });
    [[30, 4], [62, 5], [94, 7]].forEach((p) => (s += K.rect(x + p[0], y + 38, 22, 20, { c: p[1], r: 4 })));
    s += K.line(x + 28, y + 70, x + 112, y + 70, { cls: 's-mut', w: 2 }) + label(x, y, 'GUI', 'windows, icons, menus');
    x = 148;
    s += tile(x, y, 6) + K.rect(x + 20, y + 14, 100, 72, { c: null, r: 4 }) + K.rect(x + 22, y + 16, 96, 68, { c: null, r: 3, cls: 's-mut' });
    s += T(x + 28, y + 38, 'C:\\> dir', { size: 12, anchor: 'start' }) + T(x + 28, y + 56, 'C:\\> cd..', { size: 12, anchor: 'start' }) + K.line(x + 28, y + 72, x + 38, y + 72, { cls: 's-brand', w: 3 }) + label(x, y, 'CLI', 'type text commands');
    x = 292;
    s += tile(x, y, 0) + phone(x + 48, y + 8, 44, 82, null) + K.circle(x + 70, y + 54, 7, { c: 4 }) + K.circle(x + 70, y + 54, 14, { c: null, cls: 's-acc' }) + label(x, y, 'Touch Interface', 'tap, swipe, pinch');
    x = 76;
    y = 142;
    s += tile(x, y, 3) + K.rect(x + 50, y + 26, 28, 44, { c: null, r: 6 }) + K.circle(x + 64, y + 56, 8, { c: 3 });
    [10, 18].forEach((r, i) => (s += K.path('M' + (x + 84 + i * 8) + ' ' + (y + 38) + ' Q' + (x + 94 + i * 8) + ' ' + (y + 48) + ' ' + (x + 84 + i * 8) + ' ' + (y + 58), { s: 's-acc', w: 2 })));
    s += label(x, y, 'Voice UI (VUI)', 'speak commands');
    x = 220;
    s += tile(x, y, 2) + K.circle(x + 70, y + 24, 9, { c: null }) + K.line(x + 70, y + 33, x + 70, y + 66, { w: 3 }) + K.line(x + 70, y + 66, x + 58, y + 88, { w: 3 }) + K.line(x + 70, y + 66, x + 82, y + 88, { w: 3 });
    s += K.line(x + 70, y + 42, x + 46, y + 28, { w: 3 }) + K.line(x + 70, y + 42, x + 94, y + 58, { w: 3 }) + label(x, y, 'Natural UI (NUI)', 'gestures, body');
    return K.svg(440, 282, s, { title: 'Types of user interface: GUI, CLI, touch, voice and natural user interface' });
  });

  D.register('xii1.environment', () => {
    let s = '';
    s += K.rect(4, 6, 432, 214, { c: null, r: 16, dash: '6 5', cls: 's-brand' });
    s += T(220, 28, 'Environment: the real-world setting of use', { size: 13, w: 'b', cls: 't-acc' });
    [['User', 1], ['Hardware', 0], ['Software & Apps', 2]].forEach((b, i) => {
      s += K.box(22 + i * 140, 52, 108, 62, b[0] === 'Software & Apps' ? 'Software\n& Apps' : b[0], { c: b[1], size: 13, bold: true });
    });
    s += K.line(133, 83, 159, 83, { arrow: 'both', cls: 's-mut' }) + K.line(273, 83, 299, 83, { arrow: 'both', cls: 's-mut' });
    [['Physical', 'room, light, noise'], ['Social', 'people around'], ['Technical', 'device, network']].forEach((t, i) => {
      s += K.rect(22 + i * 140, 140, 120, 56, { c: null, r: 8 });
      s += T(82 + i * 140, 162, t[0], { size: 12, w: 'b' }) + T(82 + i * 140, 180, t[1], { size: 11, cls: 't-mut' });
    });
    s += T(220, 133, 'shaped by its surroundings', { size: 11, cls: 't-mut' });
    return K.svg(440, 226, s, { title: 'HCI environment: user, hardware and software inside a physical, social and technical setting' });
  });

  D.register('xii1.feedback', () => {
    let s = '';
    s += K.rect(4, 6, 214, 244, { c: 0 }) + T(111, 28, 'System Feedback', { size: 14, w: 'b' }) + T(111, 44, 'from the computer', { size: 11, cls: 't-mut' });
    s += K.rect(18, 62, 186, 40, { c: null, r: 8 }) + T(111, 87, 'Loading...', { size: 13 });
    s += K.rect(18, 112, 186, 40, { c: null, r: 8, cls: 's-grn' }) + T(98, 137, 'Message Sent!', { size: 13, cls: 't-grn' }) + tick(180, 132, 7);
    s += K.rect(18, 162, 186, 56, { c: null, r: 8, cls: 's-red' }) + T(111, 184, 'Error:', { size: 13, cls: 't-red', w: 'b' }) + T(111, 202, 'incorrect password', { size: 13, cls: 't-red' });
    s += K.rect(222, 6, 214, 244, { c: 4 }) + T(329, 28, 'User Feedback', { size: 14, w: 'b' }) + T(329, 44, 'from the person', { size: 11, cls: 't-mut' });
    s += K.rect(236, 62, 186, 44, { c: null, r: 8 }) + K.circle(264, 84, 6, { c: 4 }) + K.circle(264, 84, 13, { c: null, cls: 's-acc' }) + T(300, 89, 'tapping', { size: 13, anchor: 'start' });
    s += K.rect(236, 116, 186, 44, { c: null, r: 8 }) + K.rect(259, 126, 10, 18, { c: 3, r: 5 }) + K.path('M273 128 Q280 135 273 142', { cls: 's-acc', w: 2 }) + T(300, 143, 'speaking', { size: 13, anchor: 'start' });
    s += K.rect(236, 170, 186, 48, { c: null, r: 8 });
    for (let i = 0; i < 5; i++) s += star(260 + i * 28, 188, 10, i < 4 ? 4 : 6);
    s += T(329, 212, 'rating stars', { size: 11, cls: 't-mut' });
    return K.svg(440, 256, s, { title: 'System feedback versus user feedback' });
  });

  /* ---------- Lecture 4 ---------- */

  D.register('xii1.importance', () => {
    let s = '';
    const nodes = [
      [150, 6, 'Enhance\nProductivity', 'faster, fewer mistakes', 0],
      [6, 98, 'Promotes\nInclusivity', 'screen readers, voice', 1],
      [294, 98, 'Drives\nInnovation', 'AR/VR, AI, IoT', 2],
      [40, 216, 'Economic\nImpact', 'adoption, loyalty', 4],
      [260, 216, 'Ethical\nResponsibility', 'privacy, less bias', 3],
    ];
    nodes.forEach((n) => {
      const cx = n[0] + 70;
      const cy = n[1] + 36;
      s += K.line(220, 150, cx, cy, { cls: 's-mut', dash: '4 3' });
    });
    s += K.circle(220, 150, 38, { c: 5 }) + T(220, 150, 'Good\nHCI', { size: 16, w: 'b', vmid: true });
    nodes.forEach((n) => {
      s += K.rect(n[0], n[1], 140, 72, { c: n[4] });
      s += T(n[0] + 70, n[1] + 20, n[2], { size: 13, w: 'b', lh: 15 });
      s += T(n[0] + 70, n[1] + 62, n[3], { size: 11, cls: 't-mut' });
    });
    return K.svg(440, 296, s, { title: 'Five implications of HCI: productivity, inclusivity, innovation, economic impact, ethical responsibility' });
  });

  D.register('xii1.contrast', () => {
    let s = '';
    s += T(110, 20, 'Good contrast', { size: 14, w: 'b', cls: 't-grn' }) + tick(200, 16, 8);
    s += T(330, 20, 'Poor contrast', { size: 14, w: 'b', cls: 't-red' }) + cross(420, 16, 7);
    const card = (x, y, c, good, tcls) => {
      let o = K.rect(x, y, 210, 74, { c: c });
      const txt = T(x + 14, y + 30, 'Lahore Express', { size: 15, w: 'b', anchor: 'start', cls: tcls }) + T(x + 14, y + 54, 'Platform 3  -  10:45 AM', { size: 13, anchor: 'start', cls: tcls });
      return o + (good ? txt : faint(txt, 0.3));
    };
    s += card(4, 32, null, true) + card(226, 32, null, false);
    s += card(4, 116, 4, true);
    s += K.rect(226, 116, 210, 74, { c: 5 }) + T(240, 146, 'Lahore Express', { size: 15, w: 'b', anchor: 'start', cls: 't-grn' }) + T(240, 170, 'Platform 3  -  10:45 AM', { size: 13, anchor: 'start', cls: 't-grn' });
    s += K.circle(412, 56, 9, { c: 4 });
    for (let a = 0; a < 8; a++) {
      const g = (a * Math.PI) / 4;
      s += K.line(412 + Math.cos(g) * 13, 56 + Math.sin(g) * 13, 412 + Math.cos(g) * 18, 56 + Math.sin(g) * 18, { cls: 's-acc', w: 2 });
    }
    s += T(220, 216, 'dark text on a plain light background stays readable', { size: 12, cls: 't-mut' });
    s += T(220, 232, 'even in bright sunlight', { size: 12, cls: 't-mut' });
    return K.svg(440, 242, s, { title: 'Good contrast versus poor contrast in a railway app' });
  });

  D.register('xii1.fonts', () => {
    let s = '';
    s += K.rect(4, 6, 214, 196, { c: null, r: 10 }) + T(111, 26, 'Readable font', { size: 14, w: 'b', cls: 't-grn' });
    s += T(18, 58, 'Homework Assignments', { size: 15, w: 'b', anchor: 'start' });
    ['Math: questions 1-10', 'Science: water cycle', 'English: Chapter 5'].forEach((l, i) => {
      s += K.circle(24, 86 + i * 30, 3, { c: 0 }) + T(34, 91 + i * 30, l, { size: 14, anchor: 'start' });
    });
    s += T(111, 190, 'clear font, proper size', { size: 11, cls: 't-mut' });
    s += K.rect(222, 6, 214, 196, { c: null, r: 10 }) + T(329, 26, 'Hard to read', { size: 14, w: 'b', cls: 't-red' });
    const bad = T(234, 52, 'Homework Assignments', { size: 11, anchor: 'start' }) + T(234, 64, 'Math: questions 1-10 Science:', { size: 11, anchor: 'start' }) + T(234, 76, 'water cycle English: Chapter 5', { size: 11, anchor: 'start' }) + T(234, 88, 'answer the questions and read', { size: 11, anchor: 'start' }) + T(234, 100, 'all notes before the class test', { size: 11, anchor: 'start' });
    s += faint(bad, 0.5);
    s += T(329, 190, 'tiny, crowded, no spacing', { size: 11, cls: 't-mut' });
    s += K.line(222, 150, 436, 150, { cls: 's-mut', dash: '3 3' });
    return K.svg(440, 208, s, { title: 'Readable fonts with spacing versus tiny crowded text' });
  });

  D.register('xii1.colourblind', () => {
    let s = '';
    s += K.rect(4, 6, 214, 200, { c: null, r: 10 }) + T(111, 26, 'Colour only', { size: 14, w: 'b', cls: 't-red' });
    s += K.rect(14, 38, 194, 120, { c: 6, r: 6 });
    s += K.polyline([[30, 140], [30, 90], [100, 90], [100, 56], [190, 56]], { cls: 's-red', w: 5 });
    s += K.polyline([[30, 140], [120, 140], [120, 100], [190, 100]], { cls: 's-grn', w: 5 });
    s += K.circle(30, 140, 6, { c: null }) + K.circle(190, 56, 6, { c: null }) + K.circle(190, 100, 6, { c: null });
    s += T(111, 182, 'which route is which?', { size: 12, cls: 't-mut' });
    s += K.rect(222, 6, 214, 200, { c: null, r: 10 }) + T(329, 26, 'Colour + label + pattern', { size: 14, w: 'b', cls: 't-grn' });
    s += K.rect(232, 38, 194, 120, { c: 6, r: 6 });
    s += K.polyline([[248, 140], [248, 90], [318, 90], [318, 56], [408, 56]], { cls: 's-red', w: 5 });
    s += K.polyline([[248, 140], [338, 140], [338, 100], [408, 100]], { cls: 's-grn', w: 5, dash: '9 5' });
    s += K.box(326, 44, 56, 18, 'Route A', { c: 4, size: 11, r: 4 }) + K.box(346, 108, 56, 18, 'Route B', { c: 4, size: 11, r: 4 });
    s += K.circle(248, 140, 6, { c: null }) + K.circle(408, 56, 6, { c: null }) + K.circle(408, 100, 6, { c: null });
    s += T(329, 182, 'solid vs dashed + text labels', { size: 12, cls: 't-mut' });
    return K.svg(440, 212, s, { title: 'Map with colour-only routes versus routes with labels and line patterns' });
  });

  D.register('xii1.palette', () => {
    let s = '';
    s += T(220, 20, 'Colour + shape + label  =  safe for everyone', { size: 14, w: 'b' });
    const sw = [
      ['Present', 5, 'circle'],
      ['Absent', 3, 'square'],
      ['Late', 4, 'tri'],
      ['Leave', 1, 'diamond'],
    ];
    sw.forEach((c, i) => {
      const cx = 56 + i * 110;
      s += K.rect(cx - 50, 36, 100, 112, { c: null, r: 10 });
      if (c[2] === 'circle') s += K.circle(cx, 72, 20, { c: c[1] }) + tick(cx, 72, 9);
      if (c[2] === 'square') s += K.rect(cx - 20, 52, 40, 40, { c: c[1], r: 4 }) + cross(cx, 72, 9);
      if (c[2] === 'tri') s += K.poly([[cx, 50], [cx + 23, 92], [cx - 23, 92]], { c: c[1] }) + T(cx, 79, '!', { size: 16, w: 'b' });
      if (c[2] === 'diamond') s += K.poly([[cx, 50], [cx + 22, 72], [cx, 94], [cx - 22, 72]], { c: c[1] }) + T(cx, 72, 'L', { size: 13, w: 'b', vmid: true });
      s += T(cx, 120, c[0], { size: 13, w: 'b' }) + T(cx, 138, ['green', 'red', 'amber', 'blue'][i] + ' + ' + c[2].replace('tri', 'triangle'), { size: 11, cls: 't-mut' });
    });
    s += K.rect(6, 162, 428, 42, { c: 6, r: 8 });
    ['c1', 'c7', 'c2', 'c4'].forEach((k, i) => {
      s += K.rect(18 + i * 40, 172, 32, 22, { c: +k[1], r: 4 });
    });
    s += T(188, 188, 'vary lightness, add symbols or text', { size: 11, cls: 't-mut', anchor: 'start' });
    return K.svg(440, 212, s, { title: 'Colour-blind friendly status chips that combine colour, shape and a text label' });
  });

  D.register('xii1.inclusive-nav', () => {
    let s = '';
    s += K.rect(100, 6, 336, 196, { c: null, r: 10 }) + K.rect(100, 6, 336, 12, { c: 6, r: 6 });
    const nav = [['Home', 112, 52], ['Destinations', 168, 98], ['Tours', 270, 52], ['Contact Us', 326, 84]];
    nav.forEach((n, i) => {
      s += K.rect(n[1], 30, n[2], 26, { c: i === 1 ? 4 : 0, r: 5, cls: i === 1 ? 's-acc' : '' });
      s += T(n[1] + n[2] / 2, 47, n[0], { size: 11, w: i === 1 ? 'b' : '' });
    });
    s += K.rect(164, 26, 106, 34, { c: null, r: 8, cls: 's-brand' });
    s += K.box(196, 86, 140, 38, 'Book Now', { c: 7, size: 14, bold: true, r: 8 });
    [['Audio Guide', 112], ['Screen Reader', 214], ['Text to Speech', 316]].forEach((b) => {
      s += K.box(b[1], 146, 98, 28, b[0], { c: 1, size: 11, r: 14 });
    });
    s += T(268, 194, 'Tab key moves focus to each option', { size: 11, cls: 't-mut' });
    s += K.rect(6, 30, 80, 46, { c: 6, r: 8 }) + T(46, 53, 'Tab', { size: 15, w: 'b', vmid: true });
    s += K.rect(6, 92, 80, 46, { c: 6, r: 8 }) + T(46, 115, 'Enter', { size: 15, w: 'b', vmid: true });
    s += K.line(46, 78, 46, 90, { cls: 's-mut' });
    s += T(46, 164, 'keyboard only,', { size: 11, cls: 't-mut' }) + T(46, 178, 'no mouse needed', { size: 11, cls: 't-mut' });
    return K.svg(440, 208, s, { title: 'Inclusive navigation: keyboard Tab focus, audio guide, screen reader and text to speech' });
  });

  D.register('xii1.multimodal', () => {
    let s = '';
    s += K.box(160, 6, 120, 34, 'Important alert', { c: 4, size: 13, bold: true, r: 17 });
    const tiles = [
      ['Sight', 'captions for hearing-\nimpaired students', 1],
      ['Sound', 'voice or audio\nannouncement', 0],
      ['Touch', 'phone vibrates to\nalert the user', 7],
    ];
    tiles.forEach((t, i) => {
      const x = 4 + i * 146;
      s += K.line(220, 40, x + 69, 66, { arrow: true, cls: 's-mut' });
      s += K.rect(x, 68, 138, 140, { c: t[2] });
      s += T(x + 69, 88, t[0], { size: 14, w: 'b' });
      s += T(x + 69, 180, t[1], { size: 11, cls: 't-mut', lh: 14 });
    });
    s += K.rect(18, 98, 110, 56, { c: null, r: 4 }) + K.rect(26, 134, 94, 14, { c: 6, r: 2 }) + T(73, 142, 'Captions on', { size: 11, vmid: true }) + K.poly([[60, 108], [60, 124], [74, 116]], { c: 0 });
    s += K.rect(184, 114, 14, 22, { c: 6, r: 3 }) + K.poly([[198, 114], [214, 104], [214, 146], [198, 136]], { c: 6 });
    s += K.path('M224 112 Q234 125 224 138', { cls: 's-acc', w: 2.4 }) + K.path('M232 106 Q248 125 232 144', { cls: 's-acc', w: 2.4 });
    s += phone(344, 96, 50, 66, null) + K.path('M334 114 L328 124 L334 134', { cls: 's-acc', w: 2.4 }) + K.path('M404 114 L410 124 L404 134', { cls: 's-acc', w: 2.4 });
    return K.svg(440, 214, s, { title: 'Multimodal accessibility: information through sight, sound and touch' });
  });

  /* ---------- Lecture 5 ---------- */

  D.register('xii1.need-steps', () => {
    let s = '';
    const st = [
      ['Identify the users', 'who will use the system?', 1],
      ['Information collection', 'interviews, questionnaires, observations, surveys', 0],
      ['Analyze user needs', 'identify problems, goals and requirements', 2],
      ['Prioritize needs', 'decide which needs are most important', 4],
      ['Develop solutions', 'design a system that meets those needs', 5],
    ];
    st.forEach((t, i) => {
      const y = 6 + i * 62;
      if (i < 4) s += K.line(26, y + 42, 26, y + 68, { arrow: true, cls: 's-mut' });
      s += K.rect(56, y, 378, 50, { c: t[2] });
      s += K.circle(26, y + 25, 17, { c: t[2] }) + T(26, y + 25, String(i + 1), { size: 15, w: 'b', vmid: true });
      s += T(70, y + 21, t[0], { size: 14, w: 'b', anchor: 'start' }) + T(70, y + 39, t[1], { size: 11.5, cls: 't-mut', anchor: 'start' });
    });
    return K.svg(440, 320, s, { title: 'Five steps of need analysis' });
  });

  D.register('xii1.clutter', () => {
    let s = '';
    s += phone(8, 6, 200, 280, null) + T(108, 36, 'Too many options', { size: 12, w: 'b', cls: 't-red' });
    const names = ['Deals', 'Men', 'Women', 'Kids', 'Home', 'Toys', 'Sale', 'Cart', 'Help', 'Ads', 'New', 'Gift', 'Tech', 'Food', 'Auto', 'Pets', 'Book', 'Tools'];
    names.forEach((n, i) => {
      const x = 18 + (i % 3) * 61;
      const y = 48 + Math.floor(i / 3) * 24;
      s += K.rect(x, y, 56, 20, { c: [0, 1, 2, 3, 4, 5][i % 6], r: 4 }) + T(x + 28, y + 14, n, { size: 11 });
    });
    s += K.rect(18, 196, 172, 22, { c: 3, r: 4 }) + T(104, 211, 'BIG SALE  -  50% OFF!!', { size: 11, w: 'b' });
    s += K.rect(18, 224, 100, 20, { c: 6, r: 4 }) + T(68, 238, 'Checkout', { size: 11 });
    s += K.rect(124, 224, 66, 20, { c: 4, r: 4 }) + T(157, 238, 'Offer', { size: 11 });
    s += K.rect(18, 250, 172, 24, { c: 7, r: 4 }) + T(104, 266, 'Download our app now', { size: 11 });
    s += phone(232, 6, 200, 280, null) + T(332, 36, 'Clear layout', { size: 12, w: 'b', cls: 't-grn' });
    s += K.rect(246, 48, 172, 26, { c: null, r: 13 }) + T(332, 66, 'Search products', { size: 12, cls: 't-mut' });
    s += K.rect(246, 86, 172, 90, { c: 6, r: 6 }) + K.line(246, 86, 418, 176, { cls: 's-mut' }) + K.line(418, 86, 246, 176, { cls: 's-mut' });
    s += T(332, 196, 'Cotton Kurta  -  Rs 2,500', { size: 12 });
    s += K.box(246, 214, 172, 42, 'Checkout', { c: 5, size: 15, bold: true, r: 8 });
    return K.svg(440, 292, s, { title: 'Cluttered shopping screen versus clear layout with an obvious checkout button' });
  });

  D.register('xii1.problems', () => {
    const items = [
      ['Interface Complexity', 'too many menus, checkout hidden'],
      ['Poor Feedback', 'form freezes, no "sent" message'],
      ['Inconsistency', 'two different icons for search'],
      ['Accessibility Gaps', 'no captions, poor contrast'],
      ['Compatibility Issues', 'bank site crashes on mobile'],
      ['Contextual Neglect', 'no low-light mode at night'],
      ['High Cognitive Load', 'must remember many codes'],
      ['Lack of Testing', 'never tried on older phones'],
      ['Navigation Barriers', 'forms buried in unclear menus'],
      ['Trust Deficiency', 'no security badge or message'],
    ];
    return K.svg(440, 4 + 5 * 58, cardGrid(items, { h: 52, colors: [3, 7, 4, 3, 7, 4, 3, 7, 4, 3] }), { title: 'Ten common HCI problems with examples' });
  });

  /* ---------- Lecture 6 ---------- */

  D.register('xii1.improve-methods', () => {
    const items = [
      ['Enhance Usability', 'clear "Buy Now" button'],
      ['Strengthen Accessibility', 'captions on videos'],
      ['Ensure Consistency', 'same "Save" button everywhere'],
      ['Provide Clear Feedback', '"Payment Successful" message'],
      ['Improve Adaptability', 'site fits mobile, slow internet'],
      ['Apply User-Centered Design', 'pilot test before full release'],
      ['Use Multimodal Interaction', 'smart home with voice commands'],
      ['Continuous Testing', 'update app after user feedback'],
    ];
    return K.svg(440, 4 + 4 * 58, cardGrid(items, { h: 52, colors: [0, 1, 2, 5] }), { title: 'Eight methods for improving HCI with examples' });
  });

  D.register('xii1.ui-mockup', () => {
    let s = '';
    s += phone(150, 6, 140, 376, null);
    s += K.rect(158, 24, 124, 26, { c: 0, r: 6 });
    [0, 1, 2].forEach((i) => (s += K.line(168, 31 + i * 6, 182, 31 + i * 6, { w: 2.2 })));
    s += T(232, 41, 'MyApp', { size: 12, w: 'b' });
    s += K.rect(158, 58, 124, 66, { c: 6, r: 6 }) + K.line(158, 58, 282, 124, { cls: 's-mut' }) + K.line(282, 58, 158, 124, { cls: 's-mut' });
    s += T(162, 142, 'Name', { size: 11, cls: 't-mut', anchor: 'start' });
    s += K.rect(158, 148, 124, 26, { c: null, r: 5 }) + T(166, 165, 'Ali Khan', { size: 12, anchor: 'start' }) + K.line(224, 153, 224, 169, { cls: 's-brand', w: 2 });
    s += K.rect(160, 186, 14, 14, { c: null, r: 3 }) + tick(167, 193, 4) + T(180, 198, 'Remember me', { size: 11, anchor: 'start' });
    s += K.box(158, 212, 124, 32, 'Submit', { c: 0, size: 14, bold: true, r: 8 });
    [178, 208, 238, 268].forEach((cx, i) => {
      s += K.circle(cx, 274, 11, { c: [1, 2, 3, 4][i] });
    });
    s += K.rect(150, 340, 140, 42, { c: 4, r: 14 }) + T(176, 366, 'Home', { size: 11, w: 'b' }) + T(220, 366, 'Search', { size: 11 }) + T(262, 366, 'Profile', { size: 11 });
    s += K.rect(160, 346, 32, 4, { c: null, r: 2, cls: 'f-brand' });
    const lab = (side, y, ty, txt) => {
      if (side === 'l') return T(112, ty + 4, txt, { size: 12, w: 'b', anchor: 'end' }) + K.line(118, ty, 168, y, { arrow: true, cls: 's-brand' });
      return T(328, ty + 4, txt, { size: 12, w: 'b', anchor: 'start' }) + K.line(322, ty, 288, y, { arrow: true, cls: 's-brand' });
    };
    s += lab('l', 36, 24, 'Menu');
    s += lab('l', 90, 90, 'Image / graphic');
    s += lab('l', 162, 162, 'Text field');
    s += lab('l', 194, 206, 'Check box');
    s += lab('r', 228, 228, 'Button');
    s += lab('r', 274, 274, 'Icons');
    s += lab('r', 360, 360, 'Navigation bar');
    return K.svg(440, 388, s, { title: 'A mobile screen mock-up with menu, image, text field, check box, button, icons and navigation bar' });
  });

  D.register('xii1.ui-controls', () => {
    let s = '';
    const panel = (x, y, c, title, sub) => K.rect(x, y, 212, 100, { c: c }) + T(x + 106, y + 20, title, { size: 13, w: 'b' }) + T(x + 106, y + 92, sub, { size: 11, cls: 't-mut' });
    s += panel(4, 4, 0, 'Check boxes', 'select one or more options');
    [['Maths', 1], ['Physics', 1], ['Chemistry', 0]].forEach((o, i) => {
      s += K.rect(30, 32 + i * 18, 12, 12, { c: null, r: 2 }) + (o[1] ? tick(36, 38 + i * 18, 4) : '') + T(50, 43 + i * 18, o[0], { size: 12, anchor: 'start' });
    });
    s += panel(224, 4, 1, 'Radio buttons', 'select only one option');
    [['Beginner', 0], ['Intermediate', 1], ['Expert', 0]].forEach((o, i) => {
      s += K.circle(256, 38 + i * 18, 6, { c: null }) + (o[1] ? K.circle(256, 38 + i * 18, 3, { c: null, cls: 'f-ink' }) : '') + T(268, 43 + i * 18, o[0], { size: 12, anchor: 'start' });
    });
    s += panel(4, 110, 2, 'Slider', 'adjust volume or brightness');
    s += K.line(30, 160, 186, 160, { cls: 's-mut', w: 4 }) + K.line(30, 160, 120, 160, { cls: 's-brand', w: 4 }) + K.circle(120, 160, 9, { c: 4 });
    s += panel(224, 110, 4, 'Navigation bar', 'move between pages');
    s += K.rect(240, 150, 180, 34, { c: null, r: 12 });
    ['Home', 'Search', 'Profile'].forEach((l, i) => {
      s += T(270 + i * 60, 172, l, { size: 11, w: i === 0 ? 'b' : '' });
    });
    s += K.rect(252, 177, 36, 4, { c: null, r: 2, cls: 'f-brand' });
    return K.svg(440, 216, s, { title: 'More UI components: check boxes, radio buttons, slider and navigation bar' });
  });

  /* ---------- Lecture 7 ---------- */

  D.register('xii1.ux-journey', () => {
    let s = '';
    const st = [
      ['App opens\nquickly', 0, 10, 10],
      ['Menu is easy\nto browse', 1, 155, 10],
      ['Restaurants are\nsearched easily', 2, 300, 10],
      ['Payment\nis secure', 4, 300, 124],
      ['Order tracked\nin real time', 7, 155, 124],
    ];
    st.forEach((t, i) => {
      s += K.rect(t[2], t[3], 130, 78, { c: t[1] }) + K.circle(t[2] + 18, t[3] + 18, 12, { c: null }) + T(t[2] + 18, t[3] + 18, String(i + 1), { size: 13, w: 'b', vmid: true });
      s += T(t[2] + 65, t[3] + 46, t[0], { size: 12, lh: 15 });
    });
    s += K.line(142, 49, 153, 49, { arrow: true, cls: 's-mut' }) + K.line(287, 49, 298, 49, { arrow: true, cls: 's-mut' });
    s += K.line(365, 90, 365, 122, { arrow: true, cls: 's-mut' });
    s += K.line(298, 163, 287, 163, { arrow: true, cls: 's-mut' });
    s += K.line(153, 163, 142, 163, { arrow: true, cls: 's-mut' });
    s += K.rect(10, 124, 130, 78, { c: 5 }) + K.circle(75, 152, 18, { c: 4 }) + K.circle(68, 148, 2.5, { c: null, cls: 'f-ink' }) + K.circle(82, 148, 2.5, { c: null, cls: 'f-ink' }) + K.path('M65 158 Q75 168 85 158', { w: 2 });
    s += T(75, 192, 'Smooth, satisfying', { size: 11, w: 'b' });
    s += T(220, 220, 'User Experience of a Food Delivery App', { size: 12, cls: 't-mut' });
    return K.svg(440, 228, s, { title: 'User experience journey of ordering dinner in a food delivery app' });
  });

  const lowPhone = (x, y, mode) => {
    // mode: 0 low, 1 mid, 2 high
    let s = phone(x, y, 128, 232, mode === 2 ? 0 : null);
    const lowImg = (px, py, pw, ph) => K.rect(px, py, pw, ph, { c: mode === 2 ? 3 : mode === 1 ? 6 : null, r: 4 }) + (mode < 2 ? K.line(px, py, px + pw, py + ph, { cls: 's-mut' }) + K.line(px + pw, py, px, py + ph, { cls: 's-mut' }) : '');
    s += lowImg(x + 44, y + 22, 40, 40);
    if (mode === 0) s += K.line(x + 34, y + 76, x + 94, y + 76, { cls: 's-mut', w: 3 });
    if (mode === 1) s += T(x + 64, y + 78, 'App title', { size: 11, cls: 't-mut' });
    if (mode === 2) s += T(x + 64, y + 79, 'EduLearn', { size: 14, w: 'b' });
    const field = (fy, label) => {
      let o = K.rect(x + 14, fy, 100, 24, { c: mode === 2 ? null : mode === 1 ? 6 : null, r: mode === 2 ? 12 : 3 });
      if (mode === 0) o += K.line(x + 22, fy + 12, x + 56, fy + 12, { cls: 's-mut', w: 2 });
      else o += T(x + 24, fy + 16, label, { size: 11, anchor: 'start', cls: 't-mut' });
      return o;
    };
    s += field(y + 96, 'Username') + field(y + 128, 'Password');
    s += K.rect(x + 14, y + 166, 100, 28, { c: mode === 2 ? 0 : mode === 1 ? 6 : null, r: mode === 2 ? 14 : 3 });
    if (mode === 0) s += K.line(x + 44, y + 180, x + 84, y + 180, { cls: 's-mut', w: 3 });
    else s += T(x + 64, y + 184, 'Login', { size: 12, w: 'b' });
    s += mode === 0 ? K.line(x + 34, y + 210, x + 94, y + 210, { cls: 's-mut', w: 2 }) : T(x + 64, y + 214, 'Forgot password?', { size: 11, cls: mode === 2 ? 't-acc' : 't-mut' });
    return s;
  };

  D.register('xii1.fidelity', () => {
    let s = '';
    s += lowPhone(8, 34, 0) + lowPhone(156, 34, 1) + lowPhone(304, 34, 2);
    ['Low-fidelity', 'Mid (extra)', 'High-fidelity'].forEach((t, i) => {
      s += T(72 + i * 148, 18, t, { size: 13, w: 'b' });
    });
    ['black & white sketch', 'shapes + real labels', 'colours, images, fonts'].forEach((t, i) => {
      s += T(72 + i * 148, 286, t, { size: 11, cls: 't-mut' });
    });
    s += K.line(138, 150, 154, 150, { arrow: true, cls: 's-brand', w: 2 }) + K.line(286, 150, 302, 150, { arrow: true, cls: 's-brand', w: 2 });
    s += T(220, 306, 'early, quick, cheap  ->  looks like the final product', { size: 12, cls: 't-acc' });
    return K.svg(440, 316, s, { title: 'Same login screen drawn as low-fidelity, mid-fidelity and high-fidelity wireframes' });
  });

  D.register('xii1.login-wireframe', () => {
    let s = '';
    s += T(220, 18, 'Low-fidelity wireframe: Login screen', { size: 13, w: 'b' });
    s += phone(130, 28, 180, 300, null);
    s += K.rect(190, 52, 60, 52, { c: 6, r: 4 }) + K.line(190, 52, 250, 104, { cls: 's-mut' }) + K.line(250, 52, 190, 104, { cls: 's-mut' });
    s += K.line(170, 124, 270, 124, { cls: 's-mut', w: 4 });
    s += K.rect(150, 148, 140, 30, { c: null, r: 3 }) + K.line(160, 163, 205, 163, { cls: 's-mut', w: 2 });
    s += K.rect(150, 190, 140, 30, { c: null, r: 3 }) + K.line(160, 205, 205, 205, { cls: 's-mut', w: 2 });
    s += K.rect(150, 238, 140, 34, { c: null, r: 3 }) + K.line(195, 255, 245, 255, { cls: 's-mut', w: 3 });
    s += K.line(180, 290, 260, 290, { cls: 's-mut', w: 2 }) + K.line(165, 308, 275, 308, { cls: 's-mut', w: 2 });
    const lab = (side, y, ty, txt) =>
      side === 'l'
        ? T(116, ty + 4, txt, { size: 12, w: 'b', anchor: 'end', lh: 14 }) + K.line(122, ty, 150, y, { arrow: true, cls: 's-brand' })
        : T(324, ty + 4, txt, { size: 12, w: 'b', anchor: 'start', lh: 14 }) + K.line(318, ty, 292, y, { arrow: true, cls: 's-brand' });
    s += lab('l', 78, 78, 'Logo box\n(X = image)');
    s += lab('l', 124, 124, 'Title line');
    s += lab('r', 163, 150, 'Text boxes:\nrectangle + line');
    s += lab('r', 255, 255, 'Button:\nrectangle');
    s += lab('l', 290, 290, 'Link line');
    return K.svg(440, 336, s, { title: 'Low-fidelity login screen wireframe with labelled parts' });
  });

  D.register('xii1.design-loop', () => {
    let s = '';
    const bx = (x, y, n, t, sub, c) => K.rect(x, y, 150, 62, { c: c }) + K.circle(x + 18, y + 18, 11, { c: null }) + T(x + 18, y + 18, String(n), { size: 12, w: 'b', vmid: true }) + T(x + 86, y + 24, t, { size: 13, w: 'b' }) + T(x + 75, y + 46, sub, { size: 11, cls: 't-mut' });
    s += bx(20, 16, 1, 'Design', 'sketch the idea', 1) + bx(270, 16, 2, 'Prototype', 'interactive model', 0) + bx(270, 136, 3, 'User Testing', 'teachers and students', 4) + bx(20, 136, 4, 'Feedback', 'collect and improve', 7);
    s += K.line(172, 47, 268, 47, { arrow: true, cls: 's-brand', w: 2.2 }) + K.line(345, 80, 345, 134, { arrow: true, cls: 's-brand', w: 2.2 }) + K.line(268, 167, 172, 167, { arrow: true, cls: 's-brand', w: 2.2 }) + K.line(95, 134, 95, 80, { arrow: true, cls: 's-brand', w: 2.2 });
    s += T(220, 112, 'repeat until', { size: 12, cls: 't-acc' }) + T(220, 127, 'users are happy', { size: 12, cls: 't-acc' });
    s += K.rect(110, 236, 220, 44, { c: 5 }) + T(220, 263, '5  Final app developed', { size: 14, w: 'b' });
    s += K.polyline([[95, 200], [95, 258], [108, 258]], { cls: 's-grn', w: 2.2, arrow: true });
    s += T(100, 222, 'after successful testing', { size: 11, cls: 't-grn', anchor: 'start' });
    return K.svg(440, 290, s, { title: 'Prototype and UX design loop: design, prototype, user testing, feedback, then final app' });
  });

  /* ---------- Lecture 8 ---------- */

  D.register('xii1.figma-layout', () => {
    let s = '';
    s += K.rect(4, 4, 432, 34, { c: 6, r: 6 });
    ['Move', 'Frame (F)', 'Shape', 'Pen', 'Text', 'Hand'].forEach((t, i) => {
      s += T(40 + i * 68, 25, t, { size: 11, w: i === 1 ? 'b' : '', cls: i === 1 ? 't-acc' : '' });
    });
    s += K.rect(4, 44, 106, 244, { c: 1, r: 6 }) + T(57, 62, 'Layers', { size: 13, w: 'b' });
    ['Page 1', 'iPhone 17-1', 'iPhone 17-2', 'Frame 1'].forEach((t, i) => {
      s += T(14, 88 + i * 24, t, { size: 11, anchor: 'start', w: i === 1 ? 'b' : '' });
    });
    s += K.rect(116, 44, 208, 244, { c: 6, r: 6 }) + T(220, 62, 'Canvas', { size: 13, w: 'b' });
    s += T(160, 84, 'iPhone 17-1', { size: 11, cls: 't-acc' }) + T(266, 84, 'iPhone 17-2', { size: 11, cls: 't-mut' });
    s += K.rect(126, 92, 68, 180, { c: null, r: 3, cls: 's-brand' }) + K.rect(238, 92, 56, 180, { c: null, r: 3 });
    [[126, 92], [194, 92], [126, 272], [194, 272]].forEach((p) => (s += K.rect(p[0] - 3, p[1] - 3, 7, 7, { c: null, r: 1, cls: 's-brand' })));
    s += K.rect(330, 44, 106, 244, { c: 2, r: 6 }) + T(383, 62, 'Properties', { size: 13, w: 'b' });
    s += T(362, 84, 'Design', { size: 11, w: 'b' }) + T(406, 84, 'Prototype', { size: 11, cls: 't-mut' });
    ['W / H', 'X / Y', 'Alignment', 'Fill', 'Stroke', 'Effects'].forEach((t, i) => {
      s += K.rect(342, 94 + i * 30, 82, 22, { c: null, r: 4 }) + T(383, 109 + i * 30, t, { size: 11 });
    });
    s += T(57, 304, 'Layers', { size: 11, cls: 't-mut' }) + T(220, 304, 'Canvas', { size: 11, cls: 't-mut' }) + T(383, 304, 'Properties panel', { size: 11, cls: 't-mut' });
    return K.svg(440, 312, s, { title: 'Figma interface sketch: toolbar, layers panel, canvas with two frames and properties panel' });
  });

  D.register('xii1.frame-steps', () => {
    let s = '';
    const st = [
      ['Open Figma, create or open a file', 0],
      ['Select the Frame tool (or press F)', 1],
      ['Click and drag on the canvas to draw a frame', 2],
      ['Adjust size and position in the right panel (optional)', 4],
      ['Change fill, stroke or effects (optional)', 4],
      ['Add text, shapes, images or components inside', 5],
      ['Duplicate or create more frames (optional)', 4],
      ['Your frame is ready to use in your design!', 5],
    ];
    st.forEach((t, i) => {
      const y = 4 + i * 40;
      const opt = t[0].indexOf('optional') >= 0;
      s += K.rect(40, y, 394, 34, { c: t[1], r: 8, dash: opt ? '5 4' : '' });
      s += K.circle(20, y + 17, 14, { c: t[1] }) + T(20, y + 17, String(i + 1), { size: 13, w: 'b', vmid: true });
      s += T(52, y + 22, t[0], { size: 12, anchor: 'start', w: i === 7 ? 'b' : '' });
    });
    return K.svg(440, 328, s, { title: 'Steps to add a frame in Figma' });
  });

  D.register('xii1.signup-frame', () => {
    let s = '';
    s += phone(140, 6, 160, 322, null) + K.rect(152, 22, 136, 296, { c: null, r: 6, dash: '3 3', cls: 's-mut' });
    s += T(220, 50, 'E-Tutorial of Human\nComputer Interaction', { size: 12, w: 'b', lh: 15 });
    s += K.rect(176, 84, 88, 56, { c: 0, r: 6 }) + K.rect(190, 96, 46, 28, { c: null, r: 3 }) + K.circle(250, 116, 8, { c: 4 }) + K.rect(188, 126, 50, 6, { c: 6, r: 2 });
    s += K.rect(176, 160, 88, 6, { c: 6, r: 2 });
    s += K.box(172, 252, 96, 34, 'Sign-up', { c: 1, size: 14, bold: true, r: 17 });
    s += T(220, 308, 'white background', { size: 11, cls: 't-mut' });
    const note = (side, y, ty, txt) =>
      side === 'l'
        ? T(130, ty, txt, { size: 11, anchor: 'end', lh: 13, cls: '' }) + K.line(134, y, y < 60 ? 150 : 172, y, { arrow: true, cls: 's-brand' })
        : T(312, ty, txt, { size: 11, anchor: 'start', lh: 13, cls: '' }) + K.line(308, y, y > 250 ? 270 : 290, y, { arrow: true, cls: 's-brand' });
    s += note('l', 46, 24, 'Title: bold sans-serif\nInter or Roboto, 24 pt');
    s += note('l', 112, 100, 'Illustration:\nperson at a computer');
    s += note('r', 269, 240, 'Call-to-action button\nrounded, radius 30 px\nsky-blue or royal-blue');
    s += note('r', 190, 176, 'About 20 px padding\non every side');
    return K.svg(440, 334, s, { title: 'E-Tutorial sign-up frame: title, illustration, rounded call-to-action button and padding' });
  });

  D.register('xii1.prototype-link', () => {
    let s = '';
    s += phone(20, 8, 130, 214, null) + T(85, 36, 'Student Sign Up', { size: 11, w: 'b' });
    s += K.rect(34, 52, 102, 22, { c: null, r: 4 }) + T(42, 67, 'Full name', { size: 11, anchor: 'start', cls: 't-mut' });
    s += K.rect(34, 82, 102, 22, { c: null, r: 4 }) + T(42, 97, 'Email', { size: 11, anchor: 'start', cls: 't-mut' });
    s += K.rect(34, 112, 102, 22, { c: null, r: 4 }) + T(42, 127, 'Password', { size: 11, anchor: 'start', cls: 't-mut' });
    s += K.box(34, 152, 102, 30, 'Sign Up', { c: 1, size: 13, bold: true, r: 15 });
    s += T(85, 206, 'Frame 1', { size: 11, cls: 't-mut' });
    s += phone(290, 8, 130, 214, null) + T(355, 36, 'Welcome, Alex!', { size: 11, w: 'b' });
    s += K.circle(355, 72, 18, { c: 0 }) + T(355, 108, 'Name: Alex', { size: 11 }) + T(355, 126, 'Batch: 2025', { size: 11 }) + T(355, 144, 'Role: Student', { size: 11 });
    s += K.box(318, 160, 74, 24, 'Sign Out', { c: 6, size: 11, r: 12 });
    s += T(355, 206, 'Frame 2', { size: 11, cls: 't-mut' });
    s += K.line(138, 167, 290, 90, { arrow: true, cls: 's-grn', w: 2.6 });
    s += T(214, 112, 'on click:', { size: 12, cls: 't-grn', w: 'b' }) + T(214, 128, 'navigate to', { size: 12, cls: 't-grn', w: 'b' });
    s += K.circle(220, 34, 16, { c: 5 }) + K.poly([[215, 26], [215, 42], [229, 34]], { c: null, cls: 'f-ink' });
    s += T(220, 62, 'Present', { size: 11, cls: 't-mut' });
    s += T(220, 244, 'Prototype tab: link a button to the next frame, then Present', { size: 11, cls: 't-mut' });
    return K.svg(440, 252, s, { title: 'Linking the Sign Up button in frame 1 to the profile screen in frame 2 using the Prototype feature' });
  });

  /* ---------- Lecture 9 ---------- */

  D.register('xii1.eval-test-map', () => {
    let s = '';
    s += K.rect(4, 4, 212, 50, { c: 1 }) + T(110, 24, 'Evaluation', { size: 14, w: 'b' }) + T(110, 42, "does it meet users' needs?", { size: 11, cls: 't-mut' });
    s += K.rect(224, 4, 212, 50, { c: 0 }) + T(330, 24, 'Testing', { size: 14, w: 'b' }) + T(330, 42, 'does it work correctly?', { size: 11, cls: 't-mut' });
    ['User-centered methods', 'Formative studies', 'Summative evaluation', 'Expert reviews', 'Surveys & interviews', 'Accessibility evaluation'].forEach((t, i) => {
      s += K.box(4, 62 + i * 34, 212, 30, t, { c: null, size: 12, r: 15 });
    });
    ['Usability testing', 'Task-based testing', 'Automated audits', 'Keyboard & screen reader', 'Prototype testing', 'A/B testing', 'Compatibility testing', 'Performance & load'].forEach((t, i) => {
      s += K.box(224, 62 + i * 34, 212, 30, t, { c: null, size: 12, r: 15 });
    });
    s += T(110, 62 + 6 * 34 + 14, 'measured with SUS, NPS,', { size: 11, cls: 't-mut' }) + T(110, 62 + 6 * 34 + 28, 'task success rate', { size: 11, cls: 't-mut' });
    return K.svg(440, 62 + 8 * 34, s, { title: 'Evaluation methods and testing methods in HCI' });
  });

  D.register('xii1.usability-flow', () => {
    let s = '';
    const bx = (x, y, n, t, sub, c) => K.rect(x, y, 136, 76, { c: c }) + K.circle(x + 16, y + 16, 11, { c: null }) + T(x + 16, y + 16, String(n), { size: 12, w: 'b', vmid: true }) + T(x + 74, y + 26, t, { size: 12, w: 'b', lh: 14 }) + T(x + 68, y + 62, sub, { size: 11, cls: 't-mut' });
    s += bx(4, 6, 1, 'Choose\nreal users', 'target users', 1) + bx(152, 6, 2, 'Give realistic\ntasks', 'e.g. find a product', 0) + bx(300, 6, 3, 'Observe and\nmeasure', 'time, errors, success', 4);
    s += bx(300, 112, 4, 'Find the\nproblems', 'where users struggle', 7) + bx(152, 112, 5, 'Improve the\ndesign', 'fix and refine', 2) + bx(4, 112, 6, 'Test again', 'repeat the loop', 5);
    s += K.line(142, 44, 150, 44, { arrow: true, cls: 's-brand', w: 2 }) + K.line(290, 44, 298, 44, { arrow: true, cls: 's-brand', w: 2 });
    s += K.line(368, 84, 368, 110, { arrow: true, cls: 's-brand', w: 2 });
    s += K.line(298, 150, 290, 150, { arrow: true, cls: 's-brand', w: 2 }) + K.line(150, 150, 142, 150, { arrow: true, cls: 's-brand', w: 2 });
    s += K.polyline([[72, 110], [72, 100], [72, 86]], { cls: 's-brand', w: 2, arrow: true });
    ['Efficiency', 'Effectiveness', 'Satisfaction'].forEach((t, i) => {
      s += K.box(4 + i * 148, 214, 136, 28, t, { c: 6, size: 12, r: 14 });
    });
    s += T(220, 206, 'usability testing measures', { size: 11, cls: 't-mut' });
    return K.svg(440, 250, s, { title: 'Usability testing flow: choose users, give tasks, observe, find problems, improve, test again' });
  });

  D.register('xii1.ab-test', () => {
    let s = '';
    const scr = (x, label, c, btn) =>
      K.rect(x, 30, 120, 120, { c: null, r: 8 }) + T(x + 60, 22, label, { size: 13, w: 'b' }) + K.rect(x + 12, 42, 96, 40, { c: 6, r: 4 }) + K.line(x + 12, 96, x + 90, 96, { cls: 's-mut', w: 2 }) + K.box(x + 20, 114, 80, 26, btn, { c: c, size: 12, bold: true, r: 13 });
    s += scr(10, 'Version A', 1, 'Join');
    s += scr(150, 'Version B', 4, 'Sign up free');
    s += T(70, 172, '50% of users', { size: 11, cls: 't-mut' }) + T(210, 172, '50% of users', { size: 11, cls: 't-mut' });
    s += T(350, 22, 'Which performs better?', { size: 13, w: 'b' });
    s += T(290, 52, 'A', { size: 12, w: 'b' }) + K.rect(300, 40, 70, 18, { c: 1, r: 3 });
    s += T(290, 92, 'B', { size: 12, w: 'b' }) + K.rect(300, 80, 120, 18, { c: 4, r: 3 });
    s += T(360, 125, 'sign-ups (example)', { size: 11, cls: 't-mut' });
    s += K.line(284, 106, 430, 106, { cls: 's-mut', dash: '3 3' });
    s += K.box(284, 134, 148, 36, 'Keep the winner', { c: 5, size: 13, bold: true, r: 8 });
    return K.svg(440, 184, s, { title: 'A/B testing: two versions shown to different users and compared by real data' });
  });

  D.register('xii1.careers', () => {
    const items = [
      ['UX Designer', 'researches user needs, makes\nthe product intuitive'],
      ['UI Designer', 'visual layout: buttons, menus,\ncolours, typography'],
      ['Interaction Designer', 'flow between screens and\nactions: touch, voice, gesture'],
      ['Accessibility Specialist', 'products usable for diverse\nphysical, sensory, cognitive needs'],
      ['Usability Researcher / Tester', 'runs usability tests using\nSUS or NPS with real users'],
      ['Product Designer', 'combines UX, UI and business;\nuses tools like Figma'],
    ];
    return K.svg(440, 4 + 3 * 74, cardGrid(items, { h: 68, colors: [1, 5, 2, 3, 4, 0] }), { title: 'Six career opportunities in digital product design' });
  });

  D.register('xii1.attendance-wireframes', () => {
    let s = '';
    const ph = (i) => 6 + i * 108;
    const titles = ['1\nLogin', '2\nClass\nSelection', '3\nAttendance\nMarking', '4\nSubmit /\nConfirmation'];
    for (let i = 0; i < 4; i++) {
      const x = ph(i);
      s += phone(x, 8, 92, 190, null);
      s += T(x + 46, 226, titles[i], { size: 11, w: 'b', lh: 13 });
    }
    let x = ph(0);
    s += K.rect(x + 30, 28, 32, 28, { c: 6, r: 3 }) + K.line(x + 30, 28, x + 62, 56, { cls: 's-mut' }) + K.line(x + 62, 28, x + 30, 56, { cls: 's-mut' });
    s += K.rect(x + 12, 72, 68, 20, { c: null, r: 3 }) + K.rect(x + 12, 100, 68, 20, { c: null, r: 3 }) + K.rect(x + 16, 140, 60, 24, { c: null, r: 3 }) + K.line(x + 30, 152, x + 62, 152, { cls: 's-mut', w: 3 });
    x = ph(1);
    for (let r = 0; r < 4; r++) s += K.rect(x + 10, 30 + r * 30, 72, 24, { c: null, r: 3 }) + K.line(x + 18, 42 + r * 30, x + 56, 42 + r * 30, { cls: 's-mut', w: 2 });
    s += K.rect(x + 16, 156, 60, 26, { c: null, r: 3 });
    x = ph(2);
    for (let r = 0; r < 4; r++) s += K.rect(x + 12, 32 + r * 26, 12, 12, { c: null, r: 2 }) + (r % 2 === 0 ? tick(x + 18, 38 + r * 26, 3.5) : '') + K.line(x + 32, 38 + r * 26, x + 78, 38 + r * 26, { cls: 's-mut', w: 2 });
    s += K.rect(x + 16, 152, 60, 28, { c: null, r: 3 }) + K.line(x + 30, 166, x + 62, 166, { cls: 's-mut', w: 3 });
    x = ph(3);
    s += K.circle(x + 46, 80, 26, { c: null }) + tick(x + 46, 80, 12, 's-mut') + K.line(x + 22, 130, x + 70, 130, { cls: 's-mut', w: 3 }) + K.line(x + 28, 146, x + 64, 146, { cls: 's-mut', w: 2 });
    for (let i = 0; i < 3; i++) s += K.line(ph(i) + 94, 104, ph(i) + 112, 104, { arrow: true, cls: 's-brand', w: 2 });
    return K.svg(440, 270, s, { title: 'Four low-fidelity screens of a college attendance app: login, class selection, attendance marking, confirmation' });
  });
})();
