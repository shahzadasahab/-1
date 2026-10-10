#!/usr/bin/env python3
"""Build a self-contained HTML study guide with embedded MathJax + SVG diagrams."""

from __future__ import annotations

from pathlib import Path

from web import svgs

ROOT = Path(__file__).resolve().parent
WEB = ROOT / "web"
OUT_HTML = WEB / "index.html"


def css() -> str:
    return (WEB / "guide.css").read_text(encoding="utf-8")


def fig(svg: str, caption: str) -> str:
    return '<figure class="wide">' + svg + "<figcaption>" + caption + "</figcaption></figure>"


def box(kind: str, title: str, body: str) -> str:
    return (
        '<aside class="callout ' + kind + '"><div class="tag">' + title
        + "</div><div>" + body + "</div></aside>"
    )


def table(headers, rows) -> str:
    head = "".join("<th>" + h + "</th>" for h in headers)
    body = []
    for row in rows:
        body.append("<tr>" + "".join("<td>" + c + "</td>" for c in row) + "</tr>")
    return "<table><thead><tr>" + head + "</tr></thead><tbody>" + "".join(body) + "</tbody></table>"


def unit1() -> str:
    return "\n".join([
        "<h1>Unit 1 — Computer Systems</h1>",
        '<p class="lead">Three questions: how does a machine represent truth with two states, how do teams turn an idea into software, and how do distant machines agree on a conversation?</p>',
        box("exam", "STUDY IN THREE SITTINGS", "Logic and gates · SDLC case studies · OSI/TCP-IP. After each sitting, rebuild the main table from memory."),
        "<h2>1.1 Discrete versus continuous</h2>",
        "<p>A <strong>discrete</strong> quantity takes separate countable values (31 students, never 31.4). A <strong>continuous</strong> quantity can take any value in a range (temperature, height, time). Digital electronics copies the stairs: a wire is LOW (\\(0\\)) or HIGH (\\(1\\)).</p>",
        fig(svgs.stairs_ramp(), "Figure 1.1 — Stairs (discrete / digital) versus a ramp (continuous / analog)."),
        fig(svgs.analog_digital(), "Figure 1.2 — Analog signals vary smoothly; digital signals jump between two legal levels."),
        table(["Feature", "Analog", "Digital"], [
            ["Nature", "Continuous, infinitely many in-between values", "Discrete steps; usually two levels"],
            ["Waveform", "Sine-like", "Square"],
            ["Unit", "Physical quantity", "Bit: \\(0\\) or \\(1\\)"],
            ["Noise", "Adds permanently", "Ignored if it stays inside a band"],
            ["Examples", "Voice, vinyl, mercury thermometer", "USB, HDMI, calculator"],
        ]),
        "<h2>1.2 Boolean algebra</h2>",
        "<p>George Boole’s algebra uses only \\(\\mathrm{FALSE}=0\\) and \\(\\mathrm{TRUE}=1\\). Precedence is</p>",
        "\\[ (\\,\\cdot\\,) \\;\\to\\; \\text{NOT }(\\,'\\,) \\;\\to\\; \\text{AND }(\\,\\cdot\\,) \\;\\to\\; \\text{OR }(\\,+). \\]",
        "<ul>",
        "<li><strong>AND:</strong> \\(Y = A \\cdot B = 1\\) only if every input is \\(1\\).</li>",
        "<li><strong>OR:</strong> \\(Y = A + B = 1\\) if any input is \\(1\\).</li>",
        "<li><strong>NOT:</strong> \\(Y = A' = \\overline{A}\\) flips one bit.</li>",
        "</ul>",
        "<p><strong>Worked evaluations.</strong> For \\(A=1,\\; B=0\\): \\(Y=A'+B = 0+0=0\\). For \\(A=1,\\;B=0,\\;C=1\\): \\(Y=(A+B)\\cdot C = 1\\cdot 1=1\\). For \\(A=B=C=1\\): \\(Y=A\\cdot B + C' = 1 + 0 = 1\\).</p>",
        box("try", "TRY THIS NOW", "Evaluate \\(Y=(A\\cdot B)'+C\\) for \\(A=1,B=1,C=0\\). Answer: NAND of \\(1,1\\) is \\(0\\), then \\(0+0=0\\)."),
        "<h2>1.3 The seven gates</h2>",
        "<p>A truth table with \\(n\\) inputs has \\(2^n\\) rows. List inputs in binary order so no row is skipped.</p>",
        svgs.all_gates(),
        "<p>Derived identities you must write in math form:</p>",
        r"\[ \begin{aligned} Y_{\mathrm{NAND}} &= (A\cdot B)' ,& Y_{\mathrm{NOR}} &= (A+B)' ,\\ Y_{\mathrm{XOR}} &= A\oplus B = A'B + AB' ,& Y_{\mathrm{XNOR}} &= (A\oplus B)' = AB + A'B'. \end{aligned} \]",
        "<p>NAND and NOR are <em>universal</em>: any Boolean function can be built from only NAND, or only NOR.</p>",
        table(["A", "B", "AND", "NAND", "OR", "NOR", "XOR", "XNOR"], [
            ["0", "0", "0", "1", "0", "1", "0", "1"],
            ["0", "1", "0", "1", "1", "0", "1", "0"],
            ["1", "0", "0", "1", "1", "0", "1", "0"],
            ["1", "1", "1", "0", "1", "0", "0", "1"],
        ]),
        "<h2>1.4 Expressions, diagrams, SOP</h2>",
        "<p>For \\(Y = A\\cdot B + C\\) (three variables \\(\\Rightarrow 8\\) rows) compute the helper column \\(A\\cdot B\\), then OR with \\(C\\).</p>",
        fig(svgs.circuit_and_or(), "Figure 1.3 — AND has higher precedence, so it is drawn first; its output feeds OR together with C."),
        "<p><strong>Sum of products:</strong> each row where \\(Y=1\\) is a minterm. If a variable is \\(0\\) in that row, complement it. Then</p>",
        r"\[ Y = \sum \text{minterms of the 1-rows}. \]",
        "<p>Example: 1-rows \\(AB=01\\) and \\(11\\) give \\(Y=A'B + AB = B\\).</p>",
        box("mistake", "COMMON MISTAKE", "In a minterm, a \\(0\\) in the row means the variable is complemented. Row \\(A=0,B=1\\) is \\(A'B\\), not \\(AB'\\)."),
        "<h2>1.5 Karnaugh maps</h2>",
        "<p>Adjacent cells (including wrap-around) differ by one bit — <strong>Gray code</strong>. Group \\(2^n\\) ones; the changing variables cancel.</p>",
        fig(svgs.kmap2(), "Figure 1.4 — Two-variable map for Y = A′B + AB′ + AB."),
        fig(svgs.kmap3(), "Figure 1.5 — Three-variable map. Columns are BC = 00, 01, 11, 10 — never 00, 01, 10, 11."),
        box("try", "TRY THIS NOW", "Simplify \\(Y=\\sum m(0,1,2,3,5,7)\\). Two groups of four give \\(Y=A'+C\\)."),
        "<h2>1.6 Software Development Life Cycle</h2>",
        fig(svgs.sdlc_cycle(), "Figure 1.6 — The six SDLC phases form a maintenance cycle, not a dead end."),
        table(["Phase", "Activity", "Deliverable"], [
            ["1 Analysis", "Meet users; list features", "SRS"],
            ["2 Design", "HLD/LLD, screens, ER, UML", "Design document"],
            ["3 Implementation", "Code, Git, comments", "Working build"],
            ["4 Testing", "Unit, integration, system, UAT", "Test report"],
            ["5 Deployment", "Direct, phased, pilot, parallel", "Live software"],
            ["6 Maintenance", "Corrective, adaptive, perfective, preventive", "Patches"],
        ]),
        "<p><strong>CAPP maintenance:</strong> Corrective (login bug), Adaptive (new Windows), Perfective (dark mode), Preventive (daily backup).</p>",
        fig(svgs.waterfall_agile(), "Figure 1.7 — Waterfall finishes a phase before the next begins. Agile repeats a short sprint."),
        "<p>Al-Noor Library (fixed 2,400-book system, offline Windows, six months) fitted <strong>Waterfall</strong>. The student mobile app (unclear features, five two-week sprints, Flutter) fitted <strong>Agile / Scrum</strong>. Same school, two models — match the model to the project.</p>",
        "<h2>1.7 Communication models</h2>",
        fig(svgs.osi_stack(), "Figure 1.8 — OSI seven-layer stack with typical protocols."),
        fig(svgs.encapsulation(), "Figure 1.9 — Encapsulation names: data → segment → packet → frame → bits."),
        fig(svgs.tcpip_map(), "Figure 1.10 — TCP/IP collapses OSI 7–5 into Application and OSI 2–1 into Network Access."),
        "<p>TCP is connection-oriented and reliable (web, email, files). UDP is connectionless and cheap (live video, games). An <strong>IP address</strong> is logical; a <strong>MAC address</strong> is burned into the NIC. Routers live at Layer 3; switches at Layer 2; hubs at Layer 1. <code>ping</code> uses ICMP at the Network layer.</p>",
    ])


