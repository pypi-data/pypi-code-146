# FlexiRPG -- Button for selecting colors.
#
# Copyright (C) 2020 David Vrabel
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.

import wx

import orpg.tools.bitmap

ColorSelectedType = wx.NewEventType()
EVT_COLOR_SELECTED = wx.PyEventBinder(ColorSelectedType)

class ColorSelectedEvent(wx.PyCommandEvent):
    def __init__(self, evt_type):
        wx.PyCommandEvent.__init__(self, evt_type)


class ColorSelectorButton(wx.BitmapButton):
    """A button for selecting a colour.

    The selected colour is shown on the button and can be get/set
    using the 'color' property.

    """

    def __init__(self, parent, color=wx.BLACK, tooltip="Color"):
        super().__init__(parent)

        self._color = wx.Colour(color)
        self._icon = orpg.tools.bitmap.ColorIcon("tool_color.png")
        self.Bitmap = self._icon.bitmap(self._color)
        self.SetToolTip(wx.ToolTip(tooltip))

        self.Bind(wx.EVT_BUTTON, self._on_button)

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, v):
        self._color.RGBA = v.RGBA
        self.Bitmap = self._icon.bitmap(self._color)

    def _on_button(self, evt):
        data = wx.ColourData()
        data.SetChooseFull(True)
        with wx.ColourDialog(self, data) as dlg:
            if dlg.ShowModal() == wx.ID_OK:
                self.color = dlg.GetColourData().GetColour()
                wx.PostEvent(self, ColorSelectedEvent(ColorSelectedType))
