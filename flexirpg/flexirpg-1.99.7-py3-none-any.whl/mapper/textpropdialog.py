# FlexiRPG -- Map text properties dialog
#
# Copyright (C) 2020 David Vrabel
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.

from collections import namedtuple
import copy

import wx

import orpg.tools.bitmap
import orpg.lib.ui as ui

class TextProperties:
    def __init__(self, text="", pointsize=12,
                 color=wx.BLACK, bold=False, italic=False):
        self.text = text
        self.pointsize = pointsize
        self.color = wx.Colour(color)
        self.bold = bold
        self.italic = italic

class TextPropDialog(wx.Dialog):
    def __init__(self, parent):
        super().__init__(parent, title="Text Properties", style=wx.DEFAULT_DIALOG_STYLE)

        self._default_props = TextProperties()

        self.text_box = wx.TextCtrl(self, size=(300, -1))
        self.point_control = wx.SpinCtrl(self, min=6, max=32, initial=12)

        self.color_icon = orpg.tools.bitmap.ColorIcon("tool_color.png")
        self.color_btn = ui.ColorSelectorButton(self, tooltip="Text Color")

        self.bold_check = wx.CheckBox(self, label="Bold")
        self.italic_check = wx.CheckBox(self, label="Italic")

        vbox = wx.BoxSizer(wx.VERTICAL)

        vbox.Add(ui.StaticTextHeader(self, label="Text"))
        vbox.Add((0, 6))
        vbox.Add(self.text_box, 0, wx.EXPAND | wx.LEFT, border=12)
        vbox.Add((0, 12))

        vbox.Add(ui.StaticTextHeader(self, label="Format"))
        vbox.Add((0, 6))
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        hbox.Add(wx.StaticText(self, label="Size"), 0, wx.ALIGN_CENTRE_VERTICAL)
        hbox.Add(self.point_control, 0, wx.LEFT, border=6)
        hbox.Add(wx.StaticText(self, label="points"), 0,
                 wx.ALIGN_CENTRE_VERTICAL | wx.LEFT, border=6)
        vbox.Add(hbox, 0, wx.LEFT, border=12)
        vbox.Add((0, 6))
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        hbox.Add(self.color_btn, 0, wx.ALIGN_CENTRE_VERTICAL)
        hbox.Add(self.bold_check, 0, wx.ALIGN_CENTRE_VERTICAL | wx.LEFT, border=6)
        hbox.Add(self.italic_check, 0, wx.ALIGN_CENTRE_VERTICAL | wx.LEFT, border=6)
        vbox.Add(hbox, 0, wx.EXPAND | wx.LEFT, border=12)

        self.box = wx.BoxSizer(wx.VERTICAL)
        self.box.Add(vbox, 0, wx.ALL, border=12)
        self.box.Add(self.CreateButtonSizer(wx.CANCEL | wx.OK), 0, wx.ALIGN_RIGHT)
        self.box.AddSpacer(12)
        self.box.SetSizeHints(self)

        self.SetSizer(self.box)
        self.SetAutoLayout(True)
        self.Fit()

    @property
    def properties(self):
        return TextProperties(text=self.text_box.Value,
                              pointsize=self.point_control.Value,
                              color=self.color_btn.color,
                              bold=self.bold_check.IsChecked(),
                              italic=self.italic_check.IsChecked())

    def show(self, text_obj=None):
        if text_obj is None:
            self.text_box.Value      = self._default_props.text
            self.point_control.Value = self._default_props.pointsize
            self.color_btn.color     = self._default_props.color
            self.bold_check.Value    = self._default_props.bold
            self.italic_check.Value  = self._default_props.italic
        else:
            self.text_box.Value      = text_obj.text_string
            self.point_control.Value = text_obj.pointsize
            self.color_btn.color     = text_obj.textcolor
            self.bold_check.Value    = text_obj.bold
            self.italic_check.Value  = text_obj.italic

        self.text_box.SetFocus()
        ret = self.ShowModal()

        if ret == wx.ID_OK:
            if text_obj is None:
                self._default_props.pointsize  = self.point_control.Value
                self._default_props.color.RGBA = self.color_btn.color.RGBA
                self._default_props.bold       = self.bold_check.IsChecked()
                self._default_props.italic     = self.italic_check.IsChecked()
            else:
                text_obj.set_text_props(self.text_box.Value.strip(),
                                        self.point_control.Value,
                                        self.color_btn.color,
                                        self.bold_check.IsChecked(),
                                        self.italic_check.IsChecked())
        return ret