def unit2() -> str:
    return "\n".join([
        "<h1>Unit 2 — Computational Thinking and Algorithms</h1>",
        '<p class="lead">Computational thinking is thinking so clearly that a machine — or another human — can follow you.</p>',
        "<p>An <strong>algorithm</strong> is a finite, language-independent sequence of steps. <strong>Pseudocode</strong> writes those steps with IF/FOR/WHILE but no compiler syntax.</p>",
        "<ul>",
        "<li><strong>Decomposition</strong> — split “learn Spanish” into alphabet, vocabulary, grammar, practice.</li>",
        "<li><strong>Pattern recognition</strong> — a triangle of stars that grows by one star per row is a loop \\(i=1\\ldots n\\).</li>",
        "<li><strong>Abstraction</strong> — making tea is boil, add, steep, pour. Ignore mug colour.</li>",
        "</ul>",
        box("exam", "EXAM TIP", "Ignoring the kettle brand is abstraction, not decomposition."),
        "<h2>2.1 Bubble Sort</h2>",
        "<p>Compare neighbours; swap if out of order. After pass \\(k\\), the \\(k\\) largest items sit at the right. Nested loops give time that grows like \\(n^2\\).</p>",
        fig(svgs.bubble_sort_passes(), "Figure 2.1 — Trace of {8, 4, 1, 9, 3} in ascending order. Teal cells are already parked."),
        "<pre>FOR pass ← 0 TO n−2\n    FOR i ← 0 TO n−2−pass\n        IF DATA[i] > DATA[i+1] THEN swap</pre>",
        "<p><strong>Strengths:</strong> in-place and stable. <strong>Weaknesses:</strong> time grows like \\(n^2\\); many swaps.</p>",
        "<h2>2.2 Selection Sort</h2>",
        "<p>On pass \\(k\\), find the minimum of the unsorted tail and swap it into index \\(k\\). At most one write per pass — fewer swaps than Bubble Sort, still \\(\\Theta(n^2)\\) comparisons, not stable.</p>",
        fig(svgs.selection_sort_passes(), "Figure 2.1b — Same list under Selection Sort. Gold is the newly parked minimum."),
        "<h2>2.3 Searching</h2>",
        "<p><strong>Linear search</strong> checks items \\(1,2,\\ldots,n\\). Works on unsorted data. Worst case \\(n\\) probes.</p>",
        "<p><strong>Binary search</strong> requires a sorted array. Each step uses</p>",
        r"\[ \mathrm{mid} = \left\lfloor \frac{\mathrm{low}+\mathrm{high}}{2} \right\rfloor. \]",
        "<p>If the target is smaller, set \\(\\mathrm{high}=\\mathrm{mid}-1\\); if larger, \\(\\mathrm{low}=\\mathrm{mid}+1\\). About \\(\\log_2 n\\) probes — twenty looks for a million items.</p>",
        fig(svgs.binary_search(), "Figure 2.2 — Binary search for 3. Gold cell is mid; grey cells have been discarded."),
        box("mistake", "COMMON MISTAKE", "Binary search on an unsorted list is not “a bit worse.” It is wrong: the discarded half may hold the target."),
        table(["", "Linear", "Binary"], [
            ["Needs sorted data?", "No", "Yes"],
            ["Idea", "One-by-one", "Halve the interval"],
            ["Best for", "Small or unsorted; one-off search", "Large static sorted lists"],
            ["Growth", "\\(O(n)\\)", "\\(O(\\log n)\\)"],
        ]),
        "<p>Judge every algorithm on <strong>correctness</strong> (right for every valid input, and it finishes), <strong>efficiency</strong> (time and memory as \\(n\\) grows), and <strong>clarity</strong>.</p>",
    ])


