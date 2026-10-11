package com.sindhcs.crashcourse

import android.content.Intent
import android.os.Bundle
import android.view.Menu
import android.view.MenuItem
import android.view.WindowManager
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import com.sindhcs.crashcourse.data.CourseRepository
import com.sindhcs.crashcourse.data.ProgressStore
import com.sindhcs.crashcourse.data.TutorScript
import com.sindhcs.crashcourse.databinding.ActivityHomeBinding
import com.sindhcs.crashcourse.util.LocaleHelper
import com.sindhcs.crashcourse.util.MixedVoiceNarrator

class HomeActivity : AppCompatActivity() {

    private lateinit var binding: ActivityHomeBinding
    private var narrator: MixedVoiceNarrator? = null
    private var voiceReady = false
    private var speaking = false

    override fun attachBaseContext(newBase: android.content.Context) {
        super.attachBaseContext(LocaleHelper.wrap(newBase))
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        binding = ActivityHomeBinding.inflate(layoutInflater)
        setContentView(binding.root)
        setSupportActionBar(binding.toolbar)
        supportActionBar?.title = getString(R.string.app_name)

        narrator = MixedVoiceNarrator(
            context = this,
            onReadyChanged = { voiceReady = it },
            onSpeakingChanged = {
                speaking = it
                if (it) window.addFlags(WindowManager.LayoutParams.FLAG_KEEP_SCREEN_ON)
                else window.clearFlags(WindowManager.LayoutParams.FLAG_KEEP_SCREEN_ON)
                invalidateOptionsMenu()
                binding.listenWelcome.text = getString(if (it) R.string.stop else R.string.listen_welcome)
            },
            onLanguageIssue = { Toast.makeText(this, it, Toast.LENGTH_LONG).show() }
        )

        val courses = CourseRepository.getCourses(this)
        val xi = courses.first { it.id == "xi" }
        val xii = courses.first { it.id == "xii" }
        binding.xiProgress.text = getString(R.string.progress_label, ProgressStore.completedCount(this, xi))
        binding.xiiProgress.text = getString(R.string.progress_label, ProgressStore.completedCount(this, xii))
        binding.versionBadge.text = getString(R.string.version_badge, BuildConfig.VERSION_NAME)

        binding.cardXi.setOnClickListener { openCourse("xi") }
        binding.cardXii.setOnClickListener { openCourse("xii") }
        binding.cardHowTo.setOnClickListener {
            startActivity(Intent(this, DayActivity::class.java).apply {
                putExtra(DayActivity.EXTRA_DAY_ID, CourseRepository.getHowToDay(xi).id)
                putExtra(DayActivity.EXTRA_COURSE_ID, "xi")
                putExtra(DayActivity.EXTRA_HOWTO, true)
            })
        }
        binding.listenWelcome.setOnClickListener { toggleWelcome() }
    }

    override fun onResume() {
        super.onResume()
        updateContinueButton()
    }

    private fun updateContinueButton() {
        val last = ProgressStore.lastOpened(this)?.let { CourseRepository.getDay(this, it) }
        val howToCourse = ProgressStore.lastOpened(this)?.removeSuffix("-howto")?.takeIf {
            ProgressStore.lastOpened(this)?.endsWith("-howto") == true
        }
        when {
            last != null -> {
                binding.continueButton.visibility = android.view.View.VISIBLE
                binding.continueButton.text = getString(
                    R.string.continue_label,
                    if (last.courseId == "xi") getString(R.string.class_xi) else getString(R.string.class_xii),
                    last.day
                )
                binding.continueButton.setOnClickListener {
                    startActivity(Intent(this, DayActivity::class.java).apply {
                        putExtra(DayActivity.EXTRA_DAY_ID, last.id)
                        putExtra(DayActivity.EXTRA_COURSE_ID, last.courseId)
                    })
                }
            }
            howToCourse != null -> {
                binding.continueButton.visibility = android.view.View.VISIBLE
                binding.continueButton.text = getString(R.string.continue_how_to)
                binding.continueButton.setOnClickListener {
                    startActivity(Intent(this, DayActivity::class.java).apply {
                        putExtra(DayActivity.EXTRA_COURSE_ID, howToCourse)
                        putExtra(DayActivity.EXTRA_HOWTO, true)
                    })
                }
            }
            else -> binding.continueButton.visibility = android.view.View.GONE
        }
    }

    private fun openCourse(courseId: String) {
        startActivity(Intent(this, CourseActivity::class.java).apply {
            putExtra(CourseActivity.EXTRA_COURSE_ID, courseId)
        })
    }

    private fun toggleWelcome() {
        if (speaking) {
            narrator?.stop()
            return
        }
        if (!voiceReady) {
            Toast.makeText(this, R.string.voice_not_ready, Toast.LENGTH_SHORT).show()
            return
        }
        narrator?.setRateScale(ProgressStore.speechRate(this))
        narrator?.speakScript(TutorScript.welcome())
    }

    override fun onCreateOptionsMenu(menu: Menu): Boolean {
        menuInflater.inflate(R.menu.menu_main, menu)
        menu.findItem(R.id.action_listen).title = getString(if (speaking) R.string.stop else R.string.listen_welcome)
        return true
    }

    override fun onOptionsItemSelected(item: MenuItem): Boolean {
        return when (item.itemId) {
            R.id.action_listen -> {
                toggleWelcome()
                true
            }
            R.id.action_tts_settings -> {
                MixedVoiceNarrator.openTtsSettings(this)
                true
            }
            else -> super.onOptionsItemSelected(item)
        }
    }

    override fun onPause() {
        if (speaking) narrator?.stop()
        super.onPause()
    }

    override fun onDestroy() {
        narrator?.shutdown()
        narrator = null
        super.onDestroy()
    }
}
