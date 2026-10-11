package com.csxi.ultimatecoaching.ui

import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import androidx.recyclerview.widget.RecyclerView
import com.csxi.ultimatecoaching.data.Lesson
import com.csxi.ultimatecoaching.databinding.ItemLessonBinding
import com.csxi.ultimatecoaching.util.LocaleHelper
import com.csxi.ultimatecoaching.util.ProgressStore

class LessonAdapter(
    private val language: String,
    private val progress: ProgressStore,
    private val onClick: (Lesson) -> Unit
) : RecyclerView.Adapter<LessonAdapter.Holder>() {

    private var items: List<Lesson> = emptyList()

    fun submit(list: List<Lesson>) {
        items = list
        notifyDataSetChanged()
    }

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): Holder {
        val binding = ItemLessonBinding.inflate(LayoutInflater.from(parent.context), parent, false)
        return Holder(binding)
    }

    override fun getItemCount(): Int = items.size

    override fun onBindViewHolder(holder: Holder, position: Int) {
        val lesson = items[position]
        val title = when (language) {
            LocaleHelper.LANG_UR -> lesson.titleUr
            LocaleHelper.LANG_URDISH -> lesson.titleUrdish
            else -> lesson.titleEn
        }
        holder.binding.lessonCode.text = lesson.code
        holder.binding.lessonTitle.text = title
        holder.binding.lessonMeta.text = "${lesson.periods}  ·  ${lesson.textbook}"
        holder.binding.doneBadge.visibility = if (progress.isLessonDone(lesson.id)) View.VISIBLE else View.GONE
        holder.itemView.setOnClickListener { onClick(lesson) }
    }

    class Holder(val binding: ItemLessonBinding) : RecyclerView.ViewHolder(binding.root)
}
