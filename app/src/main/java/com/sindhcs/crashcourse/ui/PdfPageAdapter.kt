package com.sindhcs.crashcourse.ui

import android.graphics.Bitmap
import android.os.Handler
import android.os.Looper
import android.util.LruCache
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import androidx.recyclerview.widget.RecyclerView
import com.sindhcs.crashcourse.databinding.ItemPdfPageBinding
import com.sindhcs.crashcourse.util.PdfRepository
import java.util.concurrent.Executors

class PdfPageAdapter(
    private val bookletPages: List<Int>
) : RecyclerView.Adapter<PdfPageAdapter.Holder>() {

    private val cache = object : LruCache<Int, Bitmap>(cacheBytes()) {
        override fun sizeOf(key: Int, value: Bitmap): Int = value.byteCount
    }
    private val main = Handler(Looper.getMainLooper())
    private var released = false

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): Holder {
        val binding = ItemPdfPageBinding.inflate(LayoutInflater.from(parent.context), parent, false)
        return Holder(binding)
    }

    override fun onBindViewHolder(holder: Holder, position: Int) {
        val page = bookletPages[position]
        holder.boundPage = page
        val cached = cache.get(page)
        if (cached != null) {
            show(holder, cached)
            return
        }
        holder.binding.pageImage.setImageDrawable(null)
        holder.binding.pageProgress.visibility = View.VISIBLE
        val context = holder.binding.root.context.applicationContext
        val display = context.resources.displayMetrics.widthPixels
        val width = (display * 3 / 2).coerceIn(720, 1800)
        renderPool.execute {
            if (released) return@execute
            val bitmap = runCatching { PdfRepository.renderPage(context, page, width) }.getOrNull()
            main.post {
                if (released || bitmap == null) return@post
                cache.put(page, bitmap)
                if (holder.boundPage == page) show(holder, bitmap)
            }
        }
    }

    private fun show(holder: Holder, bitmap: Bitmap) {
        holder.binding.pageProgress.visibility = View.GONE
        holder.binding.pageImage.setImageBitmap(bitmap)
    }

    override fun onViewRecycled(holder: Holder) {
        holder.boundPage = -1
        holder.binding.pageImage.setImageDrawable(null)
        super.onViewRecycled(holder)
    }

    override fun getItemCount(): Int = bookletPages.size

    fun release() {
        released = true
        main.removeCallbacksAndMessages(null)
        cache.evictAll()
    }

    class Holder(val binding: ItemPdfPageBinding) : RecyclerView.ViewHolder(binding.root) {
        var boundPage: Int = -1
    }

    companion object {
        private val renderPool = Executors.newSingleThreadExecutor()

        private fun cacheBytes(): Int =
            (Runtime.getRuntime().maxMemory() / 6).coerceAtMost(96L * 1024 * 1024).toInt()
    }
}
