package com.csxi.ultimatecoaching.data

object Curriculum {

    val homeCoachUrdish: String = """
        Assalam o alaikum. Main aapka CS eleven Ultimate Coach hoon.
        Yeh Sindh Curriculum 2026, Class eleven, Computer Science hai — Units 1 se 6.
        Technical terms English mein hi rahenge, jaise exam paper mein.
        Unit 1 Computer Systems: analog digital binary, saat logic gates, S D L C, O S I aur T C P I P.
        Unit 2 Computational thinking aur algorithms: bubble, selection, linear, binary.
        Unit 3 Programming: Python, V S Code, variables, operators, if, for, while, debugging.
        Unit 4 Database: D B M S, keys, E R model, Access tables, forms, queries.
        Unit 5 Applications: A I, I o T ke chhe ajza, analytics, impacts, assistive tech.
        Unit 6 Digital literacy: data types, collection, primary secondary, inquiry project.
        Har lesson mein booklet ka asli diagram embedded hai. Pehle diagram dekho, phir Listen dabao.
        Rozana 45 se 60 minute: 5 minute flashcards, 20 minute lesson, 15 minute Try it, 10 minute Check yourself.
        Chalo, koi unit kholo aur coaching shuru karo.
    """.trimIndent()

    fun units(): List<CourseUnit> = listOf(unit1(), unit2(), unit3(), unit4(), unit5(), unit6())

    fun unit(id: String): CourseUnit? = units().find { it.id == id }

    fun lesson(id: String): Lesson? = units().asSequence().flatMap { it.lessons.asSequence() }.find { it.id == id }

    fun allLessons(): List<Lesson> = units().flatMap { it.lessons }

    private fun w(en: String, ur: String) = WordItem(en, ur)
    private fun c(qe: String, qu: String, ae: String, au: String) = CheckItem(qe, qu, ae, au)

    private fun lesson(
        id: String, unitId: String, code: String,
        titleEn: String, titleUr: String, titleUrdish: String,
        periods: String, textbook: String,
        words: List<WordItem>,
        keyIdeaEn: String, keyIdeaUr: String,
        learnEn: String, learnUr: String,
        coachUrdish: String,
        tryItEn: String, tryItUr: String,
        checks: List<CheckItem>,
        iCanEn: List<String>, iCanUr: List<String>,
        diagram: String, bookletPages: List<String>,
        isRevision: Boolean = false
    ) = Lesson(
        id, unitId, code, titleEn, titleUr, titleUrdish, periods, textbook, words,
        keyIdeaEn, keyIdeaUr, learnEn, learnUr, coachUrdish, tryItEn, tryItUr,
        checks, iCanEn, iCanUr, diagram, bookletPages, isRevision
    )

