# FlexiRPG -- Chat text buffer display window.
#
# Copyright 2020 David Vrabel
# Copyright (C) 2000-2001 The OpenRPG Project
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.

import webbrowser

import wx
import wx.html

from orpg.config import Settings
import orpg.chat.dice_tag # For <dice> tag handler.


class ChatDisplay(wx.html.HtmlWindow):
    """A HTML window for displaying the chat buffer."""

    chat_font = Settings.define("chat.font", "")
    chat_font_size = Settings.define("chat.font_size", 0)

    def __init__(self, parent, id):
        wx.html.HtmlWindow.__init__(self, parent, id,
                                    style=wx.SUNKEN_BORDER
                                    | wx.html.HW_SCROLLBAR_AUTO
                                    | wx.NO_FULL_REPAINT_ON_RESIZE)
        self.parent = parent
        self.frame = parent.frame
        self.build_menu()
        self.Bind(wx.EVT_RIGHT_DOWN, self.onPopup)
        self.Bind(wx.EVT_SCROLLWIN, self.on_scrollwin)
        self.Bind(wx.html.EVT_HTML_LINK_CLICKED, self.on_link_clicked)

        font_size = self.chat_font_size.value
        if font_size == 0:
            font_size = -1
        self.SetStandardFonts(font_size, self.chat_font.value)

        self.auto_scroll = True

    def onPopup(self, evt):
        self.PopupMenu(self.menu)

    def on_scrollwin(self, evt):
        # FIXME: should use EVT_SCROLLWIN_CHANGED but it's not
        # available until 2.9.
        wx.CallAfter(self.done_scrolling)
        evt.Skip()

    def on_link_clicked(self, evt):
        href = evt.GetLinkInfo().GetHref()
        s = href.split(':', 2)
        if s[0] == "dice":
            self.frame.tree.set_roll_value(int(s[1]))
        else:
            webbrowser.get().open(href)

    def done_scrolling(self):
        (vx, vy) = self.GetViewStart()
        page_size = self.GetScrollPageSize(wx.VERTICAL)
        max_range = self.GetScrollRange(wx.VERTICAL)

        # Enable auto-scrolling if the window is scrolled to the end
        # or scroll bars aren't present.
        self.auto_scroll = vy + page_size >= max_range or page_size == 0

    def build_menu(self):
        self.menu = wx.Menu()
        item = wx.MenuItem(self.menu, wx.ID_COPY, "Copy", "Copy")
        self.menu.Append(item)

    def save_scroll(self):
        (vx, vy) = self.GetViewStart()
        return vy

    def restore_scroll(self, vy):
        #
        # Bug workaround: If the window transitioned to needing
        # scrollbars then calling self.Scroll() does not correctly
        # scroll and a wx.CallAfter is required.  However, defering
        # the scroll sometimes gives a visual glitch (the window jumps
        # briefy to the top).  So, only defer the scroll when
        # absolutely necessary.
        #
        defer_scroll = vy <= 1

        if self.auto_scroll or vy < 0:
            max_range = self.GetScrollRange(wx.VERTICAL)
            page_size = self.GetScrollPageSize(wx.VERTICAL)
            vy = max_range - page_size

        if defer_scroll:
            wx.CallAfter(self.Scroll, -1, vy)
        else:
            self.Scroll(-1, vy)

    def scroll_down(self):
        self.restore_scroll(-1)

    def mouse_wheel(self, event):
        amt = event.GetWheelRotation()
        units = amt/(-(event.GetWheelDelta()))
        self.ScrollLines(units*3)

    def Header(self):
        bgcolor = self.parent.bgcolor.value.GetAsString(wx.C2S_HTML_SYNTAX)
        textcolor = self.parent.textcolor.value.GetAsString(wx.C2S_HTML_SYNTAX)
        return f"<html><body bgcolor='{bgcolor}' text='{textcolor}'>"

    def StripHeader(self):
        return self.GetPageSource().replace(self.Header(), '')

    def GetPageSource(self):
        return self.GetParser().GetSource()
