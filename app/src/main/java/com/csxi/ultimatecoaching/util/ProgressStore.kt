package com.csxi.ultimatecoaching.util

import android.content.Context

class ProgressStore(context: Context) {

    private val prefs = context.applicationContext.getSharedPreferences(PREFS, Context.MODE_PRIVATE)

    fun isLessonDone(lessonId: String): Boolean = prefs.getBoolean(doneKey(lessonId), false)

    fun setLessonDone(lessonId: String, done: Boolean = true) {
        prefs.edit().putBoolean(doneKey(lessonId), done).apply()
    }

    fun isICanTicked(lessonId: String, index: Int): Boolean =
        prefs.getBoolean(icanKey(lessonId, index), false)

    fun setICanTicked(lessonId: String, index: Int, ticked: Boolean) {
        prefs.edit().putBoolean(icanKey(lessonId, index), ticked).apply()
    }

    fun quizScore(unitId: String): Int = prefs.getInt(scoreKey(unitId), -1)

    fun setQuizScore(unitId: String, score: Int, total: Int) {
        prefs.edit()
            .putInt(scoreKey(unitId), score)
            .putInt(totalKey(unitId), total)
            .apply()
    }

    fun quizTotal(unitId: String): Int = prefs.getInt(totalKey(unitId), 0)

    fun completedCount(lessonIds: Collection<String>): Int =
        lessonIds.count { isLessonDone(it) }

    companion object {
        private const val PREFS = "csxi_progress"
        private fun doneKey(id: String) = "done_$id"
        private fun icanKey(id: String, i: Int) = "ican_${id}_$i"
        private fun scoreKey(id: String) = "score_$id"
        private fun totalKey(id: String) = "total_$id"
    }
}
