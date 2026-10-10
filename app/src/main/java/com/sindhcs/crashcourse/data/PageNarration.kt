package com.sindhcs.crashcourse.data

/**
 * Builds narration for one booklet page from its printed English text.
 * Urdu is used only as connective framing; printed English sentences are spoken as-is
 * through the {term} mechanism of MixedVoiceNarrator.
 */
object PageNarration {

    private const val MIN_WORDS = 3

    private val BOX_LABELS = mapOf(
        "closed-book drill" to "بند کتاب مشق",
        "tonight's 5-mark" to "آج رات کا پانچ نمبر کا کام",
        "checkpoint test" to "چیک پوائنٹ ٹیسٹ",
        "today's 3 hours" to "آج کے تین گھنٹے"
    )

    fun script(bookletPage: Int, blocks: List<PageBlock>): String {
        val parts = ArrayList<String>()
        parts.add("یہ کتابچہ کا صفحہ نمبر $bookletPage ہے۔")
        for (b in blocks) {
            val text = b.text.trim()
            if (text.isEmpty()) continue
            when (b.type) {
                "h" -> {
                    parts.add("سیکشن {$text}۔")
                    if (b.golden) parts.add("یہ ★ {Golden} موضوع ہے۔")
                }
                "remember" -> parts.add("یاد رکھیں۔ {$text}")
                "exam" -> parts.add("امتحان میں۔ {$text}")
                "trap" -> parts.add("جال سے بچیں۔ {$text}")
                "q" -> parts.add("سوال۔ {$text}")
                "answers" -> parts.add("جوابات۔ {$text}")
                "cover" -> parts.add("آج کا احاطہ۔ {$text}")
                "lock" -> parts.add("★ لازمی یاد کریں۔ {$text}")
                "box" -> {
                    val label = BOX_LABELS[text.lowercase()]
                    parts.add(if (label != null) "$label۔" else "{$text}۔")
                }
                else -> if (wordCount(text) >= MIN_WORDS) parts.add("{$text}")
            }
        }
        return parts.joinToString(" ")
    }

    fun displayText(blocks: List<PageBlock>): String {
        if (blocks.isEmpty()) return ""
        val sb = StringBuilder()
        for (b in blocks) {
            val text = b.text.trim()
            if (text.isEmpty()) continue
            when (b.type) {
                "h" -> sb.append("\n").append(if (b.golden) "★ " else "").append(text).append("\n")
                "remember" -> sb.append("Remember: ").append(text).append("\n")
                "exam" -> sb.append("Exam: ").append(text).append("\n")
                "trap" -> sb.append("Trap: ").append(text).append("\n")
                "answers" -> sb.append("Answers: ").append(text).append("\n")
                "cover" -> sb.append("Today covers: ").append(text).append("\n")
                "lock" -> sb.append("★ Lock in: ").append(text).append("\n")
                "box" -> sb.append("\n[").append(text).append("]\n")
                else -> sb.append(text).append("\n")
            }
        }
        return sb.toString().trim()
    }

    private fun wordCount(text: String): Int = text.split(' ').count { it.isNotBlank() }
}
