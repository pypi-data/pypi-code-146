# FlexiRPG -- Application and main frame.
#
# Copyright (C) 2009-2021 David Vrabel
# Copyright (C) 2000-2001 The OpenRPG Project
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.

import time

import wx
import wx.aui

from orpg.config import Paths, Settings
from orpg.log import logger, logger_setup
import orpg.player_list
import orpg.tools.passtool
import orpg.lib.ui as ui
import orpg.lib.xmlutil as xmlutil
from orpg.version import *

import orpg.mapper.image
import orpg.mapper.imageprovider
import orpg.mapper.imagelibrary
import orpg.mapper.displayimage

image_library = orpg.mapper.imagelibrary.ImageLibrary(orpg.mapper.displayimage.DisplayImage)

import orpg.gametree.gametree
import orpg.chat.chatwindow
import orpg.networking.mplay_client
import orpg.networking.mplay_queue
import orpg.networking.gsclient
import orpg.mapper.map
import orpg.tools.settingsdialog

####################################
## Main Frame
####################################

OPT_FILE_SERVERS = 1000
OPT_FILE_QUIT = 1001
OPT_EDIT_PREFS = 1002
OPT_HELP_ABOUT = 1003

class orpgFrame(wx.Frame):

    player_name = Settings.define("player.name", "No Name")
    player_status = Settings.define("player.status", "")
    client_heartbeat = Settings.define("client.heartbeat", True)

    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, id, title, wx.Point(100, 100), wx.Size(600,420), style=wx.DEFAULT_FRAME_STYLE)

        self._mgr = wx.aui.AuiManager(self)

        if wx.Platform == '__WXMSW__':
            icon = wx.Icon(Paths.image("icon_flexirpg.ico"), wx.BITMAP_TYPE_ICO)
        else:
            icon = wx.Icon(Paths.image("icon_flexirpg.png"), wx.BITMAP_TYPE_PNG)
        self.SetIcon(icon)

        # create session
        call_backs = {"on_receive":self.on_receive,
                "on_mplay_event":self.on_mplay_event,
                "on_group_event":self.on_group_event,
                "on_player_event":self.on_player_event,
                "on_password_signal":self.on_password_signal}
        self.session = orpg.networking.mplay_client.mplay_client(
            self.player_name.value, self, call_backs)
        self.session.set_text_status(self.player_status.value)

        self.Bind(orpg.networking.mplay_queue.EVT_QUEUE_READY, self.session.poll)
        self.ping_timer = wx.Timer(self, wx.NewId())
        self.Bind(wx.EVT_TIMER, self.session.update, self.ping_timer)

        image_library.register_provider(orpg.mapper.imageprovider.ImageProviderCache())
        image_library.register_provider(orpg.mapper.imageprovider.ImageProviderClient(self.session,
                                                                                      image_library))

        self.password_manager = orpg.tools.passtool.PassTool()

        # build frame windows
        self.build_menu()
        self.build_gui()
        self.build_additional_menus()

        self.tree.load_tree(Paths.config("tree.xml"))

        self.player_name.watch(self.on_player_name)
        self.player_status.watch(self.on_player_status)

        self.Bind(wx.EVT_CLOSE, self.OnCloseWindow)

    def on_password_signal(self, signal, type, id, data):
        if signal == "fail":
            self.password_manager.ClearPassword(type, id)

    def build_menu(self):
        self.mainmenu = wx.MenuBar()

        menu = wx.Menu()
        menu.Append(OPT_FILE_SERVERS, "&Browse Servers\tCtrl-B")
        menu.AppendSeparator()
        menu.Append(OPT_FILE_QUIT, "&Quit\tCtrl-Q")
        self.mainmenu.Append(menu, "&File")

        menu = wx.Menu()
        menu.Append(OPT_EDIT_PREFS, "&Preferences")
        self.mainmenu.Append(menu, "&Edit")

        menu = wx.Menu()
        menu.Append(OPT_HELP_ABOUT, "&About")
        self.mainmenu.Append(menu, "&Help")

        self.SetMenuBar(self.mainmenu)

        self.Bind(wx.EVT_MENU, self.on_menu_file_servers, id=OPT_FILE_SERVERS)
        self.Bind(wx.EVT_MENU, self.on_menu_file_quit, id=OPT_FILE_QUIT)
        self.Bind(wx.EVT_MENU, self.on_menu_edit_prefs, id=OPT_EDIT_PREFS)
        self.Bind(wx.EVT_MENU, self.on_menu_help_about, id=OPT_HELP_ABOUT)


    def on_player_name(self, setting):
        self.session.set_name(setting.value)

    def on_player_status(self, setting):
        if not self.tree.active_node:
            self.session.set_text_status(setting.value)

    #################################
    ## All Menu Events
    #################################

    # File Menu
    def on_menu_file_servers(self, evt):
        self.gs.ShowModal()

    def on_menu_file_quit(self, evt):
        self.OnCloseWindow(0)

    # Edit Menu
    def on_menu_edit_prefs(self, evt):
        self.settings_dialog.show()

    # Windows Menu
    def on_menu_windows(self, event):
        menuid = event.GetId()
        name = self.mainwindows[menuid]
        if self._mgr.GetPane(name).IsShown():
            self._mgr.GetPane(name).Hide()
        else:
            self._mgr.GetPane(name).Show()
        self._mgr.Update()

    # Help Menu
    def on_menu_help_about(self, evt):
        dlg = ui.AboutDialog(self, Paths.template("about.html"),
                             PRODUCT, VERSION)
        dlg.ShowModal()
        dlg.Destroy()

    #################################
    ##    Build the GUI
    #################################
    def build_gui(self):
        self.Freeze()
        filename = Paths.config("layout.xml")
        temp_file = open(filename)
        txt = temp_file.read()
        self.layout_doc = xmlutil.parseXml(txt)
        xml_dom = self.layout_doc.documentElement
        temp_file.close()

        self.windowsmenu = wx.Menu()
        self.mainwindows = {}
        h = int(xml_dom.getAttribute("height"))
        w = int(xml_dom.getAttribute("width"))
        posx = int(xml_dom.getAttribute("posx"))
        posy = int(xml_dom.getAttribute("posy"))
        maximized = int(xml_dom.getAttribute("maximized"))
        self.SetSize(posx, posy, w, h)

        children = xml_dom.childNodes
        for c in children:
            self.build_window(c, self)
        self.mainmenu.Insert(2, self.windowsmenu, 'Windows')

        self.gs = orpg.networking.gsclient.GameServerDialog(self)
        self.settings_dialog = orpg.tools.settingsdialog.SettingsDialog(self)

        self.Bind(wx.aui.EVT_AUI_PANE_CLOSE, self.onPaneClose)

        #Load the layout if one exists
        layout = xml_dom.getElementsByTagName("DockLayout")
        try:
            textnode = xmlutil.safe_get_text_node(layout[0])
            self._mgr.LoadPerspective(textnode.nodeValue)
        except:
            pass
        self._mgr.Update()
        self.Maximize(maximized)
        self.Thaw()

    def build_window(self, xml_dom, parent_wnd):
        name = xml_dom.nodeName
        if name == "DockLayout" or name == "dock":
            return
        dir = xml_dom.getAttribute("direction")
        pos = xml_dom.getAttribute("pos")
        height = xml_dom.getAttribute("height")
        width = xml_dom.getAttribute("width")
        cap = xml_dom.getAttribute("caption")
        dockable = xml_dom.getAttribute("dockable")
        layer = xml_dom.getAttribute("layer")

        try:
            layer = int(layer)
            dockable = int(dockable)
        except:
            layer = 0
            dockable = 1

        if name == "map":
            temp_wnd = orpg.mapper.map.map_wnd(parent_wnd, -1)
            self.map = temp_wnd
        elif name == "tree":
            temp_wnd = orpg.gametree.gametree.game_tree(parent_wnd, -1)
            self.tree = temp_wnd

        elif name == "chat":
            temp_wnd = orpg.chat.chatwindow.ChatWindow(parent_wnd, wx.DefaultSize)
            self.chattabs = temp_wnd
            self.chat = temp_wnd.MainChatPanel

        elif name == "player":
            temp_wnd = orpg.player_list.player_list(parent_wnd)
            self.players = temp_wnd

        if parent_wnd != self:
            #We dont need this if the window are beeing tabed
            return temp_wnd
        menuid = wx.NewId()
        self.windowsmenu.Append(menuid, cap, kind=wx.ITEM_CHECK)
        self.windowsmenu.Check(menuid, True)
        self.Bind(wx.EVT_MENU, self.on_menu_windows, id=menuid)
        self.mainwindows[menuid] = cap
        wndinfo = wx.aui.AuiPaneInfo()
        wndinfo.DestroyOnClose(False)
        wndinfo.Name(cap)
        wndinfo.FloatingSize(wx.Size(int(width), int(height)))
        wndinfo.BestSize(wx.Size(int(width), int(height)))
        wndinfo.Layer(int(layer))
        wndinfo.Caption(cap)

