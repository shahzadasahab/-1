package com.sindhcs.crashcourse.data

/**
 * English on-screen text for a booklet page, plus a short spoken fallback.
 * Preferred spoken walkthrough is TutorScript.pageWalkthrough.
 */
object PageNarration {

    fun script(
        context: android.content.Context,
        bookletPage: Int,
        day: CourseDay,
        blocks: List<PageBlock>
    ): String = TutorScript.pageWalkthrough(context, bookletPage, day, blocks)

    fun displayText(blocks: List<PageBlock>): String {
        if (blocks.isEmpty()) return ""
        val sb = StringBuilder()
        for (b in blocks) {
            val text = b.text.trim()
            if (text.isEmpty()) continue
            when (b.type) {
                "h" -> sb.append("\n").append(if (b.golden) "★ " else "").append(text).append("\n")
                "remember" -> sb.append("Tutor note: ").append(text).append("\n")
                "exam" -> sb.append("Exam cue: ").append(text).append("\n")
                "trap" -> sb.append("Common error: ").append(text).append("\n")
                "answers" -> sb.append("Answers: ").append(text).append("\n")
                "cover" -> sb.append("Today covers: ").append(text).append("\n")
                "lock" -> sb.append("★ Lock in: ").append(text).append("\n")
                "box" -> sb.append("\n[").append(text).append("]\n")
                else -> sb.append(text).append("\n")
            }
        }
        return sb.toString().trim()
    }
}
