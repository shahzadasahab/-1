"""Lectures 13–17 — Programming fundamentals."""

from lectures.kit import box, fig, lecture, table
from web import svgs


def lectures() -> str:
    return "".join([
        lecture(13, "Python, the IDE, and input() is a string", "Unit 3 · Programming", "45 min", [
            "Say why Python is a high-level language.",
            "Run a three-line program in VS Code.",
            "Convert input() with int() or float() before arithmetic.",
        ], "\n".join([
            box("recap", "BLOCK C OPENS", "A computer does exactly what you said, including the mistakes. Python is this course’s high-level language because it reads almost like English."),
            "<p><strong>Low-level</strong> sits next to the machine (binary, assembly). <strong>Mid-level</strong> (C) lets you touch memory. <strong>High-level</strong> (Python, Java) hides the hardware so you think about the problem. C++ is for speed; Java’s promise is “write once, run anywhere”; Python’s promise is readable syntax and a huge library world.</p>",
            "<p>An <strong>IDE</strong> is one workplace: editor, colour, run, debugger. VS Code becomes an IDE when you install the Microsoft Python extension. Save as <code>program.py</code>. Indentation is syntax: <strong>4 spaces</strong> per block. Mix tabs and spaces and you will meet <code>IndentationError</code>.</p>",
            "<pre># a comment — the interpreter ignores it\nprint(\"Hello, Intermediate\")\nprint(100)</pre>",
            "<p>Execution is top to bottom. That default order is <strong>sequence</strong>.</p>",
            table(["Type", "Keyword", "Example"], [
                ["Integer", "int", "20, −3"],
                ["Float", "float", "5.7"],
                ["String", "str", "\"Ali\", '2026'"],
                ["Boolean", "bool", "True"],
                ["List / tuple / dict", "list, tuple, dict", "[2,4], (10,), {\"name\": \"Ahmed\"}"],
            ]),
            "<p><code>input()</code> always returns a <strong>string</strong>. Convert: <code>age = int(input(\"Age: \"))</code>. Forget the conversion and <code>\"10\" + \"20\"</code> quietly gives <code>\"1020\"</code>.</p>",
            box("mistake", "THE CLASSIC FIRST-YEAR CRASH", "Using input() in arithmetic without int() or float(). Names: letters, digits, underscore; start with a letter or _; never a keyword. <code>my-var</code> is illegal (the hyphen is minus)."),
            box("exit", "EXIT TICKET", "1. What does input() return? 2. Standard indent? 3. Why is my-var illegal?"),
            box("hw", "HOMEWORK", "Type a program that asks for two numbers, converts them with float(), and prints the sum. Break it on purpose by removing float() and read the error."),
        ])),

        lecture(14, "Operators — including the bitwise family", "Unit 3 · Programming", "45 min", [
            "Use //, %, and ** correctly.",
            "Contrast = (store) with == (test).",
            "Compute AND, OR, XOR, and a left shift on small integers.",
        ], "\n".join([
            box("recap", "LAST LECTURE", "input() is a string; 4 spaces; sequence. Today the symbols that sit between values."),
            table(["Family", "Symbols", "Notes"], [
                ["Arithmetic", "+ − * / // % **", "\\(9//2=4\\), \\(9\\%2=1\\), \\(2^{3}=8\\)"],
                ["Assignment", "= += −= *=", "After a = 10; a += 5, a is 15"],
                ["Relational", "== != &gt; &lt; &gt;= &lt;=", "Return True / False"],
                ["Logical", "and · or · not", "Combine conditions"],
                ["Membership", "in · not in", '"P" in "Python" is True'],
                ["Bitwise", "&amp; | ^ ~ &lt;&lt; &gt;&gt;", "Same truth tables as Unit 1 gates"],
            ]),
            "<p>Bitwise worked example. \\(a=10=1010_{2}\\), \\(b=6=0110_{2}\\):</p>",
            r"\[ a \land b = 0010_{2}=2,\quad a \lor b = 1110_{2}=14,\quad a \oplus b = 1100_{2}=12,\quad a \ll 1 = 20 = a\cdot 2. \]",
            "<p>Also \\(\\sim x = -x-1\\) in two’s complement, so \\(\\sim 10=-11\\). If a question shows <code>0b1010</code>, the <code>0b</code> prefix is notation, not part of the value.</p>",
            box("try", "PREDICT (True/False)", "\\(9//2==4\\) · \\(9\\%2==1\\) · <code>\"Py\" in \"Python\"</code> · <code>not (True and False)</code>. All four are True."),
            box("mistake", "COMMON MISTAKE", "= stores a value. == tests equality. Mixing them inside an if is a logic bug that looks like a typo."),
            box("exit", "EXIT TICKET", "1. What is 9 // 2? 2. Bitwise AND of 10 and 6? 3. Difference between = and ==?"),
            box("hw", "HOMEWORK", "Line up 10 (1010) and 6 (0110) on paper. Compute AND, OR, XOR, and 5 &lt;&lt; 2 (= 20)."),
        ])),

        lecture(15, "Selection — if, elif, else", "Unit 3 · Programming", "45 min", [
            "Draw a selection flowchart with exactly one path taken.",
            "Write if / elif / else for a three-way choice.",
            "Nest a guard (for example refuse ÷ 0).",
        ], "\n".join([
            box("recap", "LAST LECTURE", "Operators decide True/False. Selection uses that answer to pick a path."),
            fig(svgs.python_flow(), "Figure L15.1 — Selection: exactly one path runs."),
            "<p><strong>for</strong> waits until Lecture 16. Today: <code>if</code>, <code>elif</code>, <code>else</code>. The colon opens a block; the indent is the block.</p>",
            "<pre>a = float(input(\"First number: \"))\nb = float(input(\"Second number: \"))\nop = input(\"Choose + - * / : \").strip()\nif op == \"+\":\n    print(a + b)\nelif op == \"-\":\n    print(a - b)\nelif op == \"*\":\n    print(a * b)\nelif op == \"/\":\n    if b == 0:\n        print(\"Cannot divide by zero.\")\n    else:\n        print(a / b)\nelse:\n    print(\"Unknown operator.\")</pre>",
            "<p>The nested if inside division is selection inside selection — the unit’s nested-if idea in a useful costume.</p>",
            box("exit", "EXIT TICKET", "1. How many paths of an if/elif/else run? 2. Why does / need a nested guard? 3. What does strip() remove?"),
            box("hw", "HOMEWORK", "Write even/odd: read an int, print Even if n % 2 == 0 else Odd. Then add a third branch for zero."),
        ])),

        lecture(16, "Repetition — for, while, break, continue", "Unit 3 · Programming", "45 min", [
            "Choose for when the trip count is known.",
            "Choose while until a condition dies.",
            "Trace a while-loop that never dies.",
        ], "\n".join([
            box("recap", "LAST LECTURE", "Selection picks one path. Repetition walks a path many times."),
            "<p><strong>for</strong> when the count is known: <code>range(start, stop, step)</code> — stop is exclusive. <strong>while</strong> until a condition becomes False. <code>break</code> leaves now; <code>continue</code> skips this iteration.</p>",
            "<pre>for i in range(1, 6):\n    print(i)          # 1 2 3 4 5\n\ni = 1\nwhile i &lt; 6:\n    print(i)\n    i += 1            # without this line the loop never dies</pre>",
            box("mistake", "LOGICAL ERROR, NOT A CRASH", "The textbook infinite loop: <code>i = 1; while i &lt; 6: print(i); i -= 1</code>. Trace: 1, 0, −1… \\(i\\) never reaches 6. The program is legal and will run until you kill it. Always ask: “What makes the condition False, and does every path reach it?”"),
            "<p>A one-shot guess uses <code>random.randint</code> and a single if. A PIN loop (next lecture) uses while + a bool flag.</p>",
            box("exit", "EXIT TICKET", "1. Loop when the count is known? 2. What does continue do? 3. Why does i -= 1 inside while i &lt; 6 never finish?"),
            box("hw", "HOMEWORK", "Print a triangle of stars, 1 to 5, with a nested for. Then rewrite it with a while. Same output, two control stories."),
        ])),

        lecture(17, "Libraries, errors, and the ATM studio", "Unit 3 · Programming", "45 min", [
            "Import math, random, and datetime.",
            "Name syntax, runtime, and logical errors.",
            "Read an ATM skeleton as sequence + selection + repetition.",
        ], "\n".join([
            box("recap", "LAST LECTURE", "for / while / flags. Today we borrow other people’s code and name the three ways a program can be wrong."),
            "<pre>import math, random, datetime\nprint(math.sqrt(25), math.pi)\nsecret = random.randint(1, 10)\nnow = datetime.datetime.now().strftime(\"%d-%m-%Y\")</pre>",
            "<p>Third-party libraries need <code>pip install</code> (NumPy, Pandas, Matplotlib). Built-ins are already housemates.</p>",
            table(["Error", "When", "Example"], [
                ["Syntax", "Will not start", "Missing ), bad indent, if without :"],
                ["Runtime", "Dies while running", "10/0, int(\"abc\")"],
                ["Logical", "Runs and lies", "i -= 1 in a climbing loop"],
            ]),
            "<p>Read a traceback from the <strong>bottom</strong>: last line is the disease.</p>",
            "<h2>ATM skeleton — Unit 3 in one costume</h2>",
            "<pre>PIN = \"1234\"\nbalance = 10000.0\ntries = 3\nok = False\nwhile tries &gt; 0 and not ok:\n    entered = input(\"Enter PIN: \")\n    if entered == PIN:\n        ok = True\n    else:\n        tries -= 1\n        print(\"Wrong PIN!\", tries, \"left.\")\nif not ok:\n    print(\"Card locked.\")\nelse:\n    running = True\n    while running:\n        print(\"1 Check  2 Deposit  3 Withdraw  4 Exit\")\n        choice = input(\"Choose: \")\n        if choice == \"1\":\n            print(f\"Balance: Rs. {balance:.2f}\")\n        elif choice == \"2\":\n            amt = float(input(\"Deposit: \"))\n            if amt &gt; 0:\n                balance += amt\n        elif choice == \"3\":\n            amt = float(input(\"Withdraw: \"))\n            if 0 &lt; amt &lt;= balance:\n                balance -= amt\n            else:\n                print(\"Rejected.\")\n        elif choice == \"4\":\n            running = False</pre>",
            "<p>Sequence (start values) + selection (menu) + repetition (PIN loop, menu loop) + bool flags. If you can add a transfer or a 20-try lockout, you own the unit.</p>",
            box("exit", "EXIT TICKET", "1. Three error types? 2. Where do you start reading a traceback? 3. Which structure is the PIN loop?"),
            box("hw", "HOMEWORK", "Type the ATM. Add deposit and a rejected-overdraw message. Then break the PIN on purpose and read the traceback from the bottom."),
        ])),
    ])
