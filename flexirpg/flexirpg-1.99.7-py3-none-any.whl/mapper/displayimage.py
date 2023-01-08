# Copyright (C) 2018 David Vrabel
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.

import io
import wx

import orpg.mapper.image as image

class DisplayImage(image.Image):
    """An image that can be displayed in a wx.Widget -- it has a wx.Image.
    """
    def __init__(self, image_id, size = None):
        image.Image.__init__(self, image_id, size)

        if size:
            # Create a place holder image to be displayed before the real
            # image has been fetched.
            pixels = [(0x0, 0x0, 0x0, 0x0)] * self.width * self.height

            for x in range(self.width):
                for y in range(self.height):
                    if x > 2 and x < self.width-3 and y > 2 and y < self.height-3:
                        continue
                    if (x + y) % 6 < 3:
                        colour = (230, 242, 64, 255) # Yellowish
                    else:
                        colour = (0, 0, 0, 255) # Black
                    pixels[x + y*self.width] = colour

            s = b""
            for p in pixels:
                s += b"%c%c%c%c" % (p[0], p[1], p[2], p[3])

            self.bitmap = wx.Bitmap.FromBufferRGBA(self.width, self.height, s)
            self.wximage = self.bitmap.ConvertToImage()

    def _set_image_done(self):
        self.wximage = wx.Image(io.BytesIO(self.data), self.mime_type)
        self.size = (self.wximage.GetWidth(), self.wximage.GetHeight())
        self.bitmap = wx.Bitmap(self.wximage)
