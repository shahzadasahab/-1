package com.sindhcs.crashcourse

import android.content.Intent
import android.os.Bundle
import android.view.Menu
import android.view.MenuItem
import android.widget.Toast
import androidx.appcompat.app.AlertDialog
import androidx.appcompat.app.AppCompatActivity
import com.sindhcs.crashcourse.data.CourseRepository
import com.sindhcs.crashcourse.data.ProgressStore
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
        narrator?.speakScript(CourseRepository.getWelcomeScript())
    }

    override fun onCreateOptionsMenu(menu: Menu): Boolean {
        menuInflater.inflate(R.menu.menu_main, menu)
        menu.findItem(R.id.action_listen).title = getString(if (speaking) R.string.stop else R.string.listen)
        return true
    }

    override fun onOptionsItemSelected(item: MenuItem): Boolean {
        return when (item.itemId) {
            R.id.action_language -> {
                showLanguageDialog()
                true
            }
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

    private fun showLanguageDialog() {
        val options = arrayOf(getString(R.string.english), getString(R.string.urdu))
        val current = if (LocaleHelper.getLanguage(this) == LocaleHelper.LANG_UR) 1 else 0
        AlertDialog.Builder(this)
            .setTitle(R.string.language)
            .setSingleChoiceItems(options, current) { dialog, which ->
                val lang = if (which == 1) LocaleHelper.LANG_UR else LocaleHelper.LANG_EN
                if (lang != LocaleHelper.getLanguage(this)) {
                    LocaleHelper.setLanguage(this, lang)
                    recreate()
                }
                dialog.dismiss()
            }
            .show()
    }

    override fun onDestroy() {
        narrator?.shutdown()
        narrator = null
        super.onDestroy()
    }
}
