# FlexiRPG -- Whiteboard object base class
#
# Copyright (C) 2010 David Vrabel
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
from orpg.mapper.base import *
from orpg.mapper.map_utils import *

WhiteboardObjectUpdatedEventType = wx.NewEventType()
EVT_WHITEBOARD_OBJECT_UPDATED = wx.PyEventBinder(WhiteboardObjectUpdatedEventType, 1)

class WhiteboardObjectUpdatedEvent(wx.PyCommandEvent):
    def __init__(self, evtType, id, obj):
        wx.PyCommandEvent.__init__(self, evtType, id)
        self.obj = obj

class WhiteboardObject(object):
    def __init__(self, window, id):
        self.window = window
        self.id = id
        self._z_order = 0
        self.highlighted = False
        self.is_updated = False

    def complete(self):
        """Complete the creation of an object.

        This should finalize any internal state, making it ready to be
        converted to XML.

        """
        pass

    def destroy(self):
        pass

    def snap_to_grid(self, grid):
        pass

    def draw(self, layer, dc, op=wx.COPY):
        self.draw_object(layer, dc)
        if self.highlighted:
            self.draw_handles(layer, dc)

    def highlight(self, highlight=True):
        self.highlighted = highlight

    def __get_z_order(self):
        return self._z_order

    def __set_z_order(self, z):
        self._z_order = z
        self.is_updated = True

    z_order = property(__get_z_order, __set_z_order)

    def _updated(self):
        evt = WhiteboardObjectUpdatedEvent(WhiteboardObjectUpdatedEventType, -1, self)
        wx.PostEvent(self.window, evt)
