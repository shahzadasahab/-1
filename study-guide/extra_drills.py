"""Extra worked studios and drills to deepen each unit."""

from reportlab.platypus import PageBreak, Spacer

from pdf_kit import Callout, bullets, code_block, h1, h2, h3, numbered, p, simple_table


def unit1_studio(styles):
    s = styles
    story = [
        h2(s, "1.16 Studio — more traces you should own"),
        h3(s, "Studio A: build Y = (A + B)′ · C from scratch"),
        p(s, "This is a NOR feeding an AND with C. Precedence: parentheses (the OR) first, then NOT, then AND."),
    ]
    story += numbered(s, [
        "Variables A, B, C → 8 rows, binary order.",
        "Helper column 1: A + B.",
        "Helper column 2: (A + B)′  (this is NOR).",
        "Y = that result AND C.",
        "Y is 1 only when A and B are both 0 and C is 1. One minterm: A′B′C.",
        "Diagram: OR(A,B) → bubble (or a NOR symbol) → AND with C → Y.",
    ])
    story += [
        simple_table(
            s,
            ["A", "B", "C", "A+B", "(A+B)′", "Y"],
            [
                ["0", "0", "0", "0", "1", "0"],
                ["0", "0", "1", "0", "1", "1"],
                ["0", "1", "0", "1", "0", "0"],
                ["0", "1", "1", "1", "0", "0"],
                ["1", "0", "0", "1", "0", "0"],
                ["1", "0", "1", "1", "0", "0"],
                ["1", "1", "0", "1", "0", "0"],
                ["1", "1", "1", "1", "0", "0"],
            ],
            col_widths=[55] * 6,
            center_cols=list(range(6)),
        ),
        Spacer(1, 8),
        h3(s, "Studio B: 3-variable K-map with wrap-around"),
        p(s, "Simplify Y = Σm(0, 2, 8, 10). In Gray-code columns BC = 00, 01, 11, 10 the 1s sit at the four corners of the map (cells that wrap left–right and, depending on layout, top–bottom). Those four cells share B′ and C′. A cancels. Result: <b>Y = B′C′</b>. Corner groups are the classic exam trap — if you forget wrap-around you leave four lonely minterms."),
        h3(s, "Studio C: burglar alarm"),
        p(s, "Door sensor D, window sensor W, armed switch A. The siren should sound if the system is armed AND (door OR window is open). Expression: Y = A · (D + W). Gates: OR(D,W) into AND with A. Test mentally: A=0 → always quiet. A=1, D=0, W=0 → quiet. A=1 and either contact open → siren. That is a full short practical."),
        h3(s, "Studio D: protocol-to-layer flash cards"),
        simple_table(
            s,
            ["If you see…", "Think layer", "Why"],
            [
                ["RJ45, Cat6, voltage, fibre pulse", "Physical", "Raw medium"],
                ["MAC, switch, Ethernet frame, CRC", "Data Link", "One LAN hop"],
                ["192.168.1.1, ping, router, OSPF", "Network", "Path across nets"],
                ["Port 443, handshake, segment", "Transport", "Which app, reliability"],
                ["Login session, RPC", "Session", "Conversation life"],
                ["TLS, JPEG, MP3, UTF-8", "Presentation", "Format / secret / size"],
                ["Browser, DNS lookup, SMTP send", "Application", "What the user asked"],
            ],
            col_widths=[200, 90, 205],
        ),
        Spacer(1, 8),
        Callout(s, "try", "Without looking: write the four TCP/IP layer names and the OSI layers each one swallows. Then write one protocol for each TCP/IP layer."),
        h3(s, "Studio E: a one-page Waterfall vs Agile decision"),
        p(s, "A hospital wants a pacemaker firmware update. Requirements are frozen by a regulator; a missed test can kill. Choose Waterfall (or a similarly gated model): late change is a crime, not a Scrum story. A school wants a club-events app “and whatever students ask for next month.” Choose Agile. Write that contrast in your notebook in four lines — it is a complete 4-mark compare question."),
        PageBreak(),
    ]
    return story


