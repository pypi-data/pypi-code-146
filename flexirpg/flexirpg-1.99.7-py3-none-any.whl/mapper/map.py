# FlexiRPG - Map drawing area.
#
# Copyright 2020 David Vrabel
# Copyright (C) 2000-2001 The OpenRPG Project
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.

import os
import traceback

from orpg.config import Paths, Settings
from orpg.log import logger
import orpg.lib.xmlutil as xmlutil
from orpg.mapper.map_version import MAP_VERSION
from orpg.mapper.map_msg import *
from orpg.mapper.min_dialogs import *
from orpg.mapper.map_prop_dialog import *
from orpg.mapper.miniature_lib import MiniatureLib
from orpg.mapper.miniature_ui import MiniatureManager
from orpg.mapper.mapcontrols import MapControls
from orpg.main import image_library
from orpg.mapper.whiteboard_object import EVT_WHITEBOARD_OBJECT_UPDATED
from orpg.networking.roles import *

# Various marker modes for player tools on the map
MARKER_MODE_NONE = 0
MARKER_MODE_MEASURE = 1
MARKER_MODE_TARGET = 2
MARKER_MODE_AREA_TARGET = 3

MINIMUM_ZOOM = 0.2

class MapCanvas(wx.Panel):
    def __init__(self, parent, ID, isEditor=0):
        wx.Panel.__init__(self, parent, ID, style=wx.FULL_REPAINT_ON_RESIZE | wx.SUNKEN_BORDER )
        self.parent = parent
        self.frame = parent.frame
        self.session = self.frame.session

        self.SetBackgroundStyle(wx.BG_STYLE_PAINT)
        self.layers = {}
        self.layers['bg'] = layer_back_ground(self)
        self.layers['grid'] = grid_layer(self)
        self.layers['whiteboard'] = whiteboard_layer(self)
        self.Bind(wx.EVT_PAINT, self.on_paint)
        self.Bind(wx.EVT_LEFT_DOWN, self.on_left_down)
        self.Bind(wx.EVT_LEFT_DCLICK, self.on_left_dclick)
        self.Bind(wx.EVT_LEFT_UP, self.on_left_up)
        self.Bind(wx.EVT_MIDDLE_DOWN, self.on_middle_down)
        self.Bind(wx.EVT_RIGHT_DOWN, self.on_right_down)
        self.Bind(wx.EVT_MOTION, self.on_motion)
        self.Bind(wx.EVT_MOUSEWHEEL, self.on_mousewheel)
        self.isEditor = isEditor
        self.map_version = MAP_VERSION

        self.view_port_origin = wx.Point(0, 0)
        self.zoom = 1.0
        self.scrolling = False

        self.Bind(EVT_WHITEBOARD_OBJECT_UPDATED, self.on_whiteboard_object_updated)

    def send_map_data(self, action="update"):
        wx.BeginBusyCursor()
        send_text = self.toxml(action)
        if send_text:
            if not self.isEditor:
                self.session.send(send_text)
        wx.EndBusyCursor()

    def on_paint(self, evt):
        scale = self.zoom
        topleft = self.view_port_origin
        clientsize = self.GetClientSize()
        clientsize.Scale(1/scale, 1/scale)

        dc = wx.AutoBufferedPaintDC(self)
        dc.SetDeviceOrigin(int(-topleft.x*scale), int(-topleft.y*scale))
        dc.SetUserScale(scale, scale)

        dc.SetBackground(wx.Brush(self.GetBackgroundColour(), wx.SOLID))
        dc.Clear()

        self.layers['bg'].layerDraw(dc, topleft, clientsize)
        self.layers['grid'].layerDraw(dc, topleft, clientsize)
        self.layers['whiteboard'].layerDraw(dc)

    def on_left_down(self, evt):
        if evt.ShiftDown():
            self.last_pos = self.get_relative_position_from_event(evt)
            self.scrolling = True
        else:
            self.parent.controls.on_left_down(evt)

    def on_right_down(self, evt):
        if evt.ShiftDown():
            pass
        else:
            self.parent.controls.on_right_down(evt)

    def on_left_dclick(self, evt):
        if evt.ShiftDown():
            pass
        else:
            self.parent.controls.on_left_dclick(evt)

    def on_left_up(self, evt):
        if self.scrolling:
            self.scrolling = False
        else:
            self.parent.controls.on_left_up(evt)

    def on_middle_down(self, evt):
        self.last_pos = self.get_relative_position_from_event(evt)

    def on_motion(self, evt):
        if self.scrolling or evt.MiddleIsDown():
            pos = self.get_relative_position_from_event(evt)
            self.view_port_origin.x -= pos.x - self.last_pos.x
            self.view_port_origin.y -= pos.y - self.last_pos.y
            self.last_pos = pos
            self.Refresh()
        else:
            self.parent.controls.on_motion(evt)

    def on_mousewheel(self, evt):
        rot = evt.GetWheelRotation() // evt.GetWheelDelta()
        self._zoom_adjust(evt, rot * 0.1)

    def on_zoom_out(self, evt):
        self._zoom_adjust(None, -0.1)

    def on_zoom_in(self, evt):
        self._zoom_adjust(None, 0.1)

    def _zoom_adjust(self, evt, zoom_delta):
        # Zoom about the centre of the window if there's no mouse event.
        if evt is None:
            evt = wx.MouseEvent()
            evt.SetX(round(self.GetClientSize().x / 2))
            evt.SetY(round(self.GetClientSize().y / 2))
        pos = self.get_position_from_event(evt)
        self.zoom = max(self.zoom + zoom_delta, MINIMUM_ZOOM)
        self.view_port_origin = pos - self.get_relative_position_from_event(evt)
        self.Refresh()

    def on_reset_view(self, evt):
        self.zoom = 1.0
        self.view_port_origin.x = 0
        self.view_port_origin.y = 0
        self.Refresh()

    def on_prop(self, evt):
        if self.session.denied(ROLE_GM):
            self.frame.chat.InfoPost("You must be a GM to use this feature")
            return
        dlg = general_map_prop_dialog(self.frame,
                                      self.layers['bg'], self.layers['grid'])
        if dlg.ShowModal() == wx.ID_OK:
            self.send_map_data()
            self.Refresh(False)
        dlg.Destroy()

    def on_whiteboard_object_updated(self, evt):
        self.Refresh(True)

    def get_relative_position_from_event(self, evt):
        dc = wx.ClientDC(self)
        dc.SetUserScale(self.zoom, self.zoom)
        return evt.GetLogicalPosition(dc)

    def get_position_from_event(self, evt):
        pos = self.get_relative_position_from_event(evt)
        return wx.Point(self.view_port_origin.x + pos.x, self.view_port_origin.y + pos.y)

    def toxml(self, action="update"):
        xml_str = "<map version='" + self.map_version + "'"

        s = ""
        keys = list(self.layers.keys())
        for k in keys:
            if (k != "fog" or action != "update"):
                s += self.layers[k].layerToXML(action)

        if s or action == "new":
            return "<map version='" + self.map_version + "' action='" + action + "'>" + s + "</map>"
        else:
            return ""

    def takexml(self, xml, new_ids=False):
        try:
            #parse the map DOM
            xml_dom = xmlutil.parseXml(xml)
            if xml_dom == None:
                logger.error("Error in map XML")
                return
            node_list = xml_dom.getElementsByTagName("map")

            if new_ids:
                self._generate_new_ids(xml_dom);

            if len(node_list) < 1:
                logger.error("Invalid XML format for mapper")
            else:
                # set map version to incoming data so layers can convert
                self.map_version = node_list[0].getAttribute("version")
                action = node_list[0].getAttribute("action")
                if action == "new":
                    self.layers = {}
                    try:
                        self.layers['bg'] = layer_back_ground(self)
                    except:
                        pass
                    try:
                        self.layers['grid'] = grid_layer(self)
                    except:
                        pass
                    try:
                        self.layers['whiteboard'] = whiteboard_layer(self)
                    except:
                        pass
                children = node_list[0].childNodes
                for c in children:
                    name = c.nodeName
                    if name in self.layers:
                        self.layers[name].layerTakeDOM(c)
                # all map data should be converted, set map version to current version
                self.map_version = MAP_VERSION
                self.Refresh(False)
            xml_dom.unlink()  # eliminate circular refs
        except:
            logger.exception("Error loading map")

    def _generate_new_ids(self, xml_dom):
        for mini in xml_dom.getElementsByTagName("miniature"):
            mini.setAttribute('id', 'mini-' + self.session.get_next_id())
        for line in xml_dom.getElementsByTagName("line"):
            line.setAttribute('id', 'line-' + self.session.get_next_id())
        for text in xml_dom.getElementsByTagName("text"):
            text.setAttribute('id', 'text-' + self.session.get_next_id())


