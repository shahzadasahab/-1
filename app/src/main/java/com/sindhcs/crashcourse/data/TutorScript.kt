package com.sindhcs.crashcourse.data

/**
 * Academic tutoring scripts: spoken Urdu with English exam terms left as printed.
 * On-screen copy stays English; this object is for TTS only.
 */
enum class TutorPhase { FULL, RECAP, TEACH, DRILL, HOMEWORK }

data class LectureCue(
    val bookletPage: Int,
    val title: String,
    val script: String
)

object TutorScript {

    fun welcome(): String = join(
        "السلام علیکم۔ میں آپ کا {Computer Science} کا استاد ہوں۔ میری آواز مردانہ تدریسی آواز ہے، درمیانے درجے کے طلبہ کے لیے۔",
        "یہ {Teach Yourself} تیاری کا مواد ہے: {Class XI} اور {Class XII} کا تیس دن کا {Crash Course}، {New Sindh Curriculum 2026}، اساتذہ کے ایڈیشن کے کتابچوں سے۔",
        "ہر صفحے کی علامات، منطقی گیٹس، جدول، خاکے اور فارمولے ایپ کے اندر جوں کے توں شامل ہیں۔ سکین میری بات کے ساتھ خود کھلتی ہے۔ خاکہ دیکھیں اور کاپی میں نقل کریں۔",
        "میں اردو میں سمجھاؤں گا، مگر امتحانی اصطلاحات انگریزی میں ویسی ہی رہیں گی جیسے کتابچہ پر چھپی ہیں، مثلاً {Algorithm}، {Logic Gates}، {SDLC}، {Neural Networks} اور {MVP}۔ ان کا اردو ترجمہ نہ کیجیے گا۔",
        "ہر تدریسی دن تین گھنٹے کی نشست ہے: پہلے پندرہ منٹ کل کا ★ {Golden} کارڈ، پھر آج کے کارڈز، پھر {Closed-book drill}، آخر میں ایک پانچ نمبر کا جواب {Define}، {Explain}، {Example}، {Diagram}، {Working} سے۔",
        "{Class XI} یا {Class XII} کھولیں، دن چنیں، کتابچے کے صفحات جوں کے توں دیکھیں، اور استاد کی نشست سنیں۔",
        "پیچھے رہو تو صرف ★ {Golden} کارڈز کرو۔ {Checkpoint} مت چھوڑو۔"
    )

    fun cues(
        context: android.content.Context,
        course: Course,
        day: CourseDay,
        phase: TutorPhase
    ): List<LectureCue> {
        val pages = if (day.endPage >= day.startPage) {
            (day.startPage..day.endPage).toList()
        } else {
            listOf(day.startPage)
        }
        val first = pages.first()
        val last = pages.last()
        val allBlocks = dayBlocks(context, day)
        return when (phase) {
            TutorPhase.RECAP -> listOf(LectureCue(first, "Recap", recap(course, day)))
            TutorPhase.DRILL -> listOf(LectureCue(last, "Drill", drill(day, allBlocks)))
            TutorPhase.HOMEWORK -> listOf(LectureCue(last, "Homework", homework(day)))
            TutorPhase.TEACH -> buildList {
                if (day.day != 0 && day.script.isNotBlank()) {
                    add(LectureCue(first, "Teach", day.script))
                }
                pages.forEach { page ->
                    add(
                        LectureCue(
                            page,
                            "Booklet $page",
                            pageWalkthrough(page, day, PageRepository.getBlocks(context, page))
                        )
                    )
                }
            }
            TutorPhase.FULL -> buildList {
                val openingScript = if (day.day != 0 && day.script.isNotBlank()) {
                    join(opening(course, day), recap(course, day), teachLead(day), day.script)
                } else {
                    join(opening(course, day), recap(course, day), teachLead(day))
                }
                add(LectureCue(first, "Opening", openingScript))
                pages.forEach { page ->
                    add(
                        LectureCue(
                            page,
                            "Booklet $page",
                            pageWalkthrough(page, day, PageRepository.getBlocks(context, page))
                        )
                    )
                }
                add(LectureCue(last, "Close", join(drill(day, allBlocks), homework(day))))
            }
        }.filter { it.script.isNotBlank() }
    }