def unit2_studio(styles):
    s = styles
    story = [
        h2(s, "2.10 Studio — full traces on paper"),
        h3(s, "Bubble Sort swap diary: {6, 2, 5, 1}"),
        simple_table(
            s,
            ["Pass", "Comparisons and swaps", "List at end of pass"],
            [
                ["1", "6↔2, 6↔5, 6↔1 (three swaps)", "2, 5, 1, 6"],
                ["2", "2&lt;5; 5↔1; 5&lt;6", "2, 1, 5, 6"],
                ["3", "2↔1; 1&lt;5", "1, 2, 5, 6"],
            ],
            col_widths=[55, 250, 190],
        ),
        Spacer(1, 8),
        p(s, "Largest value is parked after pass 1; the array is sorted after pass 3. Comparisons happen even when there is no swap. That is why “already almost sorted” still costs time unless you add a swapped-flag optimisation (nice to know, not required)."),
        h3(s, "Selection Sort diary on the same list"),
        p(s, "Pass 0: min is 1 at the end; one swap with 6 → {1, 2, 5, 6}. If you swap as soon as you see a smaller value (the textbook’s looser cousin), you may swap more than once per pass — count what the version in front of you actually does. Standard selection: find index of min, swap once. Here the rest is already in order, so later passes swap a cell with itself or do nothing. Fewer writes than Bubble Sort’s three-swap first pass."),
        h3(s, "Binary search diary: find 11 in {2, 5, 7, 11, 13, 17, 19}"),
        simple_table(
            s,
            ["low", "high", "mid", "DATA[mid]", "Action"],
            [
                ["0", "6", "3", "11", "Equal — stop, found at index 3"],
            ],
            col_widths=[70, 70, 70, 90, 195],
            center_cols=[0, 1, 2],
        ),
        Spacer(1, 6),
        p(s, "Lucky first hit. Now find 2 (the left edge): mid=3 (11), 2&lt;11 → high=2; mid=1 (5), 2&lt;5 → high=0; mid=0 (2) found. Three looks, not seven. Find 12 (absent): you end with low &gt; high and report “not found.” Write that failure case once so you do not invent a crash in the exam."),
        h3(s, "Tea, language, and a school app — name the strategy"),
        simple_table(
            s,
            ["Move", "Strategy"],
            [
                ["Split “build the app” into login, marks, notices", "Decomposition"],
                ["Every notice has a title, date, body — same shape", "Pattern recognition"],
                ["Ignore button colour when specifying “post a notice”", "Abstraction"],
                ["Write numbered steps before opening VS Code", "Algorithm"],
            ],
            col_widths=[320, 175],
        ),
        Spacer(1, 8),
        Callout(s, "try", "Sort {9, 4, 7, 4, 1} with both algorithms. Watch the two 4s. Bubble Sort (stable) should keep the first 4 ahead of the second. Selection Sort may swap their order. That single observation is an 3-mark “disadvantage of Selection Sort” answer."),
        PageBreak(),
    ]
    return story


def unit3_studio(styles):
    s = styles
    story = [
        h2(s, "3.15 Studio — programs to type until they feel boring"),
        h3(s, "Program 1 — guarded calculator"),
        code_block(
            s,
            """a = float(input("First number: "))
b = float(input("Second number: "))
op = input("Choose + - * / : ").strip()
if op == "+":
    print(a + b)
elif op == "-":
    print(a - b)
elif op == "*":
    print(a * b)
elif op == "/":
    if b == 0:
        print("Cannot divide by zero.")
    else:
        print(a / b)
else:
    print("Unknown operator.")""",
        ),
        p(s, "Notice the nested if inside division. That is selection inside selection — Unit 3’s nested-if idea in a useful costume."),
        h3(s, "Program 2 — one-shot guess"),
        code_block(
            s,
            """import random
secret = random.randint(1, 10)
guess = int(input("Guess 1 to 10: "))
if guess == secret:
    print("You win")
else:
    print("You lose. It was", secret)""",
        ),
        h3(s, "Program 3 — ATM skeleton (the textbook activity)"),
        code_block(
            s,
            """PIN = "1234"
balance = 10000.0
tries = 3
ok = False
while tries > 0 and not ok:
    entered = input("Enter PIN: ")
    if entered == PIN:
        ok = True
    else:
        tries -= 1
        print("Wrong PIN!", tries, "attempt(s) left.")
if not ok:
    print("Card locked.")
else:
    print("Login Successful!")
    running = True
    while running:
        print("1 Check  2 Deposit  3 Withdraw  4 Exit")
        choice = input("Choose (1-4): ")
        if choice == "1":
            print(f"Balance: Rs. {balance:.2f}")
        elif choice == "2":
            amt = float(input("Deposit: "))
            if amt > 0:
                balance += amt
                print(f"New balance: Rs. {balance:.2f}")
        elif choice == "3":
            amt = float(input("Withdraw: "))
            if 0 < amt <= balance:
                balance -= amt
                print(f"Remaining: Rs. {balance:.2f}")
            else:
                print("Rejected.")
        elif choice == "4":
            running = False
            print("Thank you! Goodbye.")
        else:
            print("Choose 1-4.")""",
        ),
        p(s, "This is sequence (start values) + selection (menu) + repetition (PIN loop, menu loop) + bool flags. If you can modify it — add a transfer, or a 20-try lockout — you own the unit."),
        h3(s, "Dry-run table for a while-loop bug"),
        p(s, "The textbook’s infinite loop: i = 1; while i &lt; 6: print(i); i -= 1. Trace: 1, 0, −1, −2… i never reaches 6. That is a logical error: the program is legal and will run until you kill it. Fix: i += 1. Always ask of a while loop: “What makes the condition False, and does every path reach it?”"),
        h3(s, "Bitwise pocket sheet"),
        p(s, "10 is 1010. 6 is 0110. Line them up. AND keeps the second column only → 0010 = 2. OR keeps every column that has a 1 → 1110 = 14. XOR keeps columns that disagree → 1100 = 12. Left shift 5 (0101) by 2 → 10100 = 20, which is 5×4. If a question shows bin() output 0b1010, the 0b prefix is notation, not part of the value."),
        PageBreak(),
    ]
    return story


