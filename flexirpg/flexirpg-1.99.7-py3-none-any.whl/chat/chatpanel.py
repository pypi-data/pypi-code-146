# FlexiRPG -- Chat panel for a chat tab.
#
# Copyright (C) 2000-2001 The OpenRPG Project
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.

import codecs
import time
import traceback

import wx

from orpg.config import Paths, Settings
from orpg.log import logger
import orpg.chat.chat_msg as chat_msg
import orpg.chat.chat_util as chat_util
from orpg.dieroller.parser import parse_all_dice_rolls, dice_roll_error
from orpg.lib.text import html_to_text
import orpg.lib.ui as ui
from orpg.networking.roles import *
from orpg.player_list import WG_LIST
import orpg.tools.bitmap
from orpg.tools.tab_complete import tab_complete

from .commands import ChatCommands
from .chatdisplay import ChatDisplay


MAIN_TAB = wx.NewId()
WHISPER_TAB = wx.NewId()
GROUP_TAB = wx.NewId()
NULL_TAB = wx.NewId()

DICE_D4   = 4
DICE_D6   = 6
DICE_D8   = 8
DICE_D10  = 10
DICE_D12  = 12
DICE_D20  = 20
DICE_D100 = 100

FORMAT_BOLD      = 101
FORMAT_ITALIC    = 102
FORMAT_UNDERLINE = 103
FORMAT_COLOR     = 104

SAVE_CHAT = 105


def log(text):
    filename = time.strftime('log-%Y-%m-%d.html', time.localtime(time.time()))
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S%z", time.gmtime(time.time()))
    header = f"[timestamp] : "
    try:
        with codecs.open(Paths.log(filename), 'a', 'utf-8') as f:
            f.write(f"{header}{text}<br />\n")
    except OSError:
        print("could not open " + Paths.user(filename) + ", ignoring...")
        pass


