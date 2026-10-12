package com.sindhcs.crashcourse.ui

import android.content.Context
import android.graphics.Matrix
import android.graphics.RectF
import android.graphics.drawable.Drawable
import android.util.AttributeSet
import android.view.GestureDetector
import android.view.MotionEvent
import android.view.ScaleGestureDetector
import androidx.appcompat.widget.AppCompatImageView

/**
 * ImageView with pinch zoom, drag and double-tap zoom. While zoomed in it asks parents
 * (ViewPager2, NestedScrollView) not to intercept touches so panning works.
 */
class ZoomImageView @JvmOverloads constructor(
    context: Context,
    attrs: AttributeSet? = null
) : AppCompatImageView(context, attrs) {

    private val matrixValues = FloatArray(9)
    private val drawMatrix = Matrix()
    private var minScale = 1f
    private var currentScale = 1f
    private val maxZoom = 4f

    private val scaleDetector = ScaleGestureDetector(context, object : ScaleGestureDetector.SimpleOnScaleGestureListener() {
        override fun onScale(detector: ScaleGestureDetector): Boolean {
            zoomBy(detector.scaleFactor, detector.focusX, detector.focusY)
            return true
        }
    })

    private val gestureDetector = GestureDetector(context, object : GestureDetector.SimpleOnGestureListener() {
        override fun onDown(e: MotionEvent): Boolean = true

        override fun onDoubleTap(e: MotionEvent): Boolean {
            val target = if (currentScale > minScale * 1.05f) minScale else minScale * 2.5f
            zoomBy(target / currentScale, e.x, e.y)
            updateParentIntercept()
            return true
        }

        override fun onScroll(e1: MotionEvent?, e2: MotionEvent, dx: Float, dy: Float): Boolean {
            if (currentScale <= minScale * 1.02f) return false
            drawMatrix.postTranslate(-dx, -dy)
            clampTranslation()
            imageMatrix = drawMatrix
            return true
        }
    })

    init {
        scaleType = ScaleType.MATRIX
    }

    override fun setImageDrawable(drawable: Drawable?) {
        super.setImageDrawable(drawable)
        fitToView()
    }

    override fun onSizeChanged(w: Int, h: Int, oldw: Int, oldh: Int) {
        super.onSizeChanged(w, h, oldw, oldh)
        fitToView()
    }

    override fun onTouchEvent(event: MotionEvent): Boolean {
        if (drawable == null) return super.onTouchEvent(event)
        scaleDetector.onTouchEvent(event)
        gestureDetector.onTouchEvent(event)
        when (event.actionMasked) {
            MotionEvent.ACTION_DOWN, MotionEvent.ACTION_POINTER_DOWN, MotionEvent.ACTION_MOVE ->
                updateParentIntercept(forceBlock = event.pointerCount > 1)
            MotionEvent.ACTION_UP, MotionEvent.ACTION_CANCEL -> parent?.requestDisallowInterceptTouchEvent(false)
        }
        return true
    }

    private fun updateParentIntercept(forceBlock: Boolean = false) {
        val zoomed = currentScale > minScale * 1.02f
        parent?.requestDisallowInterceptTouchEvent(zoomed || forceBlock)
    }

    private fun fitToView() {
        val d = drawable ?: return
        if (width == 0 || height == 0) return
        val dw = d.intrinsicWidth.toFloat()
        val dh = d.intrinsicHeight.toFloat()
        if (dw <= 0 || dh <= 0) return
        val scale = minOf(width / dw, height / dh)
        drawMatrix.reset()
        drawMatrix.postScale(scale, scale)
        drawMatrix.postTranslate((width - dw * scale) / 2f, (height - dh * scale) / 2f)
        minScale = scale
        currentScale = scale
        imageMatrix = drawMatrix
    }

    private fun zoomBy(factor: Float, focusX: Float, focusY: Float) {
        val target = (currentScale * factor).coerceIn(minScale, minScale * maxZoom)
        val applied = target / currentScale
        drawMatrix.postScale(applied, applied, focusX, focusY)
        currentScale = target
        clampTranslation()
        imageMatrix = drawMatrix
    }

    private fun clampTranslation() {
        val d = drawable ?: return
        val rect = RectF(0f, 0f, d.intrinsicWidth.toFloat(), d.intrinsicHeight.toFloat())
        drawMatrix.mapRect(rect)
        var dx = 0f
        var dy = 0f
        dx = when {
            rect.width() <= width -> (width - rect.width()) / 2f - rect.left
            rect.left > 0 -> -rect.left
            rect.right < width -> width - rect.right
            else -> 0f
        }
        dy = when {
            rect.height() <= height -> (height - rect.height()) / 2f - rect.top
            rect.top > 0 -> -rect.top
            rect.bottom < height -> height - rect.bottom
            else -> 0f
        }
        drawMatrix.postTranslate(dx, dy)
        drawMatrix.getValues(matrixValues)
    }
}