    fun session(context: android.content.Context, course: Course, day: CourseDay, phase: TutorPhase): String {
        val blocks = dayBlocks(context, day)
        return when (phase) {
            TutorPhase.RECAP -> recap(course, day)
            TutorPhase.TEACH -> teach(day)
            TutorPhase.DRILL -> drill(day, blocks)
            TutorPhase.HOMEWORK -> homework(day)
            TutorPhase.FULL -> join(
                opening(course, day),
                recap(course, day),
                teach(day),
                drill(day, blocks),
                homework(day)
            )
        }
    }

    fun pageWalkthrough(bookletPage: Int, day: CourseDay, blocks: List<PageBlock>): String {
        if (blocks.isEmpty()) return day.pageScript(bookletPage)
        val parts = ArrayList<String>()
        parts.add("اب ہم کتابچے کا صفحہ نمبر $bookletPage ساتھ پڑھتے ہیں۔ صفحہ جوں کا توں کھلا رکھیں۔")
        parts.add("میں اردو میں سمجھاؤں گا؛ چھپی ہوئی انگریزی اصطلاح اور جملے ویسے ہی پڑھوں گا جیسے صفحے پر لکھے ہیں۔")
        for (b in blocks) {
            val text = b.text.trim()
            if (text.isEmpty()) continue
            when (b.type) {
                "h" -> {
                    parts.add("اب نیا سیکشن ہے۔ عنوان یہ ہے: {$text}۔")
                    if (b.golden) {
                        parts.add("یہ ★ {Golden} موضوع ہے۔ تعریف زبانی یاد کریں، اردو میں نہ بدلیں۔")
                    }
                }
                "remember" -> parts.add("استاد کی تاکید۔ یاد رکھیں: {$text}")
                "exam" -> parts.add("امتحانی ہدایت۔ پیپر میں یوں آتا ہے: {$text}")
                "trap" -> parts.add("عام غلطی سے بچیں۔ {$text}")
                "q" -> parts.add("سوال سنتے ہیں۔ پہلے خود سوچیں۔ سوال۔ {$text}")
                "answers" -> parts.add("اب درست جواب سنتے ہیں۔ {$text}")
                "fig" -> parts.add(
                    "اس صفحے پر خاکہ، علامتیں اور شکل چھپی ہے۔ انہیں غور سے دیکھیں، کاپی میں نقل کریں، پھر بند کتاب دوبارہ بنائیں۔ عنوان: {$text}"
                )
                "cover" -> parts.add("آج کا احاطہ یہ ہے: {$text}")
                "lock" -> parts.add("★ یہ لازمی یاد ہو: {$text}")
                "box" -> parts.add(boxLabel(text))
                else -> if (wordCount(text) >= 3) {
                    parts.add("کتابچہ کہتا ہے: {$text}")
                }
            }
        }
        parts.add("اس صفحے کی اہم اصطلاحات انگریزی میں ویسی ہی لکھیں۔ اگلے صفحے پر تب جائیں جب یہ بات زبانی آ جائے۔")
        return join(*parts.toTypedArray())
    }

