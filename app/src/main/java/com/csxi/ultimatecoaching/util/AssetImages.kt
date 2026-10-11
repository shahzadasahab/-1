package com.csxi.ultimatecoaching.util

import android.content.Context
import android.graphics.BitmapFactory
import android.widget.ImageView

object AssetImages {

    fun load(context: Context, view: ImageView, assetPath: String) {
        try {
            context.assets.open(assetPath).use { stream ->
                view.setImageBitmap(BitmapFactory.decodeStream(stream))
            }
        } catch (_: Exception) {
            view.setImageResource(android.R.drawable.ic_menu_gallery)
        }
    }
}
