/** Inline SVG helpers for lecture-note diagrams */

export function stairsRampSvg() {
  return `<svg viewBox="0 0 420 140" width="400" height="133" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Stairs versus ramp analogy">
  <text x="8" y="18" font-size="12" font-weight="600" fill="#1a2332">Discrete (stairs)</text>
  <rect x="20" y="100" width="28" height="12" fill="#2563eb"/>
  <rect x="48" y="88" width="28" height="24" fill="#2563eb"/>
  <rect x="76" y="76" width="28" height="36" fill="#2563eb"/>
  <rect x="104" y="64" width="28" height="48" fill="#2563eb"/>
  <rect x="132" y="52" width="28" height="60" fill="#2563eb"/>
  <line x1="20" y1="112" x2="160" y2="112" stroke="#94a3b8" stroke-width="1"/>
  <text x="220" y="18" font-size="12" font-weight="600" fill="#1a2332">Continuous (ramp)</text>
  <polygon points="240,112 380,40 380,112" fill="#059669" opacity="0.35"/>
  <line x1="240" y1="112" x2="380" y2="40" stroke="#059669" stroke-width="3"/>
  <line x1="240" y1="112" x2="380" y2="112" stroke="#94a3b8" stroke-width="1"/>
</svg>`;
}

export function analogDigitalWaveSvg() {
  return `<svg viewBox="0 0 420 160" width="400" height="152" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Analog sine wave and digital square wave">
  <text x="8" y="16" font-size="11" fill="#4a5568">Analog</text>
  <path d="M 20 70 Q 50 30 80 70 T 140 70 T 200 70" fill="none" stroke="#7c3aed" stroke-width="2"/>
  <text x="8" y="100" font-size="11" fill="#4a5568">Digital</text>
  <polyline points="20,130 20,110 60,110 60,130 100,130 100,110 140,110 140,130 180,130 180,110 220,110" fill="none" stroke="#2563eb" stroke-width="2"/>
  <text x="230" y="115" font-size="10" fill="#2563eb">HIGH</text>
  <text x="230" y="135" font-size="10" fill="#64748b">LOW</text>
</svg>`;
}

export function logicGateRowSvg() {
  return `<svg viewBox="0 0 440 72" width="420" height="69" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Logic gate symbols">
  <g font-size="9" fill="#1a2332" text-anchor="middle">
    <rect x="8" y="20" width="36" height="32" rx="2" fill="#fff" stroke="#334155"/>
    <text x="26" y="40">&amp;</text><text x="26" y="62">AND</text>
    <path d="M 58 36 L 68 36" stroke="#334155"/><circle cx="72" cy="36" r="3" fill="#334155"/>
    <rect x="78" y="20" width="36" height="32" rx="2" fill="#fff" stroke="#334155"/>
    <text x="96" y="40">≥1</text><text x="96" y="62">OR</text>
    <polygon points="130,36 142,28 142,44" fill="#fff" stroke="#334155"/><circle cx="146" cy="36" r="3" fill="#334155"/>
    <text x="138" y="62">NOT</text>
    <rect x="158" y="20" width="36" height="32" rx="2" fill="#fff" stroke="#334155"/><text x="168" y="32" font-size="7">o</text>
    <text x="176" y="40">&amp;</text><text x="176" y="62">NAND</text>
    <rect x="208" y="20" width="36" height="32" rx="2" fill="#fff" stroke="#334155"/>
    <text x="226" y="40">=1</text><text x="226" y="62">XOR</text>
    <rect x="258" y="20" width="36" height="32" rx="2" fill="#fff" stroke="#334155"/>
    <text x="276" y="40">=1</text><circle cx="288" cy="36" r="3" fill="#334155"/><text x="276" y="62">XNOR</text>
  </g>
</svg>`;
}

export function osiStackSvg() {
  const layers = [
    ["7", "Application", "#dbeafe"],
    ["6", "Presentation", "#bfdbfe"],
    ["5", "Session", "#93c5fd"],
    ["4", "Transport", "#60a5fa"],
    ["3", "Network", "#3b82f6"],
    ["2", "Data Link", "#2563eb"],
    ["1", "Physical", "#1d4ed8"],
  ];
  return `<svg viewBox="0 0 280 220" width="260" height="204" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="OSI seven layer model">
    ${layers
      .map(
        ([n, name, fill], i) =>
          `<rect x="40" y="${10 + i * 28}" width="200" height="24" rx="4" fill="${fill}" stroke="#1e40af"/>
           <text x="52" y="${27 + i * 28}" font-size="11" fill="#0f172a" font-weight="600">${n}</text>
           <text x="72" y="${27 + i * 28}" font-size="11" fill="#0f172a">${name}</text>`
      )
      .join("")}
    <text x="140" y="215" font-size="10" fill="#64748b" text-anchor="middle">Data ↓  Physical ↑</text>
  </svg>`;
}