def unit4_studio(styles):
    s = styles
    story = [
        h2(s, "4.14 Studio — design on paper before Access"),
        h3(s, "Clinic schema (you invent this in 15 minutes)"),
        p(s, "A small clinic stores patients, doctors, and appointments. A patient may see many doctors over time; a doctor sees many patients; each visit has a date and a fee. That is M:N between Patient and Doctor, resolved as Appointment(AppointmentID PK, PatientID FK, DoctorID FK, VisitDate, Fee). Patient(PatientID, Name, Phone). Doctor(DoctorID, Name, Speciality). Referential integrity: you cannot book Patient 88 if that id is missing. Cascade delete of a doctor is dangerous (history vanishes) — better to forbid the delete or mark the doctor inactive. Writing that caution is a mature 3-mark answer."),
        h3(s, "Shop: 1:M without a junction"),
        p(s, "Customer 1—M Order. Order holds CustomerID as FK. You do <i>not</i> need a junction because one order belongs to one customer. Students over-use junction tables. Use them only when both sides are truly many."),
        h3(s, "Access query recipes"),
        simple_table(
            s,
            ["Need", "Design grid"],
            [
                ["CS students only", "Department Criteria: \"Computer Science\""],
                ["IT or CS", "Department Criteria: \"IT\"  /  or: \"Computer Science\""],
                ["Aslam in IT", "Name and Department on the SAME criteria row"],
                ["Headcount per dept", "Totals on; Department Group By; StudentID Count"],
                ["Average marks per dept", "Department Group By; Marks Avg"],
            ],
            col_widths=[150, 345],
        ),
        Spacer(1, 8),
        p(s, "AND is horizontal (one row). OR is vertical (criteria / or). Recite that until it is muscle memory — it is the usual practical-exam discriminator."),
        Callout(s, "try", "On paper, design fields for a college bus system: Bus, Route, Student. Decide keys and cardinalities. Hint: a bus serves one route (or many trips); many students ride many buses across a week — that last link may need a Ride junction with a date."),
        PageBreak(),
    ]
    return story


