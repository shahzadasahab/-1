package com.sindhcs.crashcourse.ui

import android.graphics.Color
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import androidx.recyclerview.widget.RecyclerView
import com.sindhcs.crashcourse.R
import com.sindhcs.crashcourse.data.CourseDay
import com.sindhcs.crashcourse.data.ProgressStore
import com.sindhcs.crashcourse.databinding.ItemDayBinding

class DayAdapter(
    private val onClick: (CourseDay) -> Unit
) : RecyclerView.Adapter<DayAdapter.Holder>() {

    private var items: List<CourseDay> = emptyList()

    fun submit(days: List<CourseDay>) {
        items = days
        notifyDataSetChanged()
    }

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): Holder {
        val binding = ItemDayBinding.inflate(LayoutInflater.from(parent.context), parent, false)
        return Holder(binding)
    }

    override fun onBindViewHolder(holder: Holder, position: Int) {
        holder.bind(items[position])
    }

    override fun getItemCount(): Int = items.size

    inner class Holder(private val binding: ItemDayBinding) : RecyclerView.ViewHolder(binding.root) {
        fun bind(day: CourseDay) {
            val ctx = binding.root.context
            binding.dayNumber.text = if (day.day == 0) "i" else day.day.toString()
            binding.kindBadge.text = day.kind
            binding.kindBadge.setBackgroundColor(kindColor(day.kind))
            binding.dayFocus.text = day.focus
            binding.dayGolden.text = ctx.getString(R.string.golden_today, day.golden)
            binding.dayPages.text = ctx.getString(R.string.pages_range, day.startPage, day.endPage)
            binding.doneBadge.visibility =
                if (ProgressStore.isDone(ctx, day.id)) View.VISIBLE else View.GONE
            binding.root.setOnClickListener { onClick(day) }
        }

        private fun kindColor(kind: String): Int = when (kind) {
            "Teach" -> Color.parseColor("#1B6B4A")
            "Checkpoint" -> Color.parseColor("#8A3B12")
            "How-to" -> Color.parseColor("#B8860B")
            else -> Color.parseColor("#3D4A8A")
        }
    }
}
