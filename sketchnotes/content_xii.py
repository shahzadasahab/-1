"""Complete CS XII sketchnote content — all 6 chapters, all relevant details."""

from engine import GOLD, TEAL, CORAL, NAVY, SAGE, SKY, LAV, AMBER, ROSE, MUTED
import diagrams as d


def build(doc):
    doc.cover(
        "Computer Science XII",
        [
            "HCI — interaction, accessibility, UI/UX, Figma, testing",
            "Algorithms & Data Structures — traces, Big O, linear / non-linear",
            "Programming — lists tuples sets dicts, functions, files, exceptions",
            "Data Analysis — SQLite, Pandas, Matplotlib, descriptive stats",
            "Impacts — ML / NN / DL, security, equity in collaboration",
            "Digital Entrepreneurship — prototype, MVP, beachhead, ethics",
        ],
        "Bilingual Teacher's Edition  ·  New Sindh Curriculum 2024 / 2025–27",
        [
            "Source followed: CS XII lecture notes (Ch 1–6). ★ = highly critical for examinations.",
            "Every definition, table, algorithm, worked example, case study, rubric and career note is kept.",
            "English exam track is complete; Urdu in the source is the parallel teacher translation.",
        ],
    )
    doc.toc_page([
        (1, "Computer Systems (HCI)", [
            "Traditional vs natural", "HCI domains ★", "Components + 10 interaction types",
            "UI / environment / feedback", "Importance ★ accessibility",
            "Need analysis", "Problems ★ + improve", "UI vs UX ★ Figma", "Eval + testing ★",
        ]),
        (2, "Computational Thinking & Algorithms", [
            "Trace tables ★ vs stepwise", "Modularity + readability",
            "Big O ★ conditions + loops", "Refine clarity/speed",
            "Array list stack queue tree graph ★", "Pick + trace retrieval",
        ]),
        (3, "Programming Fundamentals", [
            "Lists ★ tuples ★ sets dicts ★", "Attendance + word-freq activities",
            "Functions ★ scope", "Files r/w/a ★ with", "try/except + grade tracker",
        ]),
        (4, "Data and Analysis", [
            "DB connection 5 parts ★", "SQLite 9 steps",
            "Pandas DataFrame ★ NaN ★", "6 graph types ★", "Mean median mode + spread ★",
        ]),
        (5, "Application & Impacts", [
            "ML / NN ★ / DL", "NN components ★", "8 applications",
            "Secure collab + protect ★", "Threats + mitigate ★", "Equity vs equal access ★",
        ]),
        (6, "Entrepreneurship in the Digital Age", [
            "Problem → idea", "Prototype types ★ cycle ★",
            "Homework Helper activity", "MVP ★ vs prototype",
            "Riskiest assumption", "Canteen case", "Beachhead ★ project + rubric",
        ]),
    ])
    ch1(doc)
    ch2(doc)
    ch3(doc)
    ch4(doc)
    ch5(doc)
    ch6(doc)


# =====================================================================
# CHAPTER 1  HCI
# =====================================================================
def ch1(doc):
    doc.chapter_open(
        1, "Computer Systems (HCI)",
        "HCI is the design of technology that serves people — easy, efficient, responsive. Also called CHI (Computer-Human Interface) or MMI (Man-Machine Interaction).",
        [
            "Name five sensory channels and contrast traditional vs natural interaction.",
            "Give HCI examples in health, banking, education, networking.",
            "List HCI components and ten interaction types.",
            "Define GUI/CLI/touch/VUI/NUI, environment, system vs user feedback.",
            "State five importance implications and five accessibility principles.",
            "Run need analysis; name HCI problems and eight improvement methods.",
            "Separate UI from UX; Lo-Fi vs Hi-Fi; Figma prototype triggers.",
            "SUS, NPS, formative/summative; usability, A/B, load, a11y walkthroughs.",
        ],
    )
    doc.h1("1.1 Fundamentals of Human-Computer Interaction")
    doc.p("HCI is the fundamental design of technology to serve people: easy to use, efficient, and responsive to human needs. Also known as CHI or MMI.")
    doc.h3("Sensory channels of interaction")
    doc.table(
        ["Channel", "How humans use it", "How computers respond"],
        [
            ["Sight (بصارت)", "Look at screens, graphics, videos.", "Displays visuals on monitors/screens."],
            ["Touch (چھونا)", "Tap, type, or swipe.", "Clicks or vibrations (haptics)."],
            ["Hearing (سننا)", "Listen to sounds or voices.", "Audio feedback via speakers."],
            ["Voice (آواز)", 'Speak commands (e.g. "Alexa").', "Processes speech and replies."],
            ["Spatial (مکانی)", "Move in physical space.", "Tracks position / body (VR)."],
        ],
        col_fracs=[1.1, 1.6, 1.7],
    )
    d.sensory_hci(doc)

    doc.h1("1.1.1 Traditional vs 1.1.2 Natural Interaction")
    doc.compare(
        "Traditional interaction",
        [
            "Everyday devices with standard I/O.",
            "Computer: mouse + keyboard in; monitor + speakers out.",
            "Smartphone: tap/swipe in; screen light + vibration out.",
            "Today: TV remote, ATM keypad.",
        ],
        "Natural interaction",
        [
            "Advanced tech — no mouse/keyboard. Feels more human.",
            'Voice: "Alexa, play a song."',
            "Body & gesture: FaceID; VR by waving hands.",
            "Today: FaceID, Siri, Kinect games.",
        ],
        NAVY, ROSE,
    )
    doc.callout("tip", "Class discussion",
                "List 3 traditional interfaces you used today and 3 natural ones.")

    doc.h1("1.2 Applications of HCI", golden=True)
    doc.p("HCI designs interactive systems — desktop, web, mobile — as human-centred solutions across domains.")
    doc.table(
        ["Domain", "Application examples", "User benefit"],
        [
            ["Health care", "Patient portals, telemedicine, assistive tech.", "Remote access to medical services."],
            ["Banking", "Mobile banking, secure ATM UIs.", "Quick, secure transactions."],
            ["Education", "E-learning LMS, online exam portals.", "Better teaching, learning, engagement."],
            ["Networking & comms", "Social media, WhatsApp, Zoom.", "Global collaboration."],
        ],
        col_fracs=[1.1, 1.8, 1.6],
    )

    doc.h1("1.3 Components of HCI")
    doc.cards([
        ("Users",
         "Anyone who interacts to achieve goals. End users operate the system (beginner→expert). Stakeholders care about the outcome (managers, clients)."),
        ("The computer / platform",
         "Where humans and computers communicate via input, output and feedback. Connects actions to machine responses."),
        ("Interaction",
         "User communicates by clicking, tapping, typing, speaking. Intent becomes a system response. Types on the next cards."),
        ("iv) Task (کام)",
         "The specific action (book a ticket). Complexity (form vs 3D model). User knowledge (typing vs programming). Time (ATM vs passport app)."),
    ], cols=1)

    doc.h2("Types of user interaction")
    doc.table(
        ["Type", "Description", "Examples"],
        [
            ["Direct manipulation", "Handle digital objects like physical ones.", "Drag files; pinch-zoom images."],
            ["Command-based", "Precise typed instructions.", "MS-DOS, Linux (dir, cd)."],
            ["Menu-driven", "Pick from predefined lists.", '"Start Test", "Download".'],
            ["Form fill", "Structured blanks.", "Sign-up, ticket booking."],
            ["Conversational", "Natural language, text or voice.", "Chatbots, ChatGPT, Google Assistant."],
            ["Gesture-based", "Body or hand movements.", "Swipe; VR hands."],
            ["Voice", "Spoken commands.", '"Call Aslam" on a phone.'],
            ["Context-aware", "Environment sensed; acts without a prompt.", "Smart lights on as you enter."],
            ["Biometric", "Biological features for auth.", "Fingerprint, FaceID."],
            ["Haptic & tactile", "Physical confirmation.", "Phone vibrates while typing."],
            ["Multimodal", "Two or more types together.", "Voice + tap a search."],
        ],
        col_fracs=[1.2, 1.7, 1.5],
    )

    doc.h2("Interfaces, environment & feedback")
    doc.h3("v) User interface (UI) — the medium")
    doc.cards([
        ("GUI", "Windows, icons, menus. Windows OS, Android."),
        ("CLI", "Text typing. MS-DOS, Linux terminal."),
        ("Touch", "Tap, swipe, pinch. Phones, tablets."),
        ("VUI", "Spoken commands. Smart speakers."),
        ("NUI", "Gestures, body, immersive. VR, Kinect."),
    ], cols=1)
    doc.cards([
        ("vi) Environment",
         "Real-world setting. Physical (ATM in sunlight), social (quiet classroom), technical hardware."),
        ("vii) Feedback",
         "System feedback: Loading bar, “Message Sent!” tick, error sound. User feedback: Submit tap, 5-star rating."),
    ])

    doc.h1("1.4 Importance of HCI", golden=True)
    doc.p("Good design makes tech simple and enjoyable (touchscreens). Poor design causes confusion and risk (unclear medical-device buttons).")
    doc.table(
        ["Implication", "Description"],
        [
            ["1. Enhance productivity", "Faster work, fewer mistakes, goals hit efficiently."],
            ["2. Promotes inclusivity", "Screen readers and voice commands for equal use."],
            ["3. Drives innovation", "AR/VR, AI, IoT only get adopted if HCI is solid."],
            ["4. Economic impact", "Friendly products → adoption, loyalty, profit."],
            ["5. Ethical responsibility", "Respect privacy, reduce bias, support well-being."],
        ],
        col_fracs=[1.3, 2.7],
    )

    doc.h1("1.5 Accessibility Principles")
    doc.p("Guidelines so digital systems work for ALL — diverse physical, sensory and cognitive abilities. Remove barriers for equal access.")
    doc.cards([
        ("1. High contrast (واضح رنگ)",
         "Text/pictures stand out. Black on white in a railway app — readable in bright sun."),
        ("2. Readable fonts (آسان تحریر)",
         "Clear, simple, sized, spaced. School site in large Calibri for homework."),
        ("3. Colour-blind friendly",
         "Never colour alone — add symbols/labels. Traffic app: red circle + STOP, not just red."),
        ("4. Inclusive navigation (آسان نیویگیشن)",
         "Many ways to move. Tab-key between buttons if you cannot use a mouse."),
        ("5. Multimodal detection (متعدد حسی ذرائع)",
         "Sight + sound + touch. Captions on video; phone vibrates to alert."),
    ], cols=1)

    doc.h1("1.6 Need Analysis for Interface Design")
    doc.p("Find the gap between the current situation and the desired outcome — BEFORE designing a UI. Goals, tasks, abilities, expectations.")
    doc.numbered([
        "Identify the users (elderly? teenagers?).",
        "Collect information — interviews, questionnaires, observation.",
        "Analyse user needs — core problems, goals, requirements.",
        "Prioritise — which features first?",
        "Develop solutions that meet verified needs.",
    ])
    doc.callout("case", "Mobile banking app",
                "Interviews found: fingerprint/FaceID login; elderly need large buttons and simple nav; English + local languages. UI is built around those proven needs.")

    doc.h1("1.7 Human-Computer Interaction Problems", golden=True)
    doc.p("Difficulties that stop smooth use — the system misses human needs or cognitive limits.")
    doc.table(
        ["Problem", "Explanation & example"],
        [
            ["Interface complexity", "Too many options / confusing layout. Shopping app: cannot find Checkout."],
            ["Poor feedback", "No sign that an action worked. Submit freezes with no confirmation."],
            ["Inconsistency", "Different look/act. Magnifying glass = Search on one page, binoculars on another."],
            ["Accessibility gaps", "Ignores disability. Video tutorials with no captions."],
            ["Compatibility issues", "Fails on some devices/browsers. Fine on laptop, crashes on mobile."],
            ["Contextual neglect", "Ignores situation. Map app with no dark mode blinds a night driver."],
            ["High cognitive load", "Too much to memorise. Registration wants three SMS codes at once."],
            ["Trust deficiency", "Feels unsafe. Store asks for a card with no HTTPS lock."],
        ],
        col_fracs=[1.3, 2.7],
    )

    doc.h1("1.8 Methods for Improving HCI")
    doc.bullets([
        "Enhance usability — clear “Buy Now”.",
        "Strengthen accessibility — captions.",
        "Ensure consistency — same Save button everywhere.",
        "Provide clear feedback — “Payment Successful”.",
        "Improve adaptability — responsive to mobile.",
        "Apply User-Centred Design (UCD) — real goals + pilot tests.",
        "Use multimodal input — touch + voice + gesture.",
        "Continuous testing — update from feedback.",
    ])

    doc.h1("1.9 User Interface Design (UI)", golden=True)
    doc.p("Create and organise visual elements so users interact easily and efficiently.")
    doc.h3("1.9.1 UI components")
    doc.cards([
        ("Buttons", "Clickable actions — Submit, Cancel."),
        ("Menus", "Lists for navigating."),
        ("Icons", "Small symbols for tools/actions."),
        ("Text fields", "Typed info — passwords, search."),
        ("Checkboxes / radio", "Select options on a form."),
        ("Sliders", "Values along a bar — volume, brightness."),
    ])
    doc.h3("1.9.2 User Experience (UX)")
    doc.p("The overall experience — how smooth, comfortable and satisfying it feels.")
    doc.callout("memory", "UI is what you see; UX is how it feels",
                "Food-delivery app: UI = burger photos and red buttons. UX = fast load, tracking works, food arrives without frustration.")

    doc.h2("1.9.3 Wireframing")
    doc.p("A basic visual outline / blueprint BEFORE final design — structure without colours or polish.")
    doc.compare(
        "Low-fidelity (Lo-Fi)",
        ["Black-and-white sketch — boxes and lines.",
         "Early, fast, shareable.", "Pure structure and flow."],
        "High-fidelity (Hi-Fi)",
        ["Almost the final product.",
         "Real colours, fonts, images, clickable buttons.",
         "Used for final user testing."],
        MUTED, LAV,
    )
    doc.flow(["Lo-Fi sketch", "Add details", "Hi-Fi prototype (logo, login)"])

    doc.h2("1.10 Figma & 1.9.5 Prototypes")
    doc.p("Figma is a popular, free, web-based tool for UI and prototypes. It runs in the browser.")
    doc.numbered([
        "Sign up — open a Figma workspace.",
        "Create Frames (Frame tool, e.g. iPhone size) as the canvas.",
        "Add shapes — rectangles for buttons, circles for avatars.",
        "Add text labels (“Sign Up”).",
        "Duplicate the frame for the next screen (Home).",
    ])
    doc.p("A prototype is an early interactive model used before writing real code. In Figma’s Prototype tab you link screens: Trigger = On Tap; Action = Navigate to Home. Real users click the fake app to see if navigation makes sense.")

    doc.h1("1.11 Test and Evaluate HCI")
    doc.p("Testing checks if the product works (bugs). Evaluation checks if it meets user needs (usability). Together they improve the product before release.")
    doc.h3("1.11.1 Evaluation methods")
    doc.table(
        ["Method", "Description"],
        [
            ["SUS (System Usability Scale)", "Standard 10-item questionnaire → a usability score."],
            ["NPS (Net Promoter Score)", '"How likely to recommend to a friend?" — loyalty.'],
            ["Formative evaluation", "During development — early feedback, continuous improve."],
            ["Summative evaluation", "At the end — success against original goals."],
            ["Expert reviews", "Specialists score the app against heuristics."],
        ],
        col_fracs=[1.5, 2.5],
    )

    doc.h2("1.11.2 Testing methods", golden=True)
    doc.cards([
        ("1. Usability testing",
         "Watch real users do realistic tasks. If they get stuck, you know what to fix."),
        ("2. Task-based testing",
         '"Find a product and add to cart." Measure completion time, success rate, errors. e.g. Time 12 s, Success Yes.'),
        ("3. Automated audits",
         "Bots scan for broken links, slow pages, low contrast."),
        ("4. A/B testing",
         "Half see version A, half see B. More clicks/sign-ups wins."),
        ("5. Compatibility testing",
         "Chrome/Safari, phones/tablets/PCs, different OS."),
        ("6. Performance & load",
         "Simulate 10,000 logins at once — does speed drop or the server die?"),
        ("7. Keyboard & screen-reader",
         "Navigate with only Tab/Enter or a screen reader — accessibility compliance."),
    ], cols=1)

    doc.h2("Careers in UI/UX")
    doc.cards([
        ("UX designer", "Research needs so the app is intuitive."),
        ("UI designer", "Visual layout in Figma — colour, type, buttons."),
        ("Interaction designer", "Flow, animation, gestures."),
        ("Usability researcher", "SUS / NPS / A/B with real users."),
        ("Accessibility specialist", "Inclusive standards for disability."),
    ], cols=1)
    doc.summary([
        "HCI = human-centred tech. Channels: sight, touch, hearing, voice, spatial.",
        "Traditional = mouse/keyboard. Natural = voice/gestures.",
        "Accessibility: contrast, fonts, not-colour-only, inclusive nav, multimodal.",
        "UI = visuals; UX = feeling + efficiency.",
        "Lo-Fi = structure; Hi-Fi = realistic prototype. Figma links screens.",
        "SUS/NPS measure usability; A/B compares; audits find broken links; load tests the server.",
    ])


