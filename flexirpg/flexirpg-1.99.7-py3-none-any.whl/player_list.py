# Player list window
#
# Copyright 2020 David Vrabel
# Copyright (C) 2000-2001 The OpenRPG Project
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.

import wx

from orpg.config import Settings
from orpg.lib.text import html_to_text
from orpg.networking.roles import *
import orpg.tools.bitmap

#########################
#player frame window
#########################
PLAYER_BOOT = wx.NewId()
PLAYER_WHISPER = wx.NewId()
PLAYER_ROLE_MENU = wx.NewId()
PLAYER_ROLE_LURKER = wx.NewId()
PLAYER_ROLE_PLAYER = wx.NewId()
PLAYER_ROLE_GM = wx.NewId()
PLAYER_SHOW_VERSION = wx.NewId()
WG_LIST = {}

PLAYER_WG_MENU = wx.NewId()
PLAYER_WG_CREATE = wx.NewId()
PLAYER_WG_CLEAR_ALL = wx.NewId()
WG_MENU_LIST = {}

PLAYER_COMMAND_MENU = wx.NewId()
PLAYER_COMMAND_PASSWORD_ALTER = wx.NewId()
PLAYER_COMMAND_ROOM_RENAME = wx.NewId()

class player_list(wx.ListCtrl):
    def __init__(self, parent):
        wx.ListCtrl.__init__(self, parent, -1, wx.DefaultPosition, wx.DefaultSize,
                             wx.LC_REPORT|wx.SUNKEN_BORDER|wx.EXPAND|wx.LC_HRULES)
        self.frame = parent
        self.session = self.frame.session

        self._imageList = wx.ImageList( 16, 16, False )
        self._imageList.Add(orpg.tools.bitmap.create_from_file("icon_gm.png"))
        self._imageList.Add(orpg.tools.bitmap.create_from_file("icon_player.png"))
        self._imageList.Add(orpg.tools.bitmap.create_from_file("icon_lurker.png"))
        self._imageList.Add(orpg.tools.bitmap.create_from_file("icon_typing.png"))
        self.SetImageList( self._imageList, wx.IMAGE_LIST_SMALL )
        self._role_icons = { ROLE_GM: 0, ROLE_PLAYER: 1, ROLE_LURKER: 2, }

        # Create our column headers
        self.InsertColumn( 0, "ID", width=wx.LIST_AUTOSIZE )
        self.InsertColumn( 1, "Player", width=wx.LIST_AUTOSIZE )
        self.InsertColumn( 2, "Status" )

        # Main Menu
        self.wgMenu = wx.Menu()
        # Add the Base Menu items, so they are always at the bottom
        self.wgMenu.Append(PLAYER_WG_CREATE, "Create")
        self.wgMenu.Append(PLAYER_WG_CLEAR_ALL, "Delete All Groups")

        # Create the role menu
        self.roleMenu = wx.Menu()
        self.roleMenu.SetTitle( "Assign Role" )
        self.roleMenu.Append( PLAYER_ROLE_LURKER, "Lurker" )
        self.roleMenu.Append( PLAYER_ROLE_PLAYER, "Player" )
        self.roleMenu.Append( PLAYER_ROLE_GM, "GM" )

        # Create the room control menu
        self.commandMenu = wx.Menu()
        self.commandMenu.SetTitle( "Room Controls" )
        self.commandMenu.Append( PLAYER_COMMAND_PASSWORD_ALTER, "Password" )
        self.commandMenu.Append( PLAYER_COMMAND_ROOM_RENAME, "Room Name" )
        self.commandMenu.AppendSeparator()

        # Create the pop up menu
        self.menu = wx.Menu()
        self.menu.SetTitle( "Player Menu" )
        self.menu.Append( PLAYER_BOOT, "Boot" )
        self.menu.AppendSeparator()
        self.menu.Append( PLAYER_WHISPER, "Whisper" )
        self.menu.Append(PLAYER_WG_MENU, "Whisper Groups", self.wgMenu)
        self.menu.AppendSeparator()
        self.menu.Append( PLAYER_COMMAND_MENU, "Room Control", self.commandMenu )
        self.menu.AppendSeparator()
        self.menu.Append( PLAYER_ROLE_MENU, "Assign Role", self.roleMenu )
        self.menu.AppendSeparator()
        self.menu.Append( PLAYER_SHOW_VERSION, "Version" )

        # Event processing for our menu
        self.Bind(wx.EVT_MENU, self.on_menu_item, id=PLAYER_BOOT)
        self.Bind(wx.EVT_MENU, self.on_menu_item, id=PLAYER_WHISPER)
        self.Bind(wx.EVT_MENU, self.on_menu_role_change, id=PLAYER_ROLE_LURKER)
        self.Bind(wx.EVT_MENU, self.on_menu_role_change, id=PLAYER_ROLE_PLAYER)
        self.Bind(wx.EVT_MENU, self.on_menu_role_change, id=PLAYER_ROLE_GM)
        self.Bind(wx.EVT_MENU, self.on_menu_item, id=PLAYER_SHOW_VERSION)
        self.Bind(wx.EVT_MENU, self.on_menu_whispergroup, id=PLAYER_WG_CREATE)
        self.Bind(wx.EVT_MENU, self.on_menu_whispergroup, id=PLAYER_WG_CLEAR_ALL)
        self.Bind(wx.EVT_MENU, self.on_menu_password, id=PLAYER_COMMAND_PASSWORD_ALTER)
        self.Bind(wx.EVT_MENU, self.on_menu_room_rename, id=PLAYER_COMMAND_ROOM_RENAME)
        self.Bind(wx.EVT_LEFT_DCLICK, self.on_d_lclick)
        self.Bind(wx.EVT_RIGHT_DOWN, self.on_menu)
        self.sized = 1

    def on_menu_password( self, evt ):
        id = evt.GetId()
        boot_pwd = self.frame.password_manager.GetPassword("admin", self.session.group_id)
        if boot_pwd != None:
            alter_pwd_dialog = wx.TextEntryDialog(self,"Enter new room password: (blank for no password)","Alter Room Password")
            if alter_pwd_dialog.ShowModal() == wx.ID_OK:
                new_pass = alter_pwd_dialog.GetValue()
                self.frame.chat.InfoPost( "Requesting password change on server..." )
                self.session.set_room_pass(new_pass, boot_pwd)

    def on_menu_room_rename( self, evt ):
        id = evt.GetId()
        boot_pwd = self.frame.password_manager.GetPassword("admin", self.session.group_id)
        if boot_pwd != None:
            alter_name_dialog = wx.TextEntryDialog(self,"Enter new room name: ","Change Room Name")
            if alter_name_dialog.ShowModal() == wx.ID_OK:
                new_name = alter_name_dialog.GetValue()
                self.frame.chat.InfoPost( "Requesting room name change on server..." )
                loc = new_name.find("&")
                oldloc=0
                while loc > -1:
                    loc = new_name.find("&",oldloc)
                    if loc > -1:
                        b = new_name[:loc]
                        e = new_name[loc+1:]
                        new_name = b + "&amp;" + e
                        oldloc = loc +1
                loc = new_name.find("'")
                oldloc=0
                while loc > -1:
                    loc = new_name.find("'",oldloc)
                    if loc > -1:
                        b = new_name[:loc]
                        e = new_name[loc+1:]
                        new_name = b + "&#39;" + e
                        oldloc = loc +1
                loc = new_name.find('"')
                oldloc=0
                while loc > -1:
                    loc = new_name.find('"',oldloc)
                    if loc > -1:
                        b = new_name[:loc]
                        e = new_name[loc+1:]
                        new_name = b + "&quote" + e
                        oldloc = loc +1
                self.session.set_room_name(new_name, boot_pwd)

    def clean_sub_menus(self):
        for mid in WG_MENU_LIST:
            try:
                self.wgMenu.Remove(WG_MENU_LIST[mid]["menuid"])
                WG_MENU_LIST[mid]["menu"].Destroy()
            except:
                self.wgMenu.UpdateUI()
        if self.wgMenu.GetMenuItemCount() == 2:
            WG_MENU_LIST.clear()
        return

    def on_menu_whispergroup( self, evt ):
        "Add/Remove players from Whisper Groups"
        id = evt.GetId()
        item = self.GetItem( self.selected_item )
        #See if it is the main menu
        if id == PLAYER_WG_CREATE:
            create_new_group_dialog = wx.TextEntryDialog(self,"Enter Group Name","Create New Whisper Group")
            if create_new_group_dialog.ShowModal() == wx.ID_OK:
                group_name = create_new_group_dialog.GetValue()
                WG_LIST[group_name] = {}
            return
        elif id == PLAYER_WG_CLEAR_ALL:
            WG_LIST.clear()
            return

        #Check Sub Menus
        for mid in WG_MENU_LIST:
            if id == WG_MENU_LIST[mid]["add"]:
                WG_LIST[mid][int(item.GetText())] = int(item.GetText())
                return
            elif id == WG_MENU_LIST[mid]["remove"]:
                del WG_LIST[mid][int(item.GetText())]
                return
            elif id == WG_MENU_LIST[mid]["clear"]:
                WG_LIST[mid].clear()
                return
            elif id == WG_MENU_LIST[mid]["whisper"]:
                self.frame.chat.set_chat_text("/gw " + mid + "=")
                return
        return

    def on_menu_role_change(self, evt):
        "Change the role of the selected id."
        player_id = str(self.GetItemData(self.selected_item))
        if evt.GetId() == PLAYER_ROLE_GM:
            role = ROLE_GM
        elif evt.GetId() == PLAYER_ROLE_PLAYER:
            role = ROLE_PLAYER
        else:
            role = ROLE_LURKER
        group = self.session.get_group_info(self.session.group_id)

        if group.has_admin_pwd:
            role_pwd = self.frame.password_manager.GetPassword("admin", self.session.group_id)
        else:
            role_pwd = ""
        if role_pwd is not None:
            self.session.set_role(player_id, role, role_pwd)

    def on_d_lclick(self,evt):
        pos = wx.Point(evt.GetX(),evt.GetY())
        (item, flag) = self.HitTest(pos)
        if item > -1:
            self.do_whisper(item)

    def on_menu_item(self,evt):
        id = evt.GetId()

        if id == PLAYER_BOOT:
            id = str(self.GetItemData(self.selected_item))
            boot_pwd = self.frame.password_manager.GetPassword("admin", self.session.group_id)
            if boot_pwd != None:
                self.session.boot_player(id,boot_pwd)

        elif id == PLAYER_WHISPER:
            self.do_whisper(self.selected_item)

        elif id == PLAYER_SHOW_VERSION:
            id = str(self.GetItemData(self.selected_item))
            wx.MessageBox(f"Running client version {self.session.players[id].client_string}",
                          "Version")

    def on_menu(self, evt):
        pos = wx.Point(evt.GetX(),evt.GetY())
        (item, flag) = self.HitTest(pos)
        if item > -1:
            self.SetItemState(item, wx.LIST_STATE_SELECTED, wx.LIST_STATE_SELECTED)
            self.selected_item = item
            #  This if-else block makes the menu item to boot players active or inactive, as appropriate
            if self.session.group_id == "0":
                self.menu.Enable(PLAYER_BOOT,0)
                self.menu.SetLabel(PLAYER_BOOT,"Can't boot from Lobby")
            else:
                self.menu.Enable(PLAYER_BOOT,1)
                self.menu.SetLabel(PLAYER_BOOT,"Boot")
            self.menu.Enable(PLAYER_WG_MENU, True)
            item = self.GetItem( self.selected_item )

            if len(WG_MENU_LIST) > len(WG_LIST):
                self.clean_sub_menus()

            if len(WG_LIST) == 0:
                self.wgMenu.Enable(PLAYER_WG_CLEAR_ALL, False)
            else:
                self.wgMenu.Enable(PLAYER_WG_CLEAR_ALL, True)

            for gid in WG_LIST:
                if gid not in WG_MENU_LIST:
                    WG_MENU_LIST[gid] = {}
                    WG_MENU_LIST[gid]["menuid"] = wx.NewId()
                    WG_MENU_LIST[gid]["whisper"] = wx.NewId()
                    WG_MENU_LIST[gid]["add"] = wx.NewId()
                    WG_MENU_LIST[gid]["remove"] = wx.NewId()
                    WG_MENU_LIST[gid]["clear"] = wx.NewId()
                    WG_MENU_LIST[gid]["menu"] = wx.Menu()
                    WG_MENU_LIST[gid]["menu"].SetTitle(gid)
                    WG_MENU_LIST[gid]["menu"].Append(WG_MENU_LIST[gid]["whisper"], "Whisper")
                    WG_MENU_LIST[gid]["menu"].Append(WG_MENU_LIST[gid]["add"], "Add")
                    WG_MENU_LIST[gid]["menu"].Append(WG_MENU_LIST[gid]["remove"], "Remove")
                    WG_MENU_LIST[gid]["menu"].Append(WG_MENU_LIST[gid]["clear"], "Clear")
                    self.wgMenu.PrependMenu(WG_MENU_LIST[gid]["menuid"], gid, WG_MENU_LIST[gid]["menu"])

                if int(item.GetText()) in WG_LIST[gid]:
                    WG_MENU_LIST[gid]["menu"].Enable(WG_MENU_LIST[gid]["remove"], True)
                    WG_MENU_LIST[gid]["menu"].Enable(WG_MENU_LIST[gid]["add"], False)
                else:
                    WG_MENU_LIST[gid]["menu"].Enable(WG_MENU_LIST[gid]["remove"], False)
                    WG_MENU_LIST[gid]["menu"].Enable(WG_MENU_LIST[gid]["add"], True)

                if len(WG_LIST[gid]) == 0:
                    WG_MENU_LIST[gid]["menu"].Enable(WG_MENU_LIST[gid]["whisper"], False)
                    WG_MENU_LIST[gid]["menu"].Enable(WG_MENU_LIST[gid]["clear"], False)
                else:
                    WG_MENU_LIST[gid]["menu"].Enable(WG_MENU_LIST[gid]["whisper"], True)
                    WG_MENU_LIST[gid]["menu"].Enable(WG_MENU_LIST[gid]["clear"], True)

                #Event Stuff
                self.Bind(wx.EVT_MENU, self.on_menu_whispergroup, id=WG_MENU_LIST[gid]["whisper"] )
                self.Bind(wx.EVT_MENU, self.on_menu_whispergroup, id=WG_MENU_LIST[gid]["add"] )
                self.Bind(wx.EVT_MENU, self.on_menu_whispergroup, id=WG_MENU_LIST[gid]["remove"] )
                self.Bind(wx.EVT_MENU, self.on_menu_whispergroup, id=WG_MENU_LIST[gid]["clear"] )
            self.PopupMenu(self.menu,pos)

    def add_player(self, player):
        i = self.InsertItem(0, player.id, 0)
        self.SetItemData(i, int(player.id))
        self.update_entry(i, player)

    def del_player(self, player):
        i = self.FindItem(-1, int(player.id))
        self.DeleteItem(i)
        for gid in WG_LIST:
            if int(id) in WG_LIST[gid]:
                del WG_LIST[gid][int(player.id)]
        self.resize_columns()

    #  This method updates the player info
    #
    #  self:  reference to this PlayerList
    #  player:  reference to a player structure(list)
    #
    #  Returns:  None
    #
    def update_player(self,player):
        i = self.FindItem(-1, int(player.id))
        self.update_entry(i, player)

    def update_entry(self, idx, player):
        if player.typing:
            icon = len(self._role_icons)
        else:
            icon = self._role_icons[player.role]
        self.SetItemColumnImage(idx, 0, icon)
        self.SetItem(idx, 1, html_to_text(player.name))
        self.SetItem(idx, 2, player.status)
        self.resize_columns()

    def resize_columns(self):
        self.SetColumnWidth(0, wx.LIST_AUTOSIZE)
        self.SetColumnWidth(1, wx.LIST_AUTOSIZE)
        self.SetColumnWidth(2, self.GetClientSize().x - self.GetColumnWidth(0) - self.GetColumnWidth(1))

    def reset(self):
        WG_LIST.clear()
        self.DeleteAllItems()

    def do_whisper(self, item):
        id = self.GetItemText(item)
        if Settings.lookup("chat.use_whisper_tab").value:
            self.frame.chat.open_whisper_tab(id)
        else:
            self.frame.chat.set_chat_text("/w " + id + "=")
