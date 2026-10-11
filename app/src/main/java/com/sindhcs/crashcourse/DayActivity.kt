package com.sindhcs.crashcourse

import android.os.Bundle
import android.view.Menu
import android.view.MenuItem
import android.view.View
import android.view.WindowManager
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import androidx.viewpager2.widget.ViewPager2
import com.sindhcs.crashcourse.data.Course
import com.sindhcs.crashcourse.data.CourseDay
import com.sindhcs.crashcourse.data.CourseRepository
import com.sindhcs.crashcourse.data.PageNarration
import com.sindhcs.crashcourse.data.PageRepository
import com.sindhcs.crashcourse.data.ProgressStore
import com.sindhcs.crashcourse.data.TutorPhase
import com.sindhcs.crashcourse.data.TutorScript
import com.sindhcs.crashcourse.databinding.ActivityDayBinding
import com.sindhcs.crashcourse.ui.PdfPageAdapter
import com.sindhcs.crashcourse.util.LocaleHelper
import com.sindhcs.crashcourse.util.MixedVoiceNarrator

class DayActivity : AppCompatActivity() {

    companion object {
        const val EXTRA_DAY_ID = "day_id"
        const val EXTRA_COURSE_ID = "course_id"
        const val EXTRA_HOWTO = "howto"
    }

    private lateinit var binding: ActivityDayBinding
    private lateinit var course: Course
    private lateinit var day: CourseDay
    private var narrator: MixedVoiceNarrator? = null
    private var voiceReady = false
    private var speaking = false
    private var showingTranscript = false
    private var showingPageText = false
    private var pageAdapter: PdfPageAdapter? = null
    private var pages: List<Int> = emptyList()
    private val speeds = floatArrayOf(0.8f, 1.0f, 1.25f)

    override fun attachBaseContext(newBase: android.content.Context) {
        super.attachBaseContext(LocaleHelper.wrap(newBase))
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        binding = ActivityDayBinding.inflate(layoutInflater)
        setContentView(binding.root)

        val courseId = intent.getStringExtra(EXTRA_COURSE_ID) ?: "xi"
        course = CourseRepository.getCourse(this, courseId) ?: run {
            finish()
            return
        }
        day = if (intent.getBooleanExtra(EXTRA_HOWTO, false)) {
            CourseRepository.getHowToDay(course)
        } else {
            val id = intent.getStringExtra(EXTRA_DAY_ID)
            CourseRepository.getDay(this, id ?: "") ?: CourseRepository.getHowToDay(course)
        }

        setSupportActionBar(binding.toolbar)
        supportActionBar?.setDisplayHomeAsUpEnabled(true)
        supportActionBar?.title = if (day.day == 0) {
            getString(R.string.how_to)
        } else {
            getString(R.string.day_title, day.day)
        }

        narrator = MixedVoiceNarrator(
            context = this,
            onReadyChanged = { voiceReady = it },
            onSpeakingChanged = {
                speaking = it
                if (it) window.addFlags(WindowManager.LayoutParams.FLAG_KEEP_SCREEN_ON)
                else window.clearFlags(WindowManager.LayoutParams.FLAG_KEEP_SCREEN_ON)
                invalidateOptionsMenu()
                binding.listenButton.text = getString(if (it) R.string.stop else R.string.listen_tutor)
            },
            onLanguageIssue = { Toast.makeText(this, it, Toast.LENGTH_LONG).show() }
        )

        ProgressStore.setLastOpened(this, day.id)
        bindDay()
    }

