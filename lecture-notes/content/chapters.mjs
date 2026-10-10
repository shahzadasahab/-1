/** Intermediate Computer Science — Teach Yourself lecture note content (XI & XII) */

const C = (strings, ...values) => String.raw({ raw: strings }, ...values);

export const chapters = [
  {
    grade: "XI",
    unit: 1,
    slug: "Computer-Systems",
    title: "Computer Systems",
    tagline: "Digital logic, SDLC, and networking foundations",
    outcomes: [
      "Differentiate analog vs digital representation and signals",
      "Use Boolean algebra, truth tables, and logic gates (including Logisim)",
      "Compare Waterfall and Agile SDLC with case studies",
      "Explain OSI and TCP/IP models and layer protocols",
    ],
    sections: [
      {
        title: "1.1 Discrete vs continuous & digital systems",
        html: `
<p><strong>Discrete</strong> quantities are countable (students in a class, books on a shelf).
<strong>Continuous</strong> quantities vary smoothly (temperature, height, time).</p>
<div class="two-col">
  <div class="card"><h3>Stairs = discrete</h3><p>Only fixed step heights — like binary 0/1 levels.</p></div>
  <div class="card"><h3>Ramp = continuous</h3><p>Any height in between — like analog voltage.</p></div>
</div>
<p>A <strong>digital system</strong> uses bits: $0$ (OFF/LOW/FALSE) and $1$ (ON/HIGH/TRUE). Digital systems resist noise, copy accurately, and integrate with software.</p>
${C`<div class="callout callout-remember"><div><strong>Remember</strong>Modern phones, calculators, and traffic lights are digital at their core.</div></div>`}`,
        diagram: "stairsRamp",
        diagramCaption: "Figure 1.1 — Discrete steps vs continuous slope (analog vs digital intuition).",
      },
      {
        title: "1.2 Analog vs digital signals",
        html: `
<p>A <strong>signal</strong> carries information. <strong>Analog</strong> signals vary continuously (voice, old radio). <strong>Digital</strong> signals switch between HIGH and LOW (computer data, USB, internet packets).</p>
<table class="data">
<tr><th>Feature</th><th>Analog</th><th>Digital</th></tr>
<tr><td>Values</td><td>Infinite in range</td><td>Two levels (0, 1)</td></tr>
<tr><td>Wave shape</td><td>Smooth (sine-like)</td><td>Square steps</td></tr>
<tr><td>Noise</td><td>Easily distorted</td><td>Easy to regenerate</td></tr>
<tr><td>Examples</td><td>Vinyl, mercury thermometer</td><td>PC, smartphone, digital watch</td></tr>
</table>`,
        diagram: "analogDigital",
        diagramCaption: "Figure 1.2 — Smooth analog wave vs two-level digital wave.",
      },
      {
        title: "1.3 Boolean algebra & operations",
        html: `
<p>Boolean algebra (George Boole) uses only $0$ and $1$. Variables $A,B,C$ hold binary values; expressions combine them with AND, OR, NOT.</p>
<p><strong>AND</strong> ($Y = A \\cdot B$): output $1$ only if <em>all</em> inputs are $1$. Truth table rows for $n$ inputs: $2^n$.</p>
<table class="data"><tr><th>A</th><th>B</th><th>$Y=A\\cdot B$</th></tr>
<tr><td>0</td><td>0</td><td>0</td></tr><tr><td>0</td><td>1</td><td>0</td></tr>
<tr><td>1</td><td>0</td><td>0</td></tr><tr><td>1</td><td>1</td><td>1</td></tr></table>
<p><strong>OR</strong> ($Y = A + B$): $1$ if <em>any</em> input is $1$. <strong>NOT</strong> ($Y = \\overline{A}$): flips the bit.</p>
<p><strong>XOR</strong> ($Y = A \\oplus B$): $1$ when inputs differ: $Y = A'B + AB'$.</p>
<p><strong>XNOR</strong>: $1$ when inputs are equal. <strong>NAND</strong> and <strong>NOR</strong> are <em>universal gates</em> — any circuit can be built from them alone.</p>
<div class="callout callout-exam"><div><strong>Exam tip</strong>For 3 inputs, list binary combinations from 000 to 111 in order when building truth tables.</div></div>`,
        diagram: "logicGates",
        diagramCaption: "Figure 1.3 — Standard logic gate symbols (exam drawing practice).",
      },
      {
        title: "1.4 Logisim & building circuits",
        html: `
<p>Use <strong>Logisim Evolution</strong> to place gates, input pins (square), output pins (circle), and orthogonal wires. Simulate all input combinations.</p>
<p><strong>Example:</strong> 2-input AND — $Y=1$ only when $A=1$ and $B=1$. Wire colors: bright green = 1, dark green = 0.</p>
<div class="callout callout-try"><div><strong>Try it</strong>Build XOR from AND, OR, and NOT. Verify with four test cases $(0,0)$ through $(1,1)$.</div></div>`,
      },
      {
        title: "1.5 Software Development Life Cycle (SDLC)",
        html: `
<p>SDLC is the structured path from idea to working software: requirements → design → coding → testing → deployment → maintenance.</p>
<p><strong>Waterfall</strong> — phases run sequentially; best when requirements are stable (e.g. school library system with fixed rules).</p>
<p><strong>Agile (Scrum)</strong> — short <em>sprints</em> (often 2 weeks), evolving product backlog, frequent demos. Fits mobile apps with changing stakeholder needs (timetable, attendance, notifications).</p>
<p>Agile artifacts: product backlog, user stories, sprint reviews, retrospectives.</p>`,
        diagram: "waterfall",
        diagramCaption: "Figure 1.4 — Waterfall: each phase completes before the next begins.",
      },
      {
        title: "1.6 OSI & TCP/IP",
        html: `
<p>The <strong>OSI model</strong> has 7 layers — a teaching map for network functions. Memorize top-to-bottom:</p>
<ol>
<li>Physical — bits on wire/fiber</li>
<li>Data Link — frames, MAC addresses</li>
<li>Network — routing, IP addresses</li>
<li>Transport — TCP/UDP, ports, reliability</li>
<li>Session — dialog control</li>
<li>Presentation — encoding, encryption</li>
<li>Application — HTTP, email, DNS to users</li>
</ol>
<p><strong>TCP/IP</strong> (4 layers) is what the real internet uses: Network Access, Internet, Transport, Application. TCP gives reliable delivery; UDP is faster but unreliable.</p>
<div class="callout callout-remember"><div><strong>Remember</strong>“All People Seem To Need Data Processing” — Application (7) down to Physical (1).</div></div>`,
        diagram: "osi",
        diagramCaption: "Figure 1.5 — OSI stack: each layer serves the layer above.",
      },
    ],
    practice: [
      "Draw truth tables for NAND, NOR, and 3-input AND.",
      "Simplify $Y = A(B + C)$ using Boolean laws and build in Logisim.",
      "List two reasons a school might choose Agile over Waterfall for a student app.",
      "Name one protocol or device at OSI layers 2, 3, and 7.",
    ],
  },
  {
    grade: "XI",
    unit: 2,
    slug: "Computational-Thinking-Algorithms",
    title: "Computational Thinking & Algorithms",
    tagline: "Problem decomposition, patterns, and classic sort/search",
    outcomes: [
      "Apply decomposition, pattern recognition, and abstraction",
      "Write algorithms and pseudocode for real problems",
      "Implement and trace bubble sort and selection sort (any two sorts)",
      "Apply linear and binary search (any two searches)",
    ],
    sections: [
      {
        title: "2.1 What is computational thinking?",
        html: `
<p><strong>Computational thinking</strong> is a disciplined way to solve problems: break them down, find patterns, hide irrelevant detail, and design step-by-step procedures (<strong>algorithms</strong>).</p>
<p>An <strong>algorithm</strong> is language-independent logic. <strong>Pseudocode</strong> is human-readable structure (IF, FOR, WHILE) that programmers translate into code.</p>`,
        diagram: "decomposition",
        diagramCaption: "Figure 2.1 — Decomposition turns one hard task into manageable subtasks.",
      },
      {
        title: "2.2 Algorithmic strategies",
        html: `
<div class="flex-grid">
  <div class="card"><h3>Decomposition</h3><p>Split complex jobs (e.g. learning a language: vocabulary, grammar, tenses, practice).</p></div>
  <div class="card"><h3>Pattern recognition</h3><p>Spot repetition — row $k$ has $k$ stars → use a loop with counter.</p></div>
  <div class="card"><h3>Abstraction</h3><p>Keep essential steps (boil water, steep tea); ignore cup color or kettle brand.</p></div>
</div>
<p>Good algorithms are <strong>clear</strong>, <strong>correct</strong>, <strong>efficient</strong> in time/memory, and <strong>reusable</strong>.</p>`,
      },
      {
        title: "2.3 Bubble sort",
        html: `
<p><strong>Bubble sort</strong> compares adjacent pairs and swaps if out of order; largest values “bubble” to the end each pass.</p>
<p>For $n$ items, worst-case passes relate to $O(n^2)$ comparisons — fine for small lists, slow for huge data.</p>
<pre>FOR outer = 0 TO n-2
  FOR inner = 0 TO n-2-outer
    IF list[inner] &gt; list[inner+1] THEN swap
  END FOR
END FOR</pre>
<div class="callout callout-try"><div><strong>Try it</strong>Sort ${C`{8,4,1,9,3}`} by hand for two full passes; write swaps after each comparison.</div></div>`,
      },
      {
        title: "2.4 Selection sort & searching",
        html: `
<p><strong>Selection sort</strong> finds the minimum in the unsorted portion and swaps it into place — also $O(n^2)$ but fewer swaps than bubble sort.</p>
<p><strong>Linear search</strong> scans until found or end — works on unsorted data, $O(n)$.</p>
<p><strong>Binary search</strong> requires a <em>sorted</em> list; halve the search range each step — $O(\\log n)$.</p>
$$ \\text{mid} = \\left\\lfloor \\frac{\\text{low} + \\text{high}}{2} \\right\\rfloor $$
<div class="callout callout-exam"><div><strong>Exam tip</strong>State preconditions: binary search needs sorted input; bubble/selection do not.</div></div>`,
      },
    ],
    practice: [
      "Write pseudocode to find the largest of three numbers.",
      "Trace bubble sort on ${C`{5,2,8,1}`} until sorted.",
      "How many comparisons for binary search on 16 sorted items (worst case)?",
      "Give one real-life use of pattern recognition in apps you use daily.",
    ],
  },
  {
    grade: "XI",
    unit: 3,
    slug: "Programming-Fundamentals",
    title: "Programming Fundamentals (Python)",
    tagline: "IDE, variables, control flow, and libraries",
    outcomes: [
      "Explain low/mid/high-level languages and why Python is beginner-friendly",
      "Use an IDE (e.g. VS Code) to write and debug programs",
      "Apply selection and repetition in Python",
      "Import built-in and third-party libraries",
    ],
    sections: [
      {
        title: "3.1 Programming & language levels",
        html: `
<p>A <strong>program</strong> is a set of instructions. Languages sit on a spectrum:</p>
<ul>
<li><strong>Low-level</strong> — machine/binary (fast, hard to read)</li>
<li><strong>Mid-level</strong> — e.g. assembly (mnemonics)</li>
<li><strong>High-level</strong> — Python, Java (readable, portable)</li>
</ul>
<p><strong>Python</strong> emphasizes readability — ideal for learning logic, data work, web (Django/Flask), and automation.</p>`,
      },
      {
        title: "3.2 Python building blocks",
        html: `
<pre># variables &amp; types
name = "Ali"
age = 16
average = 78.5
is_enrolled = True

# selection
if average &gt;= 50:
    print("Pass")
else:
    print("Improve")

# repetition
for i in range(1, 6):
    print("*" * i)</pre>
<p>Common types: <code>int</code>, <code>float</code>, <code>str</code>, <code>bool</code>. Indentation defines blocks — no braces.</p>`,
      },
      {
        title: "3.3 IDE workflow",
        html: `
<p><strong>VS Code</strong> + Python extension gives editing, syntax highlight, run, and debugger. Workflow: edit → run → read traceback → fix → repeat.</p>
<div class="callout callout-try"><div><strong>Try it</strong>Write a program that asks for two numbers and prints sum, difference, product, and quotient (guard divide-by-zero).</div></div>`,
      },
      {
        title: "3.4 Libraries",
        html: `
<pre>import math
print(math.sqrt(144))

# third-party (install via pip)
# pip install requests</pre>
<p>Libraries reuse tested code — you focus on problem logic instead of reinventing wheels.</p>`,
      },
    ],
    practice: [
      "Print multiplication table of 7 using a loop.",
      "Convert Celsius to Fahrenheit: $F = \\frac{9}{5}C + 32$.",
      "Debug: why does <code>if x = 5</code> fail in Python?",
    ],
  },
  {
    grade: "XI",
    unit: 4,
    slug: "Data-and-Analysis",
    title: "Data and Analysis (Databases)",
    tagline: "Relational design, integrity, and DBMS objects",
    outcomes: [
      "Define tables, keys, and relationships (1:1, 1:M, M:N)",
      "Apply referential integrity (cascade update/delete)",
      "Draw ER diagrams and relational schemas",
      "Use tables, forms, queries, and reports in a DBMS",
    ],
    sections: [
      {
        title: "4.1 Database concepts",
        html: `
<p>A <strong>database</strong> stores related data persistently. A <strong>DBMS</strong> (e.g. Access, MySQL) manages storage, queries, and security.</p>
<p><strong>Primary key</strong> uniquely identifies a row. <strong>Foreign key</strong> links to another table’s primary key.</p>`,
        diagram: "dbRelations",
        diagramCaption: "Figure 4.1 — Students enroll in many courses (M:N via junction table).",
      },
      {
        title: "4.2 Relationships & integrity",
        html: `
<table class="data">
<tr><th>Type</th><th>Meaning</th><th>Example</th></tr>
<tr><td>1:1</td><td>One row ↔ one row</td><td>Person ↔ Passport</td></tr>
<tr><td>1:M</td><td>One parent, many children</td><td>Department ↔ Employees</td></tr>
<tr><td>M:N</td><td>Many on both sides</td><td>Students ↔ Courses</td></tr>
</table>
<p><strong>Referential integrity</strong> prevents orphan records. <strong>Cascade update/delete</strong> propagates changes when parent rows change.</p>`,
      },
      {
        title: "4.3 Queries & reports",
        html: `
<p><strong>Queries</strong> filter and calculate (SELECT, WHERE, ORDER BY). <strong>Forms</strong> ease data entry; <strong>reports</strong> present summaries for printing.</p>
<div class="callout callout-try"><div><strong>Try it</strong>Design tables Student(ID, Name) and Result(StudentID, Subject, Marks) with a 1:M link. Write a query for students with Marks &gt; 80.</div></div>`,
      },
    ],
    practice: [
      "Convert an M:N Teacher–Subject assignment into two 1:M tables.",
      "List fields you would put in an ER diagram for a library system.",
    ],
  },
  {
    grade: "XI",
    unit: 5,
    slug: "Applications-Impacts-Computing",
    title: "Applications & Impacts of Computing",
    tagline: "AI, IoT, ethics, and reliable information",
    outcomes: [
      "Describe IoT components and smart-city/industry examples",
      "Explain basics of AI and everyday uses in Pakistan",
      "Judge reliable vs unreliable online sources",
      "Discuss human and environmental impacts of computing",
    ],
    sections: [
      {
        title: "5.1 Computing in daily life",
        html: `
<p>Computing spans education (LMS), healthcare (records), banking (apps/ATMs), agriculture (weather/irrigation), and industry automation.</p>`,
      },
      {
        title: "5.2 AI & IoT",
        html: `
<p><strong>Artificial Intelligence</strong> — systems that learn patterns (recommendations, voice assistants, image filters). Needs quality data and clear purpose.</p>
<p><strong>Internet of Things (IoT)</strong> — sensors + connectivity + cloud analytics (smart meters, wearables, fleet tracking).</p>
<div class="flex-grid">
  <div class="card"><h3>Smart city</h3><p>Traffic sensors, air quality monitors</p></div>
  <div class="card"><h3>Healthcare</h3><p>Remote vitals, bed availability</p></div>
  <div class="card"><h3>Education</h3><p>Automated attendance, adaptive quizzes</p></div>
</div>`,
      },
      {
        title: "5.3 Digital citizenship",
        html: `
<p>Evaluate sources: author, date, evidence, bias. Prefer peer-reviewed, official, and cross-checked facts over viral posts.</p>
<p>Impacts include e-waste, energy use, job shifts, and privacy — balance innovation with responsibility.</p>`,
      },
    ],
    practice: [
      "Name three IoT devices at home or school and what data they collect.",
      "Compare two news URLs for credibility using a checklist.",
    ],
  },
  {
    grade: "XI",
    unit: 6,
    slug: "Digital-Literacy",
    title: "Digital Literacy",
    tagline: "Research, data collection, and presentation",
    outcomes: [
      "Plan surveys, interviews, or prototypes for original data",
      "Apply ethical, safe online research habits",
      "Present findings with charts, infographics, and reports",
    ],
    sections: [
      {
        title: "6.1 Research skills",
        html: `
<p><strong>Digital literacy</strong> is using devices and the internet safely, critically, and productively.</p>
<p>Advanced search: quoted phrases, site: filters, date ranges. Primary data — interviews, surveys; secondary — reports, articles.</p>`,
      },
      {
        title: "6.2 Data collection & ethics",
        html: `
<p>Define purpose, sample size, and consent before collecting personal data. Anonymize responses when possible.</p>`,
      },
      {
        title: "6.3 Presenting data",
        html: `
<p>Choose chart types: bar (categories), line (trends), pie (parts of whole — use sparingly). Label axes, cite sources, avoid misleading scales.</p>
<div class="callout callout-try"><div><strong>Try it</strong>Collect 10 classmates’ favorite subjects; show bar chart and one-sentence insight.</div></div>`,
      },
    ],
    practice: [
      "Draft five neutral survey questions about phone use for study.",
      "List three signs of a trustworthy website.",
    ],
  },
  {
    grade: "XII",
    unit: 1,
    slug: "Human-Computer-Interaction",
    title: "Human Computer Interaction (HCI)",
    tagline: "UX, accessibility, and Figma prototyping",
    outcomes: [
      "Explain HCI fundamentals and interaction channels",
      "Apply accessibility (contrast, readability, inclusive navigation)",
      "Analyze user needs and common HCI problems",
      "Design and evaluate wireframes in Figma",
    ],
    sections: [
      {
        title: "1.1 HCI model",
        html: `
<p><strong>HCI</strong> designs technology for people — usable, efficient, satisfying. Channels: sight (screens), touch (tap/type), hearing (audio), voice (commands), spatial (motion/gesture).</p>`,
        diagram: "hci",
        diagramCaption: "Figure 1.1 — Human sends commands; computer returns feedback through the UI.",
      },
      {
        title: "1.2 UX vs UI",
        html: `
<p><strong>UI</strong> — visual layout, controls, typography. <strong>UX</strong> — entire journey (learnability, errors, satisfaction). Good UX needs user research, not only pretty screens.</p>`,
      },
      {
        title: "1.3 Accessibility & inclusive design",
        html: `
<ul>
<li>Contrast ratio for text (WCAG guidelines)</li>
<li>Readable font sizes and line spacing</li>
<li>Keyboard navigation and clear focus states</li>
<li>Color-blind-safe palettes — don’t rely on color alone</li>
</ul>`,
      },
      {
        title: "1.4 Design process in Figma",
        html: `
<p>Flow: personas → user stories → low-fi wireframes → prototype links → usability test → iterate.</p>
<div class="callout callout-exam"><div><strong>Exam tip</strong>Link each design choice to a <em>user need</em> or <em>accessibility principle</em>, not personal taste.</div></div>`,
      },
    ],
    practice: [
      "Audit one school website for contrast and navigation clarity.",
      "Sketch three screens for a canteen ordering app.",
    ],
  },
  {
    grade: "XII",
    unit: 2,
    slug: "Computational-Thinking-Algorithms-Advanced",
    title: "Computational Thinking & Algorithms (Advanced)",
    tagline: "Tracing, efficiency, and correctness",
    outcomes: [
      "Trace algorithms with trace tables",
      "Evaluate clarity and efficiency of solutions",
      "Compare algorithm strategies for the same problem",
    ],
    sections: [
      {
        title: "2.1 Correctness & tracing",
        html: `
<p>A trace table records variables row-by-row for each statement — proves an algorithm works or reveals bugs.</p>
<pre>// swap max of two
if a &lt; b:
    temp = a; a = b; b = temp</pre>
<p>Columns: line number, inputs, each variable, output.</p>`,
      },
      {
        title: "2.2 Efficiency",
        html: `
<p>Compare growth: constant $O(1)$, linear $O(n)$, quadratic $O(n^2)$, logarithmic $O(\\log n)$.</p>
$$ T(n) \\approx c \\cdot n^2 \\quad \\text{(nested loops over n items)} $$
<p>Choose binary search over linear when data is sorted and large.</p>`,
      },
      {
        title: "2.3 Refinement strategies",
        html: `
<p>Start brute force → identify repeated work → add sorting/index → consider edge cases (empty list, duplicates).</p>`,
      },
    ],
    practice: [
      "Trace selection sort on four elements with a table.",
      "Why is $O(n^2)$ risky for $n=10^6$?",
    ],
  },
  {
    grade: "XII",
    unit: 3,
    slug: "Programming-Fundamentals-Advanced",
    title: "Programming Fundamentals (Advanced Python)",
    tagline: "Collections, functions, and modules",
    outcomes: [
      "Use lists, tuples, sets, and dictionaries appropriately",
      "Write functions with parameters and return values",
      "Handle files and exceptions at a basic level",
    ],
    sections: [
      {
        title: "3.1 Collections",
        html: `
<pre>marks = [88, 92, 75]          # list — mutable
coords = (30.2, 71.5)         # tuple — immutable
tags = {"python", "exam"}     # set — unique items
student = {"id": 1, "name": "Sara"}  # dict — key/value</pre>
<p>Pick structure by need: ordered & changeable → list; fixed record → tuple; membership tests → set; lookup by key → dict.</p>`,
      },
      {
        title: "3.2 Functions",
        html: `
<pre>def grade(m):
    if m &gt;= 80: return "A"
    if m &gt;= 60: return "B"
    return "C"

def average(nums):
    return sum(nums) / len(nums)</pre>`,
      },
      {
        title: "3.3 Files & errors",
        html: `
<pre>try:
    with open("data.txt") as f:
        print(f.read())
except FileNotFoundError:
    print("Missing file")</pre>`,
      },
    ],
    practice: [
      "Count word frequencies in a sentence using a dictionary.",
      "Write a function is_palindrome(s) ignoring case.",
    ],
  },
  {
    grade: "XII",
    unit: 4,
    slug: "Data-Analysis-Python",
    title: "Data and Analysis (Python)",
    tagline: "DB connectivity, stats, and visualization",
    outcomes: [
      "Connect Python to databases",
      "Compute mean, median, mode, spread",
      "Create bar charts, histograms, scatter plots, box plots",
    ],
    sections: [
      {
        title: "4.1 Data analysis pipeline",
        html: `
<p>Collect → clean → analyze → visualize → decide. Python libraries (pandas, matplotlib) automate heavy lifting.</p>`,
      },
      {
        title: "4.2 Central tendency & spread",
        html: `
<p>Mean: $\\bar{x} = \\frac{1}{n}\\sum x_i$. Median — middle value; mode — most frequent.</p>
<p>Range, variance, and standard deviation show spread — essential before comparing classes or sales regions.</p>`,
      },
      {
        title: "4.3 Visualization choices",
        html: `
<div class="flex-grid">
  <div class="card"><h3>Bar</h3><p>Compare categories</p></div>
  <div class="card"><h3>Histogram</h3><p>Distribution of numeric data</p></div>
  <div class="card"><h3>Scatter</h3><p>Relationship between two variables</p></div>
  <div class="card"><h3>Box plot</h3><p>Median, quartiles, outliers</p></div>
</div>`,
      },
    ],
    practice: [
      "Given five test scores, compute mean and median by hand.",
      "When would a scatter plot mislead if axes are not labeled?",
    ],
  },
  {
    grade: "XII",
    unit: 5,
    slug: "Applications-Impacts-Advanced",
    title: "Applications & Impacts (AI & Security)",
    tagline: "Neural networks, collaboration, and threats",
    outcomes: [
      "Outline neural networks and deep learning uses",
      "Explain secure collaboration and data protection",
      "Identify threats (phishing, malware) and mitigations",
      "Discuss equity and access in digital tools",
    ],
    sections: [
      {
        title: "5.1 Neural networks (conceptual)",
        html: `
<p>Neurons receive inputs, apply weights, activate, and pass signals layer-by-layer. <strong>Deep learning</strong> uses many layers for vision, speech, and language tasks.</p>
<p>Needs large datasets, compute power, and ethical oversight (bias, privacy).</p>`,
      },
      {
        title: "5.2 Security & collaboration",
        html: `
<p>Use strong passwords, 2FA, encryption in transit (HTTPS), least-privilege sharing. Threats: phishing, ransomware, social engineering.</p>
<p>Mitigate: updates, backups, user training, firewalls, antivirus.</p>`,
      },
      {
        title: "5.3 Digital equity",
        html: `
<p>Equal access means affordable connectivity, accessible interfaces, and policies that don’t exclude rural or disabled learners.</p>`,
      },
    ],
    practice: [
      "List three deep-learning apps and the data they need.",
      "Design a phishing-awareness poster for classmates.",
    ],
  },
  {
    grade: "XII",
    unit: 6,
    slug: "Entrepreneurship-Digital-Age",
    title: "Entrepreneurship in the Digital Age",
    tagline: "Ideas, prototypes, and MVP",
    outcomes: [
      "Turn problems into business ideas with local examples",
      "Differentiate low/mid/high-fidelity prototypes",
      "Define MVP and test riskiest assumptions",
      "Plan features, cost, marketing, and beachhead market",
    ],
    sections: [
      {
        title: "6.1 Entrepreneur mindset",
        html: `
<p>An <strong>entrepreneur</strong> spots problems and builds solutions that create value. Digital tools lower cost to test ideas (websites, social ads, no-code apps).</p>`,
      },
      {
        title: "6.2 Prototypes",
        html: `
<table class="data">
<tr><th>Fidelity</th><th>What it is</th><th>When to use</th></tr>
<tr><td>Low</td><td>Paper sketches</td><td>Early feedback, fast</td></tr>
<tr><td>Mid</td><td>Clickable wireframes</td><td>Test flows</td></tr>
<tr><td>High</td><td>Near-real UI</td><td>Usability before build</td></tr>
</table>`,
      },
      {
        title: "6.3 MVP & learning loop",
        html: `
<p><strong>Minimum Viable Product</strong> — smallest version that tests your riskiest assumption (will users pay? will they return?). Collect feedback → iterate.</p>
<p>Plan: core features, rough cost, marketing channel, <strong>beachhead market</strong> (first focused customer group).</p>
<div class="callout callout-try"><div><strong>Try it</strong>Pick a campus problem; write one-sentence value proposition and three MVP features only.</div></div>`,
      },
    ],
    practice: [
      "Compare prototype vs MVP for a tutoring app.",
      "Name your riskiest assumption and how to test it in one week.",
    ],
  },
];