# =====================================================================
# CHAPTER 2
# =====================================================================
def ch2(doc):
    doc.chapter_open(
        2, "Computational Thinking & Algorithms",
        "XII raises the bar: prove an algorithm is correct, make it readable, measure it with Big O, then pick the right data structure and trace how data comes back out.",
        [
            "Build a trace table and a stepwise-reasoning argument.",
            "Evaluate modularity (SRP, coupling, abstraction) and readability.",
            "Name O(1), O(log n), O(n), O(n²) and the three efficiency questions.",
            "Refine names, modules, loops, memoization.",
            "Define array, list, stack (LIFO), queue (FIFO), tree, graph + five operations.",
            "Match a scenario to a structure; trace array / list / queue retrieval.",
        ],
    )
    doc.h1("2.1 Analyse algorithms for correctness")
    doc.p("Correct means output matches expected results for a given input — consistently, for all valid inputs. Two methods: Trace Tables and Stepwise Reasoning.")

    doc.h2("2.1.1 Trace tables", golden=True)
    doc.p("Monitor how variables change during execution — a paper execution, dry run, or manual walkthrough.")
    doc.cards([
        ("Purpose",
         "Dry running (be the computer, line by line). Debugging (logical errors — runs but wrong). Validation (does what was intended)."),
        ("Components",
         "Line number. A column per variable. Input/output columns. Condition check (IF, WHILE, FOR)."),
    ])
    doc.h3("Example — eligible soldiers (height 1.57–1.91 m inclusive)")
    doc.code(
        """Step 1: Start
Step 2: SET Total = 0
Step 3: Set AllHeights = [1.91, 2.01, 1.87, 1.57, 1.48]
Step 4: FOR EACH height FROM AllHeights DO
Step 5:   IF height >= 1.57 AND height <= 1.91 THEN
Step 6:     SET Total = Total + 1
Step 7:   END IF
Step 8: END FOR EACH
Step 9: Print Total
Step 10: End""",
        title="Inputs = all heights; Output = count of eligible soldiers",
    )
    doc.table(
        ["Step", "Total", "Height", "Condition 1.57–1.91"],
        [
            ["2", "0", "—", "—"],
            ["3", "0", "list loaded", "1.91, 2.01, 1.87, 1.57, 1.48"],
            ["4–6", "1", "1.91", "True"],
            ["4–5", "1", "2.01", "False — skip +1"],
            ["4–6", "2", "1.87", "True"],
            ["4–6", "3", "1.57", "True (inclusive)"],
            ["4–5", "3", "1.48", "False — skip"],
        ],
        col_fracs=[0.7, 0.7, 1, 1.8],
    )

    doc.h2("2.1.2 Stepwise reasoning")
    doc.p("Break the algorithm into logical sections and verify the state at each stage — logic verification, not a row-by-row table.")
    doc.numbered([
        "Analyse each step.",
        "Does it start in a valid state?",
        "Does it handle all cases?",
        "Are conditions correct?",
        "If the loop is correct at the start of an iteration, is it still correct at the end?",
    ])
    doc.h3("Sum of 1..N")
    doc.code(
        """Input N
SET Sum = 0
For i = 1 to N
    Sum = Sum + i
END For
Print Sum""",
        title="Reasoning, not a 1000-row table",
    )
    doc.bullets([
        "Initial: Sum = 0 — valid.",
        "Loop runs exactly 1 to N.",
        "Each i is added.",
        "Final Sum is the total.",
        "Edge: N=0 → loop never runs, Sum stays 0 (correct). N=5 → 15 (correct).",
    ])

    doc.h2("2.1.3 Trace table vs stepwise reasoning")
    doc.table(
        ["Feature", "Trace table", "Stepwise reasoning"],
        [
            ["Best for", "Small blocks, complex loops, beginners tracking variables.",
             "Large systems, architecture, abstract proofs."],
            ["Effort", "High — hopeless if a loop runs 1,000 times.",
             "Moderate — needs logical deduction."],
            ["Primary goal", "Catch arithmetic / line-by-line errors.",
             "Catch conceptual / structural flaws."],
            ["Level", "Micro (line by line, exact values)", "Macro (logic blocks, overall state)"],
        ],
        col_fracs=[1, 1.7, 1.8],
    )

    doc.h1("2.2 Evaluating the Clarity of an Algorithm")
    doc.p("Easy to read, understand and modify. Often more important than raw speed — clearer code is easier to maintain, debug and extend. Two axes: Modularity and Readability.")
    doc.h2("2.2.1 Modularity")
    doc.p("Break into smaller independent parts — functions, classes, modules.")
    doc.numbered([
        "Single Responsibility Principle (SRP) — each module does ONE task.",
        "Coupling — loose coupling: change one part without breaking others; reuse in new contexts.",
        "Abstraction — hide implementation. Call sort() without knowing Bubble vs Selection.",
    ])
    doc.compare(
        "Poor — one monoblock",
        ["All logic in one block.",
         "Set A, n, total, avg; loop add; avg = total/n; print.",
         "Hard to reuse or test."],
        "Good — functions",
        ["FindAverage(A, n) calls CalculateSum(A, n).",
         "Main only prints FindAverage(A, n).",
         "Each function has one job."],
        CORAL, SAGE,
    )
    doc.h2("2.2.2 Readability")
    doc.p("Another person can understand purpose and logic without running it.")
    doc.cards([
        ("1. Naming", 'Bad: v = d / t.  Good: velocity = distance / time.'),
        ("2. Self-documentation", "Clear enough to explain itself — fewer comments needed."),
        ("3. Simple control flow", "Avoid IF inside IF inside IF. One-task functions."),
        ("4. Consistency", "Indentation, spacing, camelCase or snake_case throughout."),
    ])

    doc.h1("2.3 Assess Algorithm Efficiency", golden=True)
    doc.p("Efficiency = time (how fast) + space (how much memory), as input size n grows.")
    doc.h2("2.3.1 Number of steps — Big O Notation")
    doc.cards([
        ("O(1)  Constant  — excellent",
         "Same time for 10 items or 10 million. Example: arr[0]."),
        ("O(n)  Linear  — fair",
         "Double n, double time. Example: linear search on an unsorted list."),
        ("O(log n)  Logarithmic  — excellent",
         "Grows very slowly; halves the problem each step. Example: binary search on a sorted list."),
        ("O(n²)  Quadratic  — poor",
         "Nested loops. Time ~ n squared. Bubble Sort; compare every item with every other."),
    ])
    doc.h3("2.3.2 Number of conditions")
    doc.bullets([
        "Every IF costs a true/false evaluation.",
        "Nested IF = brute force — hurts readability and speed.",
        "Short-circuit: stop AND/OR as soon as the result is known.",
    ])
    doc.h3("2.3.3 Number of repetitions")
    doc.table(
        ["Type", "Impact", "Grade"],
        [
            ["Linear loop", "Each element once. Time ∝ size.", "Good  O(n)"],
            ["Logarithmic repetition", "Halves each time (binary search).", "Excellent  O(log n)"],
            ["Nested loops", "For each element, process all others. Explodes.", "Poor  O(n²)"],
        ],
        col_fracs=[1.3, 2, 1],
    )
    doc.h3("2.3.4 Efficiency evaluation framework")
    doc.numbered([
        "Does it scale? 10× input → 10× time (linear) or 100× (quadratic)? Quadratic dies on large n.",
        "What is the bottleneck? Usually the deepest loop — optimise that.",
        "Is the cost worth it? O(log n) can be harder to maintain. For 50 items, simple O(n) linear search is practically better.",
    ])

    doc.h1("2.4 Refinements")
    doc.h3("Improve clarity")
    doc.cards([
        ("Meaningful names", "average = totalSum / totalItems  not  a = b / c."),
        ("Break into modules", "CalculateSum() separate from printing."),
        ("Structure & indentation", "Packed loops without spacing are unreadable."),
        ("Comments", "Short. Explain WHY, not the obvious WHAT."),
    ])
    doc.h3("Improve efficiency")
    doc.cards([
        ("Reduce unnecessary steps",
         "After Bubble Sort’s first pass the largest is parked — shrink the inner loop."),
        ("Use a better algorithm",
         "1 million sorted records: Binary instead of Linear (seconds → milliseconds)."),
        ("Avoid re-computing",
         "If C = A+B is fixed, compute it ONCE outside the loop (memoization / caching)."),
        ("Right data structure",
         "Direct access → Array. Hierarchy → Tree. Do not force one structure everywhere."),
    ], cols=1)
    doc.code(
        """# BAD — C recomputed N times
For i = 1 to N
    C = A + B
    Print C * i
# GOOD
C = A + B
For i = 1 to N
    Print C * i""",
        title="Hoist the invariant",
    )

    doc.h1("2.5 Concept of Data Structure", golden=True)
    doc.p("A systematic way of organising, storing and managing data for efficient access, modification and processing.")
    doc.callout("analogy", "Shelf and folders",
                "Books in order are easy to find. Files in folders are grouped. Data structures do the same in memory.")
    doc.compare(
        "Linear",
        ["Strict sequence, one after another.",
         "Each item (except ends) has one predecessor and one successor.",
         "Array, Linked List, Stack, Queue."],
        "Non-linear",
        ["Hierarchy or a network.",
         "One element can connect to many others.",
         "Tree, Graph."],
        SKY, LAV,
    )

    doc.h2("2.5.1 Linear — Array")
    doc.p("Similar items, contiguous memory, same type. Index usually from 0 — jump directly (direct access). A = [23, 76, 12, 90, 34, 68] → A[3] = 90.")
    doc.callout("warn", "Limitation",
                "Insert in the middle → shift everything right. Fast to read by index, inflexible to insert.")

    doc.h3("Linked list")
    doc.p("Chain of nodes scattered in memory — not one block. Each node: Data + Link (address of next).")
    d.linked_list(doc)
    doc.p("Real life: browser Back follows the pointer to the previous page.")

    doc.h3("Stack", golden=True)
    doc.p("LIFO — Last-In, First-Out. PUSH adds on top. POP removes from top. Cannot pull from the middle.")
    doc.h3("Queue", golden=True)
    doc.p("FIFO — First-In, First-Out. ENQUEUE at Rear. DEQUEUE from Front.")
    d.stack_queue(doc)

    doc.h2("2.5.2 Non-linear — Tree")
    doc.p("Hierarchy from a single Root. One-to-many parent-child. Org chart, family tree, folders in folders.")
    d.org_tree(doc)
    doc.h3("Graph")
    doc.p("No strict hierarchy — any node may connect to any other. Nodes/vertices = items (cities, people). Edges = connections (roads, friendships). Facebook; GPS fastest route.")
    doc.h3("2.5.3 Operations on any structure")
    doc.bullets(["Insertion", "Deletion", "Traversal (visit each)", "Searching", "Sorting (asc/desc)"])

    doc.h1("2.6 Identify data structures in problem scenarios")
    doc.p("Clear before/after → linear. Branches or many links → non-linear.")
    doc.table(
        ["Scenario", "Structure", "Why"],
        [
            ["Student grades for a known class", "Array", "Fixed count, same type, fast index lookup."],
            ["Music playlist / browser history", "Linked list", "Each node knows next; easy insert/delete."],
            ["Undo / Redo", "Stack (LIFO)", "Last action is the first undone."],
            ["Printer jobs", "Queue (FIFO)", "First received, first printed."],
            ["College org chart", "Tree", "Principal → deans → HODs. Parent-child."],
            ["GPS / maps", "Graph", "Cities = nodes, roads = edges. Many routes."],
        ],
        col_fracs=[1.5, 1.1, 1.8],
    )
    doc.h3("Quick decision guide")
    doc.table(
        ["If the data…", "Then", "Use"],
        [
            ["Has Next / Previous", "Linear", "Array, Linked list"],
            ["Has Parent & Child", "Non-linear", "Tree"],
            ["Is first-come, first-served", "Linear", "Queue"],
            ["Is connections / relationships", "Non-linear", "Graph"],
            ["Must come out in reverse of entry", "Linear", "Stack"],
        ],
        col_fracs=[1.8, 1, 1.4],
    )

    doc.h1("2.7 Trace data retrieval")
    doc.p("Even among linear structures, finding an item costs different effort.")
    doc.cards([
        ("2.7.1 Array — direct access",
         "Fixed index 0..n-1. If you know the index you JUMP. Array = [10,50,20,70,90,30] → Array[2] = 20. Looping still visits 10, then 50, then 20."),
        ("2.7.2 Linked list — sequential",
         "No index. Start at Head, follow links. [12]→[98]→[23]→[87]→[56]→NULL search 87: four hops, then FOUND."),
        ("2.7.3 Queue — front only",
         "Cannot pick the middle or rear. Oldest Front item is dequeued first. Enqueue D at Rear."),
    ], cols=1)
    doc.h3("Careers")
    doc.bullets([
        "Software engineer — structures + algorithms for logic problems.",
        "Backend developer — Array vs Queue changes web performance.",
        "Algorithm engineer — search, finance, logistics.",
        "Systems analyst — efficiency and clarity of existing systems.",
        "Competitive programmer — timed algorithmic problems.",
    ])
    doc.summary([
        "Correctness: trace table (micro values) or stepwise reasoning (macro state).",
        "Clarity = modularity (SRP, loose coupling) + readability (names, flow, consistency).",
        "Big O: O(1) constant, O(log n) binary search, O(n) linear, O(n²) nested / Bubble.",
        "Refine: names, modules, shrink loops, hoist invariants, pick the right structure.",
        "Linear: array (index), list (nodes), stack LIFO, queue FIFO. Non-linear: tree, graph.",
        "Retrieval: array jumps; list walks from Head; queue only dequeues Front.",
    ])


