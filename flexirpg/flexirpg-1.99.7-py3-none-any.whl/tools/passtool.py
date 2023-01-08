# FlexiRPG -- password manager.
#
# Copyright 2020 David Vrabel
# Copyright (C) 2000-2001 The OpenRPG Project
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.

import wx

#####################
## Password Assistant
#####################
class PassSet:
    "set of passwords for a given room id on a server"
    def __init__(self):
        #room admin password (aka boot password)
        self.admin = None

        #room password
        self.room = None


class PassTool:
    """Password Management System

    This stores entered passwords so they don't need to be typed
    again.

    """
    def __init__(self):
        #server admin password
        self.server = None
        self.groups = {}

    def DumpPasswords(self):
        "Debugging Routine"
        print("Password Manager Dump\nServer: \""+self.server+"\"")
        for c in self.groups:
            ad = self.groups[c].admin
            rm = self.groups[c].room
            print( " #"+str(c)+"  R:\""+str(rm)+"\"  A:\""+str(ad)+"\"")

    def ClearPassword(self, type="ALL", groupid=None):
        if type == "ALL":
            self.server = None
            self.groups = {}
        elif type == "ALL":
            self.groups[groupid].admin = None
            self.groups[groupid].room = None
        elif type == "server":
            self.server = None
        elif type == "admin":
            self.groups[groupid].admin = None
        elif type == "room":
            self.groups[groupid].room = None

    def QueryUser(self,info_string):
        pwd_dialog = wx.TextEntryDialog(None,info_string,"Password Required")
        if pwd_dialog.ShowModal() == wx.ID_OK:
            pwd_dialog.Destroy()
            return str(pwd_dialog.GetValue())
        else:
            pwd_dialog.Destroy()
            return None

    def CheckGroupData(self, id):
        try: #see if group exists
            group=self.groups[id]
        except: #group doesn't exist... create it
            self.groups[id] = PassSet()

    def RemoveGroupData(self, id):
        try:
            #if PassSet exists for group remove it.
            del self.groups[id]
        except KeyError:
            pass

    def GetSilentPassword( self, type="server", groupid = 0):
        self.CheckGroupData( groupid )
        if type == "admin":
            if self.groups[groupid].admin != None: return str(self.groups[groupid].admin)
            else: return None
        elif type == "room":
            if self.groups[groupid].room != None: return str(self.groups[groupid].room)
            else: return None
        elif type == "server":
            if self.server != None: return str(self.server)
            else: return None

    def GetPassword(self, type="room", groupid=0):
        self.CheckGroupData( groupid )
        if type == "admin":
            return self.AdminPass(groupid)
        elif type == "room":
            return self.RoomPass(groupid)
        elif type == "server":
            return self.ServerPass()
        else:
            querystring = f"Enter password for \"{type}\""
            return self.QueryUser(querystring)

    def AdminPass( self, groupid ):
        self.CheckGroupData( groupid )
        if self.groups[groupid].admin != None:
            return self.groups[groupid].admin
        else:
            password = self.QueryUser("Please enter the Room Administrator Password:")
            if password is not None:
                self.groups[groupid].admin = password
            return password

    def RoomPass( self, groupid):
        self.CheckGroupData(groupid)
        if self.groups[ groupid ].room is not None:
            return self.groups[groupid].room
        else:
            password =  self.QueryUser("Please enter the Room Password:")
            if password is not None:
                self.groups[groupid].room = password
            return password

    def ServerPass( self ):
        if self.server is not None:
            return str(self.server)
        else:
            self.server = self.QueryUser("Please enter the Server Administrator password:")
            return str(self.server)
