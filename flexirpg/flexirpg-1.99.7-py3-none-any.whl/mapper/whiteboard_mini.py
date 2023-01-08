# FlexiRPG -- Whiteboard miniatures
#
# Copyright (C) 2000-2001 The OpenRPG Project
# Copyright (C) 2009-2010 David Vrabel
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.

import time

from orpg.config import Settings
from orpg.lib.imageid import ImageId
from orpg.mapper.exceptions import MiniatureImageMissing
from orpg.mapper.base import *
from orpg.mapper.whiteboard_object import WhiteboardObject
from orpg.main import image_library
from orpg.networking.roles import *

FACE_NONE = 0
FACE_NORTH = 1
FACE_NORTHEAST = 2
FACE_EAST = 3
FACE_SOUTHEAST = 4
FACE_SOUTH = 5
FACE_SOUTHWEST = 6
FACE_WEST = 7
FACE_NORTHWEST = 8
SNAPTO_ALIGN_CENTER = 0
SNAPTO_ALIGN_TL = 1

class WhiteboardMini(WhiteboardObject):

    show_labels = Settings.define("map.mini.label.show", False)
    label_font = Settings.define("map.mini.label.font", "")
    label_font_size = Settings.define("map.mini.label.font_size", 0)

    def __init__(self, window, id, image=None, pos=None, label=""):
        WhiteboardObject.__init__(self, window, id)
        if pos is None:
            pos = cmpPoint(0, 0)
        if image:
            self.width = image.width
            self.height = image.height
            self._set_image(image)
        else:
            self.image = None
            self.width = 0
            self.height = 0
        self.heading = FACE_NONE
        self.face = FACE_NONE
        self.label = label
        self.pos = pos
        self.locked = False
        self.hide = False
        self.left = 0
        self.right = 0
        self.top = 0
        self.bottom = 0
        font_size = self.label_font_size.value
        if not font_size:
            font_size = -1
        self.label_font = wx.Font(font_size, wx.FONTFAMILY_DEFAULT,
                                  wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False,
                                  self.label_font.value)

    def destroy(self):
        if self.image:
            self.image.del_hook(self._set_image_callback)

    def _set_image(self, image):
        self.image = image
        self.image.add_hook(self._set_image_callback)
        self.generate_bmps()

    def _set_image_callback(self, image):
        self.generate_bmps()
        self._updated()

    def generate_bmps(self):
        if self.width != self.image.width or self.height != self.image.height:
            image = self.image.wximage.Copy()
            image.Rescale(int(self.width), int(self.height))
            self.bmp = wx.Bitmap(image)
        else:
            self.bmp = self.image.bitmap

    def set_min_props(self, heading=FACE_NONE, face=FACE_NONE, label="", locked=False, hide=False, width=0, height=0):
        self.heading = heading
        self.face = face
        self.label = label
        if locked:
            self.locked = True
        else:
            self.locked = False
        if hide:
            self.hide = True
        else:
            self.hide = False
        self.width = int(width)
        self.height = int(height)
        self.is_updated = True
        self.generate_bmps()

    def move(self, delta):
        self.pos.x += delta.x
        self.pos.y += delta.y
        self.is_updated = True

    def snap_to_grid(self, grid):
        self.pos = grid.get_snapped_to_pos(self.pos, self.bmp.GetWidth(), self.bmp.GetHeight())

    def hit_test(self, pt):
        rect = self.get_rect()
        result = None
        result = rect.Contains(pt)
        return result

    def get_rect(self):
        ret = wx.Rect(self.pos.x, self.pos.y, self.bmp.GetWidth(), self.bmp.GetHeight())
        return ret

    def draw_object(self, layer, dc):
        dc.SetFont(self.label_font)

        # check if hidden and GM: we outline the mini in grey (little
        # bit smaller than the actual size) and write the label in the
        # center of the mini
        if self.hide and layer.canvas.frame.session.allowed(ROLE_GM):
            self.left = 0
            self.right = self.bmp.GetWidth()
            self.top = 0
            self.bottom = self.bmp.GetHeight()
            # grey outline
            graypen = wx.Pen("gray", 1, wx.DOT)
            dc.SetPen(graypen)
            dc.SetBrush(wx.TRANSPARENT_BRUSH)
            if self.bmp.GetWidth() <= 20:
                xoffset = 1
            else:
                xoffset = 5
            if self.bmp.GetHeight() <= 20:
                yoffset = 1
            else:
                yoffset = 5
            dc.DrawRectangle(self.pos.x + xoffset, self.pos.y + yoffset,
                             self.bmp.GetWidth() - (xoffset * 2),
                             self.bmp.GetHeight() - (yoffset * 2))
            dc.SetBrush(wx.NullBrush)
            dc.SetPen(wx.NullPen)

            ## draw label in the center of the mini
            if self.show_labels.value:
                if len(self.label):
                    dc.SetTextForeground(wx.RED)
                    (textWidth,textHeight) = dc.GetTextExtent(self.label)
                    x = self.pos.x +((self.bmp.GetWidth() - textWidth) /2) - 1
                    y = self.pos.y + (self.bmp.GetHeight() / 2)
                    dc.SetPen(wx.GREY_PEN)
                    dc.SetBrush(wx.LIGHT_GREY_BRUSH)
                    dc.DrawRectangle(x, y, textWidth+2, textHeight+2)
                    if (textWidth+2 > self.right):
                        self.right += int((textWidth+2-self.right)/2)+1
                        self.left -= int((textWidth+2-self.right)/2)+1
                    self.bottom = y+textHeight+2-self.pos.y
                    dc.SetPen(wx.NullPen)
                    dc.SetBrush(wx.NullBrush)
                    dc.DrawText(self.label, x+1, y+1)
            return True

        elif not self.hide:
            # set the width and height of the image
            bmp = self.bmp
            dc.DrawBitmap(bmp, self.pos.x, self.pos.y, True)
            self.left = 0
            self.right = self.bmp.GetWidth()
            self.top = 0
            self.bottom = self.bmp.GetHeight()

            # Draw the facing marker if needed
            if self.face != 0:
                x_mid = self.pos.x + (self.bmp.GetWidth()/2)
                x_right = self.pos.x + self.bmp.GetWidth()
                y_mid = self.pos.y + (self.bmp.GetHeight()/2)
                y_bottom = self.pos.y + self.bmp.GetHeight()

                dc.SetPen(wx.WHITE_PEN)
                dc.SetBrush(wx.RED_BRUSH)
                triangle = []

                # Figure out which direction to draw the marker!!
                if self.face == FACE_WEST:
                    triangle.append(cmpPoint(self.pos.x,self.pos.y))
                    triangle.append(cmpPoint(self.pos.x - 5, y_mid))
                    triangle.append(cmpPoint(self.pos.x, y_bottom))
                elif self.face ==  FACE_EAST:
                    triangle.append(cmpPoint(x_right, self.pos.y))
                    triangle.append(cmpPoint(x_right + 5, y_mid))
                    triangle.append(cmpPoint(x_right, y_bottom))
                elif self.face ==  FACE_SOUTH:
                    triangle.append(cmpPoint(self.pos.x, y_bottom))
                    triangle.append(cmpPoint(x_mid, y_bottom + 5))
                    triangle.append(cmpPoint(x_right, y_bottom))
                elif self.face ==  FACE_NORTH:
                    triangle.append(cmpPoint(self.pos.x, self.pos.y))
                    triangle.append(cmpPoint(x_mid, self.pos.y - 5))
                    triangle.append(cmpPoint(x_right, self.pos.y))
                elif self.face == FACE_NORTHEAST:
                    triangle.append(cmpPoint(x_mid, self.pos.y))
                    triangle.append(cmpPoint(x_right + 5, self.pos.y - 5))
                    triangle.append(cmpPoint(x_right, y_mid))
                    triangle.append(cmpPoint(x_right, self.pos.y))
                elif self.face == FACE_SOUTHEAST:
                    triangle.append(cmpPoint(x_right, y_mid))
                    triangle.append(cmpPoint(x_right + 5, y_bottom + 5))
                    triangle.append(cmpPoint(x_mid, y_bottom))
                    triangle.append(cmpPoint(x_right, y_bottom))
                elif self.face == FACE_SOUTHWEST:
                    triangle.append(cmpPoint(x_mid, y_bottom))
                    triangle.append(cmpPoint(self.pos.x - 5, y_bottom + 5))
                    triangle.append(cmpPoint(self.pos.x, y_mid))
                    triangle.append(cmpPoint(self.pos.x, y_bottom))
                elif self.face == FACE_NORTHWEST:
                    triangle.append(cmpPoint(self.pos.x, y_mid))
                    triangle.append(cmpPoint(self.pos.x - 5, self.pos.y - 5))
                    triangle.append(cmpPoint(x_mid, self.pos.y))
                    triangle.append(cmpPoint(self.pos.x, self.pos.y))
                dc.DrawPolygon(triangle)
                dc.SetBrush(wx.NullBrush)
                dc.SetPen(wx.NullPen)

            # Draw the heading if needed
            if self.heading:
                x_adjust = 0
                y_adjust = 4
                x_half = self.bmp.GetWidth()/2
                y_half = self.bmp.GetHeight()/2
                x_quarter = self.bmp.GetWidth()/4
                y_quarter = self.bmp.GetHeight()/4
                x_3quarter = x_quarter*3
                y_3quarter = y_quarter*3
                x_full = self.bmp.GetWidth()
                y_full = self.bmp.GetHeight()
                x_center = self.pos.x + x_half
                y_center = self.pos.y + y_half

                # Remember, the pen/brush must be a different color than the
                # facing marker!!!!  We'll use black/cyan for starters.
                # Also notice that we will draw the heading on top of the
                # larger facing marker.
                dc.SetPen(wx.BLACK_PEN)
                dc.SetBrush(wx.CYAN_BRUSH)
                triangle = []

                # Figure out which direction to draw the marker!!
                if self.heading == FACE_NORTH:
                    triangle.append(cmpPoint(x_center - x_quarter, y_center - y_half ))
                    triangle.append(cmpPoint(x_center, y_center - y_3quarter ))
                    triangle.append(cmpPoint(x_center + x_quarter, y_center - y_half ))
                elif self.heading ==  FACE_SOUTH:
                    triangle.append(cmpPoint(x_center - x_quarter, y_center + y_half ))
                    triangle.append(cmpPoint(x_center, y_center + y_3quarter ))
                    triangle.append(cmpPoint(x_center + x_quarter, y_center + y_half ))
                elif self.heading == FACE_NORTHEAST:
                    triangle.append(cmpPoint(x_center + x_quarter, y_center - y_half ))
                    triangle.append(cmpPoint(x_center + x_3quarter, y_center - y_3quarter ))
                    triangle.append(cmpPoint(x_center + x_half, y_center - y_quarter ))
                elif self.heading == FACE_EAST:
                    triangle.append(cmpPoint(x_center + x_half, y_center - y_quarter ))
                    triangle.append(cmpPoint(x_center + x_3quarter, y_center ))
                    triangle.append(cmpPoint(x_center + x_half, y_center + y_quarter ))
                elif self.heading == FACE_SOUTHEAST:
                    triangle.append(cmpPoint(x_center + x_half, y_center + y_quarter ))
                    triangle.append(cmpPoint(x_center + x_3quarter, y_center + y_3quarter ))
                    triangle.append(cmpPoint(x_center + x_quarter, y_center + y_half ))
                elif self.heading == FACE_SOUTHWEST:
                    triangle.append(cmpPoint(x_center - x_quarter, y_center + y_half ))
                    triangle.append(cmpPoint(x_center - x_3quarter, y_center + y_3quarter ))
                    triangle.append(cmpPoint(x_center - x_half, y_center + y_quarter ))
                elif self.heading == FACE_WEST:
                    triangle.append(cmpPoint(x_center - x_half, y_center + y_quarter ))
                    triangle.append(cmpPoint(x_center - x_3quarter, y_center ))
                    triangle.append(cmpPoint(x_center - x_half, y_center - y_quarter ))
                elif self.heading == FACE_NORTHWEST:
                    triangle.append(cmpPoint(x_center - x_half, y_center - y_quarter ))
                    triangle.append(cmpPoint(x_center - x_3quarter, y_center - y_3quarter ))
                    triangle.append(cmpPoint(x_center - x_quarter, y_center - y_half ))
                dc.DrawPolygon(triangle)
                dc.SetBrush(wx.NullBrush)
                dc.SetPen(wx.NullPen)
            # draw label
            if self.show_labels.value:
                if len(self.label):
                    dc.SetTextForeground(wx.RED)
                    (textWidth,textHeight) = dc.GetTextExtent(self.label)
                    x = self.pos.x +((self.bmp.GetWidth() - textWidth) /2) - 1
                    y = self.pos.y + self.bmp.GetHeight() + 6
                    dc.SetPen(wx.WHITE_PEN)
                    dc.SetBrush(wx.WHITE_BRUSH)
                    dc.DrawRectangle(x,y,textWidth+2,textHeight+2)
                    if (textWidth+2 > self.right):
                        self.right += int((textWidth+2-self.right)/2)+1
                        self.left -= int((textWidth+2-self.right)/2)+1
                        self.bottom = y+textHeight+2-self.pos.y
                        dc.SetPen(wx.NullPen)
                        dc.SetBrush(wx.NullBrush)
                        dc.DrawText(self.label,x+1,y+1)
            self.top-=5
            self.bottom+=5
            self.left-=5
            self.right+=5
        return True

    def draw_handles(self, layer, dc):
        dc.SetPen(wx.RED_PEN)
        dc.SetBrush(wx.TRANSPARENT_BRUSH)
        dc.DrawRectangle(self.pos.x, self.pos.y, self.bmp.GetWidth(), self.bmp.GetHeight())
        dc.SetBrush(wx.NullBrush)
        dc.SetPen(wx.NullPen)

    def toxml(self, action="update"):
        if action == "del":
            xml_str = "<miniature action='del' id='" + self.id + "'/>"
            return xml_str
        xml_str = "<miniature"
        xml_str += " action='" + action + "'"
        xml_str += " label='" + self.label + "'"
        xml_str += " id='" + self.id + "'"
        xml_str += " zorder='" + str(self.z_order) + "'"
        if self.pos != None:
            xml_str += " posx='" + str(self.pos.x) + "'"
            xml_str += " posy='" + str(self.pos.y) + "'"
        if self.heading != None:
            xml_str += " heading='" + str(self.heading) + "'"
        if self.face != None:
            xml_str += " face='" + str(self.face) + "'"
        if self.image != None:
            xml_str += " image-id='%s'" % self.image.image_id
        if self.locked:
            xml_str += "  locked='1'"
        else:
            xml_str += "  locked='0'"
        if self.hide:
            xml_str += " hide='1'"
        else:
            xml_str += " hide='0'"
        if self.width != None:
            xml_str += " width='" + str(self.width) + "'"
        if self.height != None:
            xml_str += " height='" + str(self.height) + "'"
        xml_str += " />"
        if (action == "update" and self.is_updated) or action == "new":
            self.is_updated = False
            return xml_str
        else:
            return ''

    def takedom(self, xml_dom):
        self.id = xml_dom.getAttribute("id")
        if xml_dom.hasAttribute("posx"):
            self.pos.x = int(xml_dom.getAttribute("posx"))
        if xml_dom.hasAttribute("posy"):
            self.pos.y = int(xml_dom.getAttribute("posy"))
        if xml_dom.hasAttribute("heading"):
            self.heading = int(xml_dom.getAttribute("heading"))
        if xml_dom.hasAttribute("face"):
            self.face = int(xml_dom.getAttribute("face"))
        if xml_dom.hasAttribute("locked"):
            if xml_dom.getAttribute("locked") == '1' or xml_dom.getAttribute("locked") == 'True':
                self.locked = True
            else:
                self.locked = False
        if xml_dom.hasAttribute("hide"):
            if xml_dom.getAttribute("hide") == '1' or xml_dom.getAttribute("hide") == 'True':
                self.hide = True
            else:
                self.hide = False
        if xml_dom.hasAttribute("label"):
            self.label = xml_dom.getAttribute("label")
        if xml_dom.hasAttribute("width"):
            self.width = int(xml_dom.getAttribute("width"))
        if xml_dom.hasAttribute("height"):
            self.height = int(xml_dom.getAttribute("height"))

        # Get the miniature from the cache
        if xml_dom.hasAttribute("image-id"):
            image = image_library.get(ImageId(xml_dom.getAttribute("image-id")), (self.width, self.height))

        # Backward compatibility
        elif xml_dom.hasAttribute("uuid"):
            uuid = xml_dom.getAttribute("uuid")
            image = image_library.get_from_uuid(uuid)
            if image is None:
                raise MiniatureImageMissing(f"No legacy cache file for '{uuid}'")
        else:
            raise MiniatureImageMissing(f"No 'image-id' or 'uuid' attribute'")

        self._set_image(image)
