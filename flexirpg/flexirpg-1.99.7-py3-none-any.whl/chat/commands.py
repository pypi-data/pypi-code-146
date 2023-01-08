# FlexiRPG -- Chat "slash" command handling.
#
# Copyright 2020 David Vrabel
# Copyright (C) 2000-2001 The OpenRPG Project
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.

import time

from orpg.config import Settings
import orpg.player_list

class ChatCommands:
    def __init__(self,chat):
        self.session = chat.session
        self.chat = chat
        self.cmdlist = {}
        self.shortcmdlist = {}
        self.defaultcmds()
        self.defaultcmdalias()
        self.previous_whisper = []

    def _addcommand(self, cmd, function, helpmsg):
        self.cmdlist[cmd] = {}
        self.cmdlist[cmd]['function'] = function
        self.cmdlist[cmd]['help'] = helpmsg

    def _addshortcmd(self, shortcmd, longcmd):
        self.shortcmdlist[shortcmd] = longcmd

    def defaultcmds(self):
        self._addcommand('/help', self.on_help, '- Displays this help message')
        self._addcommand('/me', self.chat.emote_message, ' - Alias for **yourname does something.**')
        self._addcommand('/whisper', self.on_whisper, 'player_id_number, ... = message - Whisper to player(s). Can contain multiple IDs.')
        self._addcommand('/gw', self.on_groupwhisper, 'group_name=message - Type /gw help for more information')
        self._addcommand('/gm', self.on_gmwhisper, 'message - Whispers to all GMs in the room')
        self._addcommand('/name', self.on_name, 'name - Change your name.')
        self._addcommand('/status', self.on_status, 'your_status - Set your online status (afk,away,etc..).')
        self._addcommand('/ping', self.on_ping, '- Ask for a response from the server.')

    def defaultcmdalias(self):
        self._addshortcmd('/?', '/help')
        self._addshortcmd('/he', '/me')
        self._addshortcmd('/she', '/me')
        self._addshortcmd('/w', '/whisper')
        self._addshortcmd('/nick', '/name')

    def docmd(self,text):
        cmd = text.split(None, 1)[0].lower()
        start = len(cmd)
        end = len(text)
        cmdargs = text[start+1:end]

        if cmd in self.cmdlist:
            self.cmdlist[cmd]['function'](cmdargs)
        elif cmd in self.shortcmdlist:
            self.docmd(self.shortcmdlist[cmd] + " " + cmdargs)
        else:
            msg = "Sorry I don't know what %s is!" % (cmd)
            self.chat.InfoPost(msg)

    def on_ping(self, cmdargs):
        ct = time.clock()
        msg = "<ping player='"+self.session.id+"' time='"+str(ct)+"' />"
        self.session.outbox.put(msg)

    def on_name(self, cmdargs):
        if cmdargs == "":
            self.chat.InfoPost("**Incorrect syntax for name.")
        else:
            Settings.lookup("player.name").value = cmdargs
            self.session.set_name(str(cmdargs))

    def on_status(self, cmdargs):
        if cmdargs ==  "":
            self.chat.InfoPost("Incorrect synatx for status.")
        else:
            Settings.lookup("player.status").value = cmdargs
            self.session.set_text_status(cmdargs)

    def on_help(self, cmdargs=""):
        cmds = list(self.cmdlist.keys())
        cmds.sort()
        shortcmds = list(self.shortcmdlist.keys())
        shortcmds.sort()
        msg = '<br /><b>Command Alias List:</b>'
        for shortcmd in shortcmds:
            msg += '<br /><b><font color="#0000CC">%s</font></b> is short for <font color="#000000">%s</font>' % (shortcmd, self.shortcmdlist[shortcmd])
        msg += '<br /><br /><b>Command List:</b>'
        for cmd in cmds:
            msg += '<br /><b><font color="#000000">%s</font></b>' % (cmd)
            for shortcmd in shortcmds:
                if self.shortcmdlist[shortcmd] == cmd:
                    msg += ', <b><font color="#0000CC">%s</font></b>' % (shortcmd)
            msg += ' %s' % (self.cmdlist[cmd]['help'])

        self.chat.InfoPost(msg)

    # This subroutine implements the whisper functionality that enables a user
    # to whisper to another user.
    #
    # !self : instance of self
    # !text : string that is comprised of a list of users and the message to
    #whisper.
    def on_whisper(self, cmdargs):
        delim = cmdargs.find("=")

        if delim < 0:
            if self.previous_whisper:
                player_ids = self.previous_whisper
            else:
                self.chat.InfoPost("**Incorrect syntax for whisper." + str(delim))
                return
        else:
            player_ids = cmdargs[:delim].split(",")
        self.previous_whisper = player_ids
        mesg = cmdargs[delim+1:].strip()
        self.chat.whisper_to_players(mesg,player_ids)

    def on_groupwhisper(self, cmdargs):
        args = cmdargs.split(None,-1)
        delim = cmdargs.find("=")

        if delim > 0:
            group_ids = cmdargs[:delim].split(",")
        elif args[0] == "add":
            if not args[2] in orpg.player_list.WG_LIST:
                orpg.player_list.WG_LIST[args[2]] = {}
            orpg.player_list.WG_LIST[args[2]][int(args[1])] = int(args[1])
            return
        elif args[0] == "remove" or args[0] == "delete":
            del orpg.player_list.WG_LIST[args[2]][int(args[1])]
            if len(orpg.player_list.WG_LIST[args[2]]) == 0:
                del orpg.player_list.WG_LIST[args[2]]
            return
        elif args[0] == "create" or args[0] == "new_group":
            if not args[1] in orpg.player_list.WG_LIST:
                orpg.player_list.WG_LIST[args[1]] = {}
            return
        elif args[0] == "list":
            if args[1] in orpg.player_list.WG_LIST:
                for n in orpg.player_list.WG_LIST[args[1]]:
                    player = self.session.get_player_info(str(n))
                    self.chat.InfoPost(player.name)
            else:
                self.chat.InfoPost("Invalid Whisper Group Name")
            return
        elif args[0] == "clear":
            if args[1] in orpg.player_list.WG_LIST:
                orpg.player_list.WG_LIST[args[1]].clear()
            else:
                self.chat.InfoPost("Invalid Whisper Group Name")
            return
        elif args[0] == "clearall":
            orpg.player_list.WG_LIST.clear()
            return
        else:
            self.chat.InfoPost("<b>/gw add</b> (player_id) (group_name) - Adds [player_id] to [group_name]")
            self.chat.InfoPost("<b>/gw remove</b> (player_id) (group_name) - Removes [player_id] from [group_name]")
            self.chat.InfoPost("<b>/gw</b> (group_name)<b>=</b>(message) - Sends [message] to [group_name]")
            self.chat.InfoPost("<b>/gw create</b> (group_name) - Creates a whisper group called [group_name]")
            self.chat.InfoPost("<b>/gw list</b> (group_name) - Lists all players in [group_name]")
            self.chat.InfoPost("<b>/gw clear</b> (group_name) - Removes all players from [group_name]")
            self.chat.InfoPost("<b>/gw clearall</b> - Removes all existing whisper groups")
            return
        msg = cmdargs[delim+1:].strip()
        for gid in group_ids:
            idList = ""
            for n in orpg.player_list.WG_LIST[gid]:
                if idList == "":
                    idList = str(n)
                else:
                    idList = str(n) + ", " + idList
            self.on_whisper(idList + "=" + msg)

    def on_gmwhisper(self, cmdargs):
        if cmdargs == "":
            self.chat.InfoPost("**Incorrect syntax for GM Whisper.")
        else:
            the_gms = self.chat.get_gms()
            if len(the_gms):
                gmstring = ""
                for each_gm in the_gms:
                    if gmstring != "":
                        gmstring += ","
                    gmstring += each_gm
                self.on_whisper(gmstring + "=" + cmdargs)
            else:
                self.chat.InfoPost("**No GMs to Whisper to.")