export function waterfallSvg() {
  return `<svg viewBox="0 0 300 200" width="280" height="187" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Waterfall SDLC">
    ${["Requirements", "Design", "Implementation", "Testing", "Deployment", "Maintenance"]
      .map(
        (label, i) =>
          `<rect x="40" y="${15 + i * 28}" width="180" height="22" rx="4" fill="#ede9fe" stroke="#7c3aed"/>
           <text x="130" y="${30 + i * 28}" font-size="10" text-anchor="middle" fill="#1a2332">${label}</text>
           ${i < 5 ? `<polygon points="130,${37 + i * 28} 125,${43 + i * 28} 135,${43 + i * 28}" fill="#7c3aed"/>` : ""}`
      )
      .join("")}
  </svg>`;
}

export function ctDecompositionSvg() {
  return `<svg viewBox="0 0 320 120" width="300" height="112" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Decomposition tree">
    <rect x="120" y="8" width="80" height="28" rx="6" fill="#2563eb" opacity="0.15" stroke="#2563eb"/>
    <text x="160" y="26" font-size="10" text-anchor="middle" fill="#1a2332">Big problem</text>
    <line x1="160" y1="36" x2="160" y2="50" stroke="#64748b"/>
    <line x1="60" y1="50" x2="260" y2="50" stroke="#64748b"/>
    <line x1="60" y1="50" x2="60" y2="58" stroke="#64748b"/>
    <line x1="160" y1="50" x2="160" y2="58" stroke="#64748b"/>
    <line x1="260" y1="50" x2="260" y2="58" stroke="#64748b"/>
    ${["Step A", "Step B", "Step C"]
      .map(
        (t, i) =>
          `<rect x="${20 + i * 100}" y="58" width="80" height="26" rx="4" fill="#f8fafc" stroke="#cbd5e1"/>
           <text x="${60 + i * 100}" y="75" font-size="9" text-anchor="middle">${t}</text>`
      )
      .join("")}
  </svg>`;
}

export function hciModelSvg() {
  return `<svg viewBox="0 0 360 160" width="340" height="151" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="HCI interaction model">
    <ellipse cx="70" cy="80" rx="55" ry="45" fill="#ccfbf1" stroke="#0d9488"/>
    <text x="70" y="75" font-size="11" text-anchor="middle" font-weight="600">Human</text>
    <text x="70" y="90" font-size="9" text-anchor="middle">Input / Output</text>
    <rect x="230" y="45" width="100" height="70" rx="8" fill="#dbeafe" stroke="#2563eb"/>
    <text x="280" y="75" font-size="11" text-anchor="middle" font-weight="600">Computer</text>
    <text x="280" y="92" font-size="9" text-anchor="middle">UI + System</text>
    <line x1="125" y1="65" x2="225" y2="65" stroke="#334155" marker-end="url(#arr)"/>
    <line x1="225" y1="95" x2="125" y2="95" stroke="#334155" marker-end="url(#arr)"/>
    <text x="175" y="58" font-size="9" text-anchor="middle">Commands</text>
    <text x="175" y="108" font-size="9" text-anchor="middle">Feedback</text>
    <defs><marker id="arr" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto"><path d="M0,0 L6,3 L0,6 Z" fill="#334155"/></marker></defs>
  </svg>`;
}

export function dbRelationsSvg() {
  return `<svg viewBox="0 0 340 100" width="320" height="94" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Database relationships">
    <rect x="10" y="25" width="70" height="50" rx="4" fill="#f8fafc" stroke="#64748b"/>
    <text x="45" y="55" font-size="10" text-anchor="middle">Student</text>
    <rect x="135" y="25" width="70" height="50" rx="4" fill="#f8fafc" stroke="#64748b"/>
    <text x="170" y="55" font-size="10" text-anchor="middle">Course</text>
    <rect x="260" y="25" width="70" height="50" rx="4" fill="#f8fafc" stroke="#64748b"/>
    <text x="295" y="55" font-size="10" text-anchor="middle">Enroll</text>
    <line x1="80" y1="50" x2="135" y2="50" stroke="#2563eb" stroke-width="2"/>
    <text x="107" y="42" font-size="8" text-anchor="middle">1:M</text>
  </svg>`;
}

export const diagramMap = {
  stairsRamp: stairsRampSvg,
  analogDigital: analogDigitalWaveSvg,
  logicGates: logicGateRowSvg,
  osi: osiStackSvg,
  waterfall: waterfallSvg,
  decomposition: ctDecompositionSvg,
  hci: hciModelSvg,
  dbRelations: dbRelationsSvg,
};

export function renderDiagram(key) {
  const fn = diagramMap[key];
  return fn ? fn() : "";
}
