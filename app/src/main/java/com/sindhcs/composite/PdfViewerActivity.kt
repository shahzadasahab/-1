package com.sindhcs.composite

import android.graphics.Bitmap
import android.graphics.pdf.PdfRenderer
import android.os.Bundle
import android.os.ParcelFileDescriptor
import android.widget.ImageView
import android.widget.TextView
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import com.google.android.material.appbar.MaterialToolbar
import com.google.android.material.button.MaterialButton
import java.io.File

class PdfViewerActivity : AppCompatActivity() {

    private var renderer: PdfRenderer? = null
    private var descriptor: ParcelFileDescriptor? = null
    private var pageIndex = 0
    private lateinit var image: ImageView
    private lateinit var pageLabel: TextView

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_pdf_viewer)

        val fileName = intent.getStringExtra(EXTRA_PDF) ?: return finish()
        pageIndex = ((intent.getIntExtra(EXTRA_PAGE, 1)) - 1).coerceAtLeast(0)

        val toolbar = findViewById<MaterialToolbar>(R.id.toolbar)
        toolbar.title = fileName
        toolbar.setNavigationOnClickListener { finish() }

        image = findViewById(R.id.pdfPage)
        pageLabel = findViewById(R.id.pageLabel)
        findViewById<MaterialButton>(R.id.prevPage).setOnClickListener { showPage(pageIndex - 1) }
        findViewById<MaterialButton>(R.id.nextPage).setOnClickListener { showPage(pageIndex + 1) }

        try {
            val cache = File(cacheDir, fileName)
            if (!cache.exists() || cache.length() == 0L) {
                assets.open("pdfs/$fileName").use { input ->
                    cache.outputStream().use { output -> input.copyTo(output) }
                }
            }
            descriptor = ParcelFileDescriptor.open(cache, ParcelFileDescriptor.MODE_READ_ONLY)
            renderer = PdfRenderer(descriptor!!)
            showPage(pageIndex)
        } catch (error: Exception) {
            Toast.makeText(this, R.string.pdf_failed, Toast.LENGTH_LONG).show()
            finish()
        }
    }

    private fun showPage(index: Int) {
        val pdf = renderer ?: return
        pageIndex = index.coerceIn(0, pdf.pageCount - 1)
        pdf.openPage(pageIndex).use { page ->
            val width = resources.displayMetrics.widthPixels
            val height = (width.toFloat() * page.height / page.width).toInt().coerceAtLeast(1)
            val bitmap = Bitmap.createBitmap(width, height, Bitmap.Config.ARGB_8888)
            page.render(bitmap, null, null, PdfRenderer.Page.RENDER_MODE_FOR_DISPLAY)
            image.setImageBitmap(bitmap)
        }
        pageLabel.text = getString(R.string.pdf_page, pageIndex + 1, pdf.pageCount)
    }

    override fun onDestroy() {
        renderer?.close()
        descriptor?.close()
        super.onDestroy()
    }

    companion object {
        const val EXTRA_PDF = "extra_pdf"
        const val EXTRA_PAGE = "extra_page"
    }
}
