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
# File: mapper/min_dialogs.py
# Author: Chris Davis
# Maintainer:
# Version:
#   $Id: min_dialogs.py,v 1.27 2006/11/13 02:23:16 digitalxero Exp $
#
# Description: This file contains some of the basic definitions for the chat
# utilities in the orpg project.
from orpg.mapper.whiteboard import *

MIN_LABEL = wx.NewId()
MIN_HEADING = wx.NewId()
MIN_FACE = wx.NewId()
MIN_HIDE = wx.NewId()
MIN_LOCK = wx.NewId()
MIN_ALIGN = wx.NewId()
wxID_MIN_WIDTH = wx.NewId()
wxID_MIN_HEIGHT = wx.NewId()
wxID_MIN_SCALING = wx.NewId()

class min_edit_panel(wx.Panel):
    def __init__(self, parent, min):
        wx.Panel.__init__(self, parent, -1)
        self.min = min
        sizer = wx.StaticBoxSizer(wx.StaticBox(self,-1,"Miniature"), wx.VERTICAL)
        sizerSize = wx.BoxSizer(wx.HORIZONTAL)
        hSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.label = wx.TextCtrl(self, MIN_LABEL, min.label)
        sizer.Add(wx.StaticText(self, -1, "Label:"), 0, wx.EXPAND)
        sizer.Add(self.label, 0, wx.EXPAND)
        sizer.Add(wx.Size(10,10))

        self.heading = wx.RadioBox(self, MIN_HEADING, "Heading", choices=["None","N","NE","E","SE","S","SW","W","NW"],majorDimension=5,style=wx.RA_SPECIFY_COLS)
        self.heading.SetSelection(min.heading)
        self.face = wx.RadioBox(self, MIN_FACE, "Facing", choices=["None","N","NE","E","SE","S","SW","W","NW"],majorDimension=5,style=wx.RA_SPECIFY_COLS)
        self.face.SetSelection(min.face)
        self.locked = wx.CheckBox(self, MIN_LOCK, " Lock")
        self.locked.SetValue(min.locked)
        self.hide = wx.CheckBox(self, MIN_HIDE, " Hide")
        self.hide.SetValue(min.hide)
        sizer.Add(self.heading, 0, wx.EXPAND)
        sizer.Add(wx.Size(10,10))
        sizer.Add(self.face, 0, wx.EXPAND)
        sizer.Add(wx.Size(10,10))

        #
        #image resizing
        #
        self.min_width_old_value = str(self.min.bmp.GetWidth())
        self.min_width = wx.TextCtrl(self, wxID_MIN_WIDTH, self.min_width_old_value)
        sizerSize.Add(wx.StaticText(self, -1, "Width: "), 0, wx.ALIGN_CENTER)
        sizerSize.Add(self.min_width, 1, wx.EXPAND)
        sizerSize.Add(wx.Size(20, 25))

        #TODO:keep in mind that self.min is a local copy???
        self.min_height_old_value = str(self.min.bmp.GetHeight())
        self.min_height = wx.TextCtrl(self, wxID_MIN_HEIGHT, self.min_height_old_value)
        sizerSize.Add(wx.StaticText(self, -1, "Height: "),0,wx.ALIGN_CENTER)
        sizerSize.Add(self.min_height, 1, wx.EXPAND)
        self.min_scaling = wx.CheckBox(self, wxID_MIN_SCALING, "Lock scaling")
        self.min_scaling.SetValue(True)
        sizerSize.Add(self.min_scaling, 1, wx.EXPAND)

        sizer.Add(sizerSize, 0, wx.EXPAND)
        sizer.Add(wx.Size(10, 10))

        # Now, add the last items on in their own sizer
        hSizer.Add(self.locked, 0, wx.EXPAND)
        hSizer.Add(wx.Size(10,10))
        hSizer.Add(self.hide, 0, wx.EXPAND)

        # Add the hSizer to the main sizer
        sizer.Add( hSizer )

        self.sizer = sizer
        self.SetSizer(self.sizer)
        self.SetAutoLayout(True)
        self.Fit()

        #self.Bind(wx.EVT_SIZE, self.on_size)
        self.Bind(wx.EVT_TEXT, self.on_text, id=MIN_LABEL)
        self.Bind(wx.EVT_TEXT, self.on_scaling, id=wxID_MIN_WIDTH)
        self.Bind(wx.EVT_TEXT, self.on_scaling, id=wxID_MIN_HEIGHT)
        self.Bind(wx.EVT_RADIOBOX, self.on_radio_box, id=MIN_HEADING)
        self.Bind(wx.EVT_RADIOBOX, self.on_radio_box, id=MIN_FACE)


    def on_scaling(self, evt):
        if self.min_scaling.GetValue() == False:
            return
        elif self.min_width.GetValue() and wxID_MIN_WIDTH == evt.GetId() and self.min_width.GetInsertionPoint():
            self.min_height.SetValue ( str(int((float(self.min_width.GetValue()) / float(self.min_width_old_value)) * float(self.min_height_old_value))) )
        elif self.min_height.GetValue() and wxID_MIN_HEIGHT == evt.GetId() and self.min_height.GetInsertionPoint():
            self.min_width.SetValue ( str(int((float(self.min_height.GetValue()) / float(self.min_height_old_value)) * float(self.min_width_old_value))) )

    def update_min(self):
        self.min.set_min_props(self.heading.GetSelection(),
                               self.face.GetSelection(),
                               self.label.GetValue(),
                               self.locked.GetValue(),
                               self.hide.GetValue(),
                               self.min_width.GetValue(),
                               self.min_height.GetValue())


    def on_radio_box(self,evt):
        id = evt.GetId()
        index = evt.GetInt()

    def on_text(self,evt):
        id = evt.GetId()

    def on_size(self,evt):
        s = self.GetClientSize()
        self.sizer.SetDimension(20,20,s[0]-40,s[1]-40)
        self.outline.SetDimensions(5,5,s[0]-10,s[1]-10)

class min_edit_dialog(wx.Dialog):
    def __init__(self,parent,min):
#520,265
        wx.Dialog.__init__(self,parent,-1,"Miniature",wx.DefaultPosition,wx.Size(520,350))
        (w,h) = self.GetClientSize()

        mastersizer = wx.BoxSizer(wx.VERTICAL)

        editor = min_edit_panel(self,min)
        #editor.SetDimensions(0,0,w,h-25)
        self.editor = editor
        mastersizer.Add(editor, 1, wx.EXPAND)
        mastersizer.Add(wx.Size(10,10))

        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(wx.Button(self, wx.ID_OK, "OK"), 1, wx.EXPAND)
        sizer.Add(wx.Size(10,10))
        sizer.Add(wx.Button(self, wx.ID_CANCEL, "Cancel"), 1, wx.EXPAND)
        #sizer.SetDimension(0,h-25,w,25)
        mastersizer.Add(sizer, 0, wx.EXPAND)

        self.SetSizer(mastersizer)
        self.SetAutoLayout(True)
        self.Fit()
        self.Bind(wx.EVT_BUTTON, self.on_ok, id=wx.ID_OK)

    def on_ok(self,evt):
        self.editor.update_min()
        self.EndModal(wx.ID_OK)