    fun lessonNotes(day: CourseDay): String {
        val cards = day.topics.joinToString("\n") { "• $it" }
        val kindNote = when (day.kind) {
            "Checkpoint" -> "Today is a timed Checkpoint. Closed book. Mark later; put weak Goldens on the Repair list."
            "Golden blitz" -> "Today is Golden blitz only. Recite each ★ Golden without notes."
            "Recap" -> "Today is recap. Teach the chapter back in five minutes, then closed-book questions."
            "Mock" -> "Today is the mock. Exam-hall conditions. No teaching."
            "Mark" -> "Today you mark against the key. Build the Repair list."
            "Repair" -> "Today you repair only the Day 29 list. No new chapter."
            "How-to" -> "This is the orientation for the 30-day tutoring method."
            else -> "Today is a teaching session. Stay with the 3-hour block."
        }
        return buildString {
            append("Tutoring session · Day ${day.day.toString().padStart(2, '0')} of 30 · ${day.kind}\n")
            append("Chapter: ${day.chapter}\n")
            append("Learning aim: ${day.focus}\n")
            append("★ Golden (must be spoken without notes): ${day.golden}\n")
            append("Booklet pages ${day.startPage}–${day.endPage} (as printed).\n\n")
            append("3-hour tutoring block\n")
            append("1. Recap (0–15 min) — yesterday’s Golden, closed book.\n")
            append("2. Teach (15–105 min) — today’s cards from the booklet.\n")
            append("3. Drill (105–135 min) — closed-book questions.\n")
            append("4. Homework (135–180 min) — one 5-mark answer: Define · Explain · Example · Diagram · Working.\n\n")
            append("Learning outcomes\n$cards\n\n")
            append("Exam rule: keep English terms exactly as printed. Do not translate them.\n")
            append(kindNote)
            if (day.displayText.isNotBlank()) {
                append("\n\n")
                append(day.displayText)
            }
        }
    }

    private fun opening(course: Course, day: CourseDay): String {
        val klass = classTerm(day.courseId)
        if (day.day == 0) {
            return join(
                "السلام علیکم۔ میں آپ کا {Computer Science} کا استاد ہوں۔",
                "آج ہم ${term(course.title)} کے تیس دن کے {Crash Course} کا طریقہ کار سمجھتے ہیں۔",
                "اصول یہ ہے: میں اردو میں سمجھاؤں گا؛ امتحانی اصطلاحات انگریزی میں ویسی ہی رہیں گی جیسے کتابچہ پر چھپی ہیں۔"
            )
        }
        return join(
            "السلام علیکم۔ میں آپ کا {Computer Science} کا استاد ہوں۔",
            "آج $klass کا دن ${day.day.toString().padStart(2, '0')} ہے، باب ${term(day.chapter)}۔",
            "آج کا تدریسی ہدف: ${term(day.focus)}۔",
            "آج کا ★ {Golden} کارڈ ${term(day.golden)} ہے۔ یہ تعریف زبانی، بغیر نوٹس، آنی چاہیے۔",
            "ایک اصول: امتحانی اصطلاحات انگریزی میں ویسی ہی بولیں اور لکھیں جیسے صفحے پر چھپی ہیں — ان کا اردو ترجمہ نہ بنائیں۔"
        )
    }

    private fun recap(course: Course, day: CourseDay): String {
        if (day.day == 0) {
            return join(
                "پہلا سبق طریقہ ہے، دہرائی نہیں۔",
                "یاد رکھیں: تین گھنٹے، ★ {Golden} پہلے، {Checkpoint} مت چھوڑو، فون دوسرے کمرے میں。"
            )
        }
        val previous = course.days.find { it.day == day.day - 1 }?.golden
        val first = if (previous.isNullOrBlank() || day.day == 1) {
            "یہ باب کا پہلا تدریسی دن ہے۔ کل کا کارڈ نہیں، اس لیے طریقہ زبانی یاد کریں: {Define}، {Explain}، {Example}، {Diagram}، {Working}۔"
        } else {
            "کل کا ★ {Golden} کارڈ ${term(previous)} بند کتاب کہیں۔ تعریف، ایک مثال، ایک امتحانی جملہ۔"
        }
        return join(
            "پہلا مرحلہ: پندرہ منٹ کی دہرائی۔ کتاب بند، نوٹس بند۔",
            first,
            "اگر تعریف نہ آئے تو صفحہ ایک بار کھول کر پڑھیں، پھر فوراً بند کتاب دہرائیں۔"
        )
    }