class map_wnd(wx.Panel):

    last_directory = Settings.define("map.last_directory", "")

    def __init__(self, parent, id):
        wx.Panel.__init__(self, parent, id)
        self.frame = parent
        self.session = self.frame.session

        self.minilib = MiniatureLib()
        self.mini_manager = MiniatureManager(self.minilib, self)

        self.canvas = MapCanvas(self, -1)
        self.controls = MapControls(self, -1, self.canvas)

        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.canvas, 1, wx.EXPAND)
        self.sizer.Add(self.controls, 0, wx.EXPAND)
        self.SetSizer(self.sizer)

        self.load_default()

    def load_default(self):
        if self.session.denied(ROLE_GM):
            self.frame.chat.InfoPost("You must be a GM to use this feature")
            return
        with open(Paths.template("default_map.xml")) as f:
            self.new_data(f.read())
        self.canvas.send_map_data("new")

    def new_data(self, data):
        self.canvas.takexml(data)

    def on_clear_map(self, evt):
        if self.session.denied(ROLE_GM):
            self.frame.chat.InfoPost("You must be a GM to use this feature")
            return
        self.controls.delete_all_objects()

    def on_save(self,evt):
        if self.session.denied(ROLE_GM):
            self.frame.chat.InfoPost("You must be a GM to use this feature")
            return
        d = wx.FileDialog(self.GetParent(), "Save Map",
                          self.last_directory.value,
                          "", "*.xml", wx.FD_SAVE)
        if d.ShowModal() == wx.ID_OK:
            self.last_directory.value = d.GetDirectory()
            f = open(d.GetPath(), "w")
            data = '<nodehandler class="min_map" icon="compass" module="core" name="miniature Map">'
            data += self.canvas.toxml("new")
            data += "</nodehandler>"
            data = data.replace(">",">\n")
            f.write(data)
            f.close()
        d.Destroy()

    def on_open(self, evt):
        if self.session.denied(ROLE_GM):
            self.frame.chat.InfoPost("You must be a GM to use this feature")
            return
        d = wx.FileDialog(self.GetParent(), "Open Map",
                          self.last_directory.value,
                          "", "*.xml", wx.FD_OPEN)
        if d.ShowModal() == wx.ID_OK:
            self.last_directory.value = d.GetDirectory()
            logger.info(f"Loading map from '{d.GetPath()}'")
            f = open(d.GetPath())
            map_xml = f.read()
            self.canvas.takexml(map_xml, True)
            self.canvas.send_map_data("new")
        d.Destroy()

    def on_mini_library(self, evt):
        self.mini_manager.select()

    def build_menu(self):
        # temp menu
        menu = wx.Menu()
        item = wx.MenuItem(menu, wx.ID_ANY, "&Clear Map")
        self.frame.Bind(wx.EVT_MENU, self.on_clear_map, item)
        menu.Append(item)
        item = wx.MenuItem(menu, wx.ID_ANY, "&Open Map", "Open Map")
        self.frame.Bind(wx.EVT_MENU, self.on_open, item)
        menu.Append(item)
        item = wx.MenuItem(menu, wx.ID_ANY, "&Save Map", "Save Map")
        self.frame.Bind(wx.EVT_MENU, self.on_save, item)
        menu.Append(item)
        menu.AppendSeparator()
        item = wx.MenuItem(menu, wx.ID_ANY, "&Miniature Library...")
        self.frame.Bind(wx.EVT_MENU, self.on_mini_library, item)
        menu.Append(item)
        menu.AppendSeparator()
        item = wx.MenuItem(menu, wx.ID_ANY, "&Properties", "Properties")
        self.frame.Bind(wx.EVT_MENU, self.canvas.on_prop, item)
        menu.Append(item)
        self.frame.mainmenu.Insert(2, menu, '&Map')