    private fun unit1(): CourseUnit = CourseUnit(
        id = "u1", number = 1,
        titleEn = "Computer Systems",
        titleUr = "کمپیوٹر سسٹمز",
        titleUrdish = "Computer Systems — Computer ke nizaam",
        weeks = "3 weeks · 9–10 periods",
        colorHex = "#0B3D91",
        coverDiagram = "diagrams/logic_gates.png",
        summaryEn = "Analog vs digital, seven logic gates, SDLC, Waterfall/Agile, OSI and TCP/IP.",
        summaryUr = "اینالاگ بمقابلہ ڈیجیٹل، سات لاجک گیٹس، ایس ڈی ایل سی، واٹر فال/ایجائیل، او ایس آئی اور ٹی سی پی/آئی پی۔",
        lessons = listOf(
            lesson(
                "1.1a", "u1", "1.1a",
                "Analog, digital and binary", "اینالاگ، ڈیجیٹل اور بائنری",
                "Analog, digital aur binary",
                "4 periods (shared 1.1)", "Textbook pp. 2–4",
                listOf(w("analog", "اینالاگ"), w("digital", "ڈیجیٹل"), w("binary", "بائنری"), w("bit", "بٹ"), w("signal", "سگنل")),
                "Digital uses only two values, 0 and 1. Analog can take any value in a range.",
                "ڈیجیٹل صرف دو قدریں استعمال کرتا ہے، 0 اور 1۔ اینالاگ حد میں کوئی بھی قدر لے سکتا ہے۔",
                "Discrete quantities are separable and countable (students in a class, cars in a park). Continuous quantities can take any value in a range (water temperature, time). A digital system uses only two values, 0 and 1, called bits. It is reliable, programmable and easy to copy, so computers, smartphones, digital watches, calculators, traffic lights and digital cameras all use it.\n\nLook at the booklet figure: the analog panel is a smooth sine wave — any voltage is allowed. The digital panel is a square wave — only HIGH (1) or LOW (0). The stairs-versus-ramp analogy: stairs have fixed heights (digital); a ramp stands at any height (analog).\n\nMaths corner: n bits give 2ⁿ patterns. To convert binary to decimal, multiply each bit by a power of 2. Example: 1011₂ = 8+0+2+1 = 11₁₀. A bit is not a byte — a byte is a group of 8 bits.",
                "منقطع مقداریں الگ اور گنتی کے قابل ہیں (جماعت کے طلبہ، پارک کی گاڑیاں)۔ مسلسل مقدار حد میں کوئی بھی قدر لے سکتی ہے (پانی کا درجہ حرارت، وقت)۔ ڈیجیٹل نظام صرف 0 اور 1 استعمال کرتا ہے جنہیں بٹس کہتے ہیں۔ یہ قابل اعتماد، قابل پروگرام اور نقل کے لیے آسان ہے اس لیے کمپیوٹر، اسمارٹ فون، ڈیجیٹل گھڑی، کیلکولیٹر، ٹریفک لائٹس اور ڈیجیٹل کیمرے یہی استعمال کرتے ہیں۔\n\nکتابچے کی شکل دیکھیں: اینالاگ سائن ویو ہے — کوئی بھی وولٹیج ممکن۔ ڈیجیٹل مربع موج ہے — صرف ہائی (1) یا لو (0)۔ سیڑھیاں بمقابلہ ramp: سیڑھیاں مقررہ قدموں والی (ڈیجیٹل)؛ ramp کسی بھی اونچائی پر (اینالاگ)۔\n\nریاضی: n بٹس سے 2ⁿ نمونے بنتے ہیں۔ بائنری کو اعشاری بنانے کے لیے ہر بٹ کو 2 کی طاقت سے ضرب دیں۔ بٹ بائٹ نہیں — بائٹ 8 بٹس کا گروپ ہے۔",
                "Assalam o alaikum. Aaj ka topic Analog, Digital aur Binary hai. Teen words yaad rakhna: analog, digital, binary. Analog signal continuously change hota hai, jaise analog clock ki sui ya awaz ka wave. Digital signal sirf do levels use karta hai: HIGH yani 1, aur LOW yani 0. Computer digital hai kyunke uski language binary hai. Booklet ka diagram dekho: left side sine wave, right side square wave. Stairs versus ramp: stairs pe sirf fixed steps hain — ye digital hai. Ramp pe koi bhi height ho sakti hai — ye analog hai. Exam tip: bit sirf 0 ya 1 hoti hai; byte 8 bits ka group hai. n bits se 2 to the power n patterns bante hain. Digital noise better resist karta hai kyunke uske sirf do clear levels hain. Check yourself: 4 bits se 16 patterns; 1011 binary 11 decimal hai.",
                "Redraw Figure 1.1 from memory: analog sine wave, digital square wave, stairs and ramp. Label each side Analog / Digital in English and Urdu.",
                "شکل 1.1 یاد سے بنائیں: اینالاگ سائن ویو، ڈیجیٹل مربع موج، سیڑھیاں اور ramp۔ دونوں طرف اینالاگ / ڈیجیٹل لکھیں۔",
                listOf(
                    c("Give two discrete and two continuous examples.", "دو منقطع اور دو مسلسل مثالیں دیں۔",
                        "Discrete: students in a class, books on a shelf. Continuous: temperature of water, height of a person.",
                        "منقطع: جماعت کے طلبہ، شیلف کی کتابیں۔ مسلسل: پانی کا درجہ حرارت، قد۔"),
                    c("Which signal resists noise better, and why?", "کون سا سگنل شور کا بہتر مقابلہ کرتا ہے؟",
                        "Digital: it has only two clear levels, so small disturbances do not change 0 or 1.",
                        "ڈیجیٹل: صرف دو واضع سطحیں ہیں، چھوٹی خلل 0 یا 1 نہیں بدلتی۔"),
                    c("What do 0 and 1 stand for in a digital system?", "ڈیجیٹل نظام میں 0 اور 1 کیا کرتے ہیں؟",
                        "0 = OFF / LOW / FALSE; 1 = ON / HIGH / TRUE.",
                        "0 = بند / نیچی / غلط؛ 1 = چالو / اونچی / درست۔"),
                    c("How many patterns can 4 bits make? Convert 1011₂.", "4 بٹس کتنے نمونے بناتی ہیں؟ 1011₂ تبدیل کریں۔",
                        "2⁴ = 16 patterns; 1011₂ = 8+0+2+1 = 11₁₀.",
                        "2⁴ = 16 نمونے؛ 1011₂ = 11۔")
                ),
                listOf("Tell analog from digital", "Explain a bit and a byte", "Convert a short binary number"),
                listOf("اینالاگ اور ڈیجیٹل الگ کر سکتا/سکتی ہوں", "بٹ اور بائٹ بتا سکتا/سکتی ہوں", "چھوٹا بائنری عدد بدل سکتا/سکتی ہوں"),
                "diagrams/analog_digital.png",
                listOf("booklet/v1_p08.jpg", "booklet/v1_p09.jpg")
            ),
            lesson(
                "1.1b", "u1", "1.1b",
                "Boolean algebra and the seven logic gates", "بولین الجبرا اور سات لاجک گیٹس",
                "Boolean algebra aur saat logic gates",
                "4 periods (shared 1.1)", "Textbook pp. 5–12",
                listOf(w("Boolean algebra", "بولین الجبرا"), w("logic gate", "لاجک گیٹ"), w("truth table", "سچائی جدول"), w("inverter", "انورٹر"), w("universal gate", "یونیورسل گیٹ")),
                "A logic gate is an electronic circuit with one output. NAND and NOR are universal — any other gate can be built from one of them.",
                "لاجک گیٹ ایک الیکٹرانک سرکٹ ہے جس کا ایک آؤٹ پٹ ہوتا ہے۔ نینڈ اور نار یونیورسل ہیں — ان سے کوئی بھی گیٹ بن سکتا ہے۔",
                "Boolean algebra uses only TRUE (1) and FALSE (0). A Boolean expression combines variables with AND, OR and NOT. Logic gates are the electronic circuits that perform those operations.\n\nAND (dot): Y = A · B — output 1 only if ALL inputs are 1. Real life: a car starts only if the key is in AND the start button is pressed.\nOR (plus): Y = A + B — 1 if ANY input is 1. A room with two doors.\nNOT (prime/bar): Y = A' — inverts. A fridge light is ON when the door is open.\nNAND = (A · B)' — 0 only if ALL are 1.\nNOR = (A + B)' — 1 only if ALL are 0.\nXOR = A ⊕ B — 1 if inputs DIFFER. Two-way light switch.\nXNOR = (A ⊕ B)' — 1 if inputs are the SAME.\n\nMemory trick: XOR = exclusively different; XNOR = same. Study the seven-gate figure and the combined truth table in the booklet.",
                "بولین الجبرا صرف درست (1) اور غلط (0) استعمال کرتا ہے۔ اظہار متغیرات کو AND، OR، NOT سے جوڑتا ہے۔ لاجک گیٹس وہ سرکٹس ہیں جو یہ عمل کرتے ہیں۔\n\nAND: تمام ان پٹ 1 ہوں تو ہی آؤٹ پٹ 1۔ OR: کوئی ایک 1 ہو۔ NOT: الٹ دیتا ہے۔ NAND اور NOR یونیورسل گیٹس ہیں۔ XOR مختلف پر 1؛ XNOR یکساں پر 1۔ کتابچے کی سات گیٹس والی شکل اور مشترکہ سچائی جدول رٹیں نہیں — سمجھیں۔",
                "Class, saat logic gates exam ka favourite sawal hai. AND tabhi 1 deta hai jab ALL inputs 1 hon — do talon wala darwaza. OR kisi ek 1 par 1 deta hai — do darwazon wala kamra. NOT invert karta hai — fridge ki light. NAND AND ka ulta hai, NOR OR ka ulta. XOR exclusively different: 1,1 par XOR 0 deta hai. XNOR same par 1. Universal gates NAND aur NOR hain — in se koi bhi doosra gate ban sakta hai. Yeh common mistake hai ke log unhe sirf opposite samajhte hain. Booklet ke figure 1.2 mein har gate ka symbol, expression aur rule hai. Truth table ke 4 rows yaad karo: 00, 01, 10, 11.",
                "Cover the booklet labels and redraw all seven gate symbols. Then fill the 2-input truth table from memory.",
                "لیبل چھپا کر ساتوں گیٹ کے علامات بنائیں۔ پھر دو ان پٹ سچائی جدول یاد سے بھریں۔",
                listOf(
                    c("Which gate gives 1 only when all inputs are 1?", "کون سا گیٹ صرف تب 1 دیتا ہے جب تمام ان پٹ 1 ہوں؟", "AND.", "اینڈ۔"),
                    c("What does XOR give for A=1, B=1?", "XOR، A=1 اور B=1 پر کیا دیتا ہے؟", "0, because the inputs are the same.", "0، کیونکہ ان پٹ یکساں ہیں۔"),
                    c("Which two gates are universal?", "کون سے دو گیٹ یونیورسل ہیں؟", "NAND and NOR.", "نینڈ اور نار۔"),
                    c("How many rows does a 3-input truth table have?", "تین ان پٹ جدول میں کتنی قطاریں؟", "2³ = 8 rows.", "8 قطاریں۔")
                ),
                listOf("Name all seven gates", "Fill a 2-input truth table", "Give a real-life example for AND, OR, XOR"),
                listOf("سات گیٹ نام لے سکتا/سکتی ہوں", "دو ان پٹ جدول بھر سکتا/سکتی ہوں", "AND، OR، XOR کی روزمرہ مثال دے سکتا/سکتی ہوں"),
                "diagrams/logic_gates.png",
                listOf("booklet/v1_p09.jpg", "booklet/v1_p10.jpg", "booklet/v1_p11.jpg")
            ),
            lesson(
                "1.1c", "u1", "1.1c",
                "Expressions, truth tables and logic diagrams", "ایکسپریشنز، سچائی جدول اور لاجک ڈایاگرام",
                "Expressions, truth tables aur logic diagrams",
                "4 periods (shared 1.1)", "Textbook pp. 13–16",
                listOf(w("expression", "اظہار"), w("precedence", "ترجیح"), w("minterm", "من ٹرم"), w("SOP", "ایس او پی"), w("logic diagram", "لاجک ڈایاگرام")),
                "Order of operations: parentheses, then NOT, then AND, then OR. SOP is the OR of minterms (rows where Y=1).",
                "اعمال کی ترتیب: پہلے قوسین، پھر ناٹ، پھر اینڈ، پھر اور۔ ایس او پی ان من ٹرمز کا اور ہے جہاں Y=1۔",
                "A logic expression uses variables, operators (AND ·, OR +, NOT ') and parentheses. To build a truth table: list the 2ⁿ input rows in binary order, add a column for each part of the expression, then compute the final output.\n\nPrecedence: 1 parentheses, 2 NOT, 3 AND, 4 OR. Example Y = A · B + C — AND happens before OR.\n\nFrom a truth table: each row where Y=1 is a minterm (SOP). Each row where Y=0 is a maxterm (POS). Worked booklet result: outputs 0,1,0,1 give Y = A'B + AB.\n\nTo draw a circuit: innermost brackets first (an OR for A+B), then NOT on C, then AND them together.",
                "الجک اظہار متغیرات، آپریٹرز اور قوسین سے بنتا ہے۔ سچائی جدول: 2ⁿ قطاریں بائنری ترتیب میں، ہر حصے کا کالم، پھر آخری Y۔ ترجیح: قوسین، ناٹ، اینڈ، اور۔ سچائی جدول سے ایس او پی ان قطاروں سے بنتی ہے جہاں آؤٹ پٹ 1 ہو۔",
                "Yaad rakhna precedence: pehle brackets, phir NOT, phir AND, phir OR. Jaise maths mein BODMAS. Y = A dot B plus C mein pehle A AND B, phir usme C OR. Truth table banate waqt binary order: 000, 001, 010... SOP matlab Sum of Products — jahan Y 1 hai un rows ke minterms ko OR karo. Circuit draw karte waqt andar wala gate pehle. Booklet ke logic diagram mein A aur B OR gate mein jate hain, C NOT se hota hai, phir dono AND se Y banate hain.",
                "For Y = (A + B) · C' draw the circuit, then complete the 8-row truth table.",
                "Y = (A + B) · C' کا سرکٹ بنائیں اور 8 قطاریں بھریں۔",
                listOf(
                    c("State the order of operations.", "اعمال کی ترتیب بتائیں۔", "Parentheses, NOT, AND, OR.", "قوسین، ناٹ، اینڈ، اور۔"),
                    c("What is a minterm used for?", "من ٹرم کس لیے؟", "To build SOP from rows where the output is 1.", "جہاں آؤٹ پٹ 1 ہو ان قطاروں سے ایس او پی بنانے کے لیے۔"),
                    c("How many rows for 3 inputs?", "تین ان پٹ پر کتنی قطاریں؟", "8.", "8۔")
                ),
                listOf("Apply precedence", "Build a truth table from an expression", "Draw a simple logic diagram"),
                listOf("ترجیح لگا سکتا/سکتی ہوں", "اظہار سے جدول بنا سکتا/سکتی ہوں", "سادہ لاجک ڈایاگرام کھینچ سکتا/سکتی ہوں"),
                "diagrams/logic_circuit.png",
                listOf("booklet/v1_p11.jpg", "booklet/v1_p12.jpg")
            ),
            lesson(
                "1.1d", "u1", "1.1d",
                "Karnaugh maps and LogiSim", "کارنو میپ اور لاجی سم",
                "Karnaugh maps aur LogiSim",
                "4 periods (shared 1.1)", "Textbook pp. 17–",
                listOf(w("Karnaugh map", "کارنو میپ"), w("grouping", "گروپ بندی"), w("simplification", "سادہ کرنا"), w("LogiSim", "لاجی سم")),
                "A K-map groups 1s in powers of 2 so the Boolean expression becomes shorter. Then prove it in LogiSim.",
                "کارنو میپ 1 کو 2 کی طاقتوں کے گروپوں میں جوڑتا ہے تاکہ اظہار چھوٹا ہو۔ پھر لاجی سم میں ثابت کریں۔",
                "A Karnaugh map is a grid version of a truth table. Adjacent 1s that form a rectangle of size 2, 4 or 8 can be circled; variables that change inside the group are dropped. Largest groups first; groups may wrap around the edges.\n\nLogiSim lab loop: place inputs, drop gates, wire the expression, add output Y, toggle every input combination, tick the paper truth table. The booklet asks you to verify Y = A · B + C against every row.",
                "کارنو میپ سچائی جدول کی گرڈ شکل ہے۔ ملحقہ 1 جو 2، 4 یا 8 کے مستطیل بناتے ہیں گھیرا جاتا ہے؛ گروپ کے اندر بدلنے والے متغیرات ہٹا دیے جاتے ہیں۔ لاجی سم میں گیٹس رکھیں، تار جوڑیں، ہر ان پٹ قطار چلائیں۔",
                "K-map se darna nahi. Yeh truth table ka naya layout hai. 1s ko 2, 4, 8 ke groups mein circle karo — sab se bara group pehle. Jo variable group ke andar change ho, usko expression se hata do. Phir wahi circuit LogiSim mein banao. Har input combo toggle karke paper par tick. Practical assessment yahi hai: expression do, circuit banao, saari rows dikhao.",
                "Simplify a 2-variable map that has 1s in cells 01, 10 and 11. Then build it in LogiSim.",
                "اس دو متغیر میپ کو سادہ کریں جس میں 01، 10، 11 پر 1 ہوں۔ پھر لاجی سم میں بنائیں۔",
                listOf(
                    c("Why group in powers of 2?", "2 کی طاقتوں میں کیوں گروپ؟", "Only those sizes correspond to dropped variables and a valid product term.", "وہی سائز درست پراڈکٹ ٹرم دیتے ہیں۔"),
                    c("What does LogiSim prove?", "لاجی سم کیا ثابت کرتا ہے؟", "That every truth-table row matches the wired circuit.", "کہ ہر قطار تار والے سرکٹ سے ملتی ہے۔")
                ),
                listOf("Group 1s on a small K-map", "Name the LogiSim lab steps"),
                listOf("چھوٹے کے میپ پر 1 گروپ کر سکتا/سکتی ہوں", "لاجی سم کے قدم بتا سکتا/سکتی ہوں"),
                "diagrams/kmap_logisim.png",
                listOf("booklet/v1_p13.jpg", "booklet/v1_p14.jpg")
            ),
            lesson(
                "1.2a", "u1", "1.2a",
                "SDLC and its six phases", "ایس ڈی ایل سی اور اس کے چھ مراحل",
                "S D L C aur uske chhe phases",
                "3 periods (shared 1.2)", "Textbook pp. 32–36",
                listOf(w("SDLC", "سافٹ ویئر ڈیولپمنٹ لائف سائیکل"), w("SRS", "ایس آر ایس"), w("deliverable", "حاصل"), w("bug", "خرابی"), w("deployment", "تعیناتی")),
                "SDLC is the structured process for building software: clear goals, better planning, quality, early risk reduction.",
                "ایس ڈی ایل سی سافٹ ویئر بنانے کا منظم انداز ہے: واضح اہداف، بہتر منصوبہ، معیار، ابتدائی خطرے میں کمی۔",
                "Software development means planning what the software must do, designing it, writing code, testing it, releasing it to users and fixing problems afterwards.\n\nThe six phases (booklet Figure 1.5):\n1 Requirement analysis — gather needs, check feasibility; deliverable SRS.\n2 System design — high-level and low-level design, database and screen design; tools include flowchart, UML, ER, wireframes; deliverable design document.\n3 Implementation (coding) — write code (Python, Java, C++), follow standards, use Git, comment the code; deliverable working software.\n4 Testing — find bugs; deliverable test reports.\n5 Deployment — go live; deliverable live software.\n6 Maintenance — updates and patches.\nFeedback: bugs and new requests start the next cycle.",
                "سافٹ ویئر ڈیولپمنٹ کا مطلب ہے منصوبہ، ڈیزائن، کوڈ، جانچ، صارفین کو دینا اور بعد میں درستی۔ چھ مراحل: تقاضوں کا تجزیہ (ایس آر ایس)، نظام کا ڈیزائن، کوڈنگ، جانچ، تعیناتی، دیکھ بھال۔ فیڈ بیک اگلا چکر شروع کرتی ہے۔",
                "S D L C yaad rakhne ka tarika: Require, Design, Code, Test, Deploy, Maintain. Phase 1 ka deliverable S R S hai — Software Requirements Specification. Phase 2 mein flowchart, U M L, E R, wireframes. Phase 3 coding plus Git. Testing se pehle deploy mat karna — yeh Waterfall ki kamzori bhi hai. Maintenance matlab patches aur naye requests. Feedback loop: bugs agle cycle ko start karte hain.",
                "For a school attendance app, write one sentence and one deliverable for each of the six phases.",
                "اسکول حاضری ایپ کے لیے چھوں مراحل کا ایک جملہ اور ایک حاصل لکھیں۔",
                listOf(
                    c("Name the six SDLC phases in order.", "چھ مراحل ترتیب سے نام لیں۔",
                        "Requirement analysis, system design, implementation, testing, deployment, maintenance.",
                        "تقاضے، ڈیزائن، نفاذ، جانچ، تعیناتی، دیکھ بھال۔"),
                    c("What is the deliverable of phase 1?", "پہلے مرحلے کا حاصل کیا ہے؟", "SRS — Software Requirements Specification.", "ایس آر ایس۔")
                ),
                listOf("List six phases with deliverables", "Explain why SDLC reduces risk"),
                listOf("چھ مراحل حاصل سمیت بتا سکتا/سکتی ہوں", "ایس ڈی ایل سی کا فائدہ سمجھا سکتا/سکتی ہوں"),
                "diagrams/sdlc.png",
                listOf("booklet/v1_p15.jpg", "booklet/v1_p16.jpg")
            ),
            lesson(
                "1.2b", "u1", "1.2b",
                "Waterfall and Agile with case studies", "واٹر فال اور ایجائیل مع کیس اسٹڈیز",
                "Waterfall aur Agile, case studies ke sath",
                "3 periods (shared 1.2)", "Textbook pp. 36–",
                listOf(w("Waterfall", "واٹر فال"), w("Agile", "ایجائیل"), w("sprint", "سپرنٹ"), w("case study", "کیس اسٹڈی")),
                "Waterfall fits fixed, clear requirements (Al-Noor library). Agile fits changing needs, using 2–4 week sprints.",
                "واٹر فال مقرر اور واضح ضرورتوں کے لیے (النور لائبریری)۔ ایجائیل بدلتی ضرورتوں کے لیے، 2 تا 4 ہفتے کے سپرنٹ۔",
                "Waterfall is a one-way cascade: each phase finishes before the next starts. Testing comes late, so change is expensive. The Al-Noor library system chose Waterfall because requirements were clear, fixed and unlikely to change.\n\nAgile delivers working software in short cycles called sprints (typically 2–4 weeks). It is iterative and documented — not a free-for-all. Capacity used = estimated effort / available days × 100%. Example: 6 + 3 over 10 days = 90%.\n\nExam trap: students assume Agile means no planning. Correct it.",
                "واٹر فال ایک طرفہ آبشار ہے؛ جانچ دیر سے آتی ہے۔ ایجائیل مختصر سپرنٹ میں کام کرتا سافٹ ویئر دیتا ہے۔ یہ بے منصوبہ نہیں۔ صلاحیت = اندازہ / دستیاب دن × 100۔",
                "Do models ratne ki nahi, case se choose karo. Al-Noor library: requirements clear aur fixed — Waterfall. School app jahan features roz badlein — Agile. Sprint 2 se 4 weeks ka chhota cycle hai jo working software par khatam hota hai. Capacity formula booklet mein hai. Common mistake: Agile ka matlab no documentation. Galat. Agile iterative hai, undocumented nahi.",
                "For a school-hall seating app, pick Waterfall or Agile and justify in four lines.",
                "اسکول ہال سیٹنگ ایپ کے لیے واٹر فال یا ایجائیل چنیں اور چار سطروں میں وجہ لکھیں۔",
                listOf(
                    c("Why was Waterfall chosen for Al-Noor library?", "النور لائبریری کے لیے واٹر فال کیوں؟",
                        "Requirements were clear, fixed and unlikely to change.", "ضروریات واضح، مقرر اور تبدیل ہونے والی نہیں تھیں۔"),
                    c("What is a sprint, and how long is it?", "سپرنٹ کیا ہے اور کتنا لمبا؟",
                        "A short development cycle ending with working software; 2–4 weeks.", "کام کرتا سافٹ ویئر والا مختصر دور؛ 2 تا 4 ہفتے۔"),
                    c("A sprint has 10 working days and plans 7 days of work. Capacity used?", "10 دن، 7 دن کام۔ صلاحیت؟", "7/10 × 100% = 70%.", "70 فیصد۔")
                ),
                listOf("Compare Waterfall and Agile", "Compute sprint capacity", "Choose a model for a given case"),
                listOf("واٹر فال اور ایجائیل موازنہ کر سکتا/سکتی ہوں", "سپرنٹ صلاحیت نکال سکتا/سکتی ہوں", "کیس کے لیے ماڈل چن سکتا/سکتی ہوں"),
                "diagrams/waterfall_agile.png",
                listOf("booklet/v1_p17.jpg", "booklet/v1_p18.jpg", "booklet/v1_p19.jpg")
            ),
            lesson(
                "1.3a", "u1", "1.3a",
                "Communication models and the OSI model", "کمیونیکیشن ماڈلز اور او ایس آئی ماڈل",
                "Communication models aur O S I model",
                "3 periods (shared 1.3)", "Textbook pp. 55–62",
                listOf(w("communication model", "کمیونیکیشن ماڈل"), w("layer", "تہہ"), w("protocol", "پروٹوکول"), w("OSI", "او ایس آئی"), w("router", "راؤٹر")),
                "OSI splits a hard job into seven layers so engineers can improve one layer without breaking the others.",
                "او ایس آئی مشکل کام کو سات تہوں میں بانٹتا ہے تاکہ ایک تہہ بدلنے سے باقی نہ ٹوٹیں۔",
                "A communication model is a set of rules that explains how data travels from one device to another. Sending data is like posting a letter: address, envelope, van, sorting office.\n\nOSI (Open Systems Interconnection) was developed by ISO in 1984. Seven layers, top to bottom:\n7 Application — HTTP, SMTP, FTP (what the user sees)\n6 Presentation — encryption, JPEG\n5 Session — start and manage the conversation\n4 Transport — TCP, UDP (ports and reliability)\n3 Network — IP, routers (routing)\n2 Data Link — MAC, switches (frames)\n1 Physical — cables and bits\n\nMnemonic: Please Do Not Throw Sausage Pizza Away.\nHTTP = secure? HTTPS is HTTP plus TLS. SMTP sends outgoing email. Both live at the Application layer. Ping uses ICMP at the Network layer.",
                "کمیونیکیشن ماڈل بتاتا ہے ڈیٹا کیسے سفر کرتا ہے۔ او ایس آئی آئی ایس او نے 1984 میں دیا۔ سات تہیں: ایپلیکیشن، پریزنٹیشن، سیشن، ٹرانسپورٹ، نیٹ ورک، ڈیٹا لنک، فزیکل۔ یاد رکھنے کی ترکیب: Please Do Not Throw Sausage Pizza Away۔",
                "O S I ke 7 layers ratne ka jumla: Please Do Not Throw Sausage Pizza Away — Physical, Data Link, Network, Transport, Session, Presentation, Application. Neeche se gino 1 se 7. Routing Network layer 3 karta hai, M A C address Data Link layer 2. H T T P S encrypted web pages, S M T P outgoing email — dono Application layer. Ping Network layer ka demo hai. ISO ne 1984 mein yeh model diya.",
                "Draw the seven layers with the mnemonic, then ping www.google.com and note whether the reply arrives.",
                "سات تہیں ترکیب سمیت بنائیں، پھر پنگ چلا کر جواب نوٹ کریں۔",
                listOf(
                    c("Who developed OSI, and when?", "او ایس آئی کس نے، کب؟", "ISO, 1984.", "آئی ایس او، 1984۔"),
                    c("Give the mnemonic for layers 1 to 7.", "1 تا 7 کی ترکیب؟",
                        "Please Do Not Throw Sausage Pizza Away.", "Please Do Not Throw Sausage Pizza Away۔"),
                    c("Which layer routes, which uses MAC?", "راؤٹنگ اور میک کون سی تہہ؟",
                        "Network (3) routes; Data Link (2) uses MAC.", "نیٹ ورک راؤٹ؛ ڈیٹا لنک میک۔"),
                    c("What do HTTPS and SMTP do?", "ایچ ٹی ٹی پی ایس اور ایس ایم ٹی پی؟",
                        "HTTPS: secure web pages (TLS). SMTP: outgoing email. Both Application-layer.",
                        "ایچ ٹی ٹی پی ایس محفوظ صفحات؛ ایس ایم ٹی پی ای میل۔ دونوں ایپلیکیشن۔")
                ),
                listOf("List 7 OSI layers with a protocol", "Explain why layering helps"),
                listOf("سات تہیں پروٹوکول سمیت بتا سکتا/سکتی ہوں", "تہہ داری کا فائدہ سمجھا سکتا/سکتی ہوں"),
                "diagrams/osi.png",
                listOf("booklet/v1_p19.jpg", "booklet/v1_p20.jpg", "booklet/v1_p21.jpg")
            ),
            lesson(
                "1.3b", "u1", "1.3b",
                "TCP/IP, encapsulation and comparison", "ٹی سی پی/آئی پی، انکیپسولیشن اور موازنہ",
                "T C P I P, encapsulation aur comparison",
                "3 periods (shared 1.3)", "Textbook pp. 63–66",
                listOf(w("encapsulation", "انکیپسولیشن"), w("header", "ہیڈر"), w("segment", "سیگمنٹ"), w("packet", "پیکٹ"), w("frame", "فریم")),
                "Going down the stack each layer adds a header (encapsulation). Coming up, headers are removed (decapsulation).",
                "نیچے جاتے ہوئے ہر تہہ ہیڈر جوڑتی ہے (انکیپسولیشن)۔ اوپر آتے ہوئے ہیڈر ہٹتے ہیں (ڈیکیپسولیشن)۔",
                "When you send data it goes down the layers of your device and every layer adds a header — encapsulation. At the receiver the data goes up and every layer reads and removes its header — decapsulation.\n\nLayer 5–7 handle data; layer 4 makes segments (TCP/UDP header with port numbers); layer 3 makes packets (IP header); layer 2 makes frames (MAC header and trailer); layer 1 sends bits.\n\nTCP/IP has four layers that map onto OSI: Application ↔ OSI 5–7, Transport ↔ 4, Internet ↔ 3, Network Access ↔ 1–2. TCP/IP is what the real internet uses; OSI is the teaching model.",
                "بھیجتے وقت ہر تہہ ہیڈر جوڑتی ہے — انکیپسولیشن۔ وصول کرتے وقت ہیڈر ہٹتے ہیں — ڈیکیپسولیشن۔ ڈیٹا سے سیگمنٹ، پیکٹ، فریم، پھر بٹس۔ ٹی سی پی/آئی پی چار تہوں والا عملی ماڈل ہے جو او ایس آئی سے نقشہ کھاتا ہے۔",
                "Encapsulation ko letter se samjho: aap likhte ho (data), envelope (header), van (frame), wire (bits). Receiver ulta karta hai — decapsulation. Naam yaad: segment Transport, packet Network/Internet, frame Data Link. T C P I P 4 layers: Application, Transport, Internet, Network Access. Exam mein comparison table aata hai — OSI teaching model, TCP/IP real internet.",
                "Draw the encapsulation stack from Data down to Bits and label TCP/IP versus OSI.",
                "ڈیٹا سے بٹس تک انکیپسولیشن کا خاکہ بنائیں اور دونوں ماڈل لیبل کریں۔",
                listOf(
                    c("What is added at each layer going down?", "نیچے جاتے ہوئے کیا جڑتا ہے؟", "A header (and at Data Link a trailer too).", "ہیڈر (ڈیٹا لنک پر ٹریلر بھی)۔"),
                    c("Map TCP/IP Application to OSI.", "ایپلیکیشن کس او ایس آئی تہوں سے؟", "OSI layers 5, 6 and 7.", "او ایس آئی 5، 6، 7۔")
                ),
                listOf("Describe encapsulation", "Compare TCP/IP with OSI"),
                listOf("انکیپسولیشن بیان کر سکتا/سکتی ہوں", "ٹی سی پی/آئی پی اور او ایس آئی موازنہ کر سکتا/سکتی ہوں"),
                "diagrams/tcpip_encap.png",
                listOf("booklet/v1_p21.jpg", "booklet/v1_p22.jpg")
            ),
            lesson(
                "1.R", "u1", "1.R",
                "Unit 1 revision and mock test", "یونٹ 1 اعادہ اور ماک ٹیسٹ",
                "Unit 1 revision aur mock test",
                "1 period", "Booklet p. 23",
                listOf(w("revision", "اعادہ"), w("mock test", "ماک ٹیسٹ")),
                "Close the booklet and say the seven gates, six SDLC phases and seven OSI layers out loud in Urdish.",
                "کتابچہ بند کر کے سات گیٹ، چھ ایس ڈی ایل سی مراحل اور سات او ایس آئی تہیں اُردش میں زبانی کہیں۔",
                "Flashcards: analog vs digital; bit vs byte; AND/OR/NOT/NAND/NOR/XOR/XNOR; precedence; SDLC deliverables; Waterfall vs Agile; OSI mnemonic; encapsulation names.\nThen take the Unit 1 mock test in this app (20 marks style).",
                "فلیش کارڈز کے بعد ایپ میں یونٹ 1 کا ماک ٹیسٹ حل کریں۔",
                "Revision coach: pehle analog digital farq, phir saat gates ke rules, phir S D L C ke chhe naam, phir Waterfall versus Agile, phir Please Do Not Throw Sausage Pizza Away, phir encapsulation. Jab yeh zabani nikal aaye to mock test kholo. Green answers pehle mat dekho.",
                "Score the mock test with the marking scheme, then reopen any lesson that dropped marks.",
                "ماک ٹیسٹ نمبر دے کر کمزور سبق دوبارہ کھولیں۔",
                listOf(c("Ready for the mock?", "ماک کے لیے تیار؟", "Open Unit 1 quiz from the home or unit screen.", "ہوم یا یونٹ سے کوئز کھولیں۔")),
                listOf("Recall every Unit 1 diagram from memory"),
                listOf("یونٹ 1 کا ہر خاکہ یاد سے بنا سکتا/سکتی ہوں"),
                "diagrams/osi.png",
                listOf("booklet/v1_p20.jpg", "booklet/v1_p15.jpg", "booklet/v1_p10.jpg"),
                isRevision = true
            )
        )
    )

