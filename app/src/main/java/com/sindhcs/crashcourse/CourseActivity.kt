package com.sindhcs.crashcourse

import android.content.Intent
import android.os.Bundle
import android.view.View
import androidx.appcompat.app.AppCompatActivity
import androidx.recyclerview.widget.LinearLayoutManager
import com.sindhcs.crashcourse.data.Course
import com.sindhcs.crashcourse.data.CourseDay
import com.sindhcs.crashcourse.data.CourseRepository
import com.sindhcs.crashcourse.databinding.ActivityCourseBinding
import com.sindhcs.crashcourse.ui.DayAdapter
import com.sindhcs.crashcourse.util.LocaleHelper

class CourseActivity : AppCompatActivity() {

    companion object {
        const val EXTRA_COURSE_ID = "course_id"
    }

    private lateinit var binding: ActivityCourseBinding
    private lateinit var course: Course
    private lateinit var adapter: DayAdapter
    private var filter = "all"

    override fun attachBaseContext(newBase: android.content.Context) {
        super.attachBaseContext(LocaleHelper.wrap(newBase))
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        binding = ActivityCourseBinding.inflate(layoutInflater)
        setContentView(binding.root)

        val courseId = intent.getStringExtra(EXTRA_COURSE_ID) ?: "xi"
        course = CourseRepository.getCourse(this, courseId) ?: run {
            finish()
            return
        }

        setSupportActionBar(binding.toolbar)
        supportActionBar?.setDisplayHomeAsUpEnabled(true)
        supportActionBar?.title = course.title

        adapter = DayAdapter { day ->
            startActivity(Intent(this, DayActivity::class.java).apply {
                putExtra(DayActivity.EXTRA_DAY_ID, day.id)
                putExtra(DayActivity.EXTRA_COURSE_ID, course.id)
            })
        }
        binding.dayList.layoutManager = LinearLayoutManager(this)
        binding.dayList.adapter = adapter

        binding.filterGroup.setOnCheckedStateChangeListener { _, _ ->
            filter = when (binding.filterGroup.checkedChipId) {
                R.id.filterTeach -> "Teach"
                R.id.filterCheckpoint -> "Checkpoint"
                R.id.filterRevision -> "revision"
                else -> "all"
            }
            render()
        }
    }

    override fun onResume() {
        super.onResume()
        render()
    }

    private fun render() {
        val howTo = CourseRepository.getHowToDay(course)
        val filtered = buildList {
            if (filter == "all") add(howTo)
            addAll(course.days.filter { matches(it) })
        }
        adapter.submit(filtered)
        binding.emptyText.visibility = if (filtered.isEmpty()) View.VISIBLE else View.GONE
    }

    private fun matches(day: CourseDay): Boolean = when (filter) {
        "all" -> true
        "Teach" -> day.kind == "Teach"
        "Checkpoint" -> day.kind == "Checkpoint"
        "revision" -> day.isRevision()
        else -> true
    }

    override fun onSupportNavigateUp(): Boolean {
        finish()
        return true
    }
}
