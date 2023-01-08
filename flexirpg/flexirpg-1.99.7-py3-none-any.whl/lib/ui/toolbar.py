# Toolbar with additional helpers.
#
# Copyright 2020 David Vrabel
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.

import wx

import orpg.tools.bitmap
from .iconselector import IconSelectorPopup, EVT_ICON_SELECTED, EVT_ICON_MORE

class IconSelectorTool(IconSelectorPopup):
    def __init__(self, toolbar, toolid, icons, selector):
        IconSelectorPopup.__init__(self, toolbar, icons, more=selector is not None)
        self._toolbar = toolbar
        self._toolid = toolid
        self._selector = selector
        toolbar.Bind(EVT_ICON_SELECTED, self.on_icon_selected)
        toolbar.Bind(EVT_ICON_MORE, self.on_icon_more)

    def on_icon_selected(self, evt):
        icon = self._icons[evt.GetId()]
        self._toolbar.SetSelected(self._toolid, icon)

    def on_icon_more(self, evt):
        icon = self._selector.select()
        if icon is None:
            # No icon was selected, check if the current one is still valid.
            icon = self._toolbar.GetSelected(self._toolid)
            if icon not in self._icons:
                icon = self._icons[0]
        self._toolbar.SetSelected(self._toolid, icon)

class ToolBar(wx.ToolBar):
    """A toolbar with support for some specialized buttons."""
    def __init__(self, parent, *args, **kwargs):
        wx.ToolBar.__init__(self, parent, *args, **kwargs)
        self.SetToolBitmapSize(wx.Size(24, 24))
        self._selected = {}
        self._more_bitmap = orpg.tools.bitmap.create_from_file("tool_more.png")

    def AddIconSelector(self, toolid, label, icons, shortHelp=""):
        """Add a button which can choose an icon."""
        self.AddTool(toolid, label, wx.Bitmap(self.GetToolBitmapSize()), shortHelp=shortHelp)
        self.SetToolClientData(toolid, icons)
        self.SetSelected(toolid, icons[0])

    def SetSelected(self, toolid, icon):
        """Set the selected icon for a tool."""
        icons = self.GetToolClientData(toolid)
        self._selected[toolid] = icon
        if icon:
            self.SetToolNormalBitmap(toolid, icon.tool_bitmap(self))
        else:
            self.SetToolNormalBitmap(toolid, self._more_bitmap)

    def GetSelected(self, toolid):
        """Get the icon selected by a tool."""
        return self._selected.get(toolid, None)

    def PopupIconSelector(self, toolid, selector=None):
        icons = self.GetToolClientData(toolid)
        if icons.count() > 0:
            tool = IconSelectorTool(self, toolid, icons, selector)
            (x, y) = self.GetScreenPosition()
            tx = self.GetToolPos(toolid) * self.GetToolSize().x
            sy = self.GetClientSize().y
            tool.Position((x + tx, y), (0, sy))
            tool.Popup()
        else:
            icon = selector.select()
            self.SetSelected(toolid, icon)
