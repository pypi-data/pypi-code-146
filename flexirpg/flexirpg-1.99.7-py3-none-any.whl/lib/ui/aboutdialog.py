# About Dialog
#
# Copyright (C) 2011 David Vrabel
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.

import string
import webbrowser
import wx

class AboutDialog(wx.Dialog):
    """
    About dialog box.

    A dialog for an application's 'about' dialog box.  The descriptive
    text is taken from a HTML file.  The HTML can contain @PRODUCT@
    and @VERSION@ strings which are substituted with the product name
    and version respectively.
    """
    def __init__(self, parent, html_file, product, version):
        wx.Dialog.__init__(self, parent, wx.ID_ANY, "About %s" % (product),
                           style = wx.DEFAULT_DIALOG_STYLE)

        with open(html_file, "r") as about_file:
            about_text = about_file.read()

        about_text = self._substitute_var(about_text, "PRODUCT", product)
        about_text = self._substitute_var(about_text, "VERSION", version)

        # Size the HTML window to its content.
        about_size = wx.Size(400, 0)
        html = self._html_window(about_text, about_size)
        about_size.height = html.GetInternalRepresentation().GetHeight()
        html = self._html_window(about_text, about_size)

        close_btn = wx.Button(self, wx.ID_CANCEL, "Close")
        close_btn.SetDefault()
        close_btn.SetFocus()

        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(html, 1, wx.EXPAND)
        vbox.Add((0,12))
        vbox.Add(close_btn, 0, wx.ALIGN_RIGHT)

        box = wx.BoxSizer(wx.VERTICAL)
        box.Add(vbox, 1, wx.ALL, border=12)
        box.Fit(self)

        self.SetAutoLayout(True)
        self.SetSizer(box)

        self.SetAffirmativeId(wx.ID_CANCEL)
        self.SetEscapeId(wx.ID_CANCEL)

        self.Bind(wx.html.EVT_HTML_LINK_CLICKED, self.on_link_clicked)

    def _substitute_var(self, text, var, val):
        return text.replace(f"@{var}@", val)

    def _html_window(self, text, size):
        html = wx.html.HtmlWindow(self, wx.ID_ANY, size=size,
                                  style=wx.html.HW_SCROLLBAR_NEVER)
        html.SetPage(text)
        html.SetBorders(0)
        return html

    def on_link_clicked(self, evt):
        webbrowser.open(evt.GetLinkInfo().GetHref())

