# Bitmap button
#
# Copyright (C) 2021 David Vrabel
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.

import wx

from orpg.config import Paths
from orpg.tools.bitmap import create_from_file

class BitmapButton(wx.BitmapButton):
    """
    Bitmap button.

    This is a wrapper for wx.BitmapButton.
    """
    def __init__(self, parent, image_name, tooltip):
        super().__init__(
            parent,
            bitmap=create_from_file(Paths.image(image_name))
        )
        self.SetToolTip(wx.ToolTip(tooltip))
