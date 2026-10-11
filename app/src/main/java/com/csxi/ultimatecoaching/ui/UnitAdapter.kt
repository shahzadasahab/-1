package com.csxi.ultimatecoaching.ui

import android.graphics.Color
import android.view.LayoutInflater
import android.view.ViewGroup
import androidx.recyclerview.widget.RecyclerView
import com.csxi.ultimatecoaching.data.CourseUnit
import com.csxi.ultimatecoaching.databinding.ItemUnitBinding
import com.csxi.ultimatecoaching.util.AssetImages
import com.csxi.ultimatecoaching.util.LocaleHelper
import com.csxi.ultimatecoaching.util.ProgressStore

class UnitAdapter(
    private val language: String,
    private val progress: ProgressStore,
    private val onClick: (CourseUnit) -> Unit
) : RecyclerView.Adapter<UnitAdapter.Holder>() {

    private var items: List<CourseUnit> = emptyList()

    fun submit(list: List<CourseUnit>) {
        items = list
        notifyDataSetChanged()
    }

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): Holder {
        val binding = ItemUnitBinding.inflate(LayoutInflater.from(parent.context), parent, false)
        return Holder(binding)
    }

    override fun getItemCount(): Int = items.size

    override fun onBindViewHolder(holder: Holder, position: Int) {
        val unit = items[position]
        val title = when (language) {
            LocaleHelper.LANG_UR -> unit.titleUr
            LocaleHelper.LANG_URDISH -> unit.titleUrdish
            else -> unit.titleEn
        }
        val summary = if (language == LocaleHelper.LANG_UR) unit.summaryUr else unit.summaryEn
        val done = progress.completedCount(unit.lessons.map { it.id })
        holder.binding.unitNumber.text = unit.number.toString()
        holder.binding.unitTitle.text = title
        holder.binding.unitMeta.text = "${unit.weeks}  ·  $done/${unit.lessons.size}"
        holder.binding.unitSummary.text = summary
        holder.binding.unitAccent.setBackgroundColor(Color.parseColor(unit.colorHex))
        AssetImages.load(holder.itemView.context, holder.binding.unitImage, unit.coverDiagram)
        holder.itemView.setOnClickListener { onClick(unit) }
    }

    class Holder(val binding: ItemUnitBinding) : RecyclerView.ViewHolder(binding.root)
}
