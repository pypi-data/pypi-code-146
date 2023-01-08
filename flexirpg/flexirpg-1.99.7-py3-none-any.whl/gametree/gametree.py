# Game tree window.
#
# Copyright (C) 2011 David Vrabel
# Copyright (C) 2000-2001 The OpenRPG Project
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.

import codecs
import os
import shutil

import wx

from orpg.config import Paths, Settings
from orpg.log import logger
from orpg.gametree.icons import node_icons
from orpg.gametree.nodehandlers import core
import orpg.gametree.nodehandlers.flexi
from orpg.gametree.gametree_version import GAMETREE_VERSION
from orpg.lib.text import html_to_text
import orpg.lib.ui as ui
import orpg.lib.xmlutil as xmlutil

STD_MENU_DELETE = wx.NewId()
STD_MENU_DESIGN = wx.NewId()
STD_MENU_USE = wx.NewId()
STD_MENU_SEND = wx.NewId()
STD_MENU_IMPORT = wx.NewId()
STD_MENU_EXPORT = wx.NewId()
STD_MENU_NEW = wx.NewId()
STD_MENU_CLONE = wx.NewId()
STD_MENU_ACTIVE = wx.NewId()
STD_MENU_RESET = wx.NewId()
TOP_NEW = wx.NewId()
TOP_SAVE_TREE = wx.NewId()
TOP_IMPORT = wx.NewId()
TOP_EXPORT = wx.NewId()
TOP_LOCK = wx.NewId()