def unit3() -> str:
    return "\n".join([
        "<h1>Unit 3 — Programming Fundamentals</h1>",
        '<p class="lead">A computer does exactly what you said, including the mistakes. Python is the high-level language this course uses because it reads almost like English.</p>',
        fig(svgs.python_flow(), "Figure 3.1 — Selection: exactly one path runs."),
        "<p><code>input()</code> always returns a <strong>string</strong>. Convert with <code>int()</code> or <code>float()</code>. Indentation is syntax: 4 spaces per block.</p>",
        table(["Family", "Symbols", "Notes"], [
            ["Arithmetic", "+ − * / // % **", "\\(9//2=4\\), \\(9\\%2=1\\), \\(2^{3}=8\\)"],
            ["Assignment", "= += −= *=", "After a = 10; a += 5, a is 15"],
            ["Relational", "== != &gt; &lt; &gt;= &lt;=", "Return True/False"],
            ["Logical", "and · or · not", "Combine conditions"],
            ["Membership", "in · not in", '"P" in "Python" is True'],
            ["Bitwise", "&amp; | ^ ~ &lt;&lt; &gt;&gt;", "Same truth tables as Unit 1 gates"],
        ]),
        "<p>Bitwise worked example. \\(a=10=1010_{2}\\), \\(b=6=0110_{2}\\):</p>",
        r"\[ a \land b = 0010_{2}=2,\quad a \lor b = 1110_{2}=14,\quad a \oplus b = 1100_{2}=12,\quad a \ll 1 = 20 = a\cdot 2. \]",
        "<p>Also \\(\\sim x = -x-1\\) in two’s complement, so \\(\\sim 10=-11\\).</p>",
        box("mistake", "COMMON MISTAKE", "= stores a value. == tests equality. Using input() in arithmetic without int()/float() is the classic first-year crash."),
        "<h2>3.1 Control and libraries</h2>",
        "<p><strong>for</strong> when the trip count is known (<code>range(start, stop, step)</code>). <strong>while</strong> until a condition dies. <code>break</code> leaves now; <code>continue</code> skips this iteration.</p>",
        "<pre>import math, random, datetime\nprint(math.sqrt(25), math.pi)\nsecret = random.randint(1, 10)\nnow = datetime.datetime.now().strftime(\"%d-%m-%Y\")</pre>",
        "<p>Third-party libraries need <code>pip install</code> (NumPy, Pandas, Matplotlib).</p>",
        table(["Error", "When", "Example"], [
            ["Syntax", "Will not start", "Missing ), bad indent, if without :"],
            ["Runtime", "Dies while running", "10/0, int(\"abc\")"],
            ["Logical", "Runs and lies", "i -= 1 in a loop that should climb — infinite loop"],
        ]),
        "<p>Read a traceback from the bottom: last line is the disease.</p>",
    ])