    private fun unit2(): CourseUnit = CourseUnit(
        id = "u2", number = 2,
        titleEn = "Computational Thinking and Algorithms",
        titleUr = "کمپیوٹیشنل تھنکنگ اور الگورتھمز",
        titleUrdish = "Computational thinking aur algorithms",
        weeks = "3 weeks · 9–10 periods",
        colorHex = "#0F766E",
        coverDiagram = "diagrams/sorting.png",
        summaryEn = "CT pillars, algorithms, bubble and selection sort, linear and binary search, evaluation.",
        summaryUr = "تھنکنگ کے ستون، الگورتھم، ببل اور سلیکشن سارٹ، لکیری اور بائنری تلاش، جانچ۔",
        lessons = listOf(
            lesson(
                "2.1", "u2", "2.1",
                "Computational thinking, algorithms and pseudocode", "کمپیوٹیشنل تھنکنگ، الگورتھم اور سیوڈو کوڈ",
                "Computational thinking, algorithms aur pseudocode",
                "shared 2.1–2.3", "Textbook pp. 71–",
                listOf(w("algorithm", "الگورتھم"), w("pseudocode", "سیوڈو کوڈ"), w("computational thinking", "کمپیوٹیشنل تھنکنگ")),
                "An algorithm is a finite, definite, effective sequence of steps with input and output. Write it in pseudocode first.",
                "الگورتھم محدود، واضح، موثر قدم ہیں جن کا ان پٹ اور آؤٹ پٹ ہو۔ پہلے سیوڈو کوڈ میں لکھیں۔",
                "Computational thinking is the habit of turning a messy human problem into steps a computer can follow. An algorithm must be finite (it stops), definite (no fuzzy steps), effective (each step is doable), and it must have input and output.\n\nPseudocode is English-like steps: FOR, WHILE, IF, THEN. It is not Python yet — that comes in Unit 3. Everyday example: making tea is an algorithm if every step is testable.",
                "کمپیوٹیشنل تھنکنگ گندہ انسانی مسئلہ کمپیوٹر کے قدموں میں بدلنے کی عادت ہے۔ الگورتھم محدود، واضح، موثر ہو اور ان پٹ آؤٹ پٹ رکھے۔ سیوڈو کوڈ انگریزی جیسے قدم ہیں۔",
                "Algorithm ki definition exam mein verbatim aati hai: finite, definite, effective, input, output. Pehle dimagh mein steps, phir pseudocode, phir code. Chai banana algorithm tab hai jab har step testable ho. Computational thinking sirf coding nahi — sochne ka tareeqa hai.",
                "Write pseudocode for 'find the largest of three numbers'.",
                "تین عدد میں سب سے بڑا تلاش کرنے کا سیوڈو کوڈ لکھیں۔",
                listOf(
                    c("Name four properties of a good algorithm.", "اچھے الگورتھم کی چار خصوصیات؟",
                        "Finite, definite, effective, input/output.", "محدود، واضح، موثر، ان پٹ/آؤٹ پٹ۔")
                ),
                listOf("Define an algorithm", "Write short pseudocode"),
                listOf("الگورتھم کی تعریف کر سکتا/سکتی ہوں", "مختصر سیوڈو کوڈ لکھ سکتا/سکتی ہوں"),
                "diagrams/computational_thinking.png",
                listOf("booklet/v1_p29.jpg", "booklet/v1_p30.jpg")
            ),
            lesson(
                "2.3", "u2", "2.3",
                "Decomposition, pattern recognition, abstraction", "مسئلہ کی تقسیم، نمونوں کی پہچان، تجرید",
                "Decomposition, pattern recognition, abstraction",
                "shared 2.1–2.3", "Textbook pp. 71–",
                listOf(w("decomposition", "تقسیم"), w("pattern recognition", "نمونہ پہچان"), w("abstraction", "تجرید")),
                "Split the problem, spot what repeats, hide the noise, then write the algorithm.",
                "مسئلہ توڑو، تکرار دیکھو، شور چھپاو، پھر الگورتھم لکھو۔",
                "Decomposition: a library system is not one problem — it is membership, catalogue, borrow, return, fine.\nPattern recognition: every borrow record has a date and a due date; late returns share a pattern.\nAbstraction: the exam does not need the colour of the library desk — keep MemberID and due date, drop decoration.\nTogether these three plus 'algorithm' are the four CT strategies.",
                "تقسیم: بڑا مسئلہ چھوٹے حصوں میں۔ نمونہ: جو بار بار آئے۔ تجرید: غیر ضروری ہٹا کر اصل بات رکھو۔ یہ چاروں ملا کر کمپیوٹیشنل تھنکنگ ہے۔",
                "Char strategies: Decomposition todna, Pattern pehchanna, Abstraction chhupana, Algorithm likhna. Library case: membership alag, borrow alag. Pattern: late return hamesha fine. Abstraction: desk ka colour nahi, Member I D chahiye. Long question 4-ii abstraction kyun zaroori — kyunke computer ko sirf relevant data chahiye.",
                "Decompose 'plan a school sports day' into at least five sub-problems and circle one repeating pattern.",
                "سکول سپورٹس ڈے کو کم از کم پانچ ذیلی مسائل میں توڑیں اور ایک تکرار کا نشان لگائیں۔",
                listOf(
                    c("Define decomposition and abstraction.", "تقسیم اور تجرید کی تعریف۔",
                        "Decomposition splits a problem; abstraction keeps relevant detail and hides the rest.",
                        "تقسیم مسئلہ توڑتی ہے؛ تجرید اصل بات رکھتی اور باقی چھپاتی ہے۔")
                ),
                listOf("Apply the four CT strategies to a school problem"),
                listOf("اسکول کے مسئلے پر چاروں حکمت عملیاں لگا سکتا/سکتی ہوں"),
                "diagrams/computational_thinking.png",
                listOf("booklet/v1_p30.jpg", "booklet/v1_p31.jpg")
            ),
            lesson(
                "2.4a", "u2", "2.4a",
                "Sorting: Bubble and Selection", "ترتیب: ببل اور سلیکشن",
                "Sorting: Bubble aur Selection",
                "shared", "Textbook pp. 76–80",
                listOf(w("sorting", "ترتیب"), w("ascending", "صعودی"), w("swap", "ادلا بدلی"), w("pass", "پاس")),
                "Bubble repeatedly swaps neighbours that are in the wrong order. Selection repeatedly brings the smallest remaining item to the front.",
                "ببل غلط ترتیب والے پڑوسیوں کا ادلا بدلی کرتا ہے۔ سلیکشن باقی سب سے چھوٹا آگے لاتا ہے۔",
                "Sorting arranges data ascending (lowest to highest) or descending. The textbook traces 8, 4, 1, 9, 3 ending as 1, 3, 4, 8, 9.\n\nBubble: compare DATA[P] with DATA[P+1]; swap if left is larger; the largest item 'bubbles' to the end each pass.\nSelection: for K = 1 to N-1 find the smallest remaining item and swap it into position K. Green cells in the booklet are already in the final place.\n\nBoth are easy to trace on paper — that is why the exam loves them.",
                "ترتیب صعودی یا نزولی۔ ببل پڑوسیوں کا موازنہ۔ سلیکشن ایک وقت میں ایک مقام درست کرتا ہے۔ کتابچہ 8،4،1،9،3 کا ٹریس دکھاتی ہے۔",
                "Dono algorithms booklet ke figure 2.2 par trace karo. Bubble: neighbours galat hon to swap, sab se bara end par bubble hota hai. Selection: har pass mein remaining ka smallest nikaal ke us index par rakh do. Pseudocode black boxes yaad karo. Idea yaad: bubble compare neighbours; selection fix one position.",
                "Trace both algorithms on 5, 2, 8, 1. Write the list after every pass.",
                "5، 2، 8، 1 پر دونوں الگورتھم ٹریس کریں۔ ہر پاس کے بعد فہرست لکھیں۔",
                listOf(
                    c("What 'bubbles' to the end in Bubble sort?", "ببل میں آخر تک کیا جاتا ہے؟", "The largest remaining item.", "باقی سب سے بڑی چیز۔"),
                    c("What does Selection fix each pass?", "سلیکشن ہر پاس کیا ٹھیک کرتا ہے؟", "One more position, filled with the smallest remaining item.", "ایک اور مقام، باقی سب سے چھوٹی چیز سے۔")
                ),
                listOf("Trace Bubble sort", "Trace Selection sort", "Write both in pseudocode"),
                listOf("ببل ٹریس کر سکتا/سکتی ہوں", "سلیکشن ٹریس کر سکتا/سکتی ہوں", "دونوں کا سیوڈو کوڈ لکھ سکتا/سکتی ہوں"),
                "diagrams/sorting.png",
                listOf("booklet/v1_p32.jpg", "booklet/v1_p33.jpg")
            ),
            lesson(
                "2.4b", "u2", "2.4b",
                "Searching: Linear and Binary", "تلاش: لکیری اور بائنری",
                "Searching: Linear aur Binary",
                "shared", "Textbook pp. 80–",
                listOf(w("linear search", "لکیری تلاش"), w("binary search", "بائنری تلاش"), w("sorted", "ترتیب شدہ")),
                "Linear works on any list. Binary is faster but the list MUST be sorted.",
                "لکیری کسی بھی فہرست پر چلتی ہے۔ بائنری تیز ہے مگر فہرست ترتیب شدہ ہونی چاہیے۔",
                "Linear search checks items one by one from the start until it finds the target or runs out. Worst case: n comparisons.\nBinary search sets low and high, looks at mid = (low+high)//2, then throws away half the list. Worst case about log₂ n. If the list is unsorted, binary search is wrong — sort first or use linear.",
                "لکیری ایک ایک کر کے دیکھتی ہے۔ بائنری درمیان سے آدھی فہرست پھینکتی ہے — صرف ترتیب شدہ فہرست پر۔",
                "Favourite exam trap: binary search unsorted list par. Galat. Pehle sort, phir binary. Linear slow hai lekin hamesha legal. Target 9 list 3,8,1,9,4 mein linear 4 comparisons. Binary sorted 1,3,4,8,9 par mid se kaatti hai. Formula mid = (low plus high) divide 2.",
                "Search for 8 in 1,3,4,8,9 with both methods. Count comparisons.",
                "1،3،4،8،9 میں 8 دونوں طریقوں سے ڈھونڈیں اور موازنے گنیں۔",
                listOf(
                    c("When must you NOT use binary search?", "بائنری کب نہیں؟", "When the data is not sorted.", "جب ڈیٹا ترتیب شدہ نہ ہو۔"),
                    c("Give the mid formula.", "مڈ کا فارمولا؟", "mid = (low + high) // 2", "مڈ = (لو + ہائی) // 2")
                ),
                listOf("Trace linear search", "Trace binary search", "Choose the right search"),
                listOf("لکیری ٹریس کر سکتا/سکتی ہوں", "بائنری ٹریس کر سکتا/سکتی ہوں", "صحیح تلاش چن سکتا/سکتی ہوں"),
                "diagrams/searching.png",
                listOf("booklet/v1_p34.jpg", "booklet/v1_p35.jpg")
            ),
            lesson(
                "2.5", "u2", "2.5",
                "Evaluating and choosing an algorithm", "الگورتھم کی جانچ اور انتخاب",
                "Algorithm evaluate karke choose karna",
                "shared", "Textbook pp. 85–87",
                listOf(w("evaluation", "جانچ"), w("time", "وقت"), w("space", "جگہ"), w("correctness", "درستگی")),
                "Pick an algorithm for correctness first, then time, memory, and how easy it is to trace in the exam.",
                "پہلے درستگی، پھر وقت، میموری، اور امتحان میں ٹریس کی آسانی۔",
                "A correct slow algorithm beats a fast wrong one. For tiny classroom lists, Bubble and Selection are fine because you can show every swap. For a huge sorted phone book, binary search wins. Write a short justification: data size, sorted or not, what you must prove on paper.",
                "درست مگر سست، غلط تیز سے بہتر ہے۔ چھوٹی فہرست پر ببل/سلیکشن ٹریس آسان۔ بڑی ترتیب شدہ فہرست پر بائنری۔",
                "Evaluate means: kya yeh sahi jawab deti hai, kitni comparisons, kitni memory, kya main paper par dikha sakta hoon. School marks ki 30 values — bubble OK. Telephone directory — binary. Justification 3 lines mein likho, sirf naam mat likho.",
                "Choose a search for (a) 8 unsorted test scores (b) 10,000 sorted roll numbers. Justify.",
                "8 بغیر ترتیب نمبر اور 10،000 ترتیب شدہ رول کے لیے تلاش چنیں۔",
                listOf(
                    c("Name three things you evaluate.", "تین چیزیں جو جانچتے ہیں؟", "Correctness, time/comparisons, memory / ease of trace.", "درستگی، وقت، میموری/ٹریس۔")
                ),
                listOf("Justify an algorithm choice in three lines"),
                listOf("تین سطروں میں انتخاب کی وجہ لکھ سکتا/سکتی ہوں"),
                "diagrams/searching.png",
                listOf("booklet/v1_p36.jpg")
            ),
            lesson(
                "2.R", "u2", "2.R",
                "Unit 2 revision and mock test", "یونٹ 2 اعادہ اور ماک ٹیسٹ",
                "Unit 2 revision aur mock test",
                "1 period", "Booklet p. 37",
                emptyList(),
                "Trace one sort and one search without looking, then sit the mock.",
                "ایک سارٹ اور ایک سرچ بغیر دیکھے ٹریس کریں، پھر ماک۔",
                "Recite: four CT strategies; algorithm properties; bubble vs selection idea; linear vs binary condition; evaluation criteria.",
                "چار حکمت عملیاں، خصوصیات، ببل بمقابلہ سلیکشن، لکیری بمقابلہ بائنری، جانچ کے معیار۔",
                "Zabani: decomposition, pattern, abstraction, algorithm. Bubble neighbours, selection one slot. Binary only sorted. Phir Unit 2 quiz kholo.",
                "Take the Unit 2 mock test in the app.",
                "ایپ میں یونٹ 2 ماک ٹیسٹ حل کریں۔",
                listOf(c("Ready?", "تیار؟", "Open the Unit 2 quiz.", "یونٹ 2 کوئز کھولیں۔")),
                listOf("Trace both sorts and both searches from memory"),
                listOf("دونوں سارٹ اور دونوں سرچ یاد سے ٹریس کر سکتا/سکتی ہوں"),
                "diagrams/sorting.png",
                listOf("booklet/v1_p32.jpg", "booklet/v1_p34.jpg"),
                isRevision = true
            )
        )
    )