class ChatPanel(wx.Panel):
    """A panel for a ChatWindow tab.

    This includes the chat display (ChatDisplay), toolbar and text entry.

    """

    bgcolor = Settings.define("chat.color.background", wx.Colour(0xff, 0xff, 0xff))
    textcolor = Settings.define("chat.color.text", wx.Colour(0, 0, 0))
    mytextcolor = Settings.define("chat.color.player", wx.Colour(0, 0, 0x80))
    syscolor = Settings.define("chat.color.system", wx.Colour(0xff, 0, 0))
    infocolor = Settings.define("chat.color.info", wx.Colour(0xff, 0x80, 0))
    emotecolor = Settings.define("chat.color.emote", wx.Colour(0, 0x80, 0))

    macros = [Settings.define(f"chat.macro.f{f}", "") for f in range(12)]

    last_directory = Settings.define("chat.last_directory", "")

    # This is the initialization subroutine
    #
    # !self : instance of self
    # !parent : parent that defines the chatframe
    # !id :
    # !openrpg :
        # !sendtarget:  who gets outbound messages: either 'all' or a playerid
    def __init__(self, parent, id, tab_type, sendtarget):
        wx.Panel.__init__(self, parent, id)
        self.parent = parent
        self.frame = parent.frame
        self.session = self.frame.session

        # who receives outbound messages, either "all" or "playerid" string
        self.sendtarget = sendtarget
        self.type = tab_type
        self.h = 0
        self.histidx = -1
        self.temptext = ""
        self.history = []
        #self.lasthistevt = None
        self.parsed=0
        #chat commands
        self.chat_cmds = ChatCommands(self)

        self.mytextcolor.watch(self.on_color_player)

        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.Bind(wx.EVT_CHAR_HOOK, self.on_panel_char)
        self.build_ctrls()
        self.chatwnd.scroll_down()
        self.sendTyping(False)

    def build_menu(self):
        menu = wx.Menu()
        item = wx.MenuItem(menu, wx.ID_ANY, "&Chat Focus\tCtrl-H", "Chat Focus")
        self.setChatFocusMenu = item
        self.frame.Bind(wx.EVT_MENU, self.set_chat_text_focus, item)
        menu.Append(item)
        menu.AppendSeparator()
        item = wx.MenuItem(menu, wx.ID_ANY, "Save Chat &Log", "Save Chat Log")
        self.frame.Bind(wx.EVT_MENU, self.on_chat_save, item)
        menu.Append(item)
        item = wx.MenuItem(menu, wx.ID_ANY, "Next Tab\tCtrl+Tab", "Swap Tabs")
        self.frame.Bind(wx.EVT_MENU, self.forward_tabs, item)
        menu.Append(item)
        item = wx.MenuItem(menu, wx.ID_ANY, "Previous Tab\tCtrl+Shift+Tab", "Swap Tabs")
        self.frame.Bind(wx.EVT_MENU, self.back_tabs, item)
        menu.Append(item)
        self.frame.mainmenu.Insert(2, menu, '&Chat')

    def forward_tabs(self, evt):
        self.parent.AdvanceSelection()

    def back_tabs(self, evt):
        self.parent.AdvanceSelection(False)

    # This subroutine builds the controls for the chat frame
    #
    # !self : instance of self
    def build_ctrls(self):
        self.chatwnd = ChatDisplay(self,-1)
        wx.CallAfter(self.chatwnd.SetPage, self.chatwnd.Header())
        self.chattxt = wx.TextCtrl(self, -1, "", style=wx.TE_PROCESS_ENTER | wx.TE_PROCESS_TAB)
        self.build_bar()
        self.basesizer = wx.BoxSizer(wx.VERTICAL)
        self.basesizer.Add( self.chatwnd,1,wx.EXPAND )
        self.basesizer.Add( self.toolbar_sizer, 0, wx.EXPAND )
        self.basesizer.Add( self.chattxt, 0, wx.EXPAND )
        self.SetSizer(self.basesizer)
        self.SetAutoLayout(True)
        self.Fit()
        #events
        self.Bind(wx.EVT_TOOL, self.onDieRoll, id=DICE_D4)
        self.Bind(wx.EVT_TOOL, self.onDieRoll, id=DICE_D6)
        self.Bind(wx.EVT_TOOL, self.onDieRoll, id=DICE_D8)
        self.Bind(wx.EVT_TOOL, self.onDieRoll, id=DICE_D10)
        self.Bind(wx.EVT_TOOL, self.onDieRoll, id=DICE_D12)
        self.Bind(wx.EVT_TOOL, self.onDieRoll, id=DICE_D20)
        self.Bind(wx.EVT_TOOL, self.onDieRoll, id=DICE_D100)
        self.Bind(wx.EVT_TOOL, self.on_text_format, id=FORMAT_BOLD)
        self.Bind(wx.EVT_TOOL, self.on_text_format, id=FORMAT_ITALIC)
        self.Bind(wx.EVT_TOOL, self.on_text_format, id=FORMAT_UNDERLINE)
        self.Bind(wx.EVT_TOOL, self.on_text_color, id=FORMAT_COLOR)
        self.Bind(wx.EVT_TOOL, self.on_chat_save, id=SAVE_CHAT)
        self.chattxt.Bind(wx.EVT_MOUSEWHEEL, self.chatwnd.mouse_wheel)
        self.chattxt.Bind(wx.EVT_CHAR, self.on_text_char)

    def build_bar(self):
        self.toolbar_sizer = wx.BoxSizer(wx.HORIZONTAL)

        self.toolbar = ui.ToolBar(self)

        # Dice tools.
        self.dice_num_spin = wx.SpinCtrl(self.toolbar, min=1, max=99, initial=1, size=(-1, 26))
        self.dice_num_spin.SetToolTip(wx.ToolTip("Number of dice"))
        self.toolbar.AddControl(self.dice_num_spin)

        self.toolbar.AddTool(DICE_D4, "d4",
                             bitmap=orpg.tools.bitmap.create_from_file("tool_d4.png"),
                             shortHelp="Roll d4")
        self.toolbar.AddTool(DICE_D6, "d6",
                             bitmap=orpg.tools.bitmap.create_from_file("tool_d6.png"),
                             shortHelp="Roll d6")
        self.toolbar.AddTool(DICE_D8, "d8",
                             bitmap=orpg.tools.bitmap.create_from_file("tool_d8.png"),
                             shortHelp="Roll d8")
        self.toolbar.AddTool(DICE_D10, "d10",
                             bitmap=orpg.tools.bitmap.create_from_file("tool_d10.png"),
                             shortHelp="Roll d10")
        self.toolbar.AddTool(DICE_D12, "d12",
                             bitmap=orpg.tools.bitmap.create_from_file("tool_d12.png"),
                             shortHelp="Roll d12")
        self.toolbar.AddTool(DICE_D20, "d20",
                             bitmap=orpg.tools.bitmap.create_from_file("tool_d20.png"),
                             shortHelp="Roll d20")
        self.toolbar.AddTool(DICE_D100, "d100",
                             bitmap=orpg.tools.bitmap.create_from_file("tool_d100.png"),
                             shortHelp="Roll d100")

        self.dice_mod_spin = wx.SpinCtrl(self.toolbar, min=-99, max=99, initial=0, size=(-1, 26))
        self.dice_mod_spin.SetToolTip(wx.ToolTip("Dice roll modifier"))
        self.toolbar.AddControl(self.dice_mod_spin)

        # Format tools.
        self.toolbar.AddTool(FORMAT_BOLD, "Bold",
                             bitmap=orpg.tools.bitmap.create_from_file("tool_bold.png"),
                             shortHelp="Bold text")
        self.toolbar.AddTool(FORMAT_ITALIC, "Italic",
                             bitmap=orpg.tools.bitmap.create_from_file("tool_italic.png"),
                             shortHelp="Italic text")
        self.toolbar.AddTool(FORMAT_BOLD, "Underline",
                             bitmap=orpg.tools.bitmap.create_from_file("tool_underline.png"),
                             shortHelp="Underline text")
        self.color_icon = orpg.tools.bitmap.ColorIcon("tool_color.png")
        self.toolbar.AddTool(FORMAT_COLOR, "Text color",
                             self.color_icon.bitmap(self.mytextcolor.value),
                             shortHelp="Text color")

        # Other tools.
        self.toolbar.AddTool(SAVE_CHAT, "Save chat",
                             orpg.tools.bitmap.create_from_file("tool_save.png"),
                             shortHelp="Save chat text")

        self.toolbar.Realize()
        self.toolbar_sizer.Add((3, 0))
        self.toolbar_sizer.Add( self.toolbar, 0, wx.EXPAND)

    def on_color_player(self, setting):
        self.toolbar.SetToolNormalBitmap(FORMAT_COLOR,
                                         self.color_icon.bitmap(setting.value))

    def on_text_char(self, event):
        self.sendTyping(True)
        event.Skip()

    def sendTyping(self, typing):
        if typing:
            # (Re)start the idle timer.
            self.parent.chat_timer.Start(5000, oneShot=wx.TIMER_ONE_SHOT)
        else:
            self.parent.chat_timer.Stop()
        self.session.player_is_typing(typing)

    def typingTimerFunc(self, event):
        self.session.player_is_typing(False)

    # This subroutine will insert text into the chat window
    #
    # !self : instance of self
    # !txt : text to be inserted into the chat window
    def set_chat_text(self, txt):
        self.chattxt.SetValue(txt)
        self.chattxt.SetFocus()
        self.chattxt.SetInsertionPointEnd()

    def get_chat_text(self):
        return self.chattxt.GetValue()

    # This subroutine sets the focus to the chat window
    def set_chat_text_focus(self, event):
        wx.CallAfter(self.chattxt.SetFocus)

    # This subrtouine grabs the user input and make the special keys and
    # modifiers work.
    #
    # !self : instance of self
    # !event :
    #
    # Note:  self.chattxt now handles it's own Key events.  It does, however still
    #        call it's parent's (self) OnChar to handle "default" behavior.
    def on_panel_char(self, event):
        s = self.chattxt.GetValue()
        #self.histlen = len(self.history) - 1

        ## RETURN KEY (no matter if there is text in chattxt)
        #  This section is run even if there is nothing in the chattxt (as opposed to the next wx.WXK_RETURN handler
        if event.GetKeyCode() == wx.WXK_RETURN:
            self.sendTyping(False)

        macroText=""
        macro_keys = [wx.WXK_F1, wx.WXK_F2, wx.WXK_F3, wx.WXK_F4,
                      wx.WXK_F5, wx.WXK_F6, wx.WXK_F7, wx.WXK_F8,
                      wx.WXK_F9, wx.WXK_F10, wx.WXK_F11, wx.WXK_F12]
        try:
            idx = macro_keys.index(event.GetKeyCode())
            macroText = self.macros[idx].value
        except ValueError:
            pass
        # Replace the existing typed text as needed and make sure the status doesn't change back.
        if len(macroText):
            self.sendTyping(False)
            s = macroText

        ## RETURN KEY (and not text in control)
        if (event.GetKeyCode() == wx.WXK_RETURN and len(s)) or len(macroText):
            self.histidx = -1
            self.temptext = ""
            self.history = [s] + self.history#prepended instead of appended now, so higher index = greater age
            if not len(macroText):
                self.chattxt.SetValue("")
            if s[0] != "/": ## it's not a slash command
                s = self.ParsePost(s, True, True, self.frame.tree.active_node)
            else:
                self.chat_cmds.docmd(s) # emote is in chatutils.py

        ## UP KEY
        elif event.GetKeyCode() == wx.WXK_UP:
            if self.histidx < len(self.history)-1:
                #text that's not in history but also hasn't been sent to chat gets stored in self.temptext
                #this way if someone presses the up key, they don't lose their current message permanently
                #(unless they also press enter at the time)
                if self.histidx == -1:
                    self.temptext = self.chattxt.GetValue()
                self.histidx += 1
                self.chattxt.SetValue(self.history[self.histidx])
                self.chattxt.SetInsertionPointEnd()
            else:
                self.histidx = len(self.history) -1#in case it got too high somehow, this should fix it
                #self.InfoPost("**Going up? I don't think so.**")
            #print self.histidx, "in",self.history

        ## DOWN KEY
        elif event.GetKeyCode() == wx.WXK_DOWN:
            #histidx of -1 indicates currently viewing text that's not in self.history
            if self.histidx > -1:
                self.histidx -= 1
                if self.histidx == -1: #remember, it just decreased
                    self.chattxt.SetValue(self.temptext)
                else:
                    self.chattxt.SetValue(self.history[self.histidx])
                self.chattxt.SetInsertionPointEnd()
            else:
                self.histidx = -1 #just in case it somehow got below -1, this should fix it
                #self.InfoPost("**Going down? I don't think so.**")
            #print self.histidx, "in",self.history

        ## TAB KEY
        elif  event.GetKeyCode() == wx.WXK_TAB:
            if s !="":
                # Try and complete the partial nick.
                nicks = [player.name for player in self.session.get_players()]
                completed_nick = tab_complete(s, nicks)
                if completed_nick:
                    self.chattxt.SetValue(completed_nick)
                    self.chattxt.SetInsertionPointEnd()

        ## PAGE UP
        elif event.GetKeyCode() == wx.WXK_PAGEUP:
            self.chatwnd.ScrollPages(-1)

        ## PAGE DOWN
        elif event.GetKeyCode() == wx.WXK_PAGEDOWN:
            self.chatwnd.ScrollPages(1)

        ## END
        elif event.GetKeyCode() == wx.WXK_END:
            event.Skip()

        ## NOTHING
        else:
            event.Skip()

    def onDieRoll(self, evt):
        """Roll the dice based on the button pressed and the die modifiers entered, if any."""
        self.chattxt.SetFocus()
        numDie = self.dice_num_spin.GetValue()
        dice = evt.GetId()
        dieMod = self.dice_mod_spin.GetValue()
        self.ParsePost(f"[{numDie}d{dice}{dieMod:+d}]", 1, 1)

    def on_chat_save(self, evt):
        f = wx.FileDialog(self, "Save Chat Log", self.last_directory.value, "",
                          "HTML (*.html)|*.html", wx.FD_SAVE)
        if f.ShowModal() == wx.ID_OK:
            self.last_directory.value = f.GetDirectory()
            file = open(f.GetPath(), "w")
            file.write(self.ResetPage() + "</body></html>")
            file.close()
        f.Destroy()

    def ResetPage(self):
        buffertext = self.chatwnd.Header() + "\n"
        buffertext += chat_util.strip_body_tags(self.chatwnd.StripHeader()).replace("<br>", "<br />").replace('</html>', '').replace("<br />", "<br />\n").replace("\n\n", '')
        return buffertext

    # This subroutine sets the color of selected text, or base text color if
    # nothing is selected
    def on_text_color(self, event):
        data = wx.ColourData()
        data.SetChooseFull(True)
        with wx.ColourDialog(self, data) as dlg:
            if dlg.ShowModal() == wx.ID_OK:
                color = dlg.GetColourData().GetColour()
                (beg,end) = self.chattxt.GetSelection()
                if beg != end:
                    txt = self.chattxt.GetValue()
                    txt = txt[:beg]+self.colorize(color, txt[beg:end]) + txt[end:]
                    self.chattxt.SetValue(txt)
                    self.chattxt.SetInsertionPointEnd()
                else:
                    self.mytextcolor.value = color
                    self.toolbar.SetToolNormalBitmap(FORMAT_COLOR,
                                                 self.color_icon.bitmap(color))

    # This subroutine take a color and a text string and formats it into html.
    #
    # !self : instance of self
    # !color : color for the text to be set
    # !text : text string to be included in the html.
    def colorize(self, color, text):
        """Puts font tags of 'color' around 'text' value, and returns the string"""
        html_color = color.GetAsString(wx.C2S_HTML_SYNTAX)
        return f"<font color='{html_color}'>{text}</font>"

    # This subroutine takes and event and inserts text with the basic format
    # tags included.
    #
    # !self : instance of self
    # !event :
    def on_text_format(self, event):
        tool = event.GetId()
        txt = self.chattxt.GetValue()
        (beg,end) = self.chattxt.GetSelection()
        if beg != end:
            sel_txt = txt[beg:end]
        else:
            sel_txt = txt
        if tool == FORMAT_BOLD:
            sel_txt = "<b>" + sel_txt + "</b>"
        elif tool == FORMAT_ITALIC:
            sel_txt = "<i>" + sel_txt + "</i>"
        elif tool == FORMAT_UNDERLINE:
            sel_txt = "<u>" + sel_txt + "</u>"
        if beg != end:
            txt = txt[:beg] + sel_txt + txt[end:]
        else:
            txt = sel_txt
        self.chattxt.SetValue(txt)
        self.chattxt.SetInsertionPointEnd()
        self.chattxt.SetFocus()

    # This subroutine will change the dimension of the window
    #
    # !self : instance of self
    # !event :
    def OnSize(self, event=None):
        self.chatwnd.scroll_down()
        event.Skip()

    def open_whisper_tab(self, player_id):
        self.parent.open_whisper_tab(player_id)

    ###### message helpers ######
    def PurgeChat(self):
        self.chatwnd.SetPage(self.chatwnd.Header())

    def system_message(self, text):
        self.send_chat_message(text,chat_msg.SYSTEM_MESSAGE)
        self.SystemPost(text)

    def info_message(self, text):
        self.send_chat_message(text,chat_msg.INFO_MESSAGE)
        self.InfoPost(text)

    def get_gms(self):
        gms = []
        if self.session.group_id != "0":
            for player in self.session.players.values():
                if player.role == ROLE_GM:
                    gms.append(player.id)
        return gms

    def GetName(self):
        return self.session.player.name

    def emote_message(self, text):
        text = self.NormalizeParse(text)
        text = self.colorize(self.emotecolor.value, text)

        if self.type == MAIN_TAB and self.sendtarget == 'all':
            self.send_chat_message(text,chat_msg.EMOTE_MESSAGE)
        elif self.type == MAIN_TAB and self.sendtarget == "gm":
            msg_type = chat_msg.WHISPER_EMOTE_MESSAGE
            the_gms = self.get_gms()
            for each_gm in the_gms:
                self.send_chat_message(text,chat_msg.WHISPER_EMOTE_MESSAGE, str(each_gm))
        elif self.type == GROUP_TAB and self.sendtarget in WG_LIST:
            for pid in WG_LIST[self.sendtarget]:
                self.send_chat_message(text,chat_msg.WHISPER_EMOTE_MESSAGE, str(pid))
        elif self.type == WHISPER_TAB:
            self.send_chat_message(text,chat_msg.WHISPER_EMOTE_MESSAGE, str(self.sendtarget))
        elif self.type == NULL_TAB:
            pass
        text = "** " + self.GetName() + " " + text + " **"
        self.EmotePost(text)

    def whisper_to_players(self, text, player_ids):
        text = self.NormalizeParse(text)
        player_names = ""
        # post to our chat before we colorize
        for m in player_ids:
            id = m.strip()
            if self.session.is_valid_id(id):
                returned_name = self.session.get_player_info(id).name
                player_names += returned_name
                player_names += ", "
            else:
                player_names += " Unknown!"
                player_names += ", "
        comma = ","
        comma.join(player_ids)
        if (self.sendtarget == "all"):
            self.InfoPost("<i>whispering to "+ player_names + " " + text + "</i> ")
        # colorize and loop, sending whisper messages to all valid clients
        text = self.colorize(self.mytextcolor.value, text)
        for id in player_ids:
            id = id.strip()
            if self.session.is_valid_id(id):
                self.send_chat_message(text,chat_msg.WHISPER_MESSAGE,id)
            else:
                self.InfoPost(id + " Unknown!")

    def send_chat_message(self, text, type=chat_msg.CHAT_MESSAGE, player_id="all"):
        send = 1
        msg = chat_msg.chat_msg()
        msg.set_text(text)
        msg.set_type(type)
        msg.set_alias(self.GetName())
        if send:
            self.session.send(msg.toxml(),player_id)
        del msg

    #### incoming chat message handler #####
    def post_incoming_msg(self, msg, player):
        # pull data
        type = msg.get_type()
        text = msg.get_text()
        if player:
            display_name = player.name
        else:
            display_name = "Server Administrator"

        # act on the type of messsage
        if (type == chat_msg.CHAT_MESSAGE):
            text = "<b>" + display_name + "</b>: " + text
            self.Post(text)
            self.parent.newMsg(0)
        elif type == chat_msg.WHISPER_MESSAGE or type == chat_msg.WHISPER_EMOTE_MESSAGE:
            displaypanel = self
            whisperingstring = " (whispering): "
            panelexists = 0
            use_whisper_tab = self.parent.use_whisper_tab.value
            use_gm_whisper_tab = self.parent.use_gm_whisper_tab.value
            use_group_whisper_tab = self.parent.use_group_whisper_tab.value
            name = '<i><b>' + display_name + '</b>: '
            text += '</i>'
            panelexists = 0
            created = 0
            try:
                if use_gm_whisper_tab:
                    the_gms = self.get_gms()
                    #Check if whisper if from a GM
                    if player.id in the_gms:
                        msg = name + ' (GM Whisper:) ' + text
                        if type == chat_msg.WHISPER_MESSAGE:
                            self.parent.GMChatPanel.Post(msg)
                        else:
                            self.parent.GMChatPanel.EmotePost("**" + msg + "**")
                        idx = self.parent.get_tab_index(self.parent.GMChatPanel)
                        self.parent.newMsg(idx)
                        panelexists = 1
                #See if message if from someone in our groups or for a whisper tab we already have
                if not panelexists and use_group_whisper_tab:
                    for panel in self.parent.group_tabs:
                        if panel.sendtarget in WG_LIST and int(player.id) in WG_LIST[panel.sendtarget]:
                            msg = name + text
                            if type == chat_msg.WHISPER_MESSAGE:
                                panel.Post(msg)
                            else:
                                panel.EmotePost("**" + msg + "**")
                            idx = self.parent.get_tab_index(panel)
                            self.parent.newMsg(idx)
                            panelexists = 1
                            break
                if not panelexists and use_whisper_tab:
                    for panel in self.parent.whisper_tabs:
                        #check for whisper tabs as well, to save the number of loops
                        if panel.sendtarget == player.id:
                            msg = name + whisperingstring + text
                            if type == chat_msg.WHISPER_MESSAGE:
                                panel.Post(msg)
                            else:
                                panel.EmotePost("**" + msg + "**")
                            idx = self.parent.get_tab_index(panel)
                            self.parent.newMsg(idx)
                            panelexists = 1
                            break
                #We did not fint the tab
                if not panelexists:
                    #If we get here the tab was not found
                    if use_group_whisper_tab:
                        for group in list(WG_LIST.keys()):
                            #Check if this group has the player in it
                            if int(player.id) in WG_LIST[group]:
                                #Yup, post message. Player may be in more then 1 group so continue as well
                                panel = self.parent.create_group_tab(group)
                                msg = name + text
                                if type == chat_msg.WHISPER_MESSAGE:
                                    wx.CallAfter(panel.Post, msg)
                                else:
                                    wx.CallAfter(panel.EmotePost, "**" + msg + "**")
                                created = 1
                    #Check to see if we should create a whisper tab
                    if not created and use_whisper_tab:
                        panel = self.parent.create_whisper_tab(player.id)
                        msg = name + whisperingstring + text
                        if type == chat_msg.WHISPER_MESSAGE:
                            wx.CallAfter(panel.Post, msg)
                        else:
                            wx.CallAfter(panel.EmotePost, "**" + msg + "**")
                        created = 1
                    #Final check
                    if not created:
                        #No tabs to create, just send the message to the main chat tab
                        msg = name + whisperingstring + text
                        if type == chat_msg.WHISPER_MESSAGE:
                            self.parent.MainChatPanel.Post(msg)
                        else:
                            self.parent.MainChatPanel.EmotePost("**" + msg + "**")
                        self.parent.newMsg(0)
            except Exception as e:
                logger.exception("Error posting whisper message")
        elif (type == chat_msg.EMOTE_MESSAGE):
            text = "** " + display_name + " " + text + " **"
            self.EmotePost(text)
            self.parent.newMsg(0)
        elif (type == chat_msg.INFO_MESSAGE):
            text = "<b>" + display_name + "</b>: " + text
            self.InfoPost(text)
            self.parent.newMsg(0)
        elif (type == chat_msg.SYSTEM_MESSAGE):
            text = "<b>" + display_name + "</b>: " + text
            self.SystemPost(text)
            self.parent.newMsg(0)

    def InfoPost(self, s):
        self.Post(self.colorize(self.infocolor.value, s))

    def SystemPost(self, s):
        self.Post(self.colorize(self.syscolor.value, s))

    def EmotePost(self, s):
        self.Post(self.colorize(self.emotecolor.value, s))

    #### Standard Post method #####
    def Post(self, s="", send=False, myself=False):
        s = chat_util.simple_html_repair(s)
        s = chat_util.strip_script_tags(s)
        s = chat_util.strip_li_tags(s)
        s = chat_util.strip_body_tags(s)
        s = chat_util.strip_misalignment_tags(s)
        newline = ''
        if myself:
            name = "<b>" + self.GetName() + "</b>: "
            s = self.colorize(self.mytextcolor.value, s)
        else:
            name = ""
        # Only add lines with visible text.
        lineHasText = html_to_text(s).replace(" ","").strip() != ""
        if lineHasText:
            if myself:
                s2 = s
                if s2 != "":
                    #Italici the messages from tabbed whispers
                    if self.type == WHISPER_TAB or self.type == GROUP_TAB or self.sendtarget == 'gm':
                        s2 = s2 + '</i>'
                        name = '<i>' + name
                        if self.type == WHISPER_TAB:
                            name += " (whispering): "
                        elif self.sendtarget == 'gm':
                            name += " (whispering to GM) "
                    newline = name +  s2 + "<br />"
                    log(name + s2)
            else:
                newline = name +  s + "<br />"
                log(name + s)
        else:
            send = False

        self.append_to_page(newline)

        if send:
            if self.type == MAIN_TAB and self.sendtarget == 'all':
                self.send_chat_message(s)
            elif self.type == MAIN_TAB and self.sendtarget == "gm":
                the_gms = self.get_gms()
                self.whisper_to_players(s, the_gms)
            elif self.type == GROUP_TAB and self.sendtarget in WG_LIST:
                members = []
                for pid in WG_LIST[self.sendtarget]:
                    members.append(str(WG_LIST[self.sendtarget][pid]))
                self.whisper_to_players(s, members)
            elif self.type == WHISPER_TAB:
                self.whisper_to_players(s, [self.sendtarget])
            elif self.type == NULL_TAB:
                pass
            else:
                self.InfoPost("Failed to send message, unknown send type for this tab")
        self.parsed=0

    ####  Post with parsing dice ####
    def ParsePost(self, s, send=False, myself=False, symtab=None):
        s = self.NormalizeParse(s, symtab)
        self.Post(s,send,myself)

    def NormalizeParse(self, s, symtab=None):
        if self.parsed == 0:
            s = self.ParseDice(s, symtab)
            self.parsed = 1
        return s

    def ParseDice(self, s, symtab):
        """Parses player input for embedded dice rolls"""
        try:
            return parse_all_dice_rolls(symtab, s)
        except dice_roll_error as e:
            self.InfoPost("Dice error: " + e.str)
            return ""

    def append_to_page(self, text):
        vy = self.chatwnd.save_scroll()
        self.chatwnd.AppendToPage(text)
        self.chatwnd.restore_scroll(vy)
