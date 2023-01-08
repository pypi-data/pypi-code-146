# Dialog for selecting multiple items from a list.
#
# Copyright (C) 2020 David Vrabel
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.

import wx

from .statictextheader import StaticTextHeader

class MultiCheckBoxDialog(wx.Dialog):
    """Dialog for selecting zero or more items from a list."""

    def __init__(self, parent, title, label, options):
        """Constructor.

        Parameters
        * parent (wx.Window) - parent window.
        * title (string)     - The title of the dialog.
        * label (string)     - The label for the list box.
        * options (list)     - A list of (object, name, checked) tuples.
        """
        wx.Dialog.__init__(self, parent, wx.ID_ANY, title)

        self._options = options
        self._checked = []

        self.check_list = wx.CheckListBox(self, choices=[o[1] for o in options])
        for i, (_, _, check) in enumerate(options):
            self.check_list.Check(i, check)

        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(StaticTextHeader(self, -1, label), 0, 0)
        vbox.Add((0, 6))

        hbox = wx.BoxSizer(wx.HORIZONTAL)
        hbox.Add((12, 0))
        hbox.Add(self.check_list, 0, wx.EXPAND)

        vbox.Add(hbox)
        vbox.Add((0, 12))
        bbox = self.CreateButtonSizer(wx.OK | wx.CANCEL)
        if bbox:
            vbox.Add(bbox, 0, wx.EXPAND)

        self.box = wx.BoxSizer(wx.VERTICAL)
        self.box.Add(vbox, 1, wx.EXPAND | wx.ALL, border = 12)
        self.box.Layout()
        self.SetSizer(self.box)
        self.SetAutoLayout(True)
        self.Fit()

        self.Bind(wx.EVT_BUTTON, self.on_ok, id=wx.ID_OK)

    def on_ok(self,evt):
        for i, (opt, _, _) in enumerate(self._options):
            if self.check_list.IsChecked(i):
                self.checked.append(opt)
        self.EndModal(wx.ID_OK)

    @property
    def checked(self):
        """Return a list of checked objects."""
        return self._checked
