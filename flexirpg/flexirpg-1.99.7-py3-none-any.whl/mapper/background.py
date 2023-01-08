# Copyright (C) 2000-2001 The OpenRPG Project
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.

import urllib.request, urllib.parse, urllib.error
import os.path
import time

from orpg.lib.imageid import ImageId
from orpg.main import image_library
from orpg.mapper.base import *

class layer_back_ground(layer_base):
    def __init__(self, canvas):
        layer_base.__init__(self)

        self.canvas = canvas
        self.image = None
        self.clear()

    def clear(self):
        self.set_color(wx.WHITE)
        self.set_image(None)

    def set_color(self, color):
        self.isUpdated = True
        self.bg_color = color
        self.canvas.SetBackgroundColour(self.bg_color)

    def set_image(self, image):
        self.isUpdated = True
        if self.image:
            self.image.del_hook(self._set_image_callback)
        self.image = image
        if self.image:
            self.image.add_hook(self._set_image_callback)

    def _set_image_callback(self, image):
        self.canvas.Refresh()

    def layerDraw(self, dc, topleft, size):
        if self.image and self.image.has_image():
            dc.DrawBitmap(self.image.bitmap, 0, 0)

    def layerToXML(self, action="update"):
        xml_str = '<bg'
        xml_str += ' color="%s"' % self.bg_color.GetAsString(wx.C2S_HTML_SYNTAX)
        if self.image:
            xml_str += ' image-id="%s"' % self.image.image_id
        else:
            xml_str += ' image-id=""'
        xml_str += "/>"
        if (action == "update" and self.isUpdated) or action == "new":
            self.isUpdated = False
            return xml_str
        else:
            return ''

    def layerTakeDOM(self, xml_dom):
        self.clear()

        if xml_dom.hasAttribute("color"):
            color = wx.Colour(xml_dom.getAttribute("color"))
            self.set_color(color)

        if xml_dom.hasAttribute("image-id"):
            image_id = xml_dom.getAttribute("image-id")
            if image_id:
                image_id = ImageId(image_id)
                self.set_image(image_library.get(image_id))

        # Backward compatibility.
        elif xml_dom.hasAttribute("image-uuid"):
            image = image_library.get_from_uuid(xml_dom.getAttribute("image-uuid"))
            if image:
                self.set_image(image)
