/* Educational SVG figures for the CS XI / XII cheat-sheet. */
const DIAGRAMS = {
  "stairs-ramp": {
    caption: "Discrete values sit on stair steps. Continuous values can stand anywhere on the ramp.",
    svg: `<svg viewBox="0 0 640 210" role="img" aria-label="Stairs versus ramp">
      <rect width="640" height="210" fill="#f7f4ea"/>
      <text x="160" y="28" text-anchor="middle" font-size="16" font-weight="700" fill="#1b212f">Discrete = stairs</text>
      <text x="480" y="28" text-anchor="middle" font-size="16" font-weight="700" fill="#1b212f">Continuous = ramp</text>
      <polyline points="40,170 40,140 90,140 90,110 140,110 140,80 190,80 190,50 240,50 240,170" fill="none" stroke="#1f5aa6" stroke-width="4"/>
      <text x="65" y="162" font-size="13" fill="#1f5aa6">1</text>
      <text x="112" y="132" font-size="13" fill="#1f5aa6">2</text>
      <text x="162" y="102" font-size="13" fill="#1f5aa6">3</text>
      <text x="210" y="72" font-size="13" fill="#1f5aa6">4</text>
      <line x1="360" y1="170" x2="600" y2="170" stroke="#9aa3b2" stroke-width="2"/>
      <line x1="360" y1="170" x2="360" y2="40" stroke="#9aa3b2" stroke-width="2"/>
      <line x1="360" y1="170" x2="600" y2="50" stroke="#0f7b6c" stroke-width="4"/>
      <circle cx="470" cy="116" r="5" fill="#b42317"/>
      <text x="478" y="110" font-size="13" fill="#b42317">any height</text>
    </svg>`
  },
  "analog-digital": {
    caption: "Analog is a smooth sine wave. Digital jumps between HIGH (1) and LOW (0).",
    svg: `<svg viewBox="0 0 640 230" role="img" aria-label="Analog sine wave and digital square wave">
      <rect width="640" height="230" fill="#f7f4ea"/>
      <text x="160" y="24" text-anchor="middle" font-size="15" font-weight="700" fill="#1b212f">Analog (sine)</text>
      <text x="480" y="24" text-anchor="middle" font-size="15" font-weight="700" fill="#1b212f">Digital (square)</text>
      <line x1="30" y1="150" x2="290" y2="150" stroke="#9aa3b2"/>
      <line x1="40" y1="50" x2="40" y2="180" stroke="#9aa3b2"/>
      <text x="28" y="46" font-size="12" fill="#4a5467">V</text>
      <text x="292" y="168" font-size="12" fill="#4a5467">t</text>
      <path d="M40 150 C70 150 70 70 110 70 C150 70 150 230 190 230 C230 230 230 70 270 70" fill="none" stroke="#1f5aa6" stroke-width="3"/>
      <line x1="350" y1="150" x2="620" y2="150" stroke="#9aa3b2"/>
      <line x1="360" y1="50" x2="360" y2="180" stroke="#9aa3b2"/>
      <text x="348" y="46" font-size="12" fill="#4a5467">V</text>
      <text x="610" y="168" font-size="12" fill="#4a5467">t</text>
      <polyline points="370,150 370,70 450,70 450,150 530,150 530,70 610,70" fill="none" stroke="#0f7b6c" stroke-width="3"/>
      <text x="400" y="64" font-size="13" fill="#0f7b6c">HIGH 1</text>
      <text x="470" y="168" font-size="13" fill="#b42317">LOW 0</text>
    </svg>`
  },
  "gates-basic": {
    caption: "AND is a D-shape, OR is a curved shield, NOT is a triangle plus a bubble.",
    svg: `<svg viewBox="0 0 660 200" role="img" aria-label="AND OR and NOT gate symbols">
      <rect width="660" height="200" fill="#f7f4ea"/>
      <text x="110" y="22" text-anchor="middle" font-weight="700" fill="#1b212f">AND</text>
      <path d="M70 50 H110 C150 50 150 130 110 130 H70 Z" fill="#e7eef8" stroke="#1f5aa6" stroke-width="3"/>
      <line x1="40" y1="74" x2="70" y2="74" stroke="#1b212f" stroke-width="2"/>
      <line x1="40" y1="106" x2="70" y2="106" stroke="#1b212f" stroke-width="2"/>
      <line x1="150" y1="90" x2="185" y2="90" stroke="#1b212f" stroke-width="2"/>
      <text x="28" y="78" font-size="13">A</text><text x="28" y="110" font-size="13">B</text><text x="190" y="94" font-size="13">Y</text>
      <text x="110" y="168" text-anchor="middle" font-size="14" fill="#1f5aa6">Y = A · B</text>
      <text x="330" y="22" text-anchor="middle" font-weight="700" fill="#1b212f">OR</text>
      <path d="M250 50 Q300 50 300 90 Q300 130 250 130 Q285 90 250 50 Z" fill="#e7f6f2" stroke="#0f7b6c" stroke-width="3"/>
      <line x1="230" y1="74" x2="268" y2="74" stroke="#1b212f" stroke-width="2"/>
      <line x1="230" y1="106" x2="268" y2="106" stroke="#1b212f" stroke-width="2"/>
      <line x1="300" y1="90" x2="340" y2="90" stroke="#1b212f" stroke-width="2"/>
      <text x="214" y="78" font-size="13">A</text><text x="214" y="110" font-size="13">B</text><text x="346" y="94" font-size="13">Y</text>
      <text x="300" y="168" text-anchor="middle" font-size="14" fill="#0f7b6c">Y = A + B</text>
      <text x="530" y="22" text-anchor="middle" font-weight="700" fill="#1b212f">NOT</text>
      <path d="M460 50 L460 130 L530 90 Z" fill="#fff6e0" stroke="#8a5a00" stroke-width="3"/>
      <circle cx="542" cy="90" r="8" fill="#fff" stroke="#8a5a00" stroke-width="3"/>
      <line x1="430" y1="90" x2="460" y2="90" stroke="#1b212f" stroke-width="2"/>
      <line x1="550" y1="90" x2="585" y2="90" stroke="#1b212f" stroke-width="2"/>
      <text x="414" y="94" font-size="13">A</text><text x="590" y="94" font-size="13">Y</text>
      <text x="520" y="168" text-anchor="middle" font-size="14" fill="#8a5a00">Y = A'</text>
    </svg>`
  },
  "gates-universal": {
    caption: "A bubble on the output means NOT. NAND is AND plus a bubble. NOR is OR plus a bubble. Either one can build every other gate.",
    svg: `<svg viewBox="0 0 640 180" role="img" aria-label="NAND and NOR gates">
      <rect width="640" height="180" fill="#f7f4ea"/>
      <text x="170" y="24" text-anchor="middle" font-weight="700">NAND = AND + bubble</text>
      <path d="M90 48 H130 C168 48 168 120 130 120 H90 Z" fill="#e7eef8" stroke="#1f5aa6" stroke-width="3"/>
      <circle cx="178" cy="84" r="8" fill="#fff" stroke="#1f5aa6" stroke-width="3"/>
      <text x="170" y="156" text-anchor="middle" fill="#1f5aa6">Y = (A · B)'</text>
      <text x="490" y="24" text-anchor="middle" font-weight="700">NOR = OR + bubble</text>
      <path d="M390 48 Q440 48 440 84 Q440 120 390 120 Q424 84 390 48 Z" fill="#e7f6f2" stroke="#0f7b6c" stroke-width="3"/>
      <circle cx="452" cy="84" r="8" fill="#fff" stroke="#0f7b6c" stroke-width="3"/>
      <text x="470" y="156" text-anchor="middle" fill="#0f7b6c">Y = (A + B)'</text>
    </svg>`
  },
  "gates-xor": {
    caption: "XOR adds an extra curve behind the OR shape and is 1 when inputs differ. XNOR adds a bubble and is 1 when inputs match.",
    svg: `<svg viewBox="0 0 640 170" role="img" aria-label="XOR and XNOR symbols">
      <rect width="640" height="170" fill="#f7f4ea"/>
      <text x="170" y="24" text-anchor="middle" font-weight="700">XOR</text>
      <path d="M70 46 Q100 80 70 114" fill="none" stroke="#1f5aa6" stroke-width="3"/>
      <path d="M90 46 Q150 46 150 80 Q150 114 90 114 Q124 80 90 46 Z" fill="#e7eef8" stroke="#1f5aa6" stroke-width="3"/>
      <text x="150" y="150" text-anchor="middle" fill="#1f5aa6">Y = A ⊕ B</text>
      <text x="470" y="24" text-anchor="middle" font-weight="700">XNOR</text>
      <path d="M370 46 Q400 80 370 114" fill="none" stroke="#0f7b6c" stroke-width="3"/>
      <path d="M390 46 Q450 46 450 80 Q450 114 390 114 Q424 80 390 46 Z" fill="#e7f6f2" stroke="#0f7b6c" stroke-width="3"/>
      <circle cx="464" cy="80" r="8" fill="#fff" stroke="#0f7b6c" stroke-width="3"/>
      <text x="470" y="150" text-anchor="middle" fill="#0f7b6c">Y = (A ⊕ B)'</text>
    </svg>`
  },
  "logic-circuit": {
    caption: "The last operation sits next to Y. For Y = A·B + C, AND is on the left and OR is on the right.",
    svg: `<svg viewBox="0 0 640 200" role="img" aria-label="Logic diagram of Y equals A and B or C">
      <rect width="640" height="200" fill="#f7f4ea"/>
      <text x="40" y="70">A</text><text x="40" y="110">B</text><text x="40" y="160">C</text>
      <path d="M90 50 H120 C150 50 150 120 120 120 H90 Z" fill="#e7eef8" stroke="#1f5aa6" stroke-width="3"/>
      <line x1="55" y1="66" x2="90" y2="66" stroke="#1b212f"/><line x1="55" y1="104" x2="90" y2="104" stroke="#1b212f"/>
      <text x="160" y="78" font-size="13" fill="#1f5aa6">A·B</text>
      <path d="M230 70 Q280 70 280 110 Q280 160 230 160 Q262 115 230 70 Z" fill="#e7f6f2" stroke="#0f7b6c" stroke-width="3"/>
      <line x1="150" y1="85" x2="248" y2="95" stroke="#1b212f"/>
      <line x1="55" y1="156" x2="248" y2="140" stroke="#1b212f"/>
      <line x1="280" y1="115" x2="340" y2="115" stroke="#1b212f"/>
      <text x="348" y="120" font-weight="700">Y = A·B + C</text>
      <text x="120" y="190" font-size="13" fill="#4a5467">1. AND first</text>
      <text x="250" y="190" font-size="13" fill="#4a5467">2. OR last, beside Y</text>
    </svg>`
  },
  "kmap": {
    caption: "Gray-code headings: 00, 01, 11, 10. A group of four is A'. The pair is BC. So F = A' + BC.",
    svg: `<svg viewBox="0 0 520 230" role="img" aria-label="3-variable Karnaugh map">
      <rect width="520" height="230" fill="#f7f4ea"/>
      <text x="20" y="48" font-size="14">A \\ BC</text>
      <text x="150" y="36" text-anchor="middle">00</text>
      <text x="250" y="36" text-anchor="middle">01</text>
      <text x="350" y="36" text-anchor="middle">11</text>
      <text x="450" y="36" text-anchor="middle">10</text>
      <text x="70" y="90" text-anchor="middle">0</text>
      <text x="70" y="160" text-anchor="middle">1</text>
      <g stroke="#1b212f" fill="#fff">
        <rect x="110" y="56" width="80" height="56"/><rect x="190" y="56" width="80" height="56"/>
        <rect x="270" y="56" width="80" height="56"/><rect x="350" y="56" width="80" height="56"/>
        <rect x="110" y="112" width="80" height="56"/><rect x="190" y="112" width="80" height="56"/>
        <rect x="270" y="112" width="80" height="56"/><rect x="350" y="112" width="80" height="56"/>
      </g>
      <rect x="112" y="58" width="316" height="52" fill="#d9e6f7" stroke="#1f5aa6" stroke-width="2"/>
      <rect x="272" y="114" width="76" height="52" fill="#f8e1b0" stroke="#8a5a00" stroke-width="2"/>
      <g font-size="18" font-weight="700" fill="#1b212f" text-anchor="middle">
        <text x="150" y="90">1</text><text x="230" y="90">1</text><text x="310" y="90">1</text><text x="390" y="90">1</text>
        <text x="150" y="146">0</text><text x="230" y="146">0</text><text x="310" y="146">1</text><text x="390" y="146">0</text>
      </g>
      <text x="260" y="210" text-anchor="middle" fill="#1f5aa6" font-weight="700">F = A' + BC</text>
    </svg>`
  },
  "sdlc": {
    caption: "Six SDLC phases run from requirements through maintenance. A mistake in requirements spreads into every later phase.",
    svg: `<svg viewBox="0 0 640 250" role="img" aria-label="SDLC cycle">
      <rect width="640" height="250" fill="#f7f4ea"/>
      <g font-size="13" font-weight="700" text-anchor="middle">
        <rect x="230" y="16" width="180" height="40" rx="8" fill="#1f5aa6"/><text x="320" y="41" fill="#fff">1. Requirements</text>
        <rect x="450" y="70" width="160" height="40" rx="8" fill="#1f5aa6"/><text x="530" y="95" fill="#fff">2. Design</text>
        <rect x="450" y="150" width="160" height="40" rx="8" fill="#0f7b6c"/><text x="530" y="175" fill="#fff">3. Implementation</text>
        <rect x="230" y="196" width="180" height="40" rx="8" fill="#8a5a00"/><text x="320" y="221" fill="#fff">4. Testing</text>
        <rect x="30" y="150" width="160" height="40" rx="8" fill="#5b3cc4"/><text x="110" y="175" fill="#fff">5. Deployment</text>
        <rect x="30" y="70" width="160" height="40" rx="8" fill="#9b1c1c"/><text x="110" y="95" fill="#fff">6. Maintenance</text>
      </g>
      <path d="M410 36 H450 M530 110 V150 M450 216 H410 M190 170 H230 M110 150 V110 M190 90 H230" fill="none" stroke="#1b212f" stroke-width="2" marker-end="url(#arrow)"/>
    </svg>`
  },
  "waterfall": {
    caption: "Waterfall finishes one phase completely before the next begins. You do not swim back upstream.",
    svg: `<svg viewBox="0 0 640 200" role="img" aria-label="Waterfall steps">
      <rect width="640" height="200" fill="#f7f4ea"/>
      <g font-size="13" font-weight="700">
        <rect x="20" y="20" width="150" height="36" fill="#1f5aa6"/><text x="30" y="43" fill="#fff">Requirements</text>
        <rect x="120" y="62" width="150" height="36" fill="#2d6cb8"/><text x="150" y="85" fill="#fff">Design</text>
        <rect x="220" y="104" width="170" height="36" fill="#0f7b6c"/><text x="236" y="127" fill="#fff">Implementation</text>
        <rect x="330" y="146" width="130" height="36" fill="#8a5a00"/><text x="358" y="169" fill="#fff">Testing</text>
        <rect x="470" y="146" width="150" height="36" fill="#5b3cc4"/><text x="486" y="169" fill="#fff">Deploy + maintain</text>
      </g>
    </svg>`
  },
  "agile": {
    caption: "Agile repeats a short cycle: plan, build a working slice, test with the user, then plan the next slice.",
    svg: `<svg viewBox="0 0 640 180" role="img" aria-label="Agile iterations">
      <rect width="640" height="180" fill="#f7f4ea"/>
      <g fill="none" stroke="#1f5aa6" stroke-width="3">
        <ellipse cx="120" cy="90" rx="70" ry="46"/>
        <ellipse cx="320" cy="90" rx="80" ry="52"/>
        <ellipse cx="520" cy="90" rx="90" ry="58"/>
      </g>
      <g text-anchor="middle" font-size="14" font-weight="700" fill="#1b212f">
        <text x="120" y="94">Sprint 1</text>
        <text x="320" y="94">Sprint 2</text>
        <text x="520" y="94">Sprint 3</text>
      </g>
      <text x="320" y="168" text-anchor="middle" fill="#4a5467">Each loop delivers working software</text>
    </svg>`
  },
  "osi": {
    caption: "OSI has 7 layers. TCP/IP groups them into 4. Please Do Not Throw Sausage Pizza Away — from Physical up to Application.",
    svg: `<svg viewBox="0 0 640 280" role="img" aria-label="OSI seven layers beside TCP IP four layers">
      <rect width="640" height="280" fill="#f7f4ea"/>
      <text x="150" y="24" text-anchor="middle" font-weight="700">OSI (7)</text>
      <text x="470" y="24" text-anchor="middle" font-weight="700">TCP/IP (4)</text>
      ${["Application", "Presentation", "Session", "Transport", "Network", "Data link", "Physical"].map((name, i) => {
        const y = 36 + i * 32;
        return `<rect x="40" y="${y}" width="220" height="28" rx="4" fill="${i < 3 ? "#1f5aa6" : i === 3 ? "#0f7b6c" : i === 4 ? "#8a5a00" : "#5b3cc4"}"/><text x="150" y="${y + 19}" text-anchor="middle" fill="#fff" font-size="13">${7 - i}. ${name}</text>`;
      }).join("")}
      ${["Application", "Transport", "Internet", "Network access"].map((name, i) => {
        const h = i === 0 ? 92 : 32;
        const y = [36, 132, 168, 204][i];
        return `<rect x="360" y="${y}" width="230" height="${h}" rx="4" fill="${["#1f5aa6", "#0f7b6c", "#8a5a00", "#5b3cc4"][i]}"/><text x="475" y="${y + h / 2 + 4}" text-anchor="middle" fill="#fff" font-size="14">${name}</text>`;
      }).join("")}
    </svg>`
  },
  "ct-pillars": {
    caption: "Computational thinking stands on four pillars: decomposition, pattern recognition, abstraction, and algorithms.",
    svg: `<svg viewBox="0 0 640 160" role="img" aria-label="Four pillars of computational thinking">
      <rect width="640" height="160" fill="#f7f4ea"/>
      <rect x="30" y="28" width="580" height="28" rx="6" fill="#1b212f"/>
      <text x="320" y="47" text-anchor="middle" fill="#fff" font-weight="700">Computational thinking</text>
      ${["Decomposition", "Patterns", "Abstraction", "Algorithm"].map((name, i) => `<rect x="${40 + i * 150}" y="70" width="130" height="64" rx="6" fill="#1f5aa6"/><text x="${105 + i * 150}" y="107" text-anchor="middle" fill="#fff" font-size="13">${name}</text>`).join("")}
    </svg>`
  },
  "algorithm-steps": {
    caption: "An algorithm is a finite, ordered, unambiguous list of steps with a start and a stop.",
    svg: `<svg viewBox="0 0 280 250" role="img" aria-label="Algorithm flowchart">
      <rect width="280" height="250" fill="#f7f4ea"/>
      <ellipse cx="140" cy="28" rx="54" ry="16" fill="#1f5aa6"/><text x="140" y="33" text-anchor="middle" fill="#fff" font-size="13">Start</text>
      <rect x="70" y="64" width="140" height="36" rx="6" fill="#e7eef8" stroke="#1f5aa6"/><text x="140" y="86" text-anchor="middle" font-size="13">Step</text>
      <polygon points="140,114 200,150 140,186 80,150" fill="#fff6e0" stroke="#8a5a00"/><text x="140" y="154" text-anchor="middle" font-size="13">Decision?</text>
      <ellipse cx="140" cy="220" rx="54" ry="16" fill="#0f7b6c"/><text x="140" y="225" text-anchor="middle" fill="#fff" font-size="13">Stop</text>
      <path d="M140 44 V64 M140 100 V114 M140 186 V204" stroke="#1b212f" fill="none"/>
    </svg>`
  },
  "bubble-sort": {
    caption: "Bubble sort compares neighbours and swaps them if they are out of order. The largest value bubbles to the end.",
    svg: `<svg viewBox="0 0 640 160" role="img" aria-label="Bubble sort swap">
      <rect width="640" height="160" fill="#f7f4ea"/>
      ${[40, 70, 50, 90].map((h, i) => `<rect x="${40 + i * 70}" y="${130 - h}" width="48" height="${h}" fill="${i === 2 || i === 3 ? "#f8e1b0" : "#1f5aa6"}"/><text x="${64 + i * 70}" y="148" text-anchor="middle">${[3, 5, 4, 8][i]}</text>`).join("")}
      <path d="M200 40 H250" stroke="#b42317" stroke-width="2" marker-end="url(#arrow)"/>
      <text x="210" y="32" fill="#b42317" font-size="13">swap 5 and 4</text>
      <text x="400" y="80" font-size="14">After the pass the 8 is home.</text>
    </svg>`
  },
  "selection-sort": {
    caption: "Selection sort finds the minimum of the unsorted part and swaps it into the next front slot.",
    svg: `<svg viewBox="0 0 640 150" role="img" aria-label="Selection sort">
      <rect width="640" height="150" fill="#f7f4ea"/>
      ${[8, 3, 6, 2].map((n, i) => `<rect x="${30 + i * 80}" y="40" width="64" height="48" rx="6" fill="${i === 0 ? "#cfe8df" : i === 3 ? "#f8e1b0" : "#e7eef8"}" stroke="#1b212f"/><text x="${62 + i * 80}" y="70" text-anchor="middle" font-size="18">${n}</text>`).join("")}
      <text x="360" y="120" font-size="14">Sorted | unsorted. Minimum of the rest is 2.</text>
    </svg>`
  },
  "search": {
    caption: "Linear search checks every item. Binary search halves a sorted list each time.",
    svg: `<svg viewBox="0 0 640 170" role="img" aria-label="Linear and binary search">
      <rect width="640" height="170" fill="#f7f4ea"/>
      <text x="20" y="28" font-weight="700">Linear</text>
      ${[2, 5, 7, 9, 11].map((n, i) => `<rect x="${20 + i * 48}" y="44" width="42" height="36" fill="${i < 3 ? "#d9e6f7" : "#fff"}" stroke="#1f5aa6"/><text x="${41 + i * 48}" y="68" text-anchor="middle">${n}</text>`).join("")}
      <text x="20" y="110" font-size="13" fill="#4a5467">check, check, check…</text>
      <text x="330" y="28" font-weight="700">Binary (sorted)</text>
      ${[2, 5, 7, 9, 11, 14, 18].map((n, i) => `<rect x="${330 + i * 40}" y="44" width="36" height="36" fill="${i === 3 ? "#f8e1b0" : "#fff"}" stroke="#0f7b6c"/><text x="${348 + i * 40}" y="68" text-anchor="middle">${n}</text>`).join("")}
      <text x="330" y="110" font-size="13" fill="#4a5467">mid = 9, then go left or right</text>
    </svg>`
  },
  "lang-levels": {
    caption: "High-level languages (Python) sit far from the machine. Assembly and machine code sit close to it.",
    svg: `<svg viewBox="0 0 420 200" role="img" aria-label="Language level pyramid">
      <rect width="420" height="200" fill="#f7f4ea"/>
      <polygon points="210,24 300,80 120,80" fill="#1f5aa6"/><text x="210" y="68" text-anchor="middle" fill="#fff" font-size="13">High-level</text>
      <polygon points="120,86 300,86 340,132 80,132" fill="#0f7b6c"/><text x="210" y="116" text-anchor="middle" fill="#fff" font-size="13">Assembly</text>
      <polygon points="80,138 340,138 380,184 40,184" fill="#1b212f"/><text x="210" y="168" text-anchor="middle" fill="#fff" font-size="13">Machine code</text>
    </svg>`
  },
  "variables": {
    caption: "A variable is a named box in memory. The name stays; the value can change.",
    svg: `<svg viewBox="0 0 640 140" role="img" aria-label="Variable boxes">
      <rect width="640" height="140" fill="#f7f4ea"/>
      ${[["marks", "85", "int"], ["name", "Ayesha", "str"], ["passed", "True", "bool"]].map((row, i) => `<rect x="${30 + i * 200}" y="36" width="160" height="64" rx="8" fill="#fff" stroke="#1f5aa6" stroke-width="2"/><text x="${40 + i * 200}" y="58" font-size="13" fill="#4a5467">${row[0]} : ${row[2]}</text><text x="${40 + i * 200}" y="82" font-size="18" font-weight="700">${row[1]}</text>`).join("")}
    </svg>`
  },
  "ifelse": {
    caption: "if / else asks one question and takes exactly one branch.",
    svg: `<svg viewBox="0 0 420 210" role="img" aria-label="if else flowchart">
      <rect width="420" height="210" fill="#f7f4ea"/>
      <polygon points="210,20 300,70 210,120 120,70" fill="#fff6e0" stroke="#8a5a00" stroke-width="2"/>
      <text x="210" y="74" text-anchor="middle" font-size="13">marks ≥ 40?</text>
      <rect x="40" y="150" width="120" height="36" rx="6" fill="#cfe8df" stroke="#0f7b6c"/>
      <text x="100" y="173" text-anchor="middle" font-size="13">Pass</text>
      <rect x="260" y="150" width="120" height="36" rx="6" fill="#f8d0d0" stroke="#9b1c1c"/>
      <text x="320" y="173" text-anchor="middle" font-size="13">Fail</text>
      <path d="M160 100 L100 150 M260 100 L320 150" stroke="#1b212f" fill="none"/>
      <text x="120" y="130" font-size="12" fill="#0f7b6c">yes</text>
      <text x="270" y="130" font-size="12" fill="#9b1c1c">no</text>
    </svg>`
  },
  "loops": {
    caption: "for walks a known range. while repeats as long as its condition stays true. break leaves; continue skips to the next round.",
    svg: `<svg viewBox="0 0 640 180" role="img" aria-label="for and while loops">
      <rect width="640" height="180" fill="#f7f4ea"/>
      <rect x="30" y="40" width="250" height="100" rx="10" fill="#e7eef8" stroke="#1f5aa6"/>
      <text x="150" y="70" text-anchor="middle" font-weight="700">for i in range(n)</text>
      <text x="150" y="98" text-anchor="middle" font-size="13">known count · 0 … n-1</text>
      <rect x="340" y="40" width="270" height="100" rx="10" fill="#fff6e0" stroke="#8a5a00"/>
      <text x="475" y="70" text-anchor="middle" font-weight="700">while condition</text>
      <text x="475" y="98" text-anchor="middle" font-size="13">repeat until the test fails</text>
    </svg>`
  },
  "debug": {
    caption: "Debugging cycle: reproduce the bug, find the line, fix one thing, test again.",
    svg: `<svg viewBox="0 0 640 150" role="img" aria-label="Debugging cycle">
      <rect width="640" height="150" fill="#f7f4ea"/>
      ${["Reproduce", "Locate", "Fix", "Test"].map((name, i) => `<rect x="${30 + i * 155}" y="40" width="130" height="48" rx="8" fill="#1f5aa6"/><text x="${95 + i * 155}" y="69" text-anchor="middle" fill="#fff">${i + 1}. ${name}</text>`).join("")}
      <path d="M160 64 H185 M315 64 H340 M470 64 H495" stroke="#8a5a00" stroke-width="2" fill="none"/>
    </svg>`
  },
  "keys-table": {
    caption: "Primary key identifies one row. Foreign key points at a primary key in another table.",
    svg: `<svg viewBox="0 0 640 170" role="img" aria-label="Primary and foreign keys">
      <rect width="640" height="170" fill="#f7f4ea"/>
      <text x="40" y="28" font-weight="700">Students</text>
      <rect x="40" y="40" width="220" height="28" fill="#1f5aa6"/><text x="50" y="59" fill="#fff" font-size="13">student_id PK | name</text>
      <rect x="40" y="68" width="220" height="28" fill="#fff" stroke="#1f5aa6"/><text x="50" y="87" font-size="13">S1 | Ayesha</text>
      <text x="360" y="28" font-weight="700">Marks</text>
      <rect x="360" y="40" width="240" height="28" fill="#0f7b6c"/><text x="370" y="59" fill="#fff" font-size="13">mark_id PK | student_id FK</text>
      <rect x="360" y="68" width="240" height="28" fill="#fff" stroke="#0f7b6c"/><text x="370" y="87" font-size="13">M9 | S1</text>
      <path d="M260 82 H360" stroke="#8a5a00" stroke-width="2" fill="none"/>
      <text x="40" y="140" font-size="13" fill="#4a5467">FK student_id must already exist in Students.</text>
    </svg>`
  },
  "er": {
    caption: "Rectangles are entities, diamonds are relationships, ovals are attributes. Cardinality says how many.",
    svg: `<svg viewBox="0 0 640 180" role="img" aria-label="Entity relationship diagram">
      <rect width="640" height="180" fill="#f7f4ea"/>
      <rect x="30" y="60" width="140" height="48" fill="#e7eef8" stroke="#1f5aa6" stroke-width="2"/>
      <text x="100" y="89" text-anchor="middle">STUDENT</text>
      <polygon points="250,84 320,50 390,84 320,118" fill="#fff6e0" stroke="#8a5a00" stroke-width="2"/>
      <text x="320" y="89" text-anchor="middle" font-size="13">ENROLS</text>
      <rect x="450" y="60" width="150" height="48" fill="#e7f6f2" stroke="#0f7b6c" stroke-width="2"/>
      <text x="525" y="89" text-anchor="middle">COURSE</text>
      <line x1="170" y1="84" x2="250" y2="84" stroke="#1b212f"/>
      <line x1="390" y1="84" x2="450" y2="84" stroke="#1b212f"/>
      <text x="190" y="74" font-size="12">N</text><text x="420" y="74" font-size="12">M</text>
      <ellipse cx="100" cy="146" rx="46" ry="16" fill="#fff" stroke="#1f5aa6"/><text x="100" y="150" text-anchor="middle" font-size="12">name</text>
    </svg>`
  },
  "access": {
    caption: "MS Access: a table stores rows, a form edits one record, a query filters rows, a chart shows the result.",
    svg: `<svg viewBox="0 0 640 150" role="img" aria-label="Access objects">
      <rect width="640" height="150" fill="#f7f4ea"/>
      ${["Table", "Form", "Query", "Chart"].map((name, i) => `<rect x="${24 + i * 155}" y="36" width="140" height="70" rx="8" fill="#fff" stroke="#1f5aa6" stroke-width="2"/><text x="${94 + i * 155}" y="78" text-anchor="middle" font-weight="700">${name}</text>`).join("")}
    </svg>`
  },
  "ai-iot": {
    caption: "AI decides, IoT senses and connects things, data analytics looks for patterns in what was collected.",
    svg: `<svg viewBox="0 0 640 170" role="img" aria-label="AI IoT and analytics">
      <rect width="640" height="170" fill="#f7f4ea"/>
      ${[["AI", "learn / decide", "#1f5aa6"], ["IoT", "sense / connect", "#0f7b6c"], ["Analytics", "find patterns", "#8a5a00"]].map((row, i) => `<circle cx="${120 + i * 200}" cy="70" r="46" fill="${row[2]}"/><text x="${120 + i * 200}" y="66" text-anchor="middle" fill="#fff" font-weight="700">${row[0]}</text><text x="${120 + i * 200}" y="84" text-anchor="middle" fill="#fff" font-size="11">${row[1]}</text>`).join("")}
    </svg>`
  },
  "assistive": {
    caption: "Assistive technology removes a barrier: screen readers, captions, alternate input, and high contrast.",
    svg: `<svg viewBox="0 0 640 140" role="img" aria-label="Assistive technologies">
      <rect width="640" height="140" fill="#f7f4ea"/>
      ${["Screen reader", "Captions", "Switch / key", "Contrast"].map((name, i) => `<rect x="${20 + i * 155}" y="40" width="140" height="56" rx="8" fill="#e7eef8" stroke="#1f5aa6"/><text x="${90 + i * 155}" y="73" text-anchor="middle" font-size="13">${name}</text>`).join("")}
    </svg>`
  },
  "data-types": {
    caption: "Qualitative data is categories (colour, opinion). Quantitative data is numbers (marks, age).",
    svg: `<svg viewBox="0 0 640 150" role="img" aria-label="Qualitative and quantitative data">
      <rect width="640" height="150" fill="#f7f4ea"/>
      <rect x="30" y="30" width="270" height="90" rx="8" fill="#fff6e0" stroke="#8a5a00"/>
      <text x="165" y="62" text-anchor="middle" font-weight="700">Qualitative</text>
      <text x="165" y="88" text-anchor="middle" font-size="13">red, agree, city</text>
      <rect x="340" y="30" width="270" height="90" rx="8" fill="#e7eef8" stroke="#1f5aa6"/>
      <text x="475" y="62" text-anchor="middle" font-weight="700">Quantitative</text>
      <text x="475" y="88" text-anchor="middle" font-size="13">85, 16 years, 3.2 kg</text>
    </svg>`
  },
  "inquiry": {
    caption: "Digital inquiry moves from a question, to a search, to evidence, to a conclusion you can show.",
    svg: `<svg viewBox="0 0 680 120" role="img" aria-label="Inquiry steps">
      <rect width="680" height="120" fill="#f7f4ea"/>
      ${["Question", "Search", "Sources", "Evidence", "Analyse", "Share"].map((name, i) => `<circle cx="${50 + i * 108}" cy="48" r="22" fill="#1f5aa6"/><text x="${50 + i * 108}" y="53" text-anchor="middle" fill="#fff" font-size="13">${i + 1}</text><text x="${50 + i * 108}" y="92" text-anchor="middle" font-size="12">${name}</text>`).join("")}
    </svg>`
  },
  "hci-senses": {
    caption: "HCI designs the meeting point of a person and a system: what they see, hear, touch, and how they move.",
    svg: `<svg viewBox="0 0 640 210" role="img" aria-label="Human computer interaction senses">
      <rect width="640" height="210" fill="#f7f4ea"/>
      <circle cx="320" cy="108" r="36" fill="#1f5aa6"/>
      <text x="320" y="113" text-anchor="middle" fill="#fff" font-weight="700">Human</text>
      ${[["Sight", "screen"], ["Hearing", "sound"], ["Touch", "tap"], ["Motion", "gesture"]].map((row, i) => {
        const pos = [[320, 36], [500, 108], [320, 180], [140, 108]][i];
        return `<rect x="${pos[0] - 58}" y="${pos[1] - 18}" width="116" height="36" rx="8" fill="#fff" stroke="#0f7b6c"/><text x="${pos[0]}" y="${pos[1] + 4}" text-anchor="middle" font-size="13">${row[0]} · ${row[1]}</text>`;
      }).join("")}
    </svg>`
  },
  "ui-ux": {
    caption: "UI is what you see and tap. UX is how the whole task feels, including speed, trust, and mistakes.",
    svg: `<svg viewBox="0 0 640 160" role="img" aria-label="UI versus UX">
      <rect width="640" height="160" fill="#f7f4ea"/>
      <rect x="30" y="24" width="270" height="112" rx="10" fill="#e7eef8" stroke="#1f5aa6"/>
      <text x="165" y="52" text-anchor="middle" font-weight="700">UI</text>
      <text x="165" y="80" text-anchor="middle" font-size="13">buttons, colour, layout</text>
      <text x="165" y="104" text-anchor="middle" font-size="13">what is on the screen</text>
      <rect x="340" y="24" width="270" height="112" rx="10" fill="#fff6e0" stroke="#8a5a00"/>
      <text x="475" y="52" text-anchor="middle" font-weight="700">UX</text>
      <text x="475" y="80" text-anchor="middle" font-size="13">can I finish the task?</text>
      <text x="475" y="104" text-anchor="middle" font-size="13">time, errors, trust</text>
    </svg>`
  },
  "wireframe": {
    caption: "A wireframe is a low-detail sketch of screens: boxes for content, not colours or final text.",
    svg: `<svg viewBox="0 0 280 220" role="img" aria-label="Phone wireframe">
      <rect width="280" height="220" fill="#f7f4ea"/>
      <rect x="80" y="16" width="120" height="188" rx="16" fill="#fff" stroke="#1b212f" stroke-width="3"/>
      <rect x="96" y="36" width="88" height="16" fill="#d9e6f7"/>
      <rect x="96" y="62" width="88" height="48" fill="#e7eef8" stroke="#1f5aa6"/>
      <rect x="96" y="118" width="40" height="18" fill="#f8e1b0"/>
      <rect x="142" y="118" width="42" height="18" fill="#f8e1b0"/>
      <rect x="96" y="146" width="88" height="28" rx="6" fill="#1f5aa6"/>
      <text x="140" y="164" text-anchor="middle" fill="#fff" font-size="12">Button</text>
    </svg>`
  },
  "trace": {
    caption: "A trace table has one row per step and one column per variable. It shows the value after that line runs.",
    svg: `<svg viewBox="0 0 520 160" role="img" aria-label="Trace table">
      <rect width="520" height="160" fill="#f7f4ea"/>
      <g font-size="14">
        <rect x="40" y="24" width="80" height="28" fill="#1b212f"/><text x="80" y="43" text-anchor="middle" fill="#fff">line</text>
        <rect x="120" y="24" width="80" height="28" fill="#1b212f"/><text x="160" y="43" text-anchor="middle" fill="#fff">n</text>
        <rect x="200" y="24" width="80" height="28" fill="#1b212f"/><text x="240" y="43" text-anchor="middle" fill="#fff">s</text>
        ${[["1", "3", "0"], ["2", "3", "3"], ["3", "2", "5"]].map((row, r) => row.map((cell, c) => `<rect x="${40 + c * 80}" y="${52 + r * 28}" width="80" height="28" fill="#fff" stroke="#1f5aa6"/><text x="${80 + c * 80}" y="${71 + r * 28}" text-anchor="middle">${cell}</text>`).join("")).join("")}
      </g>
    </svg>`
  },
  "bigo": {
    caption: "As n grows, O(1) stays flat, O(log n) rises slowly, O(n) is a straight line, and O(n²) curves up steeply.",
    svg: `<svg viewBox="0 0 640 240" role="img" aria-label="Big O growth curves">
      <rect width="640" height="240" fill="#f7f4ea"/>
      <line x1="70" y1="30" x2="70" y2="190" stroke="#1b212f"/>
      <line x1="70" y1="190" x2="420" y2="190" stroke="#1b212f"/>
      <text x="50" y="28" font-size="12">time</text>
      <text x="424" y="194" font-size="12">n</text>
      <line x1="70" y1="150" x2="400" y2="150" stroke="#0f7b6c" stroke-width="3"/>
      <path d="M70 170 Q220 168 400 120" fill="none" stroke="#1f5aa6" stroke-width="3"/>
      <line x1="70" y1="180" x2="400" y2="50" stroke="#8a5a00" stroke-width="3"/>
      <path d="M70 184 Q200 180 280 120 Q340 60 390 36" fill="none" stroke="#9b1c1c" stroke-width="3"/>
      <g font-size="13">
        <text x="450" y="70" fill="#9b1c1c">O(n²)</text>
        <text x="450" y="100" fill="#8a5a00">O(n)</text>
        <text x="450" y="130" fill="#1f5aa6">O(log n)</text>
        <text x="450" y="160" fill="#0f7b6c">O(1)</text>
      </g>
    </svg>`
  },
  "array": {
    caption: "An array stores items in order. The index starts at 0 and reaches any slot in one step.",
    svg: `<svg viewBox="0 0 640 130" role="img" aria-label="Array with indexes">
      <rect width="640" height="130" fill="#f7f4ea"/>
      ${["Ali", "Bea", "Cem", "Dua"].map((name, i) => `<rect x="${40 + i * 110}" y="36" width="100" height="48" fill="${i === 2 ? "#f8e1b0" : "#e7eef8"}" stroke="#1f5aa6" stroke-width="2"/><text x="${90 + i * 110}" y="66" text-anchor="middle" font-weight="700">${name}</text><text x="${90 + i * 110}" y="108" text-anchor="middle" font-size="13" fill="#4a5467">[${i}]</text>`).join("")}
    </svg>`
  },
  "structures": {
    caption: "A linked list points to the next node. A tree has one parent and many children. A graph can connect anything to anything.",
    svg: `<svg viewBox="0 0 640 200" role="img" aria-label="Linked list tree and graph">
      <rect width="640" height="200" fill="#f7f4ea"/>
      <text x="20" y="22" font-size="13" font-weight="700">List</text>
      <rect x="20" y="36" width="54" height="32" fill="#e7eef8" stroke="#1f5aa6"/><text x="47" y="57" text-anchor="middle">A</text>
      <rect x="90" y="36" width="54" height="32" fill="#e7eef8" stroke="#1f5aa6"/><text x="117" y="57" text-anchor="middle">B</text>
      <rect x="160" y="36" width="54" height="32" fill="#e7eef8" stroke="#1f5aa6"/><text x="187" y="57" text-anchor="middle">C</text>
      <path d="M74 52 H90 M144 52 H160" stroke="#1b212f"/>
      <text x="250" y="22" font-size="13" font-weight="700">Tree</text>
      <circle cx="330" cy="48" r="16" fill="#fff6e0" stroke="#8a5a00"/><text x="330" y="52" text-anchor="middle">R</text>
      <circle cx="290" cy="100" r="16" fill="#fff" stroke="#8a5a00"/><circle cx="370" cy="100" r="16" fill="#fff" stroke="#8a5a00"/>
      <path d="M318 62 L298 84 M342 62 L362 84" stroke="#8a5a00"/>
      <text x="450" y="22" font-size="13" font-weight="700">Graph</text>
      <circle cx="500" cy="70" r="14" fill="#e7f6f2" stroke="#0f7b6c"/>
      <circle cx="560" cy="46" r="14" fill="#e7f6f2" stroke="#0f7b6c"/>
      <circle cx="560" cy="110" r="14" fill="#e7f6f2" stroke="#0f7b6c"/>
      <path d="M514 66 L546 52 M514 78 L546 104 M546 60 V96" stroke="#0f7b6c"/>
    </svg>`
  },
  "stack-queue": {
    caption: "Stack is LIFO: last in, first out, at the top. Queue is FIFO: first in, first out, at the front.",
    svg: `<svg viewBox="0 0 640 200" role="img" aria-label="Stack and queue">
      <rect width="640" height="200" fill="#f7f4ea"/>
      <text x="80" y="24" font-weight="700">Stack (LIFO)</text>
      ${["C top", "B", "A"].map((name, i) => `<rect x="70" y="${40 + i * 36}" width="120" height="32" fill="${i === 0 ? "#f8e1b0" : "#e7eef8"}" stroke="#1f5aa6"/><text x="130" y="${61 + i * 36}" text-anchor="middle">${name}</text>`).join("")}
      <text x="210" y="70" font-size="13">push / pop here</text>
      <text x="430" y="24" font-weight="700">Queue (FIFO)</text>
      ${["front A", "B", "C rear"].map((name, i) => `<rect x="${360 + i * 80}" y="80" width="74" height="40" fill="${i === 0 ? "#cfe8df" : "#fff6e0"}" stroke="#0f7b6c"/><text x="${397 + i * 80}" y="105" text-anchor="middle" font-size="12">${name}</text>`).join("")}
      <text x="360" y="150" font-size="13">dequeue ←    → enqueue</text>
    </svg>`
  },
  "py-collections": {
    caption: "List is ordered and mutable. Tuple is ordered and fixed. Set is unique and unordered. Dict maps a key to a value.",
    svg: `<svg viewBox="0 0 640 150" role="img" aria-label="Python collections">
      <rect width="640" height="150" fill="#f7f4ea"/>
      ${[["list", "[1, 2, 2]", "#1f5aa6"], ["tuple", "(1, 2)", "#0f7b6c"], ["set", "{1, 2}", "#8a5a00"], ["dict", "{'a': 1}", "#5b3cc4"]].map((row, i) => `<rect x="${16 + i * 156}" y="28" width="146" height="96" rx="8" fill="#fff" stroke="${row[2]}" stroke-width="3"/><text x="${89 + i * 156}" y="58" text-anchor="middle" font-weight="700" fill="${row[2]}">${row[0]}</text><text x="${89 + i * 156}" y="90" text-anchor="middle" font-size="14">${row[1]}</text>`).join("")}
    </svg>`
  },
  "files": {
    caption: "Open a file in a mode, use it, then close it. r reads, w overwrites, a adds to the end.",
    svg: `<svg viewBox="0 0 640 140" role="img" aria-label="File modes">
      <rect width="640" height="140" fill="#f7f4ea"/>
      ${[["r", "read"], ["w", "overwrite"], ["a", "append"], ["x", "create new"]].map((row, i) => `<rect x="${24 + i * 155}" y="36" width="140" height="68" rx="8" fill="#e7eef8" stroke="#1f5aa6"/><text x="${94 + i * 155}" y="66" text-anchor="middle" font-size="22" font-weight="700">${row[0]}</text><text x="${94 + i * 155}" y="88" text-anchor="middle" font-size="13">${row[1]}</text>`).join("")}
    </svg>`
  },
  "exceptions": {
    caption: "try runs the risky lines. except handles a named error. finally runs either way.",
    svg: `<svg viewBox="0 0 640 150" role="img" aria-label="try except finally">
      <rect width="640" height="150" fill="#f7f4ea"/>
      <rect x="30" y="40" width="150" height="60" rx="8" fill="#e7eef8" stroke="#1f5aa6"/><text x="105" y="75" text-anchor="middle" font-weight="700">try</text>
      <rect x="240" y="24" width="160" height="44" rx="8" fill="#f8d0d0" stroke="#9b1c1c"/><text x="320" y="51" text-anchor="middle">except Error</text>
      <rect x="240" y="84" width="160" height="44" rx="8" fill="#cfe8df" stroke="#0f7b6c"/><text x="320" y="111" text-anchor="middle">else / continue</text>
      <rect x="450" y="40" width="160" height="60" rx="8" fill="#fff6e0" stroke="#8a5a00"/><text x="530" y="75" text-anchor="middle" font-weight="700">finally</text>
      <path d="M180 70 H240 M400 46 H450 M400 106 H450" stroke="#1b212f" fill="none"/>
    </svg>`
  },
  "pandas": {
    caption: "A DataFrame is a labelled table. Rows can come from SQLite, and missing numbers show up as NaN.",
    svg: `<svg viewBox="0 0 520 150" role="img" aria-label="Pandas dataframe">
      <rect width="520" height="150" fill="#f7f4ea"/>
      <g font-size="14">
        <rect x="40" y="24" width="120" height="28" fill="#1b212f"/><text x="100" y="43" text-anchor="middle" fill="#fff">name</text>
        <rect x="160" y="24" width="120" height="28" fill="#1b212f"/><text x="220" y="43" text-anchor="middle" fill="#fff">marks</text>
        <rect x="280" y="24" width="120" height="28" fill="#1b212f"/><text x="340" y="43" text-anchor="middle" fill="#fff">city</text>
        <rect x="40" y="52" width="120" height="28" fill="#fff" stroke="#1f5aa6"/><text x="100" y="71" text-anchor="middle">Ayesha</text>
        <rect x="160" y="52" width="120" height="28" fill="#fff" stroke="#1f5aa6"/><text x="220" y="71" text-anchor="middle">85</text>
        <rect x="280" y="52" width="120" height="28" fill="#fff" stroke="#1f5aa6"/><text x="340" y="71" text-anchor="middle">Karachi</text>
        <rect x="40" y="80" width="120" height="28" fill="#fff" stroke="#1f5aa6"/><text x="100" y="99" text-anchor="middle">Bilal</text>
        <rect x="160" y="80" width="120" height="28" fill="#f8d0d0" stroke="#9b1c1c"/><text x="220" y="99" text-anchor="middle">NaN</text>
        <rect x="280" y="80" width="120" height="28" fill="#fff" stroke="#1f5aa6"/><text x="340" y="99" text-anchor="middle">Lahore</text>
      </g>
    </svg>`
  },
  "stats": {
    caption: "Mean is the balance point. Median is the middle of the ordered list. Mode is the tallest bar.",
    svg: `<svg viewBox="0 0 640 180" role="img" aria-label="Mean median and mode">
      <rect width="640" height="180" fill="#f7f4ea"/>
      ${[40, 70, 70, 110, 50].map((h, i) => `<rect x="${40 + i * 50}" y="${140 - h}" width="36" height="${h}" fill="${i === 3 ? "#f8e1b0" : "#1f5aa6"}"/>`).join("")}
      <line x1="30" y1="78" x2="300" y2="78" stroke="#b42317" stroke-dasharray="4 3"/>
      <text x="250" y="70" fill="#b42317" font-size="13">mean</text>
      <text x="360" y="60" font-size="14">Ordered: 2, 4, 4, 7, 9</text>
      <text x="360" y="86" font-size="14">Median = 4 (middle)</text>
      <text x="360" y="112" font-size="14">Mode = 4 (most frequent)</text>
    </svg>`
  },
  "neural": {
    caption: "A neural net has an input layer, hidden layers, and an output. Deep learning means many hidden layers.",
    svg: `<svg viewBox="0 0 640 200" role="img" aria-label="Neural network layers">
      <rect width="640" height="200" fill="#f7f4ea"/>
      ${[[80, [50, 100, 150]], [240, [40, 80, 120, 160]], [400, [60, 110, 160]], [540, [100]]].map((col, ci) => col[1].map((y) => `<circle cx="${col[0]}" cy="${y}" r="12" fill="${["#1f5aa6", "#0f7b6c", "#8a5a00", "#9b1c1c"][ci]}"/>`).join("")).join("")}
      <text x="80" y="190" text-anchor="middle" font-size="12">input</text>
      <text x="320" y="190" text-anchor="middle" font-size="12">hidden</text>
      <text x="540" y="190" text-anchor="middle" font-size="12">output</text>
    </svg>`
  },
  "security": {
    caption: "Threats (malware, phishing, denial of service) are reduced by locks you control: updates, passwords, backups, and least privilege.",
    svg: `<svg viewBox="0 0 640 160" role="img" aria-label="Security threats and mitigation">
      <rect width="640" height="160" fill="#f7f4ea"/>
      <rect x="24" y="30" width="280" height="100" rx="8" fill="#f8d0d0" stroke="#9b1c1c"/>
      <text x="164" y="58" text-anchor="middle" font-weight="700">Threats</text>
      <text x="164" y="84" text-anchor="middle" font-size="13">malware · phishing · DoS</text>
      <rect x="336" y="30" width="280" height="100" rx="8" fill="#cfe8df" stroke="#0f7b6c"/>
      <text x="476" y="58" text-anchor="middle" font-weight="700">Mitigation</text>
      <text x="476" y="84" text-anchor="middle" font-size="13">update · MFA · backup</text>
    </svg>`
  },
  "mvp": {
    caption: "A prototype explores. An MVP is the smallest real product that tests the riskiest assumption with users.",
    svg: `<svg viewBox="0 0 640 160" role="img" aria-label="Prototype to MVP cycle">
      <rect width="640" height="160" fill="#f7f4ea"/>
      ${["Idea", "Prototype", "Test", "MVP"].map((name, i) => `<circle cx="${80 + i * 150}" cy="70" r="36" fill="${i === 3 ? "#1f5aa6" : "#fff"}" stroke="#1f5aa6" stroke-width="3"/><text x="${80 + i * 150}" y="75" text-anchor="middle" font-size="13" fill="${i === 3 ? "#fff" : "#1b212f"}" font-weight="700">${name}</text>`).join("")}
      <path d="M116 70 H154 M266 70 H304 M416 70 H454" stroke="#8a5a00" stroke-width="2" fill="none"/>
    </svg>`
  },
  "beachhead": {
    caption: "A beachhead is the first small market you can win completely, before you try to serve everyone.",
    svg: `<svg viewBox="0 0 320 200" role="img" aria-label="Beachhead market target">
      <rect width="320" height="200" fill="#f7f4ea"/>
      <circle cx="160" cy="100" r="78" fill="#e7eef8" stroke="#1f5aa6"/>
      <circle cx="160" cy="100" r="50" fill="#fff6e0" stroke="#8a5a00"/>
      <circle cx="160" cy="100" r="22" fill="#1f5aa6"/>
      <text x="160" y="104" text-anchor="middle" fill="#fff" font-size="11">first</text>
      <text x="160" y="192" text-anchor="middle" font-size="13">Win the centre before the whole map</text>
    </svg>`
  }
};
