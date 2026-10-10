/* XII Ch4 (Data and Analysis) diagrams */
(function () {
  const D = Diagrams;

  const sorted = (a) => a.slice().sort((x, y) => x - y);
  const quant = (arr, p) => {
    const s = sorted(arr);
    const i = p * (s.length - 1);
    const lo = Math.floor(i);
    const hi = Math.ceil(i);
    return s[lo] + (s[hi] - s[lo]) * (i - lo);
  };
  const f1 = (v) => String(Math.round(v * 100) / 100);

  function cyl(x, y, w, h, c, label) {
    const ry = 9;
    const rx = w / 2;
    const yb = y + h - ry;
    const body =
      '<path d="M' + x + ' ' + (y + ry) + ' L' + x + ' ' + yb + ' A' + rx + ' ' + ry + ' 0 0 0 ' + (x + w) + ' ' + yb +
      ' L' + (x + w) + ' ' + (y + ry) + ' A' + rx + ' ' + ry + ' 0 0 0 ' + x + ' ' + (y + ry) + ' Z" class="shape c' + c + '"/>';
    return body + K.ellipse(x + rx, y + ry, rx, ry, { c }) + K.text(x + rx, y + h / 2 + 4, label, { size: 13, w: 'b', vmid: true });
  }

  function frame(o) {
    let s = '';
    const Y = (v) => o.y + o.h - ((v - o.ymin) / (o.ymax - o.ymin)) * o.h;
    for (let v = o.ymin; v <= o.ymax + 1e-9; v += o.ystep) {
      s += K.line(o.x, Y(v), o.x + o.w, Y(v), { cls: 's-mut', dash: '3 4', w: 0.8 });
      s += K.text(o.x - 6, Y(v), String(v), { size: 11, anchor: 'end', vmid: true, cls: 't-mut' });
    }
    s += K.line(o.x, o.y, o.x, o.y + o.h);
    s += K.line(o.x, o.y + o.h, o.x + o.w, o.y + o.h);
    if (o.ylabel) s += K.text(o.x - 40, o.y + o.h / 2, o.ylabel, { rot: -90, size: 12, cls: 't-mut' });
    if (o.title) s += K.text(o.x + o.w / 2, 16, o.title, { size: 13, w: 'b' });
    return { svg: s, Y };
  }

  D.register('xii4.analysis-flow', () => {
    let s = '';
    const src = [['Files', 'CSV, Excel', 0], ['Databases', 'SQLite, MySQL', 1], ['Sensors', 'temperature', 2], ['Apps / Web', 'WhatsApp, Daraz', 4]];
    s += K.text(65, 16, 'Data sources', { size: 13, w: 'b' });
    src.forEach(([a, b, c], i) => {
      const y = 26 + i * 40;
      s += K.rect(8, y, 114, 34, { c });
      s += K.text(65, y + 14, a, { size: 13, w: 'b' });
      s += K.text(65, y + 28, b, { size: 11, cls: 't-mut' });
    });
    s += K.line(122, 43, 136, 43) + K.line(122, 83, 136, 83) + K.line(122, 123, 136, 123) + K.line(122, 163, 136, 163);
    s += K.line(136, 43, 136, 163);
    s += K.line(136, 103, 158, 103, { arrow: true });
    s += K.rect(160, 58, 120, 90, { c: 5 });
    s += K.text(220, 82, 'Python', { size: 16, w: 'b' });
    s += K.text(220, 102, 'sqlite3', { size: 12 });
    s += K.text(220, 118, 'pandas', { size: 12 });
    s += K.text(220, 134, 'matplotlib', { size: 12 });
    s += K.line(280, 103, 302, 103, { arrow: true });
    s += K.text(372, 16, 'Output', { size: 13, w: 'b' });
    [['Organise', 'tables', 1], ['Calculate', 'statistics', 3], ['Visualise', 'charts', 7]].forEach(([a, b, c], i) => {
      const y = 36 + i * 46;
      s += K.rect(304, y, 128, 38, { c });
      s += K.text(368, y + 16, a, { size: 13, w: 'b' });
      s += K.text(368, y + 31, b, { size: 11, cls: 't-mut' });
    });
    s += K.text(220, 196, 'Raw data  \u2192  useful information  \u2192  better decisions', { size: 13, cls: 't-acc', w: 'b' });
    return K.svg(440, 208, s, { title: 'Data sources flow into Python, which organises, calculates and visualises data' });
  });

  D.register('xii4.db-components', () => {
    let s = '';
    const items = [
      ['Python Application', 'Your program: sends requests,\nshows the results', 6],
      ['Driver', 'Software that lets Python talk\nto the database system', 0],
      ['Connection Object', 'Creates, manages and closes\nthe connection (conn)', 1],
      ['Cursor Object', 'Runs SQL queries and fetches\nthe results (cur)', 2],
      ['SQL Queries', 'Commands to create, insert,\nretrieve, update, delete', 4],
    ];
    const bh = 38;
    const gap = 26;
    items.forEach(([a, d, c], i) => {
      const y = 8 + i * (bh + gap);
      s += K.box(12, y, 150, bh, a, { c, size: 13, bold: true });
      s += K.text(180, y + 15, d, { size: 12, anchor: 'start', lh: 15 });
      s += K.line(87, y + bh + 1, 87, y + bh + gap - 1, { arrow: true, cls: 's-mut', w: 1.4 });
    });
    const y = 8 + 5 * (bh + gap);
    s += cyl(12, y - 2, 150, 46, 5, 'Database');
    s += K.text(180, y + 12, 'SQLite, MySQL: organised\ncollection of related data', { size: 12, anchor: 'start', lh: 15 });
    return K.svg(440, y + 52, s, { title: 'Components of a database connection: application, driver, connection, cursor, SQL queries, database' });
  });

  D.register('xii4.connect-flow', () => {
    let s = '';
    const rows = [
      ['1  Import', 'import sqlite3', 'load the SQLite library', 6],
      ['2  Connect', 'conn = sqlite3.connect("school.db")', 'open or create the file', 0],
      ['3  Cursor', 'cur = conn.cursor()', 'object that runs SQL', 1],
      ['4  Create table', 'cur.execute("CREATE TABLE ...")', 'define columns and types', 2],
      ['5  Insert', 'cur.execute("INSERT INTO ...")', 'add one record', 2],
      ['6  Commit', 'conn.commit()', 'save changes permanently', 5],
      ['7  Select', 'cur.execute("SELECT * FROM ...")', 'ask for the records', 2],
      ['8  Fetch', 'rows = cur.fetchall()', 'bring rows into Python', 4],
      ['9  Close', 'conn.close()', 'end the connection safely', 3],
    ];
    const h = 30;
    const gap = 15;
    rows.forEach(([a, code, d, c], i) => {
      const y = 6 + i * (h + gap);
      s += K.box(6, y, 112, h, a, { c, size: 13, bold: true });
      if (i < rows.length - 1) s += K.line(62, y + h + 1, 62, y + h + gap - 1, { arrow: true, cls: 's-mut', w: 1.4 });
      s += K.text(130, y + 12, code, { size: 12.5, anchor: 'start', w: 'b' });
      s += K.text(130, y + 26, d, { size: 11.5, anchor: 'start', cls: 't-mut' });
    });
    return K.svg(440, 6 + rows.length * (h + gap), s, { title: 'Nine steps of connecting Python to an SQLite database: import, connect, cursor, create, insert, commit, select, fetch, close' });
  });

  D.register('xii4.crud-table', () => {
    let s = '';
    const PH = 144;
    const panel = (x, y, title, rows, o) => {
      o = o || {};
      let p = K.rect(x, y, 212, PH, { r: 10, s: 's-mut' });
      p += K.text(x + 106, y + 17, title, { size: 12.5, w: 'b' });
      const cw = [36, 78, 58];
      const hx = x + 20;
      const all = [['id', 'name', 'marks']].concat(rows);
      all.forEach((r, i) => {
        let cx = hx;
        r.forEach((v, j) => {
          let c = 'c-none';
          if (i === 0) c = 'c-head';
          else if (o.hl && o.hl.includes(i - 1)) c = 'c' + (o.hc || 4);
          p += '<rect x="' + cx + '" y="' + (y + 28 + i * 22) + '" width="' + cw[j] + '" height="22" class="shape cell ' + c + '"/>';
          p += K.text(cx + cw[j] / 2, y + 28 + i * 22 + 11, String(v), { size: 12, vmid: true, w: i === 0 ? 'b' : '' });
          cx += cw[j];
        });
      });
      if (o.ghost) {
        p += K.rect(hx, y + 28 + 3 * 22, 172, 22, { r: 0, s: 's-red', dash: '4 3' });
        p += K.text(hx + 86, y + 28 + 3 * 22 + 11, '2   Sara   90', { size: 11.5, vmid: true, cls: 't-red' });
      }
      p += K.text(x + 106, y + PH - 8, o.note, { size: 11.5, cls: 't-mut' });
      return p;
    };
    const base = [[1, 'Ali', 85], [2, 'Sara', 90], [3, 'Ahmed', 78]];
    s += panel(4, 4, 'INSERT (3 times)', base, { hl: [0, 1, 2], hc: 5, note: '3 rows added' });
    s += panel(224, 4, 'SELECT ... WHERE marks > 80', [[1, 'Ali', 85], [2, 'Sara', 90]], { hl: [0, 1], hc: 1, note: 'only matching rows' });
    s += panel(4, 158, 'UPDATE ... WHERE id = 3', [[1, 'Ali', 85], [2, 'Sara', 90], [3, 'Ahmed', 82]], { hl: [2], hc: 4, note: 'Ahmed: 78 to 82' });
    s += panel(224, 158, 'DELETE ... WHERE id = 2', [[1, 'Ali', 85], [3, 'Ahmed', 82]], { hl: [], ghost: true, note: 'Sara removed' });
    return K.svg(440, 306, s, { title: 'Table after INSERT, SELECT, UPDATE and DELETE operations' });
  });

  D.register('xii4.df-anatomy', () => {
    let s = '';
    const rows = [['', 'Name', 'Math', 'Science'], [0, 'Ali', 85, 80], [1, 'Sara', 90, 88], [2, 'Ahmed', 78, 70], [3, 'Ayesha', 92, 95]];
    const fills = [[null, null, null, null], [6, null, 5, null], [6, null, 5, null], [6, 4, 3, 4], [6, null, 5, null]];
    for (let i = 1; i < 5; i++) fills[i][0] = 6;
    s += K.grid(100, 46, 74, 30, rows, { head: true, fills, size: 13 });
    s += K.text(280, 16, 'columns (attributes)', { size: 13, w: 'b', cls: 't-acc' });
    s += K.line(174, 36, 396, 36, { arrow: 'both', cls: 's-brand' });
    s += K.text(46, 118, 'index', { size: 13, w: 'b', cls: 't-acc' });
    s += K.text(46, 133, '(row labels)', { size: 11, cls: 't-mut' });
    s += K.line(80, 138, 98, 138, { arrow: true, cls: 's-brand' });
    s += K.rect(8, 214, 18, 14, { c: 4, r: 3 }) + K.text(32, 222, 'row = one record', { size: 12, anchor: 'start', vmid: true });
    s += K.rect(160, 214, 18, 14, { c: 5, r: 3 }) + K.text(184, 222, 'column', { size: 12, anchor: 'start', vmid: true });
    s += K.rect(262, 214, 18, 14, { c: 3, r: 3 }) + K.text(286, 222, 'one value (cell)', { size: 12, anchor: 'start', vmid: true });
    s += K.text(220, 244, 'df.shape = (4, 3)  \u2192  4 rows, 3 columns', { size: 12.5, cls: 't-mut' });
    return K.svg(440, 256, s, { title: 'Anatomy of a pandas DataFrame: index, columns, rows and cells' });
  });

  D.register('xii4.csv-to-df', () => {
    let s = '';
    s += K.text(72, 16, 'students.csv', { size: 13, w: 'b' });
    s += K.rect(4, 24, 136, 158, { c: 6, r: 8 });
    ['ID,Name,Age,Marks', '1,Ali,18,85', '2,Sara,17,90', '3,Ahmed,19,78', '4,Ayesha,19,92', '5,Usman,17,88'].forEach((l, i) => {
      s += K.text(12, 46 + i * 25, l, { size: 12.5, anchor: 'start', w: i === 0 ? 'b' : '' });
    });
    s += K.line(144, 103, 208, 103, { arrow: true, cls: 's-brand', w: 1.8 });
    s += K.text(176, 90, 'read_csv()', { size: 12, w: 'b', cls: 't-acc' });
    s += K.text(176, 124, 'df', { size: 13, w: 'b' });
    s += K.text(326, 16, 'DataFrame: df.head()', { size: 13, w: 'b' });
    const rows = [['', 'ID', 'Name', 'Age', 'Marks'], [0, 1, 'Ali', 18, 85], [1, 2, 'Sara', 17, 90], [2, 3, 'Ahmed', 19, 78], [3, 4, 'Ayesha', 19, 92], [4, 5, 'Usman', 17, 88]];
    s += K.grid(214, 24, 44.5, 26, rows, { head: true, size: 12, fills: rows.map((r, i) => (i === 0 ? [] : [6])) });
    s += K.text(220, 206, 'CSV = Comma Separated Values: one record per line', { size: 12.5, cls: 't-mut' });
    return K.svg(440, 218, s, { title: 'read_csv converts a CSV file into a DataFrame' });
  });

  D.register('xii4.missing-values', () => {
    let s = '';
    const cw = [56, 54, 86];
    const tbl = (x, y, rows, hl, hc) => {
      let p = '';
      rows.forEach((r, i) => {
        let cx = x;
        r.forEach((v, j) => {
          const head = i === 0;
          const hit = hl.some(([a, b]) => a === i && b === j);
          const c = head ? 'c-head' : hit ? 'c' + hc : 'c-none';
          p += '<rect x="' + cx + '" y="' + (y + i * 28) + '" width="' + cw[j] + '" height="28" class="shape cell ' + c + '"/>';
          p += K.text(cx + cw[j] / 2, y + i * 28 + 14, String(v), { size: 12.5, vmid: true, w: head ? 'b' : '' });
          cx += cw[j];
        });
      });
      return p;
    };
    const before = [['Name', 'Marks', 'Grade'], ['Ali', '85.0', 'A'], ['Sara', 'NaN', 'A+'], ['Ahmed', '78.0', 'NaN'], ['Ayesha', '92.0', 'A']];
    const after = [['Name', 'Marks', 'Grade'], ['Ali', '85.0', 'A'], ['Sara', '85.0', 'A+'], ['Ahmed', '78.0', 'Not Assigned'], ['Ayesha', '92.0', 'A']];
    s += K.text(100, 16, 'Before: NaN = missing', { size: 13, w: 'b', cls: 't-red' });
    s += tbl(4, 26, before, [[2, 1], [3, 2]], 3);
    s += K.text(338, 16, 'After: fillna()', { size: 13, w: 'b', cls: 't-grn' });
    s += K.line(204, 100, 234, 100, { arrow: true, cls: 's-brand', w: 1.8 });
    s += K.text(219, 88, 'fillna', { size: 11.5, w: 'b', cls: 't-acc' });
    s += tbl(240, 26, after, [[2, 1], [3, 2]], 5);
    s += K.text(220, 188, 'Marks: mean = (85 + 78 + 92) / 3 = 85.0', { size: 13, w: 'b' });
    s += K.text(220, 207, 'Grade: default text "Not Assigned"', { size: 12.5, cls: 't-mut' });
    return K.svg(440, 218, s, { title: 'Missing values NaN replaced using fillna: Marks with the mean, Grade with Not Assigned' });
  });

  D.register('xii4.organise-ways', () => {
    let s = '';
    const titles = ['Tabular', 'Frequency table', 'Graphical'];
    const subs = ['rows and columns', 'counts per range', 'bars, lines, dots'];
    titles.forEach((t, i) => {
      const x = 6 + i * 146;
      s += K.rect(x, 4, 136, 168, { r: 10, s: 's-mut' });
      s += K.text(x + 68, 22, t, { size: 13, w: 'b' });
      s += K.text(x + 68, 162, subs[i], { size: 11.5, cls: 't-mut' });
    });
    s += K.grid(12, 34, 41, 22, [['Name', 'Eng', 'Math'], ['Ali', 78, 82], ['Sara', 88, 76], ['Bilal', 70, 60]], { head: true, size: 11.5 });
    s += K.grid(158, 34, 60, 22, [['Marks', 'f'], ['0-49', 3], ['50-59', 5], ['60-69', 7], ['70-79', 9]], { head: true, size: 11.5 });
    const hs = [3, 5, 7, 9, 4, 2];
    const bx = 312;
    s += K.line(bx, 134, bx + 114, 134);
    hs.forEach((h, i) => {
      s += K.rect(bx + 4 + i * 17, 134 - h * 8, 15, h * 8, { c: i % 2 ? 1 : 0, r: 1 });
    });
    return K.svg(440, 178, s, { title: 'Three ways to organise data: table, frequency distribution table and graph' });
  });

  function lineChart(vals, labels, o) {
    const f = frame({ x: 56, y: 32, w: 364, h: 150, ymin: o.ymin, ymax: o.ymax, ystep: o.ystep, ylabel: o.ylabel, title: o.title });
    let s = f.svg;
    const n = vals.length;
    const X = (i) => 56 + ((i + 0.5) * 364) / n;
    s += K.polyline(vals.map((v, i) => [X(i), f.Y(v)]), { s: 's-brand', w: 2.6 });
    vals.forEach((v, i) => {
      s += K.circle(X(i), f.Y(v), 4.5, { c: 1 });
      s += K.text(X(i), f.Y(v) - 10, String(v), { size: 11 });
      s += K.text(X(i), 198, labels[i], { size: 11.5, cls: 't-mut' });
    });
    s += K.text(56 + 182, 220, o.xlabel, { size: 12, cls: 't-mut' });
    return K.svg(440, 230, s, { title: o.title });
  }

  D.register('xii4.line-chart', () =>
    lineChart([65, 70, 75, 80], ['2021', '2022', '2023', '2024'], { ymin: 60, ymax: 85, ystep: 5, ylabel: 'Percentage Marks', xlabel: 'Year', title: 'Students Performance Over Years' })
  );
  D.register('xii4.line-temps', () =>
    lineChart([12, 15, 22, 25, 30, 35, 38, 37, 33, 28, 23, 18], ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'], { ymin: 0, ymax: 40, ystep: 10, ylabel: 'Temperature (\u00b0C)', xlabel: 'Months', title: 'Average Monthly Temperature' })
  );

  D.register('xii4.bar-chart', () => {
    const names = ['Arabic', 'English', 'Math', 'Science', 'Social\nScience'];
    const vals = [45, 57, 80, 65, 50];
    const f = frame({ x: 56, y: 32, w: 364, h: 150, ymin: 0, ymax: 100, ystep: 20, ylabel: 'Marks', title: 'Marks vs Students' });
    let s = f.svg;
    const slot = 364 / names.length;
    vals.forEach((v, i) => {
      const x = 56 + i * slot + slot * 0.15;
      s += K.rect(x, f.Y(v), slot * 0.7, f.Y(0) - f.Y(v), { c: 1, r: 2 });
      s += K.text(x + slot * 0.35, f.Y(v) - 6, String(v), { size: 12, w: 'b' });
      s += K.text(x + slot * 0.35, 198, names[i], { size: 11.5, cls: 't-mut', lh: 13 });
    });
    s += K.text(56 + 182, 226, 'Students (subjects)', { size: 12, cls: 't-mut' });
    return K.svg(440, 236, s, { title: 'Bar chart of marks in five subjects' });
  });

  D.register('xii4.pie', () => {
    const names = ['Math', 'Physics', 'Computer\nScience', 'Biology', 'Chemistry'];
    const vals = [25, 15, 30, 10, 20];
    const tot = vals.reduce((a, b) => a + b, 0);
    const cx = 220;
    const cy = 126;
    const r = 80;
    let a0 = 90;
    let s = K.text(220, 16, 'Students choosing different subjects', { size: 13, w: 'b' });
    vals.forEach((v, i) => {
      const a1 = a0 + (v / tot) * 360;
      const p = (a) => [cx + r * Math.cos((a * Math.PI) / 180), cy - r * Math.sin((a * Math.PI) / 180)];
      const [x0, y0] = p(a0);
      const [x1, y1] = p(a1);
      const large = a1 - a0 > 180 ? 1 : 0;
      s += '<path d="M' + cx + ' ' + cy + ' L' + x0.toFixed(2) + ' ' + y0.toFixed(2) + ' A' + r + ' ' + r + ' 0 ' + large + ' 0 ' + x1.toFixed(2) + ' ' + y1.toFixed(2) + ' Z" class="shape c' + i + '"/>';
      const am = ((a0 + a1) / 2) * (Math.PI / 180);
      const lx = cx + (r + 12) * Math.cos(am);
      const ly = cy - (r + 12) * Math.sin(am);
      const c = Math.cos(am);
      const anchor = c > 0.15 ? 'start' : c < -0.15 ? 'end' : 'middle';
      const nm = names[i] + (names[i].includes('\n') ? ' ' : '\n') + v + '%';
      const lines = nm.split('\n');
      s += K.text(lx, ly + (Math.sin(am) > 0.8 ? -14 : -2), lines.join('\n'), { size: 12, anchor, lh: 13, vmid: true });
      a0 = a1;
    });
    return K.svg(440, 238, s, { title: 'Pie chart: Math 25%, Physics 15%, Computer Science 30%, Biology 10%, Chemistry 20%' });
  });

  D.register('xii4.histogram', () => {
    const scores = [45, 50, 55, 60, 62, 65, 68, 70, 72, 75, 78, 80, 82, 85, 88, 90, 92, 95, 98, 100];
    const bins = [40, 50, 60, 70, 80, 90, 100];
    const counts = bins.slice(1).map((hi, i) => scores.filter((v) => v >= bins[i] && (i === bins.length - 2 ? v <= hi : v < hi)).length);
    const f = frame({ x: 56, y: 32, w: 364, h: 150, ymin: 0, ymax: 6, ystep: 1, ylabel: 'Number of Students', title: 'Distribution of Student Scores' });
    let s = f.svg;
    const X = (v) => 56 + ((v - 40) / 60) * 364;
    counts.forEach((c, i) => {
      s += K.rect(X(bins[i]), f.Y(c), X(bins[i + 1]) - X(bins[i]), f.Y(0) - f.Y(c), { c: 1, r: 0 });
      s += K.text((X(bins[i]) + X(bins[i + 1])) / 2, f.Y(c) - 6, String(c), { size: 12, w: 'b' });
    });
    bins.forEach((b) => (s += K.text(X(b), 198, String(b), { size: 11.5, cls: 't-mut' })));
    s += K.text(56 + 182, 220, 'Score Range (bins)', { size: 12, cls: 't-mut' });
    return K.svg(440, 230, s, { title: 'Histogram of twenty student scores in six bins' });
  });

  D.register('xii4.scatter', () => {
    const xs = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10];
    const ys = [2, 4, 5, 4, 7, 8, 9, 12, 11, 15];
    const n = xs.length;
    const mx = xs.reduce((a, b) => a + b, 0) / n;
    const my = ys.reduce((a, b) => a + b, 0) / n;
    const m = xs.reduce((a, x, i) => a + (x - mx) * (ys[i] - my), 0) / xs.reduce((a, x) => a + (x - mx) * (x - mx), 0);
    const c = my - m * mx;
    const f = frame({ x: 56, y: 32, w: 364, h: 150, ymin: 0, ymax: 16, ystep: 4, ylabel: 'Y-axis Values', title: 'Example Scatter Plot' });
    let s = f.svg;
    const X = (v) => 56 + (v / 11) * 364;
    s += K.line(X(0.6), f.Y(m * 0.6 + c), X(10.4), f.Y(m * 10.4 + c), { s: 's-red', dash: '6 4', w: 2 });
    xs.forEach((x, i) => {
      s += K.circle(X(x), f.Y(ys[i]), 5, { c: 1 });
      s += K.text(X(x), 198, String(x), { size: 11.5, cls: 't-mut' });
    });
    s += K.text(56 + 182, 220, 'X-axis Values', { size: 12, cls: 't-mut' });
    s += K.text(70, 49, 'dashed line = trend line', { size: 12, anchor: 'start', cls: 't-red', w: 'b' });
    s += K.text(70, 63, 'higher x \u2192 higher y', { size: 12, anchor: 'start', cls: 't-mut' });
    return K.svg(440, 230, s, { title: 'Scatter plot of ten points with a rising trend line' });
  });

  D.register('xii4.boxplot', (args) => {
    const data = (args && args.data) || [20, 35, 40, 45, 50, 56, 62, 68, 110];
    const s0 = sorted(data);
    const q1 = quant(data, 0.25);
    const med = quant(data, 0.5);
    const q3 = quant(data, 0.75);
    const iqr = q3 - q1;
    const lf = q1 - 1.5 * iqr;
    const uf = q3 + 1.5 * iqr;
    const inside = s0.filter((v) => v >= lf && v <= uf);
    const lo = inside[0];
    const hi = inside[inside.length - 1];
    const out = s0.filter((v) => v < lf || v > uf);
    const vmax = 120;
    const X = (v) => 25 + v * 3.3;
    let s = K.text(220, 14, 'Screen time (minutes) of 9 classmates', { size: 13, w: 'b' });
    const by = 94;
    const bh = 36;
    const ay = 208;
    s += K.line(X(0), ay, X(vmax), ay);
    for (let v = 0; v <= vmax; v += 20) {
      s += K.line(X(v), ay, X(v), ay + 5);
      s += K.text(X(v), ay + 19, String(v), { size: 11, cls: 't-mut' });
    }
    s += K.text(X(vmax) - 4, ay + 34, 'minutes', { size: 11, anchor: 'end', cls: 't-mut' });
    s += K.line(X(lo), by + bh / 2, X(q1), by + bh / 2, { w: 2 }) + K.line(X(lo), by + 8, X(lo), by + bh - 8, { w: 2 });
    s += K.line(X(q3), by + bh / 2, X(hi), by + bh / 2, { w: 2 }) + K.line(X(hi), by + 8, X(hi), by + bh - 8, { w: 2 });
    s += K.rect(X(q1), by, X(q3) - X(q1), bh, { c: 1, r: 2 });
    s += K.line(X(med), by, X(med), by + bh, { s: 's-red', w: 3 });
    out.forEach((v) => (s += K.circle(X(v), by + bh / 2, 5, { c: 3 })));
    s += K.line(X(uf), by - 20, X(uf), by + bh + 14, { dash: '4 4', cls: 's-mut', w: 1.2 });
    const above = (x, a, b) => {
      let r = K.text(x, 36, a + '\n' + b, { size: 12, w: 'b', lh: 14 });
      r += K.line(x, 56, x, by - 2, { dash: '2 3', cls: 's-mut', w: 1 });
      return r;
    };
    s += above(X(lo), 'min', f1(lo));
    s += above(X(med), 'median', f1(med));
    s += above(X(hi), 'max', f1(hi));
    out.forEach((v) => (s += above(X(v), 'outlier', f1(v))));
    const below = (x, a, b) => {
      let r = K.text(x, by + bh + 20, a + '\n' + b, { size: 12, w: 'b', lh: 14 });
      r += K.line(x, by + bh + 2, x, by + bh + 8, { dash: '2 3', cls: 's-mut', w: 1 });
      return r;
    };
    s += below(X(q1), 'Q1', f1(q1));
    s += below(X(q3), 'Q3', f1(q3));
    s += K.text(X(uf), by + bh + 20, 'upper fence\n' + f1(uf), { size: 11, lh: 13, cls: 't-mut' });
    s += K.line(X(q1), 178, X(q3), 178, { arrow: 'both', cls: 's-brand', w: 1.4 });
    s += K.text((X(q1) + X(q3)) / 2, 196, 'IQR = ' + f1(q3) + ' \u2212 ' + f1(q1) + ' = ' + f1(iqr), { size: 12, w: 'b', cls: 't-acc' });
    return K.svg(440, 246, s, { title: 'Labelled boxplot with minimum, Q1, median, Q3, maximum and one outlier' });
  });

  D.register('xii4.boxplot-compare', () => {
    const sets = [
      ['Rainfall (mm)', [120, 135, 150, 160, 175, 180, 190, 200, 210, 220], 0],
      ['Crop Yield Index', [100, 115, 130, 140, 150, 160, 170, 185, 200, 215], 5],
    ];
    const f = frame({ x: 56, y: 30, w: 250, h: 160, ymin: 80, ymax: 240, ystep: 40, ylabel: 'Observed Values' });
    let s = f.svg;
    s += K.text(181, 14, 'Box Plot: rainfall and crop yield', { size: 13, w: 'b' });
    sets.forEach(([name, d, c], i) => {
      const cx = 56 + (i + 0.5) * 125;
      const q1 = quant(d, 0.25);
      const q2 = quant(d, 0.5);
      const q3 = quant(d, 0.75);
      const mn = Math.min(...d);
      const mx = Math.max(...d);
      s += K.line(cx, f.Y(mn), cx, f.Y(q1)) + K.line(cx, f.Y(q3), cx, f.Y(mx));
      s += K.line(cx - 14, f.Y(mn), cx + 14, f.Y(mn)) + K.line(cx - 14, f.Y(mx), cx + 14, f.Y(mx));
      s += K.rect(cx - 32, f.Y(q3), 64, f.Y(q1) - f.Y(q3), { c, r: 2 });
      s += K.line(cx - 32, f.Y(q2), cx + 32, f.Y(q2), { s: 's-red', w: 3 });
      s += K.text(cx, 208, name.replace(' (', '\n('), { size: 11.5, cls: 't-mut', lh: 13 });
      if (i === 1) {
        [['max', mx], ['Q3', q3], ['median', q2], ['Q1', q1], ['min', mn]].forEach(([l, v]) => {
          s += K.line(cx + 34, f.Y(v), 318, f.Y(v), { cls: 's-mut', dash: '2 3', w: 1 });
          s += K.text(322, f.Y(v), l + ' = ' + f1(v), { size: 12, anchor: 'start', vmid: true, w: l === 'median' ? 'b' : '' });
        });
      }
    });
    return K.svg(440, 236, s, { title: 'Two boxplots comparing rainfall and crop yield distributions' });
  });

  function balance(vals, o) {
    const sv = sorted(vals);
    const n = vals.length;
    const mean = vals.reduce((a, b) => a + b, 0) / n;
    const med = quant(vals, 0.5);
    const X = (v) => 24 + (v / o.max) * 392;
    const stacks = [];
    const place = sv.map((v) => {
      const last = stacks[stacks.length - 1];
      if (last && Math.abs(X(v) - X(last.v)) < 22) {
        last.n += 1;
        return { v, k: last.n - 1 };
      }
      stacks.push({ v, n: 1 });
      return { v, k: 0 };
    });
    const maxk = Math.max(...place.map((p) => p.k)) + 1;
    const beam = 66 + maxk * 20;
    let s = '';
    s += K.line(X(0), beam, X(o.max), beam, { w: 4 });
    for (let v = 0; v <= o.max; v += o.step) {
      s += K.line(X(v), beam + 4, X(v), beam + 9, { w: 1.2 });
      s += K.text(X(v), beam + 22, String(v), { size: 11, cls: 't-mut' });
    }
    place.forEach(({ v, k }) => {
      const label = String(v);
      const w = Math.max(20, label.length * 8 + 6);
      s += K.rect(X(v) - w / 2, beam - 3 - 18 - k * 20, w, 18, { c: 1, r: 3 });
      s += K.text(X(v), beam - 3 - 9 - k * 20, label, { size: 11, w: 'b', vmid: true });
    });
    const mx = X(mean);
    s += K.poly([[mx, beam + 2], [mx - 11, beam + 32], [mx + 11, beam + 32]], { c: 5 });
    s += K.text(mx, beam + 50, 'mean = ' + f1(mean) + ' (balance point)', { size: 12.5, w: 'b', cls: 't-grn', anchor: mx > 300 ? 'end' : 'start' });
    const medX = X(med);
    const topK = place.filter((p) => Math.abs(X(p.v) - medX) < 12).reduce((a, p) => Math.max(a, p.k), 0);
    const top = beam - 3 - 18 - topK * 20 - 4;
    s += K.line(medX, top - 24, medX, top, { arrow: true, cls: 's-red', w: 2 });
    s += K.text(medX, top - 30, 'median = ' + f1(med), { size: 12.5, w: 'b', cls: 't-red', anchor: medX > 300 ? 'end' : 'middle' });
    return K.svg(440, beam + 62, s, { title: o.title });
  }

  D.register('xii4.mean-balance', () => balance([35, 10, 15, 70, 95], { max: 100, step: 10, title: 'Marks 10, 15, 35, 70, 95 on a beam: the mean 45 is the balance point, median is 35' }));
  D.register('xii4.balance-salary', () => balance([25, 30, 32, 35, 400], { max: 420, step: 60, title: 'Salaries in thousands: one huge salary pulls the mean far above the median' }));

  D.register('xii4.mode-dots', () => {
    const vals = [20, 25, 20, 30, 20, 25, 20];
    const X = (v) => 40 + ((v - 15) / 20) * 360;
    const axisY = 158;
    let s = K.text(220, 14, 'Water bottles sold each day', { size: 13, w: 'b' });
    s += K.line(X(15), axisY, X(35), axisY);
    for (let v = 15; v <= 35; v += 5) {
      s += K.line(X(v), axisY, X(v), axisY + 5);
      s += K.text(X(v), axisY + 20, String(v), { size: 12, cls: 't-mut' });
    }
    const cnt = {};
    vals.forEach((v) => {
      cnt[v] = (cnt[v] || 0) + 1;
      s += K.circle(X(v), axisY - 12 - (cnt[v] - 1) * 22, 9, { c: v === 20 ? 3 : 1 });
    });
    s += K.text(X(20), 46, 'mode = 20', { size: 13, w: 'b', cls: 't-red' });
    s += K.text(X(20), 61, 'appears 4 times', { size: 12, cls: 't-mut' });
    s += K.text(X(25), 108, '2 times', { size: 11.5, cls: 't-mut' });
    s += K.text(X(30), 130, '1 time', { size: 11.5, cls: 't-mut' });
    return K.svg(440, 184, s, { title: 'Dot plot of daily bottle sales: the value 20 appears most often, so mode is 20' });
  });

  D.register('xii4.range', () => {
    const vals = [120, 150, 180];
    const Y = (v) => 176 - v * 0.72;
    let s = K.text(190, 16, 'Notebooks sold in three days', { size: 13, w: 'b' });
    s += K.line(20, 176, 330, 176);
    vals.forEach((v, i) => {
      const x = 40 + i * 96;
      s += K.rect(x, Y(v), 70, 176 - Y(v), { c: [5, 1, 3][i], r: 3 });
      s += K.text(x + 35, 160, String(v), { size: 14, w: 'b' });
      s += K.text(x + 35, 194, 'Day ' + (i + 1), { size: 12, cls: 't-mut' });
    });
    s += K.line(40, Y(180), 346, Y(180), { cls: 's-red', dash: '4 4', w: 1.4 });
    s += K.line(40, Y(120), 346, Y(120), { cls: 's-grn', dash: '4 4', w: 1.4 });
    s += K.line(340, Y(120) - 1, 340, Y(180) + 1, { arrow: 'both', cls: 's-brand', w: 1.6 });
    s += K.text(352, Y(150) - 14, 'Range', { size: 13, w: 'b', anchor: 'start', cls: 't-acc' });
    s += K.text(352, Y(150) + 2, '180 \u2212 120', { size: 12.5, anchor: 'start' });
    s += K.text(352, Y(150) + 18, '= 60', { size: 13, w: 'b', anchor: 'start' });
    s += K.text(44, Y(180) - 5, 'highest = 180', { size: 11.5, anchor: 'start', cls: 't-red' });
    s += K.text(44, Y(120) - 5, 'lowest = 120', { size: 11.5, anchor: 'start', cls: 't-grn' });
    return K.svg(440, 206, s, { title: 'Range of 120, 150 and 180 notebooks is 60' });
  });

  D.register('xii4.deviation', () => {
    const vals = [50, 80, 100, 130, 140];
    const mean = 100;
    const X = (v) => 70 + ((v - 30) / 120) * 340;
    let s = K.text(240, 14, 'Deviation = value \u2212 mean  (mean = 100)', { size: 13, w: 'b' });
    const axisY = 188;
    s += K.line(X(30), axisY, X(150), axisY);
    vals.forEach((v) => {
      s += K.line(X(v), axisY, X(v), axisY + 5);
      s += K.text(X(v), axisY + 19, String(v), { size: 11.5, cls: 't-mut' });
    });
    s += K.line(X(mean), 30, X(mean), axisY, { cls: 's-brand', dash: '5 4', w: 1.6 });
    vals.forEach((v, i) => {
      const y = 46 + i * 28;
      const d = v - mean;
      s += K.text(8, y, 'Day ' + (i + 1), { size: 12, anchor: 'start', vmid: true, cls: 't-mut' });
      if (d !== 0) s += K.line(X(mean), y, X(v) - Math.sign(d) * 6, y, { arrow: true, cls: d < 0 ? 's-red' : 's-grn', w: 1.4 });
      s += K.circle(X(v), y, 5, { c: d < 0 ? 3 : d > 0 ? 5 : 1 });
      const lab = d === 0 ? '0' : (d > 0 ? '+' : '\u2212') + Math.abs(d);
      s += K.text(X(v) + (d < 0 ? -10 : 10), y, lab, { size: 12.5, w: 'b', anchor: d < 0 ? 'end' : 'start', vmid: true, cls: d < 0 ? 't-red' : d > 0 ? 't-grn' : '' });
    });
    return K.svg(440, 214, s, { title: 'Deviation of each value from the mean 100 shown as arrows' });
  });

  D.register('xii4.spread-compare', () => {
    const X = (v) => 40 + ((v - 40) / 110) * 380;
    const sets = [
      ['Low spread: SD \u2248 1.41', [100, 102, 101, 99, 98], 1.4142, 64],
      ['High spread: SD \u2248 32.86', [50, 80, 100, 130, 140], 32.8634, 140],
    ];
    let s = '';
    sets.forEach(([t, d, sd, cy], i) => {
      s += K.text(10, cy - 40, t, { size: 13, w: 'b', anchor: 'start' });
      s += K.rect(X(100 - sd), cy - 17, X(100 + sd) - X(100 - sd), 34, { c: 0, r: 4 });
      d.forEach((v, k) => (s += K.circle(X(v), cy + (i ? 0 : [-9, 0, 9, -5, 5][k]), i ? 5 : 4, { c: i ? 3 : 5 })));
    });
    const ay = 188;
    s += K.line(X(40), ay, X(150), ay);
    [40, 60, 80, 100, 120, 140].forEach((v) => {
      s += K.line(X(v), ay, X(v), ay + 5);
      s += K.text(X(v), ay + 19, String(v), { size: 11.5, cls: 't-mut' });
    });
    s += K.line(X(100), 44, X(100), ay, { cls: 's-brand', dash: '5 4', w: 1.6 });
    s += K.text(X(100) + 5, 32, 'mean = 100', { size: 12, anchor: 'start', cls: 't-acc', w: 'b' });
    s += K.text(220, 226, 'shaded band = mean \u00b1 1 SD', { size: 12, cls: 't-mut' });
    return K.svg(440, 236, s, { title: 'Two sets with the same mean 100: one tightly packed, one widely spread' });
  });

  D.register('xii4.quartiles', () => {
    const d = [20, 35, 40, 45, 50, 56, 62, 68, 110];
    const w = 40;
    const st = 44;
    const x0 = 22;
    const by = 82;
    let s = '';
    d.forEach((v, i) => {
      s += K.box(x0 + i * st, by, w, 34, String(v), { c: i === 4 ? 4 : i < 4 ? 1 : 0, size: 13, bold: [2, 4, 6].includes(i) });
    });
    const cx = (i) => x0 + i * st + w / 2;
    s += K.polyline([[cx(0) - 18, 72], [cx(0) - 18, 66], [cx(4), 66], [cx(4), 72]], { s: 's-brand' });
    s += K.text(cx(2), 58, 'lower half (5 values)', { size: 12, cls: 't-acc', w: 'b' });
    s += K.polyline([[cx(4), 46], [cx(4), 40], [cx(8) + 18, 40], [cx(8) + 18, 46]], { s: 's-grn' });
    s += K.text(cx(6), 28, 'upper half (5 values)', { size: 12, cls: 't-grn', w: 'b' });
    [[2, 'Q1', '40', 's-brand'], [4, 'Q2 (median)', '50', 's-red'], [6, 'Q3', '62', 's-grn']].forEach(([i, a, b]) => {
      s += K.poly([[cx(i), 120], [cx(i) - 6, 130], [cx(i) + 6, 130]], { c: i === 4 ? 4 : 5 });
      s += K.text(cx(i), 146, a, { size: 12.5, w: 'b' });
      s += K.text(cx(i), 161, '= ' + b, { size: 12.5 });
    });
    s += K.text(220, 190, 'Sorted data, n = 9: the median 50 is shared by both halves', { size: 12, cls: 't-mut' });
    s += K.text(220, 208, 'Q1 = median of lower half   Q3 = median of upper half', { size: 12, cls: 't-mut' });
    return K.svg(440, 218, s, { title: 'Nine sorted values split into halves: Q1 is 40, median is 50, Q3 is 62' });
  });
})();