    private fun unit3(): CourseUnit = CourseUnit(
        id = "u3", number = 3,
        titleEn = "Programming Fundamentals",
        titleUr = "پروگرامنگ کے بنیادی اصول",
        titleUrdish = "Programming ke bunyadi usool — Python",
        weeks = "4 weeks · 12–14 periods",
        colorHex = "#7C3AED",
        coverDiagram = "diagrams/python_ide.png",
        summaryEn = "Python, VS Code, variables, operators, if/elif, for/while, libraries, debugging.",
        summaryUr = "پائتھن، وی ایس کوڈ، متغیرات، آپریٹرز، اگر/وگرنہ، لوپس، لائبریریز، ڈیبگنگ۔",
        lessons = listOf(
            lesson(
                "3.1", "u3", "3.1",
                "Programming, Python careers and VS Code", "پروگرامنگ، پائتھن کیریئر اور وی ایس کوڈ",
                "Programming, Python careers aur V S Code",
                "shared", "Textbook pp. 91–",
                listOf(w("programming", "پروگرامنگ"), w("IDE", "آئی ڈی ای"), w("VS Code", "وی ایس کوڈ"), w("Python", "پائتھن")),
                "Programming is giving a computer clear instructions. Python is used in data, web, AI and automation. VS Code is the class IDE.",
                "پروگرامنگ واضح ہدایات دینا ہے۔ پائتھن ڈیٹا، ویب، اے آئی میں۔ وی ایس کوڈ کلاس کا آئی ڈی ای ہے۔",
                "An IDE (Integrated Development Environment) combines editor, file explorer, terminal and run/debug. VS Code: open folder, new file hello.py, type print('Sindh CS XI'), Run.\nPython careers in Pakistan include data work, automation, web backends, and teaching. Syntax errors are spelling mistakes in code — the red underline is your friend.",
                "آئی ڈی ای ایڈیٹر، ایکسپلورر، ٹرمینل اور رن کو جوڑتا ہے۔ پہلا پروگرام print ہے۔ پائتھن کے کیریئر ڈیٹا، آٹومیشن، ویب، تدریس۔",
                "Programming matlab computer ko saaf steps dena. Python is liye choose hui ke syntax seedha hai aur careers hain: data, A I, web, automation. V S Code mein Explorer, Editor, Terminal, Run. Pehla program: print Hello. File save karna mat bhoolna, extension .py.",
                "In VS Code, save and run a file that prints your name and class.",
                "وی ایس کوڈ میں ایسی فائل چلائیں جو آپ کا نام اور جماعت چھاپے۔",
                listOf(
                    c("Name four parts of VS Code you use daily.", "وی ایس کوڈ کے چار حصے؟",
                        "Explorer, editor, terminal, Run/Debug.", "ایکسپلورر، ایڈیٹر، ٹرمینل، رن۔")
                ),
                listOf("Run a Python file in VS Code", "Give two Python career paths"),
                listOf("وی ایس کوڈ میں فائل چلا سکتا/سکتی ہوں", "دو پائتھن کیریئر بتا سکتا/سکتی ہوں"),
                "diagrams/python_ide.png",
                listOf("booklet/v1_p42.jpg", "booklet/v1_p43.jpg")
            ),
            lesson(
                "3.4a", "u3", "3.4a",
                "Variables, data types, input and output", "متغیرات، ڈیٹا ٹائپس، ان پٹ اور آؤٹ پٹ",
                "Variables, data types, input aur output",
                "shared", "Textbook pp. 104–",
                listOf(w("variable", "متغیر"), w("data type", "ڈیٹا ٹائپ"), w("input", "ان پٹ"), w("cast", "تبدیل")),
                "A variable is a named box. input() always returns a string — cast with int() or float() when you need a number.",
                "متغیر نام والا ڈبہ ہے۔ input() ہمیشہ سٹرنگ دیتا ہے — عدد کے لیے int() یا float()۔",
                "Types: str, int, float, bool. Rules: start with a letter or _; no spaces; case-sensitive; do not use keywords (if, for, class).\nname = input('Name: ')\nmarks = int(input('Marks: '))\nprint('Hello', name, 'you scored', marks)",
                "اقسام: سٹرنگ، انٹ، فلوٹ، بول۔ اصول: حرف یا _ سے شروع؛ خالی جگہ نہیں؛ کی ورڈ نہیں۔ input کو عدد بنانا ضروری ہے۔",
                "Variable named box hai. input hamesha string deta hai — yeh sab se common bug hai. '2' plus 2 TypeError. int input Marks colon. print comma se values jodta hai. Rules: letter ya underscore, no space, case-sensitive.",
                "Write a program that asks for two integers and prints their sum.",
                "دو عدد پوچھ کر مجموعہ چھاپنے کا پروگرام لکھیں۔",
                listOf(
                    c("Why does int(input()) appear so often?", "int(input()) کیوں؟",
                        "Because input() returns text and arithmetic needs a number.", "کیونکہ input متن دیتا ہے اور حساب کو عدد چاہیے۔")
                ),
                listOf("Declare typed variables", "Read input and print output"),
                listOf("متغیر بنا سکتا/سکتی ہوں", "ان پٹ لے کر آؤٹ پٹ دے سکتا/سکتی ہوں"),
                "diagrams/variables.png",
                listOf("booklet/v1_p44.jpg")
            ),
            lesson(
                "3.4b", "u3", "3.4b",
                "Operators and operands", "آپریٹرز اور اوپرینڈز",
                "Operators aur operands",
                "shared", "Textbook pp. 108–",
                listOf(w("operator", "آپریٹر"), w("operand", "اوپرینڈ"), w("modulo", "باقی"), w("floor division", "فرش تقسیم")),
                "The operator acts; the operand is acted on. // is floor division, % is remainder, ** is power.",
                "آپریٹر عمل کرتا ہے، اوپرینڈ پر عمل ہوتا ہے۔ // فرش تقسیم، % باقی، ** طاقت۔",
                "Arithmetic: + - * / // % **. Comparison: == != < > <= >= (result is bool). Logical: and or not. Assignment: = += -=. Membership: in, not in.\n7 // 2 = 3 and 7 % 2 = 1. 'A' in 'CAT' is True. True and False is False.",
                "حسابی، موازنہ، منطقی، تفویض، رکنیت۔ 7//2=3، 7%2=1۔",
                "Operator kaam karta hai, operand us par. Floor division 7 slash slash 2 = 3. Percent remainder. Double star power. Double equals comparison, single equals assignment — yeh mix-up exam mein marks katwata hai. and or not logical hain.",
                "Predict the values of 17 // 5, 17 % 5, 2 ** 5, and (3 > 1) and (2 == 2).",
                "17//5، 17%5، 2**5، اور (3>1) and (2==2) کی قدریں لکھیں۔",
                listOf(
                    c("Difference between = and == ?", "= اور == میں فرق؟", "= assigns; == compares.", "= تفویض؛ == موازنہ۔")
                ),
                listOf("Classify an operator", "Evaluate a mixed expression"),
                listOf("آپریٹر کی قسم بتا سکتا/سکتی ہوں", "ملے جلے اظہار کی قدر نکال سکتا/سکتی ہوں"),
                "diagrams/operators.png",
                listOf("booklet/v1_p45.jpg", "booklet/v1_p46.jpg")
            ),
            lesson(
                "3.5a", "u3", "3.5a",
                "Sequence and selection", "ترتیب اور انتخاب",
                "Sequence aur selection — if elif else",
                "shared", "Textbook pp. 118–",
                listOf(w("sequence", "ترتیب"), w("selection", "انتخاب"), w("condition", "شرط")),
                "Sequence is one statement after another. Selection chooses a path with if / elif / else.",
                "ترتیب ایک کے بعد ایک بیان۔ انتخاب if / elif / else سے راستہ چنتا ہے۔",
                "Indentation is part of Python syntax — the suite under if must be indented.\nif marks >= 80:\n    grade = 'A'\nelif marks >= 40:\n    grade = 'Pass'\nelse:\n    grade = 'Fail'",
                "پائتھن میں حاشیہ نحو کا حصہ ہے۔ if، elif، else راستہ چنتے ہیں۔",
                "Sequence seedha raasta. Selection sawal: marks 40 se zyada? Diamond shape flowchart mein. Python mein indent zaroori hai — bhool gaye to IndentationError. elif matlab else if, jitni conditions hon utne lag sakte hain, else optional last net hai.",
                "Write a program that prints Pass or Fail from an inputted mark, then add an A grade band.",
                "نمبر لے کر پاس/فیل چھاپیں، پھر اے گریڈ کا بینڈ جوڑیں۔",
                listOf(
                    c("What does else do?", "else کیا کرتا ہے؟", "Runs when every if/elif above was False.", "جب اوپر سب غلط ہوں تب چلتا ہے۔")
                ),
                listOf("Write an if-elif-else grade program"),
                listOf("گریڈ کا if-elif-else لکھ سکتا/سکتی ہوں"),
                "diagrams/selection.png",
                listOf("booklet/v1_p47.jpg", "booklet/v1_p48.jpg")
            ),
            lesson(
                "3.5b", "u3", "3.5b",
                "Repetition: for and while loops", "تکرار: فار اور وائل لوپس",
                "Repetition: for aur while loops",
                "shared", "Textbook pp. 124–",
                listOf(w("loop", "لوپ"), w("iteration", "تکرار"), w("range", "رینج")),
                "Known count → for. Wait for a condition → while. Forgetting the update creates an infinite loop.",
                "گنتی معلوم ہو تو for۔ شرط کا انتظار ہو تو while۔ اپ ڈیٹ بھولنا لامحدود لوپ ہے۔",
                "for i in range(1, 6): print(i)  → 1…5\nrange(5) is 0..4; range(0,10,2) is even numbers.\nwhile n > 0: print(n); n = n - 1\nTrace on paper before you run. Infinite loops freeze the terminal — stop the process, then fix the update.",
                "معلوم تعداد for۔ شرط while۔ range(5) صفر سے چار۔ اپ ڈیٹ نہ ہو تو لوپ رکی نہیں۔",
                "for jab pata ho kitni dafa. while jab condition ka intezaar. range start inclusive, stop exclusive. Infinite loop tab jab n = n minus 1 bhool jao. Paper par trace: n=3, 2, 1, stop.",
                "Print the 2-times table with for, then rewrite it with while.",
                "2 کا پہاڑا for سے، پھر while سے لکھیں۔",
                listOf(
                    c("When do you choose while over for?", "while کب؟", "When you do not know the count in advance.", "جب گنتی پہلے سے معلوم نہ ہو۔")
                ),
                listOf("Write a for loop with range", "Write a while loop that terminates"),
                listOf("رینج والا for لکھ سکتا/سکتی ہوں", "رکنے والا while لکھ سکتا/سکتی ہوں"),
                "diagrams/loops.png",
                listOf("booklet/v1_p49.jpg", "booklet/v1_p50.jpg")
            ),
            lesson(
                "3.6", "u3", "3.6",
                "Libraries and debugging", "لائبریریز اور ڈیبگنگ",
                "Libraries aur debugging",
                "shared", "Textbook pp. 130–134",
                listOf(w("library", "لائبریری"), w("import", "امپورٹ"), w("debug", "ڈیبگ"), w("traceback", "ٹریس بیک")),
                "import math, random, datetime. Read the traceback, print values, change one thing.",
                "math، random، datetime امپورٹ کریں۔ ٹریس بیک پڑھو، ویلیو چھاپو، ایک چیز بدلو۔",
                "SyntaxError: spelling, missing colon or bracket. NameError: used a name before creating it. TypeError: '2'+2. Logic error: runs but the answer is wrong.\nimport math; math.sqrt(9)\nimport random; random.randint(1, 6)",
                "سنٹیکس، نیم، ٹائپ، لاجک غلطیاں۔ پہلے امپورٹ، پھر فنکشن۔ ٹریس بیک پڑھو۔",
                "Library ready-made tools hain. import math; math.sqrt. Debugging: red underline, traceback last line, print karke dekho, ek change. SyntaxError spelling. NameError variable se pehle use. TypeError galat type. Logic error chup ke galat jawab.",
                "Write a program that imports random and prints a dice roll. Then break it on purpose and read the traceback.",
                "random سے پانسہ چھاپیں، پھر جان بوجھ کر توڑ کر ٹریس بیک پڑھیں۔",
                listOf(
                    c("Name four error types.", "چار غلطیاں؟", "Syntax, Name, Type, logic.", "سنٹیکس، نیم، ٹائپ، لاجک۔")
                ),
                listOf("Import and use a library", "Fix a bug from a traceback"),
                listOf("لائبریری استعمال کر سکتا/سکتی ہوں", "ٹریس بیک سے بگ ٹھیک کر سکتا/سکتی ہوں"),
                "diagrams/debug.png",
                listOf("booklet/v1_p51.jpg", "booklet/v1_p52.jpg")
            ),
            lesson(
                "3.R", "u3", "3.R",
                "Unit 3 revision and mock test", "یونٹ 3 اعادہ اور ماک ٹیسٹ",
                "Unit 3 revision aur mock test",
                "1 period", "Booklet p. 53",
                emptyList(),
                "Type one tiny program for variables, if, and a loop without looking at notes.",
                "بغیر نوٹس متغیر، if، اور لوپ کا چھوٹا پروگرام لکھیں۔",
                "Recite types, operator families, if-elif-else, for vs while, four errors. Then sit the mock.",
                "اقسام، آپریٹر، if، for/while، چار غلطیاں۔ پھر ماک۔",
                "Zabani: input string, int cast, = versus ==, indent, range exclusive stop, infinite while. Phir Unit 3 quiz.",
                "Take the Unit 3 mock test.",
                "یونٹ 3 ماک ٹیسٹ حل کریں۔",
                listOf(c("Ready?", "تیار؟", "Open the Unit 3 quiz.", "کوئز کھولیں۔")),
                listOf("Write a short graded program from memory"),
                listOf("یاد سے مختصر گریڈ پروگرام لکھ سکتا/سکتی ہوں"),
                "diagrams/python_ide.png",
                listOf("booklet/v1_p47.jpg", "booklet/v1_p49.jpg"),
                isRevision = true
            )
        )
    )

