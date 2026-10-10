package com.sindhcs.crashcourse.data

import android.content.Context
import org.json.JSONArray
import org.json.JSONObject

object CourseRepository {

    private var cached: List<Course>? = null

    fun getCourses(context: Context): List<Course> {
        cached?.let { return it }
        val json = context.assets.open("course/course.json").bufferedReader().use { it.readText() }
        val root = JSONObject(json)
        val courses = root.getJSONArray("courses").mapObjects { it.toCourse() }
        cached = courses
        return courses
    }

    fun getCourse(context: Context, courseId: String): Course? =
        getCourses(context).find { it.id == courseId }

    fun getDay(context: Context, dayId: String): CourseDay? =
        getCourses(context).asSequence().flatMap { it.days.asSequence() }.find { it.id == dayId }

    fun getWelcomeScript(): String =
        "السلام علیکم۔ یہ {New Sindh Curriculum 2026} کا {Computer Science XI} اور {Computer Science XII} تیس دن کا {Crash Course} ہے۔ " +
            "ہر سبق کی اصل صفحات جوں کی توں دکھائی جاتی ہیں۔ لیکچر اردو میں سنایا جاتا ہے، اور امتحانی اصطلاحات انگریزی میں ویسی ہی رہتی ہیں جیسے صفحے پر لکھی ہیں، مثلاً {Algorithm}، {Logic Gates}، {SDLC} اور {Neural Networks}۔ " +
            "پہلے {Class XI} یا {Class XII} چنیں، دن کھولیں، صفحات دیکھیں، اور لیکچر سنیں۔ پیچھے رہو تو صرف ★ {Golden} کارڈز کرو، {Checkpoint} مت چھوڑو۔"

    fun getHowToDay(course: Course): CourseDay = CourseDay(
        id = "${course.id}-howto",
        courseId = course.id,
        day = 0,
        week = 0,
        kind = "How-to",
        chapter = course.title,
        focus = "How to run this 30-Day Crash Course",
        golden = "★ Golden first · 3 hours · no phone",
        startPage = course.introStartPage,
        endPage = course.introEndPage,
        topics = listOf(
            "Days 1–23 teach",
            "Checkpoint on last chapter day",
            "Days 24–26 Golden blitz",
            "Day 27 recaps",
            "Day 28 mock",
            "Day 29 mark",
            "Day 30 repair"
        ),
        script = course.introScript
    )

    private fun JSONObject.toCourse(): Course {
        val id = getString("id")
        val days = getJSONArray("days").mapObjects { obj ->
            CourseDay(
                id = obj.getString("id"),
                courseId = id,
                day = obj.getInt("day"),
                week = obj.getInt("week"),
                kind = obj.getString("kind"),
                chapter = obj.getString("chapter"),
                focus = obj.getString("focus"),
                golden = obj.getString("golden"),
                startPage = obj.getInt("startPage"),
                endPage = obj.getInt("endPage"),
                topics = obj.optJSONArray("topics")?.toStringList() ?: emptyList(),
                script = obj.getString("script")
            )
        }
        return Course(
            id = id,
            title = getString("title"),
            titleUr = getString("titleUr"),
            subtitle = getString("subtitle"),
            introStartPage = getInt("introStartPage"),
            introEndPage = getInt("introEndPage"),
            introScript = getString("introScript"),
            days = days
        )
    }

    private fun JSONArray.toStringList(): List<String> =
        (0 until length()).map { getString(it) }

    private fun JSONArray.mapObjects(transform: (JSONObject) -> CourseDay): List<CourseDay> =
        (0 until length()).map { transform(getJSONObject(it)) }
}