def unit4() -> str:
    return "\n".join([
        "<h1>Unit 4 — Data and Analysis</h1>",
        '<p class="lead">Eighty, seventy-five, ninety is data. “The class average is 80%” is information. A database is the organised cupboard that keeps those facts consistent.</p>',
        "<p>A <strong>DBMS</strong> (Access, MySQL, Oracle, SQL Server) inserts, updates, deletes, and retrieves with less redundancy, better consistency, security, and integrity. An <strong>RDBMS</strong> stores related tables.</p>",
        table(["Key", "Role"], [
            ["Candidate", "Any unique non-null identifier — a table may have several"],
            ["Primary", "The chosen candidate; exactly one; never NULL"],
            ["Alternate", "A leftover candidate"],
            ["Foreign", "Points at another table’s primary key; may repeat"],
        ]),
        fig(svgs.cardinalities(), "Figure 4.1 — Three cardinalities. Only M:N needs a junction table."),
        fig(svgs.er_library(), "Figure 4.2 — Library ER: Member and Book are M:N, resolved as BorrowRecord."),
        "<p><strong>Referential integrity:</strong> every foreign key must match a living parent. <em>Cascade update</em> rewrites child FKs when the parent PK changes. <em>Cascade delete</em> removes child rows when the parent is deleted — use it like a chainsaw.</p>",
        "<p>Access objects: <strong>table</strong> stores, <strong>form</strong> enters, <strong>query</strong> asks, <strong>report</strong> prints. In Query Design, AND is the same criteria row; OR is different rows. Totals \\(\\Sigma\\): Group By + Count/Avg/Sum/Min/Max. Line charts show trends; pies show parts of a whole; bars compare named categories.</p>",
    ])


def unit5() -> str:
    return "\n".join([
        "<h1>Unit 5 — Applications and Impacts of Computing</h1>",
        '<p class="lead">IoT collects, analytics explains, AI decides. Treat those three words as a loop, not as synonyms.</p>',
        fig(svgs.iot_loop(), "Figure 5.1 — Smart irrigation: moisture sensor → radio → cloud analysis → valve actuator → farmer’s phone."),
        fig(svgs.analytics_pipe(), "Figure 5.2 — Analytics turns raw records into a decision only after cleaning."),
        table(["", "IoT", "Analytics", "AI"], [
            ["Job", "Sense and actuate", "Find patterns", "Decide or predict"],
            ["Pieces", "Sensors, actuators, links, cloud, UI", "Collect–store–clean–analyse–visualise", "Models, learning"],
            ["Example", "Soil probe, smartwatch", "Pass/fail pie chart", "Face unlock, recommendation"],
        ]),
        "<p><strong>Sensor ≠ actuator.</strong> A moisture probe does not open the tap; the valve does. Connectivity (Wi-Fi, Bluetooth, 4G/5G, LoRa) carries the message. Cloud stores the history. The UI is how a human looks and commands.</p>",
        "<h2>5.1 Sources and impacts</h2>",
        table(["Kind", "Meaning", "Example"], [
            ["Primary", "First-hand original", "Interview, NADRA CNIC capture"],
            ["Secondary", "Already explained", "Textbook, PBS census summary"],
            ["Tertiary", "Quick digest", "Encyclopedia, many Wikipedia leads"],
        ]),
        "<p>A nameless social-media image with no date is simply unreliable. Computing helps (recorded lessons, telemedicine, digital banks) and harms (screen fatigue, leaked records, lost jobs). Responsible use: strong passwords, no rumour-forwarding, planned offline time.</p>",
        "<p><strong>Assistive tech</strong> — mobility (wheelchair), sensory (NVDA screen reader), communication (picture boards), cognitive (audiobooks). They are how computing keeps its promise to everyone.</p>",
    ])