    private fun unit4(): CourseUnit = CourseUnit(
        id = "u4", number = 4,
        titleEn = "Database Management",
        titleUr = "ڈیٹا بیس مینجمنٹ",
        titleUrdish = "Database management — tables, keys, Access",
        weeks = "4 weeks · 12–14 periods",
        colorHex = "#B45309",
        coverDiagram = "diagrams/er_model.png",
        summaryEn = "DBMS, keys, ER, referential integrity, library schema, Access tables, forms, queries.",
        summaryUr = "ڈی بی ایم ایس، کیز، ای آر، ریفرینشل انٹیگریٹی، لائبریری اسکیمہ، ایکسس ٹیبل، فارم، کوئری۔",
        lessons = listOf(
            lesson(
                "4.1", "u4", "4.1",
                "Data, DBMS, tables and keys", "ڈیٹا، ڈی بی ایم ایس، ٹیبلز اور کیز",
                "Data, D B M S, tables aur keys",
                "shared", "Textbook pp. 139–",
                listOf(w("data", "ڈیٹا"), w("DBMS", "ڈی بی ایم ایس"), w("primary key", "پرائمری کی"), w("foreign key", "فارن کی")),
                "A DBMS stores data in tables. A primary key uniquely identifies a row. A foreign key points at another table's primary key.",
                "ڈی بی ایم ایس ڈیٹا ٹیبلز میں رکھتا ہے۔ پرائمری کی قطار کی منفرد شناخت ہے۔ فارن کی دوسری ٹیبل کی پرائمری کی کی طرف اشارہ ہے۔",
                "Data is raw facts; a database is an organised collection; a DBMS is the software (MS Access in this course) that creates, protects and queries it.\nPrimary key: unique and not null — one per table (Roll in Student).\nCandidate key: any field(s) that could have been primary.\nForeign key: value must match an existing primary key (or be NULL) — that is the seed of referential integrity.",
                "ڈیٹا خام حقائق۔ ڈیٹا بیس منظم مجموعہ۔ ڈی بی ایم ایس سافٹ ویئر۔ پرائمری کی منفرد اور خالی نہیں۔ فارن کی دوسری پرائمری کی سے ملتی ہے۔",
                "Table rows aur columns. Primary key unique plus not null — Roll. Foreign key doosri table ko join karti hai. Candidate key woh field jo primary ban sakti thi. D B M S Access is course mein. Data raw hai, information processed.",
                "Design a Student table with five fields and mark the primary key.",
                "پانچ فیلڈز کا Student ٹیبل بنائیں اور پرائمری کی نشان زد کریں۔",
                listOf(
                    c("Primary vs foreign key?", "پرائمری اور فارن کی؟",
                        "Primary uniquely identifies a row; foreign refers to a primary key elsewhere.",
                        "پرائمری قطار پہچانتی ہے؛ فارن دوسری پرائمری کی کی طرف اشارہ ہے۔")
                ),
                listOf("Define DBMS", "Choose a primary key", "Explain a foreign key"),
                listOf("ڈی بی ایم ایس بتا سکتا/سکتی ہوں", "پرائمری کی چن سکتا/سکتی ہوں", "فارن کی سمجھا سکتا/سکتی ہوں"),
                "diagrams/dbms.png",
                listOf("booklet/v1_p59.jpg", "booklet/v1_p60.jpg")
            ),
            lesson(
                "4.4", "u4", "4.4",
                "ER model and referential integrity", "ای آر ماڈل اور ریفرینشل انٹیگریٹی",
                "E R model aur referential integrity",
                "shared", "Textbook pp. 145–",
                listOf(w("entity", "وجود"), w("attribute", "صفت"), w("relationship", "تعلق"), w("cardinality", "کارڈینیلٹی")),
                "Entities are rectangles, relationships diamonds, attributes ovals. Referential integrity forbids orphan foreign keys.",
                "وجود مستطیل، تعلق لوزی، صفات بیضوی۔ ریفرینشل انٹیگریٹی یتیم فارن کی منع کرتی ہے۔",
                "Cardinalities: 1:1, 1:M, M:N. A member borrows many books — 1:M, resolved in implementation by a bridge table. You must not delete a Member who still has BorrowRecord rows.",
                "1:1، 1:کئی، کئی:کئی۔ ممبر کئی کتابیں مستعار لیتا ہے۔ جس ممبر کے عاریت ریکارڈ ہوں اسے نہ مٹائیں۔",
                "E R diagram exam drawing hai: rectangle entity, diamond relationship, oval attribute. Member borrows Book. Cardinality 1 to M. Referential integrity: BorrowRecord.Member I D us Member mein maujood hona chahiye. Delete parent pehle child rows handle karo.",
                "Draw MEMBER — borrows — BOOK with attributes MemberID and BookID underlined as keys.",
                "میمبر — عاریت — کتاب کا ای آر بنائیں اور کیز خط کشیدہ کریں۔",
                listOf(
                    c("What does referential integrity protect?", "ریفرینشل انٹیگریٹی کیا بچاتی ہے؟",
                        "It stops a foreign key pointing at a missing primary key.",
                        "فارن کی غائب پرائمری کی کی طرف اشارہ نہ کرے۔")
                ),
                listOf("Draw a 3-entity ER", "State 1:1, 1:M, M:N"),
                listOf("تین وجود کا ای آر کھینچ سکتا/سکتی ہوں", "تین کارڈینیلٹیاں بتا سکتا/سکتی ہوں"),
                "diagrams/er_model.png",
                listOf("booklet/v1_p61.jpg", "booklet/v1_p62.jpg")
            ),
            lesson(
                "4.6", "u4", "4.6",
                "Relational schema: Library case study", "ریلیشنل اسکیمہ: لائبریری کیس",
                "Library relational schema case study",
                "shared", "Textbook pp. 148–",
                listOf(w("schema", "اسکیمہ"), w("bridge table", "پل ٹیبل")),
                "MEMBER, BOOK and BORROWRECORD. The bridge table holds two foreign keys plus IssueDate and ReturnDate.",
                "میمبر، کتاب، برو ریکارڈ۔ پل ٹیبل دو فارن کیز کے ساتھ تاریخیں رکھتی ہے۔",
                "The textbook lists BorrowRecord as BorrowID, MemberID, BookID; IssueDate and ReturnDate come from the requirements. M:N between Member and Book is resolved by BorrowRecord. Do not store book title inside BorrowRecord — that duplicates data.",
                "برو ریکارڈ پل ہے۔ عنوان دوبارہ مت رکھو — ڈیٹا دہراؤ ہوگا۔",
                "Teen tables: MEMBER, BOOK, BORROWRECORD. Borrow I D primary. Member I D aur Book I D foreign. IssueDate, ReturnDate requirements se. M to N resolve ho gaya. Normalization ka simple message: title Book table mein, borrow table mein nahi.",
                "Write the three CREATE-style field lists and mark PK/FK.",
                "تینوں ٹیبل کی فیلڈ لسٹ لکھ کر پی کے/ایف کے لگائیں۔",
                listOf(
                    c("Why is BorrowRecord needed?", "برو ریکارڈ کیوں؟",
                        "To store each loan and to break the M:N into two 1:M links.",
                        "ہر عاریت رکھنے اور کئی بہ کئی کو توڑنے کے لیے۔")
                ),
                listOf("Write the library schema with keys"),
                listOf("لائبریری اسکیمہ کیز سمیت لکھ سکتا/سکتی ہوں"),
                "diagrams/schema.png",
                listOf("booklet/v1_p63.jpg", "booklet/v1_p64.jpg")
            ),
            lesson(
                "4.8", "u4", "4.8",
                "Database objects and tables in MS Access", "ایم ایس ایکسس میں آبجیکٹس اور ٹیبلز",
                "M S Access objects aur tables",
                "4–5 shared with 4.10–4.11", "Textbook pp. 152–159",
                listOf(w("table", "ٹیبل"), w("form", "فارم"), w("query", "کوئری"), w("report", "رپورٹ"), w("Design View", "ڈیزائن ویو")),
                "Form → Table → Query → Report. Create tables in Design View so you control types and the primary key.",
                "فارم ← ٹیبل ← کوئری ← رپورٹ۔ ٹیبل ڈیزائن ویو میں بنائیں تاکہ ٹائپ اور کی آپ کے اختیار میں ہوں۔",
                "Datasheet View is quick but limited. Design View: Create → Table Design → field name + data type → Primary Key button → Save. Tables come first because every other object depends on them.",
                "ڈیٹا شیٹ تیز مگر محدود۔ ڈیزائن ویو بہترین۔ پہلے ٹیبل، باقی آبجیکٹس اس پر منحصر۔",
                "Char objects: Form enter, Table store, Query filter, Report print. Data flow Form se Table, Query nikaalti, Report dikhati. Design View best practice. Field1 Field2 se mat chhodo — naam khud do, type chuno, key icon.",
                "Create a Student table in Design View with at least five fields and a primary key.",
                "ڈیزائن ویو میں پانچ فیلڈز کا Student ٹیبل اور پرائمری کی بنائیں۔",
                listOf(
                    c("Name the four Access objects in data-flow order.", "چار آبجیکٹس بہاؤ کی ترتیب؟",
                        "Form, Table, Query, Report.", "فارم، ٹیبل، کوئری، رپورٹ۔")
                ),
                listOf("Create a table in Design View", "Explain why tables come first"),
                listOf("ڈیزائن ویو میں ٹیبل بنا سکتا/سکتی ہوں", "ٹیبل کی اولیت سمجھا سکتا/سکتی ہوں"),
                "diagrams/access_objects.png",
                listOf("booklet/v1_p65.jpg", "booklet/v1_p66.jpg")
            ),
            lesson(
                "4.10", "u4", "4.10",
                "Designing forms", "فارمز بنانا",
                "Forms banana — Form Wizard",
                "shared 4.8–4.11", "Textbook pp. 159–161",
                listOf(w("form", "فارم"), w("Form Wizard", "فارم وزرڈ"), w("layout", "ترتیب"), w("control", "کنٹرول")),
                "A form is a friendly screen over a table. Columnar layout is best for data entry.",
                "فارم ٹیبل پر آسان اسکرین ہے۔ کالمی ترتیب اندراج کے لیے بہترین۔",
                "Purpose: enter, modify, view — with fewer errors and optional validation. Wizard: Create → Form Wizard → choose table and fields → layout (Columnar) → name → Finish. Layouts: Columnar (one record), Tabular (many rows), Datasheet (grid), Justified (compact).",
                "مقصد: اندراج، ترمیم، مشاہدہ۔ وزرڈ سے ٹیبل چنو، فیلڈز، کالمی ترتیب، نام، ختم۔",
                "Form table ki jagah nahi — uske upar screen hai. Data source table ya query. Columnar ek waqt ek record, data entry ke liye. Students forms, queries, reports ko interchangeable samajhte hain — galat, roles alag hain.",
                "Build a Columnar form for Student and enter five records through it, not the table.",
                "Student کا کالمی فارم بنا کر پانچ ریکارڈ فارم سے درج کریں، ٹیبل سے نہیں۔",
                listOf(
                    c("Three purposes of a form?", "فارم کے تین مقاصد؟", "Entry, modification, viewing.", "اندراج، ترمیم، مشاہدہ۔"),
                    c("Which layout shows one record at a time?", "ایک ریکارڈ کون سی ترتیب؟", "Columnar.", "کالمی۔")
                ),
                listOf("Build a wizard form", "Pick a layout for a purpose"),
                listOf("وزرڈ فارم بنا سکتا/سکتی ہوں", "مقصد کے مطابق ترتیب چن سکتا/سکتی ہوں"),
                "diagrams/forms.png",
                listOf("booklet/v1_p67.jpg", "booklet/v1_p68.jpg")
            ),
            lesson(
                "4.11", "u4", "4.11",
                "Queries, summaries and charts", "کوئریز، خلاصے اور چارٹ",
                "Queries, summaries aur charts",
                "shared 4.8–4.11", "Textbook pp. 162–169",
                listOf(w("query", "کوئری"), w("criteria", "شرائط"), w("Group By", "گروپ بائی"), w("chart", "چارٹ")),
                "A query retrieves without changing tables. AND = same row; OR = different rows. Group By summarises; a chart tells the story.",
                "کوئری ٹیبل بدلے بغیر نکالتی ہے۔ اینڈ ایک قطار، اور مختلف قطاریں۔ گروپ بائی خلاصہ، چارٹ کہانی۔",
                "Create → Query Design → add table → fields on the grid → Run. Filter: type a criterion under a field, e.g. \"Computer Science\" under Department. Totals: Count, Sum, Avg with Group By. Charts: bar, pie, line from the query result.",
                "کوئری ڈیزائن، فیلڈز، رن۔ شرط فیلڈ کے نیچے۔ اینڈ ایک قطار، اور الگ قطاریں۔ مجموعے اور چارٹ۔",
                "Query table ko nahi badalti, sirf nikaalti hai. SELECT mental model. AND same row dono true. OR alag rows. Group By summaries. Chart query se banta hai, khali guess se nahi. Practical: table plus form plus ek filtered query.",
                "Make a query that lists CS students with Marks > 70, then chart the counts by department.",
                "سی ایس طلبہ نمبر 70 سے زیادہ کی کوئری بنائیں، پھر شعبہ وار چارٹ۔",
                listOf(
                    c("AND versus OR in the grid?", "گرڈ میں اینڈ اور اور؟",
                        "AND: criteria on the same row. OR: extra OR row.",
                        "اینڈ ایک قطار؛ اور الگ قطار۔")
                ),
                listOf("Build a filtered query", "Add a Group By total", "Make a chart from a query"),
                listOf("فلٹر کوئری بنا سکتا/سکتی ہوں", "گروپ بائی جوڑ سکتا/سکتی ہوں", "کوئری سے چارٹ بنا سکتا/سکتی ہوں"),
                "diagrams/queries.png",
                listOf("booklet/v1_p68.jpg", "booklet/v1_p69.jpg")
            ),
            lesson(
                "4.R", "u4", "4.R",
                "Unit 4 revision and mock test", "یونٹ 4 اعادہ اور ماک ٹیسٹ",
                "Unit 4 revision aur mock test",
                "1 period", "Booklet p. 70",
                emptyList(),
                "Sketch the library ER and name the four Access objects, then sit the mock.",
                "لائبریری ای آر اور چار ایکسس آبجیکٹس، پھر ماک۔",
                "Recite keys, cardinalities, referential integrity, Form→Table→Query→Report, Columnar, AND/OR.",
                "کیز، کارڈینیلٹی، انٹیگریٹی، چار آبجیکٹس، کالمی، اینڈ/اور۔",
                "Zabani: primary unique, foreign points, ER shapes, BorrowRecord bridge, Design View, form purposes, query does not change tables. Phir Unit 4 quiz.",
                "Take the Unit 4 mock test.",
                "یونٹ 4 ماک ٹیسٹ حل کریں۔",
                listOf(c("Ready?", "تیار؟", "Open the Unit 4 quiz.", "کوئز کھولیں۔")),
                listOf("Draw the library schema from memory"),
                listOf("لائبریری اسکیمہ یاد سے کھینچ سکتا/سکتی ہوں"),
                "diagrams/schema.png",
                listOf("booklet/v1_p63.jpg", "booklet/v1_p65.jpg"),
                isRevision = true
            )
        )
    )

