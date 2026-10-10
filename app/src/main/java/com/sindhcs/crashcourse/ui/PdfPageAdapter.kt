package com.sindhcs.crashcourse.ui

import android.graphics.Bitmap
import android.view.LayoutInflater
import android.view.ViewGroup
import androidx.recyclerview.widget.RecyclerView
import com.sindhcs.crashcourse.databinding.ItemPdfPageBinding
import com.sindhcs.crashcourse.util.PdfRepository

class PdfPageAdapter(
    private val bookletPages: List<Int>
) : RecyclerView.Adapter<PdfPageAdapter.Holder>() {

    private val cache = mutableMapOf<Int, Bitmap>()

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): Holder {
        val binding = ItemPdfPageBinding.inflate(LayoutInflater.from(parent.context), parent, false)
        return Holder(binding)
    }

    override fun onBindViewHolder(holder: Holder, position: Int) {
        val page = bookletPages[position]
        val width = holder.binding.root.width.takeIf { it > 0 }
            ?: holder.binding.root.resources.displayMetrics.widthPixels
        val bitmap = cache.getOrPut(page) {
            PdfRepository.renderPage(holder.binding.root.context, page, width)
        }
        holder.binding.pageImage.setImageBitmap(bitmap)
    }

    override fun getItemCount(): Int = bookletPages.size

    class Holder(val binding: ItemPdfPageBinding) : RecyclerView.ViewHolder(binding.root)
}
