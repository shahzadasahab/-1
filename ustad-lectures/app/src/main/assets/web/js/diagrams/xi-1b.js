/* XI Ch1 Part B & C (SDLC and Communication Models) diagrams */
(function () {
  const D = Diagrams;
  const T = (x, y, s, o) => K.text(x, y, s, o);
  const ARR = (x1, y1, x2, y2, o) => K.line(x1, y1, x2, y2, Object.assign({ arrow: true }, o || {}));
  const PH = [1, 0, 5, 4, 2, 3];
  const OL = { 7: 1, 6: 2, 5: 3, 4: 4, 3: 5, 2: 0, 1: 7 };
  const ON = { 7: 'Application', 6: 'Presentation', 5: 'Session', 4: 'Transport', 3: 'Network', 2: 'Data Link', 1: 'Physical' };
  const UNIT = { 7: 'Data', 6: 'Data', 5: 'Data', 4: 'Segment', 3: 'Packet', 2: 'Frame', 1: 'Bits' };

  function card(x, y, w, h, c, title, sub, o) {
    o = o || {};
    const ts = o.ts || 13;
    const ss = o.ss || 11;
    let s = K.rect(x, y, w, h, { c, r: o.r == null ? 8 : o.r, s: o.s, dash: o.dash, cls: o.cls });
    const tl = String(title).split('\n').length;
    if (sub) {
      const sl = String(sub).split('\n').length;
      const th = ts * 1.25 * tl;
      const sh = ss * 1.25 * sl;
      const top = y + (h - th - 3 - sh) / 2;
      s += T(x + w / 2, top + ts * 0.95, title, { size: ts, w: 'b' });
      s += T(x + w / 2, top + th + 3 + ss * 0.95, sub, { size: ss, cls: o.scls || 't-mut' });
    } else {
      s += T(x + w / 2, y + h / 2, title, { size: ts, w: 'b', vmid: true, cls: o.tcls });
    }
    return s;
  }

  function edge(a, b, hw, hh) {
    const dx = b[0] - a[0];
    const dy = b[1] - a[1];
    const t = Math.min(hw / (Math.abs(dx) || 1e-9), hh / (Math.abs(dy) || 1e-9));
    return [a[0] + dx * t, a[1] + dy * t];
  }
  function linkBoxes(a, b, hw, hh, gap, o) {
    const p = edge(a, b, hw + gap, hh + gap);
    const q = edge(b, a, hw + gap, hh + gap);
    return ARR(p[0], p[1], q[0], q[1], o);
  }

  function ringBoxes(nodes, o) {
    const cx = 220;
    const cy = o.cy;
    const rx = o.rx || 150;
    const ry = o.ry || 108;
    const bw = o.bw || 120;
    const bh = o.bh || 52;
    const pos = nodes.map((_, i) => {
      const a = ((-60 + 60 * i) * Math.PI) / 180;
      return [cx + rx * Math.cos(a), cy + ry * Math.sin(a)];
    });
    let s = '';
    pos.forEach((p, i) => {
      s += linkBoxes(p, pos[(i + 1) % nodes.length], bw / 2, bh / 2, 3);
    });
    nodes.forEach((n, i) => {
      s += card(pos[i][0] - bw / 2, pos[i][1] - bh / 2, bw, bh, n.c, n.t, n.sub, { ts: n.ts || 13 });
    });
    return s;
  }

  function chev(x, y, w, h, c, label, size) {
    const n = 10;
    let s = K.poly([[x, y], [x + w - n, y], [x + w, y + h / 2], [x + w - n, y + h], [x, y + h], [x + n, y + h / 2]], { c });
    s += T(x + w / 2 + 2, y + h / 2, label, { size: size || 11.5, vmid: true, w: 'b' });
    return s;
  }

  /* ---------- SDLC basics ---------- */
  D.register('xi1b.dev-activities', () => {
    const items = [
      ['1. Planning', 'what it should do\n(function)'],
      ['2. Designing', 'how it will work\n(algorithm)'],
      ['3. Coding', 'write the program\n(programming)'],
      ['4. Testing', 'find and fix bugs\n(debugging)'],
      ['5. Releasing', 'give it to users\n(deployment)'],
      ['6. Support', 'fix problems\nafter release'],
    ];
    let s = T(220, 20, 'Software development', { size: 15, w: 'b' });
    items.forEach(([a, b], i) => {
      s += card(6 + (i % 3) * 144, 34 + Math.floor(i / 3) * 86, 138, 76, PH[i], a, b, { ts: 14 });
    });
    s += K.rect(6, 210, 428, 34, { c: 6, r: 8, dash: '5 4' });
    s += T(220, 232, 'Like a house: plan, materials, workers, inspections', { size: 12.5 });
    return K.svg(440, 252, s, { title: 'Six activities of software development, compared to building a house' });
  });

  D.register('xi1b.sdlc-cycle', () => {
    const nodes = [
      ['1. Requirement', 'SRS Document'],
      ['2. Design', 'Design Document'],
      ['3. Implement', 'Working code'],
      ['4. Testing', 'Test reports'],
      ['5. Deployment', 'Live software'],
      ['6. Maintenance', 'Updates & patches'],
    ].map(([t, sub], i) => ({ t, sub, c: PH[i] }));
    let s = ringBoxes(nodes, { cy: 168, ry: 112 });
    s += K.circle(220, 168, 46, { c: 6 });
    s += T(220, 165, 'SDLC', { size: 17, w: 'b' });
    s += T(220, 183, 'Phases', { size: 12.5, cls: 't-mut' });
    s += T(220, 322, 'under each phase: its deliverable', { size: 11.5, cls: 't-mut' });
    return K.svg(440, 332, s, { title: 'SDLC cycle: six phases in a ring with their deliverables' });
  });

  D.register('xi1b.flowchart-login', () => {
    const cx = 180;
    let s = '';
    const para = (x, y, w, h, c, label) => K.poly([[x + 12, y], [x + w, y], [x + w - 12, y + h], [x, y + h]], { c }) + T(x + w / 2, y + h / 2, label, { size: 13, w: 'b', vmid: true });
    s += K.rect(cx - 45, 8, 90, 34, { r: 17, c: 3 }) + T(cx, 25, 'Start', { size: 14, w: 'b', vmid: true });
    s += ARR(cx, 42, cx, 64);
    s += para(cx - 80, 64, 160, 46, 1, 'Enter\nCredentials');
    s += ARR(cx, 110, cx, 132);
    s += K.box(cx - 90, 132, 180, 46, 'Compare with\nstored credentials', { c: 0, size: 13, bold: true });
    s += ARR(cx, 178, cx, 198);
    s += K.poly([[cx, 198], [cx + 56, 236], [cx, 274], [cx - 56, 236]], { c: 4 }) + T(cx, 236, 'Valid?', { size: 14, w: 'b', vmid: true });
    s += ARR(cx - 56, 236, 124, 236);
    s += T(cx - 70, 228, 'N', { size: 14, w: 'b', cls: 't-red' });
    s += ARR(cx + 56, 236, cx + 112, 236);
    s += T(cx + 70, 228, 'Y', { size: 14, w: 'b', cls: 't-grn' });
    s += para(12, 211, 112, 50, 3, 'Error');
    s += para(236, 211, 112, 50, 5, 'Welcome');
    s += K.polyline([[68, 261], [68, 336], [cx - 45, 336]], { arrow: true });
    s += K.polyline([[292, 261], [292, 336], [cx + 45, 336]], { arrow: true });
    s += K.rect(cx - 45, 319, 90, 34, { r: 17, c: 2 }) + T(cx, 336, 'End', { size: 14, w: 'b', vmid: true });
    return K.svg(360, 364, s, { title: 'Flowchart: enter credentials, compare, valid yes goes to welcome, no goes to error' });
  });

  D.register('xi1b.design-levels', () => {
    let s = '';
    s += T(98, 16, 'High-Level Design', { size: 14, w: 'b' }) + T(98, 31, 'overall structure (HLD)', { size: 11.5, cls: 't-mut' });
    s += T(342, 16, 'Low-Level Design', { size: 14, w: 'b' }) + T(342, 31, 'detailed components (LLD)', { size: 11.5, cls: 't-mut' });
    ['User Interface', 'Application Logic', 'Database'].forEach((t, i) => {
      s += K.box(28, 44 + i * 56, 140, 34, t, { c: [1, 0, 4][i], size: 13, bold: true });
      if (i < 2) s += ARR(98, 78 + i * 56, 98, 100 + i * 56);
    });
    ['Validate input', 'Check password', 'Open session'].forEach((t, i) => {
      s += K.box(272, 44 + i * 56, 140, 34, t, { c: 0, size: 13, bold: true });
      if (i < 2) s += ARR(342, 78 + i * 56, 342, 100 + i * 56);
    });
    s += ARR(172, 117, 268, 117, { cls: 's-acc' });
    s += T(220, 108, 'zoom in', { size: 12, cls: 't-acc' });
    s += T(34, 232, 'Tools:', { size: 12.5, w: 'b' });
    [['Flowcharts', 58, 84], ['UML Diagrams', 148, 98], ['ER Diagrams', 252, 90], ['Wireframes', 348, 82]].forEach(([t, x, w]) => {
      s += K.box(x, 216, w, 32, t, { c: 6, size: 11.5, r: 16 });
    });
    return K.svg(440, 258, s, { title: 'High-level design zooms into low-level design; design tools' });
  });

  D.register('xi1b.test-levels', () => {
    const rows = [
      ['Unit', 'Unit Testing', 'Test individual components', 'By: Developers', 90, 1],
      ['Integration', 'Integration Testing', 'Test combined modules', 'By: Testing team', 130, 0],
      ['System', 'System Testing', 'Test the complete system', 'By: Testing team', 170, 5],
      ['UAT', 'User Acceptance Testing (UAT)', 'Test by actual users', 'By: End users', 210, 4],
    ];
    let s = T(220, 18, 'Scope grows from small parts to the whole product', { size: 12.5, cls: 't-mut' });
    rows.forEach(([a, full, what, who, w, c], i) => {
      const y = 32 + i * 58;
      s += K.box(8, y, w, 46, a, { c, size: 14, bold: true });
      s += T(232, y + 14, full, { size: 12.5, w: 'b', anchor: 'start' });
      s += T(232, y + 29, what, { size: 11.5, cls: 't-mut', anchor: 'start' });
      s += T(232, y + 43, who, { size: 11.5, cls: 't-acc', anchor: 'start' });
    });
    return K.svg(440, 270, s, { title: 'Four levels of testing: unit, integration, system and user acceptance' });
  });

  D.register('xi1b.black-white-box', () => {
    let s = '';
    s += T(108, 18, 'Black Box Testing', { size: 14, w: 'b' });
    s += ARR(6, 92, 62, 92) + T(34, 82, 'input', { size: 12, cls: 't-mut' });
    s += K.rect(62, 52, 92, 80, { c: 6, r: 6, cls: 'f-ink' }) + T(108, 92, '?', { size: 34, w: 'b', vmid: true, cls: 't-wht' });
    s += ARR(154, 92, 210, 92) + T(182, 82, 'output', { size: 12, cls: 't-mut' });
    s += T(108, 158, 'Tester cannot see the code', { size: 12.5 });
    s += T(108, 176, 'checks only inputs and outputs', { size: 11.5, cls: 't-mut' });
    s += T(108, 194, 'e.g. type username + password', { size: 11.5, cls: 't-mut' });
    s += K.line(220, 10, 220, 200, { cls: 's-mut', dash: '3 4' });
    s += T(332, 18, 'White Box Testing', { size: 14, w: 'b' });
    s += K.ellipse(256, 92, 15, 9, { c: 6 }) + K.circle(256, 92, 4, { c: 6, cls: 'f-ink' });
    s += ARR(274, 92, 292, 92);
    s += K.rect(294, 40, 126, 104, { c: 0, r: 6, dash: '5 3' });
    s += T(357, 56, 'code inside', { size: 11, cls: 't-mut' });
    s += K.poly([[357, 64], [381, 82], [357, 100], [333, 82]], { c: 4 }) + T(357, 82, 'if', { size: 12, w: 'b', vmid: true });
    s += K.line(341, 91, 320, 112) + K.line(373, 91, 394, 112);
    s += K.box(304, 112, 34, 24, 'A', { c: 5, size: 12, r: 4 }) + K.box(376, 112, 34, 24, 'B', { c: 3, size: 12, r: 4 });
    s += T(332, 158, 'Tester CAN see the code', { size: 12.5 });
    s += T(332, 176, 'checks internal logic', { size: 11.5, cls: 't-mut' });
    s += T(332, 194, 'e.g. is every condition tested?', { size: 11.5, cls: 't-mut' });
    return K.svg(440, 206, s, { title: 'Black box testing hides the code; white box testing can see inside' });
  });

  D.register('xi1b.deploy-strategies', () => {
    const panels = [
      ['Direct Deployment', 'replace old system at once', [['oooooooo', 'Before'], ['nnnnnnnn', 'After']]],
      ['Phased Rollout', 'release to groups gradually', [['nnnooooo', 'Group 1'], ['nnnnnnoo', 'Group 2'], ['nnnnnnnn', 'Group 3']]],
      ['Pilot Release', 'small group first, then all', [['nnoooooo', 'Pilot'], ['nnnnnnnn', 'Everyone']]],
      ['Parallel Running', 'old + new together for a while', [['bbbbbbbb', 'Both run'], ['nnnnnnnn', 'Old off']]],
    ];
    let s = '';
    panels.forEach(([t, cap, rows], i) => {
      const px = 2 + (i % 2) * 220;
      const py = 4 + Math.floor(i / 2) * 150;
      s += K.rect(px, py, 216, 142, { s: 's-mut', r: 10 });
      s += T(px + 108, py + 18, t, { size: 13.5, w: 'b' });
      s += T(px + 108, py + 34, cap, { size: 11, cls: 't-mut' });
      rows.forEach(([r, lab], j) => {
        const cy = py + 62 + j * 28;
        s += T(px + 8, cy + 4, lab, { size: 11, cls: 't-mut', anchor: 'start' });
        for (let k = 0; k < 8; k++) {
          const cx = px + 74 + k * 18;
          const ch = r[k];
          if (ch === 'b') {
            s += K.circle(cx, cy - 5, 4.5, { c: 6 }) + K.circle(cx, cy + 5, 4.5, { c: 5, cls: 'f-grn' });
          } else {
            s += K.circle(cx, cy, 7, ch === 'n' ? { c: 5, cls: 'f-grn' } : { c: 6 });
          }
        }
      });
    });
    s += K.circle(110, 318, 6, { c: 6 }) + T(122, 322, 'old system', { size: 11.5, anchor: 'start' });
    s += K.circle(250, 318, 6, { c: 5, cls: 'f-grn' }) + T(262, 322, 'new system', { size: 11.5, anchor: 'start' });
    return K.svg(440, 334, s, { title: 'Four deployment strategies: direct, phased, pilot and parallel' });
  });

  D.register('xi1b.maintenance-types', () => {
    const cards = [
      ['Corrective', 'Fix bugs found after release', 'e.g. fixing a login error', 3],
      ['Adaptive', 'Change for new environments', 'e.g. update for a new Windows', 1],
      ['Perfective', 'Add features or improve', 'e.g. add dark mode', 5],
      ['Preventive', 'Prevent future problems', 'e.g. improve code for speed', 4],
    ];
    let s = '';
    cards.forEach(([t, a, b, c], i) => {
      const x = 4 + (i % 2) * 220;
      const y = 4 + Math.floor(i / 2) * 104;
      s += K.rect(x, y, 212, 96, { c, r: 10 });
      s += T(x + 106, y + 26, t, { size: 15, w: 'b' });
      s += T(x + 106, y + 52, a, { size: 12 });
      s += T(x + 106, y + 74, b, { size: 11.5, cls: 't-mut' });
    });
    return K.svg(440, 212, s, { title: 'Four types of software maintenance with examples' });
  });

  /* ---------- SDLC models ---------- */
  D.register('xi1b.waterfall', () => {
    const names = [
      ['1. Requirements', 'Analysis & Specification'],
      ['2. Design', 'System & Software Design'],
      ['3. Implementation', 'Implementation & Coding'],
      ['4. Testing', 'Integration & Testing'],
      ['5. Deployment', 'Deployment & Release'],
      ['6. Maintenance', 'Maintenance & Evolution'],
    ];
    let s = '';
    names.forEach(([a, b], i) => {
      const x = 6 + i * 54;
      const y = 6 + i * 58;
      s += card(x, y, 158, 42, PH[i], a, b, { ts: 13, ss: 11, r: 8 });
      if (i < 5) s += ARR(x + 54 + 22, y + 42, x + 54 + 22, y + 58);
    });
    s += T(78, 214, 'Next phase begins only', { size: 12, cls: 't-mut' });
    s += T(78, 229, 'after the previous phase', { size: 12, cls: 't-mut' });
    s += T(78, 244, 'is completed', { size: 12, cls: 't-mut' });
    s += K.line(30, 300, 30, 262, { arrow: true, cls: 's-red', dash: '4 3' });
    s += T(100, 292, 'No going back!', { size: 13, w: 'b', cls: 't-red' });
    return K.svg(440, 352, s, { title: 'Waterfall model: six phases as a staircase, each starts after the previous one finishes' });
  });

  D.register('xi1b.agile-loop', () => {
    const cx = 220;
    const cy = 176;
    const R = 122;
    const r = 37;
    const labs = ['Plan', 'Design', 'Develop', 'Test', 'Deploy', 'Review &\nFeedback'];
    const cols = [1, 0, 5, 4, 2, 3];
    const ang = (i) => ((-90 + 60 * i) * Math.PI) / 180;
    let s = '';
    for (let i = 0; i < 6; i++) {
      const a0 = ang(i) + (r + 5) / R;
      const a1 = ang(i + 1) - (r + 9) / R;
      const P = (a) => (cx + R * Math.cos(a)).toFixed(1) + ' ' + (cy + R * Math.sin(a)).toFixed(1);
      s += K.path('M' + P(a0) + ' A' + R + ' ' + R + ' 0 0 1 ' + P(a1), { arrow: true });
    }
    labs.forEach((l, i) => {
      const x = cx + R * Math.cos(ang(i));
      const y = cy + R * Math.sin(ang(i));
      s += K.circle(x, y, r, { c: cols[i] }) + T(x, y + 2, l, { size: 12, w: 'b', vmid: true });
      s += K.circle(x - 28, y - 28, 9, { c: 6 }) + T(x - 28, y - 28, String(i + 1), { size: 11, w: 'b', vmid: true });
    });
    s += T(cx, 124, 'AGILE', { size: 15, w: 'b' });
    [['To Do', 3], ['In Progress', 2], ['Done', 1]].forEach(([t, n], i) => {
      const x = 147 + i * 50;
      s += K.rect(x, 136, 46, 58, { c: 6, r: 4 });
      for (let k = 0; k < n; k++) s += K.rect(x + 8, 142 + k * 16, 30, 12, { c: 4, r: 2 });
      s += T(x + 23, 210, t, { size: 11, cls: 't-mut' });
    });
    s += T(cx, 350, 'one sprint = one trip around the loop (2 to 4 weeks)', { size: 11.5, cls: 't-mut' });
    return K.svg(440, 360, s, { title: 'Agile model: plan, design, develop, test, deploy, review and feedback in a loop around a task board' });
  });

  D.register('xi1b.wf-vs-agile', () => {
    let s = '';
    s += T(8, 18, 'Waterfall: one long run', { size: 13.5, w: 'b', anchor: 'start' });
    const seg = [['Req', 48, 1], ['Design', 48, 0], ['Code', 112, 5], ['Test', 60, 4], ['Deploy', 60, 2], ['Maint.', 98, 3]];
    let x = 8;
    seg.forEach(([t, w, c]) => {
      s += K.rect(x, 28, w, 36, { c, r: 0 }) + T(x + w / 2, 46, t, { size: 11.5, vmid: true });
      x += w;
    });
    s += K.line(x - 98, 64, x - 98, 94, { cls: 's-grn', w: 2 });
    s += K.circle(x - 98, 98, 5, { cls: 'f-grn' });
    s += T(x - 98, 117, 'first working software', { size: 11.5, w: 'b' });
    s += T(x - 98, 131, 'only near the end', { size: 11.5, cls: 't-mut' });
    s += T(8, 164, 'Agile: many short sprints', { size: 13.5, w: 'b', anchor: 'start' });
    for (let i = 0; i < 5; i++) {
      const sx = 8 + i * 85;
      s += K.rect(sx, 174, 85, 36, { c: i % 2 ? 0 : 1, r: 0 }) + T(sx + 42.5, 192, 'Sprint ' + (i + 1), { size: 11.5, vmid: true });
      s += K.line(sx + 42.5, 210, sx + 42.5, 222, { cls: 's-grn', w: 2 });
      s += K.circle(sx + 42.5, 226, 5, { cls: 'f-grn' });
    }
    s += T(220, 250, 'working software after every sprint', { size: 11.5, w: 'b' });
    s += ARR(8, 272, 430, 272, { cls: 's-mut' }) + T(425, 266, 'time', { size: 11, anchor: 'end', cls: 't-mut' });
    return K.svg(440, 282, s, { title: 'Waterfall delivers once near the end; Agile delivers working software after every sprint' });
  });

  /* ---------- Case study 1 ---------- */
  D.register('xi1b.lms-screens', () => {
    let s = T(220, 16, 'Five screens designed', { size: 14, w: 'b' });
    s += K.box(6, 70, 100, 46, 'Login\nScreen', { c: 3, size: 13, bold: true });
    s += K.box(150, 70, 100, 46, 'Home\nMenu', { c: 1, size: 13, bold: true });
    s += ARR(106, 93, 150, 93);
    [['Book Management', 0], ['Borrow / Return', 5], ['Reports', 4]].forEach(([t, c], i) => {
      const y = 30 + i * 56;
      s += K.box(296, y, 138, 42, t, { c, size: 12.5, bold: true });
      s += ARR(250, 93, 296, y + 21);
    });
    s += T(78, 140, 'password check', { size: 11, cls: 't-mut' });
    s += T(190, 140, 'leads to all features', { size: 11, cls: 't-mut' });
    return K.svg(440, 186, s, { title: 'Library system screens: login, home menu, book management, borrow and return, reports' });
  });

  D.register('xi1b.gantt', () => {
    const cols = ['Jan\nWk 1-2', 'Jan\nWk 3-4', 'Feb', 'Mar', 'Apr', 'May', 'Jun+'];
    const rows = [['Requirements', 0, 1], ['Design', 1, 1], ['Implementation', 2, 2], ['Testing', 4, 1], ['Deployment', 5, 1], ['Maintenance', 6, 1]];
    const x0 = 112;
    const cw = 46;
    let s = '';
    cols.forEach((c, i) => {
      s += K.rect(x0 + i * cw, 6, cw, 38, { c: 6, r: 0, cls: 'cell' }) + T(x0 + i * cw + cw / 2, 25, c, { size: 11, vmid: true, w: 'b' });
    });
    rows.forEach(([n, st, sp], i) => {
      const y = 48 + i * 34;
      s += T(6, y + 20, n, { size: 12, anchor: 'start' });
      for (let k = 0; k < 7; k++) s += K.rect(x0 + k * cw, y, cw, 34, { r: 0, cls: 'cell' });
      s += K.rect(x0 + st * cw + 3, y + 5, sp * cw - 6, 24, { c: PH[i], r: 5 });
    });
    s += T(220, 268, 'Each phase starts after the one above it finishes', { size: 11.5, cls: 't-mut' });
    return K.svg(440, 278, s, { title: 'Gantt chart of the Al-Noor library project from January to June' });
  });

  D.register('xi1b.lms-schema', () => {
    const tabs = [
      [4, 'BOOKS', 4, [['BookID', 'INT (PK)'], ['Title', 'TEXT'], ['Author', 'TEXT'], ['Category', 'TEXT'], ['TotalCopies', 'INT']]],
      [156, 'LOANS', 3, [['LoanID', 'INT (PK)'], ['BookID', 'INT (FK)'], ['StudentID', 'INT (FK)'], ['DateBorrowed', 'DATE'], ['DateDue', 'DATE'], ['DateReturned', 'DATE']]],
      [308, 'STUDENTS', 1, [['StudentID', 'INT (PK)'], ['FullName', 'TEXT'], ['Class', 'TEXT'], ['Phone', 'TEXT']]],
    ];
    let s = '';
    tabs.forEach(([x, name, c, fields]) => {
      s += K.rect(x, 20, 124, 26, { c, r: 0, cls: 'cell' }) + T(x + 62, 33, name, { size: 13, w: 'b', vmid: true });
      fields.forEach(([f, ty], i) => {
        const pk = ty.includes('PK');
        const fk = ty.includes('FK');
        s += K.rect(x, 46 + i * 22, 124, 22, { c: pk ? 4 : fk ? 6 : undefined, r: 0, cls: 'cell' });
        s += T(x + 6, 61 + i * 22, f, { size: 12, anchor: 'start', w: pk ? 'b' : '' });
        s += T(x + 118, 61 + i * 22, ty, { size: 11, anchor: 'end', cls: 't-mut' });
      });
    });
    s += K.polyline([[128, 57], [142, 57], [142, 79], [156, 79]], { cls: 's-acc', w: 2 });
    s += K.polyline([[308, 57], [294, 57], [294, 101], [280, 101]], { cls: 's-acc', w: 2 });
    s += T(135, 52, '1', { size: 12, w: 'b', cls: 't-acc' }) + T(149, 93, 'N', { size: 12, w: 'b', cls: 't-acc' });
    s += T(301, 52, '1', { size: 12, w: 'b', cls: 't-acc' }) + T(287, 115, 'N', { size: 12, w: 'b', cls: 't-acc' });
    s += T(66, 188, '1 Book has many loans', { size: 12, cls: 't-mut' });
    s += T(358, 188, '1 Student has many loans', { size: 12, cls: 't-mut' });
    s += T(220, 12, 'PK = primary key   FK = foreign key', { size: 11, cls: 't-mut' });
    return K.svg(440, 204, s, { title: 'Database schema: BOOKS and STUDENTS are linked through LOANS' });
  });

  /* ---------- Case study 2 ---------- */
  D.register('xi1b.scrum-cycle', () => {
    const nodes = [
      ['Product\nBacklog', 4],
      ['Sprint\nPlanning', 1],
      ['Daily\nStandup', 5],
      ['Sprint\n(2 Weeks)', 7],
      ['Sprint\nReview', 2],
      ['Sprint\nRetrospective', 3],
    ].map(([t, c]) => ({ t, c }));
    let s = ringBoxes(nodes, { cy: 126, ry: 100, bh: 50 });
    s += K.circle(220, 126, 42, { c: 6 }) + T(220, 126, 'SCRUM\nCYCLE', { size: 13, w: 'b', vmid: true });
    s += K.rect(60, 252, 320, 34, { c: 5, r: 10 }) + T(220, 269, 'Working software delivered after every Sprint', { size: 12.5, w: 'b', vmid: true });
    return K.svg(440, 296, s, { title: 'Scrum cycle: backlog, planning, daily standup, sprint, review, retrospective' });
  });

  D.register('xi1b.user-story', () => {
    let s = K.box(6, 6, 56, 24, 'US-01', { c: 6, size: 12, r: 12 });
    s += T(74, 23, 'User Story: a feature told from the user\'s side', { size: 12.5, w: 'b', anchor: 'start' });
    s += T(66, 50, 'WHO', { size: 11, cls: 't-mut' }) + T(237, 50, 'WHAT', { size: 11, cls: 't-mut' }) + T(391, 50, 'IMPORTANCE', { size: 11, cls: 't-mut' });
    s += card(6, 56, 120, 54, 1, 'As a\nstudent', null, { ts: 14 });
    s += card(134, 56, 206, 54, 0, 'I want to see my class\ntimetable on my phone', null, { ts: 13 });
    s += card(348, 56, 86, 54, 3, 'Priority\nHigh', null, { ts: 13 });
    s += T(220, 134, 'As a student, I want to see my class timetable on my phone.', { size: 12, cls: 't-mut' });
    return K.svg(440, 146, s, { title: 'Anatomy of a user story: who, what and priority' });
  });

  D.register('xi1b.sprint-timeline', () => {
    const rows = [
      ['Sprint 1', 'Weeks 1-2', 'US-01 Class Timetable', 'Add teacher names'],
      ['Sprint 2', 'Weeks 3-4', 'US-02 Exam Results\n+ teacher names', 'Parents want full\nattendance record'],
      ['Sprint 3', 'Weeks 5-6', 'US-03 Absence alert\nUS-05 Attendance', 'SMS outage: switched\nto email, then back'],
      ['Sprint 4', 'Weeks 7-8', 'US-04 Library booking\nUS-07 Announcements', 'Show available copies\n(30-minute change)'],
      ['Sprint 5', 'Weeks 9-10', 'US-06 Homework\nsubmission', '3 bugs fixed,\napp approved'],
    ];
    const cs = [1, 0, 5, 7, 2];
    let s = T(52, 16, 'Sprint', { size: 12, w: 'b' }) + T(190, 16, 'Delivered', { size: 12, w: 'b' }) + T(366, 16, 'Review feedback / event', { size: 12, w: 'b' });
    rows.forEach(([a, b, c, d], i) => {
      const y = 26 + i * 58;
      s += card(6, y, 92, 42, cs[i], a, b, { ts: 12.5, ss: 11 });
      s += K.rect(106, y, 164, 42, { c: 6, r: 8 }) + T(188, y + 21, c, { size: 11.5, vmid: true });
      s += K.rect(286, y, 148, 42, { c: 4, r: 8 }) + T(360, y + 21, d, { size: 11.5, vmid: true });
      s += ARR(270, y + 21, 286, y + 21);
      if (i < 4) s += ARR(360, y + 42, 360, y + 58);
    });
    return K.svg(440, 320, s, { title: 'Five sprints of the Al-Noor student app with deliveries and review feedback' });
  });

  D.register('xi1b.sprint-progress', () => {
    const x0 = 56;
    const yb = 232;
    const u = 19.5;
    let s = T(8, 14, 'User stories completed', { size: 12, anchor: 'start', w: 'b' });
    for (let v = 0; v <= 10; v += 2) {
      s += K.line(x0, yb - v * u, 432, yb - v * u, { cls: 's-mut', w: 0.6 }) + T(x0 - 6, yb - v * u + 4, String(v), { size: 11, anchor: 'end', cls: 't-mut' });
    }
    const cs = [1, 0, 5, 7, 2];
    const pts = [];
    for (let i = 0; i < 5; i++) {
      const bx = 64 + i * 74;
      s += K.rect(bx, yb - 2 * u, 56, 2 * u, { c: cs[i], r: 4 }) + T(bx + 28, yb - u, '2', { size: 14, w: 'b', vmid: true });
      s += T(bx + 28, yb + 16, 'Sprint ' + (i + 1), { size: 11.5, w: 'b' }) + T(bx + 28, yb + 30, 'Wk ' + (1 + 2 * i) + '-' + (2 + 2 * i), { size: 11, cls: 't-mut' });
      pts.push([bx + 28, yb - 2 * (i + 1) * u]);
    }
    s += K.polyline(pts, { cls: 's-brand', w: 2.5 });
    pts.forEach((p, i) => {
      s += K.dot(p[0], p[1], 5) + T(p[0] - (i === 0 ? -14 : 12), p[1] - 8, String(2 * (i + 1)), { size: 12.5, w: 'b', cls: 't-acc', anchor: i === 0 ? 'start' : 'end' });
    });
    s += K.rect(70, 268, 12, 12, { c: 1, r: 2 }) + T(88, 278, 'Stories per sprint', { size: 11.5, anchor: 'start' });
    s += K.dot(246, 274, 5) + T(258, 278, 'Cumulative total', { size: 11.5, anchor: 'start' });
    return K.svg(440, 290, s, { title: 'Bar chart of user stories per sprint with cumulative line' });
  });

  D.register('xi1b.compare-score', () => {
    const rows = [['Flexibility', 2, 5], ['Customer\nInvolvement', 2, 5], ['Documentation', 5, 2], ['Delivery Speed', 3, 5], ['Risk\nManagement', 3, 4], ['Suitability\nfor this project', 4, 4]];
    const x0 = 134;
    const u = 54;
    let s = K.rect(150, 6, 12, 12, { c: 1, r: 2 }) + T(168, 16, 'Waterfall', { size: 12, anchor: 'start' });
    s += K.rect(250, 6, 12, 12, { c: 5, r: 2 }) + T(268, 16, 'Agile', { size: 12, anchor: 'start' });
    for (let v = 0; v <= 5; v++) {
      s += K.line(x0 + v * u, 28, x0 + v * u, 28 + 6 * 46, { cls: 's-mut', w: 0.6 }) + T(x0 + v * u, 28 + 6 * 46 + 14, String(v), { size: 11, cls: 't-mut' });
    }
    rows.forEach(([n, w, a], i) => {
      const y = 34 + i * 46;
      s += T(6, y + (n.includes('\n') ? 13 : 20), n, { size: 12, anchor: 'start' });
      s += K.rect(x0, y, w * u, 16, { c: 1, r: 3 }) + T(x0 + w * u + 6, y + 12, String(w), { size: 12, w: 'b', anchor: 'start' });
      s += K.rect(x0, y + 19, a * u, 16, { c: 5, r: 3 }) + T(x0 + a * u + 6, y + 31, String(a), { size: 12, w: 'b', anchor: 'start' });
    });
    s += T(220, 28 + 6 * 46 + 34, 'Score out of 5. Documentation is scored inversely:', { size: 11.5, cls: 't-mut' });
    s += T(220, 28 + 6 * 46 + 49, 'a lower score means less documentation is required.', { size: 11.5, cls: 't-mut' });
    return K.svg(440, 28 + 6 * 46 + 60, s, { title: 'Waterfall versus Agile scores on six criteria out of five' });
  });

  /* ---------- Communication models & OSI ---------- */
  D.register('xi1b.sender-channel-receiver', () => {
    let s = '';
    s += card(6, 22, 104, 62, 1, 'Sender', 'device', { ts: 15 });
    s += card(160, 22, 120, 62, 6, 'Communication\nchannel', null, { ts: 13 });
    s += card(330, 22, 104, 62, 5, 'Receiver', 'device', { ts: 15 });
    s += ARR(110, 53, 160, 53) + ARR(280, 53, 330, 53);
    s += T(135, 44, 'data', { size: 12, cls: 't-mut' }) + T(305, 44, 'data', { size: 12, cls: 't-mut' });
    s += K.rect(6, 108, 428, 40, { c: 4, r: 10, dash: '6 4' });
    s += T(220, 124, 'Both sides follow the same rules', { size: 13, w: 'b' });
    s += T(220, 140, 'layers + protocols = the communication model', { size: 11.5, cls: 't-mut' });
    return K.svg(440, 158, s, { title: 'Sender, communication channel and receiver following common rules' });
  });

  D.register('xi1b.postal-analogy', () => {
    const post = ['Write the\nmessage', 'Put in\nenvelope', 'Write the\naddress', 'Post office\nsorts', 'Letter\ndelivered'];
    const net = ['App creates\ndata', 'Add\nheaders', 'Add IP\naddress', 'Routers\nforward', 'Receiver\ngets data'];
    let s = T(6, 18, 'Postal system', { size: 13, w: 'b', anchor: 'start' }) + T(6, 118, 'Network: each step is like one layer', { size: 13, w: 'b', anchor: 'start' });
    for (let i = 0; i < 5; i++) {
      s += chev(4 + i * 86, 28, 88, 52, 4, post[i]);
      s += chev(4 + i * 86, 128, 88, 52, 1, net[i]);
      s += K.line(48 + i * 86, 80, 48 + i * 86, 128, { cls: 's-mut', dash: '3 4' });
    }
    return K.svg(440, 192, s, { title: 'Sending a letter by post compared with sending data over a network' });
  });

  D.register('xi1b.osi-stack', () => {
    const jobs = {
      7: ['Network services to', 'user applications'],
      6: ['Translate, encrypt,', 'compress data'],
      5: ['Open, maintain and', 'close sessions'],
      4: ['Reliable delivery,', 'error check, ports'],
      3: ['IP addressing and', 'routing'],
      2: ['MAC addressing,', 'error detection'],
      1: ['Raw bits over the', 'physical medium'],
    };
    const prot = {
      7: ['HTTP, HTTPS, FTP,', 'SMTP, DNS'],
      6: ['SSL/TLS, JPEG,', 'MP3, ASCII'],
      5: ['NetBIOS, RPC', ''],
      4: ['TCP, UDP', ''],
      3: ['IP, ICMP,', 'RIP, OSPF'],
      2: ['Ethernet, Wi-Fi', '(802.11), MAC'],
      1: ['Cables, Hubs,', 'Repeaters, Radio'],
    };
    let s = T(66, 16, 'Layer', { size: 12, w: 'b', cls: 't-mut' }) + T(200, 16, 'Main job', { size: 12, w: 'b', cls: 't-mut' }) + T(340, 16, 'Protocols', { size: 12, w: 'b', cls: 't-mut' }) + T(446, 16, 'Unit', { size: 12, w: 'b', cls: 't-mut' });
    [7, 6, 5, 4, 3, 2, 1].forEach((n, i) => {
      const y = 24 + i * 54;
      s += K.rect(4, y, 472, 50, { c: OL[n], r: 8 });
      s += T(20, y + 25, String(n), { size: 18, w: 'b', vmid: true });
      s += T(36, y + 25, ON[n], { size: 12.5, w: 'b', vmid: true, anchor: 'start' });
      s += T(134, y + 21, jobs[n][0], { size: 11, anchor: 'start' }) + T(134, y + 35, jobs[n][1], { size: 11, anchor: 'start' });
      s += T(272, prot[n][1] ? y + 21 : y + 29, prot[n][0], { size: 11, anchor: 'start' });
      if (prot[n][1]) s += T(272, y + 35, prot[n][1], { size: 11, anchor: 'start' });
      s += T(446, y + 25, UNIT[n], { size: 12, w: 'b', vmid: true });
      s += K.line(128, y + 6, 128, y + 44, { cls: 's-mut', w: 0.6 }) + K.line(266, y + 6, 266, y + 44, { cls: 's-mut', w: 0.6 }) + K.line(398, y + 6, 398, y + 44, { cls: 's-mut', w: 0.6 });
    });
    return K.svg(480, 404, s, { title: 'The seven OSI layers with their main job, protocols and data unit' });
  });

  D.register('xi1b.osi-mnemonic', () => {
    const words = { 7: 'Away', 6: 'Pizza', 5: 'Sausage', 4: 'Throw', 3: 'Not', 2: 'Do', 1: 'Please' };
    let s = T(220, 16, 'Read from the bottom (1) to the top (7)', { size: 12.5, cls: 't-mut' });
    [7, 6, 5, 4, 3, 2, 1].forEach((n, i) => {
      const y = 28 + i * 42;
      s += K.rect(8, y, 176, 36, { c: OL[n], r: 8 }) + T(24, y + 18, String(n), { size: 16, w: 'b', vmid: true }) + T(44, y + 18, ON[n], { size: 13.5, w: 'b', vmid: true, anchor: 'start' });
      s += ARR(186, y + 18, 206, y + 18, { cls: 's-mut' });
      s += T(214, y + 19, words[n], { size: 16, w: 'b', vmid: true, anchor: 'start', cls: 't-acc' });
    });
    const br = (y1, y2, t) => K.polyline([[312, y1], [320, y1], [320, y2], [312, y2]], { cls: 's-mut' }) + T(330, (y1 + y2) / 2, t, { size: 12, vmid: true, anchor: 'start', w: 'b' });
    s += br(30, 160, 'Software\nlayers\n(7 to 4)') + br(198, 232, 'Heart\nof OSI') + br(240, 316, 'Hardware\nlayers\n(2 to 1)');
    return K.svg(440, 326, s, { title: 'Mnemonic Please Do Not Throw Sausage Pizza Away for OSI layers one to seven' });
  });

  D.register('xi1b.l7-app', () => {
    let s = T(66, 16, 'Application program', { size: 11.5, cls: 't-mut' }) + T(250, 16, 'Network service', { size: 11.5, cls: 't-mut' });
    s += card(6, 24, 120, 60, 6, 'Web browser\nEmail client', null, { ts: 12.5, dash: '5 3' });
    s += ARR(126, 54, 170, 54);
    s += card(170, 24, 160, 60, 1, 'Application Layer', 'Layer 7', { ts: 13.5 });
    s += ARR(330, 54, 356, 54);
    s += T(396, 50, 'HTTP · FTP', { size: 12 }) + T(396, 66, 'SMTP · DNS', { size: 12 });
    s += ARR(250, 84, 250, 114);
    s += card(170, 114, 160, 40, 6, 'Lower layers (6 to 1)', null, { ts: 12.5 });
    s += T(220, 184, 'Analogy: a restaurant', { size: 12, w: 'b' });
    s += card(6, 194, 206, 38, 1, 'Menu: what you use', null, { ts: 12.5 });
    s += card(228, 194, 206, 38, 6, 'Kitchen: does the real work', null, { ts: 12.5 });
    return K.svg(440, 244, s, { title: 'The application layer is the network service used by programs like a browser' });
  });

  D.register('xi1b.l6-translate', () => {
    let s = T(95, 14, 'Sender', { size: 13.5, w: 'b' }) + T(345, 14, 'Receiver', { size: 13.5, w: 'b' });
    const L = [['Plain data', '"Hello"', 1], ['Compress', 'make it smaller', 2], ['Encrypt', 'make it secret', 3]];
    const Rr = [['Plain data', '"Hello"', 1], ['Decompress', 'restore size', 2], ['Decrypt', 'unscramble', 3]];
    L.forEach(([a, b, c], i) => {
      s += card(20, 26 + i * 62, 150, 42, c, a, b, { ts: 12.5 });
      if (i < 2) s += ARR(95, 68 + i * 62, 95, 88 + i * 62);
    });
    Rr.forEach(([a, b, c], i) => {
      s += card(270, 26 + i * 62, 150, 42, c, a, b, { ts: 12.5 });
      if (i < 2) s += ARR(345, 88 + i * 62, 345, 68 + i * 62);
    });
    s += ARR(170, 171, 270, 171);
    s += T(220, 160, 'network', { size: 12, cls: 't-mut' }) + T(220, 188, 'Xq7#z', { size: 12, w: 'b', cls: 't-red' });
    s += K.rect(6, 214, 428, 30, { c: 6, r: 8 });
    s += T(220, 229, 'Translation: EBCDIC to ASCII, Unicode to UTF-8', { size: 12, vmid: true });
    return K.svg(440, 252, s, { title: 'Presentation layer: compress and encrypt at the sender, decrypt and decompress at the receiver' });
  });

  D.register('xi1b.l5-session', () => {
    let s = K.box(40, 6, 100, 26, 'Device A', { c: 1, size: 13, bold: true }) + K.box(300, 6, 100, 26, 'Device B', { c: 5, size: 13, bold: true });
    s += K.line(90, 32, 90, 284, { cls: 's-mut', dash: '4 4' }) + K.line(350, 32, 350, 284, { cls: 's-mut', dash: '4 4' });
    const msg = (y, t, dir, o) => {
      o = o || {};
      return (dir > 0 ? ARR(92, y, 348, y, o) : ARR(348, y, 92, y, o)) + T(220, y - 6, t, { size: 12 });
    };
    s += msg(62, '"Hello" - open the session', 1);
    s += msg(92, 'OK, ready', -1);
    s += msg(130, 'data exchange', 1);
    s += msg(156, 'data exchange', -1);
    s += K.rect(100, 176, 150, 26, { c: 4, r: 6 }) + T(175, 189, 'checkpoint saved', { size: 12, vmid: true });
    s += msg(236, '"Goodbye" - close the session', 1);
    s += T(372, 78, 'Establish', { size: 12, w: 'b', anchor: 'start', cls: 't-acc' });
    s += T(372, 144, 'Maintain', { size: 12, w: 'b', anchor: 'start', cls: 't-acc' });
    s += T(372, 240, 'Terminate', { size: 12, w: 'b', anchor: 'start', cls: 't-acc' });
    s += T(220, 272, 'if the link breaks, resume from the checkpoint', { size: 11.5, cls: 't-mut' });
    return K.svg(440, 292, s, { title: 'Session layer: establish, maintain with checkpoints, then terminate a session' });
  });

  D.register('xi1b.duplex', () => {
    let s = '';
    const panel = (px, title, cap, both) => {
      let o = K.rect(px, 4, 214, 132, { s: 's-mut', r: 10 });
      o += T(px + 107, 24, title, { size: 14, w: 'b' });
      o += K.box(px + 14, 44, 40, 50, 'A', { c: 1, size: 14, bold: true }) + K.box(px + 160, 44, 40, 50, 'B', { c: 5, size: 14, bold: true });
      o += ARR(px + 58, 56, px + 156, 56);
      o += both ? ARR(px + 156, 82, px + 58, 82) : ARR(px + 156, 82, px + 58, 82, { dash: '4 4', cls: 's-mut' });
      o += T(px + 107, 114, cap, { size: 11.5, cls: 't-mut' });
      o += T(px + 107, 128, both ? 'both directions together' : 'one direction at a time', { size: 11.5 });
      return o;
    };
    s += panel(2, 'Half-duplex', '(walkie-talkie)', false) + panel(224, 'Full-duplex', '(phone call)', true);
    return K.svg(440, 142, s, { title: 'Half-duplex versus full-duplex communication' });
  });

  D.register('xi1b.l4-segments', () => {
    const cs = [1, 0, 5, 4];
    const box = (x, y, t, c, o) => K.rect(x, y, 62, 34, Object.assign({ c, r: 6 }, o || {})) + T(x + 31, y + 17, t, { size: 13, w: 'b', vmid: true });
    let s = '';
    s += T(6, 38, '1. Sender', { size: 12.5, w: 'b', anchor: 'start' }) + T(6, 53, 'segmentation', { size: 11.5, cls: 't-mut', anchor: 'start' });
    for (let i = 0; i < 4; i++) s += box(140 + i * 72, 26, 'S' + (i + 1), cs[i]);
    s += ARR(280, 60, 280, 98);
    s += T(290, 82, 'send over the network', { size: 11.5, cls: 't-mut', anchor: 'start' });
    s += T(6, 116, '2. Network', { size: 12.5, w: 'b', anchor: 'start' }) + T(6, 131, 'any order, one lost', { size: 11.5, cls: 't-mut', anchor: 'start' });
    [[3, 0], [1, 1], [4, 2]].forEach(([k, j]) => { s += box(140 + j * 72, 104, 'S' + k, cs[k - 1]); });
    s += K.rect(356, 104, 62, 34, { c: 3, r: 6, dash: '4 3', s: 's-red' }) + T(387, 121, 'S2 lost', { size: 12, w: 'b', vmid: true, cls: 't-red' });
    s += ARR(280, 138, 280, 178);
    s += T(290, 154, 'receiver asks: resend S2', { size: 11.5, cls: 't-red', anchor: 'start' });
    s += T(290, 168, '(error control)', { size: 11.5, cls: 't-mut', anchor: 'start' });
    s += T(6, 196, '3. Receiver', { size: 12.5, w: 'b', anchor: 'start' }) + T(6, 211, 'reassembly', { size: 11.5, cls: 't-mut', anchor: 'start' });
    for (let i = 0; i < 4; i++) s += box(140 + i * 72, 184, 'S' + (i + 1), cs[i]);
    s += T(280, 238, 'back in the correct order', { size: 12, cls: 't-grn', w: 'b' });
    return K.svg(440, 248, s, { title: 'Transport layer: segmentation, error control and reassembly' });
  });

  D.register('xi1b.ports', () => {
    let s = '';
    s += K.rect(6, 14, 140, 192, { c: 6, r: 10 });
    s += T(76, 40, 'Destination', { size: 13.5, w: 'b' }) + T(76, 56, 'device', { size: 13.5, w: 'b' });
    s += T(76, 100, 'IP address', { size: 12.5, w: 'b', cls: 't-acc' }) + T(76, 116, '192.168.1.1', { size: 12.5 });
    s += T(76, 136, 'the house address', { size: 11.5, cls: 't-mut' });
    s += T(76, 170, 'Port = which room', { size: 11.5, cls: 't-mut' }) + T(76, 185, 'inside the house', { size: 11.5, cls: 't-mut' });
    [['80', 'HTTP: web pages', 1], ['443', 'HTTPS: secure web', 2], ['21', 'FTP: file transfer', 5], ['25', 'SMTP: send email', 4]].forEach(([p, a, c], i) => {
      const y = 18 + i * 48;
      s += ARR(146, 110, 218, y + 19, { cls: 's-mut' });
      s += card(220, y, 70, 38, c, 'Port ' + p, null, { ts: 12.5 });
      s += T(298, y + 20, a, { size: 12, anchor: 'start', vmid: true });
    });
    return K.svg(440, 220, s, { title: 'Port numbers choose the application: 80 HTTP, 443 HTTPS, 21 FTP, 25 SMTP' });
  });

  D.register('xi1b.tcp-udp', () => {
    let s = '';
    const frame = (px, title, sub) => {
      let o = K.rect(px, 4, 216, 290, { s: 's-mut', r: 10 });
      o += T(px + 108, 24, title, { size: 15, w: 'b' }) + T(px + 108, 40, sub, { size: 11.5, cls: 't-mut' });
      o += K.box(px + 16, 50, 40, 24, 'A', { c: 1, size: 13, bold: true, r: 6 }) + K.box(px + 160, 50, 40, 24, 'B', { c: 5, size: 13, bold: true, r: 6 });
      o += K.line(px + 36, 74, px + 36, 230, { cls: 's-mut', dash: '3 4' }) + K.line(px + 180, 74, px + 180, 230, { cls: 's-mut', dash: '3 4' });
      return o;
    };
    const m = (px, y, t, dir, o) => (dir > 0 ? ARR(px + 38, y, px + 178, y, o) : ARR(px + 178, y, px + 38, y, o)) + T(px + 108, y - 5, t, { size: 11.5 });
    s += frame(2, 'TCP', 'connection-oriented (reliable)');
    [['connect?', 1], ['ready', -1], ['data 1', 1], ['got it (ACK)', -1], ['data 2', 1], ['got it (ACK)', -1]].forEach(([t, d], i) => { s += m(2, 96 + i * 26, t, d); });
    s += T(110, 252, 'Web, email, file transfer', { size: 11.5, w: 'b' }) + T(110, 267, 'accuracy matters', { size: 11.5, cls: 't-mut' });
    s += T(110, 285, 'slower, but nothing is lost', { size: 11.5, cls: 't-mut' });
    s += frame(222, 'UDP', 'connectionless (fast)');
    [['data 1', 1], ['data 2', 1], ['data 3', 1]].forEach(([t, d], i) => { s += m(222, 96 + i * 26, t, d); });
    s += T(330, 190, 'no connection, no reply', { size: 11.5, cls: 't-red' });
    s += T(330, 252, 'Video streaming, gaming, calls', { size: 11.5, w: 'b' }) + T(330, 267, 'speed matters more than perfection', { size: 11.5, cls: 't-mut' });
    s += T(330, 285, 'lower overhead', { size: 11.5, cls: 't-mut' });
    return K.svg(440, 298, s, { title: 'TCP with acknowledgements versus UDP without replies' });
  });

  D.register('xi1b.l3-routing', () => {
    const S = [46, 115];
    const Dn = [394, 115];
    const R = { 1: [150, 42], 2: [150, 115], 3: [150, 188], 4: [290, 78], 5: [290, 152] };
    const links = [['S', 1], ['S', 2], ['S', 3], [1, 4], [2, 4], [2, 5], [3, 5], [4, 'D'], [5, 'D']];
    const P = (k) => (k === 'S' ? S : k === 'D' ? Dn : R[k]);
    let s = '';
    links.forEach(([a, b]) => { s += K.line(P(a)[0], P(a)[1], P(b)[0], P(b)[1], { cls: 's-mut', w: 1.6 }); });
    [['S', 2], [2, 4], [4, 'D']].forEach(([a, b]) => { s += K.line(P(a)[0], P(a)[1], P(b)[0], P(b)[1], { cls: 's-grn', w: 4.5 }); });
    s += K.rect(6, 88, 80, 54, { c: 1, r: 8 }) + T(46, 108, 'Source', { size: 13, w: 'b' }) + T(46, 126, '192.168.1.1', { size: 11 });
    s += K.rect(354, 88, 80, 54, { c: 0, r: 8 }) + T(394, 108, 'Destination', { size: 12, w: 'b' }) + T(394, 126, 'IP address', { size: 11 });
    Object.keys(R).forEach((k) => {
      s += K.circle(R[k][0], R[k][1], 19, { c: 5 }) + T(R[k][0], R[k][1], 'R' + k, { size: 12.5, w: 'b', vmid: true });
    });
    s += T(220, 18, 'R = router', { size: 11.5, cls: 't-mut' });
    s += T(220, 222, 'Routers read the destination IP and forward each packet.', { size: 12 });
    s += T(220, 238, 'Best route shown in green.', { size: 12, cls: 't-grn', w: 'b' });
    return K.svg(440, 248, s, { title: 'Routers forward packets from source to destination along the best route' });
  });

  D.register('xi1b.ip-formats', () => {
    let s = T(220, 16, 'IPv4 address: 32 bits', { size: 14, w: 'b' });
    ['192', '168', '1', '1'].forEach((v, i) => {
      s += K.rect(44 + i * 76, 28, 62, 34, { c: 1, r: 6 }) + T(75 + i * 76, 45, v, { size: 14, w: 'b', vmid: true });
      s += T(75 + i * 76, 78, '8 bits', { size: 11, cls: 't-mut' });
      if (i < 3) s += T(113 + i * 76, 54, '.', { size: 18, w: 'b' });
    });
    s += T(350, 49, '= 32 bits', { size: 13, w: 'b', anchor: 'start', cls: 't-acc' });
    s += T(220, 118, 'IPv6 address: 128 bits', { size: 14, w: 'b' });
    ['2001', '0db8', '0000', '0000', '0000', '0000', '0000', '0001'].forEach((v, i) => {
      s += K.rect(8 + i * 54, 130, 48, 32, { c: 2, r: 6 }) + T(32 + i * 54, 146, v, { size: 12, w: 'b', vmid: true });
    });
    s += T(220, 180, 'eight groups x 16 bits each', { size: 11.5, cls: 't-mut' });
    s += T(220, 202, 'written short: 2001:db8::1', { size: 13, w: 'b', cls: 't-acc' });
    return K.svg(440, 214, s, { title: 'IPv4 has four 8-bit parts; IPv6 has eight 16-bit groups' });
  });

  D.register('xi1b.lan-switch', () => {
    let s = T(220, 14, 'One local network (LAN)', { size: 13.5, w: 'b' });
    s += K.rect(160, 26, 120, 40, { c: 1, r: 8 }) + T(220, 46, 'Switch', { size: 14, w: 'b', vmid: true });
    const macs = ['AA:BB:CC:DD:EE:FF', 'AA:BB:CC:DD:EE:01', 'AA:BB:CC:DD:EE:02'];
    macs.forEach((m, i) => {
      const x = 6 + i * 148;
      s += K.line(220, 66, x + 65, 112, { cls: 's-mut', w: 2 });
      s += card(x, 112, 130, 48, [0, 5, 4][i], 'PC ' + (i + 1), m, { ts: 12.5, ss: 11 });
    });
    s += T(220, 178, 'The switch delivers each frame using MAC addresses.', { size: 11.5, cls: 't-mut' });
    return K.svg(440, 188, s, { title: 'A switch connects PCs on a LAN and uses MAC addresses' });
  });

  D.register('xi1b.frame', () => {
    let s = K.polyline([[6, 34], [6, 28], [434, 28], [434, 34]], { cls: 's-mut' }) + T(220, 20, 'Frame (Layer 2 data unit)', { size: 13, w: 'b' });
    s += K.rect(6, 40, 76, 50, { c: 3, r: 0 }) + T(44, 65, 'Destination\nMAC', { size: 11, vmid: true, w: 'b' });
    s += K.rect(82, 40, 76, 50, { c: 3, r: 0 }) + T(120, 65, 'Source\nMAC', { size: 11, vmid: true, w: 'b' });
    s += K.rect(158, 40, 176, 50, { c: 5, r: 0 }) + T(246, 65, 'Packet from Network layer\n(IP header + data)', { size: 12, vmid: true, w: 'b' });
    s += K.rect(334, 40, 100, 50, { c: 4, r: 0 }) + T(384, 65, 'Trailer\nCRC', { size: 12, vmid: true, w: 'b' });
    s += T(6, 108, 'MAC header', { size: 12, w: 'b', anchor: 'start' }) + T(6, 123, 'sender + receiver MAC', { size: 11, cls: 't-mut', anchor: 'start' });
    s += T(434, 108, 'Error check', { size: 12, w: 'b', anchor: 'end' }) + T(434, 123, 'finds damaged frames', { size: 11, cls: 't-mut', anchor: 'end' });
    return K.svg(440, 134, s, { title: 'Structure of a frame: MAC header, packet and CRC trailer' });
  });

  D.register('xi1b.l1-media', () => {
    let s = T(220, 16, 'bits:', { size: 12.5, w: 'b', anchor: 'end' });
    [1, 0, 1, 1, 0].forEach((b, i) => { s += K.rect(228 + i * 28, 2, 24, 22, { c: b ? 4 : 6, r: 4 }) + T(240 + i * 28, 13, String(b), { size: 12.5, w: 'b', vmid: true }); });
    const panels = [['Copper cable', 'electrical signals'], ['Fibre-optic cable', 'light pulses'], ['Wireless', 'radio waves']];
    panels.forEach(([t, sub], i) => {
      const px = 4 + i * 146;
      s += K.rect(px, 38, 140, 132, { s: 's-mut', r: 10 });
      s += T(px + 70, 58, t, { size: 12.5, w: 'b' }) + T(px + 70, 73, sub, { size: 11.5, cls: 't-mut' });
    });
    const bits = [1, 0, 1, 1, 0];
    const yy = (b) => (b ? 104 : 138);
    let d = 'M16 ' + yy(1);
    bits.forEach((b, i) => {
      const x = 16 + i * 24;
      d += ' L' + (x + 24) + ' ' + yy(b);
      if (i < 4) d += ' L' + (x + 24) + ' ' + yy(bits[i + 1]);
    });
    s += K.path(d, { s: 's-acc', w: 2.5 });
    s += K.line(158, 120, 270, 120, { cls: 's-mut', w: 5 });
    [1, 0, 1, 1, 0].forEach((b, i) => { s += K.circle(172 + i * 22, 120, 6, { c: b ? 4 : 6, cls: b ? 'f-acc' : '' }); });
    s += K.line(334, 154, 334, 128, { w: 2.5 }) + K.poly([[334, 112], [326, 130], [342, 130]], { c: 6 });
    [10, 20, 30].forEach((r) => { s += K.path('M' + (334 - r) + ' 106 Q334 ' + (106 - r * 1.2) + ' ' + (334 + r) + ' 106', { s: 's-brand', w: 1.8 }); });
    s += K.line(398, 154, 398, 128, { w: 2.5 }) + K.poly([[398, 112], [390, 130], [406, 130]], { c: 6 });
    return K.svg(440, 180, s, { title: 'Bits travel as electrical signals, light pulses or radio waves' });
  });

  D.register('xi1b.topologies', () => {
    const cell = (cx) => cx;
    let s = '';
    const node = (x, y) => K.circle(x, y, 7, { c: 1 });
    const names = ['Star', 'Bus', 'Ring', 'Mesh'];
    names.forEach((n, i) => { s += T(55 + i * 110, 118, n, { size: 12.5, w: 'b' }); });
    // star
    let cx = 55;
    for (let k = 0; k < 5; k++) { const a = (k * 72 - 90) * Math.PI / 180; s += K.line(cx, 55, cx + 38 * Math.cos(a), 55 + 38 * Math.sin(a)); }
    for (let k = 0; k < 5; k++) { const a = (k * 72 - 90) * Math.PI / 180; s += node(cx + 38 * Math.cos(a), 55 + 38 * Math.sin(a)); }
    s += K.circle(cx, 55, 10, { c: 4 });
    // bus
    cx = 165;
    s += K.line(cx - 45, 55, cx + 45, 55, { w: 3 });
    [-35, -12, 12, 35].forEach((dx, k) => { const up = k % 2 === 0; s += K.line(cx + dx, 55, cx + dx, up ? 30 : 80) + node(cx + dx, up ? 30 : 80); });
    // ring
    cx = 275;
    s += K.circle(cx, 55, 36, {});
    for (let k = 0; k < 6; k++) { const a = (k * 60 - 90) * Math.PI / 180; s += node(cx + 36 * Math.cos(a), 55 + 36 * Math.sin(a)); }
    // mesh
    cx = 385;
    const pts = [];
    for (let k = 0; k < 5; k++) { const a = (k * 72 - 90) * Math.PI / 180; pts.push([cx + 38 * Math.cos(a), 55 + 38 * Math.sin(a)]); }
    for (let a = 0; a < 5; a++) for (let b = a + 1; b < 5; b++) s += K.line(pts[a][0], pts[a][1], pts[b][0], pts[b][1], { w: 1.2 });
    pts.forEach((p) => { s += node(p[0], p[1]); });
    return K.svg(440, 128, s, { title: 'Physical topologies: star, bus, ring and mesh' });
  });

  D.register('xi1b.sender-receiver', () => {
    let s = T(90, 18, 'SENDER', { size: 14, w: 'b' }) + T(96, 34, 'Encapsulation: headers added', { size: 11.5, cls: 't-mut' });
    s += T(350, 18, 'RECEIVER', { size: 14, w: 'b' }) + T(344, 34, 'Decapsulation: headers removed', { size: 11.5, cls: 't-mut' });
    const L = [7, 6, 5, 4, 3, 2, 1];
    L.forEach((n, i) => {
      const y = 46 + i * 52;
      const lab = n + ' ' + ON[n];
      s += card(30, y, 120, 32, OL[n], lab, null, { ts: 12, r: 6 });
      s += card(290, y, 120, 32, OL[n], lab, null, { ts: 12, r: 6 });
      s += K.line(152, y + 16, 288, y + 16, { arrow: 'both', cls: 's-mut', dash: '4 4' });
      s += T(220, y + 10, UNIT[n], { size: 12, w: 'b' });
      if (i < 6) {
        s += ARR(90, y + 32, 90, y + 52);
        s += ARR(350, y + 52, 350, y + 32);
      }
    });
    const yb = 46 + 6 * 52 + 32;
    s += K.polyline([[90, yb], [90, yb + 24], [350, yb + 24], [350, yb]], { w: 3, cls: 's-acc' });
    s += T(220, yb + 42, 'Physical medium: cable, fibre or radio', { size: 12, w: 'b' });
    return K.svg(440, yb + 54, s, { title: 'Data goes down the seven layers at the sender and up the seven layers at the receiver' });
  });

  const ENC = {
    7: ['Data', 'user creates data (URL)', 'Data', 'AH off: user sees data'],
    6: ['Data', 'encrypt, compress + PH', 'Data', 'decrypt, remove PH'],
    5: ['Data', 'session opened + SH', 'Data', 'close session, remove SH'],
    4: ['Segment', 'split data + TH (ports)', 'Segment', 'reassemble, remove TH'],
    3: ['Packet', 'add IH (source, dest IP)', 'Packet', 'read IP, remove IH'],
    2: ['Frame', 'add MH + trailer (CRC)', 'Frame', 'check CRC, remove MH + MT'],
    1: ['Bits', 'electric, light or radio', 'Bits', 'signals received as bits'],
  };
  const HN = { 7: 'AH', 6: 'PH', 5: 'SH', 4: 'TH', 3: 'IH', 2: 'MH' };

  D.register('xi1b.encap', (args) => {
    const up = args && args.dir === 'up';
    let s = T(240, 14, up ? 'Decapsulation: bottom to top, each layer removes its header' : 'Encapsulation: top to bottom, each layer adds its header', { size: 12, w: 'b', cls: up ? 't-grn' : 't-acc' });
    [7, 6, 5, 4, 3, 2, 1].forEach((n, i) => {
      const y = 26 + i * 46;
      s += K.circle(14, y + 19, 9, { c: OL[n] }) + T(14, y + 19, String(n), { size: 11, w: 'b', vmid: true });
      s += card(28, y, 84, 38, OL[n], ON[n], null, { ts: 11, r: 6 });
      let x = 118;
      if (n === 1) {
        s += K.rect(x, y + 4, 186, 30, { c: 6, r: 4 }) + T(x + 93, y + 19, '1 0 1 1 0 0 1 0 1 1 0 1 ...', { size: 12, vmid: true, w: 'b' });
      } else {
        for (let k = 7; k >= n; k--) {
          const first = k === n;
          s += K.rect(x, y + 4, 20, 30, { c: OL[k], r: 2, s: up && first ? 's-red' : undefined, dash: up && first ? '3 2' : undefined });
          s += T(x + 10, y + 19, HN[k], { size: 11, vmid: true, w: 'b' });
          x += 20;
        }
        s += K.rect(x, y + 4, 44, 30, { c: 6, r: 2 }) + T(x + 22, y + 19, 'Data', { size: 11.5, vmid: true, w: 'b' });
        x += 44;
        if (n === 2) {
          s += K.rect(x, y + 4, 22, 30, { c: 0, r: 2, s: up ? 's-red' : undefined, dash: up ? '3 2' : undefined }) + T(x + 11, y + 19, 'MT', { size: 11, vmid: true, w: 'b' });
        }
      }
      const e = ENC[n];
      s += T(316, y + 14, e[up ? 2 : 0], { size: 12.5, w: 'b', anchor: 'start', cls: up ? 't-grn' : 't-acc' });
      s += T(316, y + 30, e[up ? 3 : 1], { size: 11, anchor: 'start', cls: 't-mut' });
    });
    return K.svg(480, 26 + 7 * 46 + 6, s, { title: up ? 'Decapsulation: each layer removes its header on the way up' : 'Encapsulation: each layer adds a header on the way down' });
  });

  D.register('xi1b.tcpip-osi', () => {
    const rowY = (k) => 34 + k * 46;
    let s = T(66, 20, 'OSI Model (7)', { size: 13, w: 'b' }) + T(207, 20, 'TCP/IP Model (4)', { size: 13, w: 'b' }) + T(382, 20, 'Key protocols', { size: 13, w: 'b' });
    const oc = { 7: 1, 6: 1, 5: 1, 4: 4, 3: 5, 2: 0, 1: 0 };
    [7, 6, 5, 4, 3, 2, 1].forEach((n, k) => {
      s += card(6, rowY(k), 120, 42, oc[n], n + ' ' + ON[n], null, { ts: 12.5 });
    });
    const blocks = [
      [0, 3, 1, '4. Application', 'HTTP, HTTPS, FTP, SMTP,\nDNS, IMAP, POP3'],
      [3, 1, 4, '3. Transport', 'TCP, UDP'],
      [4, 1, 5, '2. Internet', 'IPv4, IPv6, ICMP, ARP,\nOSPF, BGP'],
      [5, 2, 0, '1. Network\nAccess', 'Ethernet, Wi-Fi (802.11),\nCables, MAC'],
    ];
    blocks.forEach(([k0, n, c, t, p]) => {
      const y = rowY(k0);
      const h = n * 46 - 4;
      s += K.line(126, y + h / 2, 144, y + h / 2, { cls: 's-mut', dash: '3 3' });
      s += card(144, y, 128, h, c, t, null, { ts: 12.5 });
      s += K.rect(284, y, 192, h, { r: 8, cls: 'cell' }) + T(380, y + h / 2, p, { size: 11.5, vmid: true });
    });
    return K.svg(480, 34 + 7 * 46 + 4, s, { title: 'TCP/IP four layers aligned with the seven OSI layers and their protocols' });
  });
})();