# Lambda here should work!
        if dir.lower() == 'top':
            wndinfo.Top()
        elif dir.lower() == 'bottom':
            wndinfo.Bottom()
        elif dir.lower() == 'left':
            wndinfo.Left()
        elif dir.lower() == 'right':
            wndinfo.Right()
        elif dir.lower() == 'center':
            wndinfo.Center()
            wndinfo.CaptionVisible(False)

        if dockable != 1:
            wndinfo.Dockable(False)
            wndinfo.Floatable(False)
        if pos != '' or pos != '0' or pos != None:
            wndinfo.Position(int(pos))
        wndinfo.Show()
        self._mgr.AddPane(temp_wnd, wndinfo)
        return temp_wnd

    def onPaneClose(self, evt):
        pane = evt.GetPane()
        for wndid, wname in list(self.mainwindows.items()):
            if pane.name == wname:
                self.windowsmenu.Check(wndid, False)
                break
        evt.Skip()
        self._mgr.Update()

    def saveLayout(self):
        (x_size,y_size) = self.GetClientSize()
        (x_pos,y_pos) = self.GetPosition()
        if self.IsMaximized():
            max = 1
        else:
            max = 0
        dock_layout = str(self._mgr.SavePerspective())

        xml_dom = self.layout_doc.documentElement
        xml_dom.setAttribute("height", str(y_size))
        xml_dom.setAttribute("width", str(x_size))
        xml_dom.setAttribute("posx", str(x_pos))
        xml_dom.setAttribute("posy", str(y_pos))
        xml_dom.setAttribute("maximized", str(max))
        layout = xml_dom.getElementsByTagName("DockLayout")
        if layout:
            elem = layout[0]
        else:
            elem = self.layout_doc.createElement('DockLayout')
            xml_dom.appendChild(elem)
        textnode = xmlutil.safe_get_text_node(elem)
        textnode.nodeValue = str(self._mgr.SavePerspective())

        filename = Paths.user("layout.xml")
        temp_file = open(filename, "w")
        temp_file.write(xmlutil.toxml(xml_dom, 1))
        temp_file.close()

    def build_additional_menus(self):
        self.chat.build_menu()
        self.map.build_menu()

    def start_timer(self):
        if self.client_heartbeat.value:
            self.ping_timer.Start(1000*60)

    def kill_mplay_session(self):
        self.game_name = ""
        self.session.start_disconnect()

    def on_player_event(self, evt):
        id = evt.get_id()
        player = evt.get_data()
        time_str = time.strftime("%H:%M", time.localtime())
        if id == orpg.networking.mplay_client.PLAYER_NEW:
            self.players.add_player(player)
            self.chat.InfoPost(player.name + " (enter): " + time_str)
        elif id == orpg.networking.mplay_client.PLAYER_DEL:
            self.players.del_player(player)
            self.chat.InfoPost(player.name + " (exit): " + time_str)
        elif id == orpg.networking.mplay_client.PLAYER_UPDATE:
            self.players.update_player(player)
        self.players.Refresh()

    def on_group_event(self, evt):
        id = evt.get_id()
        group = evt.get_data()

        if id == orpg.networking.mplay_client.GROUP_NEW:
            self.gs.refresh_rooms()
        elif id == orpg.networking.mplay_client.GROUP_DEL:
            self.password_manager.RemoveGroupData(group.id)
            self.gs.refresh_rooms()
        elif id == orpg.networking.mplay_client.GROUP_UPDATE:
            self.gs.refresh_rooms()

    def on_receive(self, data, player):
        if player:
            display_name = player.name
        else:
            display_name = "Server Administrator"

        if data[:5] == "<tree":
            self.tree.on_receive_data(data,player)
            self.chat.InfoPost(display_name + " has sent you a tree node...")
            #self.tree.OnNewData(data)

        elif data[:4] == "<map":
            self.map.new_data(data)

        elif data[:5] == "<chat":
            msg = orpg.chat.chat_msg.chat_msg(data)
            self.chat.post_incoming_msg(msg,player)
        else:
        ##############################################################################################
        #  all this below code is for comptiablity with older clients and can be removed after a bit #
        ##############################################################################################
            if data[:3] == "/me":
                # This fixes the emote coloring to comply with what has been asked for by the user
                # population, not to mention, what I committed to many moons ago.
                #  In doing so, Woody's scheme has been tossed out.  I'm sure Woody won't be
                # happy but I'm invoking developer priveledge to satisfy user request, not to mention,
                # this scheme actually makes more sense.  In Woody's scheme, a user could over-ride another
                # users emote color.  This doesn't make sense, rather, people dictate their OWN colors...which is as
                # it should be in the first place and is as it has been with normal text.  In short, this makes
                # sense and is consistent.
                data = data.replace( "/me", "" )

                # Check to see if we find the closing ">" for the font within the first 22 values
                index = data[:22].find(  ">" )
                if index == -1:
                    data = "** " + self.chat.colorize( self.chat.infocolor, display_name + data ) + " **"

                else:
                    # This means that we found a valid font string, so we can simply plug the name into
                    # the string between the start and stop font delimiter
                    print("pre data = " + data)
                    data = data[:22] + "** " + display_name + " " + data[22:] + " **"
                    print("post data = " + data)

            elif data[:2] == "/w":
                data = data.replace("/w","")
                data = "<b>" + display_name + "</b> (whispering): " + data

            else:
                # Normal text
                if player:
                    data = "<b>" + display_name + "</b>: " + data
                else:
                    data = "<b><i><u>" + display_name + "</u>-></i></b> " + data
            self.chat.Post(data)

    def on_mplay_event(self, evt):
        id = evt.get_id()
        if id == orpg.networking.mplay_client.MPLAY_CONNECTED:
            self.chat.InfoPost("Game connected!")
            self.gs.set_connected(1)
            self.password_manager.ClearPassword("ALL")

        elif id == orpg.networking.mplay_client.MPLAY_DISCONNECTED:
            self.ping_timer.Stop()
            self.chat.SystemPost("Game disconnected!")
            self.players.reset()
            self.gs.set_connected(0)

        elif id== orpg.networking.mplay_client.MPLAY_GROUP_CHANGE:
            group = evt.get_data()
            self.chat.InfoPost("Moving to room '"+group[1]+"'..")
            self.players.reset()
        elif id== orpg.networking.mplay_client.MPLAY_GROUP_CHANGE_F:
            self.chat.SystemPost("Room access denied!")

    def OnCloseWindow(self, event):
        dlg = wx.MessageDialog(self, "Quit " + PRODUCT + "?", PRODUCT, wx.YES_NO)
        if dlg.ShowModal() == wx.ID_YES:
            dlg.Destroy()
            self.closed_confirmed()

    def closed_confirmed(self):
        self.saveLayout()

        try:
            self.tree.save_tree(Paths.user("tree.xml"))
        except:
            logger.exception("Error saving gametree")

        if self.session.get_status() == orpg.networking.mplay_client.MPLAY_CONNECTED:
            self.kill_mplay_session()

        self.ping_timer.Stop()
        self.chat.parent.chat_timer.Stop()

        self._mgr.UnInit()
        mainapp = wx.GetApp()
        mainapp.ExitMainLoop()
        self.Destroy()

    def show_browse_servers_window(self):
        self._mgr.GetPane("Browse Server Window").Show()
        self._mgr.Update()

    def hide_browse_servers_window(self):
        self._mgr.GetPane("Browse Server Window").Hide()
        self._mgr.Update()


########################################
## Application class
########################################
class orpgApp(wx.App):
    def OnInit(self):
        self.frame = orpgFrame(None, wx.ID_ANY, PRODUCT)
        self.frame.Raise()
        self.frame.Refresh()
        self.frame.Show(True)
        self.SetTopWindow(self.frame)

        return True

def run_client():
    """Run the FlexiRPG application."""
    logger_setup()
    mainapp = orpg.main.orpgApp()
    mainapp.MainLoop()
