# FlexiRPG -- Whiteboard lines
#
# Copyright (C) 2000-2001 The OpenRPG Project
# Copyright (C) 2009-2010 David Vrabel
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
from orpg.mapper.base import *
import orpg.mapper.map_utils
from orpg.mapper.whiteboard_object import WhiteboardObject

class WhiteboardLine(WhiteboardObject):
    def __init__(self, window, id, color=wx.BLACK, width=1):
        WhiteboardObject.__init__(self, window, id)
        self.linecolor = wx.Colour(color)
        self.linewidth = width
        self.points = []

    def add_point(self, x, y):
        p = wx.Point(x, y)
        self.points.append(p)

    def _approximate(self):
        """
        Approximate the line with fewer points.

        For every group of three adjacent points (A, B and C), point B
        is discarded if it's sufficiently close to AC.
        """
        new_points = []
        i = 0
        while i < len(self.points):
            a = self.points[i]
            new_points.append(a)
            for j in range(i+1, len(self.points)-1):
                b = self.points[j]
                c = self.points[j+1]
                if orpg.mapper.map_utils.proximity_test(a, c, b, 0.5):
                    i += 1
                else:
                    break;
            i += 1
        self.points = new_points

    def _choose_handles(self):
        self.handles = []
        self.handles.append(self.points[0])
        dist = 0
        a = self.points[0]
        for b in self.points[1:]:
            dist += orpg.mapper.map_utils.distance_between(a[0], a[1], b[0], b[1])
            if (dist > 50):
                self.handles.append(b)
                dist = 0
            a = b
        self.handles[-1] = self.points[-1]

    def complete(self):
        self._approximate()
        self._choose_handles()

    def _points_from_string(self, line_string):
        self.points = []
        for p in line_string.split(";"):
            p = p.split(",")
            if len(p) == 2:
                self.add_point(int(p[0]), int(p[1]))
        self._choose_handles()

    def move(self, delta):
        for p in self.points:
            p.x += delta.x
            p.y += delta.y
        self.is_updated = True

    def hit_test(self, pt):
        if self.points != []:
            a = self.points[0]
            for b in self.points[1:]:
                if orpg.mapper.map_utils.proximity_test(a, b, pt, (self.linewidth+1)/2+1):
                    return True
                a = b
        return False

    def draw_object(self, layer, dc):
        # Line segments
        pen = wx.Pen(self.linecolor, self.linewidth)
        dc.SetPen(pen)
        dc.SetBrush(wx.BLACK_BRUSH)

        if self.points != []:
            a = self.points[0]
            for b in self.points[1:]:
                (xa, ya) = a
                (xb, yb) = b
                dc.DrawLine(xa, ya, xb, yb)
                a = b

    def draw_handles(self, layer, dc):
        dc.SetPen(wx.BLACK_PEN)
        dc.SetBrush(wx.LIGHT_GREY_BRUSH)

        for p in self.handles:
            (x, y) = p;
            dc.DrawRectangle(x-3, y-3, 7, 7)

    def toxml(self, action="update"):
        if action == "del":
            xml_str = "<line action='del' id='" + self.id + "'/>"
            return xml_str

        #  if there are any changes, make sure id is one of them
        xml_str = "<line"

        xml_str += " action='" + action + "'"
        xml_str += " id='" + self.id + "'"
        xml_str += " zorder='" + str(self.z_order) + "'"

        xml_str+= " line_string='"
        for p in self.points:
            (x,y) = p
            xml_str += str(x) + "," + str(y) + ";"
        xml_str += "'"

        if self.linecolor != None:
            xml_str += " color='" + self.linecolor.GetAsString(wx.C2S_HTML_SYNTAX) + "'"

        if self.linewidth != None:
            xml_str += " width='" + str(self.linewidth) + "'"

        xml_str += "/>"

        if (action == "update" and self.is_updated) or action == "new":
            self.is_updated = False
            return xml_str
        return ''

    def takedom(self, xml_dom):
        line_string = xml_dom.getAttribute("line_string")
        self._points_from_string(line_string)

        if xml_dom.hasAttribute("color") and xml_dom.getAttribute("color") != '':
            self.linecolor.Set(xml_dom.getAttribute("color"))
        if xml_dom.hasAttribute("width"):
            self.linewidth = int(xml_dom.getAttribute("width"))
