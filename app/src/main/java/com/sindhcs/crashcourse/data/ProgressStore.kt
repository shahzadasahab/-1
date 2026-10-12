package com.sindhcs.crashcourse.data

import android.content.Context

object ProgressStore {
    private const val PREFS = "cs_crash_progress"
    private const val KEY_LAST_DAY = "_last_day"
    private const val KEY_RATE = "_speech_rate"

    fun isDone(context: Context, dayId: String): Boolean =
        prefs(context).getBoolean(dayId, false)

    fun setDone(context: Context, dayId: String, done: Boolean) {
        prefs(context).edit().putBoolean(dayId, done).apply()
    }

    fun completedCount(context: Context, course: Course): Int =
        course.days.count { isDone(context, it.id) }

    fun setLastOpened(context: Context, dayId: String) {
        prefs(context).edit().putString(KEY_LAST_DAY, dayId).apply()
    }

    fun lastOpened(context: Context): String? = prefs(context).getString(KEY_LAST_DAY, null)

    fun speechRate(context: Context): Float = prefs(context).getFloat(KEY_RATE, 1.0f)

    fun setSpeechRate(context: Context, rate: Float) {
        prefs(context).edit().putFloat(KEY_RATE, rate).apply()
    }

    private fun prefs(context: Context) =
        context.getSharedPreferences(PREFS, Context.MODE_PRIVATE)
}