def unit6() -> str:
    return "\n".join([
        "<h1>Unit 6 — Digital Literacy</h1>",
        '<p class="lead">Digital literacy is not “I can open Chrome.” It is find, judge, collect, and show — without stealing words or leaking private data.</p>',
        fig(svgs.inquiry_flow(), "Figure 6.1 — Digital inquiry workflow from a sharp question to a final artefact."),
        table(["", "Qualitative", "Quantitative"], [
            ["Nature", "Words, reasons, feelings", "Numbers you can count"],
            ["Ask", "Why / how", "How many / how much"],
            ["Example", "“Notifications break my focus”", "4 hours/day, 72% distracted"],
        ]),
        "<p><strong>Primary data</strong> is what you gather for this question. <strong>Secondary data</strong> already exists (a PBS table). Advanced search: quotes for a phrase, <code>filetype:pdf</code> for reports, <code>site:.edu</code> or <code>site:.gov.pk</code> for a domain family.</p>",
        "<ol>",
        "<li>One sharp research question.</li>",
        "<li>Qualitative, quantitative, or mixed.</li>",
        "<li>Method that can actually answer it (interview, survey, observation, prototype, simulation).</li>",
        "<li>A sample that resembles the group.</li>",
        "<li>Tools: form, script, sheet.</li>",
        "<li>Collect without steering people toward your favourite answer.</li>",
        "<li>Store in a spreadsheet; keep a backup.</li>",
        "<li>Ethics: permission, no extra personal fields, no silent copying (plagiarism).</li>",
        "</ol>",
        "<p>A decorated Canva file is not an artefact if it never answers the question. Evidence → claim → recommendation.</p>",
    ])


