# FlexiRPG -- Compose miniature images from a set of parameters.
#
# Copyright (C) 2021 David Vrabel
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
import math

import wx

class MiniatureComposer:
    def __init__(self):
        self._size = (20, 20)
        self.edge_color = wx.Colour(wx.BLACK)
        self.border_color = wx.Colour(wx.RED)
        self.fill_color = wx.Colour(wx.WHITE)
        self.text_color = wx.Colour(wx.BLACK)
        self.text = "X"

        self._resize()

    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, v):
        self._size = v
        self._resize()

    def bitmap(self) -> wx.Bitmap:
        sx = self._size[0]
        sy = self._size[1]
        cx = sx / 2 - 0.5
        cy = sy / 2 - 0.5
        r = min(sx, sy) / 2

        dc = wx.MemoryDC()
        dc.SelectObject(self._bitmap)
        dc.SetBackground(wx.Brush(wx.Colour(0, 0, 0, wx.ALPHA_TRANSPARENT)))
        dc.Clear()
        gc = wx.GraphicsContext.Create(dc)

        border = gc.CreatePath()
        border.AddCircle(cx, cy, r - 0.5)
        gc.SetPen(wx.Pen(self.edge_color))
        gc.SetBrush(wx.Brush(self.border_color))
        gc.DrawPath(border)

        fill = gc.CreatePath()
        fill.AddCircle(cx, cy, r * 0.6)
        gc.SetBrush(wx.Brush(self.fill_color))
        gc.FillPath(fill)

        points = math.floor(math.sqrt(2) * (r * 0.6) / gc.GetDPI()[0] * 72)
        gc.SetFont(wx.Font(points, wx.FONTFAMILY_MODERN,
                           wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL),
                   self.text_color)
        (tw, th, _, _) = gc.GetFullTextExtent(self.text)
        gc.DrawText(self.text, cx - tw / 2 + 0.5, cy - th / 2 + 0.5)

        dc.SelectObject(wx.NullBitmap)
        return self._bitmap

    def _resize(self):
        pixels = bytes(self._size[0] * self._size[1] * 4)
        self._bitmap = wx.Bitmap.FromBufferRGBA(self._size[0], self._size[1], pixels)
