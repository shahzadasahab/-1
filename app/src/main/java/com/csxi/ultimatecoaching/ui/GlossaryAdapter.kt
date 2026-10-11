package com.csxi.ultimatecoaching.ui

import android.view.LayoutInflater
import android.view.ViewGroup
import androidx.recyclerview.widget.RecyclerView
import com.csxi.ultimatecoaching.data.GlossaryEntry
import com.csxi.ultimatecoaching.databinding.ItemGlossaryBinding
import com.csxi.ultimatecoaching.util.LocaleHelper

class GlossaryAdapter(
    private val language: String
) : RecyclerView.Adapter<GlossaryAdapter.Holder>() {

    private var items: List<GlossaryEntry> = emptyList()

    fun submit(list: List<GlossaryEntry>) {
        items = list
        notifyDataSetChanged()
    }

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): Holder {
        val binding = ItemGlossaryBinding.inflate(LayoutInflater.from(parent.context), parent, false)
        return Holder(binding)
    }

    override fun getItemCount(): Int = items.size

    override fun onBindViewHolder(holder: Holder, position: Int) {
        val item = items[position]
        holder.binding.term.text = item.term
        holder.binding.meaning.text = when (language) {
            LocaleHelper.LANG_UR -> item.ur
            LocaleHelper.LANG_URDISH -> item.urdish
            else -> item.en
        }
        holder.binding.unitChip.text = item.unitId.replace("u", "Unit ")
    }

    class Holder(val binding: ItemGlossaryBinding) : RecyclerView.ViewHolder(binding.root)
}