# =====================================================================
# CHAPTER 3
# =====================================================================
def ch3(doc):
    doc.chapter_open(
        3, "Programming Fundamentals",
        "Python’s built-in structures, functions, files and exceptions — the working toolkit for XII programming papers and mini-projects.",
        [
            "Index, slice, traverse and mutate lists; know every common method.",
            "Treat tuples as locked lists (with the mutable-inside exception).",
            "Use sets for unique items and ∪ ∩ − ^.",
            "Dictionaries: unique keys, .get() safety, .items() loops.",
            "min max len sum sorted — and .sort() vs sorted().",
            "Write functions with return values; local vs global scope.",
            "open modes r/w/a; with auto-closes; try/except FileNotFoundError.",
            "Reproduce Attendance, Word-Frequency and Grade-Tracker logic.",
        ],
    )
    doc.h1("3.1 Data Structures in Python")
    doc.table(
        ["Category", "Description & examples"],
        [
            ["Primitive", "Single values: int, float, bool."],
            ["Abstract", "Built from primitives: Lists, Tuples, Sets, Dictionaries."],
        ],
        col_fracs=[1, 3],
    )

    doc.h2("3.1.1 Lists", golden=True)
    doc.p("Most versatile built-in. Ordered, mutable, duplicates allowed. Square brackets []. Mixed types OK.")
    doc.code('numbers = [10, 2, 15, 14, 3, 33]\nnames = ["Hassan", "Qasim", "Malika"]\nmixed = [1, "Python", 3.14, True]')
    doc.h3("Indexing — positive left→right, negative right→left")
    doc.p('fruits = ["apple","mango","banana","grape","kiwi"]  →  [0]..[4] and [-5]..[-1]. fruits[0]=apple, fruits[-1]=kiwi.')
    doc.callout("tip", "[-1] grab",
                "On a 10,000-item list, [-1] is the last item — no len() required.")
    doc.h3("Slicing  list[start : stop : step]   (stop is exclusive)")
    doc.code(
        """nums = [0,1,2,3,4,5,6,7,8,9]
nums[2:6]   # [2,3,4,5]
nums[:4]    # [0,1,2,3]
nums[6:]    # [6,7,8,9]
nums[::2]   # [0,2,4,6,8]
nums[::-1]  # reversed [9..0]"""
    )
    doc.h3("Traversal")
    doc.code(
        """for num in numsList:          # Pythonic
    print(num)
index = 0
while index < len(numsList):  # by index
    print(numsList[index]); index += 1"""
    )
    doc.table(
        ["Method", "Description"],
        [
            ["len(list)", "How many items."],
            [".append(value)", "Add at the end."],
            [".insert(index, value)", "Insert at a position."],
            [".remove(value)", "First occurrence; ValueError if missing."],
            [".clear()", "Empty the list."],
            [".count(value)", "How many times value appears."],
            [".index(value)", "Index of first occurrence."],
            [".sort()", "In-place ascending; reverse=True for descending."],
            [".reverse()", "Reverse in place."],
        ],
        col_fracs=[1.4, 2.6],
    )
    doc.p("Advantages: mutable; one variable holds thousands of values; mixed types.")
    doc.h3("Activity — search a list")
    doc.code(
        """numbers = [5, 10, 15, 20, 25]
search = int(input("Enter number to search: "))
found = False
for num in numbers:
    if num == search:
        found = True
        break          # stop — no need to scan the rest
print("Number found in the list." if found else "Number NOT found in the list.")""",
        title="15 → found;  99 → not found. break saves time.",
    )

    doc.h2("3.1.2 Tuples (immutable)", golden=True)
    doc.p("Ordered, immutable “read-only list”. Parentheses (). Duplicates and mixed types allowed. Same indexing as lists.")
    doc.code(
        """t = (10, 20, 30, 40, 50)
print(t[0])      # 10
print(t[-1])     # 50
print(t[1:4])    # (20, 30, 40)
print(t[::-1])   # reversed tuple"""
    )
    doc.cards([
        ("Immutability",
         "t[0] = 99  → TypeError. Exception: a list inside a tuple CAN change: t=([1,2],[3,4]); t[0].append(99) → ([1,2,99],[3,4])."),
        ("Why bother?",
         "Protect coordinates/settings. Slightly faster than lists (fixed size). Only .count() and .index()."),
    ], cols=1)

    doc.h2("3.1.3 Sets — unique & unordered")
    doc.p("Unordered, unindexed, unique. Curly braces {}. Duplicates die on creation. No myset[0]. Items inside must be immutable; the set itself is mutable.")
    doc.code("nums = {1, 4, 3, 3, 2, 2}\nprint(nums)   # {1, 2, 3, 4}")
    doc.table(
        ["Method", "Description"],
        [
            [".add(value)", "One element."],
            [".update(values)", "Many (list or tuple)."],
            [".remove(value)", "KeyError if missing."],
            [".discard(value)", "Safe — no crash if missing. Prefer this."],
            [".clear()", "Empty → set()."],
        ],
        col_fracs=[1.3, 2.5],
    )
    doc.h3("Math operations   A={1,2,3,4}  B={3,4,5,6}")
    doc.table(
        ["Operation", "Syntax", "Result"],
        [
            ["Union (all unique)", "A | B   or  A.union(B)", "{1,2,3,4,5,6}"],
            ["Intersection (common)", "A & B   or  A.intersection(B)", "{3,4}"],
            ["Difference (in A not B)", "A - B   or  A.difference(B)", "{1,2}"],
            ["Symmetric difference", "A ^ B   or  A.symmetric_difference(B)", "{1,2,5,6}"],
        ],
        col_fracs=[1.4, 1.6, 1.4],
    )
    doc.p("Traverse with for; order not guaranteed — wrap sorted() for alphabetical.")

    doc.h2("3.1.4 Dictionaries (key-value)", golden=True)
    doc.p("Look up a word (key) to find its definition (value). { key: value }. Ordered since Python 3.7. Mutable. Duplicate keys: last value wins.")
    doc.code(
        """d = {"name": "Alice", "age": 30}
d["age"] = 31          # modify
d["city"] = "NYC"      # add
del d["city"]          # delete
d = {"a": 1, "a": 2, "a": 3}
print(d)               # {'a': 3}  last wins"""
    )
    doc.callout("analogy", "Roll number",
                "One roll number (key) points to one student (value). Reassign it and the old link is gone.")
    doc.compare(
        "dict[key]  — risky",
        ['Works if the key exists.', 'Missing key → KeyError crash.', 'person["salary"]  boom.'],
        "dict.get(key)  — safe",
        ["Missing → None (no crash).", 'Custom default: get("salary", 0) → 0.', '"name" in person → True/False.'],
        CORAL, SAGE,
    )
    doc.table(
        ["View", "Returns"],
        [[".keys()", "All keys"], [".values()", "All values"], [".items()", "Key-value tuples"]],
        col_fracs=[1, 2],
    )
    doc.code(
        """for key in inventory:                 # keys (default)
for val in inventory.values():
for key, val in inventory.items():    # most common
    print(f"{key} costs {val}")"""
    )

    doc.h2("3.1.5 Common built-in functions")
    doc.table(
        ["Function", "Purpose", "Works on"],
        [
            ["min()", "Smallest (alpha or numeric)", "List, tuple, set, dict keys"],
            ["max()", "Largest", "same"],
            ["len()", "Count", "same"],
            ["sum()", "Add numeric elements", "List, tuple, set, dict values"],
            ["sorted()", "NEW sorted list — original unchanged", "same (dict → sorted keys)"],
        ],
        col_fracs=[0.9, 1.8, 1.6],
    )
    doc.callout("note", "sorted() vs .sort()",
                ".sort() is a list method and changes the list. sorted() is a function, works on anything, returns a new list.")

    doc.h2("3.1.6 Activity — Student Attendance")
    doc.code(
        """students = ["Ali", "Sara", "Ayesha"]
present_count = 0
for student in students:
    status = input(f"Is {student} present? (yes/no): ").lower()
    if status == "yes":
        present_count += 1
print("Total:", len(students), "Present:", present_count,
      "Absent:", len(students) - present_count)""",
        title="yes/no/yes → Total 3, Present 2, Absent 1",
    )
    doc.h2("3.1.7 Activity — Word Frequency Counter")
    doc.code(
        """sentence = "python is easy python is fun python is powerful"
words = sentence.split()
word_freq = {}
for word in words:
    word_freq[word] = word_freq.get(word, 0) + 1
for word, count in word_freq.items():
    print(f"{word:<10} : {count}")
top_word = max(word_freq, key=word_freq.get)""",
        title="split → list; get(word,0)+1 is the counter heart; {word:<10} aligns the table",
    )

    doc.h1("3.2 Functions in Python", golden=True)
    doc.p("Duplicate code is long, hard to read and hard to update. Write once, reuse.")
    doc.cards([
        ("Reusability", "Write once, use anywhere."),
        ("Modularity", "Big problem → small tasks."),
        ("Readability", "Cleaner, shorter files."),
        ("Maintainability", "Fix the bug in one place."),
    ])
    doc.code("def greet():\n    print(\"Hello, World!\")\ngreet()\ngreet()   # reuse, no second print")
    doc.p("Parts: def keyword, name, parameters (inputs), indented body, optional return.")
    doc.cards([
        ("Built-in", "Ready: len(), range(), sum(), print()."),
        ("User-defined", "You write with def for tasks built-ins do not cover."),
    ])
    doc.h3("3.2.2 Return values")
    doc.code(
        """def multiply(a, b):
    return a * b
result = multiply(5, 3)     # 15 stored
print("The answer is:", result)"""
    )
    doc.h3("3.2.3 Activity — arithmetic calculator (modularity)")
    doc.code(
        """def add(a, b): return a + b
def divide(a, b):
    return a / b if b != 0 else "Cannot divide by zero"
num1 = float(input("Enter first number: "))
num2 = float(input("Enter second number: "))
print("Addition:", add(num1, num2))
print("Division:", divide(num1, num2))"""
    )
    doc.h3("3.2.4 Scope")
    doc.compare(
        "Local",
        ["Defined inside a function.", "Exists only while it runs.",
         "Main cannot see it — print(secret) after calc() → ERROR."],
        "Global",
        ["Defined outside all functions.", "Any function can read it.",
         "x = 10; def show(): print(x)"],
        AMBER, SKY,
    )

    doc.h1("3.3 File Handling", golden=True)
    doc.p("Create, read, write, update, delete files on disk. Variables die with the program (RAM). Files persist (hard drive).")
    doc.cards([
        ("Text file", "Human-readable. .txt .csv .py"),
        ("Binary file", "Bytes — media, compiled. .jpg .mp3 .dat"),
    ])
    doc.table(
        ["Mode", "Name", "Description"],
        [
            ["'r'", "Read", "Fails if the file does not exist."],
            ["'w'", "Write", "OVERWRITES existing content. Creates if missing."],
            ["'a'", "Append", "Adds at the end. Creates if missing."],
            ["'rb' / 'wb'", "Binary", "Images / audio."],
        ],
        col_fracs=[0.8, 0.8, 2.4],
    )
    doc.p("Methods: .read() whole string; .readlines() list of lines; .write(text) (add \\n yourself); .close() flushes to disk.")
    doc.callout("warn", "Danger of 'w'",
                "'w' deletes everything first. To keep old data, use 'a'.")
    doc.h2("3.6 with statement", golden=True)
    doc.p("Forget .close() and a crash can corrupt the file. with is a context manager — the file closes when the block ends, even after an error.")
    doc.code(
        """with open('myfile.txt', 'w') as new_file:
    new_file.write("Context managers are safe!\\n")
# no .close() — automatic

with open('myfile.txt', 'r') as read_file:
    for line in read_file:          # line-by-line, memory-safe
        print(line, end="")"""
    )

    doc.h2("3.8 Errors and exceptions (try-except)")
    doc.p("Catch impossible actions so the program does not crash — show a friendly message instead.")
    doc.table(
        ["Error", "Meaning"],
        [
            ["FileNotFoundError", "Path does not exist."],
            ["PermissionError", "OS will not let you read/write."],
            ["IOError", "General I/O (disk full, disconnected)."],
        ],
        col_fracs=[1.3, 2.5],
    )
    doc.code(
        """try:
    with open('missing_data.txt', 'r') as f:
        print(f.read())
except FileNotFoundError:
    print("Error: The file does not exist. Please check the name.")
except Exception as e:
    print(f"An unexpected error occurred: {e}")"""
    )
    doc.callout("tip", "Real-world practice",
                "Pro apps never dump a red traceback. Missing file → polite “Please try again later.”")

    doc.h2("3.9 Mini project — Grade Tracker")
    doc.code(
        """with open("grades.txt", "w") as f:
    f.write("Alice: 88\\n"); f.write("Bob: 75\\n"); f.write("Carol: 92\\n")
with open("grades.txt", "a") as f:
    f.write("David: 81\\n")
with open("grades.txt", "r") as f:
    lines = f.readlines()
    total = 0
    for line in lines:
        name, grade = line.strip().split(":")
        print(f"{name} scored {grade}")
        total += int(grade)
    print(f"Class average: {total/len(lines):.1f}")  # 84.0""",
        title="w create → a append → r + split + average",
    )
    doc.h3("Careers")
    doc.bullets([
        "Python / software developer.",
        "Data analyst — lists, dicts, files.",
        "Automation engineer — scripts for IT and testing.",
        "Game developer — functions + logic.",
    ])
    doc.summary([
        "List [] mutable ordered; Tuple () locked; Set {} unique; Dict {k:v} unique keys, use .get().",
        "min/max/len/sum/sorted work across structures. .sort() mutates lists only.",
        "Functions: def, params, return. Local dies inside; global lives outside.",
        "Files persist. r / w (wipe) / a. with closes safely. try/except stops crashes.",
        "Projects: attendance counter, word-frequency .get(), grade-tracker average.",
    ])


