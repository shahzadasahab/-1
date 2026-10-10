package com.sindhcs.crashcourse.data

import android.content.Context

object ProgressStore {
    private const val PREFS = "cs_crash_progress"

    fun isDone(context: Context, dayId: String): Boolean =
        prefs(context).getBoolean(dayId, false)

    fun setDone(context: Context, dayId: String, done: Boolean) {
        prefs(context).edit().putBoolean(dayId, done).apply()
    }

    fun completedCount(context: Context, course: Course): Int =
        course.days.count { isDone(context, it.id) }

    private fun prefs(context: Context) =
        context.getSharedPreferences(PREFS, Context.MODE_PRIVATE)
}