    private fun unit5(): CourseUnit = CourseUnit(
        id = "u5", number = 5,
        titleEn = "Applications and Impacts of Computing",
        titleUr = "کمپیوٹنگ کے اطلاقات اور اثرات",
        titleUrdish = "Computing ke applications aur asraat — A I, I o T",
        weeks = "Units 5–6 volume 2",
        colorHex = "#0369A1",
        coverDiagram = "diagrams/iot.png",
        summaryEn = "AI, six IoT components, analytics, IoT uses, sources, impacts, assistive tech.",
        summaryUr = "اے آئی، آئی او ٹی کے چھ اجزا، اینالیٹکس، استعمالات، مصادر، اثرات، معاون ٹیکنالوجی۔",
        lessons = listOf(
            lesson(
                "5.1", "u5", "5.1",
                "Introduction and Artificial Intelligence", "تعارف اور مصنوعی ذہانت",
                "Computing ki dunya aur Artificial Intelligence",
                "1 of first 3", "Textbook p. 175",
                listOf(w("Artificial Intelligence", "مصنوعی ذہانت"), w("chatbot", "چیٹ بوٹ"), w("smart system", "سمارٹ نظام")),
                "Computing is everyday life in Pakistan — schools, banks, hospitals, farms. AI learns from data and then decides.",
                "کمپیوٹنگ پاکستان کی روزمرہ ہے — اسکول، بینک، ہسپتال، کھیت۔ اے آئی ڈیٹا سے سیکھ کر فیصلہ کرتی ہے۔",
                "Students use phones to learn; teachers use an LMS. Hospitals keep digital records; banks use apps and ATMs; farmers use weather and smart irrigation. AI examples: chatbots, vision (faces, plates), recommendations. AI is not the same as IoT or analytics: IoT collects, analytics studies, AI decides.",
                "طلبہ فون سے سیکھتے ہیں، اساتذہ ایل ایم ایس، ہسپتال ڈیجیٹل ریکارڈ، بینک ایپ، کسان موسم۔ اے آئی، آئی او ٹی اور اینالیٹکس ایک چیز نہیں۔",
                "A I matlab machine data se seekh kar decision. Pakistan: LMS, ATM, digital hospital file, weather for kisan. Favourite MCQ: A I, I o T, analytics same thing? False. I o T collect, analytics study, A I decide. Wikipedia primary source? False — tertiary summary.",
                "List four places you already use computing this week, then mark which ones involve AI.",
                "اس ہفتے کمپیوٹنگ کے چار مقامات لکھیں اور اے آئی والے نشان زد کریں۔",
                listOf(
                    c("Are AI, IoT and analytics the same?", "کیا تینوں ایک ہیں؟",
                        "False. IoT collects, analytics studies, AI decides.",
                        "غلط۔ آئی او ٹی اکٹھا، اینالیٹکس تجزیہ، اے آئی فیصلہ۔")
                ),
                listOf("Give Pakistani examples of computing", "Separate AI from IoT"),
                listOf("پاکستانی مثالیں دے سکتا/سکتی ہوں", "اے آئی اور آئی او ٹی الگ کر سکتا/سکتی ہوں"),
                "diagrams/ai.png",
                listOf("booklet/v2_p07.jpg", "booklet/v2_p08.jpg")
            ),
            lesson(
                "5.2", "u5", "5.2",
                "Internet of Things and its six components", "انٹرنیٹ آف تھنگز اور اس کے چھ اجزا",
                "I o T ke chhe ajza — See Act Carry Decide Keep Show",
                "shared 3", "Textbook pp. 175–177",
                listOf(w("IoT", "انٹرنیٹ آف تھنگز"), w("sensor", "سینسر"), w("actuator", "ایکچویٹر"), w("connectivity", "رابطہ"), w("cloud", "کلاؤڈ"), w("interface", "انٹرفیس")),
                "Sensors SEE, actuators ACT, connectivity CARRIES, processing DECIDES, cloud KEEPS, UI SHOWS.",
                "سینسر دیکھتا، ایکچویٹر عمل، کنکٹیویٹی پہنچاتی، پروسیسنگ فیصلہ، کلاؤڈ رکھتی، یو آئی دکھاتی۔",
                "IoT is a system of internet-connected devices that collect and share data to act automatically.\ni Sensors — temperature, light, motion, soil-moisture, fingerprint, camera, smoke.\nii Actuators — motor, valve, switch, door opener, alarm. Sensor = input; actuator = output.\niii Connectivity — Wi-Fi, Bluetooth, ZigBee, LoRaWAN, NB-IoT, 4G/5G.\niv Data processing — collect → organise → analyse → decide.\nv Cloud — Google Drive, Classroom, LMS; store and process large IoT data.\nvi User interface — app, touch screen, dashboard, voice.\nExam favourite: smart street light — light sensor + lamp actuator.",
                "آئی او ٹی انٹرنیٹ سے جڑے آلات کا نظام ہے۔ چھ اجزا: سینسر، ایکچویٹر، کنکٹیویٹی، ڈیٹا پروسیسنگ، کلاؤڈ، صارف انٹرفیس۔ سینسر ان پٹ، ایکچویٹر آؤٹ پٹ۔",
                "Memory trick zabani: Sensors See, Actuators Act, Connectivity Carries, Data processing Decides, Cloud Keeps, U I Shows. Sensor input, actuator output — favourite exam. Automatic door: motion sensor, control unit, motor actuator. Smartwatch Bluetooth se phone U I ko data bhejti hai. Cloud Drive, Classroom. Connectivity ke 6 names: Wi-Fi, Bluetooth, ZigBee, LoRaWAN, NB-IoT, 4G/5G.",
                "Label a blank six-box IoT diagram from the word bank, then name sensor and actuator in a smart street light.",
                "چھ خانوں والا خاکہ بھریں اور سمارٹ اسٹریٹ لائٹ کا سینسر/ایکچویٹر نام لیں۔",
                listOf(
                    c("Sensor versus actuator?", "سینسر اور ایکچویٹر؟",
                        "Sensor collects from the physical world; actuator performs a physical action on a command.",
                        "سینسر معلومات جمع؛ ایکچویٹر حکم پر عمل۔"),
                    c("Name the six components in booklet order.", "چھ اجزا؟",
                        "Sensors, actuators, connectivity, data processing, cloud, user interface.",
                        "سینسر، ایکچویٹر، کنکٹیویٹی، پروسیسنگ، کلاؤڈ، یو آئی۔")
                ),
                listOf("List six IoT components with a verb", "Give sensor/actuator pairs"),
                listOf("چھ اجزا فعل سمیت بتا سکتا/سکتی ہوں", "سینسر/ایکچویٹر جوڑی دے سکتا/سکتی ہوں"),
                "diagrams/iot.png",
                listOf("booklet/v2_p09.jpg", "booklet/v2_p10.jpg", "booklet/v2_p11.jpg")
            ),
            lesson(
                "5.3", "u5", "5.3",
                "Data Analytics", "ڈیٹا اینالیٹکس",
                "Data Analytics — collect, clean, decide",
                "shared", "Textbook pp. 177–179",
                listOf(w("analytics", "اینالیٹکس"), w("visualise", "نمودار"), w("insight", "بصیرت")),
                "Analytics turns raw IoT readings into a decision. Cycle: collect → clean → analyse → visualise → decide.",
                "اینالیٹکس خام ریڈنگ کو فیصلے میں بدلتا ہے۔ چکر: اکٹھا، صاف، تجزیہ، نمودار، فیصلہ۔",
                "Example: soil-moisture readings → chart → irrigate only when dry. Analytics is not AI and not IoT. A bar chart of weekly moisture is analytics; the valve that then opens is the actuator; a model that predicts next week's rain is closer to AI.",
                "مثال: مٹی کی نمی کا چارٹ، خشک ہو تو آبپاشی۔ اینالیٹکس نہ اے آئی ہے نہ آئی او ٹی۔",
                "Cycle yaad: Collect, Clean, Analyse, Visualise, Decide. IoT data raw hota hai, analytics usko useful banati hai. Exam: teen names same? Nahi.",
                "Take five imaginary moisture numbers and sketch a bar chart plus one sentence decision.",
                "پانچ نمی کے اعداد کا بار چارٹ اور ایک جملے کا فیصلہ۔",
                listOf(
                    c("List the analytics cycle.", "اینالیٹکس کا چکر؟",
                        "Collect, clean, analyse, visualise, decide.",
                        "اکٹھا، صاف، تجزیہ، نمودار، فیصلہ۔")
                ),
                listOf("Walk an IoT reading through the analytics cycle"),
                listOf("ریڈنگ کو اینالیٹکس چکر سے گزار سکتا/سکتی ہوں"),
                "diagrams/analytics.png",
                listOf("booklet/v2_p12.jpg", "booklet/v2_p13.jpg")
            ),
            lesson(
                "5.4", "u5", "5.4",
                "Uses of IoT in different areas", "مختلف شعبوں میں آئی او ٹی",
                "IoT ke istemaal — city, farm, hospital, grid, wearables",
                "shared", "Textbook pp. 180–183",
                listOf(w("smart city", "سمارٹ شہر"), w("smart grid", "سمارٹ گرڈ"), w("wearable", "ویئر ایبل"), w("smart farming", "سمارٹ کاشتکاری")),
                "For each area name a sensor, an actuator and a benefit. Smart grid and wearables are in the SLO even if the textbook is thin — the booklet enriches them.",
                "ہر شعبے میں سینسر، ایکچویٹر، فائدہ۔ سمارٹ گرڈ اور ویئر ایبل نصاب میں ہیں — کتابچہ نے بڑھایا۔",
                "Smart city: traffic and street lights. Industry: machine temperature. Healthcare: patient monitors. Education: smart classrooms. Automation: home/factory. Smart grid: balance electricity load, cut waste. Smart farming: soil moisture → valve. Wearables: watch/band measures steps and heart rate, sends to a phone UI.\nMemory: Sensor → actuator → benefit in each area.",
                "سمارٹ شہر، صنعت، صحت، تعلیم، خودکار، گرڈ، کاشتکاری، ویئر ایبل۔ ہر جگہ سینسر ← ایکچویٹر ← فائدہ۔",
                "SLO lambi list: smart cities, industries, healthcare, education, automation, smart grid, smart farming, wearables. Grid aur wearables booklet ne extra cover kiye. Farming: soil sensor, water valve actuator, paani bachta hai. Wearable: sensors on wrist, phone UI. Street light: light sensor, lamp actuator.",
                "Fill an eight-row table: area, sensor, actuator, benefit.",
                "آٹھ قطاروں کا جدول: شعبہ، سینسر، ایکچویٹر، فائدہ۔",
                listOf(
                    c("In a smart street light, name sensor and actuator.", "اسٹریٹ لائٹ کا سینسر/ایکچویٹر؟",
                        "Light/motion sensor; lamp (or dimmer) actuator.",
                        "روشنی/حرکت سینسر؛ لیمپ ایکچویٹر۔")
                ),
                listOf("Give IoT uses in eight areas", "Always pair sensor with actuator"),
                listOf("آٹھ شعبوں میں استعمال بتا سکتا/سکتی ہوں", "سینسر کے ساتھ ایکچویٹر جوڑ سکتا/سکتی ہوں"),
                "diagrams/iot_uses.png",
                listOf("booklet/v2_p14.jpg", "booklet/v2_p15.jpg", "booklet/v2_p16.jpg", "booklet/v2_p17.jpg")
            ),
            lesson(
                "5.5", "u5", "5.5",
                "AI in education · careers and skills", "تعلیم میں اے آئی · کیریئر اور مہارتیں",
                "A I education, careers aur skills",
                "shared", "Textbook pp. 183–",
                listOf(w("career", "کیریئر"), w("skill", "مہارت"), w("ethics", "اخلاق")),
                "AI can quiz and translate; you still own the exam explanation. Careers: analyst, IoT tech, developer, teacher.",
                "اے آئی کوئز اور ترجمہ کر سکتی ہے؛ امتحان کی وضاحت آپ کی ہے۔ کیریئر: اینالسٹ، آئی او ٹی، ڈیولپر، استاد۔",
                "Skills: problem solving, Python, ethics, teamwork. Watch-outs: bias, privacy, cheating, over-trusting a bot. Pakistan: NADRA systems, banks, farms, college LMS.",
                "مہارت: مسئلہ حل، پائتھن، اخلاق، ٹیم۔ خطرات: تعصب، رازداری، نقل۔",
                "Classroom A I madadgar hai lekin paper aap likhte ho. Careers: data analyst, I o T technician, app developer, CS teacher. Skills: computational thinking plus ethics. Privacy: doosre ka data share mat karo.",
                "Write a 6-line career card: job title, two skills, one ethical risk.",
                "چھ سطروں کا کیریئر کارڈ: نوکری، دو مہارتیں، ایک اخلاقی خطرہ۔",
                listOf(
                    c("Name two risks of classroom AI.", "کلاس اے آئی کے دو خطرات؟",
                        "Cheating / over-trust, and privacy of student data.",
                        "نقل/اندھا اعتماد، اور طلبہ کے ڈیٹا کی رازداری۔")
                ),
                listOf("List three computing careers", "State one AI ethics rule"),
                listOf("تین کیریئر بتا سکتا/سکتی ہوں", "ایک اخلاقی قاعدہ کہہ سکتا/سکتی ہوں"),
                "diagrams/ai_edu.png",
                listOf("booklet/v2_p18.jpg", "booklet/v2_p19.jpg")
            ),
            lesson(
                "5.6", "u5", "5.6",
                "Information sources", "معلومات کے مصادر",
                "Reliable versus unreliable sources",
                "shared", "Textbook pp. 183–186",
                listOf(w("primary source", "بنیادی ماخذ"), w("secondary", "ثانوی"), w("tertiary", "تیسرے درجے"), w("reliable", "قابل اعتماد")),
                "Check author, date, evidence and purpose. Wikipedia summarises others — it is tertiary, not primary.",
                "مصنف، تاریخ، ثبوت، مقصد چیک کریں۔ وکی پیڈیا دوسروں کا خلاصہ ہے — بنیادی نہیں، تیسرے درجے کا ہے۔",
                "More reliable: textbook, journal, government/exam board, named expert with date and references. Treat with care: anonymous social posts, no date, forwarded rumours. A news article is usually secondary. Your own class survey is primary (Unit 6).",
                "زیادہ قابل اعتماد: کتاب، جریدہ، سرکاری بورڈ، نام والا ماہر۔ احتیاط: گمنام پوسٹ، بغیر تاریخ افواہ۔",
                "Exam: Wikipedia primary? False. Everything on internet equally reliable? False. Hamesha author, date, evidence. Primary aap khud collect; secondary kisi aur ne; tertiary sirf summary.",
                "Take one textbook page, one news link and one social post. Score each on author/date/evidence.",
                "ایک کتابی صفحہ، ایک خبر، ایک سوشل پوسٹ — مصنف/تاریخ/ثبوت پر نمبر دیں۔",
                listOf(
                    c("Why is Wikipedia not a primary source?", "وکی پیڈیا بنیادی کیوں نہیں؟",
                        "It summarises other people's work, so it is tertiary.",
                        "یہ دوسروں کا خلاصہ ہے، اس لیے تیسرے درجے کا۔")
                ),
                listOf("Judge a source with four checks"),
                listOf("چار چیک سے ماخذ جانچ سکتا/سکتی ہوں"),
                "diagrams/sources.png",
                listOf("booklet/v2_p20.jpg", "booklet/v2_p21.jpg")
            ),
            lesson(
                "5.7", "u5", "5.7",
                "Impacts of computing", "کمپیوٹنگ کے اثرات",
                "Human, cultural aur environmental asar",
                "shared", "Textbook pp. 186–",
                listOf(w("impact", "اثر"), w("e-waste", "ای ویسٹ"), w("privacy", "رازداری")),
                "Impacts are human (jobs, health, privacy), cultural (language, values, online behaviour) and environmental (e-waste, energy, smart-grid savings).",
                "اثرات انسانی (نوکری، صحت، رازداری)، ثقافتی (زبان، اقدار) اور ماحولیاتی (ای ویسٹ، توانائی، گرڈ)۔",
                "The SLO names environmental, cultural and human impact — say one concrete example in each column. Smart grid is a positive environmental example; discarded phones are a negative one.",
                "ہر کالم میں ایک ٹھوس مثال۔ سمارٹ گرڈ مثبت ماحولیاتی؛ پھینکے فون منفی۔",
                "Teen columns: Human, Cultural, Environmental. Jobs badalna human. Roman Urdu memes cultural. E-waste environmental. Balanced answer: faida plus nuqsan. Privacy human impact ka exam favourite.",
                "Make a 3×2 table: benefit and harm for each impact type.",
                "ہر اثر کی قسم پر فائدہ اور نقصان کا جدول۔",
                listOf(
                    c("Give one environmental benefit and one harm.", "ایک ماحولیاتی فائدہ اور نقصان؟",
                        "Benefit: smart grid reduces waste. Harm: e-waste from phones.",
                        "فائدہ: سمارٹ گرڈ فضلہ کم۔ نقصان: فونز کا ای ویسٹ۔")
                ),
                listOf("Give human, cultural and environmental examples"),
                listOf("تینوں اقسام کی مثال دے سکتا/سکتی ہوں"),
                "diagrams/impacts.png",
                listOf("booklet/v2_p22.jpg", "booklet/v2_p23.jpg", "booklet/v2_p24.jpg")
            ),
            lesson(
                "5.8", "u5", "5.8",
                "Assistive technologies", "معاون ٹیکنالوجیز",
                "Assistive tech — computing jo deewar girati hai",
                "shared", "Textbook pp. 189–",
                listOf(w("assistive technology", "معاون ٹیکنالوجی"), w("screen reader", "اسکرین ریڈر"), w("caption", "کیپشن")),
                "A screen reader is assistive — it reads on-screen text aloud. Design so more people can learn.",
                "اسکرین ریڈر معاون ہے — متن بول کر سناتا ہے۔ ایسا ڈیزائن کہ زیادہ لوگ سیکھ سکیں۔",
                "Examples: screen reader, magnifier, speech-to-text, alt text and captions, switch/sip-puff, high contrast. True/False from the booklet: a screen reader is assistive — True.",
                "مثالیں: اسکرین ریڈر، میگنیفائر، اسپیچ ٹو ٹیکسٹ، آلٹ ٹیکسٹ، سوئچ، ہائی کنٹراسٹ۔",
                "Assistive matlab barrier hatana. Screen reader andha ya low vision student ke liye. Captions deaf students ke liye. Alt text image ke liye. Inclusive design sab ke liye faida.",
                "Pick one classmate need (real or imagined) and name two assistive tools that would help.",
                "ایک ضرورت چن کر دو معاون اوزار نام لیں۔",
                listOf(
                    c("Is a screen reader assistive technology?", "کیا اسکرین ریڈر معاون ہے؟",
                        "True. It reads on-screen text aloud.",
                        "درست۔ یہ اسکرین کا متن بول کر سناتا ہے۔")
                ),
                listOf("Name five assistive tools", "Explain who each tool helps"),
                listOf("پانچ معاون اوزار نام لے سکتا/سکتی ہوں", "ہر اوزار کس کی مدد کرتا ہے بتا سکتا/سکتی ہوں"),
                "diagrams/assistive.png",
                listOf("booklet/v2_p25.jpg", "booklet/v2_p26.jpg", "booklet/v2_p27.jpg")
            ),
            lesson(
                "5.R", "u5", "5.R",
                "Unit 5 revision and mock test", "یونٹ 5 اعادہ اور ماک ٹیسٹ",
                "Unit 5 revision aur mock test",
                "1 period", "Booklet p. 28",
                emptyList(),
                "Say the six IoT verbs, then sit the mock.",
                "چھ آئی او ٹی افعال کہہ کر ماک۔",
                "See, Act, Carry, Decide, Keep, Show. AI ≠ IoT ≠ analytics. Eight IoT uses. Four source checks. Three impacts. Assistive list.",
                "دیکھو، عمل، پہنچاؤ، فیصلہ، رکھو، دکھاؤ۔ آٹھ استعمال۔ چار چیک۔ تین اثرات۔",
                "Zabani chhe verbs, phir street light pair, phir Wikipedia tertiary, phir e-waste, phir screen reader. Phir Unit 5 quiz.",
                "Take the Unit 5 mock test.",
                "یونٹ 5 ماک ٹیسٹ حل کریں۔",
                listOf(c("Ready?", "تیار؟", "Open the Unit 5 quiz.", "کوئز کھولیں۔")),
                listOf("Teach the six IoT components without notes"),
                listOf("بغیر نوٹس چھ اجزا پڑھا سکتا/سکتی ہوں"),
                "diagrams/iot.png",
                listOf("booklet/v2_p09.jpg", "booklet/v2_p14.jpg"),
                isRevision = true
            )
        )
    )

