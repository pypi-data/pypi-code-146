# Static text control for headings
#
# Copyright (C) 2011 David Vrabel
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.

import wx

class StaticTextHeader(wx.StaticText):
    """
    Static text control for dialog headings.

    This is the same as the wx.StaticText control except (as per the
    Gnome HIG) the font is bold.
    """
    def __init__(self, parent, *args, **kwargs):
        wx.StaticText.__init__(self, parent, *args, **kwargs)
        font = self.GetFont()
        font.SetWeight(wx.FONTWEIGHT_BOLD)
        self.SetFont(font)
