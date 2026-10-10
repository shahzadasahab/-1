#!/usr/bin/env python3
"""Build bilingual CS XI/XII crash-course lecture catalog for the Android app."""
from __future__ import annotations

import json
from pathlib import Path

OUT = Path(__file__).resolve().parents[1] / "app/src/main/assets/course/course.json"


def T(*parts: str) -> str:
    return " ".join(p.strip() for p in parts if p.strip())


def display_text(
    n: int,
    week: int,
    kind: str,
    chapter: str,
    focus: str,
    golden: str,
    start: int,
    end: int,
    topics: list[str],
) -> str:
    cards = "\n".join(f"• {t}" for t in topics)
    return (
        f"Day {n:02d} of 30 · Week {week} · {kind}\n"
        f"Chapter: {chapter}\n"
        f"Focus: {focus}\n"
        f"★ Golden: {golden}\n"
        f"Booklet pages {start}–{end} (as printed).\n\n"
        f"Today's cards:\n{cards}\n\n"
        "Read the embedded pages as printed. English exam terms stay exactly as written."
    )


def day(
    course: str,
    n: int,
    week: int,
    kind: str,
    chapter: str,
    focus: str,
    golden: str,
    start: int,
    end: int,
    topics: list[str],
    script: str,
) -> dict:
    return {
        "id": f"{course}-d{n:02d}",
        "day": n,
        "week": week,
        "kind": kind,
        "chapter": chapter,
        "focus": focus,
        "golden": golden,
        "startPage": start,
        "endPage": end,
        "topics": topics,
        "script": script,
        "displayText": display_text(n, week, kind, chapter, focus, golden, start, end, topics),
    }


XI_INTRO = T(
    "یہ {Computer Science XI} کا تیس دن کا {Crash Course} ہے، {New Sindh Curriculum 2026}۔",
    "دن 1 سے 23 ہر موضوع revision cards کی صورت میں پڑھاتے ہیں۔ ہر باب کا آخری دن timed {Checkpoint} ہے۔",
    "دن 24 سے 26 صرف ★ {Golden blitz} ہے۔ دن 27 recaps، دن 28 {Mock}، دن 29 marking، دن 30 {Repair}۔",
    "ہر تدریسی دن تین گھنٹے: پہلے 15 منٹ کل کا ★ {Golden} زبانی، پھر آج کے کارڈز، پھر {Closed-book drill}، رات کو {Define} · {Explain} · {Example} · {Diagram} · {Working} سے پانچ نمبر۔",
    "پیچھے رہو تو صرف ★ {Golden} کارڈز کرو۔ {Checkpoint} مت چھوڑو۔ نیا باب اس وقت تک نہ شروع کرو جب تک اس باب کی {Golden} تعریف زبانی نہ آئے۔",
    "فون دوسرے کمرے میں رکھو۔ صفحات جوں کے توں دیکھیں، اصطلاحات انگریزی میں ویسی ہی یاد کریں جیسے چھپی ہیں۔",
)

XI_INTRO_EN = T(
    "This is the Computer Science XI 30-Day Crash Course for the New Sindh Curriculum 2026.",
    "Days 1–23 teach every topic as revision cards. The last day of each chapter is a timed Checkpoint.",
    "Days 24–26 are Golden blitz only. Day 27 is recaps. Day 28 is the mock. Day 29 you mark. Day 30 you repair and stop.",
    "Every teaching day is 3 hours: 0–15 min recite yesterday’s Golden, 15–105 min today’s cards, 105–135 min closed-book drill, 135–180 min one 5-mark answer using Define · Explain · Example · Diagram · Working.",
    "If you fall behind, do only the Golden cards. Never skip a checkpoint. Do not start a new chapter until you can say that chapter’s Golden definitions without looking.",
    "Phone in another room. Study the booklet pages as printed. English exam terms stay exactly as written.",
)

XII_INTRO_EN = T(
    "This is the Computer Science XII 30-Day Crash Course for the New Sindh Curriculum 2026.",
    "Chapter 1 Computer Systems (HCI). Chapter 2 Computational Thinking and Algorithms. Chapter 3 Programming Fundamentals. Chapter 4 Data and Analysis. Chapter 5 Application and Impacts of Computing. Chapter 6 Entrepreneurship in the Digital Age.",
    "Same method: 3 hours, Golden first, never skip a Checkpoint. Last week is Golden blitz, Recap, Mock, Mark, Repair.",
    "Booklet pages stay as printed. Listen in Urdu; English terms such as HCI, Trace Tables, Big O Notation, and MVP stay as written.",
)

XII_INTRO = T(
    "یہ {Computer Science XII} کا تیس دن کا {Crash Course} ہے، {New Sindh Curriculum 2026}۔",
    "باب ایک {Computer Systems (HCI)}، باب دو {Computational Thinking and Algorithms}، باب تین {Programming Fundamentals}، باب چار {Data and Analysis}، باب پانچ {Application and Impacts of Computing}، باب چھ {Entrepreneurship in the Digital Age}۔",
    "طریقہ وہی ہے: تین گھنٹے، ★ {Golden} پہلے، {Checkpoint} مت چھوڑو، آخری ہفتے {Golden blitz}، {Recap}، {Mock}، {Mark}، {Repair}۔",
    "صفحات جوں کے توں ہیں۔ لیکچر اردو میں ہے، اصطلاحات جیسے {HCI}، {Trace Tables}، {Big O Notation}، {MVP} انگریزی میں ویسی ہی بولی جائیں گی۔",
)

