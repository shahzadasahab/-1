package com.csxi.ultimatecoaching

import android.content.Intent
import android.os.Bundle
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import androidx.recyclerview.widget.LinearLayoutManager
import com.csxi.ultimatecoaching.data.Curriculum
import com.csxi.ultimatecoaching.databinding.ActivityUnitBinding
import com.csxi.ultimatecoaching.ui.LessonAdapter
import com.csxi.ultimatecoaching.util.AssetImages
import com.csxi.ultimatecoaching.util.LocaleHelper
import com.csxi.ultimatecoaching.util.ProgressStore

class UnitActivity : AppCompatActivity() {

    private lateinit var binding: ActivityUnitBinding
    private lateinit var progress: ProgressStore

    override fun attachBaseContext(newBase: android.content.Context) {
        super.attachBaseContext(LocaleHelper.wrap(newBase))
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        binding = ActivityUnitBinding.inflate(layoutInflater)
        setContentView(binding.root)
        progress = ProgressStore(this)
        val language = LocaleHelper.getLanguage(this)
        val unit = Curriculum.unit(intent.getStringExtra(EXTRA_UNIT_ID) ?: "")
        if (unit == null) {
            Toast.makeText(this, R.string.missing_unit, Toast.LENGTH_SHORT).show()
            finish()
            return
        }
        setSupportActionBar(binding.toolbar)
        supportActionBar?.setDisplayHomeAsUpEnabled(true)
        val title = when (language) {
            LocaleHelper.LANG_UR -> unit.titleUr
            LocaleHelper.LANG_URDISH -> unit.titleUrdish
            else -> unit.titleEn
        }
        supportActionBar?.title = "Unit ${unit.number}"
        binding.unitHeading.text = title
        binding.unitSummary.text = if (language == LocaleHelper.LANG_UR) unit.summaryUr else unit.summaryEn
        binding.unitMeta.text = unit.weeks
        AssetImages.load(this, binding.unitImage, unit.coverDiagram)

        val adapter = LessonAdapter(language, progress) { lesson ->
            startActivity(
                Intent(this, LessonActivity::class.java)
                    .putExtra(LessonActivity.EXTRA_LESSON_ID, lesson.id)
            )
        }
        binding.lessonList.layoutManager = LinearLayoutManager(this)
        binding.lessonList.adapter = adapter
        binding.lessonList.isNestedScrollingEnabled = false
        adapter.submit(unit.lessons)

        binding.btnQuiz.setOnClickListener {
            startActivity(
                Intent(this, QuizActivity::class.java)
                    .putExtra(QuizActivity.EXTRA_UNIT_ID, unit.id)
            )
        }
    }

    override fun onResume() {
        super.onResume()
        val unit = Curriculum.unit(intent.getStringExtra(EXTRA_UNIT_ID) ?: "") ?: return
        (binding.lessonList.adapter as? LessonAdapter)?.submit(unit.lessons)
        val done = progress.completedCount(unit.lessons.map { it.id })
        binding.unitProgress.text = getString(R.string.progress_line, done, unit.lessons.size)
    }

    override fun onSupportNavigateUp(): Boolean {
        finish()
        return true
    }

    companion object {
        const val EXTRA_UNIT_ID = "unit_id"
    }
}
