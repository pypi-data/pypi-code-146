# Copyright (C) 2009-2020 David Vrabel
# Copyright (C) 2000-2001 The OpenRPG Project
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.

import wx

from orpg.config import Settings
import orpg.lib.ui as ui
from orpg.networking.mplay_client import OPENRPG_PORT

class server_instance:
    def __init__(self, address, port):
        self.address = address
        self.port = port

    def name(self):
        return self.address + ":" + str(self.port)

    def __eq__(self, obj):
        return self.address == obj.address and self.port == obj.port

class GameServerDialog(wx.Dialog):

    recent_servers = Settings.define("client.recent_servers", "")

    def __init__(self,parent):
        wx.Dialog.__init__(self, parent, -1, title="Browse Servers", style=wx.DEFAULT_DIALOG_STYLE)
        self.frame = parent
        self.session = self.frame.session

        self.servers = []
        self.build_ctrls()
        self.refresh_server_list()

    def build_ctrls(self):
        self.server_list = wx.ListCtrl(self, style=(wx.LC_REPORT
                                                    | wx.SUNKEN_BORDER
                                                    | wx.LC_SINGLE_SEL))
        self.server_list.InsertColumn(0, "Address", wx.LIST_FORMAT_LEFT, 300)
        self.server_list.InsertColumn(1, "Port", wx.LIST_FORMAT_LEFT, 60)
        self.address_text = wx.TextCtrl(self, -1)

        self.connect_btn =  wx.Button(self, label="Connect")
        self.disconnect_btn = wx.Button(self, label="Disconnect")

        self.room_list = wx.ListCtrl(self, style=(wx.LC_REPORT
                                                  | wx.SUNKEN_BORDER
                                                  | wx.LC_SINGLE_SEL))
        self.room_list.InsertColumn(0, "Room Name", wx.LIST_FORMAT_LEFT, 200)
        self.room_list.InsertColumn(1, "Players", wx.LIST_FORMAT_LEFT, 80)
        self.room_list.InsertColumn(2, "Password", wx.LIST_FORMAT_LEFT, 80)
        self.join_btn = wx.Button(self, label="Join")

        self.room_name_text = wx.TextCtrl(self, -1)
        self.room_pwd_text = wx.TextCtrl(self, -1)
        self.room_admin_pwd_text = wx.TextCtrl(self, -1)
        self.create_btn = wx.Button(self, label="Create")

        self.close_btn = wx.Button(self, wx.ID_CLOSE)

        # Server sizer.
        server_sizer = wx.BoxSizer(wx.VERTICAL)
        server_sizer.Add(ui.StaticTextHeader(self, label="Recent Servers"))
        server_sizer.Add((0, 6))
        server_sizer.Add(self.server_list, 1, wx.EXPAND | wx.LEFT, border=12)
        server_sizer.Add((0, 12))
        server_sizer.Add(ui.StaticTextHeader(self, label="Server Address"))
        server_sizer.Add((0, 6))
        server_sizer.Add(self.address_text, 0, wx.EXPAND | wx.LEFT, border=12)
        server_sizer.Add((0, 6))
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        hbox.Add(self.connect_btn)
        hbox.Add((6, 0))
        hbox.Add(self.disconnect_btn)
        server_sizer.Add(hbox, 0, wx.ALIGN_RIGHT)

        # Room sizer
        # - Join
        room_sizer = wx.BoxSizer(wx.VERTICAL)
        room_sizer.Add(ui.StaticTextHeader(self, label="Join Room"))
        room_sizer.Add((0, 6))
        room_sizer.Add(self.room_list, 1, wx.EXPAND | wx.LEFT, border=12)
        room_sizer.Add((0, 6))
        room_sizer.Add(self.join_btn, 0, wx.ALIGN_RIGHT)
        room_sizer.Add((0, 12))
        # - Create
        room_sizer.Add(ui.StaticTextHeader(self, label="Create Room"))
        room_sizer.Add((0, 6))
        fbox = wx.FlexGridSizer(rows=8, cols=2, hgap=1, vgap=1)
        fbox.AddGrowableCol(1)
        fbox.Add(wx.StaticText(self, label="Room Name"), 0, wx.ALIGN_CENTER_VERTICAL|wx.RIGHT, border=6)
        fbox.Add(self.room_name_text, 0, wx.EXPAND)
        fbox.Add(wx.StaticText(self, label="Password"), 0, wx.ALIGN_CENTER_VERTICAL|wx.RIGHT, border=6)
        fbox.Add(self.room_pwd_text, 0, wx.EXPAND)
        fbox.Add(wx.StaticText(self, label="Admin Password"), 0, wx.ALIGN_CENTER_VERTICAL|wx.RIGHT, border=6)
        fbox.Add(self.room_admin_pwd_text, 0, wx.EXPAND)
        room_sizer.Add(fbox, 0, wx.EXPAND | wx.LEFT, border=12)
        room_sizer.Add((0, 6))
        room_sizer.Add(self.create_btn, 0, wx.ALIGN_RIGHT)

        # Server | Room
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        hbox.Add(server_sizer, 1, wx.EXPAND)
        hbox.Add((18, 0))
        hbox.Add(room_sizer, 1, wx.EXPAND)
        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(hbox, 1, wx.EXPAND)
        vbox.Add((0, 12))
        vbox.Add(self.close_btn, 0, wx.ALIGN_RIGHT)

        self.box = wx.BoxSizer(wx.VERTICAL)
        self.box.Add(vbox, 1, wx.EXPAND | wx.ALL, border = 12)
        self.box.SetSizeHints(self)

        self.SetSizer(self.box)
        self.SetAutoLayout(True)
        self.Fit()

        ## Event Handlers
        self.server_list.Bind(wx.EVT_LIST_ITEM_SELECTED, self.on_server_list_selected)
        self.server_list.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.on_server_list_activated)
        self.address_text.Bind(wx.EVT_TEXT, self.on_address_text)
        self.connect_btn.Bind(wx.EVT_BUTTON, self.on_connect)
        self.disconnect_btn.Bind(wx.EVT_BUTTON, self.on_disconnect)

        self.room_list.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.on_room_list_activated)
        self.join_btn.Bind(wx.EVT_BUTTON, self.on_join)

        self.create_btn.Bind(wx.EVT_BUTTON, self.on_create)

        self.close_btn.Bind(wx.EVT_BUTTON, self.on_close)

        self.set_connected(self.session.is_connected())

    def on_server_list_selected(self, evt):
        address = self.servers[evt.Index].name()
        self.address_text.ChangeValue(address)

    def on_server_list_activated(self, evt):
        address = self.address_text.GetValue()
        self.do_connect(address)

    def on_address_text(self, evt):
        selected_server = self.server_list.GetFirstSelected()
        if selected_server >= 0:
            self.server_list.Select(selected_server, False)

    def on_connect(self, evt):
        address = self.address_text.GetValue()
        self.do_connect(address)

    def on_disconnect(self, evt):
        self.frame.kill_mplay_session()

    def on_room_list_activated(self, evt):
        self.do_join_group(evt.Index)

    def on_join(self, evt):
        selected_room = self.room_list.GetFirstSelected()
        if selected_room >= 0:
            self.do_join_group(selected_room)

    def on_create(self, evt):
        self.do_create_group()

    def on_close(self, evt):
        self.EndModal(wx.ID_CLOSE)

    def set_connected(self,connected):
        self.connect_btn.Enable(not connected)
        self.disconnect_btn.Enable(connected)
        self.join_btn.Enable(connected)
        self.create_btn.Enable(connected)
        if not connected:
            self.room_list.DeleteAllItems()
            self.cur_room_index = -1

    def refresh_rooms(self):
        self.room_list.DeleteAllItems()
        for g in self.session.get_groups():
            i = self.room_list.GetItemCount()
            if (g[2]=="True") or (g[2]=="1"):
                pwd="Yes"
            else:
                pwd="No"
            self.room_list.InsertItem(i, g[1])
            self.room_list.SetItem(i, 1, g[3])
            self.room_list.SetItem(i, 2, pwd)
            self.room_list.SetItemData(i, int(g[0]))

    def refresh_server_list(self):
        self.servers = []
        self.server_list.DeleteAllItems()

        if not self.recent_servers.value:
            return

        for server in self.recent_servers.value.split(","):
            a = server.split(':')
            address = a[0]
            if len(a) > 1:
                port = int(a[1])
            else:
                port = OPENRPG_PORT
            self.servers.append(server_instance(address, port))
            i = self.server_list.GetItemCount()
            self.server_list.InsertItem(i, address)
            self.server_list.SetItem(i, 1, str(port))

    def add_server_bookmark(self, server):
        a = server.split(':')
        address = a[0]
        if len(a) > 1:
            port = int(a[1])
        else:
            port = OPENRPG_PORT
        server = server_instance(address, port)

        try:
            self.servers.remove(server)
        except ValueError:
            pass
        self.servers.insert(0, server)
        if len(self.servers) > 5:
            self.servers.pop()

        self.recent_servers.value = ",".join([s.name() for s in self.servers])
        self.refresh_server_list()

    def do_connect(self, address):
        if self.session.is_connected():
            if self.session.host_server == address:
                return
            else:
                self.frame.kill_mplay_session()

        self.frame.chat.InfoPost("Locating server at " + address + "...")
        if self.session.connect(address):
            self.add_server_bookmark(address)
            self.frame.start_timer()
        else:
            self.frame.chat.SystemPost("Failed to connect to game server...")

    def do_join_group(self, index):
        group_id = str(self.room_list.GetItemData(index))
        group = self.session.get_group_info(group_id)
        if (group[2] == "True") or (group[2] == "1"):
            pwd = self.frame.password_manager.GetPassword("room", group_id)
            if pwd is None: # User cancelled.
                return
        else:
            pwd = ""
        self.session.send_join_group(group_id,pwd)
        self.EndModal(wx.ID_CLOSE)

    def do_create_group(self):
        name = self.room_name_text.GetValue()
        pwd = self.room_pwd_text.GetValue()
        admin_pwd = self.room_admin_pwd_text.GetValue()

        self.session.send(f"{self.session.name} is creating room '{name}'.")
        self.session.send_create_group(name, pwd, admin_pwd, "")
        self.EndModal(wx.ID_CLOSE)
