package com.sindhcs.crashcourse.data

data class Course(
    val id: String,
    val title: String,
    val titleUr: String,
    val subtitle: String,
    val introStartPage: Int,
    val introEndPage: Int,
    val introScript: String,
    val days: List<CourseDay>
)

data class CourseDay(
    val id: String,
    val courseId: String,
    val day: Int,
    val week: Int,
    val kind: String,
    val chapter: String,
    val focus: String,
    val golden: String,
    val startPage: Int,
    val endPage: Int,
    val topics: List<String>,
    val script: String
) {
    val pageCount: Int get() = endPage - startPage + 1

    fun bookletPage(index: Int): Int = startPage + index

    fun pageScript(bookletPage: Int): String {
        val topicsLine = topics.joinToString("، ") { "{$it}" }
        return "یہ کتابچہ کا صفحہ {$bookletPage} ہے، {$chapter}، $focus۔ " +
            "صفحہ جوں کا توں دیکھیں۔ آج کے کارڈز: $topicsLine۔ " +
            "★ Golden موضوع {$golden} ہے۔ اصطلاحات انگریزی میں ویسی ہی بولی جائیں گی جیسے صفحے پر لکھی ہیں۔"
    }

    fun isRevision(): Boolean = kind in REVISION_KINDS

    companion object {
        val REVISION_KINDS = setOf("Golden blitz", "Recap", "Mock", "Mark", "Repair", "How-to")
    }
}
