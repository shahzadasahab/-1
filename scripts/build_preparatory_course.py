#!/usr/bin/env python3
"""Build the embedded Teach-Yourself crash course from the four booklets.

Writes:
  app/src/main/assets/course/pages.json   — English text of every printed page
  app/src/main/assets/course/course.json  — XI and XII 30-day plans with Urdu scripts
  app/src/main/assets/course/tts.json     — Urdu description + {English terms} for TTS

The combined booklet PDF (crash-course.pdf) is produced separately and already
contains every symbol, gate, table and diagram.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

import pymupdf

ROOT = Path(__file__).resolve().parents[1]
PDF = ROOT / "app/src/main/assets/course/crash-course.pdf"
PAGES = ROOT / "app/src/main/assets/course/pages.json"
COURSE = ROOT / "app/src/main/assets/course/course.json"

ARABIC = re.compile(r"[\u0600-\u06FF\uFB50-\uFDFF\uFE70-\uFEFF]")
LATIN = re.compile(r"[A-Za-z]")
PRIVATE = re.compile(r"[\ue000-\uf8ff\u200b-\u200f\u202a-\u202e\ufffd]")
SKIP = re.compile(
    r"^(Teach-Yourself Booklet|Teacher's Edition|Complete Edition|Sindh Textbook Board|"
    r"Page \d+ of \d+|\d+\s*/\s*\d+|GRADE XII|TEST EDITION)",
    re.I,
)
FIGURE = re.compile(
    r"\b(Figure|Fig\.|Table \d|Truth table|K-map|Karnaugh|logic diagram|Logic gate|"
    r"symbol|flowchart|Flow chart|stack|queue)\b",
    re.I,
)
HEADING = re.compile(
    r"^(\d+\.\d+[a-z]?|[1-6]\.[A-Z]|Unit \d|Lesson |Mock test|Glossary|Formula sheet|"
    r"Bilingual |How to use|Contents|Check yourself|Try it|Answer key)",
    re.I,
)
BOXES = {
    "check yourself": "checkpoint",
    "try it": "drill",
    "mock test": "checkpoint",
    "answer key": "answers",
    "teacher's note": "remember",
    "common misconception": "trap",
}


def clean(line: str) -> str:
    line = ARABIC.sub(" ", line)
    line = PRIVATE.sub("", line)
    line = line.replace("{", "(").replace("}", ")")
    line = re.sub(r"\s+", " ", line).strip(" ·|-–—")
    return line.strip()


def classify(text: str) -> list[dict]:
    blocks: list[dict] = []
    for raw in text.splitlines():
        line = clean(raw)
        if not line or SKIP.match(line):
            continue
        letters = LATIN.findall(line)
        if len(letters) < 2 and not re.search(r"[=+\-×÷<>≤≥∑]|\d", line):
            continue
        if len(line) < 3:
            continue
        low = line.lower()
        boxed = next((kind for key, kind in BOXES.items() if low.startswith(key)), None)
        if boxed == "checkpoint":
            blocks.append({"t": "box", "x": "Checkpoint test"})
            continue
        if boxed == "drill":
            blocks.append({"t": "box", "x": "Closed-book drill"})
            continue
        if boxed == "answers":
            blocks.append({"t": "answers", "x": line})
            continue
        if boxed == "remember":
            blocks.append({"t": "remember", "x": line})
            continue
        if boxed == "trap":
            blocks.append({"t": "trap", "x": line})
            continue
        if FIGURE.search(line) and len(line) < 220:
            blocks.append({"t": "fig", "x": line})
            continue
        if HEADING.match(line) and len(line) < 110:
            blocks.append({"t": "h", "x": line, "g": "golden" in low})
            continue
        if blocks and blocks[-1]["t"] == "p":
            prev = blocks[-1]["x"]
            if prev and prev[-1] not in ".?!:" and line[:1].islower() and len(prev) < 280:
                blocks[-1]["x"] = f"{prev} {line}"
                continue
        if len(letters) >= 3:
            blocks.append({"t": "p", "x": line[:420]})
    # Keep the page speakable: headings, figures, then the clearest paragraphs.
    priority = {"h": 0, "fig": 1, "remember": 2, "trap": 2, "box": 2, "answers": 3, "p": 4}
    ranked = sorted(enumerate(blocks), key=lambda ib: (priority.get(ib[1]["t"], 5), ib[0]))
    keep_idx = sorted(i for i, _ in ranked[:16])
    return [blocks[i] for i in keep_idx]


def extract_pages() -> None:
    doc = pymupdf.open(PDF)
    pages = {}
    for i, page in enumerate(doc, start=1):
        pages[str(i)] = classify(page.get_text("text") or "")
    PAGES.write_text(json.dumps(pages, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    total = sum(len(v) for v in pages.values())
    print(f"pages.json {len(pages)} pages, {total} blocks, {PAGES.stat().st_size} bytes")


def T(*parts: str) -> str:
    return " ".join(p.strip() for p in parts if p and p.strip())


def day(
    course: str,
    n: int,
    week: int,
    kind: str,
    chapter: str,
    focus: str,
    golden: str,
    book: str,
    start: int,
    end: int,
    topics: list[str],
    urdu: str,
) -> dict:
    return {
        "course": course,
        "day": n,
        "week": week,
        "kind": kind,
        "chapter": chapter,
        "focus": focus,
        "golden": golden,
        "book": book,
        "localStart": start,
        "localEnd": end,
        "topics": topics,
        "script": urdu,
    }


XI = [
    day("xi", 1, 1, "Teach", "Computer Systems", "Analog, digital and binary",
        "Analog and Digital Signals", "xi14", 6, 8,
        ["Discrete and continuous quantities", "Analog signals", "Digital signals", "Bit"],
        T(
            "آج {Class XI} کے {Unit 1} کا پہلا سبق ہے۔ ★ {Golden} موضوع {Analog and Digital Signals} ہے۔",
            "{Discrete} مقدار گنی جاتی ہے، جیسے کلاس کے طلبہ۔ {Continuous} مقدار ناپی جاتی ہے، جیسے پانی کا درجہ حرارت۔ سیڑھیاں {Discrete} ہیں، ramp {Continuous} ہے۔",
            "{Digital system} صرف دو قیمتیں استعمال کرتا ہے: 0 یعنی {OFF}، {LOW}، {FALSE}، اور 1 یعنی {ON}، {HIGH}، {TRUE}۔ ایک {Bit} بتی کے سوئچ کی طرح ہے۔",
            "★ {Analog signals} ہموار {Sine Wave} ہیں، جیسے آواز۔ {Digital signals} صرف دو سطحیں رکھتی ہیں، {Square Wave}۔ {Analog} شور سے متاثر ہوتا ہے، {Digital} شور کے خلاف مضبوط ہے۔",
            "صفحے پر دونوں لہریں چھپی ہیں۔ انہیں نقل کریں۔ امتحان میں جدول اور دونوں لہریں کھینچنی آئیں گی۔ اصطلاحات کا ترجمہ نہ کریں۔",
        )),
    day("xi", 2, 1, "Teach", "Computer Systems", "Boolean algebra and logic gates",
        "Logic Gates (AND, OR, NOT)", "xi14", 9, 10,
        ["Boolean algebra", "AND gate", "OR gate", "NOT gate", "Truth table"],
        T(
            "دن 02۔ ★ {Golden}: {Logic Gates}، بنیادی گیٹس {AND}، {OR}، {NOT}۔",
            "{Boolean Algebra} {George Boole} نے بنائی۔ صرف {TRUE} 1 اور {FALSE} 0۔ جال: Boolean میں جمع کا نشان {OR} ہے، حساب کا جمع نہیں۔",
            "{AND} تب 1 جب تمام inputs 1 ہوں — دو تالے والا دروازہ۔ {OR} تب 1 جب کوئی ایک 1 ہو۔ {NOT} الٹ دیتا ہے، اس لیے اسے inverter کہتے ہیں۔",
            "صفحے پر گیٹ کی شکلیں چھپی ہیں: {AND} کی شکل D، {OR} نوک دار، {NOT} مثلث پر bubble۔ شکل نقل کریں، نام انگریزی میں لکھیں۔",
            "{Truth Table} ہر ممکن input اور output دکھاتی ہے۔ دو inputs کی چار قطاریں: 00، 01، 10، 11۔",
        )),
    day("xi", 3, 1, "Teach", "Computer Systems", "Expressions, truth tables and diagrams",
        "Truth Tables and Logic Diagrams", "xi14", 11, 12,
        ["Logic expressions", "Minterms", "Maxterms", "Logic diagrams"],
        T(
            "دن 03۔ ★ {Golden}: {Truth Tables} اور {Logic Diagrams}۔",
            "{XOR} تب 1 جب inputs مختلف ہوں۔ {XNOR} تب 1 جب دونوں یکساں ہوں۔",
            "{Minterm} وہ حاصل ضرب ہے جو ایک قطار میں 1 دیتی ہے۔ {Maxterm} وہ حاصل جمع ہے جو 0 دیتی ہے۔",
            "Expression کو گیٹ کی تصویر بنانا {Logic Diagram} ہے۔ ترتیب: پہلے {NOT}، پھر {AND}، آخر میں {OR} — یا جو ترتیب صفحے پر دی گئی ہو۔",
            "چھپے ہوئے diagram کو کاپی میں بنائیں۔ بند کتاب ایک چھوٹی expression کا diagram خود کھینچیں۔",
        )),
    day("xi", 4, 1, "Teach", "Computer Systems", "Karnaugh maps and LogiSim",
        "Karnaugh Maps and LogiSim", "xi14", 13, 14,
        ["Karnaugh map", "Gray code", "Universal gates NAND and NOR", "LogiSim"],
        T(
            "دن 04۔ ★ {Golden}: {Karnaugh Maps} یعنی {K-Maps}، اور {LogiSim}۔",
            "{NAND} یعنی {NOT AND}، {NOR} یعنی {NOT OR}۔ دونوں {Universal gates} ہیں — پورا منطق سرکٹ صرف {NAND} یا صرف {NOR} سے بن سکتا ہے۔",
            "★ {K-Map} {Truth Table} کو خانوں میں سمیٹتی ہے تاکہ سادہ گروپ ملیں۔ پڑوسی خانے صرف ایک {Bit} بدلتے ہیں، یہ {Gray code} ہے۔ گروپ 1، 2، 4، 8 کے ہوں۔",
            "صفحے کا {K-Map} جوں کا توں نقل کریں، پھر بند کتاب 2 variable اور 3 variable map بنائیں۔",
            "{LogiSim Evolution} میں گیٹ رکھیں، تار جوڑیں، input دے کر output دیکھیں۔ فائل کی توسیع {.circ} ہے۔",
        )),
    day("xi", 5, 1, "Checkpoint", "Computer Systems", "SDLC, Waterfall, Agile, OSI and TCP/IP",
        "SDLC, the Waterfall Model, Agile, and the OSI 7-Layer Model", "xi14", 15, 27,
        ["SDLC", "Waterfall model", "Agile model", "OSI 7-layer model", "TCP/IP"],
        T(
            "دن 05 {Checkpoint}۔ ★ {Golden}: {SDLC}، {Waterfall}، {Agile}، اور {OSI 7-Layer Model}۔",
            "{Software Development Life Cycle} کے عام مراحل: {Requirement}، {Design}، {Implementation}، {Testing}، {Deployment}، {Maintenance}۔",
            "★ {Waterfall Model} ایک طرف بہتا ہے، واپس آنا مہنگا ہے۔ {Agile} چھوٹے {Sprint} میں بناتا ہے، عموماً 2 سے 4 ہفتے۔ گاہک ہر {Sprint} کے بعد کام دیکھتا ہے۔",
            "★ {OSI} کی سات تہیں: {Physical}، {Data Link}، {Network}، {Transport}، {Session}، {Presentation}، {Application}۔ یاد: Please Do Not Throw Sausage Pizza Away۔",
            "{TCP/IP} چار تہیں: {Network Access}، {Internet}، {Transport}، {Application}۔ {OSI} نمونہ ہے، {TCP/IP} عملی انٹرنیٹ۔",
            "تہوں کا خاکہ صفحے پر ہے۔ نقل کریں۔ پھر بند کتاب چالیس منٹ کا باب ٹیسٹ۔ 60 فیصد سے کم ہو تو کل {Golden repair}، نیا باب نہیں۔",
        )),
    day("xi", 6, 2, "Teach", "Computational Thinking and Algorithms", "Algorithms, pseudocode and decomposition",
        "Algorithm, Pseudocode and Decomposition", "xi14", 28, 31,
        ["Computational thinking", "Algorithm", "Pseudocode", "Decomposition", "Pattern recognition", "Abstraction"],
        T(
            "دن 06، {Unit 2}۔ ★ {Golden}: {Algorithm}، {Pseudocode}، {Decomposition}۔",
            "{Computational Thinking} چار ستون: {Decomposition}، {Pattern Recognition}، {Abstraction}، {Algorithm}۔",
            "★ {Algorithm} قدم بہ قدم ہدایات ہیں: شروع، واضح قدم، اختتام۔ کھانا پکانے کی ترکیب الگورتھم کی مثال ہے۔",
            "★ {Pseudocode} انگریزی نما ڈھانچہ ہے، مخصوص زبان نہیں۔ {Algorithm} سوچ ہے، {Pseudocode} اس کی لکھائی، حقیقی کوڈ {Python}۔",
            "★ {Decomposition} بڑے مسئلے کو چھوٹے حصوں میں توڑنا۔ {Abstraction} غیر ضروری تفصیل چھپاتا ہے۔ صفحے کے خاکے نقل کریں۔",
        )),
    day("xi", 7, 2, "Teach", "Computational Thinking and Algorithms", "Bubble sort, selection sort, linear and binary search",
        "Bubble Sort, Selection Sort and Binary Search", "xi14", 32, 35,
        ["Bubble sort", "Selection sort", "Linear search", "Binary search"],
        T(
            "دن 07۔ ★ {Golden}: {Bubble Sort}، {Selection Sort}، {Binary Search}۔",
            "{Bubble Sort}: پڑوسی جوڑوں کا موازنہ، بڑا آگے دھکیل دو، آخر تک {Pass}۔ سادہ، سست، تقریباً n مربع موازنے۔",
            "{Selection Sort}: ہر {Pass} میں باقی فہرست کا سب سے چھوٹا چن کر جگہ پر لگاؤ۔ swaps کم ہوتے ہیں۔",
            "{Linear Search} شروع سے آخر تک ایک ایک دیکھتا ہے۔ ترتیب ضروری نہیں۔ بدترین صورت n قدم۔",
            "★ {Binary Search} صرف ترتیب شدہ فہرست پر۔ درمیان دیکھو۔ برابر ہو تو مل گیا؛ مطلوبہ بڑا ہو تو دایاں نصف، چھوٹا ہو تو بایاں نصف۔ پیچیدگی {O(log n)}۔",
            "صفحے کی جدول اور شکل جوں کی توں نقل کریں، پھر ایک چھوٹی فہرست پر دونوں sort خود چلائیں۔",
        )),
    day("xi", 8, 2, "Checkpoint", "Computational Thinking and Algorithms", "Evaluate and choose an algorithm",
        "Evaluating an Algorithm", "xi14", 36, 40,
        ["Correctness", "Clarity", "Efficiency", "Memory", "Checkpoint test"],
        T(
            "دن 08 {Checkpoint}۔ ★ {Golden}: الگورتھم کی جانچ — درستگی، وضاحت، رفتار، یادداشت۔",
            "درست الگورتھم ہر جائز input پر درست output دیتا ہے۔ واضح الگورتھم دوسرا شخص پڑھ کر چلا سکتا ہے۔",
            "کارکردگی: {Bubble Sort} اور {Selection Sort} تقریباً {O(n²)} ہیں۔ {Binary Search} {O(log n)} ہے، مگر فہرست ترتیب شدہ ہونی چاہیے۔",
            "صفحات پر mock اور کلید ہے۔ پہلے بند کتاب ٹیسٹ حل کریں، پھر سبز جواب پڑھیں۔ {Binary Search} کی تعریف، شرط، اور ایک مثال لازمی لکھیں۔",
        )),
    day("xi", 9, 2, "Teach", "Programming Fundamentals", "Programming, Python and the IDE",
        "Python and the IDE (VS Code)", "xi14", 41, 43,
        ["Programming", "High-level and low-level languages", "Python", "IDE", "VS Code"],
        T(
            "دن 09، {Unit 3}۔ ★ {Golden}: {Python} اور {IDE}، مثال {Visual Studio Code}۔",
            "{Programming} کمپیوٹر کو ہدایات دینا ہے۔ {Low-level} مشین کے قریب، {High-level} انسان کے قریب۔ {Python} high-level ہے۔",
            "{Compiled} زبانیں پہلے مشین کوڈ بناتی ہیں۔ {Interpreted} لائن بہ لائن چلتی ہیں۔ {Python} interpreted ہے۔",
            "{IDE} وہ جگہ ہے جہاں کوڈ لکھا، چلایا اور سنبھالا جاتا ہے۔ یادداشتی لفظ {ESARD}: {Editor}، {Syntax highlighting}، {Auto-completion}، {Run}، {Debugger}۔",
            "صفحے کی جدول نقل کریں۔ کل {Variables} اور {Data Types} آئیں گے۔",
        )),
    day("xi", 10, 2, "Teach", "Programming Fundamentals", "Variables, data types, operators",
        "Variables, Data Types and Operators", "xi14", 44, 46,
        ["Variables", "int, float, str, bool", "input and print", "Arithmetic operators", "Assignment"],
        T(
            "دن 10۔ ★ {Golden}: {Variables}، {Data Types}، {Operators}۔",
            "{Variable} نام والا ڈبہ ہے۔ {int} عدد، {float} اعشاری، {str} متن، {bool} {True} یا {False}۔ {type()} قسم بتاتا ہے۔",
            "{print} دکھاتا ہے، {input} پوچھتا ہے۔ {Python} انڈینٹیشن سے بلاک بناتا ہے، اور نام case-sensitive ہیں۔",
            "عمل: جمع، تفریق، ضرب، تقسیم، {//} مکمل تقسیم، {%} باقی، {**} طاقت۔ {Assignment} = قیمت رکھتا ہے۔ {Operand} وہ قیمت ہے جس پر عمل ہو، {Operator} خود عمل۔",
            "صفحے کا نمونہ کوڈ خود ٹائپ کریں، پھر بند کتاب تین متغیر بنائیں۔",
        )),
    day("xi", 11, 3, "Teach", "Programming Fundamentals", "Sequence and selection",
        "Selection: if and if-else", "xi14", 47, 48,
        ["Sequence", "if", "if-else", "Relational operators", "Logical operators"],
        T(
            "دن 11۔ ★ {Golden}: {Selection}، {if} اور {if-else}۔",
            "{Control structure} تین: {Sequence} سیدھا چلے، {Selection} انتخاب کرے، {Repetition} دہرائے۔",
            "تقابلی عمل == != < > <= >= نتیجہ {bool} دیتے ہیں۔ منطقی: {and} دونوں سچ، {or} کوئی ایک، {not} الٹ۔ {in} رکنیت ہے۔",
            "{if} شرط سچ ہو تو بلاک چلتا ہے۔ {if-else} دو راستے دیتا ہے۔ امتحان میں flowchart اور چھوٹا کوڈ دونوں مانگتے ہیں۔ صفحے کا خاکہ نقل کریں۔",
        )),
    day("xi", 12, 3, "Teach", "Programming Fundamentals", "for and while loops",
        "for loop, while loop, break and continue", "xi14", 49, 50,
        ["if-elif-else", "for loop", "range()", "while loop", "break", "continue", "Nested loops"],
        T(
            "دن 12۔ ★ {Golden}: {for}، {range()}، {while}، {break}، {continue}۔",
            "کئی شرطیں ہوں تو {elif} زنجیر۔ اندر {if} کو {Nested if} کہتے ہیں۔",
            "{for} معلوم تکرار کے لیے: {for i in range(5)}۔ {range(start, stop, step)} میں stop شامل نہیں۔",
            "{while} جب تک شرط سچ رہے چلتا ہے۔ شرط نہ بدلی تو {Infinite loop}۔ {break} لوپ توڑتا ہے، {continue} یہ چکر چھوڑ کر اگلا شروع کرتا ہے۔",
            "گنتی معلوم ہو تو {for}، شرط پر رکنا ہو تو {while}۔ صفحے کا کوڈ خود چلائیں اور trace لکھیں۔",
        )),
    day("xi", 13, 3, "Checkpoint", "Programming Fundamentals", "Libraries, debugging and the unit mock",
        "Libraries and Debugging", "xi14", 51, 57,
        ["Libraries", "Debugging", "Syntax error", "Logic error", "Checkpoint test"],
        T(
            "دن 13 {Checkpoint}۔ ★ {Golden}: {Libraries} اور {Debugging}۔",
            "{Library} تیار کوڈ کا مجموعہ ہے، جیسے ریاضی کے فنکشن۔ خود وہی کوڈ دوبارہ نہ لکھیں۔",
            "غلطیاں: {Syntax error} زبان کا قاعدہ ٹوٹنا، پروگرام چلتا ہی نہیں۔ {Logic error} پروگرام چلتا ہے مگر جواب غلط۔ {Debugger} لائن بہ لائن روک کر متغیر دکھاتا ہے۔",
            "بند کتاب باب کا mock حل کریں۔ پھر کلید سے میل کھائیں۔ کمزور ★ {Golden} {Repair list} میں لکھیں۔",
        )),
    day("xi", 14, 3, "Teach", "Database Management", "Data, DBMS, tables and keys",
        "DBMS, tables and keys", "xi14", 58, 60,
        ["Data and information", "DBMS", "Table, record, field", "Primary key", "Foreign key"],
        T(
            "دن 14، {Unit 4}۔ ★ {Golden}: {DBMS}، tables اور keys۔",
            "{Data} کچا حقائق ہے۔ {Information} وہی data جب معنی دے دے۔ {Database} متعلقہ data کا منظم مجموعہ ہے۔",
            "{DBMS} وہ سافٹ ویئر ہے جو database بناتا، محفوظ رکھتا اور سوالوں کے جواب دیتا ہے۔ مثال {MS Access}۔",
            "{Table} میں قطاریں {records} ہیں اور کالم {fields}۔ ★ {Primary key} ہر record کو منفرد بناتی ہے۔ {Foreign key} دوسری table کی primary key ہے۔",
            "صفحے کا جدول نقل کریں۔ ایک اسکول کی table خود بنائیں: StudentID بطور {Primary key}۔",
        )),
    day("xi", 15, 3, "Teach", "Database Management", "ER model, integrity and the library schema",
        "ER Model and Referential Integrity", "xi14", 61, 64,
        ["Entity", "Attribute", "Relationship", "Referential integrity", "Relational schema"],
        T(
            "دن 15۔ ★ {Golden}: {ER model} اور {Referential integrity}۔",
            "{Entity} وہ چیز ہے جس کا data رکھتے ہیں، جیسے Student یا Book۔ {Attribute} اس کی خصوصیت ہے۔ {Relationship} entities کو جوڑتا ہے: one-to-many، many-to-many۔",
            "★ {Referential integrity} کا مطلب: {Foreign key} کی قیمت یا تو خالی ہو یا دوسری table کی موجود {Primary key} ہو۔ یتیم record جائز نہیں۔",
            "لائبریری کیس اسٹڈی کا {Relational schema} صفحے پر ہے۔ مستطیل entity، بیضوی attribute، ہیرے relationship — خاکہ نقل کریں۔",
        )),
    day("xi", 16, 4, "Teach", "Database Management", "Tables and forms in MS Access",
        "MS Access tables and forms", "xi14", 65, 67,
        ["MS Access objects", "Datasheet view", "Design view", "Forms"],
        T(
            "دن 16۔ ★ {Golden}: {MS Access} کے objects، tables اور {Forms}۔",
            "{Table} data رکھتی ہے۔ {Form} data داخل کرنے کی سکرین ہے۔ {Query} سوال ہے۔ {Report} چھپنے والا خالصہ ہے۔",
            "{Design view} میں فیلڈ کا نام، {Data type} اور {Primary key} مقرر ہوتی ہے۔ {Datasheet view} میں قطاریں بھری جاتی ہیں۔",
            "{Form} صارف کو table کی پیچیدگی سے بچاتا ہے۔ صفحے کی سکرین جیسی شکل کاپی میں بنائیں: عنوان، فیلڈز، محفوظ کرنے کا بٹن۔",
        )),
    day("xi", 17, 4, "Checkpoint", "Database Management", "Queries, charts and the unit mock",
        "Queries, summaries and charts", "xi14", 68, 80,
        ["Select query", "Criteria", "Summary", "Chart", "Checkpoint test"],
        T(
            "دن 17 {Checkpoint}۔ ★ {Golden}: {Queries}، summaries اور charts۔",
            "{Select query} table سے قطاریں چنتی ہے۔ {Criteria} شرط ہے، جیسے Marks >= 50۔ {Sort} ترتیب دیتا ہے۔",
            "Summary: {Sum}، {Average}، {Count}۔ Chart اعداد کو تصویر بناتا ہے — {bar chart} موازنہ، {pie chart} حصہ۔",
            "بند کتاب mock حل کریں۔ {Primary key}، {Foreign key}، {Referential integrity} کی تعریف زبانی آئے۔ فرہنگ کے صفحات بھی اسی نشست میں ہیں۔",
        )),
    day("xi", 18, 4, "Teach", "Applications and Impacts of Computing", "Artificial intelligence and the Internet of Things",
        "Artificial Intelligence and IoT", "xi56", 1, 11,
        ["Artificial Intelligence", "Internet of Things", "Six components of IoT", "Sensor", "Actuator"],
        T(
            "دن 18، {Unit 5}۔ ★ {Golden}: {Artificial Intelligence} اور {IoT}۔",
            "{AI} وہ کمپیوٹر نظام ہے جو ایسے کام کرے جن میں انسان کو ذہانت لگتی ہے: پہچان، فیصلہ، سیکھنا۔",
            "★ {Internet of Things} چیزوں کا جال ہے جو internet سے جڑ کر data بھیجتی ہیں۔ چھ اجزا صفحے کے خاکے پر ہیں: {Sensor}، کنیکٹیویٹی، data کی پروسیسنگ، {Actuator}، interface، اور سیکیورٹی۔ خاکہ نقل کریں۔",
            "اسمارٹ گھر کی مثال: sensor درجہ حرارت ناپے، actuator پنکھا چلائے۔ اصطلاح {IoT} انگریزی میں ہی لکھیں۔",
        )),
    day("xi", 19, 4, "Teach", "Applications and Impacts of Computing", "Data analytics and uses of IoT",
        "Data Analytics", "xi56", 12, 17,
        ["Data analytics", "Descriptive analytics", "Predictive analytics", "Smart farming", "Smart home"],
        T(
            "دن 19۔ ★ {Golden}: {Data Analytics}۔",
            "{Data analytics} data سے معنی نکالنا ہے۔ {Descriptive} بتاتا ہے کیا ہوا۔ {Predictive} بتاتا ہے کیا ہو سکتا ہے۔",
            "{IoT} کے استعمال: {Smart home}، {Smart farming}، صحت، نقل و حمل۔ سمارٹ کاشتکاری میں sensor نمی ناپتا ہے اور پانی اسی وقت کھلتا ہے۔",
            "صفحے کے خاکے اور ریاضی کا کونا نقل کریں۔ ایک جملے میں بتائیں analytics فیصلہ کیسے بدلتا ہے۔",
        )),
    day("xi", 20, 4, "Checkpoint", "Applications and Impacts of Computing", "Impacts, sources and assistive technologies",
        "Impacts of computing and assistive technologies", "xi56", 18, 34,
        ["AI in education", "Information sources", "Impacts of computing", "Assistive technologies", "Checkpoint test"],
        T(
            "دن 20 {Checkpoint}۔ ★ {Golden}: computing کے اثرات اور {Assistive technologies}۔",
            "{AI} تعلیم میں مشق، فوری رائے، اور ہر طالب علم کی رفتار دے سکتا ہے۔ خطرہ: غلط جواب پر اندھا اعتماد، اور نجی data۔",
            "معلومات کے ماخذ: {Primary} خود اکٹھا کیا، {Secondary} پہلے سے موجود۔ قابل اعتبار ماخذ مصنف، تاریخ اور ثبوت دکھاتا ہے۔",
            "{Assistive technology} معذوری والے شخص کو کمپیوٹر استعمال کرنے دیتی ہے: screen reader، voice input، بڑے بٹن۔ یہ {equity} ہے۔",
            "mock بند کتاب حل کریں۔ اثرات کے مثبت اور منفی دونوں پہلو لکھیں، اور خاکہ اگر صفحے پر ہو تو نقل کریں۔",
        )),
    day("xi", 21, 5, "Teach", "Digital Literacy", "Digital literacy, types of data and collection",
        "Digital literacy and types of data", "xi56", 35, 42,
        ["Digital literacy", "Information Age", "Qualitative data", "Quantitative data", "Primary and secondary data"],
        T(
            "دن 21، {Unit 6}۔ ★ {Golden}: {Digital literacy} اور data کی اقسام۔",
            "{Digital literacy} صرف بٹن دبانا نہیں۔ یہ جاننا ہے کہ digital اوزار سے سوال پوچھیں، data اکٹھا کریں، جانچیں، اور ایمانداری سے پیش کریں۔",
            "{Qualitative} data الفاظ اور صفات ہیں، جیسے رائے۔ {Quantitative} data عدد ہیں، جیسے نمبر۔ {Primary} خود اکٹھا ہوتا ہے، {Secondary} کتاب یا ویب سے آتا ہے۔",
            "اکٹھا کرنے کے طریقے: سروے، مشاہدہ، انٹرویو، sensor، موجودہ ریکارڈ۔ صفحے کی جدول نقل کریں۔",
        )),
    day("xi", 22, 5, "Teach", "Digital Literacy", "Designing a collection and presenting data",
        "Data-collection approach and presenting data", "xi56", 43, 51,
        ["Data-collection plan", "Digital tools", "Chart", "Digital Inquiry Project"],
        T(
            "دن 22۔ ★ {Golden}: data اکٹھا کرنے کا منصوبہ اور {Digital Inquiry Project}۔",
            "منصوبے میں چار باتیں لکھیں: سوال کیا ہے، کون سا data چاہیے، کہاں سے آئے گا، اور کیسے پیش ہوگا۔",
            "پیشکش: table درست عدد دیتی ہے، {bar chart} موازنہ، {line chart} وقت کے ساتھ تبدیلی، {pie chart} حصہ۔ غلط chart معنی بدل دیتا ہے۔",
            "کیس اسٹڈی کا خاکہ صفحے پر ہے۔ اپنے اسکول کا ایک چھوٹا inquiry سوال لکھیں اور artefact کا خاکہ بنائیں۔",
        )),
    day("xi", 23, 5, "Checkpoint", "Digital Literacy", "Inquiry project, revision and mock",
        "Presenting data and the inquiry project", "xi56", 52, 64,
        ["Inquiry artefact", "Revision", "Mock test", "Glossary"],
        T(
            "دن 23 {Checkpoint}۔ ★ {Golden}: data کی پیشکش اور inquiry project۔",
            "آج نیا نظریہ کم ہے، کام زیادہ۔ artefact مکمل کریں: سوال، طریقہ، table یا chart، ایک نتیجہ۔",
            "بند کتاب {Unit 6} کا mock حل کریں۔ {Primary} اور {Secondary}، {Qualitative} اور {Quantitative} کی تعریف مثال کے ساتھ لکھیں۔",
            "فرہنگ کے صفحات کھول کر وہ اصطلاح دہرائیں جو زبان پر نہ آئی۔",
        )),
    day("xi", 24, 5, "Golden blitz", "Computer Systems", "Gates, K-maps and OSI without notes",
        "Logic Gates, K-Maps, SDLC and OSI", "xi14", 9, 14,
        ["Analog and digital", "Logic gates", "K-map", "SDLC", "OSI model"],
        T(
            "دن 24 صرف ★ {Golden blitz} ہے۔ نیا سبق نہیں۔",
            "بند کتاب بولیں: {Analog} بمقابلہ {Digital}، {AND} {OR} {NOT}، {NAND} اور {NOR} universal کیوں ہیں، {K-Map} کا قاعدہ، {Waterfall} بمقابلہ {Agile}، {OSI} کی سات تہیں۔",
            "جو تعریف نہ آئے، صفحہ ایک بار کھولیں، خاکہ نقل کریں، پھر فوراً بند کتاب دہرائیں۔",
        )),
    day("xi", 25, 5, "Golden blitz", "Algorithms and Programming", "Sorts, search, loops and keys",
        "Binary Search, loops, DBMS keys", "xi14", 32, 36,
        ["Bubble sort", "Binary search", "if and loops", "Primary key", "ER model"],
        T(
            "دن 25 {Golden blitz}، {Unit 2} سے {Unit 4} تک۔",
            "بند کتاب: {Algorithm} کی تعریف، {Bubble Sort} کا ایک pass، {Binary Search} کی شرط، {for} اور {while} کا فرق، {Primary key} اور {Foreign key}، {Referential integrity}۔",
            "صفحے کی جدول صرف اس وقت کھولیں جب تعریف رک جائے۔",
        )),
    day("xi", 26, 6, "Golden blitz", "Impacts and Digital Literacy", "AI, IoT, data types",
        "AI, IoT, data types and digital literacy", "xi56", 6, 16,
        ["AI", "IoT", "Data analytics", "Assistive technology", "Primary and secondary data"],
        T(
            "دن 26 {Golden blitz}، {Unit 5} اور {Unit 6}۔",
            "بند کتاب: {AI} کی تعریف، {IoT} کے چھ اجزا، {Data analytics}، {Assistive technology}، {Qualitative} بمقابلہ {Quantitative}، {Primary} بمقابلہ {Secondary}۔",
            "خاکہ صرف دیکھ کر بند کر دیں، پھر خود بنائیں۔",
        )),
    day("xi", 27, 6, "Recap", "All units", "Teach each chapter back in five minutes",
        "All Golden definitions", "xi14", 2, 5,
        ["Method", "Golden cards", "Diagram habit"],
        T(
            "دن 27 {Recap} ہے۔ ہر باب پانچ منٹ میں واپس سکھائیں، نوٹس بند۔",
            "ترتیب: {Computer Systems}، {Algorithms}، {Python}، {Database}، {AI} اور {IoT}، {Digital literacy}۔",
            "ہر باب میں ایک تعریف، ایک مثال، ایک خاکہ۔ اصطلاح انگریزی میں رہے۔ جو باب کمزور ہو، اس کا نام {Repair list} پر لکھیں۔",
        )),
    day("xi", 28, 6, "Mock", "All units", "Closed-book mock",
        "Sit the mock as an exam", "xi14", 23, 27,
        ["Closed book", "Time limit", "No new teaching"],
        T(
            "دن 28 {Mock} ہے۔ میں سبق نہیں پڑھاتا۔",
            "کتاب بند، فون دور، وقت رکھیں۔ {Unit 1} کا mock صفحوں پر ہے۔ باقی ابواب کے mock اپنے checkpoint دنوں والے صفحات پر دوبارہ بیٹھیں۔",
            "ہر خاکے والا سوال خالی نہ چھوڑیں۔ آدھا خاکہ بھی نمبر دیتا ہے۔ آج کلید نہ دیکھیں۔",
        )),
    day("xi", 29, 6, "Mark", "All units", "Mark against the key",
        "Build the Repair list", "xi56", 29, 34,
        ["Answer key", "Marking scheme", "Repair list"],
        T(
            "دن 29 {Mark} ہے۔ اندازے سے نمبر نہ لگائیں۔ کلید اور marking scheme سے میل کھائیں۔",
            "ہر کمزور ★ {Golden} {Repair list} میں لکھیں: اصطلاح، کیا غلط ہوا، کون سا خاکہ نہیں بنا۔",
            "60 فیصد سے کم باب کل کے {Repair} میں پہلے آئے۔",
        )),
    day("xi", 30, 6, "Repair", "All units", "Repair only yesterday’s list",
        "Repair list only", "xi14", 75, 80,
        ["Repair list", "Glossary", "Stop"],
        T(
            "دن 30 {Repair} ہے۔ نیا باب نہیں۔ صرف کل کی فہرست۔",
            "ہر اصطلاح فرہنگ میں دیکھیں، تعریف بند کتاب کہیں، خاکہ ایک بار بنائیں۔",
            "شام کو رک جائیں۔ دس بجے سوئیں۔ ہال میں کتاب نہیں ہوگی، ★ {Golden} سر میں ہونا چاہیے۔",
        )),
]

XII = [
    day("xii", 1, 1, "Teach", "Computer Systems — HCI", "What HCI is, and its components",
        "HCI and its components", "xii14", 6, 11,
        ["Human-Computer Interaction", "Human", "Computer", "Interaction", "Environment"],
        T(
            "السلام علیکم۔ {Class XII}، دن 01، {Unit 1}۔ ★ {Golden}: {HCI} اور اس کے اجزا۔",
            "{HCI} یعنی {Human-Computer Interaction}: انسان اور کمپیوٹر کے درمیان وہ ڈائیلاگ جس سے کام ہو۔",
            "اجزاء صفحے کے خاکے پر ہیں: {Human} صارف، {Computer} نظام، {Interaction} درمیان کا پل، اور {Environment} جگہ — گھر، کلاس، شور والی ورکشاپ، بیرونی {ATM}۔ خاکہ نقل کریں۔",
            "اچھا {HCI} غلطی کم کرتا ہے، کام تیز کرتا ہے، اور زیادہ لوگوں کو شامل کرتا ہے۔ اصطلاح {HCI} کا ترجمہ نہ لکھیں۔",
        )),
    day("xii", 2, 1, "Teach", "Computer Systems — HCI", "Accessibility, needs, UI, UX and Figma",
        "Accessibility, UI, UX and Figma", "xii14", 12, 17,
        ["Accessibility", "Contrast ratio", "Need analysis", "UI", "UX", "Wireframe", "Figma"],
        T(
            "دن 02۔ ★ {Golden}: {Accessibility}، {UI}، {UX}، {Wireframe}، {Figma}۔",
            "{Accessibility} کا مطلب ہے زیادہ سے زیادہ لوگ استعمال کر سکیں: contrast، پڑھنے کے قابل فونٹ، رنگ کے علاوہ لیبل، کی بورڈ سے راستہ۔",
            "متن کا contrast عموماً کم از کم {4.5 : 1} ہونا چاہیے۔ صفحے پر کم contrast اور زیادہ contrast کی مثال چھپی ہے۔ دونوں دیکھیں۔",
            "{UI} وہ ہے جو نظر آتا ہے: بٹن، متن، ترتیب۔ {UX} وہ احساس ہے جو کام کے بعد رہتا ہے۔ {Wireframe} لے آؤٹ کا سادہ خاکہ ہے۔ {Figma} میں prototype بنتا ہے۔",
            "دو frames جوڑنے کی {Figma} سیٹنگز صفحے پر ہیں۔ نام انگریزی میں نقل کریں۔",
        )),
    day("xii", 3, 1, "Checkpoint", "Computer Systems — HCI", "Test, evaluate and the unit mock",
        "Test and evaluate a user interface", "xii14", 18, 25,
        ["Usability test", "SUS", "Model answer", "Mock test"],
        T(
            "دن 03 {Checkpoint}۔ ★ {Golden}: interface کی جانچ۔",
            "جانچ میں حقیقی کام دیں، دیکھیں صارف کہاں رکتا ہے، پھر درستگی کریں۔ {SUS} دس سوالوں کا پیمانہ ہے، وفاداری {Net Promoter Score} سے الگ چیز ہے۔",
            "لمبے سوال کا طریقہ: مسئلہ لکھیں، {Accessibility} کی خلاف ورزی بتائیں، contrast کا نمبر دیں، پھر تجویز۔ صفحے کا model answer پڑھ کر بند کتاب اپنی زبان میں لکھیں۔",
            "mock بند کتاب۔ {HCI} کے اجزا کا خاکہ لازمی بنائیں۔",
        )),
    day("xii", 4, 1, "Teach", "Computational Thinking and Algorithms", "Correctness, clarity and the growth of work",
        "Algorithm correctness, clarity and Big O", "xii14", 26, 32,
        ["Correctness", "Clarity", "Modularity", "Readability", "Decomposition"],
        T(
            "دن 04، {Unit 2}۔ ★ {Golden}: {Correctness} اور {Clarity}۔",
            "درست الگورتھم ہر جائز input پر درست output دیتا ہے۔ واضح الگورتھم میں {Modularity} اور {Readability} ہوتے ہیں: چھوٹے نام والے حصے، دہرایا کام الگ فنکشن۔",
            "صفحے پر ایک بلاک بمقابلہ دو modules کا خاکہ ہے، {Figure 2.1}۔ نقل کریں اور بتائیں ماڈیول غلطی کہاں سمٹتا ہے۔",
            "{Trace table} قدم بہ قدم متغیر دکھاتی ہے۔ یہ درستگی جانچنے کا آلہ ہے۔ {Figure 2.2} دکھاتی ہے n بڑھنے پر کام کیسے بڑھتا ہے۔ گراف نقل کریں۔",
        )),
    day("xii", 5, 1, "Teach", "Computational Thinking and Algorithms", "Stacks, queues and Big O classes",
        "Stack, queue and Big O Notation", "xii14", 33, 40,
        ["Stack", "LIFO", "Queue", "FIFO", "Big O notation", "O(n²)", "O(n log n)"],
        T(
            "دن 05۔ ★ {Golden}: {Stack}، {Queue}، اور {Big O Notation}۔",
            "{Stack} {LIFO} ہے: آخری آیا، پہلے گیا، جیسے پلیٹوں کا ڈھیر۔ عمل {Push} اور {Pop}۔ {Queue} {FIFO} ہے: پہلا آیا، پہلے گیا، جیسے پرنٹر کی قطار۔",
            "صفحے پر {STACK} اور {QUEUE} کے خاکے چھپے ہیں۔ TOP کا تیر اور دونوں سمتیں نقل کریں۔",
            "{Big O} بتاتا ہے input بڑھنے پر قدم کتنے تیزی سے بڑھتے ہیں۔ {O(n²)} نیسٹڈ لوپ ہے۔ {O(n log n)} بڑی فہرست چھانٹنے کے لیے بہتر ہے۔ صفحے کی درجہ بندی والی table نقل کریں۔",
        )),
    day("xii", 6, 2, "Teach", "Computational Thinking and Algorithms", "Trace tables and choosing a structure",
        "Trace tables and choosing a data structure", "xii14", 41, 47,
        ["Trace table", "Linear search", "Factorial", "Choosing a structure"],
        T(
            "دن 06۔ ★ {Golden}: {Trace table} اور ساخت کا انتخاب۔",
            "trace میں ہر قدم کے بعد متغیر کی نئی قیمت لکھیں۔ صفحے کی traces دیکھیں: زیادہ سے زیادہ عدد، {Linear search}، factorial۔ پھر بند کتاب ایک نئی فہرست کا trace بنائیں۔",
            "انتخاب: واپسی کی تاریخ چاہیے تو {Stack}، باری چاہیے تو {Queue}، انڈیکس سے سیدھی رسائی چاہیے تو list۔ صفحے کا منظرنامہ والا جدول نقل کریں۔",
        )),
    day("xii", 7, 2, "Checkpoint", "Computational Thinking and Algorithms", "Trace tables and the unit mock",
        "Trace tables", "xii14", 48, 51,
        ["Trace table", "Linear search trace", "Factorial trace", "Mock test"],
        T(
            "دن 07 {Checkpoint}۔ ★ {Golden}: {Trace table}۔",
            "trace میں ہر قدم کے بعد متغیر کی نئی قیمت لکھیں۔ پرانی قیمت کاٹ کر نئی لکھنا امتحان میں نمبر دیتا ہے۔",
            "صفحے کی traces دیکھیں: زیادہ سے زیادہ عدد، {Linear search}، factorial۔ پھر بند کتاب ایک نئی فہرست کا trace خود بنائیں۔",
            "mock میں {Big O} کا موازنہ اور {Stack} بمقابلہ {Queue} لازمی آئے گا۔",
        )),
    day("xii", 8, 2, "Teach", "Programming Fundamentals", "Lists and tuples",
        "Lists and tuples", "xii14", 52, 58,
        ["List", "Index", "Slice", "Tuple", "Traversal"],
        T(
            "دن 08، {Unit 3}۔ ★ {Golden}: {List} اور {Tuple}۔",
            "{List} بدلنے کے قابل ترتیب ہے۔ انڈیکس 0 سے شروع۔ {append}، {insert}، {pop}، {len}۔",
            "{Slice} کا اصول: start شامل، stop شامل نہیں۔ {Tuple} ترتیب تو ہے مگر بدل نہیں سکتی۔ گول قوسین، اور اگر ایک عنصر ہو تو آخر میں comma۔",
            "{Traversal} بائیں سے دائیں: {for item in list}۔ صفحے کی slice tables نقل کریں اور تین slice بند کتاب لکھیں۔",
        )),
    day("xii", 9, 2, "Teach", "Programming Fundamentals", "Sets and dictionaries",
        "Sets and dictionaries", "xii14", 59, 65,
        ["Set", "Union", "Intersection", "Dictionary", "Key", "Value"],
        T(
            "دن 09۔ ★ {Golden}: {Set} اور {Dictionary}۔",
            "{Set} میں دہرایا عنصر نہیں رہتا، اور ترتیب کا وعدہ نہیں۔ {Union} دونوں کا مجموعہ، {Intersection} مشترک، difference وہ جو پہلے میں ہو دوسرے میں نہ ہو۔",
            "{Dictionary} {key} سے {value} جوڑتا ہے۔ key منفرد ہوتی ہے۔ طلبہ کے نام سے نمبر، یہ dictionary ہے۔",
            "صفحے کی set drills خود حساب کریں، پھر {Python} سے ملا کر دیکھیں۔",
        )),
    day("xii", 10, 2, "Teach", "Programming Fundamentals", "Functions, scope and files",
        "Functions, scope and file handling", "xii14", 66, 72,
        ["Function", "Parameter", "Return", "Scope", "open()", "with open()"],
        T(
            "دن 10۔ ★ {Golden}: {Function}، {scope}، اور files۔",
            "{Function} نام والا بلاک ہے جو {parameter} لیتا ہے اور {return} سے جواب دیتا ہے۔ {Figure 3.6} کال کا سفر دکھاتی ہے۔ خاکہ نقل کریں۔",
            "{Local scope} فنکشن کے اندر۔ {Global} باہر۔ اندر کا نام باہر نہیں ملتا جب تک واپس نہ کیا جائے۔",
            "فائل: {open(path, mode)}، {read}، {readline}، {readlines}، {write}، {close}۔ ★ {with open()} زیادہ محفوظ ہے کیونکہ بلاک ختم ہوتے ہی فائل بند ہو جاتی ہے۔",
        )),
    day("xii", 11, 3, "Checkpoint", "Programming Fundamentals", "Predict the output and the unit mock",
        "Functions and file handling", "xii14", 73, 76,
        ["Predict the output", "Scope bugs", "Mock test"],
        T(
            "دن 11 {Checkpoint}۔ پہلے output خود بتائیں، پھر صفحہ دیکھیں۔",
            "عام غلطیاں: slice میں stop شامل سمجھ لینا، set میں ترتیب مان لینا، {close()} بھول جانا، local متغیر باہر چھاپنا۔",
            "mock بند کتاب۔ ایک فنکشن لکھیں جو فہرست کا سب سے بڑا عدد بنائے، بغیر {max()} کے۔ اور {with open()} کی ایک وجہ لکھیں۔",
        )),
    day("xii", 12, 3, "Teach", "Data and Analysis", "Database connectivity and DataFrames",
        "Database connectivity and DataFrames", "xii14", 77, 82,
        ["SQL", "Connection", "Cursor", "commit()", "DataFrame", "Cleaning"],
        T(
            "دن 12، {Unit 4}۔ ★ {Golden}: database connectivity اور {DataFrame}۔",
            "پروگرام database سے {connection} بناتا ہے، {cursor} سوال چلاتا ہے، {commit()} تبدیلی مستقل محفوظ کرتا ہے۔ {commit()} کے بغیر {INSERT}، {UPDATE}، {DELETE} فائل میں نہیں جمے۔",
            "{DataFrame} جدول جیسا object ہے، قطاریں مشاہدے، کالم متغیر۔ صفائی: خالی قدر، غلط قسم، دہرایا ریکارڈ۔",
            "صفحے کا کوڈ خود ٹائپ کریں۔ {SQL} انگریزی میں ہی لکھیں۔",
        )),
    day("xii", 13, 3, "Teach", "Data and Analysis", "Charts with matplotlib",
        "matplotlib charts", "xii14", 83, 88,
        ["bar chart", "line chart", "histogram", "matplotlib", "Axis labels"],
        T(
            "دن 13۔ ★ {Golden}: {matplotlib} سے charts۔",
            "{bar chart} زمروں کا موازنہ۔ {line chart} وقت کے ساتھ رجحان۔ {histogram} عدد کی تقسیم، مسلسل وقفے۔",
            "ہر chart پر عنوان، محور کے نام، اور اکائی ہونی چاہیے۔ صفحے کی شکل نقل کریں، پھر بتائیں یہ bar ہے یا histogram، اور کیوں۔",
            "جھوٹا پیمانہ معنی بدل دیتا ہے۔ محور صفر سے شروع ہے یا نہیں، یہ امتحانی نکتہ ہے۔",
        )),
    day("xii", 14, 3, "Checkpoint", "Data and Analysis", "Mean, median, mode, spread",
        "Mean, median and variance", "xii14", 89, 95,
        ["Mean", "Median", "Mode", "Variance", "Outlier", "Mock test"],
        T(
            "دن 14 {Checkpoint}۔ ★ {Golden}: {Mean}، {Median}، {Mode}، {Variance}۔",
            "{Mean} اوسط ہے۔ {Median} درمیانہ قدر جب data ترتیب شدہ ہو۔ {Mode} سب سے زیادہ بار آنے والی قدر۔ mode ایک ہو، زیادہ ہوں، یا کوئی نہ ہو۔",
            "{Variance} پھیلاؤ کا مربع ہے۔ کم variance: قدریں mean سے چمٹی ہوئی۔ زیادہ variance: بکھری ہوئی۔ صفحے کی {Figure 4.3} دونوں دکھاتی ہے، mean ایک جیسا، پھیلاؤ الگ۔ نقل کریں۔",
            "{Outlier} دور کی قدر ہے۔ باڑ کا قاعدہ صفحے پر ہے: {1.5} ضرب {IQR}۔ mock بند کتاب۔",
        )),
    day("xii", 15, 3, "Teach", "Applications and Impacts of Computing", "Neural networks and deep learning",
        "Neural Networks and Deep Learning", "xii56", 1, 5,
        ["Machine learning", "Neural network", "Deep learning", "Neuron", "Activation"],
        T(
            "دن 15، {Unit 5}۔ ★ {Golden}: {Neural Networks} اور {Deep Learning}۔",
            "{Machine learning} data سے نمونے سیکھ کر پیش گوئی کرتا ہے۔ {Neural network} جڑے ہوئے nodes کی تہیں ہیں: {input layer}، {hidden layer}، {output layer}۔ یہ model ہے۔",
            "★ {Deep learning} وہ طریقہ ہے جو کئی hidden layers اور بہت سے data سے، اکثر {GPU} پر، اس model کو سکھاتا ہے۔ model اور method الگ ہیں۔ مثال: چہرے سے فون کھولنا۔",
            "صفحے پر ایک neuron کا خاکہ ہے: inputs، weights، {bias}، weighted sum، {activation}، output۔ علامات x1، w1، Σ، f(z) نقل کریں۔ یہ خاکہ امتحان میں بنتا ہے۔",
        )),
    day("xii", 16, 4, "Teach", "Applications and Impacts of Computing", "Secure collaboration and threats",
        "Secure collaboration and security threats", "xii56", 6, 11,
        ["Authentication", "Authorisation", "Encryption", "Phishing", "Malware", "Password strength"],
        T(
            "دن 16۔ ★ {Golden}: محفوظ اشتراک اور خطرات۔",
            "{Authentication} پوچھتا ہے آپ کون ہیں۔ {Authorisation} بتاتا ہے آپ کو کیا کرنے کی اجازت ہے۔ دونوں الگ ہیں۔",
            "خطرات: {Phishing} جعلی پیغام، {Malware} نقصان دہ سافٹ ویئر، کمزور پاس ورڈ، غیر محفوظ لنک۔ تدارک: لمبا ملا جلا پاس ورڈ، دو مرحلے کی تصدیق، شک کی ای میل پر کلک نہ کریں۔",
            "صفحے پر پاس ورڈ کی گنتی اور Caesar cipher کا ذکر ہے۔ اعداد کی طاقت دیکھیں: لمبائی بڑھے تو امکان دیوار کی طرح بڑھتا ہے۔ جدول نقل کریں۔",
        )),
    day("xii", 17, 4, "Checkpoint", "Applications and Impacts of Computing", "Equity, access and the unit mock",
        "Equity and equal access", "xii56", 12, 17,
        ["Equity", "Equal access", "Deep learning in healthcare", "Mock test"],
        T(
            "دن 17 {Checkpoint}۔ ★ {Golden}: {Equity} اور {equal access}۔",
            "{Equality} سب کو ایک جیسا دینا ہے۔ {Equity} ضرورت کے مطابق اضافی سہارا دینا تاکہ موقع برابر ہو۔ دیہی اسکول میں آف لائن مواد equity ہو سکتا ہے۔",
            "لمبے سوال میں پاکستان کی صحت کی مثال: {X-ray} input، deep neural model، بیماری کی نشاندہی output۔ حدود بھی لکھیں: غلط تشخیص، data کی رازداری۔",
            "mock بند کتاب۔ neuron کا خاکہ اور ایک threat لازمی۔",
        )),
    day("xii", 18, 4, "Teach", "Entrepreneurship in the Digital Age", "Entrepreneur, problem and idea",
        "Entrepreneur and entrepreneurship", "xii56", 18, 22,
        ["Entrepreneur", "Entrepreneurship", "Problem", "Idea", "Calculated risk"],
        T(
            "دن 18، {Unit 6}۔ ★ {Golden}: {Entrepreneur} اور {Entrepreneurship}۔",
            "{Entrepreneur} مسئلہ دیکھتا ہے، حل سوچتا ہے، اور اسے پروڈکٹ یا سروس بناتا ہے۔ اکثر چھوٹا آغاز، لوگوں کی بات، سمجھ بوجھ کا خطرہ۔",
            "سفر کا خاکہ صفحے پر ہے: {Problem}، {Idea}، {Prototype}، {Feedback}، {MVP}، {Beachhead}۔ یہ تیر نقل کریں۔ یہی باب کا نقشہ ہے۔",
            "مقامی مثال انگریزی اصطلاح کے ساتھ لکھیں، جیسے اسکول کی کینٹین کی قطار کے لیے آرڈر ایپ۔",
        )),
    day("xii", 19, 4, "Teach", "Entrepreneurship in the Digital Age", "Prototypes and fidelity",
        "Prototype and fidelity", "xii56", 23, 27,
        ["Prototype", "Low fidelity", "Mid fidelity", "High fidelity", "Iteration"],
        T(
            "دن 19۔ ★ {Golden}: {Prototype} اور fidelity۔",
            "{Prototype} نمونہ ہے جو دکھاتا ہے حل کیسا لگے گا یا کیسے چلے گا۔ {Low-fidelity} کاغذ۔ {Mid-fidelity} کلک ہونے والا خاکہ۔ {High-fidelity} اصل کے قریب۔",
            "{Figure 6.1} تینوں دکھاتی ہے۔ نقل کریں۔ {Figure 6.2} چکر ہے: بنائیں، آزمائیں، سنیں، بہتر کریں۔ اس چکر کا نام {iteration} ہے۔",
            "عام غلطی: prototype اور {MVP} کو ایک سمجھنا۔ prototype دکھاتا ہے، {MVP} حقیقی صارف کے لیے واقعی چلتا ہے۔",
        )),
    day("xii", 20, 5, "Teach", "Entrepreneurship in the Digital Age", "MVP and the riskiest assumption",
        "MVP and the riskiest assumption", "xii56", 28, 32,
        ["MVP", "Riskiest assumption", "Cost per user", "Ethics"],
        T(
            "دن 20۔ ★ {Golden}: {MVP} اور {riskiest assumption}۔",
            "{MVP} یعنی {Minimum Viable Product}: سب سے چھوٹی چیز جو حقیقی صارف کے اصل کام آئے، تاکہ سیکھا جا سکے۔",
            "{Riskiest assumption} وہ مفروضہ ہے جس کے غلط ہونے پر پورا خیال گر جائے۔ آن لائن ٹیوشن میں خطرناک مفروضہ یہ ہو سکتا ہے کہ طلبہ پیسے دیں گے۔ پہلے اسی کو آزمائیں۔",
            "صفحے کی لاگت دیکھیں: سستا ٹیسٹ جلدی اور کم نقصان سے غلط ثابت ہوتا ہے۔ اخلاق: صرف ضروری ذاتی معلومات، اجازت کے بغیر تصویر شیئر نہیں، جھوٹا دعویٰ نہیں۔",
        )),
    day("xii", 21, 5, "Checkpoint", "Entrepreneurship in the Digital Age", "Beachhead market and the final project",
        "Beachhead market and the MVP plan", "xii56", 33, 36,
        ["Beachhead market", "MVP plan", "Features, cost, marketing", "Mock test"],
        T(
            "دن 21 {Checkpoint}۔ ★ {Golden}: {Beachhead market} اور {MVP} کا منصوبہ۔",
            "{Beachhead} پہلی چھوٹی منڈی ہے جہاں پورا زور لگائیں۔ چھوٹی اس لیے کہ سیکھنا تیز ہو، پھیلنے سے پہلے۔",
            "منصوبے میں تین کالم: features، cost، marketing۔ صفحے کی مثال نقل کریں، پھر اپنا ایک مسئلہ اسی خاکے میں اتاریں۔",
            "mock بند کتاب۔ {Prototype} اور {MVP} کا فرق، اور ایک {riskiest assumption} لازمی۔",
        )),
    day("xii", 22, 5, "Teach", "Revision tools", "Flashcards and the formula sheet",
        "Bilingual flashcards and the formula sheet", "xii56", 37, 42,
        ["Flashcards", "Formula sheet", "Big O", "Variance", "Contrast ratio"],
        T(
            "دن 22۔ ★ {Golden} کارڈز اور فارمولہ شیٹ۔",
            "فلیش کارڈ: اصطلاح انگریزی میں پڑھیں، اردو معنی بولیں، پھر نیچے کی سطر دیکھیں۔ الٹا نہ کریں — امتحان میں اصطلاح انگریزی ہی لکھی جائے گی۔",
            "فارمولہ شیٹ پر {Big O}، variance، contrast، اور {MVP} کی لاگت ایک صفحے پر ہے۔ رنگ اکائی بتاتا ہے۔ پورا صفحہ کاپی میں اتاریں۔",
        )),
    day("xii", 23, 5, "Checkpoint", "Revision tools", "Glossary and the tracker",
        "Glossary terms", "xii56", 43, 49,
        ["Glossary", "Answer key", "Assessment tracker"],
        T(
            "دن 23 {Checkpoint}۔ فرہنگ A سے Z۔",
            "ہر وہ اصطلاح گھیریں جو کل کے mock میں کمزور رہے۔ {Equity}، {Wireframe}، {Net Promoter Score}، {Malware} جیسی اصطلاحات انگریزی میں دہرائیں۔",
            "ٹریکر پر نشان لگائیں: کون سا سبق پڑھا، کون سا خاکہ بنا، کون سا mock ہوا۔ خالی خانہ کل کے {Repair} میں جائے گا۔",
        )),
    day("xii", 24, 5, "Golden blitz", "HCI", "HCI diagrams without notes",
        "HCI, accessibility, UI and UX", "xii14", 6, 11,
        ["HCI components", "Contrast", "Wireframe", "Figma"],
        T(
            "دن 24 {Golden blitz}۔ {Unit 1} کے خاکے بند کتاب۔",
            "بولیں اور بنائیں: {HCI} کے چار اجزا، contrast {4.5 : 1}، {UI} بمقابلہ {UX}، {Wireframe}۔",
            "صفحہ صرف اس وقت کھولیں جب شکل نہ بنے۔",
        )),
    day("xii", 25, 6, "Golden blitz", "Computational Thinking and Algorithms", "Stack, queue and Big O without notes",
        "Stack, queue and Big O Notation", "xii14", 33, 40,
        ["Big O", "Stack", "Queue", "Trace table", "Mean", "Variance"],
        T(
            "دن 25 {Golden blitz}۔ صفحات پر {Stack}، {Queue} اور {Big O} کے خاکے ہیں۔ بند کتاب بنائیں: {LIFO}، {FIFO}، {O(n²)} بمقابلہ {O(n log n)}۔",
            "جو شکل نہ بنے صرف ایک بار صفحہ کھولیں، نقل کریں، پھر بند کر دیں۔",
        )),
    day("xii", 26, 6, "Golden blitz", "AI and Entrepreneurship", "Neuron diagram and MVP",
        "Neural Networks, equity, prototype and MVP", "xii56", 1, 5,
        ["Neural network", "Deep learning", "Phishing", "Equity", "Prototype", "MVP", "Beachhead"],
        T(
            "دن 26 {Golden blitz}۔ سب سے اہم خاکہ neuron کا ہے: inputs، weights، bias، activation۔",
            "پھر {Authentication} بمقابلہ {Authorisation}، {Equity} بمقابلہ equality، {Prototype} بمقابلہ {MVP}، {Beachhead}۔",
            "جو خاکہ نہ بنے وہی کل کے {Repair} میں پہلا نمبر ہے۔",
        )),
    day("xii", 27, 6, "Recap", "All units", "Teach each chapter back",
        "All Golden definitions", "xii14", 1, 5,
        ["HCI", "Big O", "Python structures", "Statistics", "Neural networks", "MVP"],
        T(
            "دن 27 {Recap}۔ چھ ابواب، ہر ایک پانچ منٹ، نوٹس بند۔",
            "ترتیب: {HCI}، {Algorithms}، {Python}، {Data and Analysis}، {Neural Networks}، {Entrepreneurship}۔",
            "ہر باب: تعریف، مثال، خاکہ۔ کمزور باب {Repair list} پر۔",
        )),
    day("xii", 28, 6, "Mock", "All units", "Closed-book mock",
        "Sit the mock as an exam", "xii56", 16, 17,
        ["Closed book", "30 marks", "Diagrams compulsory"],
        T(
            "دن 28 {Mock} ہے۔ سبق بند۔ وقت رکھیں، فون دور۔",
            "خاکے والے سوال خالی نہ چھوڑیں: {HCI} کے اجزا، neuron، {Stack}، chart کا انتخاب۔",
            "آج کلید نہیں۔ کل نمبر لگیں گے۔",
        )),
    day("xii", 29, 6, "Mark", "All units", "Mark against the answer key",
        "Build the Repair list", "xii56", 45, 48,
        ["Answer key", "Marking", "Repair list"],
        T(
            "دن 29 {Mark} ہے۔ کلید سے میل کھائیں، اندازے سے نہیں۔",
            "ہر کٹا ہوا خاکہ اور ہر غلط اصطلاح {Repair list} میں لکھیں۔ اصطلاح کی ہجے انگریزی میں درست کریں۔",
        )),
    day("xii", 30, 6, "Repair", "All units", "Repair only yesterday’s list",
        "Repair list only", "xii56", 38, 42,
        ["Flashcards", "Formula sheet", "Stop"],
        T(
            "دن 30 {Repair} ہے۔ صرف کل کی فہرست۔ فلیش کارڈ اور فارمولہ شیٹ کھولیں۔",
            "ہر کارڈ: انگریزی اصطلاح، ایک اردو جملہ سمجھ کا، ایک خاکہ۔ پھر کارڈ بند۔",
            "شام کو رک جائیں۔ نیا باب نہیں۔ ہال میں ★ {Golden} سر میں ہونا چاہیے۔ اللہ حافظ۔",
        )),
]


def display(d: dict, start: int, end: int) -> str:
    cards = "\n".join(f"• {t}" for t in d["topics"])
    return (
        f"Teach Yourself · Day {d['day']:02d} of 30 · Week {d['week']} · {d['kind']}\n"
        f"Chapter: {d['chapter']}\n"
        f"Learning aim: {d['focus']}\n"
        f"★ Golden (must be spoken without notes): {d['golden']}\n"
        f"Booklet pages {start}–{end} (as printed). Every symbol and diagram on these pages is inside the app.\n\n"
        "3-hour tutoring block\n"
        "1. Recap (0–15 min) — yesterday’s Golden, closed book.\n"
        "2. Teach (15–105 min) — today’s pages, including every diagram.\n"
        "3. Drill (105–135 min) — closed-book questions.\n"
        "4. Homework (135–180 min) — one 5-mark answer: Define · Explain · Example · Diagram · Working.\n\n"
        f"Learning outcomes\n{cards}\n\n"
        "Exam rule: keep English terms exactly as printed. Do not translate them."
    )


XI_INTRO = T(
    "السلام علیکم۔ میں آپ کا {Computer Science} کا استاد ہوں۔ یہ {Class XI} کا تیس دن کا {Teach Yourself Crash Course} ہے، {New Sindh Curriculum 2026}۔",
    "کتابچہ اساتذہ والا دو لسانی ایڈیشن ہے۔ میں اردو میں سمجھاؤں گا۔ امتحانی اصطلاحات انگریزی میں ویسی ہی رہیں گی جیسے صفحے پر چھپی ہیں — {Algorithm}، {Logic Gates}، {SDLC}، {IoT}۔",
    "ہر علامت، گیٹ، جدول اور خاکہ ایپ کے اندر چھپا ہوا ہے۔ صفحہ میری بات کے ساتھ کھلے گا۔ خاکہ کاپی میں نقل کریں۔",
    "دن 1 سے 23 پڑھاتے ہیں، ہر باب کا آخری دن {Checkpoint} ہے۔ دن 24 سے 26 ★ {Golden blitz}، دن 27 {Recap}، دن 28 {Mock}، دن 29 {Mark}، دن 30 {Repair}۔",
    "ہر نشست تین گھنٹے: پندرہ منٹ کل کا {Golden}، پھر صفحات، پھر بند کتاب مشق، رات کو پانچ نمبر {Define} {Explain} {Example} {Diagram} {Working} سے۔",
)

XII_INTRO = T(
    "السلام علیکم۔ میں آپ کا {Computer Science} کا استاد ہوں۔ یہ {Class XII} کا تیس دن کا {Teach Yourself Crash Course} ہے، {New Sindh Curriculum 2026}۔",
    "باب: {HCI}، {Algorithms} اور {Big O Notation}، {Python} کے {List} {Tuple} {Set} {Dictionary}، {Data and Analysis}، {Neural Networks}، اور {MVP}۔",
    "میں اردو میں سمجھاؤں گا۔ یہ اصطلاحات انگریزی میں ویسی ہی بولیں جیسی کتابچے پر چھپی ہیں۔ neuron، contrast، اور prototype کے خاکے ایپ میں شامل ہیں۔ انہیں نقل کریں۔",
    "طریقہ وہی ہے: تین گھنٹے، ★ {Golden} پہلے، {Checkpoint} مت چھوڑو، آخری دن {Repair}۔",
)


def build_course() -> None:
    doc = pymupdf.open(PDF)
    counts = {"xi14": 80, "xi56": 64, "xii14": 95, "xii56": 49}
    assert doc.page_count == sum(counts.values()), doc.page_count
    offset = {}
    cursor = 0
    for key, n in counts.items():
        offset[key] = cursor
        cursor += n

    def place(days: list[dict]) -> list[dict]:
        placed = []
        for d in days:
            start = offset[d["book"]] + d["localStart"]
            end = offset[d["book"]] + d["localEnd"]
            if not (1 <= start <= end <= doc.page_count):
                raise SystemExit(f"bad range {d['course']} day {d['day']}: {start}-{end}")
            placed.append({**d, "startPage": start, "endPage": end})
        return placed

    def course(cid: str, title: str, subtitle: str, days: list[dict], intro: str, intro_book: str) -> dict:
        placed = place(days)
        intro_start = offset[intro_book] + 1
        intro_end = offset[intro_book] + 5
        out_days = []
        for d in placed:
            out_days.append({
                "id": f"{cid}-d{d['day']:02d}",
                "day": d["day"],
                "week": d["week"],
                "kind": d["kind"],
                "chapter": d["chapter"],
                "focus": d["focus"],
                "golden": d["golden"],
                "startPage": d["startPage"],
                "endPage": d["endPage"],
                "topics": d["topics"],
                "script": d["script"],
                "displayText": display(d, d["startPage"], d["endPage"]),
            })
        return {
            "id": cid,
            "title": title,
            "subtitle": subtitle,
            "introStartPage": intro_start,
            "introEndPage": intro_end,
            "introScript": intro,
            "introDisplay": (
                f"{title}. Teacher’s Edition, bilingual. "
                "30 days. Urdu tutor. English exam terms as printed. "
                "Every symbol and diagram from the booklet is embedded in this app."
            ),
            "days": out_days,
        }

    root = {
        "courses": [
            course(
                "xi",
                "Computer Science XI",
                "Teach Yourself · Units 1–6 · Teacher’s Edition",
                XI,
                XI_INTRO,
                "xi14",
            ),
            course(
                "xii",
                "Computer Science XII",
                "Teach Yourself · Units 1–6 · Teacher’s Edition",
                XII,
                XII_INTRO,
                "xii14",
            ),
        ]
    }
    # Coverage report.
    covered = set()
    for c in root["courses"]:
        covered.update(range(c["introStartPage"], c["introEndPage"] + 1))
        for d in c["days"]:
            covered.update(range(d["startPage"], d["endPage"] + 1))
            assert d["day"] and d["script"] and d["startPage"] <= d["endPage"]
        assert [d["day"] for d in c["days"]] == list(range(1, 31))
    missing = [i for i in range(1, doc.page_count + 1) if i not in covered]
    print("uncovered pages", missing)
    COURSE.write_text(json.dumps(root, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"course.json {COURSE.stat().st_size} bytes")
    for c in root["courses"]:
        print(c["id"], "days", len(c["days"]), "intro", c["introStartPage"], c["introEndPage"])
        for d in c["days"]:
            print(f"  d{d['day']:02d} {d['kind']:12} p{d['startPage']}-{d['endPage']} {d['golden'][:48]}")


if __name__ == "__main__":
    extract_pages()
    build_course()
    import embed_tts_text
    embed_tts_text.main()
