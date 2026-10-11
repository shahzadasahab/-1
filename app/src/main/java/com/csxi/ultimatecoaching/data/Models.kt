package com.csxi.ultimatecoaching.data

data class WordItem(
    val en: String,
    val ur: String
)

data class CheckItem(
    val questionEn: String,
    val questionUr: String,
    val answerEn: String,
    val answerUr: String
)

data class QuizQuestion(
    val id: String,
    val unitId: String,
    val promptEn: String,
    val promptUr: String,
    val promptUrdish: String,
    val optionsEn: List<String>,
    val optionsUr: List<String>,
    val correctIndex: Int,
    val explainEn: String,
    val explainUr: String
)

data class GlossaryEntry(
    val term: String,
    val en: String,
    val ur: String,
    val urdish: String,
    val unitId: String
)

data class Lesson(
    val id: String,
    val unitId: String,
    val code: String,
    val titleEn: String,
    val titleUr: String,
    val titleUrdish: String,
    val periods: String,
    val textbook: String,
    val words: List<WordItem>,
    val keyIdeaEn: String,
    val keyIdeaUr: String,
    val learnEn: String,
    val learnUr: String,
    val coachUrdish: String,
    val tryItEn: String,
    val tryItUr: String,
    val checks: List<CheckItem>,
    val iCanEn: List<String>,
    val iCanUr: List<String>,
    val diagram: String,
    val bookletPages: List<String>,
    val isRevision: Boolean = false
)

data class CourseUnit(
    val id: String,
    val number: Int,
    val titleEn: String,
    val titleUr: String,
    val titleUrdish: String,
    val weeks: String,
    val colorHex: String,
    val coverDiagram: String,
    val summaryEn: String,
    val summaryUr: String,
    val lessons: List<Lesson>
)