# =====================================================================
# CHAPTER 4
# =====================================================================
def ch4(doc):
    doc.chapter_open(
        4, "Data and Analysis",
        "Python as the bridge from maths to real analysis: connect a database, wrangle a DataFrame, draw the right graph, and summarise with mean / median / mode and spread.",
        [
            "Name the five connection components and the driver→cursor→SQL flow.",
            "Reproduce the 9-step SQLite script (connect, cursor, create, insert, commit, select, fetch, close).",
            "Build a DataFrame from a dict; read_csv / read_excel; derive columns.",
            "Find NaN with isnull(); fillna or dropna.",
            "Pick bar, line, pie, histogram, scatter, box — and write the plt calls.",
            "Compute mean/median/mode and range/variance/σ/min/max; know when mean lies.",
        ],
    )
    doc.h1("4.1 Concept of Data Analysis")
    doc.p("Examine, organise and interpret data to extract useful information — decisions, trends, problems.")
    doc.bullets([
        "Schools — results → improve teaching.",
        "Businesses — sales → profit and customer behaviour.",
        "Hospitals — records → diagnosis and treatment.",
    ])
    doc.p("Why Python? Simple, powerful libraries. Reads files and databases, structures data, does stats, draws charts. Five lines replace hours in a spreadsheet.")

    doc.h2("4.1.1 Data sources & 4.1.2 Connectivity", golden=True)
    doc.p("Sources: schools, websites, sensors, databases. Connectivity = the program talking to the source to access, retrieve and update.")
    doc.table(
        ["Component", "Description"],
        [
            ["1. Database", "Organised structured data. SQLite (built-in, light) or MySQL (large web)."],
            ["2. Driver", "Translator between Python and that DBMS."],
            ["3. Connection object", "Opens, manages, closes the pipeline."],
            ["4. Cursor object", "Executes SQL and retrieves rows — a pointer through results."],
            ["5. SQL queries", "CREATE, INSERT, SELECT, UPDATE, DELETE."],
        ],
        col_fracs=[1.3, 2.7],
    )
    doc.flow(["Python app", "Driver", "Connection", "Cursor", "SQL", "Database"])

    doc.h1("4.2 Creating a SQLite Database in Python")
    doc.p("Built-in — no heavy server. One .db file next to the script. No passwords or ports.")
    doc.table(
        ["Step", "Syntax", "Why"],
        [
            ["1", "import sqlite3", "Load the library."],
            ["2", "conn = sqlite3.connect('school.db')", "Create/open the file."],
            ["3", "cur = conn.cursor()", "Vehicle for queries."],
            ["4", 'cur.execute("CREATE TABLE students (id INTEGER, name TEXT, marks INTEGER)")',
             "Columns + types."],
            ["5", "cur.execute(\"INSERT INTO students VALUES (1, 'Ali', 85)\")",
             "Strings in SQL need quotes."],
            ["6", "conn.commit()", "WITHOUT this, inserts vanish when the program ends."],
            ["7", 'cur.execute("SELECT * FROM students")', "* = all columns."],
            ["8", "rows = cur.fetchall();  for r in rows: print(r)", "List of rows."],
            ["9", "conn.close()", "Free memory, unlock the file."],
        ],
        col_fracs=[0.5, 2.2, 1.5],
    )

    doc.h1("4.3 Basic Operations on Data using Pandas", golden=True)
    doc.p("Raw data is often unstructured or incomplete. Pandas is the library for structured analysis. Third-party: pip install pandas.")
    doc.h3("4.3.1 DataFrame")
    doc.p("Core 2-D table — rows (records) × columns (attributes), like Excel or SQL. Filter, sort, aggregate.")
    doc.code(
        """import pandas as pd
data = {'Name': ['Ali', 'Sara', 'Ahmed'], 'Math': [85, 90, 78], 'Science': [80, 88, 70]}
df = pd.DataFrame(data)
print(df)
# Optional args: index, columns, dtype, copy.  pd is the alias.""",
        title="DataFrame_name = pd.DataFrame(data, index, columns, dtype, copy)",
    )
    doc.h3("4.3.2 Load files")
    doc.code(
        """df = pd.read_csv('students.csv')
print(df.head())                    # first 5 rows — safe on 1M-row files
df = pd.read_excel('students.xlsx', sheet_name='Sheet1')"""
    )
    doc.h3("New columns — vectorised, no for-loop")
    doc.code(
        """df['Total'] = df['Math'] + df['Science']
df['Average'] = df['Total'] / 2
# Ali 165 / 82.5   Sara 178 / 89.0   Ahmed 148 / 74.0   Ayesha 187 / 93.5"""
    )

    doc.h2("4.3.3 Handling missing values", golden=True)
    doc.p("Missing data is NaN (Not a Number). It MUST be handled or stats crash.")
    doc.code(
        """data = {"Name": ["Ali","Sara","Ahmed","Ayesha"],
        "Marks": [85.0, None, 78.0, 92.0],   # Sara missing
        "Grade": ["A", "A", None, "A"]}       # Ahmed missing
print(df.isnull())            # True where missing
print(df.isnull().sum())      # Marks:1  Grade:1
df["Marks"] = df["Marks"].fillna(df["Marks"].mean())
df["Grade"] = df["Grade"].fillna("Not Assigned")
df = df.dropna()              # alternative: delete any row with NaN"""
    )
    doc.table(
        ["Function", "Job"],
        [
            ["isnull()", "True/False mask of missing cells."],
            ["sum() with isnull()", "Count missing per column."],
            ["fillna(value)", "Replace (often with the column mean)."],
            ["dropna()", "Delete rows that contain any NaN."],
        ],
        col_fracs=[1.4, 2.4],
    )

    doc.h1("4.4 Data Organisation and Representation")
    doc.p("Arrange collected data so it is easy to understand, analyse and communicate.")
    doc.cards([
        ("4.4.1 Tabular", "Rows and columns — exact values side by side (subject scores)."),
        ("4.4.2 Frequency table",
         "Group into bins. 50–59:5, 60–69:7, 70–79:9, 80–89:4, 90–100:2. Most students scored 70–79."),
    ])
    doc.h3("4.4.3 Graphical — Matplotlib")
    doc.p("matplotlib.pyplot is the common education/research library.")
    doc.flow(["import plt", "figure()", "plot/bar", "xlabel/ylabel", "title", "show()"])
    doc.callout("tip", "Why visualise?",
                "10,000 temperature rows mean nothing. One line graph shows if it is rising.")

    doc.h1("4.5 Types of Graphs", golden=True)
    doc.cards([
        ("Bar / column",
         "Compare discrete categories. Height/length = value. Subjects, months, departments.\nplt.bar(subjects, marks, color='skyblue', edgecolor='black')"),
        ("4.5.2 Line",
         "Best for trends over time (monthly temp, stocks).\nplt.plot(months, temps, marker='o'); plt.grid(True)"),
        ("4.5.3 Pie",
         "Parts of a whole. Weak when too many slices or values are almost equal.\nplt.pie(students, labels=subjects, autopct='%1.1f%%', startangle=90)\n25+15+30+10 → 31.2 / 18.8 / 37.5 / 12.5 %"),
        ("4.5.4 Histogram",
         "Distribution of continuous numbers in bins. Bars TOUCH (unlike a bar chart).\nplt.hist(scores, bins=[40,50,60,70,80,90,100], edgecolor='black')"),
        ("4.5.5 Scatter",
         "Relationship of two numeric variables — correlation, trend, outliers.\nplt.scatter(rainfall_mm, crop_yield, color='green', alpha=0.7)\nMore rain ↔ more yield (positive)."),
        ("4.5.6 Box plot  ★",
         "Five-number summary: min, Q1, median (Q2), Q3, max. Best outlier hunter.\nplt.boxplot([class_a, class_b], labels=['Class A','Class B'])\nWhiskers = min/max; box = middle 50%; line = median."),
    ], cols=1)

    doc.h1("4.6 Descriptive Statistics")
    doc.p("Summarise thousands of records with a few numbers.")
    doc.h2("4.6.1 Measures of central tendency")
    doc.cards([
        ("Mean (average)",
         "Sum / count. Uses every value. 70+80+90 / 3 = 80. Distorted by outliers: nine people earn $10, one earns $1,000 → mean $109 (looks rich; 90% are not). Then use median."),
        ("Median",
         "Middle value after sorting. Odd count 35,10,15,70,95 → 10,15,35,70,95 → 35. Resistant to outliers."),
        ("Mode",
         "Most frequent. One, several, or none. Bottles 20,25,20,30,20,25,20 → 20 (four times)."),
    ], cols=1)
    doc.table(
        ["Measure", "Best when…", "Scenario"],
        [
            ["Mean", "Values cluster; no crazy extremes.", "Typical test scores."],
            ["Median", "Huge outliers would break the average.", "Salaries when the CEO earns millions."],
            ["Mode", "You want the most popular choice.", "Most common shoe size sold."],
        ],
        col_fracs=[0.8, 1.7, 1.7],
    )
    doc.h2("4.6.2 Measures of spread (dispersion)", golden=True)
    doc.p("Central tendency says where the centre is. Spread says how stretched or tight the data is around that centre.")
    doc.cards([
        ("Range", "Max − Min. Sales 120,150,180 → range 60. Simplest."),
        ("Variance σ²",
         "Average squared distance from the mean. Small = consistent; large = wild."),
        ("Standard deviation σ",
         "√variance. Same units as the data (marks, not marks²). Low σ = reliable; high σ = unpredictable."),
        ("Min / Max",
         "Smallest / largest recorded. [70,80,90,60,75] → min 60, max 90. Box-plot whiskers."),
    ])
    doc.callout("memory", "Box plots display these",
                "Whiskers = min & max. Box = middle 50%. Line inside = median.")
    doc.h3("Careers")
    doc.cards([
        ("Data analyst", "Python, Pandas, Excel — trends for decisions."),
        ("DBA", "Design and secure MySQL/Oracle."),
        ("Data scientist", "Stats + models + AI predictions."),
        ("Viz specialist", "Matplotlib / Power BI dashboards."),
        ("BI analyst", "Reports CEOs can act on."),
        ("Backend developer", "Python/Java that talks to databases."),
    ])
    doc.summary([
        "Analysis = examine + organise + interpret. Python + libraries do the heavy lift.",
        "Connection: Database, Driver, Connection, Cursor, SQL. SQLite = one .db file. Always commit() and close().",
        "DataFrame = 2-D table. read_csv / read_excel / df.head(). New columns are vectorised.",
        "NaN: isnull, fillna (often mean), dropna.",
        "Bar=categories, Line=time, Pie=parts, Hist=bins (touching), Scatter=correlation, Box=outliers + 5-number.",
        "Centre: mean (every value, outlier-fragile), median (middle), mode (most common). Spread: range, variance, σ, min, max.",
    ])


