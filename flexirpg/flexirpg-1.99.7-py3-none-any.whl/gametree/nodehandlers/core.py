# Base class for game tree nodes.
#
# Copyright (C) 2011 David Vrabel
# Copyright (C) 2000-2001 The OpenRPG Project
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.

import wx

import orpg.lib.xmlutil as xmlutil

class node_handler(object):
    """ Base nodehandler with virtual functions and standard implmentations """
    def __init__(self, tree, xml_dom, tree_node):
        self.tree = tree
        self.master_dom = xml_dom
        self.mytree_node = tree_node
        self.myeditor = None # designing
        self.tree.SetItemData(tree_node, self)

        self.enabled_colour = wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOWTEXT)
        self.disabled_colour = wx.SystemSettings.GetColour(wx.SYS_COLOUR_GRAYTEXT)

        self.__active = False
        self.active = xmlutil.bool_attrib(xml_dom, "active", False)

        self.__auto_reset = 0
        self.auto_reset = self.master_dom.getAttribute("auto_reset") == "1"

        self._update_tree_node(self.enabled, self.icon)

    def use_node(self):
        if self.enabled:
            self.on_use()

    def reset_node(self):
        self.on_reset()
        self.enabled = True

    def on_drop(self, dropped, where):
        """Move a dropped tree item.

        Where the dropped item is moved to depends on where it was
        dropped on the target item: before (upper half), after (lower
        half), or as a child (to the right).
        """
        if where & (wx.TREE_HITTEST_ABOVE | wx.TREE_HITTEST_BELOW
                    | wx.TREE_HITTEST_TOLEFT | wx.TREE_HITTEST_TORIGHT):
            return
        if dropped == self or self.tree.is_parent_node(self.mytree_node, dropped.mytree_node):
            return
        xml_dom = dropped.delete()
        parent = self.master_dom.parentNode
        if where & wx.TREE_HITTEST_ONITEMRIGHT:
            xml_dom = self.master_dom.appendChild(xml_dom)
            parent_node = self.mytree_node
            prev_sib = None
        elif where & wx.TREE_HITTEST_ONITEMUPPERPART:
            xml_dom = parent.insertBefore(xml_dom,self.master_dom)
            parent_node = self.tree.GetItemParent(self.mytree_node)
            prev_sib = self.tree.GetPrevSibling(self.mytree_node)
            if not prev_sib.IsOk():
                prev_sib = parent_node
        else:
            next_sib = self.tree.GetNextSibling(self.mytree_node)
            if next_sib:
                node = self.tree.GetItemData(next_sib)
                xml_dom = parent.insertBefore(xml_dom, node.master_dom)
            else:
                xml_dom = parent.appendChild(xml_dom)
            parent_node = self.tree.GetItemParent(self.mytree_node)
            prev_sib = self.mytree_node
        self.tree.load_xml(xml_dom, parent_node, prev_sib)

    def toxml(self, pretty = False):
        return xmlutil.toxml(self.master_dom, pretty)

    def delete(self):
        """ removes the tree_node and xml_node, and returns the removed xml_node """
        self.for_each_in_subtree(node_handler.__cleanup)
        self.tree.Delete(self.mytree_node)
        parent = self.master_dom.parentNode
        return parent.removeChild(self.master_dom)

    def __cleanup(self):
        if self.__auto_reset:
            self.tree.del_auto_reset_node(self)
        if self.__active:
            self.tree.deactivate(self)

    def for_each_in_subtree(self, func):
        (child, cookie) = self.tree.GetFirstChild(self.mytree_node)
        while child.IsOk():
            n = self.tree.GetItemData(child)
            n.for_each_in_subtree(func)
            (child, cookie) = self.tree.GetNextChild(self.mytree_node, cookie)
        func(self)

    def _update_tree_node(self, enabled, icon):
        if enabled:
            self.tree.SetItemTextColour(self.mytree_node, self.enabled_colour)
        else:
            self.tree.SetItemTextColour(self.mytree_node, self.disabled_colour)
            icon = self.tree.icons["disabled"]
        self.tree.SetItemImage(self.mytree_node, icon)
        self.tree.SetItemImage(self.mytree_node, icon, wx.TreeItemIcon_Selected)
        self.tree.Refresh()

    def __get_name(self):
        return self.master_dom.getAttribute("name")

    def __set_name(self, name):
        self.master_dom.setAttribute("name", name)
        if self.tree.GetItemText(self.mytree_node) != name:
            self.tree.SetItemText(self.mytree_node, name)

    name = property(__get_name, __set_name)

    def __get_icon(self):
        name = self.master_dom.getAttribute("icon")
        return self.tree.icons[name]

    def __set_icon(self, icon):
        name = self.tree.icons.name(icon)
        self.master_dom.setAttribute("icon", name)
        self._update_tree_node(self.enabled, icon)

    icon = property(__get_icon, __set_icon)

    def __get_enabled(self):
        return self.master_dom.getAttribute("enabled") != "0"

    def __set_enabled(self, enabled):
        if enabled:
            s = "1"
        else:
            s = "0"
        self.master_dom.setAttribute("enabled", s)
        self._update_tree_node(enabled, self.icon);

    enabled = property(__get_enabled, __set_enabled)

    @property
    def active(self):
        return self.__active

    @active.setter
    def active(self, v):
        if v:
            self.master_dom.setAttribute("active", "1")
            self.tree.activate(self)
            self.__active = True
        elif self.__active:
            self.__active = False
            self.tree.deactivate(self)
            if self.master_dom.hasAttribute("active"):
                self.master_dom.removeAttribute("active")

    def __get_auto_reset(self):
        return self.__auto_reset

    def __set_auto_reset(self, auto_reset):
        if auto_reset == self.__auto_reset:
            return
        self.__auto_reset = auto_reset
        if auto_reset:
            self.master_dom.setAttribute("auto_reset", "1")
            self.tree.add_auto_reset_node(self)
        else:
            if self.master_dom.hasAttribute("auto_reset"):
                self.master_dom.removeAttribute("auto_reset")
            self.tree.del_auto_reset_node(self)

    auto_reset = property(__get_auto_reset, __set_auto_reset)

    def refresh(self):
        pass
