package com.csxi.ultimatecoaching.data

object Glossary {

    fun all(): List<GlossaryEntry> = listOf(
        e("Analog", "Continuous values in a range.", "حد میں مسلسل قدریں۔", "Range mein koi bhi value — sine wave.", "u1"),
        e("Digital", "Only discrete levels, usually 0 and 1.", "صرف منقطع سطحیں، عموماً 0 اور 1۔", "Sirf 0 aur 1.", "u1"),
        e("Bit", "A single 0 or 1. Eight bits make a byte.", "ایک 0 یا 1۔ آٹھ بٹس = بائٹ۔", "Bit byte nahi hota.", "u1"),
        e("Logic gate", "Circuit with one output from Boolean inputs.", "بولین ان پٹ سے ایک آؤٹ پٹ والا سرکٹ۔", "AND OR NOT family.", "u1"),
        e("Truth table", "Every input combo and the output.", "ہر ان پٹ امتزاج اور آؤٹ پٹ۔", "n inputs, 2 to the n rows.", "u1"),
        e("SDLC", "Structured software life cycle of six phases.", "سافٹ ویئر کے چھ منظم مراحل۔", "Require Design Code Test Deploy Maintain.", "u1"),
        e("Waterfall", "One-way phases; testing comes late.", "ایک طرفہ مراحل؛ جانچ دیر سے۔", "Fixed requirements — Al-Noor.", "u1"),
        e("Agile", "Short sprints that deliver working software.", "مختصر سپرنٹ، کام کرتا سافٹ ویئر۔", "2 se 4 weeks, documented iterative.", "u1"),
        e("OSI", "ISO 1984 seven-layer teaching model.", "1984 کا سات تہہ ماڈل۔", "Please Do Not Throw Sausage Pizza Away.", "u1"),
        e("Encapsulation", "Each layer adds a header going down.", "نیچے جاتے ہوئے ہیڈر جوڑنا۔", "Data, segment, packet, frame, bits.", "u1"),
        e("Algorithm", "Finite definite effective steps with I/O.", "محدود واضح موثر قدم، ان پٹ آؤٹ پٹ۔", "Pehle pseudocode.", "u2"),
        e("Decomposition", "Split a big problem into parts.", "بڑا مسئلہ ٹکڑوں میں۔", "Library = member + borrow + fine.", "u2"),
        e("Abstraction", "Keep relevant detail, hide the rest.", "اصل رکھو، شور چھپاو۔", "Desk colour drop, MemberID keep.", "u2"),
        e("Bubble sort", "Swap neighbours; largest bubbles to the end.", "پڑوسی ادلا بدلی؛ سب سے بڑا آخر میں۔", "Pass by pass trace.", "u2"),
        e("Binary search", "Halve a SORTED list using mid.", "ترتیب شدہ فہرست آدھی، مڈ سے۔", "Unsorted par mat chalana.", "u2"),
        e("Variable", "A named box that holds a value.", "نام والا ڈبہ۔", "Rules: letter or _, no space.", "u3"),
        e("input()", "Always returns a string in Python.", "پائتھن میں ہمیشہ سٹرنگ۔", "int(input()) for numbers.", "u3"),
        e("==", "Compares two values; result is True/False.", "موازنہ؛ نتیجہ درست/غلط۔", "Single = assigns.", "u3"),
        e("for / while", "Known count versus wait-for-condition.", "معلوم گنتی بمقابلہ شرط کا انتظار۔", "Update bhoolna = infinite.", "u3"),
        e("Primary key", "Unique, not null, one per table.", "منفرد، خالی نہیں، ایک فی ٹیبل۔", "Roll in Student.", "u4"),
        e("Foreign key", "Points at another table's primary key.", "دوسری ٹیبل کی پرائمری کی۔", "Must exist or be NULL.", "u4"),
        e("ER model", "Entities, relationships, attributes.", "وجود، تعلق، صفات۔", "Rectangle, diamond, oval.", "u4"),
        e("Referential integrity", "No orphan foreign keys.", "یتیم فارن کی نہیں۔", "Delete parent only after children.", "u4"),
        e("Form", "Friendly screen for enter/edit/view.", "اندراج/ترمیمی اسکرین۔", "Columnar for data entry.", "u4"),
        e("Query", "Retrieves without changing tables.", "ٹیبل بدلے بغیر نکالتی ہے۔", "AND same row, OR extra row.", "u4"),
        e("IoT", "Internet-connected devices that act on data.", "انٹرنیٹ سے جڑے آلات۔", "See Act Carry Decide Keep Show.", "u5"),
        e("Sensor", "Collects from the physical world (input).", "مادی دنیا سے معلومات (ان پٹ)۔", "Temperature, soil, motion.", "u5"),
        e("Actuator", "Performs a physical action (output).", "حکم پر طبعی عمل (آؤٹ پٹ)۔", "Motor, valve, lamp.", "u5"),
        e("AI", "Learns from data and decides.", "ڈیٹا سے سیکھ کر فیصلہ۔", "Not the same as IoT or analytics.", "u5"),
        e("Assistive technology", "Computing that removes a barrier.", "رکاوٹ ہٹانے والی کمپیوٹنگ۔", "Screen reader, captions, alt text.", "u5"),
        e("Digital literacy", "Find, judge, use, share data ethically.", "ڈھونڈو، جانچو، استعمال، اخلاقی شیئر۔", "Inquiry cycle.", "u6"),
        e("Primary data", "You collected it for this inquiry.", "اس انکوائری کے لیے آپ نے اکٹھا کیا۔", "Class survey, your sensor.", "u6"),
        e("Secondary data", "Someone else collected it.", "کسی اور نے اکٹھا کیا۔", "Census, textbook table.", "u6"),
        e("Qualitative", "Words, labels, opinions.", "الفاظ، لیبل، رائے۔", "Blood group, favourite subject.", "u6")
    )

    private fun e(term: String, en: String, ur: String, urdish: String, unitId: String) =
        GlossaryEntry(term, en, ur, urdish, unitId)
}
