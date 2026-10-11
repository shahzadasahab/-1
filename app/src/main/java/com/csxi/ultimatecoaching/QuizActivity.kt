package com.csxi.ultimatecoaching

import android.os.Bundle
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import androidx.core.content.ContextCompat
import com.csxi.ultimatecoaching.data.Curriculum
import com.csxi.ultimatecoaching.data.QuizQuestion
import com.csxi.ultimatecoaching.data.Quizzes
import com.csxi.ultimatecoaching.databinding.ActivityQuizBinding
import com.csxi.ultimatecoaching.util.LocaleHelper
import com.csxi.ultimatecoaching.util.ProgressStore
import com.csxi.ultimatecoaching.util.VoiceNarrator

class QuizActivity : AppCompatActivity() {

    private lateinit var binding: ActivityQuizBinding
    private lateinit var progress: ProgressStore
    private lateinit var questions: List<QuizQuestion>
    private var index = 0
    private var score = 0
    private var language = LocaleHelper.LANG_URDISH
    private var locked = false
    private var voice: VoiceNarrator? = null

    override fun attachBaseContext(newBase: android.content.Context) {
        super.attachBaseContext(LocaleHelper.wrap(newBase))
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        binding = ActivityQuizBinding.inflate(layoutInflater)
        setContentView(binding.root)
        language = LocaleHelper.getLanguage(this)
        progress = ProgressStore(this)
        val unitId = intent.getStringExtra(EXTRA_UNIT_ID) ?: ""
        val unit = Curriculum.unit(unitId)
        questions = Quizzes.forUnit(unitId)
        if (unit == null || questions.isEmpty()) {
            Toast.makeText(this, R.string.missing_unit, Toast.LENGTH_SHORT).show()
            finish()
            return
        }
        setSupportActionBar(binding.toolbar)
        supportActionBar?.setDisplayHomeAsUpEnabled(true)
        supportActionBar?.title = getString(R.string.mock_unit, unit.number)
        voice = VoiceNarrator(this, {}, {}, null)
        showQuestion()
        listOf(binding.opt0, binding.opt1, binding.opt2, binding.opt3).forEachIndexed { i, button ->
            button.setOnClickListener { choose(i) }
        }
        binding.nextButton.setOnClickListener {
            if (index < questions.lastIndex) {
                index += 1
                showQuestion()
            } else {
                finishQuiz()
            }
        }
        binding.coachButton.setOnClickListener {
            val q = questions[index]
            voice?.speak(q.promptUrdish + ". Options: " + q.optionsEn.joinToString(". "), LocaleHelper.LANG_URDISH)
        }
    }

    private fun showQuestion() {
        locked = false
        val q = questions[index]
        binding.progressLabel.text = getString(R.string.question_of, index + 1, questions.size)
        binding.prompt.text = when (language) {
            LocaleHelper.LANG_UR -> q.promptUr
            LocaleHelper.LANG_URDISH -> q.promptUrdish
            else -> q.promptEn
        }
        val options = if (language == LocaleHelper.LANG_UR) q.optionsUr else q.optionsEn
        val buttons = listOf(binding.opt0, binding.opt1, binding.opt2, binding.opt3)
        buttons.forEachIndexed { i, button ->
            button.text = options.getOrNull(i) ?: ""
            button.isEnabled = true
            button.setBackgroundColor(ContextCompat.getColor(this, R.color.surface))
            button.setTextColor(ContextCompat.getColor(this, R.color.on_surface))
        }
        binding.explain.text = ""
        binding.nextButton.isEnabled = false
        binding.nextButton.text = if (index == questions.lastIndex) getString(R.string.finish) else getString(R.string.next)
    }

    private fun choose(choice: Int) {
        if (locked) return
        locked = true
        val q = questions[index]
        val buttons = listOf(binding.opt0, binding.opt1, binding.opt2, binding.opt3)
        buttons.forEach { it.isEnabled = false }
        if (choice == q.correctIndex) {
            score += 1
            buttons[choice].setBackgroundColor(ContextCompat.getColor(this, R.color.correct))
        } else {
            buttons[choice].setBackgroundColor(ContextCompat.getColor(this, R.color.wrong))
            buttons[q.correctIndex].setBackgroundColor(ContextCompat.getColor(this, R.color.correct))
        }
        buttons.forEach { it.setTextColor(ContextCompat.getColor(this, R.color.on_primary)) }
        binding.explain.text = if (language == LocaleHelper.LANG_UR) q.explainUr else q.explainEn
        binding.nextButton.isEnabled = true
    }

    private fun finishQuiz() {
        val unitId = intent.getStringExtra(EXTRA_UNIT_ID) ?: return
        progress.setQuizScore(unitId, score, questions.size)
        binding.prompt.text = getString(R.string.quiz_result, score, questions.size)
        binding.explain.text = if (score * 2 >= questions.size) {
            getString(R.string.quiz_pass)
        } else {
            getString(R.string.quiz_retry)
        }
        listOf(binding.opt0, binding.opt1, binding.opt2, binding.opt3, binding.coachButton).forEach {
            it.isEnabled = false
        }
        binding.nextButton.text = getString(R.string.close)
        binding.nextButton.setOnClickListener { finish() }
    }

    override fun onSupportNavigateUp(): Boolean {
        finish()
        return true
    }

    override fun onDestroy() {
        voice?.shutdown()
        super.onDestroy()
    }

    companion object {
        const val EXTRA_UNIT_ID = "unit_id"
    }
}
