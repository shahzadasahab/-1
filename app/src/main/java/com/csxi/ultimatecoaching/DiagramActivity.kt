package com.csxi.ultimatecoaching

import android.os.Bundle
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import com.csxi.ultimatecoaching.databinding.ActivityDiagramBinding
import com.csxi.ultimatecoaching.util.AssetImages
import com.csxi.ultimatecoaching.util.LocaleHelper

class DiagramActivity : AppCompatActivity() {

    override fun attachBaseContext(newBase: android.content.Context) {
        super.attachBaseContext(LocaleHelper.wrap(newBase))
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        val binding = ActivityDiagramBinding.inflate(layoutInflater)
        setContentView(binding.root)
        val path = intent.getStringExtra(EXTRA_PATH)
        if (path.isNullOrBlank()) {
            Toast.makeText(this, R.string.missing_lesson, Toast.LENGTH_SHORT).show()
            finish()
            return
        }
        setSupportActionBar(binding.toolbar)
        supportActionBar?.setDisplayHomeAsUpEnabled(true)
        supportActionBar?.title = path.substringAfterLast('/')
        AssetImages.load(this, binding.fullImage, path)
        binding.toolbar.setNavigationOnClickListener { finish() }
    }

    companion object {
        const val EXTRA_PATH = "asset_path"
    }
}