# =====================================================================
# CHAPTER 5
# =====================================================================
def ch5(doc):
    doc.chapter_open(
        5, "Application and Impacts of Computing",
        "XII’s impact chapter is AI-deep and security-deep: how networks learn, how collaboration stays safe, how threats look, and why equity is not the same as equal access.",
        [
            "Define ML, NN, DL and draw input → hidden → output.",
            "List 8 NN components and 6 DL components.",
            "Give Pakistan-sector impacts and 8 application families.",
            "Authentication, access control, encryption (sym/asym), backup, firewall.",
            "Malware, phishing, DoS, identity theft + identification signs + 2FA.",
            "Equal access vs equity with a Zoom-captions example.",
        ],
    )
    doc.h1("5.1 Machine Learning, Neural Networks and Deep Learning")
    doc.p("AI areas that let computers learn from data and decide without being programmed for every step. Face unlock, Siri/Alexa, photo search, medical diagnosis, translation.")
    doc.h3("5.1.1 Machine Learning")
    doc.p("A model is a trained brain: (1) Data in — massive amounts. (2) Learning — patterns and rules. (3) Prediction on new unseen data. Neural nets are one ML type; Deep Learning is an advanced ML method.")

    doc.h2("5.1.2 Neural Networks", golden=True)
    doc.p("Inspired by the brain, implemented as maths. Neurons/nodes pass information layer to layer.")
    d.neural_net(doc)
    doc.callout("analogy", "Face unlock",
                "Camera (input) → eye distance / nose shape (hidden) → match stored face → unlock (output).")

    doc.h2("5.1.3 Deep Learning")
    doc.p("ML that uses multi-layer neural nets. “Deep” = data crosses several hidden layers. Early layers learn edges/shapes/colours; deeper layers combine them into a face or a car model.")
    doc.p("Photo gallery: type “car” or “flower” and related photos appear because a deep net already learned patterns from millions of images.")
    doc.compare(
        "Neural network (the model)",
        ["Layers, nodes, connections.", "Can be shallow — one or two hidden layers."],
        "Deep learning (the method)",
        ["Trains nets with MANY hidden layers.", "Needs huge data and GPU-level power."],
        LAV, CORAL,
    )

    doc.h2("5.1.4 Components of Neural Networks", golden=True)
    doc.table(
        ["Component", "Description"],
        [
            ["1. Input layer", "Raw data — pixels, sound waves, text."],
            ["2. Neurons / nodes", "Receive, calculate, pass forward."],
            ["3. Hidden layer(s)", "Between in and out — learn patterns."],
            ["4. Weights", "Strength / importance of each connection."],
            ["5. Bias", "Extra constant that helps the model adjust."],
            ["6. Activation function", "Gate: is this signal important enough to pass on?"],
            ["7. Output layer", "Final decision — “this is a cat”."],
            ["8. Loss function", "How wrong vs reality — so the net can correct itself."],
        ],
        col_fracs=[1.4, 2.6],
    )
    doc.h3("5.1.5 Components of Deep Learning")
    doc.cards([
        ("Large input data", "Data-hungry — thousands to millions of records."),
        ("Many hidden layers", "Dozens or hundreds — intricate patterns."),
        ("Automatic feature learning", "No human highlighting features — the net extracts them."),
        ("Learning algorithm", "Backpropagation reduces mistakes."),
        ("High computing power", "GPUs for millions of points across deep layers."),
        ("Training process", "Repeated loops called epochs."),
    ])

    doc.h2("Future in Pakistan — National AI Policy 2025")
    doc.table(
        ["Sector", "Potential impact"],
        [
            ["Education", "Smart learning, tutoring, auto assessment, find who needs help."],
            ["Healthcare", "Disease detection, medical images, hospital data — rural specialist gap."],
            ["Agriculture", "Crops, weather, irrigation, yield — national economy."],
            ["Business & banking", "Fraud, chatbots, forecasts, risk."],
            ["Local languages", "Speech, translation, TTS for Urdu, Sindhi, regional languages."],
        ],
        col_fracs=[1.2, 2.8],
    )
    doc.callout("tip", "What students should prepare",
                "Python, mathematics, data analysis, problem-solving, ethical use.")

    doc.h1("5.2 Applications of Neural Networks & Deep Learning")
    doc.cards([
        ("1. Image recognition", "Objects/faces in cameras, photo search, biometric locks. Phone face unlock."),
        ("2. Speech recognition", "Speech → text/commands; accents. “Set a morning alarm.”"),
        ("3. NLP", "Understand language. Chatbots, translators, AI writers. Google Translate EN→Urdu."),
        ("4. Healthcare", "X-ray / CT / MRI — early disease. Highlight pneumonia on a lung film."),
        ("5. Recommenders", "Past behaviour → next video. CS videos → more programming tutorials."),
        ("6. Autonomous vehicles", "Cameras + radar → roads, signals, people. Pedestrian → auto-brake."),
        ("7. Fraud detection", "Banks flag unusual spend vs your pattern."),
        ("8. Assistive tech", "Speech-to-text for people who cannot type easily."),
    ], cols=1)

    doc.h1("5.3 Secure Collaboration and Data Protection", golden=True)
    doc.p("Share files, attend class, edit together — only if data stays protected.")
    doc.h3("5.3.1 Secure collaboration")
    doc.cards([
        ("i) Authentication / identity",
         "Prove who you are: password, PIN, OTP, biometrics. Banking OTP before login."),
        ("ii) Access control",
         "What an authenticated user may do: view / edit / comment / download / share. Teacher: students view-only; group leaders edit."),
        ("iii) Accountability",
         "Actions stick to verified accounts. LMS: who uploaded, who submitted."),
        ("iv) Data privacy",
         "Protect names, numbers, marks, passwords. Share only with the right people. Confidential in storage and transit. Legal/ethical rules."),
        ("v) Safe transmission",
         "Stop interception. Official encrypted LMS, not an open public forum."),
    ], cols=1)
    doc.h3("5.3.2 Data protection")
    doc.cards([
        ("Encryption",
         "Readable → ciphertext. Symmetric = one key both ways. Asymmetric = public encrypts, private decrypts."),
        ("Strong passwords", "Upper + lower + numbers + symbols. e.g. Zk@2026#Pass. Stops brute force."),
        ("Backup & recovery", "Copy on cloud / external drive after hardware death or attack."),
        ("Firewall + antivirus",
         "Firewall = network barrier, blocks suspicious traffic. Antivirus = finds/removes viruses, spyware, ransomware, Trojans on the machine."),
    ])

    doc.h1("5.4 Security Threats and Mitigation", golden=True)
    doc.p("A threat can harm a system or its data. Mitigation prevents it or shrinks the damage.")
    doc.h3("5.4.1 Common threats")
    doc.cards([
        ("1. Malware", "Viruses, worms, spyware, ransomware, Trojans. Cracked software that secretly corrupts files."),
        ("2. Phishing", "Fake emails/sites steal passwords, bank details, OTPs."),
        ("3. Unauthorized access", "No permission — weak/shared passwords, unlocked devices."),
        ("4. Data / identity theft", "Copy data; use Name/CNIC/bank details to pretend to be someone."),
        ("5. Denial of Service (DoS)", "Flood a site with fake requests until real users cannot log in (exam portal)."),
        ("6. Human error", "Delete the wrong file, email confidential data, fall for a simple scam."),
    ], cols=1)
    doc.h3("5.4.2 Identifying threats")
    doc.table(
        ["Sign", "Likely meaning"],
        [
            ["Slow machine, missing files, random pop-ups", "Malware / background activity"],
            ["Failed logins or strange locations", "Unauthorized access attempt"],
            ["Urgent email, asks for OTP, bad grammar, odd links", "Phishing"],
            ["Unexpected delete/copy/move of records", "Data theft or insider misuse"],
            ["Traffic spike / site suddenly dying", "DoS in progress"],
        ],
        col_fracs=[2, 2],
    )
    doc.callout("tip", "First line of defence",
                "No cracked software, unverified sites, or random USB sticks.")
    doc.h3("5.4.3 Mitigation")
    doc.cards([
        ("Antivirus & firewalls", "Scan USBs; block bad network traffic."),
        ("Strong passwords & 2FA", "Password + OTP on the phone."),
        ("Encryption", "Unreadable if intercepted."),
        ("Regular backups", "Recover from crash, error, ransomware."),
        ("User awareness", "Tech fails if humans click unknown links or share passwords."),
    ], cols=1)

    doc.h1("5.5 Equity and Equal Access", golden=True)
    doc.compare(
        "Equal access",
        ["Everyone gets the exact same tools.",
         "Same Zoom login for every student."],
        "Equity",
        ["Extra, specific support so people can reach the same outcome.",
         "Live captions in Zoom for a student who cannot hear well."],
        SKY, SAGE,
    )
    doc.h3("5.5.1 Functions")
    doc.bullets([
        "Need-based support — audio descriptions for visually impaired students.",
        "Remove barriers — mobile-friendly, low-data apps for remote Pakistan.",
        "Active participation — recorded lectures when power/internet dies.",
        "Different learning needs — video + text + audio.",
    ])
    doc.h3("5.5.2 Collaboration tools")
    doc.table(
        ["Tool", "Educational use"],
        [
            ["Google Docs", "Real-time write/edit/comment — group assignments."],
            ["Zoom", "Meetings, classes, screen share."],
            ["Microsoft Teams", "Meetings + files + class groups."],
            ["Google Classroom / LMS", "Lectures, assignments, quizzes, grades."],
            ["WhatsApp", "Quick announcements — use responsibly."],
            ["Email", "Formal notices, large attachments, written record."],
        ],
        col_fracs=[1.3, 2.7],
    )
    doc.callout("warn", "Fairness check",
                "If homework is accepted only via an app that needs a high-end phone, that is NOT equal access. Prefer web or light apps.")
    doc.h3("Careers")
    doc.cards([
        ("ML engineer", "Face recognition, NLP, recommenders."),
        ("Cybersecurity analyst", "Malware/phishing watch + firewalls/2FA."),
        ("AI researcher", "New DL techniques — labs / R&D."),
        ("Data privacy officer", "Legal privacy + secure collaboration."),
        ("Ethical hacker", "Legal pentests before criminals DoS or malware you."),
    ], cols=1)
    doc.summary([
        "ML = trained brain. NN = brain-inspired layers. DL = many hidden layers + GPUs + huge data.",
        "NN parts: input, neurons, hidden, weights, bias, activation, output, loss.",
        "Apps: vision, speech, NLP, health images, recommenders, self-driving, fraud, assistive.",
        "Secure collab: authenticate, control access, track, encrypt, official channels.",
        "Threats: malware, phishing, DoS, theft, human error. Mitigate with 2FA, AV, backups, awareness.",
        "Equal = same tools. Equity = extra support (captions) so outcomes can match.",
    ])


