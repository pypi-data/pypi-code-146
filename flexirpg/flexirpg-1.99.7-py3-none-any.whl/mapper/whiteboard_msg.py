# Copyright (C) 2000-2001 The OpenRPG Project
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
# File: mapper/whiteboard_msg.py
# Author: Chris Davis
# Maintainer:
# Version:
#   $Id: whiteboard_msg.py,v 1.12 2007/03/09 14:11:56 digitalxero Exp $
#
# Description: This file contains some of the basic definitions for the chat
# utilities in the orpg project.
#
__version__ = "$Id: whiteboard_msg.py,v 1.12 2007/03/09 14:11:56 digitalxero Exp $"

from orpg.mapper.base_msg import *

class item_msg(map_element_msg_base):

    def __init__(self,reentrant_lock_object = None, tagname = "line"):
        self.tagname = tagname   # set this to be for items.  Tagname gets used in some base class functions.
        map_element_msg_base.__init__(self,reentrant_lock_object)   # call base class



    # convenience method to use if only this item is modified
    #   outputs a <map/> element containing only the changes to this item
    def standalone_update_text(self,update_id_string):
        buffer = "<map id='" + update_id_string + "'>"
        buffer += "<whiteboard>"
        buffer += self.get_changed_xml()
        buffer += "</whiteboad></map>"
        return buffer

    # convenience method to use if only this item is modified
    #   outputs a <map/> element that deletes this item
    def standalone_delete_text(self,update_id_string):
        buffer = None

        if "id" in self._props:
            buffer = "<map id='" + update_id_string + "'>"
            buffer += "<whiteboard>"
            buffer += "<"+self.tagname+" action='del' id='" + self._props("id") + "'/>"
            buffer += "</whiteboard></map>"

        return buffer

    # convenience method to use if only this item is modified
    #   outputs a <map/> element to add this item
    def standalone_add_text(self,update_id_string):
        buffer = "<map id='" + update_id_string + "'>"
        buffer += "<whiteboard>"
        buffer += self.get_all_xml()
        buffer += "</whiteboard></map>"
        return buffer

    def get_all_xml(self,action="new",output_action=1):
        return map_element_msg_base.get_all_xml(self,action,output_action)

    def get_changed_xml(self,action="update",output_action=1):
        return map_element_msg_base.get_changed_xml(self,action,output_action)



class whiteboard_msg(map_element_msg_base):

    def __init__(self,reentrant_lock_object = None):
        self.tagname = "whiteboard"
        map_element_msg_base.__init__(self,reentrant_lock_object)

    def init_from_dom(self,xml_dom):
        self.p_lock.acquire()
        if xml_dom.tagName == self.tagname:
            for a in range(xml_dom.attributes.length):
                attr = xml_dom.attributes.item(a)
                self.init_prop(attr.nodeName, attr.nodeValue)

            for c in xml_dom.childNodes:
                item = item_msg(self.p_lock,c.nodeName)

                try:
                    item.init_from_dom(c)
                except Exception as e:
                    print(e)
                    continue

                id = item.get_prop("id")
                action = item.get_prop("action")


                if action == "new":
                    self.children[id] = item

                elif action == "del":
                    if id in self.children:
                        self.children[id] = None
                        del self.children[id]

                elif action == "update":
                    if id in self.children:
                        self.children[id].init_props(item.get_all_props())

        else:
            self.p_lock.release()
            raise Exception("Error attempting to initialize a " + self.tagname + " from a non-<" + self.tagname + "/> element in whiteboard")
        self.p_lock.release()



    def set_from_dom(self,xml_dom):
        self.p_lock.acquire()
        if xml_dom.tagName == self.tagname:
            for a in range(xml_dom.attributes.length):
                attr = xml_dom.attributes.item(a)
                self.init_prop(attr.nodeName, attr.nodeValue)

            for c in xml_dom.childNodes:
                item = item_msg(self.p_lock, c.nodeName)

                try:
                    item.set_from_dom(c)
                except Exception as e:
                    print(e)
                    continue

                id = item.get_prop("id")
                action = item.get_prop("action")

                if action == "new":
                    self.children[id] = item

                elif action == "del":
                    if id in self.children:
                        self.children[id] = None
                        del self.children[id]

                elif action == "update":
                    if id in self.children:
                        self.children[id].set_props(item.get_all_props())

        else:
            self.p_lock.release()
            raise Exception("Error attempting to set a " + self.tagname + " from a non-<" + self.tagname + "/> element")
        self.p_lock.release()