def depth() -> str:
    return "\n".join([
        "<h1>Case studies and closed-book drills</h1>",
        "<h2>Al-Noor Library — why Waterfall worked</h2>",
        "<p>1,200 students, 2,400 books, paper register, lost copies, handwritten overdue lists. Requirements were frozen: add/edit books, search, 14-day loans, overdue alerts, printed reports, offline Windows. Team of four, six months, Python + Tkinter + SQLite. Waterfall fitted because nothing experimental was asked. Testing (black box) found a search crash on misspellings and an overdue alert that ran only if a button was clicked. Both were fixed and retested. A two-week <strong>pilot</strong> sat on the librarian’s desk before students used it. Later maintenance: printer-driver fix (corrective), e-book category (adaptive), faster search (perfective), daily USB backup (preventive). Overdue returns fell about 70%.</p>",
        "<h2>Al-Noor Student App — why Agile worked</h2>",
        "<p>Nobody could list every feature on day one. Five two-week sprints, Flutter, five-person Scrum team. Sprint 1 shipped login + timetable; feedback added teacher names. Sprint 2 shipped exam results; parents then asked for a full attendance record. Sprint 3 shipped SMS absence alerts; when the gateway died for two days the team switched to email and kept moving. Sprint 4 connected to the library through an API and added an available-copies counter in thirty minutes. Sprint 5 shipped homework photos and fixed three launch bugs. Five of ten original stories shipped in ten weeks. That flexibility is the point of Agile.</p>",
        box("try", "DECISION RULE", "Pacemaker firmware with a frozen regulator spec → Waterfall (late change can kill). A club-events app that will grow with student requests → Agile. Four lines in a notebook is a complete 4-mark compare."),
        "<h2>Logic studio — \\(Y=(A+B)'\\cdot C\\)</h2>",
        "<p>NOR of \\(A,B\\) feeding AND with \\(C\\). Eight rows; \\(Y=1\\) only on \\(A=B=0,\\,C=1\\). One minterm: \\(A'B'C\\).</p>",
        table(["A", "B", "C", "A+B", "(A+B)′", "Y"], [
            ["0", "0", "0", "0", "1", "0"],
            ["0", "0", "1", "0", "1", "1"],
            ["0", "1", "0", "1", "0", "0"],
            ["0", "1", "1", "1", "0", "0"],
            ["1", "0", "0", "1", "0", "0"],
            ["1", "0", "1", "1", "0", "0"],
            ["1", "1", "0", "1", "0", "0"],
            ["1", "1", "1", "1", "0", "0"],
        ]),
        "<p>K-map wrap-around: \\(Y=\\sum m(0,2,8,10)\\) occupies the four corners. Shared literals are \\(B'\\) and \\(C'\\); \\(A\\) cancels. Result \\(Y=B'C'\\). Forget wrap-around and you leave four lonely minterms.</p>",
        "<h2>Protocol flash cards</h2>",
        table(["If you see…", "Layer", "Why"], [
            ["RJ45, Cat6, voltage, fibre pulse", "Physical", "Raw medium"],
            ["MAC, switch, Ethernet frame, CRC", "Data Link", "One LAN hop"],
            ["192.168.1.1, ping, router, OSPF", "Network", "Path across nets"],
            ["Port 443, handshake, segment", "Transport", "Which app, reliability"],
            ["Login session, RPC", "Session", "Conversation life"],
            ["TLS, JPEG, MP3, UTF-8", "Presentation", "Format / secret / size"],
            ["Browser, DNS lookup, SMTP send", "Application", "What the user asked"],
        ]),
        "<h2>Algorithm studio — same list, two sorts</h2>",
        "<p>Bubble Sort on \\(\\{6,2,5,1\\}\\): pass 1 → \\(\\{2,5,1,6\\}\\) (three swaps); pass 2 → \\(\\{2,1,5,6\\}\\); pass 3 → \\(\\{1,2,5,6\\}\\). Selection Sort finds min \\(1\\) and swaps once with \\(6\\) → \\(\\{1,2,5,6\\}\\). Fewer writes. Watch equal keys: Bubble Sort is stable; Selection Sort may swap two 4s.</p>",
        "<p>Binary search for 11 in \\(\\{2,5,7,11,13,17,19\\}\\): \\(\\mathrm{mid}=\\lfloor(0+6)/2\\rfloor=3\\), hit on the first probe. For 2 (left edge) you need three looks. For 12 (absent) you finish with \\(\\mathrm{low}&gt;\\mathrm{high}\\) and report not found — write that failure case so you do not invent a crash.</p>",
        table(["Move", "Strategy"], [
            ["Split “build the app” into login, marks, notices", "Decomposition"],
            ["Every notice has a title, date, body — same shape", "Pattern recognition"],
            ["Ignore button colour when specifying “post a notice”", "Abstraction"],
            ["Write numbered steps before opening VS Code", "Algorithm"],
        ]),
        "<h2>Python studio — ATM skeleton</h2>",
        "<pre>PIN = \"1234\"\nbalance = 10000.0\ntries = 3\nok = False\nwhile tries &gt; 0 and not ok:\n    entered = input(\"Enter PIN: \")\n    if entered == PIN:\n        ok = True\n    else:\n        tries -= 1\n        print(\"Wrong PIN!\", tries, \"left.\")\nif not ok:\n    print(\"Card locked.\")\nelse:\n    running = True\n    while running:\n        print(\"1 Check  2 Deposit  3 Withdraw  4 Exit\")\n        choice = input(\"Choose: \")\n        if choice == \"1\":\n            print(f\"Balance: Rs. {balance:.2f}\")\n        elif choice == \"2\":\n            amt = float(input(\"Deposit: \"))\n            if amt &gt; 0:\n                balance += amt\n        elif choice == \"3\":\n            amt = float(input(\"Withdraw: \"))\n            if 0 &lt; amt &lt;= balance:\n                balance -= amt\n            else:\n                print(\"Rejected.\")\n        elif choice == \"4\":\n            running = False</pre>",
        "<p>Sequence + selection + repetition + bool flags. Nested-if cousin: a guarded calculator that refuses \\(/0\\). Infinite-loop cousin: <code>i = 1; while i &lt; 6: print(i); i -= 1</code> — a logical error, legal Python that never dies.</p>",
        "<h2>Clinic ER (15 minutes on paper)</h2>",
        "<p>Patient and Doctor are M:N, resolved as Appointment(AppointmentID PK, PatientID FK, DoctorID FK, VisitDate, Fee). Cascade-delete of a doctor wipes history — forbid the delete or mark inactive. Customer 1—M Order needs no junction: one order belongs to one customer. AND is the same criteria row; OR is different rows.</p>",
        table(["Need", "Access Design grid"], [
            ["CS students only", "Department Criteria: \"Computer Science\""],
            ["IT or CS", "Criteria / or: two department values"],
            ["Aslam in IT", "Name and Department on the SAME row"],
            ["Headcount per dept", "Totals on; Department Group By; StudentID Count"],
            ["Average marks per dept", "Department Group By; Marks Avg"],
        ]),
        "<h2>Society and literacy studios</h2>",
        "<p>Memorise the smart-home skeleton: sensor → Wi-Fi → hub/cloud → analytics vs set-point → rule/AI → actuator → phone UI. If Wi-Fi dies the chain breaks — that one failure sentence shows you understand dependency.</p>",
        table(["Exhibit", "Verdict"], [
            ["Your interview with the librarian", "Primary source / primary data"],
            ["PBS graph of literacy rates", "Secondary"],
            ["Wikipedia lead paragraph", "Tertiary; start only"],
            ["Anonymous “forward this” image", "Unreliable — no author or date"],
            ["Government .gov.pk PDF, 2024", "Usually reliable secondary"],
        ]),
        "<p>Impact formula: field + one help + one harm + one responsible action. Mini inquiry (90 minutes): one question, two advanced searches, eight mixed items, 15 classmates with permission, one chart, one recommendation aimed at a real audience.</p>",
        "<h2>Unit self-tests (closed book)</h2>",
        "<p><strong>Unit 1.</strong> How many legal levels has a digital signal? Write \\(A\\oplus B\\) as a sum of products. Why is NAND universal? First SDLC deliverable? Which OSI layer adds ports / IP / MAC? Why might a cricket stream use UDP?</p>",
        "<p><strong>Unit 2.</strong> Define an algorithm. Which CT strategy ignores mug colour? Why does Selection Sort often swap less than Bubble Sort? One limitation of binary search. Name correctness, efficiency, clarity.</p>",
        "<p><strong>Unit 3.</strong> Legal comment syntax? Why is <code>my-var</code> illegal? What does <code>input()</code> return? Standard indent? Loop when the count is known? Bitwise AND? Three error types?</p>",
        "<p><strong>Unit 4.</strong> DBMS besides Access? ER rectangle? Relationship that needs a junction? Object for retrieval vs friendly entry? Aggregate for a mean? Define a foreign key. Cascade update? Chart for a monthly trend?</p>",
        "<p><strong>Unit 5.</strong> Watch → phone heart-rate is mainly which tech? Device that judges dry soil vs opens the valve? Duplicate rows are which analytics step? Interview is which source? Two reasons a website is unreliable? One help and one harm in healthcare? What does a screen reader do? Six IoT components?</p>",
        "<p><strong>Unit 6.</strong> Digital literacy in one sentence. “Notifications wreck my focus” — qualitative or quantitative? Best PDF search for internet use in Pakistan? Your own survey replies? What does <code>site:</code> do? Copying without credit? Why ask permission?</p>",
        "<h2>Selected answers</h2>",
        "<p>Digital: two levels, a noisy 1 is restored. \\(A\\oplus B = A'B+AB'\\). NAND builds any gate. SRS. Transport / Network / Data Link. UDP: late frames are useless. Algorithm: finite language-free steps. Abstraction. Selection: at most one swap per pass. Binary search needs sorted data. input → str. 4 spaces. for. \\(\\&\\). Syntax, runtime, logical. MySQL/Oracle/SQL Server. Entity. M:N. Query / Form. Avg(). FK points at another PK. Child FKs follow a parent PK change. Line chart. IoT. Sensor / valve. Cleaning. Primary. No author or date. Telemedicine / leaked files. Speaks on-screen text. Sensors, actuators, connectivity, processing, cloud, UI. Quotes + filetype:pdf. Primary data. Restrict domain. Plagiarism. Consent.</p>",
    ])