    private fun bindDay() {
        val week = if (day.week == 0) getString(R.string.how_to) else getString(R.string.week_label, day.week)
        binding.dayMeta.text = "$week · ${day.kind} · ${day.chapter}"
        binding.dayFocus.text = day.focus
        binding.dayGolden.text = getString(R.string.golden_today, day.golden)
        val topicBlock = day.topics.joinToString("\n") { "• $it" }
        binding.dayTopics.text = "${getString(R.string.topics_today)}\n$topicBlock"
        binding.transcriptText.text = TutorScript.lessonNotes(day)
        updateDoneButton()

        pages = (day.startPage..day.endPage).toList()
        pageAdapter = PdfPageAdapter(pages)
        binding.pagePager.adapter = pageAdapter
        binding.pagePager.offscreenPageLimit = 1
        binding.pagePager.registerOnPageChangeCallback(object : ViewPager2.OnPageChangeCallback() {
            override fun onPageSelected(position: Int) {
                updatePageIndicator(position, pages)
                updatePageText()
            }
        })
        updatePageIndicator(0, pages)

        binding.listenButton.setOnClickListener { toggleSpeech(tutorScript()) }
        binding.listenPageButton.setOnClickListener {
            val index = binding.pagePager.currentItem
            val booklet = pages.getOrElse(index) { day.startPage }
            val blocks = PageRepository.getBlocks(this, booklet)
            toggleSpeech(TutorScript.pageWalkthrough(booklet, day, blocks))
        }
        binding.pageTextToggle.setOnClickListener {
            showingPageText = !showingPageText
            binding.pageText.visibility = if (showingPageText) View.VISIBLE else View.GONE
            binding.pageTextToggle.text = getString(if (showingPageText) R.string.hide_page_text else R.string.page_text)
            updatePageText()
        }
        updateSpeedButton()
        binding.speedButton.setOnClickListener {
            val current = ProgressStore.speechRate(this)
            val next = speeds[(speeds.indexOfFirst { it == current } + 1).mod(speeds.size)]
            ProgressStore.setSpeechRate(this, next)
            narrator?.setRateScale(next)
            updateSpeedButton()
        }
        binding.transcriptToggle.setOnClickListener {
            showingTranscript = !showingTranscript
            binding.transcriptText.visibility = if (showingTranscript) View.VISIBLE else View.GONE
            binding.transcriptToggle.text = getString(
                if (showingTranscript) R.string.hide_transcript else R.string.transcript
            )
        }
        binding.doneButton.setOnClickListener {
            if (day.day == 0) return@setOnClickListener
            ProgressStore.setDone(this, day.id, !ProgressStore.isDone(this, day.id))
            updateDoneButton()
        }
        binding.prevDay.setOnClickListener { openRelative(-1) }
        binding.nextDay.setOnClickListener { openRelative(1) }
        binding.prevDay.visibility = if (day.day <= 1) View.INVISIBLE else View.VISIBLE
        binding.nextDay.visibility = if (day.day == 0 || day.day >= 30) View.INVISIBLE else View.VISIBLE
        binding.doneButton.visibility = if (day.day == 0) View.GONE else View.VISIBLE
    }

    private fun selectedPhase(): TutorPhase = when (binding.phaseGroup.checkedChipId) {
        R.id.phaseRecap -> TutorPhase.RECAP
        R.id.phaseTeach -> TutorPhase.TEACH
        R.id.phaseDrill -> TutorPhase.DRILL
        R.id.phaseHomework -> TutorPhase.HOMEWORK
        else -> TutorPhase.FULL
    }

    private fun tutorScript(): String = TutorScript.session(this, course, day, selectedPhase())

    private fun updateSpeedButton() {
        binding.speedButton.text = getString(R.string.speed_label, "${ProgressStore.speechRate(this)}x")
    }

    private fun updatePageText() {
        if (!showingPageText) return
        val booklet = pages.getOrElse(binding.pagePager.currentItem) { day.startPage }
        val text = PageNarration.displayText(PageRepository.getBlocks(this, booklet))
        binding.pageText.text = text.ifEmpty { getString(R.string.page_text_empty) }
    }

    private fun updatePageIndicator(position: Int, pages: List<Int>) {
        val booklet = pages.getOrElse(position) { day.startPage }
        binding.pageIndicator.text = getString(R.string.page_of, position + 1, pages.size, booklet)
    }

    private fun updateDoneButton() {
        val done = ProgressStore.isDone(this, day.id)
        binding.doneButton.text = getString(if (done) R.string.mark_undone else R.string.mark_done)
    }

    private fun toggleSpeech(script: String) {
        if (speaking) {
            narrator?.stop()
            return
        }
        if (!voiceReady) {
            Toast.makeText(this, R.string.voice_not_ready, Toast.LENGTH_SHORT).show()
            return
        }
        narrator?.setRateScale(ProgressStore.speechRate(this))
        if (narrator?.speakScript(script) != true) {
            Toast.makeText(this, R.string.voice_install_prompt, Toast.LENGTH_LONG).show()
        }
    }

    private fun openRelative(delta: Int) {
        val target = course.days.find { it.day == day.day + delta } ?: return
        intent.putExtra(EXTRA_DAY_ID, target.id)
        intent.putExtra(EXTRA_HOWTO, false)
        recreate()
    }

    override fun onCreateOptionsMenu(menu: Menu): Boolean {
        menuInflater.inflate(R.menu.menu_main, menu)
        menu.findItem(R.id.action_listen).title = getString(if (speaking) R.string.stop else R.string.listen_tutor)
        return true
    }

    override fun onOptionsItemSelected(item: MenuItem): Boolean {
        return when (item.itemId) {
            R.id.action_listen -> {
                toggleSpeech(tutorScript())
                true
            }
            R.id.action_tts_settings -> {
                MixedVoiceNarrator.openTtsSettings(this)
                true
            }
            else -> super.onOptionsItemSelected(item)
        }
    }

    override fun onSupportNavigateUp(): Boolean {
        finish()
        return true
    }

    override fun onPause() {
        if (speaking) narrator?.stop()
        super.onPause()
    }

    override fun onDestroy() {
        pageAdapter?.release()
        narrator?.shutdown()
        narrator = null
        super.onDestroy()
    }
}