def unit5_studio(styles):
    s = styles
    story = [
        h2(s, "5.13 Studio — long answers you can reuse"),
        h3(s, "The smart-home paragraph (memorise the skeleton, not the sentences)"),
        p(s, "A temperature sensor measures the room (IoT / sensor). The reading travels over Wi-Fi (connectivity) to a hub or cloud (processing / cloud). Analytics compares it with the user’s set-point. AI or a simple rule decides “too hot.” An actuator starts the fan. The phone app (UI) shows 31 °C and a power-use graph. If the Wi-Fi dies, the chain breaks — that single failure sentence shows you understand dependency."),
        h3(s, "Source courtroom"),
        simple_table(
            s,
            ["Exhibit", "Verdict", "Reason"],
            [
                ["Your interview with the librarian", "Primary source / primary data", "You were there"],
                ["PBS graph of literacy rates", "Secondary source; secondary data for you", "Already processed"],
                ["Wikipedia lead paragraph", "Tertiary; use only to start", "Digest of other writing"],
                ["Anonymous “forward this” image", "Unreliable", "No author, date, or evidence"],
                ["Government .gov.pk PDF, 2024", "Usually reliable secondary", "Named institution, dated"],
            ],
            col_widths=[180, 140, 175],
        ),
        Spacer(1, 8),
        h3(s, "Impact paragraph formula"),
        p(s, "Field + one concrete help + one concrete harm + one responsible action. Example: “In education, recorded lessons let a student replay a proof (help), but six-hour screen days blunt attention (harm). A responsible student uses the recording for the hard ten minutes, then walks.” Four sentences, full marks on a 4-mark impact item."),
        h3(s, "Assistive tech — one career bridge"),
        p(s, "NVDA reads a website aloud. An inclusive UX designer writes alt text and keyboard routes so that reader has a path. The skill mix is code + empathy, not pity. If an exam asks “importance,” hit education access, communication, independence, work, and social life — five short bullets."),
        PageBreak(),
    ]
    return story


def unit6_studio(styles):
    s = styles
    story = [
        h2(s, "6.12 Studio — run a 90-minute mini inquiry"),
        p(s, "Do this once for real. It is the unit. Everything else is commentary."),
    ]
    story += numbered(s, [
        "Question (5 min): pick one — smartphone use in college / online exams / weekend internet hours.",
        "Search (15 min): two advanced queries, keep two sources that pass the author-date-evidence test. Write why you kept them.",
        "Instrument (15 min): eight questions, mix of closed and open. No CNIC, no phone number.",
        "Sample (20 min): 15+ classmates, permission first.",
        "Sheet (15 min): enter, average, percent, one bar or pie.",
        "Artefact (20 min): five slides or one infographic using the ten-heading skeleton. One recommendation aimed at a real audience (principal, parents, or students).",
    ])
    story += [
        Callout(s, "exam", "If the paper asks you to “design a data-collection approach,” they want steps 1–8 from §6.5, not a speech about how important research is. Method marks live in sample, tool, and ethics."),
        h3(s, "Bias checklist (write these in the margin of every form)"),
    ]
    story += bullets(s, [
        "Leading item: “How badly does the phone ruin your grades?” — already accuses.",
        "Only your friend group — sample bias.",
        "Only closed questions when you promised to explain “why.”",
        "Chart with a truncated axis that exaggerates a tiny difference.",
        "Secondary PDF from 2009 used as if it were this year’s Pakistan.",
    ])
    story += [
        p(s, "Fair wording, a mixed sample, a named date on every secondary source, and an honest visual — that is digital literacy as a practice, not a slogan."),
        PageBreak(),
    ]
    return story


def closing_week(styles):
    s = styles
    story = [
        h1(s, "Final week — mixed drills without a teacher"),
        h2(s, "Day 1 (logic + network)"),
    ]
    story += bullets(s, [
        "Write all seven 2-input tables from a blank page.",
        "K-map: Y = Σm(1,3,5,7) → should collapse toward C (check your Gray order).",
        "List OSI layers upward and downward. Add one protocol each.",
        "Explain encapsulation of HTTPS in five sentences.",
    ])
    story += [
        h2(s, "Day 2 (algorithms + Python)"),
    ]
    story += bullets(s, [
        "Trace both sorts on {8, 3, 6, 2}.",
        "Binary-search 6 in {1,2,3,4,5,6,7,8,9}; write every mid.",
        "Code the calculator and the guess game; break them on purpose; read the traceback.",
        "Predict True/False: 9//2==4, 9%2==1, \"Py\" in \"Python\", not (True and False).",
    ])
    story += [
        h2(s, "Day 3 (data + society + literacy)"),
    ]
    story += bullets(s, [
        "ER: library, clinic, or bus — boxes, keys, one M:N resolved.",
        "Write AND vs OR query rows.",
        "Irrigation long answer in six labelled sentences.",
        "Classify five sources you actually have on your phone.",
        "Sit the 40-mark paper again. Target 32.",
    ])
    story += [
        Callout(s, "why", "A teach-yourself course fails at the last mile: people reread highlights instead of producing traces. The days above produce traces. That is the whole method."),
        PageBreak(),
    ]
    return story
