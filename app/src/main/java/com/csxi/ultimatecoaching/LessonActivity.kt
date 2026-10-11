package com.csxi.ultimatecoaching

import android.content.Intent
import android.os.Bundle
import android.view.LayoutInflater
import android.view.Menu
import android.view.MenuItem
import android.widget.CheckBox
import android.widget.LinearLayout
import android.widget.TextView
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import androidx.core.content.ContextCompat
import com.csxi.ultimatecoaching.data.Curriculum
import com.csxi.ultimatecoaching.data.Lesson
import com.csxi.ultimatecoaching.databinding.ActivityLessonBinding
import com.csxi.ultimatecoaching.databinding.ItemDiagramBinding
import com.csxi.ultimatecoaching.util.AssetImages
import com.csxi.ultimatecoaching.util.LocaleHelper
import com.csxi.ultimatecoaching.util.ProgressStore
import com.csxi.ultimatecoaching.util.VoiceNarrator
import com.google.android.material.chip.Chip

class LessonActivity : AppCompatActivity() {

    private lateinit var binding: ActivityLessonBinding
    private lateinit var progress: ProgressStore
    private lateinit var lesson: Lesson
    private var language = LocaleHelper.LANG_URDISH
    private var voice: VoiceNarrator? = null
    private var voiceReady = false
    private var speaking = false

    override fun attachBaseContext(newBase: android.content.Context) {
        super.attachBaseContext(LocaleHelper.wrap(newBase))
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        binding = ActivityLessonBinding.inflate(layoutInflater)
        setContentView(binding.root)
        language = LocaleHelper.getLanguage(this)
        progress = ProgressStore(this)
        val found = Curriculum.lesson(intent.getStringExtra(EXTRA_LESSON_ID) ?: "")
        if (found == null) {
            Toast.makeText(this, R.string.missing_lesson, Toast.LENGTH_SHORT).show()
            finish()
            return
        }
        lesson = found
        setSupportActionBar(binding.toolbar)
        supportActionBar?.setDisplayHomeAsUpEnabled(true)
        supportActionBar?.title = lesson.code

        voice = VoiceNarrator(
            this,
            onReadyChanged = { voiceReady = it },
            onSpeakingChanged = {
                speaking = it
                invalidateOptionsMenu()
                binding.coachButton.text = if (it) getString(R.string.stop) else getString(R.string.urdish_coach)
            },
            onLanguageIssue = { Toast.makeText(this, it, Toast.LENGTH_LONG).show() }
        )

        bindLesson()
        binding.coachButton.setOnClickListener { toggleCoach() }
        binding.markDone.setOnClickListener {
            progress.setLessonDone(lesson.id, true)
            Toast.makeText(this, R.string.marked_done, Toast.LENGTH_SHORT).show()
            binding.markDone.isEnabled = false
        }
        if (progress.isLessonDone(lesson.id)) {
            binding.markDone.isEnabled = false
            binding.markDone.text = getString(R.string.already_done)
        }
    }