    private fun teachLead(day: CourseDay): String {
        val cards = day.topics.joinToString("، ") { term(it) }.ifBlank { term(day.focus) }
        return when (day.kind) {
            "Checkpoint" -> "آج تدریس مختصر ہے کیونکہ آگے {Checkpoint} ہے۔ صفحات کے ساتھ چلتے ہیں۔"
            "Golden blitz" -> "آج نیا سبق نہیں۔ صفحات پر ★ {Golden} کارڈز دیکھیں گے۔"
            "Recap", "Mock", "Mark", "Repair", "How-to" -> "اب کتابچے کے صفحات کے ساتھ چلتے ہیں۔"
            else -> join(
                "دوسرا مرحلہ: تدریس۔ میں صفحہ بہ صفحہ سکین کھولوں گا، آپ چھپی ہوئی بات دیکھیں۔",
                "ہر صفحے کی علامات، جدول اور خاکے ایپ میں جوں کے توں شامل ہیں۔ صرف سننا کافی نہیں — خاکہ دیکھیں اور نقل کریں۔",
                "آج کے کارڈز: $cards۔"
            )
        }
    }

    private fun teach(day: CourseDay): String {
        val cards = day.topics.joinToString("، ") { term(it) }.ifBlank { term(day.focus) }
        val lead = when (day.kind) {
            "Checkpoint" -> "آج تدریس مختصر ہے کیونکہ آگے {Checkpoint} ہے۔ کمزور جگہ ایک بار دیکھ لیں، پھر کتاب بند۔"
            "Golden blitz" -> "آج نیا سبق نہیں۔ صرف ★ {Golden} کارڈز۔ میں ترتیب سے پڑھاؤں گا، آپ بند کتاب دہرائیں گے۔"
            "Recap" -> "آج {Recap} ہے۔ باب واپس سکھائیں، نوٹس سے نہ پڑھیں۔"
            "Mock" -> "آج {Mock} ہے۔ میں ہدایت دیتا ہوں، سبق نہیں پڑھاتا۔ ہال کے حالات رکھیں۔"
            "Mark" -> "آج نمبر لگائیں گے۔ کلید سے میل کھائیں، اندازے سے نہیں۔"
            "Repair" -> "آج صرف {Repair}۔ نیا {Chapter} نہیں۔"
            "How-to" -> "اب طریقہ کار سنتے ہیں۔"
            else -> join(
                "دوسرا مرحلہ: تدریس۔ کتابچے کے صفحات ${day.startPage} سے ${day.endPage} کھولیں۔ میرے ساتھ سمجھیں، صرف دیکھیں نہیں۔",
                "آج کے کارڈز: $cards۔"
            )
        }
        return join(
            lead,
            day.script,
            "ہر کارڈ کے بعد رکیں: کیا تعریف زبانی آتی ہے؟ ایک مثال بنتی ہے؟ پیپر میں انگریزی اصطلاح ویسی ہی لکھی جائے گی؟"
        )
    }

    private fun drill(day: CourseDay, blocks: List<PageBlock>): String {
        if (day.kind in setOf("Mock", "Mark", "Repair", "How-to")) {
            return when (day.kind) {
                "Mock" -> "مشق کی جگہ آج {Mock} پیپر حل کریں۔ وقت رکھیں، صفحہ نہ دیکھیں۔"
                "Mark" -> "مشق کی جگہ آج کلید سے میل کھائیں۔ ہر کمزور ★ {Golden} {Repair list} میں لکھیں۔"
                "Repair" -> "مشق یہی ہے: {Repair list} کی ہر تعریف بند کتاب کہیں، پھر جدول یا {Trace Table} کھینچیں۔"
                else -> "اب کتابچے کے تعارفی صفحات دیکھیں اور طریقہ ایک بار زبانی دہرائیں۔"
            }
        }
        val questions = blocks.filter { it.type == "q" && it.text.isNotBlank() }
        val answers = blocks.filter { it.type == "answers" && it.text.isNotBlank() }
        val parts = ArrayList<String>()
        parts.add("تیسرا مرحلہ: {Closed-book drill}۔ کتاب بند کریں، فون دور رکھیں۔")
        parts.add("میں سوال پڑھتا ہوں۔ آپ زبانی جواب دیں، پھر درست جواب سنیں۔")
        if (questions.isEmpty()) {
            val cards = day.topics.joinToString("، ") { term(it) }
            parts.add("آج کے کارڈز بند کتاب دہرائیں: $cards۔")
            parts.add("★ {Golden} کارڈ ${term(day.golden)} کی تعریف بغیر دیکھے کہیں۔")
        } else {
            questions.forEach { parts.add("سوال۔ ${term(it.text)} سوچنے کے لیے ایک لمحہ لیں۔") }
        }
        answers.forEach { parts.add("اب درست جوابات۔ ${term(it.text)}") }
        return join(*parts.toTypedArray())
    }

