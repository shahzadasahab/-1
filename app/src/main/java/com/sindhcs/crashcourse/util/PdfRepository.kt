package com.sindhcs.crashcourse.util

import android.content.Context
import android.graphics.Bitmap
import android.graphics.pdf.PdfRenderer
import android.os.ParcelFileDescriptor
import java.io.File
import java.io.FileOutputStream

object PdfRepository {
    private const val ASSET = "course/crash-course.pdf"
    private const val CACHE_NAME = "crash-course.pdf"

    private var renderer: PdfRenderer? = null
    private var descriptor: ParcelFileDescriptor? = null

    @Synchronized
    fun ensureOpen(context: Context): PdfRenderer {
        renderer?.let { return it }
        val file = File(context.cacheDir, CACHE_NAME)
        if (!file.exists() || file.length() == 0L) {
            context.assets.open(ASSET).use { input ->
                FileOutputStream(file).use { output -> input.copyTo(output) }
            }
        }
        descriptor = ParcelFileDescriptor.open(file, ParcelFileDescriptor.MODE_READ_ONLY)
        renderer = PdfRenderer(descriptor!!)
        return renderer!!
    }

    @Synchronized
    fun pageCount(context: Context): Int = ensureOpen(context).pageCount

    @Synchronized
    fun renderPage(context: Context, bookletPage: Int, widthPx: Int): Bitmap {
        val pdf = ensureOpen(context)
        val index = (bookletPage - 1).coerceIn(0, pdf.pageCount - 1)
        val page = pdf.openPage(index)
        val width = widthPx.coerceAtLeast(720)
        val height = (width.toFloat() * page.height / page.width).toInt().coerceAtLeast(1)
        val bitmap = Bitmap.createBitmap(width, height, Bitmap.Config.ARGB_8888)
        bitmap.eraseColor(0xFFFFFFFF.toInt())
        page.render(bitmap, null, null, PdfRenderer.Page.RENDER_MODE_FOR_DISPLAY)
        page.close()
        return bitmap
    }

    @Synchronized
    fun close() {
        renderer?.close()
        descriptor?.close()
        renderer = null
        descriptor = null
    }
}
