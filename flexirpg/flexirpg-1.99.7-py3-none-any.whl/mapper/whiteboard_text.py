# FlexiRPG -- Whiteboard text
#
# Copyright (C) 2000-2001 The OpenRPG Project
# Copyright (C) 2009-2010 David Vrabel
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.

from orpg.config import Settings
import orpg.lib.xmlutil as xmlutil
from orpg.mapper.base import *
from orpg.mapper.map_utils import *
from orpg.mapper.whiteboard_object import WhiteboardObject

class WhiteboardText(WhiteboardObject):

    text_font = Settings.define("map.text.font", "")

    def __init__(self, window, id, text_string="", pos=wx.Point(0,0),
                 pointsize=12, color=wx.BLACK, bold=False, italic=False):
        WhiteboardObject.__init__(self, window, id)
        self.text_string = text_string
        self.pos = wx.Point(pos)
        self.pointsize = pointsize
        self.textcolor = wx.Colour(color)
        self.bold = bold
        self.italic = italic

        self._font = wx.Font(self.pointsize,
                             wx.FONTFAMILY_DEFAULT,
                             wx.FONTSTYLE_ITALIC if italic else wx.FONTSTYLE_NORMAL,
                             wx.FONTWEIGHT_BOLD if bold else wx.FONTWEIGHT_NORMAL,
                             False,
                             self.text_font.value)
        self._bbox = None

    def move(self, delta):
        self.pos += delta
        self.is_updated = True

    def set_text_props(self, text_string, pointsize, color, bold, italic):
        self.text_string = text_string
        self.pointsize = pointsize
        self.textcolor.RGBA = color.RGBA
        self.bold = bold
        self.italic = italic
        self.is_updated = True
        self._update_font()

    def hit_test(self, pt):
        if self._bbox:
            return self._bbox.Contains(pt.x - self.pos.x, pt.y - self.pos.y)
        return False

    def _update_font(self):
        self._font.SetPointSize(self.pointsize)
        self._font.SetStyle(wx.FONTSTYLE_ITALIC if self.italic else wx.FONTSTYLE_NORMAL)
        self._font.SetWeight(wx.FONTWEIGHT_BOLD if self.bold else wx.FONTWEIGHT_NORMAL)
        self._bbox = None

    def _update_bbox(self, dc):
        dc.SetFont(self._font)
        (w,h,d,v) = dc.GetFullTextExtent(self.text_string)
        self._bbox = wx.Rect(0, 0, w, h)

    def draw_object(self, layer, dc):
        dc.SetTextForeground(self.textcolor)
        dc.SetFont(self._font)
        dc.DrawText(self.text_string, self.pos.x, self.pos.y)
        dc.SetTextForeground(wx.Colour(0,0,0))

        if not self._bbox:
            self._update_bbox(dc)

    def draw_handles(self, layer, dc):
        dc.SetPen(wx.BLACK_PEN)
        dc.SetBrush(wx.LIGHT_GREY_BRUSH)

        l = self.pos.x
        t = self.pos.y
        r = self.pos.x + self._bbox.width
        b = self.pos.y + self._bbox.height

        dc.DrawRectangle(l-7, t-7, 7, 7)
        dc.DrawRectangle(r,   t-7, 7, 7)
        dc.DrawRectangle(l-7, b,   7, 7)
        dc.DrawRectangle(r,   b,   7, 7)

    def toxml(self, action="update"):
        if action == "update" and not self.is_updated:
            return ""

        if action == "del":
            xml_str = "<text action='del' id='" + self.id + "'/>"
            return xml_str

        xml_str = (f"<text"
                   f" action='{action}'"
                   f" id='{self.id}'"
                   f" zorder='{self.z_order}'"
                   f" text_string='{self.text_string}'"
                   f" posx='{self.pos.x}'"
                   f" posy='{self.pos.y}'"
                   f" pointsize='{self.pointsize}'"
                   f" color='{self.textcolor.GetAsString(wx.C2S_HTML_SYNTAX)}'"
                   f" bold='{self.bold}'"
                   f" italic='{self.italic}'"
                   f"/>")
        self.is_updated = False
        return xml_str

    def takedom(self, xml_dom):
        self.text_string = xml_dom.getAttribute("text_string")

        self.pos.x = xmlutil.int_attrib(xml_dom, "posx", 0)
        self.pos.y = xmlutil.int_attrib(xml_dom, "posy", 0)
        self.pointsize = xmlutil.int_attrib(xml_dom, "pointsize", 12)
        self.bold = xmlutil.bool_attrib(xml_dom, "bold", False)
        self.italic = xmlutil.bool_attrib(xml_dom, "italic", False)
        self.textcolor.Set(xmlutil.str_attrib(xml_dom, "color", "#FFFFFF"))

        self._update_font()
