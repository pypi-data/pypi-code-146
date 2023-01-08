# FlexiRPG -- Settings dialog
#
# Copyright 2021 David Vrabel
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.

import wx

from orpg.config import Settings
import orpg.lib.ui as ui


class SettingsDialog(wx.Dialog):
    """A dialog for user-editable settings/preferences."""

    def __init__(self, parent):
        super().__init__(parent,
                         title="Preferences",
                         style=wx.DEFAULT_DIALOG_STYLE)

        # The configurable settings.
        self.name = Settings.lookup("player.name")
        self.status = Settings.lookup("player.status")
        self.color = Settings.lookup("chat.color.player")

        self.whisper_tabs = Settings.lookup("chat.use_whisper_tab")
        self.gm_tabs = Settings.lookup("chat.use_gm_whisper_tabs")
        self.group_tabs = Settings.lookup("chat.use_group_whisper_tabs")

        self.macros = [Settings.lookup(f"chat.macro.f{f}") for f in range(12)]

        # Controls
        self.name_text = wx.TextCtrl(self)
        self.status_text = wx.TextCtrl(self, size=(300, -1))
        self.color_selector = ui.ColorSelectorButton(self, tooltip="Player Color")

        self.whisper_tab_check = wx.CheckBox(self, label="Anyone")
        self.gm_tab_check = wx.CheckBox(self, label="GMs")
        self.group_tab_check = wx.CheckBox(self, label="Groups")

        self.macro_texts = [wx.TextCtrl(self, size=(300, -1)) for f in range(12)]

        # Layout
        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(ui.StaticTextHeader(self, label="Player"), 0, wx.BOTTOM, border=12)
        fbox = wx.FlexGridSizer(rows=3, cols=2, hgap=6, vgap=1)
        fbox.AddGrowableCol(1)
        fbox.Add(wx.StaticText(self, label="Name"), 0, wx.ALIGN_CENTRE_VERTICAL)
        fbox.Add(self.name_text, 1, wx.EXPAND)
        fbox.Add(wx.StaticText(self, label="Status"), 0, wx.ALIGN_CENTRE_VERTICAL)
        fbox.Add(self.status_text, 1, wx.EXPAND)
        fbox.Add(wx.StaticText(self, label="Color"), 0, wx.ALIGN_CENTRE_VERTICAL)
        fbox.Add(self.color_selector)
        vbox.Add(fbox, 0, wx.EXPAND | wx.LEFT | wx.BOTTOM, border=12)

        vbox.Add(ui.StaticTextHeader(self, label="Chat"), 0, wx.BOTTOM, border=12)
        vbox.Add(wx.StaticText(self, label="Use Tabs for Whispers Between"), 0, wx.LEFT, border=12)
        vbox.AddSpacer(6)
        vbox.Add(self.whisper_tab_check, 0, wx.LEFT, border=24)
        vbox.Add(self.gm_tab_check, 0, wx.LEFT, border=24)
        vbox.Add(self.group_tab_check, 0, wx.LEFT, border=24)
        vbox.AddSpacer(12)

        vbox.Add(ui.StaticTextHeader(self, label="Macros"), 0, wx.BOTTOM, border=12)
        fbox = wx.FlexGridSizer(rows=12, cols=2, hgap=6, vgap=1)
        fbox.AddGrowableCol(1)
        for f, text in enumerate(self.macro_texts):
            fbox.Add(wx.StaticText(self, label=f"F{f+1}"), 0, wx.ALIGN_CENTRE_VERTICAL)
            fbox.Add(text, 1, wx.EXPAND)
        vbox.Add(fbox, 0, wx.EXPAND | wx.LEFT, border=12)

        self.box = wx.BoxSizer(wx.VERTICAL)
        self.box.Add(vbox, 0, wx.ALL, border=12)
        self.box.Add(self.CreateButtonSizer(wx.CANCEL | wx.OK), 0, wx.ALIGN_RIGHT)
        self.box.AddSpacer(12)
        self.box.SetSizeHints(self)

        self.SetSizer(self.box)
        self.SetAutoLayout(True)
        self.Fit()

    def show(self):
        self.name_text.Value = self.name.value
        self.status_text.Value = self.status.value
        self.color_selector.color = self.color.value
        
        self.whisper_tab_check.Value = self.whisper_tabs.value
        self.gm_tab_check.Value = self.gm_tabs.value
        self.group_tab_check.Value = self.group_tabs.value

        for setting, text in zip(self.macros, self.macro_texts):
            text.Value = setting.value

        if self.ShowModal() == wx.ID_OK:
            self.name.value = self.name_text.Value
            self.status.value = self.status_text.Value
            self.color.value = self.color_selector.color

            self.whisper_tabs.value = self.whisper_tab_check.Value
            self.gm_tabs.value = self.gm_tab_check.Value
            self.group_tabs.value = self.group_tab_check.Value

            for setting, text in zip(self.macros, self.macro_texts):
                setting.value = text.Value