def extras() -> str:
    return "\n".join([
        "<h1>Studios, rehearsal paper, and recitation cards</h1>",
        "<h2>Burglar alarm</h2>",
        "<p>Armed switch \\(A\\), door \\(D\\), window \\(W\\). Siren</p>",
        r"\[ Y = A \cdot (D + W). \]",
        fig(svgs.burglar_alarm(), "Figure S.1 — OR of the contacts, then AND with the armed switch."),
        "<p>If \\(A=0\\) the house stays quiet. Build it in LogiSim and poke all eight rows.</p>",
        "<h2>Final week — mixed drills without a teacher</h2>",
        "<p><strong>Day 1 (logic + network).</strong> Write all seven 2-input tables from a blank page. K-map \\(Y=\\sum m(1,3,5,7)\\) should collapse toward \\(C\\). List OSI layers both ways with one protocol each. Explain HTTPS encapsulation in five sentences.</p>",
        "<p><strong>Day 2 (algorithms + Python).</strong> Trace both sorts on \\(\\{8,3,6,2\\}\\). Binary-search 6 in \\(\\{1..9\\}\\) writing every mid. Code a calculator and a guess game; break them on purpose; read the traceback. Predict: \\(9//2==4\\), \\(9\\%2==1\\), <code>\"Py\" in \"Python\"</code>, <code>not (True and False)</code>.</p>",
        "<p><strong>Day 3 (data + society + literacy).</strong> Draw library, clinic, or bus ER. Write AND vs OR query rows. Irrigation long answer in six labelled sentences. Classify five sources on your phone. Sit the 40-mark paper again. Target 32.</p>",
        "<h2>40-mark rehearsal (60 minutes, closed book)</h2>",
        "<p><strong>A (10×1).</strong> Digital levels? XOR 1 when? First SDLC phase? TCP/IP layer count? Search that needs sorted data? <code>input()</code> type? ER rectangle? Soil dryness device? Your own survey replies? <code>site:</code> does what?</p>",
        "<p><strong>B (6×2).</strong> Analog vs digital · when Waterfall · why binary search fails on {9, 1, 4, 7} · <code>=</code> vs <code>==</code> · referential integrity · NADRA interview vs textbook paragraph.</p>",
        "<p><strong>C (3×6).</strong> Truth table of \\(Y=A'\\cdot B+C\\) plus SOP · Bubble-sort trace of {6, 2, 5, 1} · Sindh irrigation chain naming sensor, link, analytics, AI, actuator, UI.</p>",
        "<p><strong>Scheme A:</strong> two values; different; analysis; 4; binary; str; entity; sensor; primary; restrict domain.</p>",
        "<h2>Recitation cards</h2>",
        "<p><strong>A Gates.</strong> AND all 1s · OR any 1 · NOT flip · NAND not-all-1s · NOR only all 0s · XOR different · XNOR same · rows \\(2^n\\).</p>",
        "<p><strong>B SDLC.</strong> Analyse → Design → Code → Test → Deploy → Maintain (CAPP).</p>",
        "<p><strong>C OSI.</strong> Please Do Not Throw Sausage Pizza Away. ping = ICMP = layer 3.</p>",
        "<p><strong>D Algorithms.</strong> Bubble neighbours · Selection parks min · Linear any list · Binary sorted only · \\(\\mathrm{mid}=\\lfloor(lo+hi)/2\\rfloor\\).</p>",
        "<p><strong>E Python.</strong> input → str · indent 4 · syntax / runtime / logic.</p>",
        "<p><strong>F Data.</strong> PK unique · FK points home · M:N + junction · AND same row · OR different rows.</p>",
        "<p><strong>G Society.</strong> Collect / explain / decide · sensor ≠ actuator · consent · no plagiarism.</p>",
    ])