class game_tree(wx.TreeCtrl):

    tree_is_locked = Settings.define("tree.locked", False)
    last_directory = Settings.define("tree.last_directory", "")

    def __init__(self, parent, id):
        wx.TreeCtrl.__init__(self, parent, style=wx.TR_EDIT_LABELS | wx.TR_HAS_BUTTONS)
        self.frame = parent
        self.session = self.frame.session

        self.icons = orpg.gametree.icons.node_icons()
        self.SetImageList(self.icons)

        self.build_std_menu()
        self.nodehandlers = {
            "flexinode": orpg.gametree.nodehandlers.flexi.flexinode_handler,
        }
        self.active_node = None
        self.auto_reset_nodes = []
        self.roll_value = 0
        self.dragged_obj = None

        self.Bind(wx.EVT_SET_FOCUS, self.on_set_focus)
        self.Bind(wx.EVT_TREE_ITEM_ACTIVATED, self.on_item_activated)
        self.Bind(wx.EVT_RIGHT_DOWN, self.on_rclick)
        self.Bind(wx.EVT_TREE_BEGIN_DRAG, self.on_drag, id=id)
        self.Bind(wx.EVT_TREE_END_DRAG, self.on_drop, id=id)
        self.Bind(wx.EVT_TREE_BEGIN_LABEL_EDIT, self.on_label_begin, id=self.GetId())
        self.Bind(wx.EVT_TREE_END_LABEL_EDIT, self.on_label_change, id=self.GetId())
        self.Bind(wx.EVT_CHAR, self.on_char)
        self.Bind(wx.EVT_TREE_ITEM_EXPANDING, self.on_expanding)

        self.root = self.AddRoot("Game Tree", self.root_icon)
        self.lock_tree(self.tree_is_locked.value)

    ## locate_valid_tree
    ## GUI based dialogs to locate/fix missing treefile issues --Snowdog 3/05
    def locate_valid_tree(self, error, msg, dir, filename):
        """prompts the user to locate a new tree file or create a new one"""
        dlg = wx.MessageDialog(self, msg, error, wx.YES|wx.NO|wx.ICON_ERROR)
        if dlg.ShowModal() == wx.ID_YES:
            file = None
            filetypes = "Game tree (*.xml)|*.xml|All files (*.*)|*.*"
            dlg = wx.FileDialog(self, "Locate Gametree file", dir, filename,
                                filetypes, wx.FD_OPEN | wx.FD_CHANGE_DIR)
            if dlg.ShowModal() == wx.ID_OK:
                file = dlg.GetPath()
            dlg.Destroy()
            return file
        else:
            return None

    def load_tree_from_file(self, filename):
        tmp = None
        xml_dom = None
        xml_doc = None

        logger.info("Reading Gametree file: " + filename + "...")
        tmp = codecs.open(filename, mode='r', encoding='utf-8')
        self.xml_doc = xmlutil.parseXml(tmp.read())
        tmp.close()
        if self.xml_doc:
            xml_dom = self.xml_doc.documentElement

        if not xml_dom:
            raise Exception("Invalid XML")

        if xml_dom.tagName != "gametree":
            raise Exception("Not a game tree file")

        # get gametree version - we could write conversion code here!
        self.master_dom = xml_dom

        version = self.master_dom.getAttribute("version")
        # see if we should load the gametree

        children = self.master_dom.childNodes
        logger.info("Parsing Gametree Nodes...")
        for c in children:
            self.load_xml(c,self.root)

        logger.info("Gametree loaded.")

    def load_tree_default(self):
        self.xml_doc = xmlutil.parseXml("<gametree/>")
        self.master_dom = self.xml_doc.documentElement
        self.SetItemData(self.root,self.master_dom)

    def load_tree(self, filename):
        error = 0

        while True:
            try:
                self.load_tree_from_file(filename)
                break

            except IOError as e:
                (errno, strerror) = e
            except Exception as e:
                (strerror,) = e
            emsg = "Unable to load game tree '" + filename + "'.\n\n" + strerror + ".\n\nSelect a different game tree?"
            fn = filename[(filename.rfind(os.sep) + len(os.sep)):]
            filename = self.locate_valid_tree("Game Tree Error", emsg, Paths.user(), fn)
            if not filename:
                self.load_tree_default()
                return False
            error = error + 1

        if error < 1:
            shutil.copyfile(filename, Paths.user("lastgood.xml"))
        else:
            logger.info("Not overwriting lastgood.xml file.")
        self.refresh_all()
        return True

    def build_std_menu(self, obj=None):
        # build standard menu
        self.std_menu = wx.Menu()
        self.std_menu.Append(STD_MENU_USE,"&Use")
        self.std_menu.Append(STD_MENU_DESIGN,"&Edit")
        self.std_menu.Append(STD_MENU_NEW, "Insert &New")
        self.std_menu.Append(STD_MENU_CLONE,"&Clone")
        self.std_menu.AppendCheckItem(STD_MENU_ACTIVE, "&Active")
        self.std_menu.AppendSeparator()
        self.std_menu.Append(STD_MENU_RESET,"&Reset")
        self.std_menu.AppendSeparator()
        self.std_menu.Append(STD_MENU_SEND,"Send to &Player...")
        self.std_menu.Append(STD_MENU_IMPORT, "&Insert from File...")
        self.std_menu.Append(STD_MENU_EXPORT, "&Save Node As...")
        self.std_menu.AppendSeparator()
        self.std_menu.Append(STD_MENU_DELETE,"&Delete")
        self.std_menu.Enable(STD_MENU_DELETE, not self.tree_is_locked.value)

        self.Bind(wx.EVT_MENU, self.on_node_use, id=STD_MENU_USE)
        self.Bind(wx.EVT_MENU, self.on_node_design, id=STD_MENU_DESIGN)
        self.Bind(wx.EVT_MENU, self.on_new, id=STD_MENU_NEW)
        self.Bind(wx.EVT_MENU, self.on_clone, id=STD_MENU_CLONE)
        self.Bind(wx.EVT_MENU, self.on_active, id=STD_MENU_ACTIVE)
        self.Bind(wx.EVT_MENU, self.on_reset, id=STD_MENU_RESET)
        self.Bind(wx.EVT_MENU, self.on_send_to, id=STD_MENU_SEND)
        self.Bind(wx.EVT_MENU, self.on_import, id=STD_MENU_IMPORT)
        self.Bind(wx.EVT_MENU, self.on_export, id=STD_MENU_EXPORT)
        self.Bind(wx.EVT_MENU, self.on_del, id=STD_MENU_DELETE)

        self.top_menu = wx.Menu()
        self.top_menu.Append(TOP_NEW, "Insert &New")
        self.top_menu.AppendSeparator()
        self.top_menu.Append(TOP_SAVE_TREE,"&Save")
        self.top_menu.Append(TOP_IMPORT, "&Insert from File...")
        self.top_menu.Append(TOP_EXPORT, "&Save Tree As...")
        self.top_menu.AppendSeparator()
        self.top_menu.AppendCheckItem(TOP_LOCK, "&Lock Tree")
        self.top_menu.Check(TOP_LOCK, self.tree_is_locked.value)

        self.Bind(wx.EVT_MENU, self.on_new, id=TOP_NEW)
        self.Bind(wx.EVT_MENU, self.on_save_tree, id=TOP_SAVE_TREE)
        self.Bind(wx.EVT_MENU, self.on_import_file, id=TOP_IMPORT)
        self.Bind(wx.EVT_MENU, self.on_export_tree, id=TOP_EXPORT)
        self.Bind(wx.EVT_MENU, self.on_lock_tree, id=TOP_LOCK)

    @property
    def root_icon(self):
        return self.icons['locked'] if self.tree_is_locked.value else self.icons['folder']

    def on_receive_data(self, data, player):
        beg = data.find("<tree>")
        end = data.rfind("</tree>")
        data = data[6:end]
        self.import_xml(self.root, data)

    def on_send_to(self, evt):
        player_opts = []
        for player in self.session.get_players():
            if player.id != self.session.id:
                player_opts.append((player, f"({player.id}) {player.name}", False))
        if not player_opts:
            return

        with ui.MultiCheckBoxDialog(self, "Send Node to Players",
                                    "Players", player_opts) as dlg:
            if dlg.ShowModal() == wx.ID_OK:
                item = self.GetSelection()
                obj = self.GetItemData(item)
                xmldata = "<tree>" + xmlutil.toxml(obj) + "</tree>"
                if len(dlg.checked) == len(player_opts):
                    self.session.send(xmldata)
                else:
                    for player in dlg.checked:
                        self.session.send(xmldata, player.id)

    def on_new(self, evt):
        new_dom = self.xml_doc.createElement("nodehandler")
        new_dom.setAttribute("class", "flexinode")
        new_dom.setAttribute("name", "New Node")

        item = self.GetSelection();
        if item == self.RootItem:
            parent_dom = self.master_dom
        else:
            node = self.GetItemData(item);
            parent_dom = node.master_dom
        new_dom = parent_dom.insertBefore(new_dom, parent_dom.firstChild)
        self.load_xml(new_dom, item, item)
        self.Expand(item)

    def on_clone(self, evt):
        item = self.GetSelection()
        obj = self.GetItemData(item)
        parent_node = self.GetItemParent(item)
        prev_sib = self.GetPrevSibling(item)
        if not prev_sib.IsOk():
            prev_sib = parent_node
        xml_dom = xmlutil.parseXml(xmlutil.toxml(obj))
        xml_dom = xml_dom.firstChild
        parent = obj.master_dom.parentNode
        xml_dom = parent.insertBefore(xml_dom, obj.master_dom)
        self.load_xml(xml_dom, parent_node, prev_sib)

    def on_active(self, evt):
        item = self.GetSelection()
        obj = self.GetItemData(item)
        obj.active = self.std_menu.IsChecked(STD_MENU_ACTIVE)
        self.refresh_status()

    def on_reset(self, evt):
        node = self.GetItemData(self.GetSelection())
        node.for_each_in_subtree(core.node_handler.reset_node)
        self.refresh_all()

    def __on_import_common(self, parent_node):
        f = wx.FileDialog(self, "Insert Node", self.last_directory.value, "",
                          "XML files (*.xml)|*.xml", wx.FD_OPEN)
        if f.ShowModal() == wx.ID_OK:
            self.last_directory.value = f.GetDirectory()
            file = codecs.open(f.GetPath(), mode='r', encoding='utf-8')
            self.import_xml(parent_node, file.read())
        f.Destroy()

    def on_import(self, evt):
        self.__on_import_common(self.GetSelection())

    def on_export(self, evt):
        item = self.GetSelection()
        obj = self.GetItemData(item)
        f = wx.FileDialog(self, "Save Node", self.last_directory.value, "",
                          "XML files (*.xml)|*.xml", wx.FD_SAVE)
        if f.ShowModal() == wx.ID_OK:
            self.last_directory.value = f.GetDirectory()
            file = codecs.open(f.GetPath(), mode='w', encoding='utf-8')
            file.write(obj.toxml(True))
            file.close()
        f.Destroy()

    def on_export_tree(self, evt):
        f = wx.FileDialog(self, "Save Tree", self.last_directory.value, "",
                          "XML files (*.xml)|*.xml", wx.FD_SAVE)
        if f.ShowModal() == wx.ID_OK:
            self.last_directory.value = f.GetDirectory()
            self.save_tree(f.GetPath())
        f.Destroy()

    def on_lock_tree(self, evt):
        self.lock_tree(self.top_menu.IsChecked(TOP_LOCK))

    def on_save_tree(self, evt):
        self.save_tree(Paths.user("tree.xml"))

    def save_tree(self, filename):
        self.master_dom.setAttribute("version",GAMETREE_VERSION)
        file = codecs.open(filename, mode='w', encoding='utf-8')
        file.write(xmlutil.toxml(self.master_dom,1))
        file.close()

    def on_import_file(self, evt):
        self.__on_import_common(self.root)

    def on_node_design(self, evt):
        item = self.GetSelection()
        obj = self.GetItemData(item)
        obj.on_design(evt)

    def on_node_use(self, evt):
        item = self.GetSelection()
        obj = self.GetItemData(item)
        self.use_node(obj)

    def on_del(self, evt):
        item = self.GetSelection()
        if item:
            self.try_delete_item(item)

    def __valid_import_xml(self, xml_doc):
        if not xml_doc:
            return False
        xml_dom = xml_doc.documentElement
        if not xml_dom:
            return False
        if xml_dom.tagName != "gametree" and xml_dom.tagName != "nodehandler":
            return False
        return True;

    def import_xml(self, parent_node, txt):
        xml_doc = xmlutil.parseXml(txt)
        if not self.__valid_import_xml(xml_doc):
            wx.MessageBox("Import Failed: Invalid or missing node data")
            return

        xml_dom = xml_doc.documentElement

        if parent_node == self.root:
            parent_dom = self.master_dom
        else:
            parent_dom = self.GetItemData(parent_node).master_dom

        if xml_dom.tagName == "gametree":
            before_dom = parent_dom.firstChild
            prev_node = parent_node
            for c in xml_dom.childNodes:
                c = self.master_dom.insertBefore(c, before_dom)
                prev_node = self.load_xml(c, parent_node, prev_node)
            return

        xml_dom = parent_dom.insertBefore(xml_dom, parent_dom.firstChild)
        self.load_xml(xml_dom, parent_node, parent_node)

    def load_xml(self, xml_dom, parent_node, prev_node=None):
        #add the first tree node
        i = 0
        text = xml_dom.getAttribute("name")
        icon = xml_dom.getAttribute("icon")
        i = self.icons[icon]
        name = xml_dom.nodeName
        if prev_node:
            if prev_node == parent_node:
                new_tree_node = self.PrependItem(parent_node, text, i, i)
            else:
                new_tree_node = self.InsertItem(parent_node,prev_node, text, i, i)
        else:
            new_tree_node = self.AppendItem(parent_node, text, i, i)

        #create a nodehandler or continue loading xml into tree
        if name == "nodehandler":
            try:
                py_class = xml_dom.getAttribute("class")
                if not py_class in self.nodehandlers:
                    raise Exception("Unknown Nodehandler for " + py_class)
                self.nodehandlers[py_class](self, xml_dom, new_tree_node)
            except Exception as er:
                logger.exception(f"Error loading {xml_dom.getAttribute('class')} node")
                self.Delete(new_tree_node)
                parent = xml_dom.parentNode
                parent.removeChild(xml_dom)
        if parent_node == self.root:
            self.Expand(self.root)
        return new_tree_node

    def try_delete_item(self, item):
        if self.tree_is_locked.value:
            return
        node = self.GetItemData(item)
        if isinstance(node, core.node_handler):
            node.delete()

    def on_set_focus(self, evt):
        # FIXME: we should be able to use evt.GetWindow() to get the
        # previously focused window but it always returns None.
        # Assume it's the chat window instead.
        self.previously_focused_window = self.frame.chat

    def on_item_activated(self, evt):
        item = evt.GetItem()
        obj = self.GetItemData(item)
        if isinstance(obj,core.node_handler):
            self.use_node(obj)
        self.previously_focused_window.SetFocus()

    def on_rclick(self, evt):
        pt = evt.GetPosition()
        (item, flag) = self.HitTest(pt)
        if item.IsOk():
            obj = self.GetItemData(item)
            self.SelectItem(item)
            if isinstance(obj, core.node_handler):
                self.std_menu.Check(STD_MENU_ACTIVE, obj.active)
                self.PopupMenu(self.std_menu)
            else:
                self.PopupMenu(self.top_menu)
        else:
            self.PopupMenu(self.top_menu)

    def on_label_begin(self, evt):
        if evt.GetItem() == self.GetRootItem():
            evt.Veto()

    def on_label_change(self, evt):
        item = evt.GetItem()
        txt = evt.GetLabel()
        if txt != "":
            node = self.GetItemData(item)
            node.name = txt
        else:
            evt.Veto()

    def on_drag(self, evt):
        if self.tree_is_locked.value:
            return
        item = evt.GetItem()
        obj = self.GetItemData(item)
        if isinstance(obj, core.node_handler):
            self.dragged_obj = obj
            evt.Allow()

    def on_drop(self, evt):
        item = evt.GetItem()
        if item.IsOk():
            obj = self.GetItemData(item)
            if isinstance(obj, core.node_handler):
                (item, where) = self.HitTest(evt.GetPoint())
                obj.on_drop(self.dragged_obj, where)
        self.dragged_obj = None
        evt.Allow()

    def on_char(self, evt):
        # Activating a node with the keyboard doesn't change focus
        self.previously_focused_window = self

        key_code = evt.GetKeyCode()
        item = self.GetSelection()
        if item and key_code == wx.WXK_DELETE:
            self.try_delete_item(item)
        elif item and key_code == wx.WXK_F2:
            self.EditLabel(item)
        else:
            evt.Skip()

    def on_expanding(self, evt):
        self.refresh_children(evt.GetItem())

    def lock_tree(self, locked: bool):
        self.tree_is_locked.value = locked
        self.SetItemImage(self.root, self.root_icon)
        self.top_menu.Enable(TOP_NEW, not locked)
        self.top_menu.Enable(TOP_IMPORT, not locked)
        self.std_menu.Enable(STD_MENU_NEW, not locked)
        self.std_menu.Enable(STD_MENU_CLONE, not locked)
        self.std_menu.Enable(STD_MENU_IMPORT, not locked)
        self.std_menu.Enable(STD_MENU_DELETE, not locked)

    def is_parent_node(self, node, compare_node):
        parent_node = self.GetItemParent(node)
        if compare_node == parent_node:
            return True
        elif parent_node == self.root:
            return False
        else:
            return self.is_parent_node(parent_node, compare_node)

    def use_node(self, obj):
        obj.use_node()
        self.refresh_all()

    def refresh_all(self):
        self.refresh_status()
        self.refresh_expanded()

    def refresh_status(self):
        if self.active_node:
            status_text = html_to_text(self.active_node.status_text())
            self.session.set_text_status(status_text)

    def refresh_expanded(self):
        self.refresh_children(self.root)

    def refresh_children(self, item):
        child, i = self.GetFirstChild(item)
        while child.IsOk():
            self.refresh_item(child)
            if self.IsExpanded(child):
                self.refresh_children(child)
            child, i = self.GetNextChild(item, i)

    def refresh_item(self, item):
        node = self.GetItemData(item)
        if node:
            node.refresh()

    def set_roll_value(self, value):
        """Set the value to be used for the __roll magic variable."""
        self.roll_value = value
        for node in self.auto_reset_nodes:
            node.reset_node()
        self.refresh_expanded()

    def add_auto_reset_node(self, node):
        self.auto_reset_nodes.append(node)

    def del_auto_reset_node(self, node):
        self.auto_reset_nodes.remove(node)

    def activate(self, node):
        if self.active_node:
            self.active_node.active = False
        self.active_node = node
        self.SetItemBold(node.mytree_node, True)

    def deactivate(self, node):
        if self.active_node == node:
            self.SetItemBold(node.mytree_node, False)
            self.active_node = None
            self.session.set_text_status(Settings.lookup("player.status").value)