    private fun homework(day: CourseDay): String = when (day.kind) {
        "Checkpoint" -> join(
            "آج {Checkpoint} ہے۔ وقت مقرر رکھیں۔ کتاب بند۔",
            "جتنے نمبر بنیں لکھیں۔ کمزور ★ {Golden} کارڈ بعد میں {Repair list} میں جائیں گے۔",
            "نیا باب اس وقت تک نہ کھولیں جب تک اس باب کی {Golden} تعریف زبانی نہ آئے۔ اللہ حافظ۔"
        )
        "Golden blitz" -> join(
            "آج رات نیا پانچ نمبر نہیں۔ صرف وہ ★ {Golden} کارڈز دہرائیں جو زبان پر نہ آئے۔",
            "کل پھر بند کتاب۔ اللہ حافظ۔"
        )
        "Recap" -> join(
            "آج رات باب کو پانچ منٹ میں واپس سکھائیں۔ اصطلاحات انگریزی میں رہیں۔ اللہ حافظ۔"
        )
        "Mock" -> join(
            "کاپی جمع۔ آج سبق بند۔ کل کلید سے نمبر۔ اللہ حافظ۔"
        )
        "Mark" -> join(
            "رات تک {Repair list} مکمل ہو۔ کل صرف یہی فہرست۔ اللہ حافظ۔"
        )
        "Repair" -> join(
            "شام کو رک جائیں۔ دس بجے سوئیں۔ نیا {Chapter} نہیں۔ ★ {Golden} کارڈز سر میں رہیں، ہال میں کتاب نہیں۔ اللہ حافظ۔"
        )
        "How-to" -> join(
            "اب پہلا تدریسی دن کھولیں۔ فون دوسرے کمرے میں رکھیں۔ صفحات جوں کے توں۔ اللہ حافظ۔"
        )
        else -> join(
            "چوتھا مرحلہ: آج رات کا پانچ نمبر کا کام۔ موضوع: ${term(day.golden)}۔",
            "طریقہ لازمی ہے: {Define}، {Explain}، {Example}، {Diagram}، {Working}۔",
            "کل صبح پہلے پندرہ منٹ میں یہی جواب بغیر نوٹس پڑھنا ہے۔",
            "نیا باب اس وقت تک نہ کھولیں جب تک آج کا ★ {Golden} کارڈ زبانی نہ آئے۔",
            "اللہ حافظ۔ اگلی نشست میں حاضر رہیں۔"
        )
    }

    private fun dayBlocks(context: android.content.Context, day: CourseDay): List<PageBlock> {
        if (day.startPage <= 0 || day.endPage < day.startPage) return emptyList()
        return (day.startPage..day.endPage).flatMap { PageRepository.getBlocks(context, it) }
    }

    private fun boxLabel(text: String): String = when (text.lowercase()) {
        "closed-book drill" -> "اب {Closed-book drill} شروع کرتے ہیں۔ کتاب بند۔"
        "tonight's 5-mark" -> "اب آج رات کا پانچ نمبر کا کام دیکھیں۔ طریقہ {Define}، {Explain}، {Example}، {Diagram}، {Working}۔"
        "checkpoint test" -> "اب {Checkpoint} کی ہدایت۔ وقت رکھیں، صفحہ نہ دیکھیں۔"
        "today's 3 hours" -> "آج کی تین گھنٹے کی تدریسی نشست کا ڈھانچہ یہ ہے۔"
        else -> "اب ${term(text)}۔"
    }

    private fun classTerm(courseId: String): String =
        if (courseId == "xii") "{Class XII}" else "{Class XI}"

    private fun term(text: String): String = "{${text.trim()}}"

    private fun wordCount(text: String): Int = text.split(' ').count { it.isNotBlank() }

    private fun join(vararg parts: String): String =
        parts.map { it.trim() }.filter { it.isNotEmpty() }.joinToString(" ")
}