XI = [
    day(
        "xi", 1, 1, "Teach", "Computer Systems", "Computer Systems (1/5)",
        "Analog and Digital Signals", 5, 6,
        ["Discrete and Continuous Quantities", "Introduction to Digital Systems", "Analog and Digital Signals", "Boolean Algebra"],
        T(
            "السلام علیکم۔ {Class XI}، دن 01، باب {Computer Systems}۔ آج کا ★ Golden موضوع {Analog and Digital Signals} ہے۔",
            "{Discrete} مقداریں گنی جاتی ہیں، جیسے کلاس میں طلبہ؛ درمیان میں کچھ نہیں۔ {Continuous} مقداریں ناپی جاتی ہیں، جیسے پانی کا درجہ حرارت۔ یاد رکھو: سیڑھیاں {Discrete}، ramp {Continuous}۔",
            "{Digital system} صرف دو قیمتیں استعمال کرتا ہے: 0 یعنی {OFF}، {LOW} یا {FALSE}، اور 1 یعنی {ON}، {HIGH} یا {TRUE}۔ فائدے: {Reliable}، {Accurate}، آسان ڈیزائن، {Programmable}۔ ایک {Bit} بتی کے سوئچ کی طرح ہے — آن یا آف۔",
            "★ {Signal} وہ بدلتی وولٹیج ہے جو معلومات لے کر جاتی ہے۔ {Analog signals} ہموار {Sine Wave} ہیں، جیسے انسانی آواز۔ {Digital signals} صرف دو سطحیں رکھتی ہیں، {Square Wave}، جیسے قلعے کی دیوار۔ {Analog} شور سے متاثر، {Digital} شور کے خلاف مضبوط۔ امتحان میں جدول اور دونوں لہریں کھینچنا آئے گا۔",
            "{Boolean Algebra} {George Boole} نے بنائی۔ صرف {TRUE} 1 اور {FALSE} 0۔ {AND}، {OR}، {NOT} بنیادی عمل ہیں۔ جال: Boolean میں جمع کا نشان {OR} ہے، جمع نہیں۔",
            "ڈرل: کتاب کے صفحات {Discrete} ہیں؛ 1 کا مطلب {ON}؛ ڈیجیٹل لہریں {Square Wave}؛ بانی {George Boole}۔",
        ),
    ),
    day(
        "xi", 2, 1, "Teach", "Computer Systems", "Computer Systems (2/5)",
        "Logic Gates (Basic Gates: AND, OR, NOT)", 7, 9,
        ["Boolean Operations", "Truth Tables", "Logic Gates (Basic Gates: AND, OR, NOT)", "Universal Logic Gates (NAND and NOR)"],
        T(
            "دن 02۔ ★ Golden: {Logic Gates (Basic Gates: AND, OR, NOT)}۔",
            "{AND} تب 1 جب تمام inputs 1 ہوں — دو تالے والا دروازہ۔ {OR} تب 1 جب کوئی ایک 1 ہو — دو دروازوں والا کمرہ۔ {NOT} الٹ کر دیتا ہے، inverter۔",
            "{Truth Table} ہر ممکن input اور اس کا output دکھاتی ہے۔ n inputs ہوں تو قطاریں 2 کی طاقت n۔ دو inputs کی چار قطاریں: 00، 01، 10، 11۔",
            "★ {Logic gates} الیکٹرانک سرکٹس ہیں جو Boolean عمل کرتے ہیں۔ {AND} کی شکل D، {OR} نوک دار، {NOT} مثلث پر bubble۔ شارٹ کٹ: {AND} صرف 11 پر 1؛ {OR} صرف 00 پر 0۔ امتحان: symbol، expression، {Truth Table}۔",
            "{NAND} یعنی {NOT AND}، {NOR} یعنی {NOT OR}۔ دونوں {Universal gates} ہیں — دنیا کا کوئی بھی منطق سرکٹ صرف {NAND} یا صرف {NOR} سے بن سکتا ہے۔ {NAND} {AND} کا الٹ، {NOR} {OR} کا الٹ۔",
            "ڈرل: {OR} کا نشان جمع؛ چار inputs کی table میں 16 قطاریں؛ A=0 B=0 پر {OR} صفر؛ universal اس لیے کہ صرف ان سے پورا سرکٹ بنتا ہے۔",
        ),
    ),
    day(
        "xi", 3, 1, "Teach", "Computer Systems", "Computer Systems (3/5)",
        "Logic Diagrams, Karnaugh Maps (K-Maps)", 10, 11,
        ["Advanced Logic Gates (XOR and XNOR)", "Logic Expressions, Minterms and Maxterms", "Logic Diagrams", "Karnaugh Maps (K-Maps)"],
        T(
            "دن 03۔ ★ Golden: {Logic Diagrams} اور {Karnaugh Maps (K-Maps)}۔",
            "{XOR} تب 1 جب inputs مختلف ہوں۔ {XNOR} تب 1 جب دونوں یکساں ہوں — مساوات کا گیٹ۔",
            "{Minterm} وہ حاصل ضرب ہے جو ایک قطار میں 1 دیتی ہے؛ {Maxterm} وہ حاصل جمع جو 0 دیتی ہے۔ Expression کو گیٹ کی تصویر بنانا {Logic Diagram} ہے۔ پہلے {NOT}، پھر {AND}، آخر میں {OR} — یا دیا گیا ترتیب۔",
            "★ {K-Map} {Truth Table} کو خانوں میں سمیٹتی ہے تاکہ سادہ گروپ ملیں۔ پڑوسی خانے صرف ایک {Bit} بدلتے ہیں، {Gray code}۔ گروپ 1، 2، 4، 8 کے طاقتوں میں، جتنا بڑا گروپ اتنی سادہ expression۔ امتحان میں 2 اور 3 variable {K-Map} لازمی ہے۔",
            "صفحے پر diagram اور {K-Map} جوں کے توں نقل کرو، پھر بند کتاب کھینچو۔",
        ),
    ),
    day(
        "xi", 4, 1, "Teach", "Computer Systems", "Computer Systems (4/5)",
        "Software Development Life Cycle (SDLC), The Waterfall Model", 12, 14,
        ["LogiSim Evolution: Simulation Tool", "Building a Circuit in LogiSim", "Software Development Life Cycle (SDLC)", "The Waterfall Model"],
        T(
            "دن 04۔ پہلے {LogiSim} سے سرکٹ بنا کر چلاؤ: گیٹ رکھو، تار جوڑو، input دے کر output دیکھو۔ یہ مشق ہے، ★ Golden {SDLC} اور {The Waterfall Model} ہیں۔",
            "{Software Development Life Cycle} سافٹ ویئر بنانے کے مرحلے ہیں۔ عام مراحل: {Requirement}، {Design}، {Implementation}، {Testing}، {Deployment}، {Maintenance}۔ ہر مرحلہ اگلے سے پہلے مکمل۔",
            "★ {Waterfall Model} ایک طرف بہتا پانی ہے: اوپر سے نیچے، واپس مشکل۔ فائدہ: ترتیب صاف، دستاویز مضبوط۔ نقصان: تبدیلی مہنگی، گاہک دیر سے دیکھتا ہے۔ چھوٹے، واضح منصوبوں کے لیے ٹھیک؛ بدلتے تقاضوں کے لیے کمزور۔",
            "پانچ نمبر: تعریف، مراحل کی فہرست، ایک فائدہ، ایک نقصان، ایک مثال۔",
        ),
    ),
    day(
        "xi", 5, 1, "Checkpoint", "Computer Systems", "Computer Systems (5/5)",
        "The Agile Model, Communication Models and the OSI 7-Layer Model", 15, 18,
        ["The Agile Model", "Waterfall vs Agile", "Communication Models and the OSI 7-Layer Model", "TCP/IP Model vs OSI Model", "Checkpoint Test"],
        T(
            "دن 05 {Checkpoint}۔ ★ Golden: {The Agile Model} اور {OSI 7-Layer Model}۔",
            "{Agile} چھوٹے چکر {Sprint} میں بناتا ہے، عموماً 2 سے 4 ہفتے۔ {Plan}، {Design}، {Build}، {Test}، {Review}، پھر دہراؤ۔ گاہک ہر {Sprint} کے بعد کام دیکھتا ہے۔ {Waterfall} سخت ترتیب؛ {Agile} لچک۔",
            "مواصلات کے ماڈل بتاتے ہیں ڈیٹا کیسے سفر کرتا ہے۔ ★ {OSI 7-Layer Model}: {Physical}، {Data Link}، {Network}، {Transport}، {Session}، {Presentation}، {Application}۔ یاد: Please Do Not Throw Sausage Pizza Away۔",
            "{TCP/IP} چار تہیں: {Network Access}، {Internet}، {Transport}، {Application}۔ {OSI} نمونہ ہے، {TCP/IP} عملی انٹرنیٹ۔",
            "چالیس منٹ کا ٹیسٹ بند کتاب۔ 60 فیصد سے کم تو کل صبح {Golden repair}، نیا باب نہیں۔",
        ),
    ),
    day(
        "xi", 6, 2, "Teach", "Computational Thinking & Algorithm", "Computational Thinking & Algorithm (1/3)",
        "Algorithm, Algorithm vs Pseudocode, Decomposition", 19, 21,
        ["Computational Thinking", "Algorithm", "Algorithm vs Pseudocode", "Decomposition", "Pattern Recognition"],
        T(
            "دن 06، باب {Computational Thinking & Algorithm}۔ ★ Golden: {Algorithm}، {Algorithm vs Pseudocode}، {Decomposition}۔",
            "{Computational Thinking} مسائل کو کمپیوٹر کے انداز میں توڑنا: {Decomposition}، {Pattern Recognition}، {Abstraction}، {Algorithm}۔",
            "★ {Algorithm} قدم بہ قدم ہدایات ہیں جو شروع، واضح قدم، اور اختتام رکھتی ہیں۔ کھانا پکانے کی ترکیب الگورتھم کی مثال ہے۔",
            "★ {Pseudocode} انگریزی نما ڈھانچہ ہے، مخصوص زبان نہیں۔ {Algorithm} سوچ ہے؛ {Pseudocode} اس سوچ کی لکھائی؛ حقیقی کوڈ {Python} وغیرہ۔",
            "★ {Decomposition} بڑے مسئلے کو چھوٹے حصوں میں توڑنا، جیسے امتحان کی تیاری کو ابواب میں بانٹنا۔ {Pattern Recognition} بار بار آنے والی شکل دیکھنا۔",
        ),
    ),
    day(
        "xi", 7, 2, "Teach", "Computational Thinking & Algorithm", "Computational Thinking & Algorithm (2/3)",
        "Sorting Algorithms: Bubble Sort, Sorting Algorithms: Selection Sort", 22, 24,
        ["Abstraction", "Sorting and Searching Algorithms", "Bubble Sort", "Selection Sort"],
        T(
            "دن 07۔ {Abstraction} غیر ضروری تفصیل چھپاتا ہے — کار چلاتے ہو، انجن کا ہر پیچ نہیں دیکھتے۔",
            "★ {Bubble Sort}: پڑوسی جوڑوں کا موازنہ، بڑا سامنے دھکیل دو، آخر تک {Pass}۔ n عناصر پر تقریباً n مربع موازنے۔ سادہ، سست۔",
            "★ {Selection Sort}: ہر {Pass} میں باقی فہرست کا سب سے چھوٹا چن کر اپنی جگہ لگاؤ۔ بھی n مربع، مگر swaps کم۔",
            "امتحان میں دونوں کے قدم، ایک چھوٹی فہرست پر کام، اور {Time complexity} پوچھتے ہیں۔ صفحے کی جدول جوں کی توں یاد کرو۔",
        ),
    ),
    day(
        "xi", 8, 2, "Checkpoint", "Computational Thinking & Algorithm", "Computational Thinking & Algorithm (3/3)",
        "Searching Algorithms: Binary Search", 25, 28,
        ["Linear Search", "Binary Search", "Evaluation Criteria of Algorithms", "Checkpoint Test"],
        T(
            "دن 08 {Checkpoint}۔ ★ Golden: {Binary Search}۔",
            "{Linear Search} شروع سے آخر تک ایک ایک دیکھتا ہے — انارکی الماری۔ ترتیب ضروری نہیں۔ بدترین صورت n قدم۔",
            "★ {Binary Search} صرف ترتیب شدہ فہرست پر۔ درمیان دیکھو: برابر تو مل گیا؛ چھوٹا ہو تو دائیں نصف، بڑا ہو تو بائیں نصف۔ ہر بار آدھا۔ پیچیدگی {O(log n)}۔",
            "الگورتھم جانچو: درستگی، وضاحت، رفتار، یادداشت۔ چالیس منٹ کا باب ٹیسٹ بند کتاب۔ {Binary Search} کی تعریف، شرط، اور مثال لازمی لکھو۔",
        ),
    ),
    day(
        "xi", 9, 2, "Teach", "Programming Fundamentals", "Programming Fundamentals (1/5)",
        "none — still copy every table", 29, 31,
        ["Programming", "Programming Language Types", "Career Growth with Python", "Integrated Development Environment"],
        T(
            "دن 09، باب {Programming Fundamentals}۔ آج ★ Golden الگ نہیں، ہر جدول نقل کرو۔",
            "{Programming} کمپیوٹر کو ہدایات دینا۔ زبانیں: {Low-level} مشین کے قریب، {High-level} انسان کے قریب جیسے {Python}۔ {Compiled} پہلے مشین کوڈ بناتی ہیں، {Interpreted} لائن بہ لائن چلتی ہیں؛ {Python} interpreted ہے۔",
            "{Python} سادہ نحو، سائنس، ویب، {AI} میں کام۔ {IDE} وہ سافٹ ویئر ہے جہاں لکھتے، چلاتے، غلطی دیکھتے ہو — {VS Code}، {PyCharm}، {IDLE}۔",
            "کل ★ {Variables} اور {Data Types} آئیں گے۔ آج کی لغت زبانی ہو۔",
        ),
    ),
    day(
        "xi", 10, 2, "Teach", "Programming Fundamentals", "Programming Fundamentals (2/5)",
        "Fundamentals of Python Programming, Variables, Data Types in Python, Operators and Operands: Arithmetic and Assignment",
        32, 34,
        ["Fundamentals of Python Programming", "Variables", "Data Types in Python", "Input and Output Handling", "Arithmetic and Assignment Operators"],
        T(
            "دن 10۔ ★ Golden: {Python} کی بنیاد، {Variables}، {Data Types}، {Arithmetic} اور {Assignment}۔",
            "{Python} انڈینٹیشن سے بلاک بناتا ہے۔ نام کیس حساس۔ {print} دکھاتا ہے، {input} پوچھتا ہے۔",
            "{Variable} نام والا ڈبہ۔ {int} عدد، {float} اعشاری، {str} متن، {bool} {True} یا {False}۔ {type()} قسم بتاتا ہے۔",
            "عمل: جمع، تفریق، ضرب، تقسیم، {//} مکمل تقسیم، {%} باقی، {**} طاقت۔ {Assignment} = قیمت رکھتا ہے؛ {+=} پرانی میں جمع۔ {Operand} وہ قیمت جس پر عمل ہو، {Operator} خود عمل۔",
        ),
    ),
    day(
        "xi", 11, 3, "Teach", "Programming Fundamentals", "Programming Fundamentals (3/5)",
        "Relational, Logical and Membership Operators, Bitwise Operators, Control Structures, Selection Statements: if and if-else",
        35, 37,
        ["Relational, Logical and Membership Operators", "Bitwise Operators", "Control Structures", "Sequence", "Selection Statements: if and if-else"],
        T(
            "دن 11۔ ★ Golden: موازنہ، منطقی، {Membership}، {Bitwise}، {Control Structures}، {if} اور {if-else}۔",
            "تقابلی: == != < > <= >= نتیجہ {bool}۔ منطقی: {and} دونوں سچ، {or} کوئی ایک، {not} الٹ۔ {in} اور {not in} رکنیت۔",
            "{Bitwise} {AND} {OR} {XOR} {NOT} شفٹ — بٹس پر۔ {Control structure} تین: {Sequence} سیدھا، {Selection} انتخاب، {Repetition} دہراؤ۔",
            "{if} شرط سچ ہو تو بلاک۔ {if-else} دو راستے۔ امتحان میں فلو چارٹ اور ایک چھوٹا کوڈ دونوں مانگتے ہیں۔",
        ),
    ),
    day(
        "xi", 12, 3, "Teach", "Programming Fundamentals", "Programming Fundamentals (4/5)",
        "Selection Statements: if-elif-else and Nested if, Repetition Statements: the for Loop and range(), The while Loop, break and continue, Nested Loops",
        38, 40,
        ["if-elif-else and Nested if", "for Loop and range()", "while Loop", "break and continue", "Nested Loops and for vs while"],
        T(
            "دن 12۔ ★ Golden: {if-elif-else}، {Nested if}، {for}، {range()}، {while}، {break}، {continue}۔",
            "کئی شرطیں ہوں تو {elif} زنجیر۔ اندر {if} {Nested if}۔",
            "{for} معلوم تکرار: {for i in range(5)}۔ {range(start, stop, step)} stop شامل نہیں۔ {while} جب تک شرط سچ، احتیاط {Infinite loop} سے۔",
            "{break} لوپ توڑتا ہے، {continue} یہ چکر چھوڑ کر اگلا۔ اندر لوپ {Nested}۔ جانیں کب {for}، کب {while} — گنتی معلوم ہو تو {for}، شرط پر رکنا ہو تو {while}۔",
        ),
    ),
    day(
        "xi", 13, 3, "Checkpoint", "Programming Fundamentals", "Programming Fundamentals (5/5)",
        "none — still copy every table", 41, 44,
        ["Libraries in Python", "Built-in Libraries", "Third-Party Libraries", "Debugging Code in Python", "Checkpoint Test"],
        T(
            "دن 13 {Checkpoint}۔ لائبریریاں تیار اوزار ہیں۔ {Built-in} جیسے {math}، {random} {import} سے آتی ہیں۔ {Third-party} جیسے {numpy} الگ نصب۔",
            "{Debugging}: پیغام پڑھو، لائن دیکھو، {print} سے قیمت چیک کرو، منطقی غلطی الگ، نحوی غلطی الگ۔",
            "چالیس منٹ باب ٹیسٹ۔ {Variable}، {if-else}، {for}، {while}، عمل کے نشان زبانی ہوں۔ 60 فیصد سے کم تو {Golden repair}۔",
        ),
    ),
    day(
        "xi", 14, 3, "Teach", "Data and Analysis", "Data and Analysis (1/3)",
        "Keys and Integrity Constraints", 45, 46,
        ["Data, Information and Database", "Database Management System (DBMS)", "Database Components", "Keys and Integrity Constraints"],
        T(
            "دن 14، باب {Data and Analysis}۔ {Data} خام حقائق، {Information} پروسیس شدہ فیصلے کی بات۔ {Database} منظم متعلقہ ڈیٹا۔ {DBMS} وہ سافٹ ویئر جو اسے سنبھالے، تکرار کم کرے۔",
            "اجزاء: {Table}، {Record} قطار، {Field} کالم، {Query}، {Form}، {Report}۔",
            "★ {Keys}: {Primary Key} قطار کی منفرد پہچان، خالی نہیں۔ {Foreign Key} دوسری جدول کے {Primary Key} کی طرف اشارہ۔ {Integrity Constraints} اصول ہیں جو غلط ڈیٹا روکیں: {Entity}، {Referential}، {Domain}۔",
        ),
    ),
    day(
        "xi", 15, 3, "Teach", "Data and Analysis", "Data and Analysis (2/3)",
        "Entity Relationship Model (ER-Model), Referential Integrity", 47, 49,
        ["Entity Relationship Model (ER-Model)", "Referential Integrity", "Relational Schema Development", "Case Study"],
        T(
            "دن 15۔ ★ Golden: {ER-Model} اور {Referential Integrity}۔",
            "{Entity} حقیقی چیز، {Attribute} اس کی صفت، {Relationship} ربط۔ {ER} ڈایاگرام مستطیل وجود، بیضوی صفت، ہیرے رشتہ۔ {One-to-One}، {One-to-Many}، {Many-to-Many}۔",
            "★ {Referential Integrity}: {Foreign Key} کی قیمت یا تو خالی یا موجود {Primary Key} سے ملے۔ یتیم ریکارڈ منع۔ {Relational Schema} جدولوں، کنجوں، رشتوں کی لکھائی۔ کیس سٹڈی صفحے پر جوں کی توں کھینچو۔",
        ),
    ),
    day(
        "xi", 16, 4, "Checkpoint", "Data and Analysis", "Data and Analysis (3/3)",
        "Creating Queries in MS Access", 50, 53,
        ["Creation of Tables in Microsoft Access", "Designing Forms", "Creating Queries in MS Access", "Data Reports", "Checkpoint Test"],
        T(
            "دن 16 {Checkpoint}۔ {MS Access} میں جدول {Design View} سے فیلڈ اور {Data Type}، ایک {Primary Key}۔ {Form} اندراج کی کھڑکی۔",
            "★ {Query} سوال ہے جو قطار چنتا ہے۔ {Select Query} دکھاتا ہے، معیار سے چھانتا ہے۔ {SQL} میں {SELECT}، {FROM}، {WHERE}۔ رپورٹ چھپی شکل۔",
            "چالیس منٹ ٹیسٹ۔ کنج، {ER}، {Referential Integrity}، {Query} ★ Golden ہیں۔",
        ),
    ),
    day(
        "xi", 17, 4, "Teach", "Application and Impacts of Computing", "Application and Impacts of Computing (1/3)",
        "Artificial Intelligence (AI), Internet of Things (IoT) & Components", 54, 56,
        ["Introduction to Computing Impacts", "Artificial Intelligence (AI)", "Internet of Things (IoT) & Components"],
        T(
            "دن 17۔ ★ Golden: {Artificial Intelligence (AI)} اور {Internet of Things (IoT)}۔",
            "کمپیوٹنگ صحت، تعلیم، کاروبار، شہر بدل رہی ہے۔",
            "★ {AI} مشین کو انسانی سوچ کے قریب کام سکھانا: پہچان، فیصلہ، زبان۔ مثال: نقشے کی سفارش، چہرے کی پہچان۔ {Narrow AI} ایک کام؛ عام انسانی {AI} ابھی تحقیق۔",
            "★ {IoT} وہ چیزیں جو سینسر اور انٹرنیٹ سے آپس میں بات کریں۔ اجزاء: {Sensor}، {Actuator}، {Connectivity}، {Processor}، {User Interface}، کلاؤڈ۔ اسمارٹ پنکھا، اسمارٹ میٹر۔ دونوں اصطلاحیں انگریزی میں جوں کی توں لکھو۔",
        ),
    ),
    day(
        "xi", 18, 4, "Teach", "Application and Impacts of Computing", "Application and Impacts of Computing (2/3)",
        "Information Sources (Primary, Secondary, Tertiary)", 57, 58,
        ["Uses of IoT", "Scope of AI in Education in Pakistan", "Career Connection in IoT and AI", "Information Sources (Primary, Secondary, Tertiary)"],
        T(
            "دن 18۔ {IoT} کھیتی، صحت، گھر، ٹریفک میں۔ پاکستان کی تعلیم میں {AI} مشق، ترجمہ، حاضری میں مدد دے سکتا ہے، مگر ڈیٹا اور استاد کی تربیت چاہیے۔",
            "★ {Information Sources}: {Primary} اصل، جیسے انٹرویو، سروے، تجربہ۔ {Secondary} کسی کا خلاصہ، جیسے درسی کتاب، مضمون۔ {Tertiary} فہرست اور انسائیکلوپیڈیا جو دونوں کی رہنمائی کرے۔ امتحان میں تینوں کی تعریف اور ایک ایک مثال۔",
        ),
    ),
    day(
        "xi", 19, 4, "Checkpoint", "Application and Impacts of Computing", "Application and Impacts of Computing (3/3)",
        "Assistive Technologies", 59, 62,
        ["Impacts of Computing in Various Fields", "Assistive Technologies", "Importance of Assistive Technologies", "Career Connection", "Checkpoint Test"],
        T(
            "دن 19 {Checkpoint}۔ ★ Golden: {Assistive Technologies}۔",
            "کمپیوٹنگ کے مثبت اور منفی اثر لکھنا آئے: رفتار، ملازمت، رازداری۔",
            "★ {Assistive Technologies} وہ اوزار جو معذوری والے شخص کو کمپیوٹر اور دنیا استعمال کرنے دیں: اسکرین ریڈر، بریل ڈسپلے، آواز سے ٹائپ، سوئچ۔ اہمیت: برابر رسائی، عزت، قانون اور اخلاق۔",
            "چالیس منٹ ٹیسٹ۔ {AI}، {IoT} اجزاء، مصادر کی تین اقسام، {Assistive Technologies}۔",
        ),
    ),
    day(
        "xi", 20, 4, "Teach", "Digital Literacy", "Digital Literacy (1/4)",
        "Types of Data, Data-Collection Strategies, Interviews and Surveys", 63, 65,
        ["Introduction to Digital Literacy", "Digital Literacy in the Information Age", "Types of Data", "Data-Collection Strategies", "Interviews and Surveys"],
        T(
            "دن 20، باب {Digital Literacy}۔ یہ تلاش، جانچ، اور ڈیٹا سے بات بنانے کی صلاحیت ہے۔",
            "★ {Types of Data}: {Qualitative} الفاظ اور رائے، {Quantitative} عدد۔ {Primary} خود اکٹھا، {Secondary} پہلے سے موجود۔",
            "★ حکمت عملی: سوال، مشاہدہ، تجربہ، دستاویز۔ ★ {Interview} گہری بات، کم لوگوں سے۔ {Survey} ایک جیسے سوال، زیادہ لوگوں سے۔ سوال متعصب نہ ہو، نمونہ واضح ہو۔",
        ),
    ),
    day(
        "xi", 21, 5, "Teach", "Digital Literacy", "Digital Literacy (2/4)",
        "Prototypes, Observation and Simulations, Primary and Secondary Data", 66, 67,
        ["Prototypes, Observation and Simulations", "Primary and Secondary Data", "Designing a Data-Collection Plan"],
        T(
            "دن 21۔ ★ Golden: {Prototypes}، {Observation}، {Simulations}، {Primary} اور {Secondary Data}۔",
            "{Prototype} ابتدائی ماڈل تاکہ خیال آزمایا جائے۔ {Observation} دیکھ کر ریکارڈ۔ {Simulation} نقل تاکہ خطرے کے بغیر سیکھیں۔",
            "{Primary} نیا، مہنگا، درست سوال پر۔ {Secondary} سستا، تیز، مگر مقصد دوسرا ہو سکتا ہے۔ منصوبہ: سوال، آبادی، اوزار، اخلاق، اجازت۔",
        ),
    ),
    day(
        "xi", 22, 5, "Teach", "Digital Literacy", "Digital Literacy (3/4)",
        "Case Study: Digital Inquiry Project, Steps 1 – 3: Advanced Search and Methodology, Steps 4 – 6: Survey Preparation and Primary Data Collection",
        68, 70,
        ["Infographics and Reports", "Case Study: Digital Inquiry Project", "Steps 1-3 Advanced Search and Methodology", "Steps 4-6 Survey Preparation and Primary Data Collection"],
        T(
            "دن 22۔ ★ Golden: {Digital Inquiry Project} اور اس کے پہلے چھ قدم۔",
            "{Infographic} تصویر میں خلاصہ، رپورٹ تفصیل۔",
            "قدم 1 سے 3: سوال، {Advanced Search}، طریقہ کار — کلیدی الفاظ، معتبر ویب، حوالہ۔ قدم 4 سے 6: سروے کے سوال، اجازت، {Primary Data} اکٹھا۔ کیس سٹڈی کے قدم صفحے پر جوں کے توں یاد کرو۔",
        ),
    ),
    day(
        "xi", 23, 5, "Checkpoint", "Digital Literacy", "Digital Literacy (4/4)",
        "Steps 7 – 9: Secondary Data and Spreadsheet Organisation, Steps 10 – 12: Data Analysis, Conclusion and Recommendations, The Final Digital Artefact",
        71, 74,
        ["Steps 7-9 Secondary Data and Spreadsheet", "Steps 10-12 Analysis, Conclusion, Recommendations", "The Final Digital Artefact", "Checkpoint Test"],
        T(
            "دن 23 {Checkpoint}۔ ★ Golden: قدم 7 سے 12 اور {Digital Artefact}۔",
            "7 سے 9: {Secondary Data}، اسپریڈ شیٹ میں کالم، صفائی، چارٹ۔ 10 سے 12: تجزیہ، نتیجہ، سفارش۔ آخری {Digital Artefact} وہ فائل ہے جو ثبوت، چارٹ اور حوالے جوڑے۔",
            "کیریئر جدول صفحے پر ہے: تحقیق، صحافت، تجزیہ — سب یہی مہارت۔ چالیس منٹ ٹیسٹ۔",
        ),
    ),
    day(
        "xi", 24, 5, "Golden blitz", "Chapters 1–2", "★ only · Chapters 1–2",
        "14 Golden cards", 75, 81,
        ["Analog and Digital Signals", "Logic Gates", "Logic Diagrams", "K-Maps", "SDLC", "Waterfall", "Agile", "OSI 7-Layer", "Algorithm", "Pseudocode", "Decomposition", "Bubble Sort", "Selection Sort", "Binary Search"],
        T(
            "دن 24 {Golden blitz}، باب 1 اور 2۔ نیا غیر گولڈن موضوع نہیں۔ ہر جدول یاد سے لکھو۔",
            "زبانی سلسلہ: {Analog} ہموار، {Digital} دو سطح۔ {AND} {OR} {NOT}۔ {K-Map} گروپ۔ {SDLC} مراحل۔ {Waterfall} نیچے، {Agile} {Sprint}۔ سات تہہ {OSI}۔ {Algorithm} قدم، {Pseudocode} لکھائی، {Decomposition} توڑ۔ {Bubble} پڑوسی، {Selection} سب سے چھوٹا، {Binary Search} آدھا آدھا، ترتیب لازم۔",
            "ایک ★ موضوع پر پانچ نمبر {Define Explain Example Diagram Working}۔",
        ),
    ),
    day(
        "xi", 25, 6, "Golden blitz", "Chapters 3–4", "★ only · Chapters 3–4",
        "16 Golden cards", 82, 88,
        ["Python fundamentals", "Variables", "Data Types", "Operators", "Control Structures", "if and loops", "Keys and Integrity", "ER-Model", "Referential Integrity", "Queries in MS Access"],
        T(
            "دن 25 {Golden blitz} باب 3 اور 4۔ {Python} کی قسمیں، عمل، {if} {for} {while} یاد سے کوڈ لکھو۔",
            "{Primary Key} منفرد، {Foreign Key} ربط، {ER} شکل، {Referential Integrity} یتیم ریکارڈ منع، {Query} سوال۔ ہر گولڈن کارڈ کی جدول بند آنکھوں سے۔",
        ),
    ),
    day(
        "xi", 26, 6, "Golden blitz", "Chapters 5–6", "★ only · Chapters 5–6",
        "15 Golden cards", 89, 95,
        ["AI", "IoT & Components", "Information Sources", "Assistive Technologies", "Types of Data", "Data-Collection", "Interviews and Surveys", "Prototypes", "Primary and Secondary Data", "Digital Inquiry steps"],
        T(
            "دن 26 {Golden blitz} باب 5 اور 6۔ {AI} تعریف، {IoT} اجزاء کی فہرست، مصادر کی تین اقسام مثال سمیت، {Assistive Technologies} ایک آلہ ایک فائدہ۔",
            "ڈیٹا کی اقسام، انٹرویو بمقابلہ سروے، {Prototype}، {Primary} {Secondary}، انکوائری کے بارہ قدم تین تین کے گروپ میں زبانی۔",
        ),
    ),
    day(
        "xi", 27, 6, "Recap", "All chapters", "Say every chapter recap aloud, book closed",
        "All chapters", 96, 97,
        ["Chapter 1 Computer Systems", "Chapter 2 Computational Thinking & Algorithm", "Chapter 3 Programming Fundamentals", "Chapter 4 Data and Analysis", "Chapter 5 Application and Impacts", "Chapter 6 Digital Literacy"],
        T(
            "دن 27 {Recap}۔ کتاب بند، ہر باب بلند آواز۔",
            "باب 1: مقدار، سگنل، گیٹ، {SDLC}، {OSI}۔ باب 2: سوچ، الگورتھم، ترتیب، تلاش۔ باب 3: {Python}، متغیر، کنٹرول۔ باب 4: ڈیٹا بیس، کنج، {ER}، {Query}۔ باب 5: {AI} {IoT} مصادر امدادی ٹیک۔ باب 6: ڈیجیٹل خواندگی اور انکوائری کے قدم۔ جو رکا، لکھ کر پھر کہو۔",
        ),
    ),
    day(
        "xi", 28, 6, "Mock", "Whole syllabus", "2 hours 30 minutes · 75 marks · no notes",
        "Whole syllabus", 98, 100,
        ["Mock paper hall conditions"],
        T(
            "دن 28 {Mock}۔ ڈھائی گھنٹے، 75 نمبر، نوٹس نہیں، فون نہیں، دن 29 کی کلید نہیں۔ ہال کی شرط۔ وقت بانٹو: MCQ تیز، گولڈن سوال جدول اور ڈایاگرام سے۔ ختم پر نام اور صفحہ گنو۔",
        ),
    ),
    day(
        "xi", 29, 6, "Mark", "Missed Goldens", "Mark to the key. List every ★ Golden you missed.",
        "Missed Goldens", 101, 102,
        ["Mark the mock", "Repair list of missed Goldens"],
        T(
            "دن 29 marking۔ کلید سے میل کھاؤ۔ ہر ★ {Golden} جس پر صفر یا آدھا نمبر آیا repair list میں لکھو: موضوع، کیا رہ گیا۔ کل صرف یہی فہرست۔ نیا باب مت کھولو۔",
        ),
    ),
    day(
        "xi", 30, 6, "Repair", "Missed Goldens only", "Redo the Day 29 list only. Sleep by 10 pm.",
        "Missed Goldens only", 103, 103,
        ["Redo Day 29 list", "Sleep by 10 pm"],
        T(
            "دن 30 {Repair}۔ صرف دن 29 کی فہرست: تعریف کہو، جدول کھینچو، مثال دو۔ شام چھ بجے رک جاؤ۔ دس بجے سو جاؤ۔ نیا موضوع حرام۔ قلم، پیمانہ، اور گولڈن کارڈز سر میں لے کر جاؤ، ہال میں کتاب نہیں۔",
        ),
    ),
]