    private fun bindLesson() {
        val title = when (language) {
            LocaleHelper.LANG_UR -> lesson.titleUr
            LocaleHelper.LANG_URDISH -> lesson.titleUrdish
            else -> lesson.titleEn
        }
        binding.lessonTitle.text = title
        binding.lessonMeta.text = "${lesson.periods}  ·  ${lesson.textbook}"
        binding.keyIdea.text = if (language == LocaleHelper.LANG_UR) lesson.keyIdeaUr else lesson.keyIdeaEn
        binding.learnText.text = if (language == LocaleHelper.LANG_UR) lesson.learnUr else lesson.learnEn
        binding.tryIt.text = if (language == LocaleHelper.LANG_UR) lesson.tryItUr else lesson.tryItEn

        binding.wordChips.removeAllViews()
        lesson.words.forEach { word ->
            val chip = Chip(this)
            chip.text = "${word.en} · ${word.ur}"
            chip.isClickable = false
            binding.wordChips.addView(chip)
        }

        bindDiagramStack(
            binding.examDiagramStack,
            listOf(lesson.diagram),
            exam = true
        )
        bindDiagramStack(
            binding.bookletDiagramStack,
            lesson.bookletPages,
            exam = false
        )

        binding.checkList.removeAllViews()
        lesson.checks.forEachIndexed { index, item ->
            val q = TextView(this)
            q.text = "${index + 1}. " + if (language == LocaleHelper.LANG_UR) item.questionUr else item.questionEn
            q.setTextColor(ContextCompat.getColor(this, R.color.on_surface))
            q.textSize = 15f
            q.setPadding(0, 16, 0, 4)
            val a = TextView(this)
            a.text = getString(R.string.answer_prefix) + " " +
                if (language == LocaleHelper.LANG_UR) item.answerUr else item.answerEn
            a.setTextColor(ContextCompat.getColor(this, R.color.secondary))
            a.textSize = 14f
            binding.checkList.addView(q)
            binding.checkList.addView(a)
        }

        binding.iCanList.removeAllViews()
        val items = if (language == LocaleHelper.LANG_UR) lesson.iCanUr else lesson.iCanEn
        items.forEachIndexed { index, label ->
            val box = CheckBox(this)
            box.text = label
            box.isChecked = progress.isICanTicked(lesson.id, index)
            box.setOnCheckedChangeListener { _, checked ->
                progress.setICanTicked(lesson.id, index, checked)
            }
            val lp = LinearLayout.LayoutParams(
                LinearLayout.LayoutParams.MATCH_PARENT,
                LinearLayout.LayoutParams.WRAP_CONTENT
            )
            binding.iCanList.addView(box, lp)
        }
    }

    private fun bindDiagramStack(stack: LinearLayout, paths: List<String>, exam: Boolean) {
        stack.removeAllViews()
        val inflater = LayoutInflater.from(this)
        paths.forEachIndexed { index, path ->
            val card = ItemDiagramBinding.inflate(inflater, stack, false)
            AssetImages.load(this, card.diagramImage, path)
            card.diagramLabel.text = if (exam) {
                getString(R.string.exam_diagram_label, index + 1)
            } else {
                val page = path.substringAfterLast('/').removeSuffix(".jpg").replace('_', ' ')
                getString(R.string.booklet_page_label, page)
            }
            card.root.setOnClickListener {
                startActivity(Intent(this, DiagramActivity::class.java).putExtra(DiagramActivity.EXTRA_PATH, path))
            }
            stack.addView(card.root)
        }
    }

    private fun toggleCoach() {
        if (speaking) {
            voice?.stop()
            return
        }
        if (!voiceReady) {
            Toast.makeText(this, R.string.voice_not_ready, Toast.LENGTH_SHORT).show()
            return
        }
        if (voice?.speak(lesson.coachUrdish, LocaleHelper.LANG_URDISH) != true) {
            Toast.makeText(this, R.string.voice_install_prompt, Toast.LENGTH_LONG).show()
        }
    }

    override fun onCreateOptionsMenu(menu: Menu): Boolean {
        menuInflater.inflate(R.menu.menu_lesson, menu)
        val listen = menu.findItem(R.id.action_listen)
        listen.title = if (speaking) getString(R.string.stop) else getString(R.string.urdish_coach)
        return true
    }

    override fun onOptionsItemSelected(item: MenuItem): Boolean {
        return when (item.itemId) {
            R.id.action_listen -> {
                toggleCoach()
                true
            }
            else -> super.onOptionsItemSelected(item)
        }
    }

    override fun onSupportNavigateUp(): Boolean {
        finish()
        return true
    }

    override fun onDestroy() {
        voice?.shutdown()
        voice = null
        super.onDestroy()
    }

    companion object {
        const val EXTRA_LESSON_ID = "lesson_id"
    }
}