# =====================================================================
# CHAPTER 6
# =====================================================================
def ch6(doc):
    doc.chapter_open(
        6, "Entrepreneurship in the Digital Age",
        "An entrepreneur spots a problem and turns a solution into a product. In the digital age that can start with WhatsApp or a Google Form — then a paper prototype, an MVP, a beachhead market.",
        [
            "Define entrepreneur / entrepreneurship and list local digital examples.",
            "Walk Observe → Ask → Select → Suggest → Test.",
            "Explain why a prototype exists; Lo / Mid / Hi-Fi with Table 6.3.",
            "Draw Design–Build–Test–Iterate; complete the Homework Helper activity.",
            "Define MVP; contrast it with a prototype (looks right vs will they use it).",
            "Name the riskiest assumption and a test for it.",
            "Retell the canteen MVP (3 days, 5 items, extra collection line).",
            "Choose a beachhead; fill the project sheet; apply the rubric and ethics.",
        ],
    )
    doc.h1("6.1 Entrepreneur & Entrepreneurship")
    doc.p("An entrepreneur identifies a problem, thinks of a solution, and tries to turn it into a product or service. Many start with a small idea, limited resources, and a wish to help.")
    doc.bullets([
        "They observe people and listen.",
        "They take calculated risks.",
        "They improve the idea step by step.",
    ])
    doc.p("Entrepreneurship is the process of planning, starting, testing and improving a business idea — creativity, problem-solving, teamwork, communication, calculated risk.")
    doc.callout("note", "Simple meaning",
                "Entrepreneur asks: What problem can I solve? Entrepreneurship tests and improves that solution until it is useful.")
    doc.flow(["1 Problem", "2 Solution", "3 Product"])

    doc.h1("6.2 Entrepreneurship in the Digital Age", golden=True)
    doc.p("Use digital tools to start, test, improve and grow: phones, social media, websites, forms, payments, maps, videos, simple apps.")
    doc.p("You do not always need a complex app. A WhatsApp group, Google Form, Facebook page or simple site can test an idea. Past: big money, offices, long plans. Now: test quickly; if users dislike it, change before you spend.")
    doc.callout("tip", "No-code counts",
                "Handmade cards on Instagram, or a shopkeeper’s WhatsApp Ajrak catalogue — digital entrepreneurship without a line of code.")
    doc.h3("Table 6.1  Local examples (Sindh / Pakistan)")
    doc.table(
        ["Problem", "Digital idea", "First users"],
        [
            ["Parents miss college notices.", "WhatsApp notice + reminder service.", "Parents of first-year students."],
            ["Small embroidery shop, few customers.", "Catalogue + order form on Facebook/WhatsApp.", "Customers in the same city."],
            ["Students forget test dates.", "Google Calendar guide or simple reminder app.", "Grade XII students."],
            ["Canteen queues at break.", "Pre-order form for snacks.", "Students and teachers."],
        ],
        col_fracs=[1.4, 1.5, 1.3],
    )
    doc.callout("warn", "Pick a real problem",
                "Do not pick an idea because it sounds modern. A weak problem makes a weak business.")

    doc.h1("6.3 From Problem to Business Idea")
    doc.p("Start by watching daily life — home, college, market, village, city.")
    doc.bullets([
        "What problem do people face?",
        "Who faces it?",
        "How often?",
        "What do they do now?",
        "Can technology help simply?",
    ])
    doc.callout("case", "Scattered notes",
                "Notes live in WhatsApp, email, photocopy, class groups. Idea: one subject-wise notes organiser.")
    doc.callout("tip", "Scope",
                "Do not start with “fix the whole education system.” Start with “Grade XII practical-file dates in one college.” Smaller = testable.")
    doc.table(
        ["Step", "What students do", "Example"],
        [
            ["Observe", "Notice repeated problems.", "Students forget practical-file dates."],
            ["Ask users", "Talk to people who face it.", "Ask five classmates how they remember."],
            ["Select one problem", "One clear problem only.", "Practical-file reminder."],
            ["Suggest a solution", "Simple digital or paper idea.", "Reminder form or app screen."],
            ["Test early", "Show before final build.", "Ask classmates if they would use it."],
        ],
        col_fracs=[1.1, 1.5, 1.6],
    )
    doc.flow(["Problem", "Idea", "Prototype", "Feedback", "MVP"])

    doc.h1("6.4 Prototype", golden=True)
    doc.p("An early model of a product, service, site or app. It shows how the idea may look or work. It is NOT the final product — it is made to test and collect feedback.")
    doc.bullets([
        "Makes the idea visible — users see, not only hear.",
        "Finds mistakes early (hidden button, too much text, missing feature).",
        "Saves time and money before coding.",
    ])
    doc.p("Form: paper sketch, cardboard, clickable PowerPoint, Canva, Figma wireframe, simple site, service flowchart. Canteen pre-order can start as screens on paper.")

    doc.h2("6.5 Types of Prototypes  (fidelity = closeness to final)")
    doc.cards([
        ("6.5.1 Low-fidelity",
         "Quick, rough, paper. No colours/fonts. Main idea + flow. Cheap, fast, easy to change — best for students first."),
        ("6.5.2 Mid-fidelity",
         "PowerPoint / Canva / Figma. Organised screens and navigation, not final graphics. Test screen-to-screen flow."),
        ("6.5.3 High-fidelity",
         "Looks almost final: colours, buttons, sample data, some working features. Only after the basic idea is tested."),
    ], cols=1)
    doc.table(
        ["Type", "Meaning", "Best use", "Example"],
        [
            ["Low-Fi", "Quick rough model", "Very early testing", "Hand-drawn homework-reminder screens"],
            ["Mid-Fi", "Clearer layout + flow", "Testing navigation", "Clickable PPT / Figma"],
            ["High-Fi", "Close to final", "Realistic experience", "Working small order-form site"],
        ],
        col_fracs=[0.8, 1.2, 1.2, 1.6],
    )
    doc.flow(["Low-Fi (paper)", "Mid-Fi (PowerPoint)", "High-Fi (Figma/HTML)"])
    doc.callout("warn", "Common mistake",
                "Building a full app before you know users need it. A rough prototype protects you.")

    doc.h1("6.6 Prototype Development Cycle", golden=True)
    doc.p("Not one-shot. Create, test, improve, test again = iteration.")
    d.prototype_cycle(doc)
    doc.cards([
        ("1. Design", "Understand the problem. Decide what the prototype must show (flow, features)."),
        ("2. Build", "First version, physical or digital. Aim = visibility, not beauty."),
        ("3. Test", "Give it to users. Watch what they understand and where they stick."),
        ("4. Iterate", "Improve from feedback. Cut extras, add missing pieces."),
    ])

    doc.h1("6.7 Class Activity — Homework Helper / ClassBuddy")
    doc.p("Students forget homework, tests, required items. Do NOT build a full app. Understand → draw Lo-Fi → test → improve.")
    doc.h3("Step 1  Understand — interview 10 students")
    doc.p("7 / 10 forget at least one task a week. They want a reminder before leaving home. They want a very simple design.")
    doc.table(
        ["Finding", "Meaning", "Design decision"],
        [
            ["7 of 10 forget tasks.", "The problem is common.", "Show a daily task list."],
            ["Reminders needed before leaving home.", "Time of reminder matters.", "Add a morning-notification option."],
            ["Students want simple apps.", "Design must stay simple.", "Large buttons, clear labels."],
        ],
        col_fracs=[1.5, 1.3, 1.5],
    )
    doc.p("Step 2: Draw three paper screens — Today’s classes · Add homework · Show reminder — with arrows between them.")
    doc.p("Step 3: Five classmates try the paper. Observer stays silent. Task: “add one homework.”")
    doc.table(
        ["User feedback", "Problem", "Improvement"],
        [
            ['"I cannot quickly find Add Homework."', "Button not visible.", "Larger, centred Add Homework button."],
            ['"I want reminders by subject."', "Reminder too general.", "Add subject name + due date."],
            ['"I want all tasks for the week."', "Daily view is not enough.", "Add a Weekly View button."],
        ],
        col_fracs=[1.5, 1.2, 1.6],
    )
    doc.p("Step 5: Redraw with those three changes. A prototype has not failed when users complain — it fails if the team ignores useful feedback.")

    doc.h1("6.8 Minimum Viable Product (MVP)", golden=True)
    doc.p("The simplest working version — only the features needed to test the idea with real users.")
    doc.cards([
        ("Minimum", "Only essential features. No extras."),
        ("Viable", "Usable enough to actually solve the main problem."),
    ])
    doc.p("Not the final product. Not only a drawing. A small working version that tests whether users need the solution.")
    doc.p("Full canteen app might have login, payment, tracking, discounts. The MVP can be a Google Form where students pick snacks before break.")
    doc.callout("note", "Simple meaning",
                "An MVP answers: Will people actually use this? It tests real behaviour, not only visual design.")

    doc.h1("6.9 Prototype vs MVP")
    doc.p("Related, not the same. Prototype tests design. MVP tests real use and demand.")
    doc.table(
        ["Point", "Prototype", "MVP"],
        [
            ["Main purpose", "Show how the idea may look or work.", "Test whether users will actually use it."],
            ["Working status", "May not work — sketch or model.", "Must work at least in a basic way."],
            ["Users", "Small group feedback on design.", "Early real users in daily life."],
            ["Cost", "Very low.", "Low, but some basic development."],
            ["Example", "Paper screens for canteen orders.", "Google Form used for real orders for three days."],
        ],
        col_fracs=[1, 1.6, 1.8],
    )
    doc.callout("memory", "Key takeaway",
                "Prototype = “Does it look right and make sense?”   MVP = “Will people use it and find value?”")

    doc.h1("6.10 Identifying the Riskiest Assumption")
    doc.p("An assumption is something we believe but have not tested. The riskiest one can kill the whole business if it is wrong. Test it early — saves time and money.")
    doc.table(
        ["Business idea", "Risky assumption", "How to test (MVP)"],
        [
            ["Online tuition finder", "Students will pay for online tutoring.", "Ask 20 students; offer a trial class."],
            ["Canteen pre-order form", "Students will order snacks before break.", "Google Form for one real week."],
            ["Ajrak online catalogue", "Customers will order via WhatsApp.", "Share with 30 customers; count real orders."],
            ["College van updates", "Parents/students will check daily.", "Trial WhatsApp broadcast for one route."],
        ],
        col_fracs=[1.3, 1.5, 1.6],
    )

    doc.h1("6.11 Developing an MVP")
    doc.p("Select only essential features. Building everything at once is difficult, costly and slow. The plan must state problem, users, ONE main feature, basic design, cost, marketing, feedback, improvement.")
    doc.table(
        ["Element", "Question", "Example answer"],
        [
            ["Problem", "What are we solving?", "Students wait too long at the canteen."],
            ["Target users", "Who first?", "Grade XII in one college."],
            ["Main feature", "The ONE feature that solves it?", "Pre-order snacks before break."],
            ["Basic design", "What steps?", "Menu, name, class, order time."],
            ["Cost", "Free / low-cost tools?", "Google Form or printed slips."],
            ["Marketing", "How will early users hear?", "WhatsApp to the class group."],
            ["Feedback", "How will they respond?", "Short form after 3 days."],
        ],
        col_fracs=[1, 1.4, 1.8],
    )

    doc.h1("6.12 Case Study — Canteen Pre-Order MVP")
    doc.p("Problem: long lines; snacks finish before students reach the counter. Goal: NOT a full app. Test whether students will order before break and whether staff can cope.")
    doc.numbered([
        "Paper prototype: select item → enter name → collect order.",
        "Feedback: keep the menu short; pay at collection.",
        "MVP: Google Form, five items.",
        "Canteen prepares pre-orders. Test three days only — learn fast.",
    ])
    doc.table(
        ["MVP element", "Decision"],
        [
            ["Features", "Menu, student name, class, item, quantity."],
            ["Cost & tools", "Free Google Form or printed slips."],
            ["Marketing", "Class announcement + WhatsApp."],
            ["Testing period", "Three days."],
            ["Feedback", "Did you save time? Would you use it again?"],
            ["Improvement", "Keep only 5 items; close orders 20 minutes before break."],
        ],
        col_fracs=[1.2, 2.6],
    )
    doc.p("Result: students liked saving time; staff found too many items hard. Team kept five items and added a separate collection line — based on real feedback.")

    doc.h1("6.13 Testing an MVP")
    doc.p("Give the working version to real users. Collect numbers and comments. Plan before launch: how many users, how long, what you will record.")
    doc.table(
        ["Type", "Question", "Example result"],
        [
            ["Number-based", "How many tried it?", "40 students used the form."],
            ["Number-based", "How many would use it again?", "30 of 40 said yes."],
            ["Comment-based", "What was confusing?", "Did not know the order closing time."],
            ["Observation", "Where did they struggle?", "Forgot to enter class name."],
        ],
        col_fracs=[1.1, 1.5, 1.6],
    )
    doc.callout("note", "Data skill link",
                "Feedback is useful only when studied. Count responses, spot repeated problems, decide which improvement is first.")

    doc.h1("6.14 Beachhead Market", golden=True)
    doc.p("A small, focused group of first users with a clear, immediate need. Serve them first — test the MVP properly — then expand. “All students in Pakistan” is too broad. “Grade XII board-exam students in one college” is reachable.")
    doc.bullets([
        "Specific and narrowly defined.",
        "Reachable by the startup team.",
        "Users have a strong, immediate need.",
    ])
    doc.table(
        ["Idea", "Weak first market", "Better beachhead"],
        [
            ["Study app", "All students in Pakistan.", "Grade XII exam students in one college."],
            ["Canteen pre-order", "All canteens in the city.", "One college canteen at lunch."],
            ["Ajrak catalogue", "All online shoppers.", "Existing customers of one local shop."],
            ["Van updates", "All transport users.", "Students/parents of ONE van route."],
        ],
        col_fracs=[1.2, 1.4, 1.8],
    )
    doc.p("A small first market does not mean the idea stays small. Learn, improve, then expand — even globally.")

    doc.h1("6.15 Complete Student Project")
    doc.p("Groups complete one small, local, classroom-possible project: problem → prototype → feedback → MVP plan → riskiest assumption → beachhead.")
    doc.p("Ideas: homework/test reminder, college notice organiser, canteen pre-order, shop WhatsApp catalogue, van updates, lost-and-found, study-notes organiser.")
    doc.table(
        ["Project sheet field", "Fill in…"],
        [
            ["Problem statement", "One clear local problem."],
            ["Target users", "Who first?"],
            ["Business idea", "Simple digital/paper solution."],
            ["Low-fidelity prototype", "What screens / flow?"],
            ["Feedback from users", "What they said."],
            ["Improvement after feedback", "What you changed and why."],
            ["MVP plan", "Essential feature + tools + test window."],
            ["Riskiest assumption", "The belief that could kill it."],
            ["How you will test that assumption", "Concrete trial."],
            ["Beachhead market", "Narrow first group."],
            ["Marketing for first users", "How they hear about it."],
        ],
        col_fracs=[1.5, 2.3],
    )
    doc.h3("Table 6.13  Rubric")
    doc.table(
        ["Criteria", "Excellent", "Satisfactory", "Needs improvement"],
        [
            ["Problem ID", "Clear, local, important.", "Understandable, needs detail.", "Vague or too broad."],
            ["Prototype", "Clear flow and features.", "Shows the basic idea.", "Incomplete or unclear."],
            ["Feedback & fixes", "Collected; changes clearly based on it.",
             "Collected but weak analysis.", "No clear feedback; changes unexplained."],
            ["MVP plan", "Essential features + clear test.", "Basic features; testing fuzzy.",
             "Confused with the final product."],
        ],
        col_fracs=[1, 1.2, 1.2, 1.3],
    )

    doc.h2("6.16 Ethical and safe use of digital tools")
    doc.p("Respect privacy, truthfulness and fairness when collecting feedback. Do not collect unnecessary personal information. Do not share phone numbers or photos without permission.")
    doc.callout("note", "Equity point",
                "Design for weak internet, limited devices, language difficulty. Large buttons, simple Urdu/Sindhi instructions, low data — that is equal access.")
    doc.h3("Careers")
    doc.cards([
        ("Tech entrepreneur / founder", "Problem → prototype → MVP → launch."),
        ("Product manager", "User needs, feature priority, prototype/MVP tests."),
        ("Business analyst", "Recommend digital solutions; test assumptions first."),
        ("Innovation / startup consultant", "Validate ideas, MVPs, beachheads."),
        ("Digital marketing specialist", "Reach the beachhead, then grow."),
        ("Venture / incubator analyst", "Evaluate early ideas for investment or incubation."),
    ])
    doc.summary([
        "Entrepreneurship = identify a problem and test a solution until it is useful.",
        "Digital age = forms, WhatsApp, pages — cheap, fast tests.",
        "Ideas come from daily observation and talking to users. Keep the problem small.",
        "Prototype (Lo/Mid/Hi-Fi) tests “does it look right?” Cycle: Design, Build, Test, Iterate.",
        "MVP is the simplest working product. Tests “will they use it?”",
        "Riskiest assumption can kill the business — test it early.",
        "Beachhead = small reachable first market with a sharp need.",
        "Ethics: privacy, truth, fairness. Equity: low-data, large type, local language.",
    ])
