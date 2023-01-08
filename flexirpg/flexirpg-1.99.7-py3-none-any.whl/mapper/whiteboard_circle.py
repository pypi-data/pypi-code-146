# FlexiRPG -- Whiteboard circles
#
# Copyright (C) 2020 David Vrabel
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.

from math import ceil, degrees, floor

import orpg.lib.xmlutil as xmlutil
from orpg.mapper.base import *
from orpg.mapper.map_utils import distance_between, proximity_test
from orpg.mapper.whiteboard_object import WhiteboardObject

class WhiteboardCircle(WhiteboardObject):

    MIN_RADIUS = 1          # pixels
    SELECTION_TOLERANCE = 2 # pixels

    def __init__(self, window, id, color=wx.BLACK, width=1):
        WhiteboardObject.__init__(self, window, id)
        self.linecolor = wx.Colour(color)
        self.linewidth = width
        self.centre = wx.Point(0, 0)
        self._radius = 0
        self._start_angle = 0 # rad (0 is x-axis).
        self._end_angle = 0   # rad (start = end => circle).
        # Points for the two radius lines.
        #   [start, centre, end] relative to centre.
        self._handles = [wx.Point(), wx.Point(), wx.Point()]

    @property
    def radius(self):
        return self._radius

    @radius.setter
    def radius(self, r):
        self._radius = max(self.MIN_RADIUS, round(r))
        self._update_handles()

    @property
    def centre_angle(self):
        return (self._start_angle + self._end_angle) / 2

    @centre_angle.setter
    def centre_angle(self, th):
        arc_angle = self.arc_angle
        self._start_angle = th - arc_angle / 2
        self._end_angle   = th + arc_angle / 2
        self._update_handles()

    @property
    def arc_angle(self):
        return self._end_angle - self._start_angle

    @arc_angle.setter
    def arc_angle(self, th):
        self._end_angle = self._start_angle + th
        self._update_handles()

    def is_circle(self):
        return self._start_angle == self._end_angle

    def move(self, delta):
        self.centre += delta
        self.is_updated = True

    def hit_test(self, pt):
        """Is 'pt' near the circle or segment?

        If the shape is a whole circle, only the circumference is
        tested. For a segment the two radiuses are also checked.

        """
        tolerance = self.linewidth / 2 + self.SELECTION_TOLERANCE
        p = pt - self.centre
        d = sqrt(p.x * p.x + p.y * p.y)
        on_circle = floor(d - tolerance) <= self.radius <= ceil(d + tolerance)
        if self.is_circle():
            return on_circle
        else:
            theta = atan2(p.y, p.x)
            return ((on_circle and self._start_angle <= theta <= self._end_angle)
                    or proximity_test(self._handles[0], self._handles[1], p, tolerance)
                    or proximity_test(self._handles[1], self._handles[2], p, tolerance))

    def draw_object(self, layer, dc):
        dc.SetPen(wx.Pen(self.linecolor, self.linewidth))
        dc.SetBrush(wx.TRANSPARENT_BRUSH)
        if self.is_circle():
            dc.DrawCircle(self.centre.x, self.centre.y, self.radius)
        else:
            dc.DrawLines(self._handles, self.centre.x, self.centre.y)
            dc.DrawEllipticArc(self.centre.x - self.radius, self.centre.y - self.radius,
                               2 * self.radius, 2 * self.radius,
                               -degrees(self._end_angle), -degrees(self._start_angle))

    def draw_handles(self, layer, dc):
        dc.SetPen(wx.BLACK_PEN)
        dc.SetBrush(wx.LIGHT_GREY_BRUSH)
        for p in self._handles:
            dc.DrawRectangle(self.centre.x + p.x - 3, self.centre.y + p.y - 3, 7, 7)

    def toxml(self, action="update"):
        if action == "update" and not self.is_updated:
            return ""

        if action == "del":
            xml_str = f"<line action='del' id='{self.id}'/>"
            return xml_str

        xml_str = (f"<circle"
                   f" action='{action}'"
                   f" id='{self.id}'"
                   f" zorder='{self.z_order}'"
                   f" x='{self.centre.x}'"
                   f" y='{self.centre.y}'"
                   f" r='{self._radius}'"
                   f" sa='{self._start_angle}'"
                   f" ea='{self._end_angle}'"
                   f" color='{self.linecolor.GetAsString(wx.C2S_HTML_SYNTAX)}'"
                   f" width='{self.linewidth}'"
                   f"/>")
        self.is_updated = False
        return xml_str

    def takedom(self, xml_dom):
        self.centre.x = xmlutil.int_attrib(xml_dom, "x", 0)
        self.centre.y = xmlutil.int_attrib(xml_dom, "y", 0)
        self._radius = xmlutil.int_attrib(xml_dom, "r", 0)
        self._start_angle = xmlutil.float_attrib(xml_dom, "sa", 0.0)
        self._end_angle = xmlutil.float_attrib(xml_dom, "ea", 0.0)
        self.linecolor.Set(xmlutil.str_attrib(xml_dom, "color", "#FFFFFF"))
        self.linewidth = xmlutil.int_attrib(xml_dom, "width", 1)
        self._update_handles()

    def _update_handles(self):
        if self.is_circle():
            start_angle = 0.0
            end_angle = pi / 2
        else:
            start_angle = self._start_angle
            end_angle = self._end_angle
        r = self._radius
        self._handles[0].x = round(r * cos(start_angle))
        self._handles[0].y = round(r * sin(start_angle))
        self._handles[2].x = round(r * cos(end_angle))
        self._handles[2].y = round(r * sin(end_angle))
        self.is_updated = True
