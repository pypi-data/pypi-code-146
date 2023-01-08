# Icon selector buttons.
#
# Copyright (C) 2011 David Vrabel
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.

import math
from itertools import chain

import wx

import orpg.tools.bitmap

IconSelectedType = wx.NewEventType()
IconMoreType = wx.NewEventType()
EVT_ICON_SELECTED = wx.PyEventBinder(IconSelectedType)
EVT_ICON_MORE = wx.PyEventBinder(IconMoreType)

class IconSelectedEvent(wx.PyCommandEvent):
    def __init__(self, evt_type, id):
        wx.PyCommandEvent.__init__(self, evt_type, id)

class IconMoreEvent(wx.PyCommandEvent):
    def __init__(self, evt_type):
        wx.PyCommandEvent.__init__(self, evt_type)

class IconSelectorButton(wx.BitmapButton):
    def __init__(self, parent, icons, selected = 0):
        wx.BitmapButton.__init__(self, parent, wx.ID_ANY,
                                wx.Bitmap(icons.image(selected)))

        self._icons = icons
        self._popup = IconSelectorPopup(self, icons)

        self.Bind(wx.EVT_BUTTON, self.on_button)
        self.Bind(EVT_ICON_SELECTED, self.on_icon_selected)

    def on_button(self, evt):
        (x, y) = self.GetScreenPosition()
        (w, h) = self.GetSize()
        self._popup.Position((x, y), (0, h))
        self._popup.Popup()

    def on_icon_selected(self, evt):
        self.SetBitmapLabel(wx.Bitmap(self._icons.image(evt.GetId())))
        evt.Skip()

class IconSelectorPopup(wx.PopupTransientWindow):

    COLUMNS_MAX_DEFAULT = 15
    WINDOW_BORDER = 1
    ICON_BORDER = 3

    def __init__(self, parent, icons, more=False):
        wx.PopupTransientWindow.__init__(self, parent, flags = wx.BORDER_SIMPLE)

        self._icons = icons
        self._more = more
        self._more_bitmap = orpg.tools.bitmap.create_from_file("tool_more.png")
        self._icon_size = self._max_icon_dimension()
        self._max_columns = self.COLUMNS_MAX_DEFAULT
        self._selected = None

        self.SetBackgroundStyle(wx.BG_STYLE_CUSTOM)

        (self.cols, self.rows) = self._grid_size()
        if more:
            self._more_index = self.cols * self.rows - 1

        self._spacing = self._icon_size + 2 * self.ICON_BORDER + self.WINDOW_BORDER

        w = self.cols * self._spacing + self.WINDOW_BORDER
        h = self.rows * self._spacing + self.WINDOW_BORDER

        self.SetSize((w, h))

        self.Bind(wx.EVT_PAINT, self.on_paint)
        self.Bind(wx.EVT_MOUSE_EVENTS, self.on_mouse)
        self.Bind(wx.EVT_KEY_DOWN, self.on_key_down)

    def _max_icon_dimension(self):
        d = max(self._more_bitmap.Width, self._more_bitmap.Height)
        for i in range(self._icons.count()):
            (w, h) = self._icons.image(i).GetSize()
            if w > d:
                d = w
            if h > d:
                d = h
        return d

    def _grid_size(self):
        num_icons = self._icons.count()
        if num_icons == 0:
            return (1, 1)

        # Aim for a roughly square grid of icons, but not too wide.
        cols = math.ceil(math.sqrt(num_icons))
        if cols > self._max_columns:
            cols = self._max_columns
        rows = (num_icons + cols - 1) // cols

        # Add extra column for the "..." button if needed.
        if self._more and cols * rows == num_icons:
            cols += 1

        return (cols, rows)

    def on_paint(self, evt):
        (w, h) = self.GetClientSize()
        sp = self._spacing
        wb = self.WINDOW_BORDER

        dc = wx.AutoBufferedPaintDC(self)
        rn = wx.RendererNative.GetDefault()

        dc.SetBrush(wx.Brush(wx.WHITE))
        dc.SetPen(wx.Pen(wx.LIGHT_GREY))
        dc.DrawRectangle(0, 0, w, h)

        for i in chain(
                range(self._icons.count()),
                [self._more_index] if self._more else []):
            x = wb + i % self.cols * sp
            y = wb + i // self.cols * sp
            if i == self._selected:
                rn.DrawItemSelectionRect(self, dc, (x, y, sp - wb, sp - wb),
                                         wx.CONTROL_SELECTED | wx.CONTROL_FOCUSED)
            if i < self._icons.count():
                bmp = wx.Bitmap(self._icons.image(i))
            else:
                bmp = self._more_bitmap
            dc.DrawBitmap(bmp, x + (sp - bmp.Width) // 2, y + (sp - bmp.Height) // 2, True)

        dc.SetPen(wx.Pen(wx.LIGHT_GREY))
        for c in range(1, self.cols):
            x = wb + c * sp
            dc.DrawLine(x-1, 1, x-1, h - 1)
            for r in range(1,self.rows):
                y = wb + r * sp
                dc.DrawLine(1, y-1, w-1, y-1)

    def on_key_down(self, evt):
        if evt.GetKeyCode() == wx.WXK_ESCAPE:
            self.Dismiss()

    def on_mouse(self, evt):
        sel = None

        (w, h) = self.GetClientSize()
        (x, y) = evt.GetPosition()
        wb = self.WINDOW_BORDER
        x -= wb
        y -= wb
        if 0 <= x < (w - wb) and 0 <= y < (h - wb):
            c = x // self._spacing
            r = y // self._spacing
            i = c + r * self.cols
            if i < self._icons.count() or (self._more and i == self._more_index):
                sel = i
        if sel != self._selected:
            self._selected = sel
            self.Refresh()

        if evt.LeftDown() and self._selected is not None:
            if i < self._icons.count():
                evt = IconSelectedEvent(IconSelectedType, i)
            else:
                evt = IconMoreEvent(IconMoreType)
            wx.PostEvent(self.GetParent(), evt)
            self.Dismiss()
