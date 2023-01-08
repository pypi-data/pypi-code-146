# FlexiRPG -- main chat window.
#
# Copyright 2020 David Vrabel
# Copyright (C) 2000-2001 The OpenRPG Project
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.

import wx
import wx.lib.agw.flatnotebook as FNB

from orpg.config import Settings
from orpg.lib.text import html_to_text
import orpg.tools.bitmap
from .chatpanel import ChatPanel, MAIN_TAB, WHISPER_TAB, GROUP_TAB, NULL_TAB


class ChatWindow(FNB.FlatNotebook):
    """Main chat window.

    This is a tabbed notebook that holds one or more ChatPanels.

    """

    use_whisper_tab = Settings.define("chat.use_whisper_tab", False)
    use_gm_whisper_tab = Settings.define("chat.use_gm_whisper_tabs", False)
    use_group_whisper_tab = Settings.define("chat.use_group_whisper_tabs", False)

    def __init__(self, parent, size):
        FNB.FlatNotebook.__init__(self, parent, True, size=size,
                                  agwStyle=(FNB.FNB_DROPDOWN_TABS_LIST
                                            | FNB.FNB_NO_NAV_BUTTONS
                                            | FNB.FNB_MOUSE_MIDDLE_CLOSES_TABS
                                            | FNB.FNB_HIDE_ON_SINGLE_TAB
                                            | FNB.FNB_FANCY_TABS))

        self.frame = parent
        self.whisper_tabs = []
        self.group_tabs = []
        self.null_tabs = []
        self.il = wx.ImageList(16, 16)
        self.il.Add(orpg.tools.bitmap.create_from_file("icon_player.png"))
        self.il.Add(orpg.tools.bitmap.create_from_file("icon_blank.png"))
        self.SetImageList(self.il)
        self.chat_timer = wx.Timer(self, wx.NewId())
        # Create "main" chatpanel tab, undeletable, connected to 'public' room.
        self.MainChatPanel = ChatPanel(self, -1, MAIN_TAB, 'all')
        self.AddPage(self.MainChatPanel, "Main Room")
        self.SetPageImage(0, 1)
        self.Bind(wx.EVT_TIMER, self.MainChatPanel.typingTimerFunc)
        # Hook up event handler for flipping tabs
        self.Bind(FNB.EVT_FLATNOTEBOOK_PAGE_CHANGED, self.onPageChanged)
        self.Bind(FNB.EVT_FLATNOTEBOOK_PAGE_CHANGING, self.onPageChanging)
        self.Bind(FNB.EVT_FLATNOTEBOOK_PAGE_CLOSING, self.onCloseTab)
        self.GMChatPanel = None
        if self.use_gm_whisper_tab.value:
            self.create_gm_tab()
        self.SetSelection(0)

    def get_tab_index(self, chatpanel):
        "Return the index of a chatpanel in the wxNotebook."
        for i in range(self.GetPageCount()):
            if (self.GetPage(i) == chatpanel):
                return i

    def create_gm_tab(self):
        if self.GMChatPanel == None:
            self.GMChatPanel = ChatPanel(self, -1, MAIN_TAB, 'gm')
            self.AddPage(self.GMChatPanel, "GM", False)
            self.SetPageImage(self.GetPageCount()-1, 1)

    def create_whisper_tab(self, playerid):
        "Add a new chatpanel directly connected to integer 'playerid' via whispering."
        private_tab = ChatPanel(self, -1, WHISPER_TAB, playerid)
        playername = html_to_text(self.MainChatPanel.session.get_player_info(playerid).name)
        self.AddPage(private_tab, playername, False)
        self.whisper_tabs.append(private_tab)
        self.newMsg(self.GetPageCount()-1)
        return private_tab

    def create_group_tab(self, group_name):
        "Add a new chatpanel directly connected to integer 'playerid' via whispering."
        private_tab = ChatPanel(self, -1, GROUP_TAB, group_name)
        self.AddPage(private_tab, group_name, False)
        self.group_tabs.append(private_tab)
        self.newMsg(self.GetPageCount()-1)
        return private_tab

    def create_null_tab(self, tab_name):
        "Add a new chatpanel directly connected to integer 'playerid' via whispering."
        private_tab = ChatPanel(self, -1, NULL_TAB, tab_name)
        self.AddPage(private_tab, tab_name, False)
        self.null_tabs.append(private_tab)
        self.newMsg(self.GetPageCount()-1)
        return private_tab

    def open_whisper_tab(self, player_id):
        whisper_tab = False
        for tab in self.whisper_tabs:
            if tab.sendtarget == player_id:
                whisper_tab = tab
                break;
        if not whisper_tab:
            whisper_tab = self.create_whisper_tab(player_id)
        self.SetSelection(self.GetPageIndex(whisper_tab))
        whisper_tab.chattxt.SetFocus()

    def onCloseTab(self, evt):
        try:
            tabid = evt.GetSelection()
        except:
            tabid = self.GetSelection()

        if self.GetPageText(tabid) == 'Main Room':
            #send no close error to chat
            evt.Veto()
            return
        if self.GetPageText(tabid) == 'GM':
            msg = "Are You Sure You Want To Close This Page?"
            dlg = wx.MessageDialog(self, msg, "NotebookCtrl Question",
                                   wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION)

            if wx.Platform != '__WXMAC__':
                dlg.SetFont(wx.Font(8, wx.NORMAL, wx.NORMAL, wx.NORMAL, False))

            if dlg.ShowModal() in [wx.ID_NO]:
                dlg.Destroy()
                evt.Veto()
                return
            dlg.Destroy()
            self.GMChatPanel = None
            self.use_gm_whisper_tab.value = False
        panel = self.GetPage(tabid)
        if panel in self.whisper_tabs:
            self.whisper_tabs.remove(panel)
        elif panel in self.group_tabs:
            self.group_tabs.remove(panel)
        elif panel in self.null_tabs:
            self.null_tabs.remove(panel)

    def newMsg(self, tabid):
        if tabid != self.GetSelection():
            self.SetPageImage(tabid, 0)

    def onPageChanging(self, event):
        """When private chattabs are selected, set the bitmap back to 'normal'."""
        event.Skip()

    def onPageChanged(self, event):
        """When private chattabs are selected, set the bitmap back to 'normal'."""
        selected_idx = event.GetSelection()
        self.SetPageImage(selected_idx, 1)
        page = self.GetPage(selected_idx)
        #wx.CallAfter(page.set_chat_text_focus, 0)
        event.Skip()

