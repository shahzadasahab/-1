"""Unit 3 — Programming Fundamentals (Python)."""

from reportlab.platypus import PageBreak, Spacer

from pdf_kit import Callout, bullets, code_block, h1, h2, h3, numbered, p, simple_table


def build(styles):
    s = styles
    story = [
        h1(s, "Unit 3 — Programming Fundamentals"),
        p(s, "A computer is obedient and ignorant. It will do exactly what you said, including the mistakes. A program is the list of instructions; a programming language is the agreed spelling of those instructions. This unit teaches you to write, run, and debug simple Python — the language this course chose because it reads almost like English and is used in data, AI, web work, and automation.", "Lead"),
        h2(s, "3.1 What you must be able to do"),
    ]
    story += bullets(s, [
        "Classify languages as low-, mid-, or high-level and say why Python is high-level.",
        "Use VS Code: editor, terminal, extensions, run, and the debugger idea.",
        "Declare variables, pick types, and convert input() strings to int/float.",
        "Apply arithmetic, assignment, relational, logical, membership, and bitwise operators.",
        "Write sequence, if / elif / else, nested if, for, while, break, continue, and nested loops.",
        "Import built-in libraries (math, random, datetime) and install a third-party library with pip.",
        "Name syntax, runtime, and logical errors and read a traceback.",
    ])
    story += [
        h2(s, "3.2 Language levels and why Python"),
        p(s, "<b>Low-level</b> languages sit next to the machine: binary, and assembly’s mnemonics. Fast, tiny, painful for humans. <b>Mid-level</b> languages (C is the usual example) let you touch memory and still write readable code. <b>High-level</b> languages (Python, Java) hide the hardware so you can think about the problem."),
        p(s, "C++ is chosen when you need speed and control (games, operating systems). Java’s promise is “write once, run anywhere” (large apps, Android). Python’s promise is readable syntax and a huge library world: Django/Flask websites, data analysis, AI, office automation, security scripts. Learning Python in Year 1 is a career door, not a toy."),
        h2(s, "3.3 The IDE — Visual Studio Code"),
        p(s, "An <b>IDE</b> is one workplace: editor, syntax colour, autocomplete, run button, debugger. VS Code is a free editor that becomes an IDE when you install extensions. For this course install the Microsoft Python extension (and optionally Pylance, Python Debugger, a formatter)."),
        p(s, "Tour: Explorer (files), Search, Source Control (Git), Run and Debug, Extensions, the top search bar (Ctrl+P / Ctrl+Shift+P). Save as <b>program.py</b>. Run with the play button or “Run Python File in Terminal.” Output appears in the Terminal panel."),
        Callout(s, "note", "Python decides blocks by indentation, not braces. The course standard is 4 spaces per level. Mix tabs and spaces and you will meet IndentationError. Pick 4 spaces and never look back."),
        h2(s, "3.4 A first program"),
        code_block(
            s,
            """# This is a comment — the interpreter ignores it
print("Hello, World!")
print("Welcome to Python")
print(100)""",
        ),
        p(s, "Execution is top to bottom. That default order is called <b>sequence</b>."),
        h2(s, "3.5 Variables and data types"),
        p(s, "A variable is a named box in memory. Python does not ask you to announce the type; it infers it from the value, and the type can change later. Names: letters, digits, underscore; must start with a letter or _; case-sensitive; never a keyword (if, while, for)."),
        simple_table(
            s,
            ["Type", "Keyword", "Meaning", "Example"],
            [
                ["Integer", "int", "Whole number", "20, -3"],
                ["Float", "float", "Decimal", "5.7, 100.0"],
                ["Complex", "complex", "a + bj", "1+3j"],
                ["String", "str", "Text", "\"Ali\", '2026'"],
                ["Boolean", "bool", "True or False", "True"],
                ["List", "list", "Ordered, changeable", "[2, 4, 6]"],
                ["Tuple", "tuple", "Ordered, unchangeable", "(10, \"hi\")"],
                ["Set", "set", "Unique, unordered", "{\"p\", \"d\"}"],
                ["Dictionary", "dict", "Key : value", "{\"name\": \"Ahmed\"}"],
            ],
            col_widths=[90, 70, 160, 175],
        ),
        Spacer(1, 8),
        h2(s, "3.6 Input and output"),
        p(s, "<b>print()</b> writes to the screen. Useful forms: print(\"msg\"), print(\"msg\", var), and f-strings: print(f\"My name is {name} and I am {age}\")."),
        p(s, "<b>input(prompt)</b> always returns a <b>string</b>. If you need a number, convert: age = int(input(\"Age: \")) and height = float(input(\"Height: \")). Forget the conversion and \"16\" + 1 will explode, or \"10\" + \"20\" will quietly give \"1020\"."),
        Callout(s, "mistake", "The single most common first-year bug: using input() in arithmetic without int() or float()."),
        h2(s, "3.7 Operators"),
        h3(s, "Arithmetic"),
        simple_table(
            s,
            ["Symbol", "Meaning", "10 and 3"],
            [
                ["+", "Add", "13"],
                ["-", "Subtract", "7"],
                ["*", "Multiply", "30"],
                ["/", "True division", "3.333…"],
                ["//", "Floor division", "3"],
                ["%", "Remainder (modulus)", "1"],
                ["**", "Power", "1000"],
            ],
            col_widths=[70, 200, 225],
            center_cols=[0, 2],
        ),
        Spacer(1, 6),
        p(s, "Assignment shortcuts: =, +=, -=, *=, /=, //=, **=, %=. After a = 10; a += 5, a is 15."),
        p(s, "Relational operators return bool: == != &gt; &lt; &gt;= &lt;=. Logical: <b>and</b> (both), <b>or</b> (either), <b>not</b> (flip). Membership: <b>in</b> / <b>not in</b> — \"P\" in \"Python\" is True."),
        Callout(s, "mistake", "= assigns. == compares. if a = 5 is a syntax error in Python; if a == 5 is a test."),
        h3(s, "Bitwise — the same gates, now on binary digits"),
        p(s, "A bit is 0 or 1. bin(n) shows the binary form. Treat integers as rows of switches."),
        simple_table(
            s,
            ["Op", "Name", "Rule"],
            [
                ["&amp;", "AND", "1 only if both bits are 1"],
                ["|", "OR", "1 if at least one bit is 1"],
                ["^", "XOR", "1 if the bits differ"],
                ["~", "NOT", "Flip every bit (two’s complement: ~x == -x-1)"],
                ["&lt;&lt;", "Left shift", "Shift toward the high end; fill 0s. n &lt;&lt; k equals n × 2<sup>k</sup>"],
                ["&gt;&gt;", "Right shift", "Shift toward the low end. n &gt;&gt; k equals floor(n / 2<sup>k</sup>)"],
            ],
            col_widths=[50, 90, 355],
        ),
        Spacer(1, 6),
        p(s, "Worked: a=10 (1010), b=6 (0110). a &amp; b = 0010 = 2. a | b = 1110 = 14. a ^ b = 1100 = 12. ~10 = -11. 5 &lt;&lt; 1 = 10; 20 &gt;&gt; 2 = 5. Notice the rhyme with Unit 1’s AND/OR/XOR tables — that is not an accident."),
        h2(s, "3.8 Control structures"),
        p(s, "Almost every program is built from three shapes: <b>sequence</b> (do this, then that), <b>selection</b> (choose a path), <b>repetition</b> (do it again)."),
        h3(s, "Selection"),
        p(s, "<b>if</b> runs a block only when the condition is True; otherwise it skips. <b>if–else</b> always runs exactly one of two blocks. <b>if–elif–else</b> tests from the top and runs the first True block; else is the “none of the above.” <b>Nested if</b> puts a second decision inside the first (age first, then salary, then approve a loan)."),
        code_block(
            s,
            """age = int(input("Enter your age: "))
if age <= 0:
    print("Invalid age!")
elif age <= 12:
    print("Child")
elif age <= 17:
    print("Teenager")
elif age <= 35:
    print("Young Adult")
elif age <= 60:
    print("Middle-Aged Adult")
else:
    print("Senior Citizen")""",
        ),
        p(s, "Colon after the condition. Indented block. else has no condition. elif is “else if.”"),
        h3(s, "Repetition"),
        p(s, "<b>for</b> when you know the trip count or you are walking a sequence. <b>while</b> when you keep going until a condition dies (user types \"done\", PIN becomes valid). range(stop) → 0..stop-1; range(start, stop); range(start, stop, step). Negative step counts down."),
        code_block(
            s,
            """for i in range(0, 10, 2):
    print("Even", i)          # 0 2 4 6 8

count = 1
while count <= 5:
    print(count)
    count += 1                # forget this and you loop forever""",
        ),
        p(s, "<b>break</b> leaves the loop now. <b>continue</b> skips the rest of this iteration. Nested loops: the inner loop finishes a full cycle for every outer step — the usual way to print a grid or a pattern of stars (Unit 2’s pattern recognition in code)."),
        Callout(s, "exam", "“Known number of iterations” → for. “Until the user says stop” → while. break vs continue is a favourite MCQ."),
        h3(s, "Putting the three structures in one program"),
        p(s, "A shopping-bill loop (while) reads item names until \"done\" (selection), adds prices, then applies 20% / 10% / 0% discount (if–elif–else). An even/odd checker that runs three times is for + input + if. Build both. They are the skeleton of the ATM activity at the end of the textbook chapter."),
        h2(s, "3.9 Libraries"),
        p(s, "A library is code someone already tested. Five import styles:"),
        code_block(
            s,
            """import math
print(math.sqrt(25), math.pi)

import math as m
print(m.sqrt(16))

from math import sqrt, pi, factorial
print(sqrt(49), pi)

from math import *     # convenient, but names can clash""",
        ),
        p(s, "<b>Built-in</b> (no install): math (pi, ceil, floor, pow, sqrt), random (randint, random, uniform), datetime (now, strftime). <b>Third-party</b> (pip install name): NumPy, Pandas, Matplotlib. A student report card that stamps today’s date, invents a roll number, and computes a percentage is a perfect three-library exercise."),
        h2(s, "3.10 Debugging"),
        simple_table(
            s,
            ["Kind", "When it shows", "Example", "Feel"],
            [
                ["Syntax", "Before the program really runs", "Missing ), wrong indent, if without :", "Python refuses to start"],
                ["Runtime / exception", "During execution", "int(\"abc\"), 10/0", "Traceback, then death"],
                ["Logical", "Program “works” but is wrong", "i -= 1 in a loop that should climb", "Silent, worst to find"],
            ],
            col_widths=[90, 130, 160, 115],
        ),
        Spacer(1, 6),
        p(s, "A <b>traceback</b> names the file, the line, and the error type (ValueError, IndentationError, ZeroDivisionError). Read it from the bottom up: the last line is the disease; the lines above are the path. Print intermediate values. Use the VS Code debugger to pause and inspect. Logical errors need a trace table — the same habit you used on algorithms in Unit 2."),
        h2(s, "3.11 Mini practice set (type these, do not only read)"),
    ]
    story += numbered(s, [
        "Calculator: two integers and a choice (+ − * /). Guard division by zero.",
        "Guess the number: random.randint(1, 10), one guess, “You win” / “You lose.”",
        "ATM sketch: PIN with 3 tries; menu for balance, deposit, withdraw, exit; reject overdraft.",
        "Predict: 4 == 5-1, 55 &gt;= 11*5, 22 != 23-1. Which are True?",
    ])
    story += [
        h2(s, "3.12 Recap"),
        p(s, "Python is a high-level, dynamically typed language. input() is a string. Indentation is syntax. Three control shapes build every program. Libraries save you from reinventing square roots. Three error kinds: will not run, dies while running, runs and lies."),
        h2(s, "3.13 Self-test"),
    ]
    story += numbered(s, [
        "Which comment syntax is legal in Python?",
        "Why is my-var an illegal variable name?",
        "What does input() always return?",
        "Standard indentation width?",
        "Which loop when the count is known?",
        "Which bitwise operator is 1 only when both bits are 1?",
        "Name the three error types.",
        "Write a one-line f-string that prints name and age.",
    ])
    story += [
        h2(s, "3.14 Answers"),
        p(s, "<b>1.</b> # this is a comment.  <b>2.</b> Hyphens are not allowed; the interpreter reads subtraction.  <b>3.</b> str.  <b>4.</b> 4 spaces.  <b>5.</b> for.  <b>6.</b> &amp; (bitwise AND).  <b>7.</b> Syntax, runtime, logical.  <b>8.</b> print(f\"{name} is {age}\").", "Answer"),
        p(s, "True/False drill: A True (4==4), B True (55==55), C False (22==22, so != is False).", "Answer"),
        PageBreak(),
    ]
    return story
