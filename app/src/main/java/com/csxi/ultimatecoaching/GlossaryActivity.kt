package com.csxi.ultimatecoaching

import android.os.Bundle
import android.text.Editable
import android.text.TextWatcher
import androidx.appcompat.app.AppCompatActivity
import androidx.recyclerview.widget.LinearLayoutManager
import com.csxi.ultimatecoaching.data.Glossary
import com.csxi.ultimatecoaching.databinding.ActivityGlossaryBinding
import com.csxi.ultimatecoaching.ui.GlossaryAdapter
import com.csxi.ultimatecoaching.util.LocaleHelper

class GlossaryActivity : AppCompatActivity() {

    private lateinit var binding: ActivityGlossaryBinding
    private lateinit var adapter: GlossaryAdapter

    override fun attachBaseContext(newBase: android.content.Context) {
        super.attachBaseContext(LocaleHelper.wrap(newBase))
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        binding = ActivityGlossaryBinding.inflate(layoutInflater)
        setContentView(binding.root)
        setSupportActionBar(binding.toolbar)
        supportActionBar?.setDisplayHomeAsUpEnabled(true)
        supportActionBar?.title = getString(R.string.glossary)
        val language = LocaleHelper.getLanguage(this)
        adapter = GlossaryAdapter(language)
        binding.termList.layoutManager = LinearLayoutManager(this)
        binding.termList.adapter = adapter
        adapter.submit(Glossary.all())
        binding.search.addTextChangedListener(object : TextWatcher {
            override fun beforeTextChanged(s: CharSequence?, start: Int, count: Int, after: Int) = Unit
            override fun onTextChanged(s: CharSequence?, start: Int, before: Int, count: Int) = Unit
            override fun afterTextChanged(s: Editable?) {
                val q = s?.toString()?.trim().orEmpty().lowercase()
                val filtered = Glossary.all().filter {
                    q.isEmpty() ||
                        it.term.lowercase().contains(q) ||
                        it.en.lowercase().contains(q) ||
                        it.ur.contains(q) ||
                        it.urdish.lowercase().contains(q)
                }
                adapter.submit(filtered)
            }
        })
    }

    override fun onSupportNavigateUp(): Boolean {
        finish()
        return true
    }
}
