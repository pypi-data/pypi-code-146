# Copyright (C) 2000-2001 The OpenRPG Project
# Copyright (C) 2009 David Vrabel
#
#    openrpg-dev@lists.sourceforge.net
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.
# --
#
# File: mapper/whiteboard.py
# Author: Chris Davis
# Maintainer:
# Version:
#   $Id: whiteboard.py,v 1.47 2007/03/09 14:11:55 digitalxero Exp $
#
# Description: This file contains some of the basic definitions for the chat
# utilities in the orpg project.
#

import random

from orpg.log import logger
from orpg.mapper.base import *
from orpg.mapper.exceptions import MapError
from orpg.mapper.map_utils import *
from orpg.mapper.whiteboard_stack import WhiteboardStack
from orpg.mapper.whiteboard_line import WhiteboardLine
from orpg.mapper.whiteboard_circle import WhiteboardCircle
from orpg.mapper.whiteboard_text import WhiteboardText
from orpg.mapper.whiteboard_mini import WhiteboardMini

from orpg.main import image_library

##-----------------------------
## whiteboard layer
##-----------------------------
class whiteboard_layer(layer_base):

    def __init__(self, canvas):
        self.canvas = canvas

        layer_base.__init__(self)

        self.objects = WhiteboardStack()

    def raise_object(self, obj):
        self.objects.raise_(obj)
        self.send_updates()

    def lower_object(self, obj):
        self.objects.lower(obj)
        self.send_updates()

    def raise_object_to_top(self, obj):
        self.objects.raise_to_top(obj)
        self.send_updates()

    def lower_object_to_bottom(self, obj):
        self.objects.lower_to_bottom(obj)
        self.send_updates()

    def new_line(self, color, width):
        id = 'line-' + self.canvas.session.get_next_id()
        line = WhiteboardLine(self.canvas, id, color=color, width=width)
        self.objects.append(line)
        return line

    def complete_object(self, obj):
        obj.complete()
        xml_str = "<map><whiteboard>"
        xml_str += obj.toxml("new")
        xml_str += "</whiteboard></map>"
        self.canvas.frame.session.send(xml_str)

    def new_circle(self, color, width):
        id = "circle-" + self.canvas.session.get_next_id()
        circle = WhiteboardCircle(self.canvas, id, color=color, width=width)
        self.objects.append(circle)
        return circle

    def get_object_by_id(self, id):
        for obj in self.objects:
            if str(obj.id) == str(id):
                return obj
        return None

    def del_object(self, obj):
        xml_str = "<map><whiteboard>"
        xml_str += obj.toxml("del")
        xml_str += "</whiteboard></map>"
        self.canvas.frame.session.send(xml_str)
        self.objects.remove(obj)
        self.canvas.Refresh()

    def del_all_objects(self):
        for obj in self.objects:
            self.del_object(obj)

    def layerDraw(self, dc):
        for obj in self.objects:
            obj.draw(self, dc)

    def find_object_at_position(self, pos):
        for obj in reversed(self.objects):
            if obj.hit_test(pos):
                return obj
        return None

    def set_font(self, font):
        self.font = font

    def add_text(self, text_string, pos, pointsize, color, bold, italic):
        id = 'text-' + self.canvas.session.get_next_id()
        text = WhiteboardText(self.canvas, id, text_string, pos, pointsize, color, bold, italic)
        self.objects.append(text)

        xml_str = "<map><whiteboard>"
        xml_str += text.toxml("new")
        xml_str += "</whiteboard></map>"
        self.canvas.frame.session.send(xml_str)
        self.canvas.Refresh(True)

    def add_miniature(self, mini_tmpl, pos):
        id = 'mini-' + self.canvas.session.get_next_id()
        image = image_library.get(mini_tmpl.image_id, mini_tmpl.size)
        top_left = wx.Point(pos.x - image.width // 2, pos.y - image.width // 2)
        mini = WhiteboardMini(self.canvas, id, image, top_left, label=mini_tmpl.new_label())
        mini.snap_to_grid(self.canvas.layers['grid'])
        self.objects.append(mini)
        xml_str = "<map><whiteboard>"
        xml_str += mini.toxml("new")
        xml_str += "</whiteboard></map>"
        self.canvas.frame.session.send(xml_str)
        self.canvas.Refresh(True)

    def send_updates(self):
        xml = self.layerToXML()
        if xml != "":
            self.canvas.frame.session.send("<map>" + xml + "</map>")

    def layerToXML(self, action="update"):
        white_string = ""
        if self.objects:
            for l in self.objects:
                white_string += l.toxml(action)

        if len(white_string):
            s = "<whiteboard>"
            s += white_string
            s += "</whiteboard>"
            return s
        return ""

    def layerTakeDOM(self, xml_dom):
        children = xml_dom.childNodes
        for l in children:
            nodename = l.nodeName

            action = l.getAttribute("action")
            id = l.getAttribute('id')

            if action == "del":
                obj = self.get_object_by_id(id)
                if obj:
                    self.objects.remove(obj)
                continue

            zorder = int(l.getAttribute('zorder'))

            if action == "new":
                if nodename == "line":
                    obj = WhiteboardLine(self.canvas, id)
                elif nodename == "circle":
                    obj = WhiteboardCircle(self.canvas, id)
                elif nodename == "cone":
                    obj = WhiteboardCone(self.canvas, id)
                elif nodename == "text":
                    obj = WhiteboardText(self.canvas, id)
                elif nodename == "miniature":
                    obj = WhiteboardMini(self.canvas, id)
                else:
                    continue
                try:
                    obj.takedom(l)
                    self.objects.insert(obj, zorder)
                except MapError as e:
                    logger.info(f"Ignoring map object {id}: {e}")
            else:
                obj = self.get_object_by_id(id)
                if obj:
                    obj.takedom(l)
                    self.objects.move(obj, zorder)
