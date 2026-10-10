/* XI Ch4 (Data and Analysis: Databases, ER models, MS Access) diagrams */
(function () {
  const D = Diagrams;

  /* ---------- local helpers ---------- */
  const T = (x, y, str, o) => {
    const t = K.text(x, y, str, o);
    return o && o.u ? t.replace('<text ', '<text text-decoration="underline" ') : t;
  };
  const cell = (x, y, w, h, cl) =>
    '<rect x="' + x + '" y="' + y + '" width="' + w + '" height="' + h + '" class="shape cell ' + cl + '"/>';
  const sum = (a) => a.reduce((p, c) => p + c, 0);
  const arr = (x1, y1, x2, y2, o) => K.line(x1, y1, x2, y2, Object.assign({ arrow: true }, o || {}));

  /** table: ws = column widths; o.pk = header cols underlined; o.fill(i,j) -> colour idx; o.tcls(i,j) -> text class */
  function tbl(x, y, ws, head, rows, o) {
    o = o || {};
    const rh = o.rh || 24;
    const hh = o.hh || rh;
    const sz = o.size || 12;
    const pk = o.pk || [];
    let s = '';
    let cx = x;
    ws.forEach((w, j) => {
      const hf = o.hfill && o.hfill[j] != null ? 'c' + o.hfill[j] : 'c-head';
      s += cell(cx, y, w, hh, hf);
      s += T(cx + w / 2, y + hh / 2, head[j], { size: sz, vmid: true, w: 'b', u: pk.indexOf(j) >= 0 });
      cx += w;
    });
    rows.forEach((r, i) => {
      cx = x;
      ws.forEach((w, j) => {
        const f = o.fill ? o.fill(i, j) : null;
        s += cell(cx, y + hh + i * rh, w, rh, f == null ? 'c-none' : 'c' + f);
        s += K.text(cx + w / 2, y + hh + i * rh + rh / 2, r[j], { size: sz, vmid: true, cls: o.tcls ? o.tcls(i, j) : '' });
        cx += w;
      });
    });
    return s;
  }

  /** entity card with attribute list: fields = [{n, tag}] ; tag 'PK' | 'FK' */
  function ent(x, y, w, title, fields, o) {
    o = o || {};
    let s = cell(x, y, w, 26, 'c' + (o.c == null ? 1 : o.c));
    s += K.text(x + w / 2, y + 13, title, { size: 13, vmid: true, w: 'b' });
    fields.forEach((f, i) => {
      s += cell(x, y + 26 + i * 22, w, 22, 'c-none');
      s += T(x + 8, y + 26 + i * 22 + 11, f.n, { size: 12, vmid: true, anchor: 'start', u: f.tag === 'PK' });
      if (f.tag) s += K.text(x + w - 7, y + 26 + i * 22 + 11, f.tag, { size: 11, vmid: true, anchor: 'end', w: 'b', cls: f.tag === 'PK' ? 't-grn' : 't-red' });
    });
    return s;
  }

  const frame = (x, y, w, h, r) => cell(x, y, w, h, 'c-none').replace('<rect ', '<rect rx="' + (r == null ? 6 : r) + '" ');
  const many = (x, y, dir) =>
    K.line(x + dir * 12, y, x, y - 8) + K.line(x + dir * 12, y, x, y) + K.line(x + dir * 12, y, x, y + 8);
  const one = (x, y, dir) => K.line(x + dir * 10, y - 8, x + dir * 10, y + 8);
  const diamond = (cx, cy, hw, hh, label, c) =>
    K.poly([[cx, cy - hh], [cx + hw, cy], [cx, cy + hh], [cx - hw, cy]], { c: c == null ? 2 : c }) +
    K.text(cx, cy, label, { size: 12, vmid: true, w: 'b' });
  const oval = (cx, cy, rx, ry, label, o) => {
    o = o || {};
    return K.ellipse(cx, cy, rx, ry, { c: o.c == null ? 0 : o.c }) + T(cx, cy, label, { size: 12, vmid: true, u: o.u });
  };
  const check = (x, y) =>
    cell(x, y, 12, 12, 'c-none') + K.path('M' + (x + 2) + ' ' + (y + 6) + ' L' + (x + 5) + ' ' + (y + 9.5) + ' L' + (x + 10) + ' ' + (y + 2.5), { s: 's-grn', w: 2 });
  const key = (x, y) =>
    K.circle(x, y, 4.5, { c: 4 }) + K.line(x + 4.5, y, x + 14, y) + K.line(x + 10, y, x + 10, y + 4) + K.line(x + 14, y, x + 14, y + 4);
  const tri = (x, y) => K.poly([[x - 5, y - 3], [x + 5, y - 3], [x, y + 3]], { c: 6 });
  const btn = (x, y, w, h, label, c) => K.rect(x, y, w, h, { c: c == null ? 6 : c, r: 4 }) + K.text(x + w / 2, y + h / 2, label, { size: 11, vmid: true });

  /* ============ 4.1 Data, Information, Database ============ */

  D.register('xi4.data-info', () => {
    let s = '';
    s += K.rect(8, 30, 150, 92, { c: 4 });
    s += K.text(83, 52, 'DATA', { w: 'b', size: 14 });
    s += K.text(83, 78, '80, 75, 90, 70, 85', { size: 13 });
    s += K.text(83, 104, 'raw facts and figures', { size: 12, cls: 't-mut' });
    s += arr(158, 76, 282, 76, { s: 's-brand', w: 3 });
    s += K.text(220, 62, 'Processing', { size: 13, w: 'b' });
    s += K.text(220, 98, 'sum / count', { size: 12, cls: 't-mut' });
    s += K.rect(282, 30, 150, 92, { c: 5 });
    s += K.text(357, 52, 'INFORMATION', { w: 'b', size: 14 });
    s += K.text(357, 78, 'Average = 80%', { size: 13 });
    s += K.text(357, 104, 'meaningful result', { size: 12, cls: 't-mut' });
    s += K.text(220, 158, 'Data  >  Processing  >  Information', { size: 13, cls: 't-mut' });
    s += K.text(83, 20, 'Input', { size: 12, cls: 't-mut' });
    s += K.text(357, 20, 'Output', { size: 12, cls: 't-mut' });
    return K.svg(440, 172, s, { title: 'Data is processed to become information' });
  });

  D.register('xi4.dbms-bridge', () => {
    let s = '';
    const px = 52;
    s += K.circle(px, 62, 13, { c: 3 });
    s += K.path('M' + (px - 24) + ' 112 Q' + (px - 24) + ' 82 ' + px + ' 82 Q' + (px + 24) + ' 82 ' + (px + 24) + ' 112 Z', { c: 3 });
    s += K.text(px, 134, 'User', { size: 13, w: 'b' });
    s += arr(82, 94, 152, 94, { arrow: 'both', s: 's-brand', w: 2.5 });
    s += K.rect(152, 54, 136, 80, { c: 2 });
    s += K.text(220, 82, 'DBMS', { size: 16, w: 'b' });
    s += K.text(220, 106, 'software bridge', { size: 12, cls: 't-mut' });
    s += arr(288, 94, 340, 94, { arrow: 'both', s: 's-brand', w: 2.5 });
    const cx = 392;
    s += K.path('M' + (cx - 40) + ' 66 L' + (cx - 40) + ' 122 A40 11 0 0 0 ' + (cx + 40) + ' 122 L' + (cx + 40) + ' 66', { c: 1 });
    s += K.ellipse(cx, 66, 40, 11, { c: 1 });
    s += K.text(cx, 98, 'Database', { size: 13, w: 'b' });
    s += K.text(px, 24, 'asks / enters', { size: 12, cls: 't-mut' });
    s += K.text(cx, 40, 'stores data', { size: 12, cls: 't-mut' });
    ['Insert', 'Update', 'Delete', 'Retrieve'].forEach((t, i) => {
      s += K.rect(60 + i * 90, 160, 80, 26, { c: 0, r: 13 });
      s += K.text(100 + i * 90, 173, t, { size: 13, vmid: true });
    });
    s += K.text(220, 214, 'MS Access  |  MySQL  |  Oracle  |  SQL Server', { size: 12, cls: 't-mut' });
    return K.svg(440, 226, s, { title: 'A DBMS is a bridge between the user and the database' });
  });

  D.register('xi4.redundancy', () => {
    let s = '';
    s += K.text(220, 14, 'Department table (stored once)', { size: 12, cls: 't-mut' });
    s += tbl(133, 22, [64, 120], ['DeptID', 'DeptName'], [['1', 'Computer Science']], { pk: [0], hfill: [5, null], fill: (i, j) => (j === 0 ? 5 : null) });
    const xs = [8, 155, 302];
    ['Student table', 'Exam table', 'Fee table'].forEach((t, i) => {
      s += K.rect(xs[i], 126, 130, 56, { c: 1 });
      s += K.text(xs[i] + 65, 144, t, { size: 13, w: 'b' });
      s += K.text(xs[i] + 65, 166, 'DepartmentID = 1', { size: 12 });
      s += arr(xs[i] + 65, 126, 165 + i * 55, 72, { s: 's-brand', dash: '4 3' });
    });
    s += K.text(220, 208, 'Other tables only refer to the ID: less redundancy', { size: 12, cls: 't-mut' });
    return K.svg(440, 220, s, { title: 'Department stored once, other tables refer to it by DepartmentID' });
  });

  /* ============ 4.2 Tables, records, fields ============ */

  D.register('xi4.table-anatomy', () => {
    let s = '';
    const x = 10;
    const y = 52;
    const ws = [76, 90, 56, 62];
    s += tbl(x, y, ws, ['StudentID', 'Name', 'Class', 'Marks'], [['1', 'Ali', 'XI', '85'], ['2', 'Sara', 'XI', '90'], ['3', 'Hina', 'XI', '78']], {
      rh: 28,
      pk: [0],
      hfill: [5, 0, 0, 0],
      fill: (i, j) => (i === 1 ? 4 : null),
    });
    s += K.text(x + ws[0] + ws[1] / 2 + 10, 16, 'Field (column)', { size: 13, w: 'b', cls: 't-acc' });
    s += arr(x + ws[0] + ws[1] / 2, 24, x + ws[0] + ws[1] / 2, y - 2, { s: 's-brand' });
    s += arr(352, y + 28 + 42, x + sum(ws) + 2, y + 28 + 42, { s: 's-acc', w: 2.5 });
    s += K.text(392, y + 28 + 36, 'Record', { size: 13, w: 'b', anchor: 'start' });
    s += K.text(392, y + 28 + 52, '(row)', { size: 12, anchor: 'start', cls: 't-mut' });
    const vx = x + ws[0] + ws[1] + ws[2] + ws[3] / 2;
    s += arr(vx, 196, vx, y + 28 * 4 + 2, { s: 's-mut' });
    s += K.text(vx, 212, 'one value (cell)', { size: 12, cls: 't-mut' });
    s += arr(x + ws[0] / 2, 196, x + ws[0] / 2, y + 28 * 4 + 2, { s: 's-grn' });
    s += K.text(x + ws[0] / 2 + 8, 212, 'Primary Key', { size: 12, cls: 't-grn', anchor: 'start' });
    return K.svg(450, 226, s, { title: 'A table: fields are columns, records are rows' });
  });

  /* ============ 4.3.1 Keys ============ */

  D.register('xi4.keys-emp', () => {
    let s = '';
    const ws = [70, 74, 110, 120];
    const x = 45;
    const y = 66;
    const cx = (j) => x + sum(ws.slice(0, j)) + ws[j] / 2;
    s += K.text(x + sum(ws) / 2, 16, 'Candidate Keys', { size: 14, w: 'b' });
    s += K.line(cx(0), 26, cx(3), 26, { cls: 's-mut' });
    [0, 2, 3].forEach((j) => (s += K.line(cx(j), 26, cx(j), 38, { cls: 's-mut' })));
    s += K.text(cx(0), 54, 'PK', { size: 13, w: 'b', cls: 't-grn' });
    s += K.text(cx(2), 54, 'Alternate', { size: 13, w: 'b', cls: 't-acc' });
    s += K.text(cx(3), 54, 'Alternate', { size: 13, w: 'b', cls: 't-acc' });
    s += tbl(
      x,
      y,
      ws,
      ['EmpID', 'EmpName', 'EmpLicense#', 'EmpPassport'],
      [['1001', 'Matt', 'LC1201', 'MA100LC'], ['1002', 'Maxy', 'LC2078', 'XY100LC2'], ['1003', 'Roy', 'LK00928', 'LK100RO']],
      { pk: [0], hfill: [5, null, 4, 4], fill: (i, j) => (j === 0 ? 5 : j >= 2 ? 4 : null) }
    );
    s += cell(45, 176, 14, 14, 'c5') + K.text(66, 183, 'Primary Key: the one chosen to identify records', { size: 12, anchor: 'start', vmid: true });
    s += cell(45, 198, 14, 14, 'c4') + K.text(66, 205, 'Alternate Key: candidate keys not chosen', { size: 12, anchor: 'start', vmid: true });
    return K.svg(450, 222, s, { title: 'Emp table: candidate keys, primary key and alternate keys' });
  });

  D.register('xi4.fk-link', () => {
    let s = '';
    const y = 36;
    const rh = 26;
    const emp = [['1001', 'Matt', '1'], ['1002', 'Maxy', '2'], ['1003', 'Roy', '3'], ['1004', 'Zoya', '3']];
    const dep = [['1', 'BPO'], ['2', 'Account'], ['3', 'IT']];
    s += K.text(87, 16, 'Employee (child)', { size: 13, w: 'b' });
    s += K.text(366, 16, 'Department (parent)', { size: 13, w: 'b' });
    s += tbl(10, y, [56, 62, 40], ['EmpID', 'EmpName', 'Did'], emp, { rh, hfill: [5, null, 3], fill: (i, j) => (j === 2 ? 3 : null) });
    s += tbl(290, y, [44, 106], ['Did', 'DeptName'], dep, { rh, hfill: [5, null], fill: (i, j) => (j === 0 ? 5 : null), pk: [0] });
    const cy = (i) => y + rh + rh * i + rh / 2;
    [0, 1, 2, 2].forEach((d, i) => (s += arr(168, cy(i), 288, cy(d), { s: 's-red', w: 2 })));
    s += K.text(228, 22, 'FK refers to PK', { size: 12, cls: 't-red', w: 'b' });
    s += K.text(39, 176, 'PK', { size: 12, w: 'b', cls: 't-grn' });
    s += K.text(148, 176, 'FK', { size: 12, w: 'b', cls: 't-red' });
    s += K.text(312, 154, 'PK', { size: 12, w: 'b', cls: 't-grn' });
    s += K.text(225, 196, 'FK can repeat: Roy and Zoya both belong to Did 3', { size: 12, cls: 't-mut' });
    return K.svg(450, 206, s, { title: 'Foreign key Did in Employee refers to primary key Did in Department' });
  });

  /* ============ 4.4 ER model ============ */

  D.register('xi4.er-symbols', () => {
    let s = '';
    s += K.rect(32, 26, 90, 40, { c: 1, r: 2 }) + K.text(77, 46, 'Student', { size: 14, vmid: true, w: 'b' });
    s += K.text(77, 88, 'Entity', { size: 13, w: 'b' }) + K.text(77, 104, 'rectangle', { size: 12, cls: 't-mut' });
    s += oval(228, 46, 48, 22, 'Name');
    s += K.text(228, 88, 'Attribute', { size: 13, w: 'b' }) + K.text(228, 104, 'oval', { size: 12, cls: 't-mut' });
    s += oval(386, 46, 54, 22, 'StudentID', { c: 4, u: true });
    s += K.text(386, 88, 'Key attribute', { size: 13, w: 'b' }) + K.text(386, 104, 'underlined', { size: 12, cls: 't-mut' });
    s += diamond(77, 166, 52, 26, 'Enrols');
    s += K.text(77, 216, 'Relationship', { size: 13, w: 'b' }) + K.text(77, 232, 'diamond', { size: 12, cls: 't-mut' });
    s += K.rect(160, 150, 30, 32, { c: 1, r: 2 }) + K.rect(268, 150, 30, 32, { c: 1, r: 2 });
    s += K.line(190, 166, 268, 166) + one(190, 166, 1) + many(268, 166, -1);
    s += K.text(204, 146, '1', { size: 13, w: 'b' }) + K.text(254, 146, 'M', { size: 13, w: 'b' });
    s += K.text(229, 216, 'Cardinality', { size: 13, w: 'b' }) + K.text(229, 232, "1 and M, crow's foot", { size: 12, cls: 't-mut' });
    s += K.rect(340, 152, 40, 26, { c: 5, r: 13 }) + K.text(360, 165, 'PK', { size: 13, vmid: true, w: 'b' });
    s += K.rect(392, 152, 40, 26, { c: 3, r: 13 }) + K.text(412, 165, 'FK', { size: 13, vmid: true, w: 'b' });
    s += K.text(386, 216, 'Key tags', { size: 13, w: 'b' }) + K.text(386, 232, 'Primary / Foreign', { size: 12, cls: 't-mut' });
    return K.svg(450, 242, s, { title: 'ER diagram symbols: entity, attribute, key attribute, relationship, cardinality' });
  });

  D.register('xi4.rel-types', () => {
    let s = '';
    const panels = [
      { t: 'One-to-One', code: '1:1', L: 'Student', R: 'ID Card', l: ['Ali'], r: ['C-101'], links: [[0, 0]] },
      { t: 'One-to-Many', code: '1:M', L: 'Teacher', R: 'Students', l: ['Mr. Ahmed'], r: ['Ali', 'Sara', 'Hina'], links: [[0, 0], [0, 1], [0, 2]] },
      { t: 'Many-to-Many', code: 'M:N', L: 'Students', R: 'Classes', l: ['Ali', 'Sara', 'Hina'], r: ['Math', 'Physics', 'English'], links: [[0, 0], [0, 1], [1, 1], [2, 1], [2, 2]] },
    ];
    panels.forEach((p, k) => {
      const y0 = k * 108 + 2;
      s += frame(2, y0, 446, 102, 10);
      s += K.text(12, y0 + 20, p.t, { size: 14, w: 'b', anchor: 'start' });
      s += K.text(404, y0 + 58, p.code, { size: 22, w: 'b', cls: 't-acc' });
      s += K.text(100, y0 + 40, p.L, { size: 12, cls: 't-mut' });
      s += K.text(300, y0 + 40, p.R, { size: 12, cls: 't-mut' });
      const ys = (n, i) => (n === 1 ? y0 + 70 : y0 + 52 + i * 18);
      p.links.forEach(([a, b]) => (s += K.line(160, ys(p.l.length, a), 260, ys(p.r.length, b), { cls: 's-brand', w: 2 })));
      p.l.forEach((n, i) => (s += K.dot(160, ys(p.l.length, i), 6) + K.text(150, ys(p.l.length, i), n, { size: 12, anchor: 'end', vmid: true })));
      p.r.forEach((n, i) => (s += K.dot(260, ys(p.r.length, i), 6) + K.text(270, ys(p.r.length, i), n, { size: 12, anchor: 'start', vmid: true })));
    });
    return K.svg(450, 330, s, { title: 'One-to-one, one-to-many and many-to-many relationships' });
  });

  D.register('xi4.er-school', () => {
    let s = '';
    const T1 = { x: 6, y: 100, w: 84, h: 36 };
    const C = { x: 216, y: 100, w: 90, h: 36 };
    const S = { x: 380, y: 198, w: 90, h: 36 };
    const ctr = (r) => [r.x + r.w / 2, r.y + r.h / 2];
    const [tx, ty] = ctr(T1);
    const [cx, cy] = ctr(C);
    const [sx, sy] = ctr(S);
    const dgx = 152;
    const eX = 261;
    const eY = 216;
    // attribute connectors first (shapes drawn on top)
    const attrs = [
      [48, 56, tx, ty, 'TeacherID', true],
      [48, 186, tx, ty, 'Name'],
      [190, 40, cx, cy, 'ClassID', true],
      [261, 40, cx, cy, 'Subject'],
      [332, 40, cx, cy, 'RoomNo'],
      [sx, 150, sx, sy, 'StudentID', true],
      [sx, 272, sx, sy, 'Name'],
      [196, 282, eX, eY, 'StudentID'],
      [326, 282, eX, eY, 'ClassID'],
    ];
    attrs.forEach((a) => (s += K.line(a[0], a[1], a[2], a[3])));
    s += K.line(T1.x + T1.w, ty, dgx - 38, ty) + K.line(dgx + 38, ty, C.x, cy);
    s += K.line(cx, C.y + C.h, eX, eY - 24);
    s += K.line(eX + 48, eY, S.x, sy);
    s += K.rect(T1.x, T1.y, T1.w, T1.h, { c: 1, r: 2 }) + K.text(tx, ty, 'TEACHER', { size: 13, vmid: true, w: 'b' });
    s += K.rect(C.x, C.y, C.w, C.h, { c: 1, r: 2 }) + K.text(cx, cy, 'CLASS', { size: 13, vmid: true, w: 'b' });
    s += K.rect(S.x, S.y, S.w, S.h, { c: 1, r: 2 }) + K.text(sx, sy, 'STUDENT', { size: 13, vmid: true, w: 'b' });
    s += diamond(dgx, ty, 38, 22, 'TEACHES');
    s += diamond(eX, eY, 52, 24, 'ENROLMENT');
    attrs.forEach((a) => {
      const enrol = a[1] === 282;
      s += oval(a[0], a[1], 36, 15, a[4], { c: enrol ? 4 : 0, u: a[5] });
    });
    const lab = (x, y, t) => K.text(x, y, t, { size: 13, w: 'b', cls: 't-acc' });
    s += lab(100, ty - 6, '1') + lab(190, ty - 6, 'N');
    s += lab(cx + 10, 156, '1') + lab(eX + 10, 186, 'N');
    s += lab(sx - 54, sy - 8, '1') + lab(eX + 66, eY - 8, 'N');
    return K.svg(476, 304, s, { title: 'ER diagram: Teacher teaches Class, Student enrols in Class through Enrolment' });
  });

  D.register('xi4.mn-junction', () => {
    let s = '';
    s += K.rect(20, 18, 100, 38, { c: 1, r: 2 }) + K.text(70, 37, 'Student', { size: 14, vmid: true, w: 'b' });
    s += K.rect(330, 18, 100, 38, { c: 1, r: 2 }) + K.text(380, 37, 'Class', { size: 14, vmid: true, w: 'b' });
    s += K.line(120, 37, 330, 37, { cls: 's-red', w: 2.5, dash: '6 4' });
    s += K.text(150, 30, 'M', { size: 14, w: 'b', cls: 't-red' }) + K.text(300, 30, 'N', { size: 14, w: 'b', cls: 't-red' });
    s += K.text(225, 56, 'M:N is not supported directly', { size: 13, cls: 't-red', w: 'b' });
    s += arr(225, 70, 225, 98, { s: 's-brand', w: 3 });
    s += K.text(300, 90, 'add a junction table', { size: 13, cls: 't-acc', w: 'b' });
    const y = 112;
    s += K.text(66, y - 4, 'Student', { size: 13, w: 'b' }) + K.text(225, y - 4, 'Enrolment (junction)', { size: 13, w: 'b' }) + K.text(388, y - 4, 'Class', { size: 13, w: 'b' });
    s += tbl(8, y, [40, 76], ['ID', 'Name'], [['1', 'Ali'], ['2', 'Sara']], { rh: 22, pk: [0], hfill: [5, null], fill: (i, j) => (j === 0 ? 5 : null) });
    s += tbl(165, y, [60, 60], ['StudentID', 'ClassID'], [['1', 'C1'], ['1', 'C2'], ['2', 'C1']], { rh: 22, size: 11, hfill: [3, 3], fill: () => 3 });
    s += tbl(330, y, [40, 76], ['ID', 'Subject'], [['C1', 'Math'], ['C2', 'Physics']], { rh: 22, pk: [0], hfill: [5, null], fill: (i, j) => (j === 0 ? 5 : null) });
    s += K.line(124, 146, 165, 146) + one(124, 146, 1) + many(165, 146, -1);
    s += K.line(285, 146, 330, 146) + many(285, 146, 1) + one(330, 146, -1);
    s += K.text(146, 168, '1:M', { size: 12, w: 'b', cls: 't-acc' }) + K.text(310, 168, 'M:1', { size: 12, w: 'b', cls: 't-acc' });
    s += K.text(225, 222, 'Two 1:M relationships replace one M:N', { size: 13, cls: 't-mut' });
    return K.svg(450, 234, s, { title: 'Many-to-many resolved with a junction table' });
  });

  /* ============ 4.5 Referential integrity ============ */

  D.register('xi4.ref-violation', () => {
    let s = '';
    s += K.text(90, 16, 'Student (parent)', { size: 13, w: 'b' });
    s += K.text(350, 16, 'Result (child)', { size: 13, w: 'b' });
    s += tbl(10, 26, [76, 94], ['StudentID', 'Name'], [['101', 'Ali'], ['102', 'Sara'], ['103', 'Hina']], { rh: 28, pk: [0], hfill: [5, null], fill: (i, j) => (j === 0 ? 5 : null) });
    s += tbl(270, 26, [84, 80], ['StudentID', 'Marks'], [['101', '85'], ['102', '90'], ['109', '70']], {
      rh: 28,
      hfill: [3, null],
      fill: (i, j) => (i === 2 ? 3 : j === 0 ? 3 : null),
      tcls: (i, j) => (i === 2 && j === 0 ? 't-red' : ''),
    });
    const cy = (i) => 26 + 28 + 28 * i + 14;
    s += arr(270, cy(0), 182, cy(0), { s: 's-grn', w: 2 });
    s += arr(270, cy(1), 182, cy(1), { s: 's-grn', w: 2 });
    s += K.line(270, cy(2), 214, cy(2), { cls: 's-red', w: 2, dash: '5 3' });
    s += K.line(204, cy(2) - 8, 220, cy(2) + 8, { cls: 's-red', w: 3 }) + K.line(220, cy(2) - 8, 204, cy(2) + 8, { cls: 's-red', w: 3 });
    s += K.text(225, 168, 'No student 109 in parent table!', { size: 13, w: 'b', cls: 't-red' });
    s += K.text(225, 190, 'Referential integrity blocks this orphan record', { size: 12, cls: 't-mut' });
    return K.svg(450, 204, s, { title: 'A Result row whose StudentID does not exist in Student violates referential integrity' });
  });

  function cascade(kind) {
    const upd = kind === 'update';
    const pw = [76, 64];
    const cw = [60, 76, 84];
    const px = 8;
    const ccx = 172;
    const parent = (rows, hi) =>
      tbl(px, 0, pw, ['StudentID', 'Name'], rows, { rh: 22, size: 12, pk: [0], fill: (i, j) => (hi[i] != null ? hi[i] : null), hfill: [5, null] });
    const child = (rows, hi) =>
      tbl(ccx, 0, cw, ['EnrollID', 'StudentID', 'Course'], rows, { rh: 22, size: 12, fill: (i, j) => (hi[i] != null ? hi[i] : null), hfill: [null, 3, null] });
    const block = (oy, tag, prow, phi, crow, chi) => {
      let b = '';
      b += K.text(px, 12, 'Students (Parent)', { size: 12, anchor: 'start', cls: 't-mut' });
      b += K.text(ccx, 12, 'Enrollments (Child)', { size: 12, anchor: 'start', cls: 't-mut' });
      b += K.text(440, 12, tag, { size: 13, w: 'b', anchor: 'end', cls: 't-acc' });
      b += K.g(K.g(parent(prow, phi) + child(crow, chi), { t: 'translate(0 20)' }));
      return K.g(b, { t: 'translate(0 ' + oy + ')' });
    };
    let s = '';
    const P0 = [['101', 'Ali'], ['102', 'Sara'], ['103', 'Hina']];
    const C0 = [['1', '101', 'Math'], ['2', '102', 'Physics'], ['3', '103', 'English'], ['4', '101', 'Computer']];
    if (upd) {
      s += block(0, 'BEFORE', P0, { 0: 4 }, C0, { 0: 4, 3: 4 });
      s += arr(220, 132, 220, 168, { s: 's-brand', w: 3 });
      s += K.text(228, 154, 'StudentID 101 becomes 201', { size: 13, w: 'b', anchor: 'start', cls: 't-acc' });
      s += block(176, 'AFTER', [['201', 'Ali'], ['102', 'Sara'], ['103', 'Hina']], { 0: 5 }, [['1', '201', 'Math'], ['2', '102', 'Physics'], ['3', '103', 'English'], ['4', '201', 'Computer']], { 0: 5, 3: 5 });
      s += K.text(225, 318, 'Child rows follow the parent key automatically', { size: 12, cls: 't-mut' });
    } else {
      s += block(0, 'BEFORE', P0, { 1: 3 }, C0, { 1: 3 });
      s += arr(220, 132, 220, 168, { s: 's-red', w: 3 });
      s += K.text(228, 154, 'Delete StudentID 102 (Sara)', { size: 13, w: 'b', anchor: 'start', cls: 't-red' });
      s += block(176, 'AFTER', [['101', 'Ali'], ['103', 'Hina']], {}, [['1', '101', 'Math'], ['3', '103', 'English'], ['4', '101', 'Computer']], {});
      s += K.text(225, 318, 'All of Sara\'s enrollments are deleted too', { size: 12, cls: 't-mut' });
    }
    return K.svg(450, 330, s, { title: upd ? 'Cascade update: changing a parent key updates child rows' : 'Cascade delete: deleting a parent record deletes child rows' });
  }
  D.register('xi4.cascade-update', () => cascade('update'));
  D.register('xi4.cascade-delete', () => cascade('delete'));

  /* ============ 4.6 Relational schema ============ */

  D.register('xi4.schema', () => {
    let s = '';
    s += ent(6, 10, 130, 'Student', [{ n: 'StudentID', tag: 'PK' }, { n: 'Name' }, { n: 'Class' }, { n: 'Address' }], { c: 1 });
    s += ent(168, 10, 124, 'Enrollment', [{ n: 'StudentID', tag: 'FK' }, { n: 'CourseID', tag: 'FK' }], { c: 3 });
    s += ent(324, 10, 126, 'Course', [{ n: 'CourseID', tag: 'PK' }, { n: 'CourseName' }], { c: 1 });
    s += arr(168, 47, 138, 47, { s: 's-red', w: 2 });
    s += arr(292, 69, 322, 49, { s: 's-red', w: 2 });
    s += K.text(228, 106, 'junction table', { size: 12, cls: 't-mut' });
    s += K.text(10, 156, 'Schema (text notation)', { size: 13, w: 'b', anchor: 'start', cls: 't-acc' });
    ['Student (StudentID, Name, Class, Address)', 'Course (CourseID, CourseName)', 'Enrollment (StudentID, CourseID)'].forEach((t, i) => {
      s += K.text(10, 180 + i * 22, t, { size: 13, anchor: 'start' });
    });
    return K.svg(456, 244, s, { title: 'Relational schema of Student, Course and Enrollment tables' });
  });

  /* ============ 4.7 Library case study ============ */

  D.register('xi4.er-steps', () => {
    let s = '';
    const steps = [
      ['Requirement Analysis', 'books, members, dates'],
      ['Identify Entities', 'Book, Member'],
      ['Identify Attributes', 'BookID, Title, Author, ...'],
      ['Identify Relationships', 'a Member borrows a Book'],
      ['Determine Cardinality', 'Member M : N Book'],
      ['Resolve Many-to-Many', 'new entity BorrowRecord'],
      ['Final ER Schema', 'Member 1:M Record M:1 Book'],
    ];
    steps.forEach((st, i) => {
      const y = 6 + i * 46;
      s += K.rect(6, y, 214, 34, { c: i === 5 ? 4 : i === 6 ? 5 : 0, r: 8 });
      s += K.circle(26, y + 17, 11, { c: 6 });
      s += K.text(26, y + 17, String(i + 1), { size: 13, vmid: true, w: 'b' });
      s += K.text(44, y + 17, st[0], { size: 13, vmid: true, anchor: 'start', w: 'b' });
      s += K.text(232, y + 17, st[1], { size: 12, vmid: true, anchor: 'start', cls: 't-mut' });
      if (i < steps.length - 1) s += arr(113, y + 34, 113, y + 46, { s: 's-brand', w: 2 });
    });
    return K.svg(450, 330, s, { title: 'Seven steps of ER design with the library example' });
  });

  D.register('xi4.er-library-chen', () => {
    let s = '';
    const B = [20, 150, 84, 36];
    const M = [376, 150, 84, 36];
    const bc = [62, 168];
    const mc = [418, 168];
    const dcx = 240;
    const at = [
      [44, 40, bc, 'BookID', 1],
      [140, 40, bc, 'Title'],
      [44, 296, bc, 'Author'],
      [140, 296, bc, 'Publisher'],
      [340, 40, mc, 'MemberID', 1],
      [430, 40, mc, 'ContactInfo'],
      [380, 296, mc, 'Name'],
    ];
    at.forEach((a) => (s += K.line(a[0], a[1], a[2][0], a[2][1])));
    s += K.line(B[0] + B[2], 168, dcx - 56, 168) + K.line(dcx + 56, 168, M[0], 168);
    s += K.rect(B[0], B[1], B[2], B[3], { c: 1, r: 2 }) + K.text(bc[0], bc[1], 'Book', { size: 14, vmid: true, w: 'b' });
    s += K.rect(M[0], M[1], M[2], M[3], { c: 1, r: 2 }) + K.text(mc[0], mc[1], 'Member', { size: 14, vmid: true, w: 'b' });
    s += diamond(dcx, 168, 56, 28, 'Borrows');
    at.forEach((a) => (s += oval(a[0], a[1], a[3] === 'ContactInfo' ? 42 : 38, 16, a[3], { c: a[4] ? 4 : 0, u: !!a[4] })));
    s += K.text(130, 160, 'M', { size: 14, w: 'b', cls: 't-acc' }) + K.text(342, 160, 'N', { size: 14, w: 'b', cls: 't-acc' });
    s += K.text(240, 232, 'M:N', { size: 20, w: 'b', cls: 't-red' });
    s += K.text(240, 252, 'needs a junction entity', { size: 12, cls: 't-mut' });
    return K.svg(476, 320, s, { title: 'Library ER diagram: Member borrows Book (many-to-many)' });
  });

  D.register('xi4.er-library-final', () => {
    let s = '';
    const dy = 68;
    s += K.line(98, dy, 186, dy) + K.line(302, dy, 384, dy);
    s += ent(2, 22, 96, 'Book', [{ n: 'BookID', tag: 'PK' }, { n: 'Title' }, { n: 'Author' }, { n: 'Publisher' }], { c: 1 });
    s += ent(186, 22, 116, 'BorrowRecord', [{ n: 'BorrowID', tag: 'PK' }, { n: 'MemberID', tag: 'FK' }, { n: 'BookID', tag: 'FK' }], { c: 4 });
    s += ent(384, 22, 96, 'Member', [{ n: 'MemberID', tag: 'PK' }, { n: 'Name' }, { n: 'ContactInfo' }], { c: 1 });
    s += one(98, dy, 1) + many(186, dy, -1) + many(302, dy, 1) + one(384, dy, -1);
    s += diamond(142, dy, 28, 20, 'Borrows').replace(/font-size="12"/, 'font-size="11"');
    s += diamond(343, dy, 28, 20, 'Borrows').replace(/font-size="12"/, 'font-size="11"');
    const lab = (x, t) => K.text(x, dy + 20, t, { size: 13, w: 'b', cls: 't-acc' });
    s += lab(106, '1') + lab(178, 'M') + lab(314, 'M') + lab(376, '1');
    s += K.text(241, 14, 'Book 1:M BorrowRecord M:1 Member', { size: 12, cls: 't-mut' });
    s += K.text(10, 158, 'PK = Primary Key', { size: 12, anchor: 'start', w: 'b', cls: 't-grn' });
    s += K.text(166, 158, 'FK = Foreign Key', { size: 12, anchor: 'start', w: 'b', cls: 't-red' });
    s += K.text(322, 158, 'M = Many', { size: 12, anchor: 'start', w: 'b', cls: 't-acc' });
    return K.svg(482, 170, s, { title: 'Final ER diagram of the library system with BorrowRecord junction entity' });
  });

  /* ============ 4.8 Database objects and MS Access ============ */

  D.register('xi4.objects', () => {
    let s = '';
    const xs = [2, 120, 238, 356];
    const items = [
      ['Form', 'enter data', 2],
      ['Table', 'store data', 0],
      ['Query', 'retrieve data', 1],
      ['Report', 'present data', 4],
    ];
    items.forEach((it, i) => {
      const x = xs[i];
      s += K.rect(x, 20, 94, 120, { c: it[2], r: 10 });
      s += K.text(x + 47, 124, it[0], { size: 15, w: 'b' });
      s += K.text(x + 47, 162, it[1], { size: 12, cls: 't-mut' });
      if (i < 3) s += arr(x + 96, 80, x + 116, 80, { s: 's-brand', w: 2.5 });
    });
    // icons
    s += cell(16, 34, 66, 14, 'c-none') + cell(16, 52, 66, 14, 'c-none') + cell(16, 70, 40, 14, 'c-none') + K.rect(58, 70, 24, 14, { c: 4, r: 3 }) + cell(16, 90, 66, 14, 'c-none');
    s += cell(134, 36, 66, 14, 'c-head') + cell(134, 50, 22, 42, 'c-none') + cell(156, 50, 22, 42, 'c-none') + cell(178, 50, 22, 42, 'c-none') + cell(134, 78, 66, 14, 'c-none');
    s += K.circle(268, 62, 16, { c: 6 }) + K.line(280, 74, 292, 90, { w: 4 }) + K.line(252, 100, 296, 100, { cls: 's-mut' }) + K.line(252, 108, 286, 108, { cls: 's-mut' });
    s += K.rect(376, 34, 54, 72, { c: 6, r: 3 }) + K.line(384, 48, 422, 48, { cls: 's-mut' }) + K.line(384, 60, 422, 60, { cls: 's-mut' }) + K.line(384, 72, 410, 72, { cls: 's-mut' }) + K.rect(384, 82, 38, 16, { c: 4, r: 2 });
    s += K.text(225, 190, 'Tables hold the data; the other three objects depend on them', { size: 12, cls: 't-mut' });
    return K.svg(452, 204, s, { title: 'Four database objects: Form, Table, Query, Report' });
  });

  D.register('xi4.access-window', () => {
    let s = '';
    s += frame(2, 2, 476, 336, 8);
    s += cell(2, 2, 476, 24, 'c-head') + K.text(240, 14, 'StudentDB.accdb : Database - Access', { size: 12, vmid: true, w: 'b' });
    const tabs = [['File', 10, 40], ['Home', 54, 46], ['Create', 104, 58], ['External Data', 166, 92], ['Database Tools', 262, 100], ['Help', 366, 40]];
    tabs.forEach(([t, x, w]) => {
      s += cell(x, 30, w, 20, t === 'Create' ? 'c4' : 'c-none') + K.text(x + w / 2, 40, t, { size: 12, vmid: true, w: t === 'Create' ? 'b' : '' });
    });
    s += K.text(440, 40, 'Ribbon', { size: 12, cls: 't-mut', vmid: true });
    s += cell(6, 52, 468, 78, 'c-head');
    const groups = [
      ['Tables', 12, 112, 0, ['Table', 'Table\nDesign']],
      ['Queries', 130, 108, 1, ['Query\nWizard', 'Query\nDesign']],
      ['Forms', 244, 168, 2, ['Form', 'Form\nDesign', 'Form\nWizard']],
      ['Reports', 418, 54, 3, ['Report']],
    ];
    groups.forEach(([n, x, w, c, bs]) => {
      s += frame(x, 56, w, 70, 4);
      bs.forEach((b, i) => (s += K.rect(x + 4 + i * 54, 60, 48, 40, { c: c, r: 4 }) + K.text(x + 28 + i * 54, 80, b, { size: 11, vmid: true })));
      s += K.text(x + w / 2, 115, n, { size: 11, cls: 't-mut' });
    });
    s += cell(6, 134, 130, 200, 'c-none') + cell(6, 134, 130, 22, 'c-head') + K.text(71, 145, 'All Access Objects', { size: 11, vmid: true, w: 'b' });
    [['Tables', 176, 1], ['Students', 194, 0], ['Queries', 218, 1], ['Forms', 242, 1], ['Reports', 266, 1]].forEach(([t, y, b]) => {
      s += K.text(b ? 16 : 30, y, t, { size: 12, anchor: 'start', w: b ? 'b' : '' });
    });
    s += K.text(71, 322, 'Navigation Pane', { size: 11, cls: 't-mut' });
    s += cell(142, 134, 332, 200, 'c-none') + cell(146, 138, 76, 20, 'c4') + K.text(184, 148, 'Students', { size: 12, vmid: true, w: 'b' });
    s += tbl(152, 168, [72, 100, 130], ['StudentID', 'StudentName', 'Department'], [['1', 'Ali Raza', 'Computer Science'], ['2', 'Sara Khan', 'Software Eng.'], ['3', 'Ahmed Ali', 'Computer Science']], { rh: 24, size: 11 });
    s += K.text(308, 322, 'Work area: tables, forms, queries, reports open here', { size: 11, cls: 't-mut' });
    return K.svg(480, 342, s, { title: 'MS Access window: ribbon, navigation pane and work area' });
  });

  D.register('xi4.datasheet-view', () => {
    let s = '';
    const ws = [44, 100, 56, 100];
    const mk = (y, head, hi) =>
      tbl(40, y, ws, head, [['1', 'John', '21', 'BCA'], ['2', 'Priya', '22', 'BCOM'], ['3', 'Rahul', '20', 'BBA'], ['*', '(New)', '', '']], { rh: 22, hfill: hi ? [null, 4, 4, 4] : [null, null, null, null], tcls: (i, j) => (i === 3 ? 't-mut' : '') });
    s += K.text(225, 16, 'Step 1: new table opens in Datasheet View', { size: 13, w: 'b' });
    s += mk(26, ['ID', 'Field1', 'Field2', 'Field3'], false);
    s += arr(225, 144, 225, 174, { s: 's-brand', w: 3 });
    s += K.text(236, 164, 'double-click header, type new name', { size: 12, anchor: 'start', cls: 't-acc' });
    s += K.text(225, 192, 'Step 2: fields renamed', { size: 13, w: 'b' });
    s += mk(200, ['ID', 'Name', 'Age', 'Course'], true);
    return K.svg(450, 322, s, { title: 'Creating a table in Datasheet View and renaming fields' });
  });

  D.register('xi4.design-view', () => {
    let s = '';
    s += cell(6, 4, 76, 20, 'c4') + K.text(44, 14, 'Students', { size: 12, vmid: true, w: 'b' });
    const ws = [34, 100, 100, 220];
    const rows = [
      ['', 'StudentID', 'AutoNumber', 'Unique student ID'],
      ['', 'Name', 'Short Text', 'Student full name'],
      ['', 'Department', 'Short Text', 'Student department'],
      ['', 'Age', 'Number', 'Student age in years'],
      ['', 'Email', 'Short Text', 'Student email address'],
    ];
    s += tbl(6, 28, ws, ['', 'Field Name', 'Data Type', 'Description (Optional)'], rows, { rh: 22, size: 12, fill: (i, j) => (i === 1 ? 4 : null), tcls: () => '' });
    s += key(14, 61);
    s += cell(6, 172, 454, 124, 'c-none');
    s += cell(6, 172, 454, 20, 'c-head') + K.text(14, 182, 'Field Properties (field: Name)', { size: 12, vmid: true, w: 'b', anchor: 'start' });
    s += cell(330, 175, 56, 14, 'c4') + K.text(358, 182, 'General', { size: 11, vmid: true }) + cell(390, 175, 56, 14, 'c-none') + K.text(418, 182, 'Lookup', { size: 11, vmid: true });
    const props = [['Field Size', '255'], ['Caption', 'Student Name'], ['Validation Rule', 'Is Not Null'], ['Validation Text', 'Name is required.'], ['Required', 'No'], ['Allow Zero Length', 'No']];
    props.forEach((p, i) => {
      s += K.text(14, 205 + i * 15, p[0], { size: 11, anchor: 'start', vmid: true, cls: 't-mut' });
      s += K.text(150, 205 + i * 15, p[1], { size: 11, anchor: 'start', vmid: true });
    });
    s += K.text(250, 262, 'Rules keep the data clean', { size: 11, cls: 't-acc', anchor: 'start', w: 'b' });
    s += key(252, 280) + K.text(274, 281, 'Primary Key', { size: 11, anchor: 'start', vmid: true });
    return K.svg(466, 302, s, { title: 'Table Design View: field names, data types, descriptions and field properties' });
  });

  /* ============ 4.10 Forms ============ */

  D.register('xi4.form-anatomy', () => {
    let s = '';
    s += frame(6, 4, 298, 330, 6);
    s += cell(6, 4, 298, 28, 'c-head') + K.text(155, 18, 'STUDENT REGISTRATION FORM', { size: 12, vmid: true, w: 'b' });
    const lab = (y, t) => K.text(16, y, t, { size: 12, anchor: 'start', vmid: true });
    const inp = (y, t, w) => cell(112, y - 11, w || 180, 22, 'c-none') + (t ? K.text(118, y, t, { size: 11, anchor: 'start', vmid: true, cls: 't-mut' }) : '');
    s += lab(52, 'Student ID:') + inp(52, '');
    s += lab(84, 'Full Name:') + inp(84, 'Ali Hassan');
    s += lab(116, 'Gender:');
    ['Male', 'Female', 'Other'].forEach((g, i) => {
      s += K.circle(120 + i * 62, 116, 6, { c: i === 0 ? 4 : null }) + K.text(130 + i * 62, 116, g, { size: 11, anchor: 'start', vmid: true });
    });
    s += lab(148, 'Department:') + inp(148, 'Computer Science') + tri(280, 148);
    s += lab(180, 'Hobbies:');
    ['Reading', 'Sports', 'Music'].forEach((g, i) => {
      s += check(112 + i * 62, 174) + K.text(128 + i * 62, 180, g, { size: 11, anchor: 'start', vmid: true });
    });
    s += lab(214, 'Date of Birth:') + inp(214, '15-08-2006', 120) + cell(236, 203, 28, 22, 'c4') + K.text(250, 214, 'cal', { size: 11, vmid: true });
    s += lab(262, 'Address:') + cell(112, 240, 180, 46, 'c-none') + K.text(118, 252, 'House No. A-123,', { size: 11, anchor: 'start', vmid: true, cls: 't-mut' }) + K.text(118, 268, 'Gulshan-e-Iqbal, Karachi', { size: 11, anchor: 'start', vmid: true, cls: 't-mut' });
    [['Submit', 12, 5], ['Update', 82, 0], ['Reset', 152, 6], ['Delete', 222, 3]].forEach(([t, x, c]) => {
      s += btn(x, 300, 66, 26, t, c);
    });
    const call = (y, n, t1, t2) => {
      let c = K.circle(322, y, 10, { c: 4 }) + K.text(322, y, String(n), { size: 12, vmid: true, w: 'b' });
      const two = t2 && t2.indexOf('\n') > 0;
      c += K.text(340, t2 ? y - (two ? 14 : 8) : y, t1, { size: 12, anchor: 'start', vmid: true, w: 'b' });
      if (t2) c += K.text(340, y + (two ? 6 : 8), t2, { size: 11, anchor: 'start', vmid: true, cls: 't-mut', lh: 13 });
      return c;
    };
    s += call(52, 1, 'Label', 'names the field');
    s += call(84, 2, 'Text Box', 'type text or numbers');
    s += call(116, 3, 'Radio Buttons', 'select only one');
    s += call(148, 4, 'Combo List', 'predefined options');
    s += call(180, 5, 'Check Boxes', 'many selections');
    s += call(214, 6, 'Date Picker', 'avoids wrong format');
    s += call(262, 7, 'Text Area', 'long, multi-line text');
    s += call(316, 8, 'Buttons', 'Submit, Update,\nReset, Delete');
    return K.svg(480, 340, s, { title: 'Components of a database form' });
  });

  D.register('xi4.form-layouts', () => {
    let s = '';
    const names = [['Columnar', 'one record at a time'], ['Tabular', 'many records in rows'], ['Datasheet', 'spreadsheet style'], ['Justified', 'compact arrangement']];
    names.forEach((n, k) => {
      const x = 4 + k * 112;
      s += frame(x, 8, 104, 112, 6);
      if (k === 0) {
        for (let i = 0; i < 4; i++) s += K.rect(x + 8, 18 + i * 25, 30, 9, { c: 4, r: 2 }) + cell(x + 42, 15 + i * 25, 54, 15, 'c-none');
      } else if (k === 1) {
        for (let j = 0; j < 3; j++) s += cell(x + 8 + j * 29, 16, 29, 14, 'c4');
        for (let i = 0; i < 4; i++) for (let j = 0; j < 3; j++) s += cell(x + 8 + j * 29, 30 + i * 22, 29, 22, 'c-none');
      } else if (k === 2) {
        for (let i = 0; i < 6; i++) for (let j = 0; j < 4; j++) s += cell(x + 6 + j * 23, 14 + i * 16, 23, 16, i === 0 ? 'c-head' : 'c-none');
      } else {
        const rows = [[28, 52], [40, 40], [92], [28, 64], [92]];
        let yy = 16;
        rows.forEach((r) => {
          let xx = x + 6;
          r.forEach((w) => {
            s += K.rect(xx, yy, w - 4, 8, { c: 4, r: 2 }) + cell(xx, yy + 9, w - 4, 11, 'c-none');
            xx += w;
          });
          yy += 21;
        });
      }
      s += K.text(x + 52, 140, n[0], { size: 13, w: 'b' }) + K.text(x + 52, 156, n[1], { size: 11, cls: 't-mut' });
    });
    return K.svg(456, 168, s, { title: 'Four Access form layouts: columnar, tabular, datasheet, justified' });
  });

  D.register('xi4.wizard-dialog', () => {
    let s = '';
    s += frame(4, 4, 432, 246, 6);
    s += cell(4, 4, 432, 24, 'c-head') + K.text(220, 16, 'Form Wizard', { size: 13, vmid: true, w: 'b' });
    s += K.text(14, 44, 'Which fields do you want on your form?', { size: 12, anchor: 'start' });
    s += K.text(14, 68, 'Tables/Queries:', { size: 12, anchor: 'start', vmid: true, cls: 't-mut' });
    s += cell(116, 57, 170, 22, 'c-none') + K.text(124, 68, 'Table: Student', { size: 12, anchor: 'start', vmid: true }) + tri(274, 68);
    s += K.text(14, 98, 'Available Fields:', { size: 12, anchor: 'start', cls: 't-mut' }) + K.text(288, 98, 'Selected Fields:', { size: 12, anchor: 'start', cls: 't-mut' });
    s += cell(14, 104, 140, 92, 'c-none') + cell(288, 104, 140, 92, 'c-none');
    ['CNIC', 'Department', 'ContactNumber'].forEach((f, i) => (s += (i === 0 ? cell(14, 104, 140, 22, 'c4') : '') + K.text(22, 115 + i * 22, f, { size: 12, anchor: 'start', vmid: true })));
    ['StudentID', 'StudentName', 'FatherName'].forEach((f, i) => (s += K.text(296, 115 + i * 22, f, { size: 12, anchor: 'start', vmid: true })));
    [['>', 0], ['>>', 1], ['<', 2], ['<<', 3]].forEach(([t, i]) => (s += btn(176, 104 + i * 24, 88, 20, t, t === '>>' ? 4 : 6)));
    s += K.text(220, 214, '>  add one field     >>  add all fields', { size: 11, cls: 't-mut' });
    [['Cancel', 106], ['< Back', 172], ['Next >', 238], ['Finish', 304]].forEach(([t, x]) => (s += btn(x, 222, 60, 22, t, t === 'Next >' ? 5 : 6)));
    return K.svg(440, 256, s, { title: 'Form Wizard dialog: choose fields from the Student table' });
  });

  D.register('xi4.student-form', () => {
    let s = '';
    s += frame(4, 4, 432, 270, 6);
    s += cell(4, 4, 432, 24, 'c-head') + cell(10, 7, 150, 21, 'c4') + K.text(85, 18, 'StudentRegistration', { size: 12, vmid: true, w: 'b' });
    const rows = [['StudentID', '1'], ['StudentName', 'Ali Hassan'], ['FatherName', 'Muhammad Iqbal'], ['CNIC', '42101-1234567-1'], ['Department', 'Computer Science'], ['ContactNumber', '0301-2345678']];
    rows.forEach(([l, v], i) => {
      const y = 54 + i * 30;
      s += K.text(24, y, l, { size: 12, anchor: 'start', vmid: true, w: 'b' });
      s += cell(150, y - 11, 260, 22, 'c-none') + K.text(158, y, v, { size: 12, anchor: 'start', vmid: true });
    });
    s += cell(4, 240, 432, 34, 'c-head');
    s += K.text(14, 257, 'Record:', { size: 12, anchor: 'start', vmid: true });
    [['|<', 66], ['<', 92], ['>', 178], ['>|', 204], ['>*', 230]].forEach(([t, x]) => (s += btn(x, 246, 22, 22, t, 6)));
    s += cell(120, 246, 54, 22, 'c-none') + K.text(147, 257, '1 of 20', { size: 11, vmid: true });
    s += cell(262, 246, 70, 22, 'c-none') + K.text(297, 257, 'No Filter', { size: 11, vmid: true, cls: 't-mut' });
    s += cell(338, 246, 92, 22, 'c-none') + K.text(384, 257, 'Search', { size: 11, vmid: true, cls: 't-mut' });
    return K.svg(440, 280, s, { title: 'Student registration form made with Form Wizard (columnar layout)' });
  });

  /* ============ 4.11 Queries ============ */

  function qgrid(kind) {
    const cfg = {
      select: { f: ['StudentName', 'Department'], c: ['', ''], o: ['', ''], note: 'No criteria: every record is shown', hi: [] },
      single: { f: ['StudentName', 'Department'], c: ['', '"Computer Science"'], o: ['', ''], note: 'Single criterion: only Computer Science students', hi: [[4, 1]] },
      or: { f: ['Department', 'StudentName'], c: ['"IT"', ''], o: ['"Computer Science"', ''], note: 'Criteria on different rows = OR\nIT or Computer Science', hi: [[4, 0], [5, 0]] },
      and: { f: ['Department', 'StudentName'], c: ['"IT"', '"Aslam"'], o: ['', ''], note: 'Criteria on the same row = AND\nIT department and name Aslam', hi: [[4, 0], [4, 1]] },
      or2: { f: ['Department', 'StudentName'], c: ['"IT"', ''], o: ['', '"Aslam"'], note: 'Criteria on different rows = OR\nIT department or name Aslam', hi: [[4, 0], [5, 1]] },
    }[kind];
    let s = '';
    const lw = 56;
    const cw = 190;
    const rh = 26;
    const y = 30;
    s += K.text(10, 14, 'Query Design grid', { size: 13, w: 'b', anchor: 'start', cls: 't-acc' });
    const labels = ['Field:', 'Table:', 'Sort:', 'Show:', 'Criteria:', 'or:'];
    const vals = [cfg.f, ['Students', 'Students'], ['', ''], ['', ''], cfg.c, cfg.o];
    labels.forEach((l, i) => {
      s += cell(6, y + i * rh, lw, rh, 'c-head') + K.text(6 + lw - 6, y + i * rh + rh / 2, l, { size: 11, vmid: true, anchor: 'end', w: 'b' });
      [0, 1].forEach((j) => {
        const hi = cfg.hi.some((h) => h[0] === i && h[1] === j);
        s += cell(6 + lw + j * cw, y + i * rh, cw, rh, hi ? 'c4' : 'c-none');
        if (i === 3) s += check(6 + lw + j * cw + cw / 2 - 6, y + i * rh + 7);
        else s += K.text(6 + lw + j * cw + cw / 2, y + i * rh + rh / 2, vals[i][j], { size: 12, vmid: true, w: i === 0 ? 'b' : '' });
      });
    });
    s += K.text(225, y + 6 * rh + 22, cfg.note, { size: 13, w: 'b', cls: 't-acc', lh: 18 });
    return K.svg(440, y + 6 * rh + (cfg.note.indexOf('\n') > 0 ? 62 : 44), s, { title: 'Access query design grid: ' + kind });
  }
  ['select', 'single', 'or', 'and', 'or2'].forEach((k) => D.register('xi4.qgrid-' + k, () => qgrid(k)));

  D.register('xi4.query-filter', () => {
    let s = '';
    const data = [['Ali Raza', 'Computer Science'], ['Sara Khan', 'Software Engineering'], ['Ahmed Ali', 'Computer Science'], ['Fatima Noor', 'Information Technology'], ['Usman Tariq', 'Software Engineering']];
    s += K.text(10, 14, 'Students table (all records)', { size: 13, w: 'b', anchor: 'start' });
    s += tbl(10, 22, [120, 200], ['StudentName', 'Department'], data, { rh: 24, fill: (i) => (data[i][1] === 'Computer Science' ? 5 : null), tcls: (i) => (data[i][1] === 'Computer Science' ? '' : 't-mut') });
    s += K.poly([[130, 176], [250, 176], [200, 204], [180, 204]], { c: 4 });
    s += K.text(190, 190, 'Criteria', { size: 12, vmid: true, w: 'b' });
    s += K.text(262, 190, 'Department =\n"Computer Science"', { size: 12, anchor: 'start', cls: 't-acc', w: 'b', vmid: true });
    s += arr(190, 204, 190, 226, { s: 's-brand', w: 2.5 });
    s += K.text(10, 244, 'Query result', { size: 13, w: 'b', anchor: 'start' });
    s += tbl(10, 252, [120, 200], ['StudentName', 'Department'], [data[0], data[2]], { rh: 24, fill: () => 5 });
    return K.svg(440, 332, s, { title: 'A query keeps only records that match the criteria' });
  });

  D.register('xi4.groupby', () => {
    let s = '';
    const rows = [['S1', 'Computer Science'], ['S3', 'Computer Science'], ['S5', 'Computer Science'], ['S2', 'IT'], ['S6', 'IT'], ['S4', 'Software Engineering'], ['S7', 'Software Engineering']];
    const col = [0, 0, 0, 1, 1, 2, 2];
    s += K.text(10, 14, 'Student table', { size: 13, w: 'b', anchor: 'start' });
    s += tbl(8, 22, [50, 150], ['ID', 'Department'], rows, { rh: 24, fill: (i) => col[i] });
    s += K.text(300, 14, 'Query result', { size: 13, w: 'b', anchor: 'start' });
    s += tbl(252, 22, [138, 62], ['Department', 'Count'], [['Computer Science', '3'], ['IT', '2'], ['Software Engineering', '2']], { rh: 24, size: 12, fill: (i) => i });
    const yc = (i) => 22 + 24 + (i === 0 ? 36 : i === 1 ? 96 : 144);
    [[0, 0], [1, 1], [2, 2]].forEach(([g, r]) => (s += arr(210, yc(g), 250, 22 + 24 + r * 24 + 12, { s: 's-brand', w: 2.2 })));
    s += K.text(10, 238, 'Total row:  Department = Group By,   ID = Count', { size: 13, w: 'b', anchor: 'start', cls: 't-acc' });
    s += K.text(10, 260, 'Same department values are combined into one group', { size: 12, anchor: 'start', cls: 't-mut' });
    return K.svg(446, 272, s, { title: 'Group By combines records of the same department and counts them' });
  });

  /* ============ 4.11.5 Statistics ============ */

  D.register('xi4.mean-calc', () => {
    let s = '';
    const vals = [80, 75, 90, 70, 85];
    const base = 168;
    const sc = 1.4;
    s += K.line(36, base, 440, base, { cls: 's-mut' }) + K.line(36, base, 36, 20, { cls: 's-mut' });
    vals.forEach((v, i) => {
      const x = 52 + i * 70;
      s += K.rect(x, base - v * sc, 48, v * sc, { c: v >= 80 ? 5 : 4, r: 3 });
      s += K.text(x + 24, base - v * sc + 18, String(v), { size: 13, w: 'b' });
      s += K.text(x + 24, base + 16, 'Test ' + (i + 1), { size: 12, cls: 't-mut' });
    });
    const ay = base - 80 * sc;
    s += K.line(36, ay, 440, ay, { cls: 's-red', w: 2, dash: '6 4' });
    s += K.text(442, ay - 6, 'mean = 80', { size: 12, anchor: 'end', w: 'b', cls: 't-red' });
    s += K.text(225, 208, 'Sum = 400, n = 5,  Mean = 400 / 5 = 80', { size: 13, w: 'b' });
    return K.svg(446, 222, s, { title: 'Five marks and their mean of 80 shown as a dashed line' });
  });

  /* ============ 4.11.6 Charts ============ */

  const axes = (x0, y0, x1, y1) => K.line(x0, y0, x1, y0, { cls: 's-mut' }) + K.line(x0, y0, x0, y1, { cls: 's-mut' });

  D.register('xi4.chart-bar', () => {
    let s = '';
    const d = [['English', 78, 0], ['Urdu', 85, 1], ['Maths', 92, 2], ['Science', 70, 3]];
    s += K.text(225, 16, 'Marks obtained by a student out of 100', { size: 13, w: 'b' });
    s += axes(80, 190, 420, 30);
    [0, 25, 50, 75, 100].forEach((v) => {
      const x = 80 + v * 3.2;
      s += K.line(x, 190, x, 194, { cls: 's-mut' }) + K.text(x, 208, String(v), { size: 11, cls: 't-mut' });
    });
    d.forEach(([n, v, c], i) => {
      const y = 38 + i * 38;
      s += K.rect(80, y, v * 3.2, 28, { c: c, r: 3 });
      s += K.text(72, y + 14, n, { size: 12, anchor: 'end', vmid: true });
      s += K.text(80 + v * 3.2 + 6, y + 14, String(v), { size: 12, anchor: 'start', vmid: true, w: 'b' });
    });
    s += K.text(250, 226, 'Marks', { size: 12, cls: 't-mut' });
    return K.svg(446, 236, s, { title: 'Bar chart: horizontal bars compare subject marks' });
  });

  D.register('xi4.chart-column', () => {
    let s = '';
    const d = [['Accountancy', 41], ['Economics', 37], ['Maths', 29], ['Science', 39]];
    s += K.text(225, 16, 'Lectures taken by Teacher A', { size: 13, w: 'b' });
    s += axes(46, 180, 430, 30);
    [0, 10, 20, 30, 40, 50].forEach((v) => {
      const y = 180 - v * 3;
      s += K.line(42, y, 46, y, { cls: 's-mut' }) + K.text(38, y, String(v), { size: 11, anchor: 'end', vmid: true, cls: 't-mut' });
    });
    d.forEach(([n, v], i) => {
      const x = 66 + i * 92;
      s += K.rect(x, 180 - v * 3, 56, v * 3, { c: i, r: 3 });
      s += K.text(x + 28, 180 - v * 3 - 6, String(v), { size: 13, w: 'b' });
      s += K.text(x + 28, 198, n, { size: 12 });
    });
    return K.svg(446, 210, s, { title: 'Column chart: vertical bars compare lectures per subject' });
  });

  D.register('xi4.chart-pie', () => {
    let s = '';
    const d = [['Computer Science', 40, 0], ['IT', 25, 1], ['Software Engineering', 20, 2], ['Others', 15, 4]];
    const cx = 100;
    const cy = 112;
    const r = 84;
    let a0 = -Math.PI / 2;
    d.forEach(([n, p, c], i) => {
      const a1 = a0 + (p / 100) * Math.PI * 2;
      const pt = (a) => [cx + r * Math.cos(a), cy + r * Math.sin(a)];
      const [x0, y0] = pt(a0);
      const [x1, y1] = pt(a1);
      s += K.path('M' + cx + ' ' + cy + ' L' + x0.toFixed(1) + ' ' + y0.toFixed(1) + ' A' + r + ' ' + r + ' 0 ' + (p > 50 ? 1 : 0) + ' 1 ' + x1.toFixed(1) + ' ' + y1.toFixed(1) + ' Z', { c: c });
      const am = (a0 + a1) / 2;
      s += K.text(cx + r * 0.6 * Math.cos(am), cy + r * 0.6 * Math.sin(am), p + '%', { size: 13, w: 'b', vmid: true });
      s += K.rect(216, 56 + i * 32, 16, 16, { c: c, r: 3 }) + K.text(240, 64 + i * 32, n, { size: 12, anchor: 'start', vmid: true });
      a0 = a1;
    });
    s += K.text(330, 30, 'Students by department', { size: 13, w: 'b' });
    return K.svg(446, 208, s, { title: 'Pie chart: share of students in each department' });
  });

  D.register('xi4.chart-line', () => {
    let s = '';
    const m = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct'];
    const v = [33, 63, 28, 30, 35, 12, 20, 50, 80, 25];
    const X = (i) => 56 + i * 38;
    const Y = (k) => 180 - k * 1.7;
    s += K.text(225, 16, 'Website Users by Months (k = thousand)', { size: 13, w: 'b' });
    s += axes(40, 180, 436, 28);
    [0, 30, 60, 90].forEach((k) => (s += K.text(34, Y(k), k + 'k', { size: 11, anchor: 'end', vmid: true, cls: 't-mut' })));
    s += K.line(40, Y(37.4), 436, Y(37.4), { cls: 's-red', w: 2, dash: '6 4' });
    s += K.line(52, 38, 80, 38, { cls: 's-red', w: 2, dash: '6 4' }) + K.text(86, 38, 'Average = about 37k', { size: 12, anchor: 'start', vmid: true, w: 'b', cls: 't-red' });
    s += K.polyline(v.map((k, i) => [X(i), Y(k)]), { cls: 's-brand', w: 3 });
    v.forEach((k, i) => {
      s += K.dot(X(i), Y(k), 4);
      s += K.text(X(i), Y(k) - 8, String(k), { size: 11, w: 'b' });
      s += K.text(X(i), 198, m[i], { size: 11, cls: 't-mut' });
    });
    return K.svg(446, 212, s, { title: 'Line chart: website users per month with the average line' });
  });
})();
