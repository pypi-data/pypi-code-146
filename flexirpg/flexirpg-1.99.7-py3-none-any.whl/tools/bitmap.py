# Utilities for managing bitmaps
#
# Copyright 2010,2020 David Vrabel
#
import io
import os

import numpy as np
from PIL import Image
import wx

from orpg.config import Paths


def create_from_file(filename):
    return wx.Bitmap(Paths.image(filename))

class ColorIcon:
    """Generate bitmaps color picker icons from a template image."""
    key_color = 0xff00ff # Magenta

    def __init__(self, template_filename: str):
        template_path = Paths.image(template_filename)
        image = Image.open(template_path).convert("RGBA")
        self.pixels = np.array(image).reshape((-1,)).view(dtype=np.uint32)
        self.mask = (self.pixels & 0xffffff) == self.key_color
        self.width = image.width
        self.height = image.height

    def bitmap(self, color: wx.Colour):
        """Return a new bitmap for 'color', using the template."""
        colored_pixels = np.where(self.mask, color.GetRGBA(), self.pixels)
        return wx.Bitmap.FromBufferRGBA(self.width, self.height, colored_pixels)
