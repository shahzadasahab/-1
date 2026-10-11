package com.csxi.ultimatecoaching.ui

import android.view.LayoutInflater
import android.view.ViewGroup
import androidx.recyclerview.widget.RecyclerView
import com.csxi.ultimatecoaching.databinding.ItemDiagramBinding
import com.csxi.ultimatecoaching.util.AssetImages

class DiagramAdapter(
    private val paths: List<String>,
    private val onClick: (String) -> Unit
) : RecyclerView.Adapter<DiagramAdapter.Holder>() {

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): Holder {
        val binding = ItemDiagramBinding.inflate(LayoutInflater.from(parent.context), parent, false)
        return Holder(binding)
    }

    override fun getItemCount(): Int = paths.size

    override fun onBindViewHolder(holder: Holder, position: Int) {
        val path = paths[position]
        AssetImages.load(holder.itemView.context, holder.binding.diagramImage, path)
        val label = if (path.startsWith("booklet/")) {
            "Booklet " + path.removePrefix("booklet/").removeSuffix(".jpg").replace("_", " ")
        } else {
            "Exam diagram ${position + 1}"
        }
        holder.binding.diagramLabel.text = label
        holder.itemView.setOnClickListener { onClick(path) }
    }

    class Holder(val binding: ItemDiagramBinding) : RecyclerView.ViewHolder(binding.root)
}