    private fun unit6(): CourseUnit = CourseUnit(
        id = "u6", number = 6,
        titleEn = "Digital Literacy",
        titleUr = "ڈیجیٹل خواندگی",
        titleUrdish = "Digital literacy — data collect karke present karna",
        weeks = "Inquiry cycle",
        colorHex = "#047857",
        coverDiagram = "diagrams/inquiry.png",
        summaryEn = "Literacy, data types, collection, primary/secondary, design, presentation, inquiry project.",
        summaryUr = "خواندگی، ڈیٹا کی اقسام، جمع، بنیادی/ثانوی، منصوبہ، پیشکش، انکوائری پروجیکٹ۔",
        lessons = listOf(
            lesson(
                "6.1", "u6", "6.1",
                "Digital literacy in the Information Age", "معلومات کے دور میں ڈیجیٹل خواندگی",
                "Digital literacy — Find, judge, use, share",
                "shared", "Textbook / booklet p. 36",
                listOf(w("digital literacy", "ڈیجیٹل خواندگی"), w("information age", "معلومات کا دور"), w("ethics", "اخلاق")),
                "Digital literacy is finding, judging, using and sharing data ethically with digital tools.",
                "ڈیجیٹل خواندگی ڈیٹا کو اخلاقی طور پر ڈھونڈنا، جانچنا، استعمال اور شیئر کرنا ہے۔",
                "The inquiry cycle: Ask → Collect → Clean → Analyse → Present → Reflect. You are not just a consumer of WhatsApp forwards — you are an investigator.",
                "چکر: پوچھو، اکٹھا، صاف، تجزیہ، پیش، غور۔ صرف فارورڈ پڑھنے والے نہیں، تحقیق کرنے والے ہیں۔",
                "Literacy sirf type karna nahi. Find, judge, use, share ethically. Cycle: Ask, Collect, Clean, Analyse, Present, Reflect. Age of information mein zyada data hai, is liye judgement zyada zaroori hai.",
                "Write one inquiry question about your own class that you could actually answer this week.",
                "اپنی جماعت کے بارے میں ایک ایسا سوال لکھیں جو اس ہفتے حل ہو سکے۔",
                listOf(
                    c("Name the six inquiry-cycle words.", "چکر کے چھ الفاظ؟",
                        "Ask, collect, clean, analyse, present, reflect.",
                        "پوچھو، اکٹھا، صاف، تجزیہ، پیش، غور۔")
                ),
                listOf("Define digital literacy", "Sketch the inquiry cycle"),
                listOf("ڈیجیٹل خواندگی کی تعریف کر سکتا/سکتی ہوں", "انکوائری چکر کھینچ سکتا/سکتی ہوں"),
                "diagrams/digital_literacy.png",
                listOf("booklet/v2_p36.jpg")
            ),
            lesson(
                "6.2", "u6", "6.2",
                "Types of data", "ڈیٹا کی اقسام",
                "Qualitative versus quantitative data",
                "shared", "Booklet p. 37",
                listOf(w("qualitative", "معیارى"), w("quantitative", "مقداری"), w("discrete", "منقطع"), w("continuous", "مسلسل")),
                "Qualitative is words and labels. Quantitative is numbers. Numbers split into discrete (countable) and continuous (measurable).",
                "معیارى الفاظ۔ مقداری اعداد۔ اعداد منقطع (گنتی) یا مسلسل (پیمائش)۔",
                "Favourite subject, blood group, yes/no → qualitative (nominal or ordinal). Marks, height, time → quantitative. Students in a class are discrete; temperature is continuous — the same idea as Unit 1 analog/digital.",
                "پسندیدہ مضمون معیارى۔ نمبر مقداری۔ طلبہ منقطع، درجہ حرارت مسلسل۔ یونٹ 1 سے جوڑیں۔",
                "Qualitative words, quantitative numbers. Discrete countable, continuous measurable. Blood group qualitative. Marks quantitative discrete if whole marks. Height continuous. Unit 1 se link: analog continuous, digital discrete.",
                "Sort ten class facts into a four-box: qualitative / quantitative / discrete / continuous.",
                "دس حقائق چار خانوں میں چھانٹیں।",
                listOf(
                    c("Is blood group qualitative?", "کیا بلڈ گروپ معیارى ہے؟", "Yes — it is a label, not a measurement.", "ہاں — لیبل ہے، پیمائش نہیں۔")
                ),
                listOf("Classify a datum into the four types"),
                listOf("ڈیٹا کی چار اقسام میں بانٹ سکتا/سکتی ہوں"),
                "diagrams/data_types.png",
                listOf("booklet/v2_p37.jpg", "booklet/v2_p38.jpg")
            ),
            lesson(
                "6.3", "u6", "6.3",
                "Data-collection strategies", "ڈیٹا اکٹھا کرنے کے طریقے",
                "Collection strategies — method sawaal se match ho",
                "shared", "Booklet p. 39",
                listOf(w("survey", "سروے"), w("interview", "انٹرویو"), w("observation", "مشاہدہ"), w("experiment", "تجربہ")),
                "Match the method to the question: survey for many people, interview for depth, sensor for automatic readings.",
                "طریقہ سوال سے ملے: سروے بہت لوگوں، انٹرویو گہرائی، سینسر خودکار ریڈنگ۔",
                "Survey/questionnaire, interview, observation, experiment, sensor/logger, document/log (existing school records). Each has bias: surveys skip people who are absent; observation changes behaviour if people know they are watched.",
                "سروے، انٹرویو، مشاہدہ، تجربہ، سینسر، دستاویز۔ ہر ایک میں تعصب ہو سکتا ہے۔",
                "Strategy choose karo sawaal se. Kitne log? Survey. Kyun? Interview. Kya waqai ho raha hai? Observation. Ek cheez badalni hai? Experiment. School register pehle se maujood? Document. Bias likhna mat bhoolna.",
                "For 'Do students skip breakfast?' pick a method and name one bias.",
                "کیا طلبہ ناشتہ چھوڑتے ہیں؟ طریقہ اور ایک تعصب لکھیں۔",
                listOf(
                    c("When is a sensor better than a survey?", "سینسر سروے سے کب بہتر؟",
                        "When you need automatic, repeated physical readings.",
                        "جب بار بار طبعی ریڈنگ چاہیے جو خود لکھی جائے۔")
                ),
                listOf("Match a method to a question", "Name one bias per method"),
                listOf("سوال سے طریقہ جوڑ سکتا/سکتی ہوں", "ہر طریقے کا ایک تعصب بتا سکتا/سکتی ہوں"),
                "diagrams/collection.png",
                listOf("booklet/v2_p39.jpg", "booklet/v2_p40.jpg")
            ),
            lesson(
                "6.4", "u6", "6.4",
                "Primary and secondary data", "بنیادی اور ثانوی ڈیٹا",
                "Primary aap collect; secondary kisi aur ne",
                "shared", "Booklet p. 41",
                listOf(w("primary data", "بنیادی ڈیٹا"), w("secondary data", "ثانوی ڈیٹا")),
                "Primary: you collect it for THIS inquiry. Secondary: someone else collected it. Wikipedia is often tertiary.",
                "بنیادی: اس انکوائری کے لیے آپ نے اکٹھا کیا۔ ثانوی: کسی اور نے۔ وکی پیڈیا اکثر تیسرے درجے۔",
                "Primary: class survey, soil sensor you placed, interview you ran. Secondary: textbook table, PBS census, news chart. Use both: secondary for context, primary for your original claim.",
                "بنیادی: جماعتی سروے، آپ کا سینسر۔ ثانوی: کتابی جدول، مردم شماری۔ دونوں استعمال کرو۔",
                "Simple test: kya MAIN ne is sawaal ke liye collect kiya? Haan to primary. Textbook table secondary. Wikipedia summary tertiary. Inquiry project mein primary zaroori hai warna aapki apni baat nahi.",
                "Label six sources as P, S or T (primary, secondary, tertiary).",
                "چھ مصادر پر پی، ایس یا ٹی لگائیں۔",
                listOf(
                    c("Is a census table primary for your project?", "مردم شماری آپ کے پروجیکٹ کی بنیادی؟",
                        "No — you did not collect it; it is secondary.",
                        "نہیں — آپ نے اکٹھا نہیں کیا؛ ثانوی ہے۔")
                ),
                listOf("Sort sources as primary/secondary/tertiary"),
                listOf("مصادر بنیادی/ثانوی/تیسرے میں چھانٹ سکتا/سکتی ہوں"),
                "diagrams/primary_secondary.png",
                listOf("booklet/v2_p41.jpg", "booklet/v2_p42.jpg")
            ),
            lesson(
                "6.5", "u6", "6.5",
                "Designing a data-collection approach", "اکٹھا کرنے کا منصوبہ",
                "Plan: ethics, sample, tools, consent",
                "shared", "Booklet p. 43",
                listOf(w("sample", "نمونہ"), w("consent", "رضامندی"), w("bias", "تعصب"), w("ethics", "اخلاق")),
                "Before you collect: question, who, how many, tool, consent, how you will store names.",
                "اکٹھا کرنے سے پہلے: سوال، کون، کتنے، اوزار، رضامندی، نام کیسے محفوظ۔",
                "A sample is the people or things you actually measure. Random is fairer than 'my friends only'. Consent: tell them why, let them refuse. Do not publish phone numbers. Pilot the questionnaire on two friends first.",
                "نمونہ وہ ہیں جنہیں آپ ناپتے ہیں۔ صرف دوستوں سے بہتر بے ترتیب۔ رضامندی، رازداری، پہلے دو دوستوں پر آزمائش۔",
                "Design likhe baghair collect mat karo. Sawal, sample, tool, consent, storage. Friends-only sample biased. Pilot se confusing sawal nikalte hain. Names code karo S1, S2.",
                "Write a one-page plan for a 15-student breakfast survey including consent wording.",
                "15 طلبہ ناشتہ سروے کا ایک صفحہ منصوبہ، رضامندی کے الفاظ سمیت۔",
                listOf(
                    c("Why pilot a questionnaire?", "سوالنامہ پہلے کیوں آزمائیں؟",
                        "To find confusing items before the real sample answers.",
                        "اصل نمونے سے پہلے الجھے سوال نکل آئیں۔")
                ),
                listOf("Write an ethical collection plan"),
                listOf("اخلاقی منصوبہ لکھ سکتا/سکتی ہوں"),
                "diagrams/collection.png",
                listOf("booklet/v2_p43.jpg", "booklet/v2_p44.jpg", "booklet/v2_p45.jpg")
            ),
            lesson(
                "6.6", "u6", "6.6",
                "Presenting data using digital tools", "ڈیجیٹل اوزاروں سے پیشکش",
                "Bar, pie, line, table, spreadsheet, slides",
                "shared", "Booklet p. 46",
                listOf(w("chart", "چارٹ"), w("spreadsheet", "اسپریڈ شیٹ"), w("slide", "سلائیڈ")),
                "Choose the chart that matches the story. Spreadsheet first, slides second. Title, axis labels, source.",
                "کہانی سے چارٹ چنو۔ پہلے شیٹ، پھر سلائیڈ۔ عنوان، محور، ماخذ۔",
                "Bar compares categories. Pie is parts of a whole (few slices). Line is change over time. A table holds exact values. Every chart needs a title, units and a source line. Do not 3-D explode a pie — it lies.",
                "بار موازنہ، پائی حصے، لائن وقت۔ جدول درست قدریں۔ عنوان، اکائی، ماخذ۔",
                "Tool chart se match: categories bar, share pie, time line. Spreadsheet sort, formula, chart. Slides story. 3D pie mat banana. Source line 'Class XI-A survey, 15 students' likho.",
                "Make one bar and one pie from the same 15-student table and say which tells the story better.",
                "ایک ہی جدول سے بار اور پائی بنائیں اور بہتر کہانی والا چنیں۔",
                listOf(
                    c("When is a pie a bad idea?", "پائی کب بری؟",
                        "When there are many tiny slices or you need exact values.",
                        "جب سلائسیں بہت ہوں یا درست قدریں درکار ہوں۔")
                ),
                listOf("Pick a chart type", "Label a chart fully"),
                listOf("چارٹ کی قسم چن سکتا/سکتی ہوں", "چارٹ مکمل لیبل کر سکتا/سکتی ہوں"),
                "diagrams/present.png",
                listOf("booklet/v2_p46.jpg", "booklet/v2_p47.jpg", "booklet/v2_p48.jpg")
            ),
            lesson(
                "6.7", "u6", "6.7",
                "Case study: the Digital Inquiry Project", "کیس: ڈیجیٹل انکوائری پروجیکٹ",
                "Poora inquiry cycle jo exam mein defend ho",
                "shared", "Booklet p. 49",
                listOf(w("inquiry", "انکوائری"), w("citation", "حوالہ"), w("reflection", "غور")),
                "Question → ethical plan → primary data → clean in a sheet → chart + comment → cite → present → reflect on bias.",
                "سوال ← اخلاقی منصوبہ ← بنیادی ڈیٹا ← شیٹ ← چارٹ+تبصرہ ← حوالہ ← پیش ← تعصب پر غور۔",
                "This is the capstone of Unit 6. You must be able to defend every step: why this question, why this sample, what bias remains, what the chart actually shows (not what you wish it showed).",
                "یہ یونٹ 6 کا تاج ہے۔ ہر قدم کا دفاع: سوال، نمونہ، باقی تعصب، چارٹ واقعی کیا دکھاتا ہے۔",
                "Project 8 steps: Question, Plan ethics, Collect primary, Clean, Chart plus comment, Cite, Present, Reflect. Comment mein sirf 'zyada hain' mat likho — number quote karo. Bias honestly likho. Yeh long question ka template hai.",
                "Fill the eight-step card for your own mini project and tick what is already done.",
                "اپنے منی پروجیکٹ کے آٹھ قدم بھریں اور ہو چکا وہ ٹک کریں۔",
                listOf(
                    c("Why reflect at the end?", "آخر میں غور کیوں؟",
                        "To admit bias, limits and what you would change next time.",
                        "تعصب، حد اور اگلی بار کیا بدلیں گے اعتراف کرنے کے لیے۔")
                ),
                listOf("Run a mini inquiry cycle", "Defend a chart in three sentences"),
                listOf("منی انکوائری چلا سکتا/سکتی ہوں", "چارٹ تین جملوں میں دفاع کر سکتا/سکتی ہوں"),
                "diagrams/inquiry.png",
                listOf("booklet/v2_p49.jpg", "booklet/v2_p50.jpg", "booklet/v2_p51.jpg")
            ),
            lesson(
                "6.R", "u6", "6.R",
                "Unit 6 revision and mock test", "یونٹ 6 اعادہ اور ماک ٹیسٹ",
                "Unit 6 revision aur mock test",
                "1 period", "Booklet p. 52",
                emptyList(),
                "Teach the inquiry cycle on a blank page, then sit the mock.",
                "خالی صفحے پر انکوائری چکر پڑھا کر ماک۔",
                "Literacy definition, four data types, six methods, P/S/T, ethics plan, chart choice, eight project steps.",
                "خواندگی، چار اقسام، چھ طریقے، پی/ایس/ٹی، اخلاقی منصوبہ، چارٹ، آٹھ قدم۔",
                "Zabani cycle, qualitative versus quantitative, primary test, pie kab nahi, project ke 8 steps. Phir Unit 6 quiz.",
                "Take the Unit 6 mock test.",
                "یونٹ 6 ماک ٹیسٹ حل کریں۔",
                listOf(c("Ready?", "تیار؟", "Open the Unit 6 quiz.", "کوئز کھولیں۔")),
                listOf("Defend a full inquiry without notes"),
                listOf("بغیر نوٹس پوری انکوائری دفاع کر سکتا/سکتی ہوں"),
                "diagrams/inquiry.png",
                listOf("booklet/v2_p49.jpg", "booklet/v2_p36.jpg"),
                isRevision = true
            )
        )
    )
}