def html() -> str:
    mjax = """
<script>
window.MathJax = {
  tex: {
    inlineMath: [['\\\\(', '\\\\)'], ['$', '$']],
    displayMath: [['\\\\[', '\\\\]'], ['$$', '$$']],
    processEscapes: true
  },
  svg: { fontCache: 'local', displayAlign: 'center' },
  startup: {
    pageReady: function () {
      return MathJax.startup.defaultPageReady().then(function () {
        document.documentElement.dataset.mathjax = 'ready';
      });
    }
  }
};
</script>
<script src="vendor/tex-svg.js"></script>
"""
    return (
        "<!DOCTYPE html>\n<html lang=\"en\">\n<head>\n"
        "<meta charset=\"utf-8\"/>\n"
        "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\"/>\n"
        "<title>Class XI Computer Science — Teach Yourself Study Guide</title>\n"
        "<style>" + css() + "</style>\n"
        + mjax + "\n</head>\n<body>\n"
        '<section class="cover"><div class="cover-inner">\n'
        '<div class="kicker">SINDH · CLASS XI · COMPUTER SCIENCE</div>\n'
        "<h1>Teach Yourself<br/>Study Guide</h1>\n"
        "<p>An in-depth companion with embedded MathJax notation and SVG diagrams "
        "for Digital Logic, SDLC, Networks, Algorithms, Python, Databases, IoT &amp; AI, "
        "and Digital Literacy.</p>\n"
        '<p class="kicker">Read · Try · Check · Recite · Review</p>\n'
        "</div></section>\n"
        '<header class="bar"><span>Class XI Computer Science · Teach Yourself Study Guide</span>'
        "<span>MathJax + SVG edition</span></header>\n<main>\n"
        "<h1>How to teach yourself with this book</h1>\n"
        '<p class="lead">Companion to the Sindh Textbook Board Class XI Computer Science syllabus — '
        "original explanations, not a reprint. Formulae are typeset with MathJax; circuits, stacks, "
        "and traces are inline SVG.</p>\n"
        "<ol>\n"
        "<li><strong>Read for the map</strong> (ten minutes of headings).</li>\n"
        "<li><strong>Read for the mechanism</strong> — cover a worked line and try it first.</li>\n"
        "<li><strong>Try this now</strong> boxes are mini exams.</li>\n"
        "<li><strong>Recite</strong> the seven gates, six SDLC phases, OSI mnemonic, three error types, four keys.</li>\n"
        "<li><strong>Review</strong> tomorrow, next week, next month.</li>\n"
        "</ol>\n"
        + box("", "KEY IDEA", "Understanding is not recall. Recitation is how professionals keep protocols in their heads.")
        + "<h2>Eight-week plan</h2>\n"
        + table(["Week", "Focus", "Artefact"], [
            ["1", "Unit 1 logic, gates, K-maps", "LogiSim circuit + table"],
            ["2", "SDLC + OSI/TCP-IP", "Waterfall vs Agile from memory"],
            ["3", "Unit 2 sorts", "Two full traces"],
            ["4", "Search + start Python", "Binary search on a register"],
            ["5", "Python control", "Calculator + even/odd"],
            ["6", "Libraries + ER", "ATM or report card; one ER"],
            ["7", "Access + IoT", "Grouped query; irrigation paragraph"],
            ["8", "Literacy + mixed paper", "Mini artefact + rehearsal exam"],
        ])
        + unit1() + unit2() + unit3() + unit4() + unit5() + unit6() + depth() + extras()
        + '<p class="lead">The board paper rewards people who can do a truth table, trace a sort, '
        "write a small program, draw an ER fragment, and judge a source. If you have worked the "
        "amber boxes twice, you are the teacher you were waiting for.</p>\n"
        "</main>\n</body>\n</html>\n"
    )


def main() -> None:
    OUT_HTML.parent.mkdir(parents=True, exist_ok=True)
    OUT_HTML.write_text(html(), encoding="utf-8")
    print("Wrote", OUT_HTML, "(", OUT_HTML.stat().st_size, "bytes)")


if __name__ == "__main__":
    main()