XII = [
    day(
        "xii", 1, 1, "Teach", "Computer Systems (HCI)", "Computer Systems (HCI) (1/4)",
        "Applications of HCI (Domains of Life)", 108, 110,
        ["Fundamentals of Human-Computer Interaction", "Traditional Interaction and Natural Interaction", "Applications of HCI (Domains of Life)"],
        T(
            "السلام علیکم۔ {Class XII} دن 01، باب {Computer Systems (HCI)}۔ {HCI} انسان اور کمپیوٹر کے درمیان بات چیت کا علم ہے۔",
            "روایتی تعامل کی بورڈ ماؤس؛ {Natural Interaction} چھونا، بولنا، اشارہ۔",
            "★ {Applications of HCI} چار روزمرہ میدان: {healthcare}، {banking}، {education}، {networking}۔ صحت میں ریکارڈ، بینک میں ایپ، کلاس میں بورڈ، میسج میں چیٹ — سب انٹرفیس ہے۔ امتحان میں چار میدان اور ایک ایک مثال۔",
        ),
    ),
    day(
        "xii", 2, 1, "Teach", "Computer Systems (HCI)", "Computer Systems (HCI) (2/4)",
        "Importance of HCI", 111, 112,
        ["Types of User Interaction", "Interface Types, Environment and Feedback", "Importance of HCI", "Accessibility Principles"],
        T(
            "دن 02۔ تعامل: کمانڈ، مینو، فارم، قدرتی۔ انٹرفیس، ماحول، {Feedback} — نظام جواب دے۔",
            "★ {Importance of HCI}: مشین قریب اور قابلِ استعمال بنے، پیچیدہ ٹیک روزمرہ اوزار بنے۔ غلط {HCI} غلط دوا، غلط رقم۔ {Accessibility} سب کے لیے: تضاد، بڑا متن، کی بورڈ، اسکرین ریڈر۔",
        ),
    ),
    day(
        "xii", 3, 1, "Teach", "Computer Systems (HCI)", "Computer Systems (HCI) (3/4)",
        "Human-Computer Interaction Problems, User Interface Design (UI vs UX)", 113, 115,
        ["Need Analysis for Interface Design", "Human-Computer Interaction Problems", "Methods for Improving HCI", "User Interface Design (UI vs UX)"],
        T(
            "دن 03۔ ★ Golden: مسائل اور {UI vs UX}۔",
            "ضرورت کا تجزیہ: صارف کون، کام کیا، رکاوٹ کیا۔ مسائل: الجھا مینو، چھوٹا بٹن، کم {Feedback}، سست جواب، زبان مشکل۔ بہتری: صارف کی جانچ، سادہ لیبل، مستقل رنگ۔",
            "★ {UI} دکھائی دینے والے بٹن رنگ آئیکن — کپڑے۔ {UX} پورا سفر — دن کیسا گزرا۔ امتحان: فرق اور مثال۔ بٹن {UI} ہے؛ فارم تین منٹ میں جمع ہو جانا {UX} ہے۔",
        ),
    ),
    day(
        "xii", 4, 1, "Checkpoint", "Computer Systems (HCI)", "Computer Systems (HCI) (4/4)",
        "Testing Methods (Usability, A/B, Automated)", 116, 119,
        ["Wireframing, Figma and Prototypes", "Test and Evaluate HCI", "Testing Methods (Usability, A/B, Automated)", "Checkpoint Test"],
        T(
            "دن 04 {Checkpoint}۔ {Wireframe} سادہ خانے، {Figma} سے {Prototype}۔",
            "★ تین جانچ: {Usability} وقت شدہ کام — صارف کر سکتا ہے؟ {A/B} دو نسخے، کون جیتا؟ {Automated} بوٹ ٹوٹا لنک اور کم تضاد ڈھونڈے۔ آٹھ نمبر پر سات قطار جدول۔ چالیس منٹ ٹیسٹ۔",
        ),
    ),
    day(
        "xii", 5, 1, "Teach", "Computational Thinking & Algorithms", "Computational Thinking & Algorithms (1/5)",
        "Trace Tables, Comparing Trace Tables and Stepwise Reasoning", 120, 122,
        ["Analyze algorithms for correctness", "Trace Tables", "Stepwise Reasoning", "Comparing Trace Tables"],
        T(
            "دن 05۔ الگورتھم کی درستگی جانچنی ہے۔",
            "★ {Trace Table} ہر قدم پر متغیر کی قیمت لکھتی ہے۔ کالم نام، قطاریں قدم۔",
            "{Stepwise Reasoning} الفاظ میں کیوں یہ قدم۔ دونوں کا موازنہ: جدول نمبر دکھاتی ہے، استدلال وجہ۔ امتحان میں دیے کوڈ کی {Trace Table} بھرو۔",
        ),
    ),
    day(
        "xii", 6, 2, "Teach", "Computational Thinking & Algorithms", "Computational Thinking & Algorithms (2/5)",
        "Number of Steps (Big O Notation)", 123, 125,
        ["Modularity", "Readability", "Assess Algorithm Efficiency", "Number of Steps (Big O Notation)", "Number of Conditions"],
        T(
            "دن 06۔ {Modularity} حصوں میں توڑنا، {Readability} پڑھنے کے لائق نام۔",
            "کارکردگی: وقت اور یادداشت۔ ★ {Big O Notation} بدترین بڑھنے کی شرح۔ {O(1)} مستقل، {O(n)} لکیری، {O(n^2)} مربع جیسے {Bubble Sort}، {O(log n)} جیسے {Binary Search}۔ شرطوں کی گنتی بھی لاگت ہے۔ امتحان میں دیے لوپ کی {Big O} بتاؤ۔",
        ),
    ),
    day(
        "xii", 7, 2, "Teach", "Computational Thinking & Algorithms", "Computational Thinking & Algorithms (3/5)",
        "Concept of Data Structure", 126, 128,
        ["Number of Repetitions", "The Efficiency Evaluation Framework", "Refinements", "Concept of Data Structure"],
        T(
            "دن 07۔ تکرار کی گنتی لوپ سے۔ {Efficiency Evaluation Framework}: درستگی، وضاحت، قدم، یادداشت، پھر بہتری۔",
            "★ {Data Structure} ڈیٹا رکھنے کا منظم طریقہ۔ انتخاب الگورتھم کی رفتار بدل دیتا ہے۔ فہرست، ڈھیر، قطار — کل تفصیل۔ آج تعریف: نام، ترتیب، آپریشن۔",
        ),
    ),
    day(
        "xii", 8, 2, "Teach", "Computational Thinking & Algorithms", "Computational Thinking & Algorithms (4/5)",
        "Linear Data Structures: Stack, Linear Data Structures: Queue", 129, 131,
        ["Linked List", "Stack", "Queue"],
        T(
            "دن 08۔ {Linked List} گرہ اور اگلے کا اشارہ، درمیان میں داخل آسان۔",
            "★ {Stack} {LIFO} — آخر میں آیا پہلے نکلے۔ {Push} رکھو، {Pop} نکالو، {Peek} دیکھو۔ مثال: ان ڈو، پلیٹوں کا ڈھیر۔",
            "★ {Queue} {FIFO} — پہلے آیا پہلے نکلے۔ {Enqueue} پیچھے، {Dequeue} آگے۔ مثال: ٹکٹ لائن، پرنٹر۔ امتحان میں دونوں کا فرق اور ڈایاگرام۔",
        ),
    ),
    day(
        "xii", 9, 2, "Checkpoint", "Computational Thinking & Algorithms", "Computational Thinking & Algorithms (5/5)",
        "none — still copy every table", 132, 135,
        ["Operations on Data Structures", "Identify data structures in scenarios", "Trace data retrieval in Array, List", "Checkpoint Test"],
        T(
            "دن 09 {Checkpoint}۔ آپریشن: {Insert}، {Delete}، {Search}، {Traverse}، {Update}۔ منظر میں پہچانو: آخر سے ان ڈو {Stack}، لائن {Queue}، ترتیب اشاریہ {Array}۔",
            "{Array} اور List سے قدر نکالنے کی {Trace} صفحے پر کرو۔ چالیس منٹ ٹیسٹ۔ {Trace Table}، {Big O}، {Stack}، {Queue} لازمی۔",
        ),
    ),
    day(
        "xii", 10, 2, "Teach", "Programming Fundamentals", "Programming Fundamentals (1/4)",
        "Lists (Ordered, Mutable, Methods), Tuples (Ordered, Immutable), Dictionaries (Key-Value Pairs)",
        136, 139,
        ["Data Structures in Python", "Lists", "Tuples", "Sets", "Dictionaries"],
        T(
            "دن 10۔ ★ Golden: {List}، {Tuple}، {Dictionary}۔",
            "{List} مرتب، {Mutable}، مربع بریکٹ۔ {append} {insert} {remove} {sort}۔ {Tuple} مرتب، {Immutable}، گول بریکٹ — تبدیل نہیں، ریکارڈ کے لیے۔ {Set} غیر مرتب منفرد۔",
            "★ {Dictionary} {Key-Value Pairs}، curly braces۔ کلید منفرد، قدر کچھ بھی۔ {student['name']}۔ امتحان میں تینوں کا فرق جدول۔",
        ),
    ),
    day(
        "xii", 11, 3, "Teach", "Programming Fundamentals", "Programming Fundamentals (2/4)",
        "Functions in Python", 140, 142,
        ["Common Built-in Functions", "Activity: Student Attendance System", "Activity: Word tools", "Functions in Python"],
        T(
            "دن 11۔ {min} {max} {len} {sum} تیار افعال۔ سرگرمیوں میں حاضری اور الفاظ۔",
            "★ {Function} نام والا بلاک، {def} سے۔ پیرامیٹر ان پٹ، جسم کام، بار بار بلاؤ۔ فائدہ: {Decomposition}، کم تکرار، جانچ آسان۔ خالی جسم میں {pass}۔",
        ),
    ),
    day(
        "xii", 12, 3, "Teach", "Programming Fundamentals", "Programming Fundamentals (3/4)",
        "File Handling and Operations (Modes r, w, a)", 143, 144,
        ["Functions with Return Values", "Arithmetic Calculator Using Functions", "Scope of Local and Global Variables", "File Handling and Operations (Modes r, w, a)"],
        T(
            "دن 12۔ {return} جواب باہر بھیجتا ہے۔ کیلکولیٹر افعال میں توڑو۔ {Local} فنکشن کے اندر، {Global} باہر؛ اندر والا باہر نہیں بدلتا جب تک {global} نہ کہو۔",
            "★ فائل موڈ: {r} پڑھنا، فائل ہونی چاہیے۔ {w} لکھنا، پرانی مٹے۔ {a} آخر میں جوڑنا۔ {read} {write} {close} یاد رکھو۔ کل {with} آئے گا۔",
        ),
    ),
    day(
        "xii", 13, 3, "Checkpoint", "Programming Fundamentals", "Programming Fundamentals (4/4)",
        "The with Statement (Context Manager)", 145, 148,
        ["The with Statement (Context Manager)", "Errors and Exceptions (Try-Except)", "Mini File Handling", "Checkpoint Test"],
        T(
            "دن 13 {Checkpoint}۔ ★ {with} {Context Manager} فائل خود بند کرتا ہے، بھول نہیں ہوتی: {with open('data.txt') as f}۔",
            "{try} خطرناک کام، {except} غلطی پکڑو تاکہ پروگرام نہ گرے۔ چالیس منٹ ٹیسٹ: {List Tuple Dictionary}، {def}، موڈ {r w a}، {with}۔",
        ),
    ),
    day(
        "xii", 14, 3, "Teach", "Data and Analysis", "Data and Analysis (1/2)",
        "Data Sources and Database Connection, Pandas and DataFrames, Handling Missing Values (NaN)",
        149, 150,
        ["Concept of Data Analysis", "Data Sources and Database Connection", "Creating a SQLite Database in Python", "Pandas and DataFrames", "Handling Missing Values (NaN)"],
        T(
            "دن 14۔ تجزیہ: صفائی، خلاصہ، فیصلہ۔",
            "★ ماخذ اور کنکشن: {CSV}، {SQLite}، {API}۔ {Python} میں {sqlite3} سے ڈیٹا بیس۔",
            "★ {Pandas} کا {DataFrame} جدول ہے۔ {read_csv}، سر، قطار۔ ★ خالی جگہ {NaN}۔ {dropna} ہٹاؤ، {fillna} بھرو۔ امتحان میں تینوں گولڈن ایک ساتھ آ سکتے ہیں۔",
        ),
    ),
    day(
        "xii", 15, 3, "Checkpoint", "Data and Analysis", "Data and Analysis (2/2)",
        "Data Visualization and Types of Graphs, Descriptive Statistics", 151, 154,
        ["Data Organization and Representation", "Data Visualization and Types of Graphs", "Descriptive Statistics", "Career Opportunities", "Checkpoint Test"],
        T(
            "دن 15 {Checkpoint}۔ ★ چارٹ: {Bar} موازنہ، {Line} وقت، {Pie} حصہ، {Histogram} پھیلاؤ، {Scatter} تعلق۔ غلط چارٹ غلط کہانی۔",
            "★ {Descriptive Statistics}: {mean} اوسط، {median} درمیانی، {mode} سب سے عام، {range}، {min} {max}۔ کیریئر: تجزیہ کار، تحقیق۔ چالیس منٹ ٹیسٹ۔",
        ),
    ),
    day(
        "xii", 16, 4, "Teach", "Application and Impacts of Computing", "Application and Impacts of Computing (1/4)",
        "Neural Networks (NN), Components of Neural Networks", 155, 157,
        ["Machine Learning, Neural Networks and Deep Learning", "Machine Learning (ML)", "Neural Networks (NN)", "Deep Learning", "Components of Neural Networks"],
        T(
            "دن 16۔ {AI} بڑا چھتا، اس میں {Machine Learning}، اس میں {Deep Learning}۔ {ML} مثالوں سے قاعدہ سیکھتا ہے۔",
            "★ {Neural Network} دماغ کے نیوران کی نقل۔ ★ اجزاء: {Input layer}، {Hidden layers}، {Output layer}، {Weights}، {Bias}، {Activation function}، {Loss}، {Training}۔ نیوران: وزنی جمع جمع {bias}، پھر activation۔ {Deep} یعنی کئی hidden تہیں۔ آٹھ نام ایک ایک سطر امتحان کا گولڈن سوال۔",
        ),
    ),
    day(
        "xii", 17, 4, "Teach", "Application and Impacts of Computing", "Application and Impacts of Computing (2/4)",
        "Secure Collaboration (Authentication, MFA, Access Control)", 158, 160,
        ["Components of Deep Learning", "Future of AI, NN and DL in Pakistan", "Applications of Neural Networks", "Secure Collaboration (Authentication, MFA, Access Control)"],
        T(
            "دن 17۔ {Deep Learning} کے جز: بہت ڈیٹا، {GPU}، تہیں، تربیت۔ پاکستان میں صحت، زراعت، زبان کے مواقع۔ استعمال: تصویر، آواز، سفارش۔",
            "★ {Secure Collaboration}: {Authentication} تم کون — پاس ورڈ۔ {MFA} دوسرا ثبوت، جیسے کوڈ۔ {Access Control} تم کیا کر سکتے ہو — طالب علم دیکھے، ایڈمن بدلے۔ تین اصطلاحیں الگ رکھو۔",
        ),
    ),
    day(
        "xii", 18, 4, "Teach", "Application and Impacts of Computing", "Application and Impacts of Computing (3/4)",
        "Common Security Threats (Malware, Phishing, DoS)", 161, 163,
        ["Data Protection (Encryption, Passwords, Backup, Firewall)", "Common Security Threats (Malware, Phishing, DoS)", "Identifying Security Threats", "Apply Mitigation Techniques"],
        T(
            "دن 18۔ حفاظت: {Encryption} بدل کر بھیجو، مضبوط پاس ورڈ، {Backup}، {Firewall}۔",
            "★ دھمکیاں: {Malware} نقصان دہ پروگرام، {Phishing} جعلی پیغام سے راز چوری، {DoS} سروس دبا کر گرا دینا — نتیجے کے دن یا ای ٹیسٹ پر۔ پہچانو: عجیب لنک، اچانک سستی، انجان منسلکہ۔ روک: اپ ڈیٹ، مشکوک لنک نہ کھولو، نقل، {MFA}۔",
        ),
    ),
    day(
        "xii", 19, 4, "Checkpoint", "Application and Impacts of Computing", "Application and Impacts of Computing (4/4)",
        "Functions of Equity and Equal Access", 164, 167,
        ["Equity and Equal Access in Digital Collaboration", "Functions of Equity and Equal Access", "Collaboration Tools", "Checkpoint Test"],
        T(
            "دن 19 {Checkpoint}۔ ★ {Functions of Equity and Equal Access}: سب کو جگہ، مختلف سیکھنے کے انداز — ویڈیو متن آواز، کمزور انٹرنیٹ والوں کا خیال، احترام۔ چار عنوان ترتیب سے 5 سے 8 نمبر۔ اوزار: مشترکہ دستاویز، میٹ، چیٹ — مگر رسائی برابر۔ چالیس منٹ ٹیسٹ۔",
        ),
    ),
    day(
        "xii", 20, 4, "Teach", "Entrepreneurship in the Digital Age", "Entrepreneurship in the Digital Age (1/4)",
        "Entrepreneurship in the Digital Age, Prototype", 168, 170,
        ["Entrepreneur and Entrepreneurship", "Entrepreneurship in the Digital Age", "Local Examples of Digital Entrepreneurship", "From Problem to Business Idea", "Prototype"],
        T(
            "دن 20، باب {Entrepreneurship in the Digital Age}۔ {Entrepreneur} مسئلہ دیکھ کر کاروبار بناتا ہے۔",
            "★ ڈیجیٹل دور: ایپ، ادائیگی، سوشل، گھر بیٹھے منڈی۔ مقامی مثالیں جدول 6.1 پر جوں کی توں۔ مسئلہ سے خیال: کس کا درد، کیا حل۔",
            "★ {Prototype} خیال کا پہلا چھوتا ماڈل — کاغذی سکرین یا کارڈ بورڈ — سیکھنے کے لیے، کمال کے لیے نہیں۔",
        ),
    ),
    day(
        "xii", 21, 5, "Teach", "Entrepreneurship in the Digital Age", "Entrepreneurship in the Digital Age (2/4)",
        "Prototype Development Cycle, Minimum Viable Product (MVP)", 171, 173,
        ["Types of Prototypes", "Prototype Development Cycle", "Class Activity: Create a Prototype", "Minimum Viable Product (MVP)", "Difference between Prototype and MVP"],
        T(
            "دن 21۔ اقسام: کاغذی، ڈیجیٹل، کام کرتا نمونہ۔ fidelity یعنی کتنا حقیقی لگے۔",
            "★ {Prototype Development Cycle}: بناؤ، دکھاؤ، سنو، بدلواؤ — {iteration}۔",
            "★ {MVP} وہ سب سے چھوٹی اصل چیز جو مشتری استعمال کر کے سکھائے۔ {Prototype} سیکھنے کا ماڈل ہو سکتا ہے جعلی؛ {MVP} حقیقی مگر تنگ۔ فرق امتحان میں جدول۔",
        ),
    ),
    day(
        "xii", 22, 5, "Teach", "Entrepreneurship in the Digital Age", "Entrepreneurship in the Digital Age (3/4)",
        "none — still copy every table", 174, 175,
        ["Identifying the Riskiest Assumption", "Developing an MVP", "Case Study: MVP for a Canteen Pre-Order System", "Testing an MVP"],
        T(
            "دن 22۔ سب سے خطرناک مفروضہ وہ دعویٰ ہے جس کے جھوٹے ہونے پر پورا خیال گرتا ہے۔ پہلے اسی کو جانچو۔",
            "کیس: کینٹین پری آرڈر۔ یاد: 5 items، 3 days، 20 minutes — پانچ آئٹم، تین دن ٹیسٹ، آرڈر بند۔ کاغذی {Prototype}، پھر {Google Form} {MVP}، رائے، بہتری۔ {MVP} جانچ: کیا آرڈر آیا، کیا وقت بچا، کیا الجھن ہوئی۔",
        ),
    ),
    day(
        "xii", 23, 5, "Checkpoint", "Entrepreneurship in the Digital Age", "Entrepreneurship in the Digital Age (4/4)",
        "Beachhead Market", 176, 179,
        ["Beachhead Market", "Complete Student Project", "Ethical and Safe Use of Digital Tools", "Career", "Checkpoint Test"],
        T(
            "دن 23 {Checkpoint}۔ ★ {Beachhead Market} پہلی چھوٹی مخصوص منڈی جہاں پہلے جیتو، سمندر نہیں، ساحل کا ٹکڑا۔ مثال: پورا شہر نہیں، ایک اسکول کی کینٹین۔",
            "پروجیکٹ مکمل کرو۔ اخلاق: اجازت، ڈیٹا کی حفاظت، جھوٹی تعریف نہیں۔ کیریئر جدول: صارف سمجھو، مفروضہ جانچو، چھوٹا شروع۔ چالیس منٹ ٹیسٹ۔",
        ),
    ),
    day(
        "xii", 24, 5, "Golden blitz", "Chapters 1–2", "★ only · Chapters 1–2",
        "11 Golden cards", 180, 185,
        ["Applications of HCI", "Importance of HCI", "HCI Problems", "UI vs UX", "Testing Methods", "Trace Tables", "Big O Notation", "Data Structure", "Stack", "Queue"],
        T(
            "دن 24 {Golden blitz} باب 1 اور 2۔ چار میدان {HCI}، اہمیت، مسائل، {UI} کپڑے {UX} پورا دن، تین ٹیسٹ تصویریں۔ {Trace Table} بھرو، {Big O} بتاؤ، {Stack LIFO} {Queue FIFO} کھینچو۔ نیا غیر گولڈن نہیں۔",
        ),
    ),
    day(
        "xii", 25, 6, "Golden blitz", "Chapters 3–4", "★ only · Chapters 3–4",
        "11 Golden cards", 186, 190,
        ["Lists", "Tuples", "Dictionaries", "Functions", "File modes r w a", "with statement", "Data sources", "Pandas DataFrames", "NaN", "Graphs", "Descriptive Statistics"],
        T(
            "دن 25 {Golden blitz} باب 3 اور 4۔ تین ڈھانچے کا فرق، {def}، فائل موڈ، {with}۔ {Pandas} {DataFrame}، {NaN} علاج، چارٹ انتخاب، اوسط میڈین موڈ۔ ہر جدول یاد سے۔",
        ),
    ),
    day(
        "xii", 26, 6, "Golden blitz", "Chapters 5–6", "★ only · Chapters 5–6",
        "10 Golden cards", 191, 196,
        ["Neural Networks", "NN Components", "Secure Collaboration", "Malware Phishing DoS", "Equity and Equal Access", "Digital Entrepreneurship", "Prototype", "Prototype Cycle", "MVP", "Beachhead Market"],
        T(
            "دن 26 {Golden blitz} باب 5 اور 6۔ نیٹ ورک کے آٹھ جز، {Authentication MFA Access Control}، تین دھمکیاں، برابری کے چار عنوان۔ {Prototype} چکر، {MVP} فرق، {Beachhead Market} ساحل۔",
        ),
    ),
    day(
        "xii", 27, 6, "Recap", "All chapters", "Say every chapter recap aloud, book closed",
        "All chapters", 197, 198,
        ["HCI recap", "Algorithms and Data Structures", "Python structures functions files", "Data and Analysis", "AI Security Collaboration", "Entrepreneurship"],
        T(
            "دن 27 کتاب بند recap۔ باب 1 {HCI} جانچ اور رسائی۔ باب 2 ٹرِیس، {Big O}، {Stack} {Queue}۔ باب 3 فہرست ٹوپل ڈکشنری فنکشن فائل۔ باب 4 {Pandas} چارٹ شماریات۔ باب 5 {AI} سیکیورٹی برابری۔ باب 6 خیال، نمونہ، {MVP}، ساحلی منڈی۔",
        ),
    ),
    day(
        "xii", 28, 6, "Mock", "Whole syllabus", "2 hours 30 minutes · 75 marks · no notes",
        "Whole syllabus", 199, 201,
        ["Mock paper hall conditions"],
        T(
            "دن 28 {Mock}۔ ڈھائی گھنٹے، 75 نمبر، نوٹس نہیں۔ خود انویجیلیٹ۔ گولڈن سوال جدول اور مثال سے۔ دن 29 کی کلید نہیں دیکھنی۔",
        ),
    ),
    day(
        "xii", 29, 6, "Mark", "Missed Goldens", "Mark to the key. List every ★ Golden you missed.",
        "Missed Goldens", 202, 203,
        ["Mark the mock", "Repair list"],
        T(
            "دن 29 marking۔ کلید سے میل کھاؤ۔ ہر ★ {Golden} جس پر صفر یا آدھا آیا {Repair list} میں لکھو۔ {Wireframe} یا {Accessibility} رہ گیا ہو تو جدول دوبارہ۔ کل صرف یہی فہرست۔",
        ),
    ),
    day(
        "xii", 30, 6, "Repair", "Missed Goldens only", "Redo the Day 29 list only. Sleep by 10 pm.",
        "Missed Goldens only", 204, 204,
        ["Redo Day 29 list", "Sleep by 10 pm"],
        T(
            "دن 30 {Repair}۔ صرف دن 29 کی {Repair list}: تعریف کہو، جدول کھینچو۔ شام چھ بجے رک، دس بجے سو۔ نیا {Chapter} نہیں۔ ★ {Golden} کارڈز سر میں، ہال میں کتاب نہیں۔ اللہ حافظ۔",
        ),
    ),
]


def main() -> None:
    assert len(XI) == 30, len(XI)
    assert len(XII) == 30, len(XII)
    catalog = {
        "title": "CS XI & XII 30-Day Crash Course",
        "curriculum": "New Sindh Curriculum 2026",
        "narration": "ur-en-mixed",
        "termRule": "English exam terms are wrapped in {braces} and spoken as printed on the booklet pages.",
        "courses": [
            {
                "id": "xi",
                "title": "Computer Science XI",
                "subtitle": "30-Day Crash Course · Days 1–23 teach · 24–30 revise, mock, repair",
                "introStartPage": 1,
                "introEndPage": 4,
                "introScript": XI_INTRO,
                "introDisplay": XI_INTRO_EN,
                "days": XI,
            },
            {
                "id": "xii",
                "title": "Computer Science XII",
                "subtitle": "30-Day Crash Course · HCI, algorithms, Python, AI, entrepreneurship",
                "introStartPage": 104,
                "introEndPage": 107,
                "introScript": XII_INTRO,
                "introDisplay": XII_INTRO_EN,
                "days": XII,
            },
        ],
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(catalog, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Wrote {OUT} ({OUT.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
