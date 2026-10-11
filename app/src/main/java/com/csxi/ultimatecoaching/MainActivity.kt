package com.csxi.ultimatecoaching

import android.content.Intent
import android.os.Bundle
import android.view.Menu
import android.view.MenuItem
import android.widget.Toast
import androidx.appcompat.app.AlertDialog
import androidx.appcompat.app.AppCompatActivity
import androidx.recyclerview.widget.LinearLayoutManager
import com.csxi.ultimatecoaching.data.Curriculum
import com.csxi.ultimatecoaching.databinding.ActivityMainBinding
import com.csxi.ultimatecoaching.ui.UnitAdapter
import com.csxi.ultimatecoaching.util.AssetImages
import com.csxi.ultimatecoaching.util.LocaleHelper
import com.csxi.ultimatecoaching.util.ProgressStore
import com.csxi.ultimatecoaching.util.VoiceNarrator

class MainActivity : AppCompatActivity() {

    private lateinit var binding: ActivityMainBinding
    private lateinit var progress: ProgressStore
    private var language = LocaleHelper.LANG_URDISH
    private var voice: VoiceNarrator? = null
    private var voiceReady = false
    private var speaking = false

    override fun attachBaseContext(newBase: android.content.Context) {
        super.attachBaseContext(LocaleHelper.wrap(newBase))
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        binding = ActivityMainBinding.inflate(layoutInflater)
        setContentView(binding.root)
        language = LocaleHelper.getLanguage(this)
        progress = ProgressStore(this)
        setSupportActionBar(binding.toolbar)
        supportActionBar?.title = getString(R.string.app_name)

        voice = VoiceNarrator(
            this,
            onReadyChanged = { voiceReady = it },
            onSpeakingChanged = {
                speaking = it
                invalidateOptionsMenu()
            },
            onLanguageIssue = { Toast.makeText(this, it, Toast.LENGTH_LONG).show() }
        )

        AssetImages.load(this, binding.coverImage, "diagrams/cover.png")
        binding.versionBadge.text = getString(R.string.version_badge, BuildConfig.VERSION_NAME)
        refreshProgress()

        val adapter = UnitAdapter(language, progress) { unit ->
            startActivity(Intent(this, UnitActivity::class.java).putExtra(UnitActivity.EXTRA_UNIT_ID, unit.id))
        }
        binding.unitList.layoutManager = LinearLayoutManager(this)
        binding.unitList.adapter = adapter
        binding.unitList.isNestedScrollingEnabled = false
        adapter.submit(Curriculum.units())

        binding.btnGlossary.setOnClickListener {
            startActivity(Intent(this, GlossaryActivity::class.java))
        }
        binding.btnMock.setOnClickListener { showUnitPicker(forQuiz = true) }
        binding.btnCoach.setOnClickListener { toggleHomeCoach() }
    }

    override fun onResume() {
        super.onResume()
        refreshProgress()
        (binding.unitList.adapter as? UnitAdapter)?.submit(Curriculum.units())
    }

    private fun refreshProgress() {
        val lessons = Curriculum.allLessons()
        val done = progress.completedCount(lessons.map { it.id })
        binding.progressText.text = getString(R.string.progress_line, done, lessons.size)
        binding.progressBar.max = lessons.size
        binding.progressBar.progress = done
    }

    override fun onCreateOptionsMenu(menu: Menu): Boolean {
        menuInflater.inflate(R.menu.menu_main, menu)
        val listen = menu.findItem(R.id.action_listen)
        listen.title = if (speaking) getString(R.string.stop) else getString(R.string.urdish_coach)
        listen.setIcon(if (speaking) android.R.drawable.ic_media_pause else android.R.drawable.ic_media_play)
        return true
    }

    override fun onOptionsItemSelected(item: MenuItem): Boolean {
        return when (item.itemId) {
            R.id.action_language -> {
                showLanguageDialog()
                true
            }
            R.id.action_listen -> {
                toggleHomeCoach()
                true
            }
            R.id.action_glossary -> {
                startActivity(Intent(this, GlossaryActivity::class.java))
                true
            }
            else -> super.onOptionsItemSelected(item)
        }
    }

    private fun toggleHomeCoach() {
        if (speaking) {
            voice?.stop()
            return
        }
        if (!voiceReady) {
            Toast.makeText(this, R.string.voice_not_ready, Toast.LENGTH_SHORT).show()
            return
        }
        if (voice?.speak(Curriculum.homeCoachUrdish, LocaleHelper.LANG_URDISH) != true) {
            Toast.makeText(this, R.string.voice_install_prompt, Toast.LENGTH_LONG).show()
        }
    }

    private fun showLanguageDialog() {
        val options = arrayOf(
            getString(R.string.english),
            getString(R.string.urdish),
            getString(R.string.urdu)
        )
        val current = when (language) {
            LocaleHelper.LANG_URDISH -> 1
            LocaleHelper.LANG_UR -> 2
            else -> 0
        }
        AlertDialog.Builder(this)
            .setTitle(R.string.language)
            .setSingleChoiceItems(options, current) { dialog, which ->
                val newLang = when (which) {
                    1 -> LocaleHelper.LANG_URDISH
                    2 -> LocaleHelper.LANG_UR
                    else -> LocaleHelper.LANG_EN
                }
                if (newLang != language) {
                    LocaleHelper.setLanguage(this, newLang)
                    recreate()
                }
                dialog.dismiss()
            }
            .show()
    }

    private fun showUnitPicker(forQuiz: Boolean) {
        val units = Curriculum.units()
        val names = units.map {
            "Unit ${it.number} · " + if (language == LocaleHelper.LANG_UR) it.titleUr else it.titleEn
        }.toTypedArray()
        AlertDialog.Builder(this)
            .setTitle(if (forQuiz) R.string.mock_tests else R.string.units_title)
            .setItems(names) { _, which ->
                val unit = units[which]
                if (forQuiz) {
                    startActivity(
                        Intent(this, QuizActivity::class.java)
                            .putExtra(QuizActivity.EXTRA_UNIT_ID, unit.id)
                    )
                } else {
                    startActivity(
                        Intent(this, UnitActivity::class.java)
                            .putExtra(UnitActivity.EXTRA_UNIT_ID, unit.id)
                    )
                }
            }
            .show()
    }

    override fun onDestroy() {
        voice?.shutdown()
        voice = null
        super.onDestroy()
    }
}
