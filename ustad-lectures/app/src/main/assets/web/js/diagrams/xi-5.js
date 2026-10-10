/* XI Ch5 (Applications and Impacts of Computing) diagrams */
(function () {
  const D = Diagrams;
  const T = (x, y, s, o) => K.text(x, y, s, o);

  const cloud = (x, y, sc, c) =>
    K.g(K.path('M0 30 A12 12 0 0 1 4 8 A16 16 0 0 1 34 4 A14 14 0 0 1 56 14 A12 12 0 0 1 54 30 Z', { c: c == null ? 1 : c }), {
      t: 'translate(' + x + ',' + y + ') scale(' + sc + ')',
    });

  const tick = (x, y) => K.polyline([[x + 4, y + 11], [x + 9, y + 17], [x + 19, y + 5]], { s: 's-grn', w: 3 });

  const card = (x, y, w, h, icon, title, sub, c) =>
    K.rect(x, y, w, h, { c: c == null ? 6 : c }) +
    icon +
    T(x + w / 2, y + h - 30, title, { size: 14, w: 'b' }) +
    T(x + w / 2, y + h - 12, sub, { size: 12, cls: 't-mut' });

  const wifi = (cx0, cy0) => {
    let s = '';
    [6, 12, 18].forEach((r) => {
      const dx = r * Math.SQRT1_2;
      s += K.path('M' + (cx0 + dx) + ' ' + (cy0 - dx) + ' A' + r + ' ' + r + ' 0 0 1 ' + (cx0 + dx) + ' ' + (cy0 + dx), { s: 's-acc', w: 2 });
    });
    return s + K.dot(cx0, cy0, 3);
  };

  /* ---------- Lecture 1 ---------- */
  D.register('xi5.smart-loop', () => {
    let s = '';
    s += T(220, 20, 'Smart home: the room is hot', { size: 14, w: 'b' });
    const names = ['Temperature\nsensor', 'Data\nAnalytics', 'AI\n(the brain)', 'Fan / AC\n(actuator)'];
    const roles = ['IoT collects\nthe data', 'studies the\ndata', 'decides what\nto do', 'does the\naction'];
    const vals = ['34 °C', 'Room is HOT', 'Turn ON fan', 'Fan is ON'];
    const cols = [0, 1, 2, 5];
    for (let i = 0; i < 4; i++) {
      const x = 8 + i * 108;
      s += K.box(x, 40, 92, 60, names[i], { c: cols[i], size: 13, bold: true });
      s += T(x + 46, 122, roles[i], { size: 12, cls: 't-mut' });
      s += K.box(x, 160, 92, 30, vals[i], { s: 's-brand', size: 12 });
      if (i < 3) s += K.line(x + 94, 70, x + 106, 70, { arrow: true, s: 's-acc', w: 2 });
    }
    s += T(220, 224, 'AI acts like the "brain" of a smart system', { size: 13, cls: 't-acc' });
    return K.svg(440, 240, s, { title: 'IoT sensor collects, Data Analytics studies, AI decides, actuator acts' });
  });

  D.register('xi5.ai-examples', () => {
    let s = '';
    const w = 140;
    const xs = [0, 150, 300];
    // Face unlock
    let cx = xs[0] + w / 2;
    let ic = K.circle(cx, 52, 17, { c: 4 }) + K.dot(cx - 6, 49, 2.5) + K.dot(cx + 6, 49, 2.5) + K.path('M' + (cx - 6) + ' 59 Q' + cx + ' 65 ' + (cx + 6) + ' 59', { s: 's-acc', w: 2 });
    [[-30, -30, 1, 1], [30, -30, -1, 1], [-30, 30, 1, -1], [30, 30, -1, -1]].forEach(([dx, dy, sx, sy]) => {
      ic += K.polyline([[cx + dx + sx * 10, 52 + dy], [cx + dx, 52 + dy], [cx + dx, 52 + dy + sy * 10]], { s: 's-brand', w: 3 });
    });
    s += card(xs[0], 6, w, 160, ic, 'Face unlock', 'phone knows you', 0);
    // Video suggestions
    cx = xs[1] + w / 2;
    ic = K.rect(cx - 30, 32, 60, 40, { c: 3, r: 8 }) + K.poly([[cx - 8, 41], [cx - 8, 63], [cx + 12, 52]], { c: 6 });
    ic += K.rect(cx - 30, 76, 60, 6, { c: 6, r: 3 }) + K.rect(cx - 30, 76, 24, 6, { c: 3, r: 3 });
    s += card(xs[1], 6, w, 160, ic, 'YouTube', 'suggests videos', 1);
    // Chatbot
    cx = xs[2] + w / 2;
    ic = K.rect(cx - 34, 30, 44, 26, { c: 2, r: 8 }) + K.rect(cx - 10, 52, 44, 26, { c: 0, r: 8 });
    ic += K.dot(cx - 24, 43, 2.5) + K.dot(cx - 14, 43, 2.5) + K.dot(cx - 4, 43, 2.5);
    ic += K.line(cx, 65, cx + 22, 65, { s: 's-mut', w: 2 }) + K.line(cx, 71, cx + 14, 71, { s: 's-mut', w: 2 });
    s += card(xs[2], 6, w, 160, ic, 'Chatbot', 'answers questions', 2);
    s += T(220, 190, 'Each one learns from data to decide', { size: 13, cls: 't-acc' });
    return K.svg(440, 200, s, { title: 'Three AI examples: face unlock, video suggestions and chatbot' });
  });

  /* ---------- Lecture 2 ---------- */
  D.register('xi5.watch-phone', () => {
    let s = '';
    // watch
    s += K.rect(52, 26, 36, 22, { c: 6, r: 4 }) + K.rect(52, 122, 36, 22, { c: 6, r: 4 });
    s += K.rect(40, 48, 60, 74, { c: 0, r: 12 });
    s += T(70, 78, '72', { size: 18, w: 'b' }) + T(70, 96, 'bpm', { size: 11, cls: 't-mut' });
    s += T(70, 168, 'Smartwatch', { size: 13, w: 'b' }) + T(70, 184, 'collects data', { size: 12, cls: 't-mut' });
    // link
    s += K.line(110, 85, 270, 85, { arrow: true, s: 's-brand', w: 2 });
    s += T(190, 70, 'Bluetooth', { size: 13, w: 'b', cls: 't-acc' });
    s += T(190, 106, 'steps, heart rate, sleep', { size: 12, cls: 't-mut' });
    // phone
    s += K.rect(282, 22, 90, 128, { c: 1, r: 14 });
    s += K.rect(290, 36, 74, 96, { r: 6 });
    s += T(327, 56, 'Steps 6420', { size: 12 }) + T(327, 78, 'Heart 72', { size: 12 }) + T(327, 100, 'Sleep 7 h', { size: 12 });
    s += K.dot(327, 142, 3);
    s += T(327, 168, 'Mobile phone', { size: 13, w: 'b' }) + T(327, 184, 'shows the user', { size: 12, cls: 't-mut' });
    return K.svg(420, 196, s, { title: 'Smartwatch sends steps, heart rate and sleep data to a phone over Bluetooth' });
  });

  D.register('xi5.iot-architecture', (args) => {
    const home = args && args.example === 'home';
    const rows = home
      ? [
          ['Sensors', 'collect data', 'Temperature sensor', 'reads room temperature'],
          ['Connectivity', 'network / gateway', 'Wi-Fi router', 'carries the reading'],
          ['Cloud', 'stores data', 'Cloud server', 'keeps the readings'],
          ['Data Processing', 'analytics', 'Room is hot?', 'yes, 34 °C is too hot'],
          ['UI + Actuator', 'app and action', 'Phone app + Fan', 'user sees; fan turns ON'],
        ]
      : [
          ['Sensors', 'collect data', 'Soil moisture + weather', 'field is dry, no rain'],
          ['Connectivity', 'network / gateway', 'LoRaWAN / 4G', 'sends readings out'],
          ['Cloud', 'stores data', 'Cloud server', 'keeps field history'],
          ['Data Processing', 'analytics', 'Crop needs water?', 'yes, soil is too dry'],
          ['UI + Actuator', 'app and action', 'Farmer app + Valve', 'farmer sees; pump ON'],
        ];
    let s = '';
    s += T(100, 16, 'IoT component', { size: 13, w: 'b', cls: 't-acc' });
    s += T(342, 16, home ? 'Example: smart home' : 'Example: smart farming', { size: 13, w: 'b', cls: 't-acc' });
    const cs = [0, 1, 2, 3, 5];
    rows.forEach((r, i) => {
      const y = 30 + i * 64;
      s += K.rect(8, y, 184, 48, { c: cs[i] });
      s += T(100, y + 20, r[0], { size: 14, w: 'b' }) + T(100, y + 38, r[1], { size: 12, cls: 't-mut' });
      s += K.rect(248, y, 184, 48, { s: 's-brand' });
      s += T(340, y + 20, r[2], { size: 13, w: 'b' }) + T(340, y + 38, r[3], { size: 12, cls: 't-mut' });
      s += T(220, y + 29, 'e.g.', { size: 12, cls: 't-mut' });
      if (i < 4) {
        s += K.line(100, y + 49, 100, y + 63, { arrow: true, s: 's-acc', w: 2 });
        s += K.line(340, y + 49, 340, y + 63, { arrow: true, s: 's-acc', w: 2 });
      }
    });
    return K.svg(440, 350, s, { title: 'IoT architecture from sensors to connectivity, cloud, data processing and user interface or actuator' });
  });

  D.register('xi5.sensor-actuator', () => {
    let s = '';
    const L = ['Temperature', 'Motion', 'Fingerprint', 'Camera', 'Smoke', 'Soil moisture'];
    const R = ['Motor', 'Electric switch', 'Door opener', 'Water valve', 'Fan controller', 'Alarm system'];
    s += K.rect(6, 6, 200, 36, { c: 0 }) + T(106, 24, 'Sensors', { size: 15, w: 'b', vmid: true });
    s += K.rect(234, 6, 200, 36, { c: 5 }) + T(334, 24, 'Actuators', { size: 15, w: 'b', vmid: true });
    s += T(106, 60, 'detect the physical world', { size: 12, cls: 't-mut' });
    s += T(334, 60, 'perform physical actions', { size: 12, cls: 't-mut' });
    L.forEach((v, i) => {
      s += K.box(16, 72 + i * 36, 180, 28, v, { s: 's-acc', size: 13 });
      s += K.box(244, 72 + i * 36, 180, 28, R[i], { s: 's-grn', size: 13 });
    });
    s += K.line(206, 150, 232, 150, { arrow: true, s: 's-brand', w: 2 });
    s += T(220, 140, 'signal', { size: 11, cls: 't-mut' });
    s += T(106, 296, 'INPUT', { size: 13, w: 'b', cls: 't-acc' });
    s += T(334, 296, 'OUTPUT', { size: 13, w: 'b', cls: 't-grn' });
    return K.svg(440, 306, s, { title: 'Sensors are inputs that detect; actuators are outputs that act' });
  });

  D.register('xi5.auto-door', () => {
    let s = '';
    s += T(220, 18, 'Automatic door system', { size: 14, w: 'b' });
    const b = [
      ['Motion\nsensor', 0, 'detects a person'],
      ['Control\nunit', 2, 'processes the signal'],
      ['Motor\n(actuator)', 5, 'opens the door'],
    ];
    b.forEach((v, i) => {
      const x = 20 + i * 165;
      s += K.circle(x + 45, 44, 11, { c: 6 }) + T(x + 45, 45, String(i + 1), { size: 12, w: 'b', vmid: true });
      s += K.box(x, 62, 90, 56, v[0], { c: v[1], size: 13, bold: true });
      s += T(x + 45, 140, v[2], { size: 12, cls: 't-mut' });
      if (i < 2) {
        s += K.line(x + 94, 90, x + 161, 90, { arrow: true, s: 's-acc', w: 2 });
        s += T(x + 127, 82, i === 0 ? 'signal' : 'command', { size: 11, cls: 't-mut' });
      }
    });
    // door closed -> open
    s += T(80, 186, 'Door closed', { size: 12, cls: 't-mut' });
    s += K.rect(40, 196, 40, 70, { c: 1, r: 2 }) + K.rect(80, 196, 40, 70, { c: 1, r: 2 });
    s += K.line(150, 232, 290, 232, { arrow: true, s: 's-brand', w: 2 });
    s += T(220, 224, 'motor slides panels', { size: 11, cls: 't-mut' });
    s += T(360, 186, 'Door open', { size: 12, cls: 't-mut' });
    s += K.rect(300, 196, 40, 70, { c: 1, r: 2 }) + K.rect(380, 196, 40, 70, { c: 1, r: 2 });
    s += K.rect(342, 196, 36, 70, { dash: '4 3' });
    return K.svg(440, 280, s, { title: 'Motion sensor signals the control unit which commands the motor to open the door' });
  });

  D.register('xi5.connectivity', () => {
    let s = '';
    s += K.box(10, 10, 110, 44, 'IoT device', { c: 0, bold: true });
    s += K.box(320, 10, 110, 44, 'Phone / Cloud', { c: 1, bold: true });
    s += K.line(124, 32, 316, 32, { arrow: 'both', s: 's-brand', w: 2 });
    s += T(220, 24, 'Connectivity', { size: 13, w: 'b', cls: 't-acc' });
    s += T(220, 50, 'send data and receive commands', { size: 11, cls: 't-mut' });
    const items = [
      ['Wi-Fi', 'home, school, office'],
      ['Bluetooth', 'watch to phone'],
      ['ZigBee', 'smart home devices'],
      ['LoRaWAN', 'long range, farms'],
      ['NB-IoT', 'smart meters'],
      ['4G / 5G', 'mobile network'],
    ];
    items.forEach((v, i) => {
      const x = 10 + (i % 2) * 220;
      const y = 80 + Math.floor(i / 2) * 56;
      s += K.rect(x, y, 210, 46, { c: [0, 1, 2, 3, 4, 5][i] });
      s += T(x + 105, y + 19, v[0], { size: 14, w: 'b' }) + T(x + 105, y + 37, v[1], { size: 12, cls: 't-mut' });
    });
    s += T(220, 266, 'Weak or lost connection: no data, no commands', { size: 13, cls: 't-red' });
    return K.svg(440, 280, s, { title: 'Six connectivity technologies used by IoT devices' });
  });

  /* ---------- Lecture 3 ---------- */
  D.register('xi5.da-pipeline', () => {
    const rows = [
      ['1  Data Collection', 'raw data from sources', 'marks, attendance, surveys', 0],
      ['2  Data Storage', 'keep it safe', 'files, database, cloud', 1],
      ['3  Data Cleaning', 'fix the errors', 'missing marks, wrong roll no.', 3],
      ['4  Data Analysis', 'find patterns', 'which subjects are weak?', 2],
      ['5  Data Visualization', 'charts and graphs', 'bar chart, pie chart', 4],
      ['Decision', 'better decision', 'extra classes for weak students', 5],
    ];
    let s = '';
    s += T(100, 14, 'Step', { size: 13, w: 'b', cls: 't-acc' }) + T(330, 14, 'School result example', { size: 13, w: 'b', cls: 't-acc' });
    rows.forEach((r, i) => {
      const y = 24 + i * 56;
      s += K.rect(6, y, 190, 42, { c: r[3] });
      s += T(101, y + 18, r[0], { size: 14, w: 'b' }) + T(101, y + 34, r[1], { size: 11, cls: 't-mut' });
      s += K.line(198, y + 21, 226, y + 21, { s: 's-mut', dash: '3 3' });
      s += K.rect(228, y, 206, 42, { s: 's-brand', dash: i === 5 ? '5 3' : null });
      s += T(331, y + 22, r[2], { size: 12, vmid: true });
      if (i < 5) s += K.line(101, y + 43, 101, y + 55, { arrow: true, s: 's-acc', w: 2 });
    });
    return K.svg(440, 360, s, { title: 'Five steps of Data Analytics shown with a school result example' });
  });

  D.register('xi5.data-cleaning', () => {
    let s = '';
    s += T(92, 16, 'Raw data (dirty)', { size: 13, w: 'b', cls: 't-red' });
    s += T(348, 16, 'Clean data', { size: 13, w: 'b', cls: 't-grn' });
    const dirty = [['Roll', 'Name', 'Marks'], ['101', 'Ali', '78'], ['102', 'Sara', ''], ['1O3', 'Bilal', '65'], ['101', 'Ali', '78']];
    const fills = [[], [], [null, null, 3], [7, null, null], [4, 4, 4]];
    s += K.grid(8, 26, 56, 30, dirty, { head: true, fills, size: 13 });
    const clean = [['Roll', 'Name', 'Marks'], ['101', 'Ali', '78'], ['102', 'Sara', '82'], ['103', 'Bilal', '65']];
    s += K.grid(262, 26, 56, 30, clean, { head: true, fills: [[], [5, 5, 5], [5, 5, 5], [5, 5, 5]], size: 13 });
    s += K.line(186, 86, 254, 86, { arrow: true, s: 's-brand', w: 3 });
    s += T(220, 76, 'clean', { size: 13, w: 'b', cls: 't-acc' });
    // legend
    const lg = [[3, 'missing value'], [7, 'wrong roll no.'], [4, 'duplicate record']];
    lg.forEach((v, i) => {
      const y = 196 + i * 26;
      s += K.rect(60, y, 22, 16, { c: v[0], r: 3 }) + T(94, y + 12, v[1], { size: 13, anchor: 'start' });
    });
    s += T(300, 232, 'Fix mistakes before results', { size: 12, cls: 't-mut' });
    return K.svg(440, 270, s, { title: 'Data cleaning: missing value, wrong roll number and duplicate row are fixed' });
  });

  D.register('xi5.da-charts', () => {
    let s = '';
    s += T(120, 16, 'Marks by subject (bar chart)', { size: 13, w: 'b' });
    s += T(360, 16, 'Pass / Fail (pie chart)', { size: 13, w: 'b' });
    const base = 190;
    s += K.line(24, base, 240, base, { s: 's-mut' }) + K.line(24, base, 24, 36, { s: 's-mut' });
    const subs = [['Urdu', 72], ['Eng', 65], ['Math', 48], ['Phy', 55], ['CS', 80]];
    subs.forEach((v, i) => {
      const h = v[1] * 1.4;
      const x = 36 + i * 41;
      s += K.rect(x, base - h, 30, h, { c: v[0] === 'Math' ? 3 : 0, r: 3 });
      s += T(x + 15, base - h - 5, String(v[1]), { size: 11 }) + T(x + 15, base + 16, v[0], { size: 11, cls: 't-mut' });
    });
    s += T(120, 226, 'Maths is weakest', { size: 12, cls: 't-red' });
    // pie
    const cx = 360;
    const cy = 100;
    const r = 56;
    const a0 = -Math.PI / 2;
    const a1 = a0 + 0.18 * 2 * Math.PI;
    s += K.circle(cx, cy, r, { c: 5 });
    s += K.path('M' + cx + ' ' + cy + ' L' + cx + ' ' + (cy - r) + ' A' + r + ' ' + r + ' 0 0 1 ' + (cx + r * Math.cos(a1)).toFixed(1) + ' ' + (cy + r * Math.sin(a1)).toFixed(1) + ' Z', { c: 3 });
    s += T(cx - 20, cy + 14, 'Pass', { size: 13, w: 'b' }) + T(cx - 20, cy + 30, '82%', { size: 13 });
    s += T(cx + 10, cy - r - 6, 'Fail 18%', { size: 12, w: 'b', cls: 't-red', anchor: 'start' });
    s += T(cx, 180, 'parts of 100%', { size: 11, cls: 't-mut' });
    return K.svg(440, 240, s, { title: 'A bar chart of marks by subject and a pie chart of pass and fail percentage' });
  });

  /* ---------- Lecture 4 ---------- */
  D.register('xi5.smart-city', () => {
    let s = '';
    const w = 212;
    const h = 130;
    const pos = [[0, 0], [228, 0], [0, 142], [228, 142]];
    // traffic
    let x = pos[0][0], y = pos[0][1], cx = x + w / 2;
    let ic = K.rect(cx - 15, y + 8, 30, 66, { c: 6, r: 6 }) + K.circle(cx, y + 22, 7, { c: 3 }) + K.circle(cx, y + 41, 7, { c: 4 }) + K.circle(cx, y + 60, 7, { c: 5 });
    ic += K.rect(cx + 28, y + 14, 26, 14, { c: 1, r: 3 }) + K.circle(cx + 41, y + 21, 4, {}) + K.line(cx + 15, y + 30, cx + 28, y + 24, { s: 's-mut' });
    s += card(x, y, w, h, ic, 'Smart Traffic', 'signals adjust by traffic flow', 0);
    // street light
    x = pos[1][0]; y = pos[1][1]; cx = x + w / 2;
    ic = K.line(cx - 18, y + 76, cx - 18, y + 18, { s: 's-mut', w: 3 }) + K.line(cx - 18, y + 18, cx + 8, y + 18, { s: 's-mut', w: 3 });
    ic += K.poly([[cx + 2, y + 20], [cx + 16, y + 20], [cx + 22, y + 30], [cx - 4, y + 30]], { c: 4 });
    ic += K.poly([[cx - 4, y + 32], [cx + 22, y + 32], [cx + 34, y + 76], [cx - 16, y + 76]], { c: 4, cls: 'beam' }).replace('class="shape c4 beam"', 'class="shape c4" opacity="0.35"');
    ic += K.circle(cx + 56, y + 24, 9, { c: 4 });
    [[0, -15], [0, 15], [-15, 0], [15, 0]].forEach((d) => (ic += K.line(cx + 56 + d[0] * 0.75, y + 24 + d[1] * 0.75, cx + 56 + d[0], y + 24 + d[1], { s: 's-acc', w: 2 })));
    s += card(x, y, w, h, ic, 'Smart Street Lighting', 'ON/OFF by daylight', 1);
    // parking
    x = pos[2][0]; y = pos[2][1]; cx = x + w / 2;
    ic = K.rect(cx - 66, y + 12, 22, 22, { c: 1, r: 4 }) + T(cx - 55, y + 24, 'P', { size: 15, w: 'b', vmid: true, cls: 't-wht' });
    [0, 1, 2].forEach((i) => {
      const sx = cx - 54 + i * 40;
      ic += K.rect(sx, y + 40, 34, 36, { dash: '4 3' });
      if (i !== 1) ic += K.rect(sx + 6, y + 46, 22, 24, { c: 3, r: 5 });
      else ic += tick(sx + 7, y + 49) + T(sx + 17, y + 36, 'free', { size: 11, cls: 't-grn' });
    });
    s += card(x, y, w, h, ic, 'Smart Parking', 'sensors find the empty slot', 2);
    // waste
    x = pos[3][0]; y = pos[3][1]; cx = x + w / 2;
    ic = K.poly([[cx - 20, y + 28], [cx + 20, y + 28], [cx + 15, y + 76], [cx - 15, y + 76]], { c: 5 });
    ic += K.rect(cx - 24, y + 18, 48, 10, { c: 6, r: 3 });
    ic += K.line(cx - 8, y + 36, cx - 7, y + 68, { s: 's-mut' }) + K.line(cx + 8, y + 36, cx + 7, y + 68, { s: 's-mut' });
    ic += wifi(cx + 34, y + 44) + T(cx + 50, y + 66, 'FULL', { size: 12, w: 'b', cls: 't-red', anchor: 'start' });
    s += card(x, y, w, h, ic, 'Waste Management', 'smart bin sends an alert', 3);
    return K.svg(440, 272, s, { title: 'Smart city applications: traffic, street lighting, parking and waste' });
  });

  D.register('xi5.smart-grid', () => {
    let s = '';
    s += K.rect(150, 8, 270, 44, { c: 1 }) + T(285, 24, 'Utility control centre', { size: 14, w: 'b' }) + T(285, 42, 'sees usage, plans load', { size: 12, cls: 't-mut' });
    // power station
    s += K.rect(10, 130, 76, 56, { c: 6 }) + K.rect(20, 100, 14, 30, { c: 6, r: 2 }) + K.rect(46, 110, 14, 20, { c: 6, r: 2 });
    s += T(48, 206, 'Power station', { size: 12 });
    s += K.line(86, 160, 396, 160, { s: 's-acc', w: 4 });
    s += T(150, 148, 'electricity', { size: 12, cls: 't-acc' });
    [215, 290, 365].forEach((x, i) => {
      s += K.poly([[x - 30, 188], [x, 168], [x + 30, 188]], { c: 3 }) + K.rect(x - 24, 188, 48, 22, { c: 6, r: 2 });
      s += K.rect(x - 8, 193, 16, 12, { c: 4, r: 2 });
      s += K.line(x, 168, x, 160, { s: 's-acc', w: 2 });
      s += K.line(x, 156, x, 58, { arrow: true, dash: '4 3', s: 's-brand', w: 2 });
    });
    s += T(290, 228, 'Smart meters in homes', { size: 12 });
    s += T(298, 106, 'meter data', { size: 12, cls: 't-acc', anchor: 'start' });
    return K.svg(440, 240, s, { title: 'Smart grid: smart meters send usage data to the control centre while electricity flows to homes' });
  });

  D.register('xi5.telemedicine', () => {
    let s = '';
    // patient
    s += K.circle(60, 74, 13, { c: 4 }) + K.line(60, 87, 60, 132, { s: 's-mut', w: 4 }) + K.line(60, 98, 38, 118, { s: 's-mut', w: 4 }) + K.line(60, 98, 82, 118, { s: 's-mut', w: 4 });
    s += K.line(60, 132, 46, 162, { s: 's-mut', w: 4 }) + K.line(60, 132, 74, 162, { s: 's-mut', w: 4 });
    s += K.rect(32, 114, 14, 10, { c: 1, r: 3 });
    s += T(66, 40, 'Heart 98', { size: 12, w: 'b', cls: 't-red' });
    s += T(60, 190, 'Patient in village', { size: 13, w: 'b' }) + T(60, 206, 'wears a smartwatch', { size: 12, cls: 't-mut' });
    // cloud
    s += cloud(172, 56, 1.7, 1);
    s += T(220, 96, 'Internet', { size: 13, w: 'b', vmid: true });
    // hospital
    s += K.rect(334, 62, 96, 100, { c: 0, r: 4 }) + K.rect(366, 118, 32, 44, { c: 6, r: 2 });
    s += K.rect(374, 74, 16, 36, { c: 3, r: 2 }) + K.rect(364, 84, 36, 16, { c: 3, r: 2 }) + K.rect(374, 84, 16, 16, { c: 3, r: 0 });
    s += T(382, 190, 'City hospital', { size: 13, w: 'b' }) + T(382, 206, 'doctor checks data', { size: 12, cls: 't-mut' });
    s += K.line(92, 96, 164, 96, { arrow: true, s: 's-brand', w: 2 }) + K.line(280, 96, 330, 96, { arrow: true, s: 's-brand', w: 2 });
    s += K.line(330, 146, 280, 146, { arrow: true, s: 's-grn', w: 2, dash: '4 3' }) + K.line(164, 146, 92, 146, { arrow: true, s: 's-grn', w: 2, dash: '4 3' });
    s += T(128, 88, 'data', { size: 12, cls: 't-mut' }) + T(305, 88, 'data', { size: 12, cls: 't-mut' });
    s += T(220, 176, 'advice / alert', { size: 12, cls: 't-grn' });
    return K.svg(440, 220, s, { title: 'Telemedicine: smartwatch data goes through the cloud to a doctor and advice returns to the village' });
  });

  /* ---------- Lecture 5 ---------- */
  D.register('xi5.smart-home', () => {
    let s = '';
    s += K.poly([[4, 100], [142, 30], [280, 100]], { c: 3 });
    s += K.rect(14, 100, 256, 120, { r: 2 });
    // bulb
    s += K.circle(56, 140, 14, { c: 4 }) + K.rect(50, 154, 12, 8, { c: 6, r: 2 });
    [[-22, 0], [22, 0], [0, -22]].forEach((d) => (s += K.line(56 + d[0] * 0.8, 140 + d[1] * 0.8, 56 + d[0], 140 + d[1], { s: 's-acc', w: 2 })));
    s += T(56, 188, 'Light', { size: 12 });
    // camera
    s += K.rect(98, 128, 38, 22, { c: 1, r: 4 }) + K.circle(117, 139, 6, {}) + K.line(117, 150, 117, 160, { s: 's-mut', w: 3 });
    s += T(117, 188, 'Camera', { size: 12 });
    // AC
    s += K.rect(158, 124, 44, 24, { c: 0, r: 4 }) + K.line(164, 140, 196, 140, { s: 's-mut' }) + K.line(164, 144, 196, 144, { s: 's-mut' });
    [168, 180, 192].forEach((x) => (s += K.line(x, 154, x - 3, 164, { s: 's-acc', w: 2 })));
    s += T(180, 188, 'AC', { size: 12 });
    // speaker
    s += K.rect(224, 124, 26, 38, { c: 2, r: 9 }) + K.circle(237, 134, 4, {});
    s += T(237, 188, 'Voice', { size: 12 });
    s += T(142, 238, 'Smart home', { size: 12, cls: 't-mut' });
    // phone
    s += K.rect(346, 70, 66, 112, { c: 1, r: 12 }) + K.rect(354, 84, 50, 78, { r: 4 });
    s += T(379, 106, 'Lights', { size: 11 }) + T(379, 124, 'Camera', { size: 11 }) + T(379, 142, 'AC', { size: 11 });
    s += K.line(340, 110, 286, 110, { arrow: 'both', dash: '4 3', s: 's-brand', w: 2 });
    s += T(313, 100, 'Wi-Fi', { size: 12, cls: 't-acc' });
    s += T(379, 204, 'Mobile app', { size: 13, w: 'b' }) + T(379, 220, 'control from away', { size: 12, cls: 't-mut' });
    return K.svg(440, 246, s, { title: 'Smart home devices controlled by a mobile app over the internet' });
  });

  D.register('xi5.smart-farm', () => {
    let s = '';
    // field
    s += K.rect(0, 190, 440, 60, { c: 5, r: 0 });
    for (let i = 0; i < 7; i++) s += K.line(10 + i * 44, 222, 30 + i * 44, 200, { s: 's-grn', w: 2 }) + K.line(30 + i * 44, 200, 40 + i * 44, 222, { s: 's-grn', w: 2 });
    // pipe to field
    s += K.line(352, 232, 40, 232, { s: 's-acc', w: 4 });
    // 1 soil sensor
    s += K.line(60, 196, 60, 224, { s: 's-mut', w: 3 }) + K.rect(50, 172, 20, 24, { c: 0, r: 4 });
    // 2 weather pole
    s += K.line(160, 192, 160, 132, { s: 's-mut', w: 3 }) + K.rect(144, 116, 32, 18, { c: 1, r: 3 }) + K.line(160, 116, 160, 104, { s: 's-mut', w: 2 }) + K.circle(160, 102, 4, { c: 4 });
    // 6 drone
    s += K.rect(250, 112, 34, 10, { c: 6, r: 4 }) + K.line(240, 108, 260, 108, { s: 's-mut', w: 3 }) + K.line(274, 108, 294, 108, { s: 's-mut', w: 3 }) + K.circle(267, 128, 4, { c: 2 });
    // 3 cloud
    s += cloud(214, 14, 1.4, 1);
    // 4 phone
    s += K.rect(380, 20, 36, 62, { c: 1, r: 8 }) + K.rect(385, 28, 26, 40, { r: 3 }) + T(398, 48, 'ON', { size: 11, w: 'b', vmid: true });
    // 5 pump house
    s += K.rect(352, 140, 66, 50, { c: 4, r: 4 }) + K.circle(385, 165, 12, { c: 6 }) + K.rect(348, 226, 12, 12, { c: 3, r: 2 });
    s += K.line(354, 190, 354, 226, { s: 's-acc', w: 4 });
    // arrows
    s += K.polyline([[60, 170], [60, 44], [210, 44]], { arrow: true, dash: '4 3', s: 's-brand', w: 2 });
    s += K.line(160, 98, 222, 56, { arrow: true, dash: '4 3', s: 's-brand', w: 2 });
    s += K.line(267, 108, 267, 64, { arrow: true, dash: '4 3', s: 's-brand', w: 2 });
    s += K.line(300, 44, 376, 44, { arrow: true, s: 's-brand', w: 2 });
    s += K.line(398, 84, 398, 136, { arrow: true, s: 's-red', w: 2 });
    // badges
    [[60, 160, 1], [138, 108, 2], [285, 26, 3], [398, 100, 4], [385, 132, 5], [300, 134, 6]].forEach((b) => {
      s += K.circle(b[0], b[1], 10, { c: 6, s: 's-brand' }) + T(b[0], b[1] + 1, String(b[2]), { size: 12, w: 'b', vmid: true });
    });
    // legend
    const lg = ['1 Soil moisture sensor', '2 Weather sensor', '3 Cloud and analytics', '4 Farmer phone app', '5 Tube-well pump + valve', '6 Drone with camera'];
    lg.forEach((v, i) => (s += T(12 + Math.floor(i / 3) * 226, 272 + (i % 3) * 20, v, { size: 12, anchor: 'start' })));
    return K.svg(440, 336, s, { title: 'Smart farming: soil and weather sensors, cloud, farmer app, pump and drone' });
  });

  /* ---------- Lecture 6 ---------- */
  D.register('xi5.skills-wheel', () => {
    let s = '';
    const skills = ['Programming', 'Electronics', 'Networking', 'Data handling', 'Problem-Solving', 'Communication', 'Ethics'];
    const cx = 220;
    const cy = 154;
    s += skills
      .map((v, i) => {
        const a = (i / 7) * 2 * Math.PI - Math.PI / 2;
        return K.line(cx, cy, cx + 160 * Math.cos(a), cy + 112 * Math.sin(a), { s: 's-mut' });
      })
      .join('');
    s += K.circle(cx, cy, 46, { c: 4 }) + T(cx, cy - 6, 'IoT / AI', { size: 14, w: 'b', vmid: true }) + T(cx, cy + 12, 'career', { size: 13, vmid: true });
    skills.forEach((v, i) => {
      const a = (i / 7) * 2 * Math.PI - Math.PI / 2;
      const x = cx + 160 * Math.cos(a);
      const y = cy + 112 * Math.sin(a);
      s += K.box(x - 52, y - 15, 104, 30, v, { c: i % 8, size: 12 });
    });
    return K.svg(440, 310, s, { title: 'Seven skills needed for IoT and AI careers' });
  });

  /* ---------- Lecture 7 ---------- */
  D.register('xi5.source-types', () => {
    const rows = [
      ['Primary', 'original, first-hand', 'interview, diary, speech, photo, NADRA record', 5],
      ['Secondary', 'explained by others', 'textbook, news report, research paper, PBS report', 1],
      ['Tertiary', 'summary of both', 'encyclopedia, dictionary, handbook, Wikipedia', 4],
    ];
    let s = '';
    rows.forEach((r, i) => {
      const y = 8 + i * 98;
      s += K.rect(6, y, 132, 66, { c: r[3] });
      s += T(72, y + 28, r[0], { size: 15, w: 'b' }) + T(72, y + 48, r[1], { size: 11, cls: 't-mut' });
      s += K.rect(150, y, 284, 66, { s: 's-brand' });
      s += T(292, y + 33, r[2].replace(/(.{26,}?), /, '$1,\n'), { size: 13, vmid: true });
      if (i < 2) {
        s += K.line(72, y + 68, 72, y + 96, { arrow: true, s: 's-acc', w: 2 });
        s += T(82, y + 86, i === 0 ? 'studied and explained' : 'collected and summarised', { size: 12, cls: 't-mut', anchor: 'start' });
      }
    });
    return K.svg(440, 298, s, { title: 'Primary, secondary and tertiary sources of information with examples' });
  });

  D.register('xi5.source-chain', () => {
    let s = '';
    const b = [
      ['Census forms', 'and surveys', 'Primary', 5],
      ['PBS report', 'tables and graphs', 'Secondary', 1],
      ['Wikipedia', 'article: Pakistan', 'Tertiary', 4],
    ];
    b.forEach((v, i) => {
      const x = 6 + i * 150;
      s += K.rect(x, 40, 128, 70, { c: v[3] });
      s += T(x + 64, 66, v[0], { size: 14, w: 'b' }) + T(x + 64, 88, v[1], { size: 12, cls: 't-mut' });
      s += T(x + 64, 28, v[2], { size: 13, w: 'b', cls: 't-acc' });
      if (i < 2) s += K.line(x + 130, 75, x + 148, 75, { arrow: true, s: 's-acc', w: 2 });
    });
    s += T(220, 140, 'Data collected directly, then analysed, then summarised', { size: 12, cls: 't-mut' });
    return K.svg(440, 156, s, { title: 'Census data becomes a PBS report and then a Wikipedia summary' });
  });

  D.register('xi5.credibility', () => {
    const q = [
      ['Is it complete and recorded correctly?', 'Primary'],
      ['Is it true, not false or made up?', 'Primary'],
      ['Is it up to date?', 'Secondary'],
      ['Does it give proper references?', 'Secondary'],
      ['Has an expert verified it?', 'Secondary'],
      ['Is the website or author known?', 'Tertiary'],
      ['Is it detailed, not oversimplified?', 'Tertiary'],
    ];
    let s = T(220, 18, 'Credibility checklist', { size: 15, w: 'b' });
    q.forEach((v, i) => {
      const y = 32 + i * 38;
      s += K.rect(6, y, 26, 26, { s: 's-grn', r: 5 }) + tick(9, y + 4);
      s += T(42, y + 14, v[0], { size: 13, anchor: 'start', vmid: true });
      s += K.rect(356, y + 2, 78, 22, { c: [5, 1, 4][['Primary', 'Secondary', 'Tertiary'].indexOf(v[1])], r: 11 }) + T(395, y + 13, v[1], { size: 11, vmid: true });
    });
    s += K.rect(6, 304, 428, 44, { s: 's-brand', r: 10 });
    s += T(220, 320, 'Mostly YES: reliable, you can use it', { size: 13, w: 'b', cls: 't-grn' });
    s += T(220, 338, 'Any NO: check again, may be unreliable', { size: 13, w: 'b', cls: 't-red' });
    return K.svg(440, 360, s, { title: 'Checklist of seven questions for judging whether an information source is reliable' });
  });

  /* ---------- Lecture 8 ---------- */
  D.register('xi5.impact-scale', () => {
    let s = '';
    s += K.rect(205, 56, 30, 150, { c: 6, r: 3 }) + K.rect(150, 200, 140, 14, { c: 6, r: 4 });
    s += K.line(90, 56, 350, 56, { s: 's-mut', w: 5 }) + K.circle(220, 56, 10, { c: 4 });
    [[90, 5], [350, 3]].forEach((p) => {
      s += K.line(p[0], 56, p[0] - 56, 106, { s: 's-mut' }) + K.line(p[0], 56, p[0] + 56, 106, { s: 's-mut' });
      s += K.poly([[p[0] - 66, 106], [p[0] + 66, 106], [p[0] + 50, 134], [p[0] - 50, 134]], { c: p[1] });
    });
    s += T(90, 120, 'Positive', { size: 14, w: 'b', vmid: true });
    s += T(350, 120, 'Negative', { size: 14, w: 'b', vmid: true });
    s += T(90, 158, 'easy learning\nfast communication\nbetter healthcare', { size: 12, lh: 17 });
    s += T(350, 158, 'privacy risk\nscreen time\njob changes', { size: 12, lh: 17 });
    s += T(220, 238, 'Use technology responsibly to keep the balance', { size: 13, cls: 't-acc' });
    return K.svg(440, 252, s, { title: 'Balance of positive and negative impacts of computing' });
  });

  /* ---------- Lecture 9 ---------- */
  D.register('xi5.assistive-types', () => {
    let s = '';
    const w = 212;
    const h = 130;
    // mobility
    let x = 0, y = 0, cx = x + w / 2;
    let ic = K.circle(cx - 6, y + 52, 20, { s: 's-acc' }) + K.circle(cx - 6, y + 52, 3, { c: 4 });
    ic += K.polyline([[cx - 14, y + 18], [cx - 14, y + 44], [cx + 18, y + 44]], { s: 's-mut', w: 4 }) + K.line(cx + 18, y + 44, cx + 28, y + 70, { s: 's-mut', w: 4 }) + K.circle(cx - 14, y + 12, 6, { c: 4 });
    s += card(x, y, w, h, ic, 'Mobility aids', 'wheelchair, walker, crutches', 0);
    // sensory
    x = 228; cx = x + w / 2;
    ic = K.ellipse(cx - 24, y + 48, 22, 12, { s: 's-acc' }) + K.circle(cx - 24, y + 48, 7, { c: 1 }) + K.dot(cx - 24, y + 48, 3);
    ic += wifi(cx + 24, y + 48);
    s += card(x, y, w, h, ic, 'Sensory aids', 'screen reader, hearing aid', 1);
    // communication
    x = 0; y = 142; cx = x + w / 2;
    ic = K.rect(cx - 36, y + 14, 72, 48, { c: 2, r: 10 }) + K.poly([[cx - 12, y + 62], [cx - 22, y + 76], [cx + 2, y + 62]], { c: 2 });
    ic += K.circle(cx - 14, y + 38, 8, { c: 4 }) + K.rect(cx + 2, y + 30, 22, 16, { c: 5, r: 3 });
    s += card(x, y, w, h, ic, 'Communication aids', 'speech device, picture board', 2);
    // cognitive
    x = 228; cx = x + w / 2;
    ic = K.path('M' + cx + ' ' + (y + 28) + ' Q' + (cx - 20) + ' ' + (y + 16) + ' ' + (cx - 40) + ' ' + (y + 24) + ' L' + (cx - 40) + ' ' + (y + 66) + ' Q' + (cx - 20) + ' ' + (y + 58) + ' ' + cx + ' ' + (y + 70) + ' Z', { c: 4 });
    ic += K.path('M' + cx + ' ' + (y + 28) + ' Q' + (cx + 20) + ' ' + (y + 16) + ' ' + (cx + 40) + ' ' + (y + 24) + ' L' + (cx + 40) + ' ' + (y + 66) + ' Q' + (cx + 20) + ' ' + (y + 58) + ' ' + cx + ' ' + (y + 70) + ' Z', { c: 4 });
    [32, 42, 52].forEach((d) => (ic += K.line(cx - 32, y + d, cx - 8, y + d + 3, { s: 's-mut' }) + K.line(cx + 8, y + d + 3, cx + 32, y + d, { s: 's-mut' })));
    s += card(x, y, w, h, ic, 'Cognitive and learning aids', 'audiobook, spell-check', 3);
    return K.svg(440, 272, s, { title: 'Four groups of assistive technology: mobility, sensory, communication and cognitive' });
  });
})();
