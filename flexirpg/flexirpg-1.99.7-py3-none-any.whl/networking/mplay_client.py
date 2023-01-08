# Networking client
#
# Copyright 2020 David Vrabel
# Copyright (C) 2000-2001 The OpenRPG Project
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.

from collections import namedtuple
import errno
import os
from queue import Queue
import socket
from string import *
from struct import pack, unpack, calcsize
import time
import traceback
import zlib

import orpg.lib.xmlutil as xmlutil
import orpg.networking.mplay_queue as mplay_queue
from orpg.version import *

from orpg.networking.client_base import (
    client_base, MPLAY_CONNECTED, MPLAY_DISCONNECTING,
    MPLAY_DISCONNECTED, OPENRPG_PORT)
from .player import Player
from .roles import *

# We should be sending a length for each packet
MPLAY_GROUP_CHANGE = 4
MPLAY_GROUP_CHANGE_F = 5
PLAYER_NEW = 1
PLAYER_DEL = 2
PLAYER_GROUP = 3

#  The next two messages are used to inform others that a player is typing
PLAYER_TYPING = 4
PLAYER_NOT_TYPING = 5
PLAYER_UPDATE = 6
GROUP_JOIN = 1
GROUP_NEW = 2
GROUP_DEL = 3
GROUP_UPDATE = 4

class mplay_event:
    def __init__(self,id,data=None):
        self.id = id
        self.data = data

    def get_id(self):
        return self.id

    def get_data(self):
        return self.data

BOOT_MSG = "YoU ArE ThE WeAkEsT LiNk. GoOdByE."

Group = namedtuple("Group", ["id", "name", "has_pwd", "num_players", "has_admin_pwd"])

#========================================================================
#
#
#                           MPLAY CLIENT
#
#
#========================================================================
class mplay_client(client_base):
    "mplay client"
    def __init__(self, name, window, callbacks):
        client_base.__init__(self)
        self.set_name(name)
        self.window = window
        self.on_receive = callbacks['on_receive']
        self.on_mplay_event = callbacks['on_mplay_event']
        self.on_group_event = callbacks['on_group_event']
        self.on_player_event = callbacks['on_player_event']
        self.on_password_signal = callbacks['on_password_signal']
        self.players = {}
        self.groups = {}
        self.unique_cookie = 0
        self.msg_handlers = {}
        self.core_msg_handlers = []
        self.load_core_msg_handlers()

    @property
    def id(self):
        return self.player.id

    def set_name(self,name):
        self.player.name = name
        self.update()

    def set_text_status(self, status):
        if self.player.status != status:
            self.player.status = status
            self.update()

    def player_is_typing(self, typing):
        if typing == self.player.typing:
            return
        self.player.typing = typing
        self.update()

    def update(self, evt=None):
        if self.status == MPLAY_CONNECTED:
            self.outbox.put(self.toxml('update'))
            self.inbox.put(self.toxml('update'))

    def get_group_info(self, id=0):
        self.statLock.acquire()
        id = self.groups[id]
        self.statLock.release()
        return id

    def get_my_group(self):
        self.statLock.acquire()
        id = self.groups[self.group_id]
        self.statLock.release()
        return id

    def get_groups(self):
        self.statLock.acquire()
        groups = list(self.groups.values())
        self.statLock.release()
        return groups

    def get_players(self):
        self.statLock.acquire()
        players = list(self.players.values())
        self.statLock.release()
        return players

    def get_player_info(self,id):
        self.statLock.acquire()
        player = self.players[id]
        self.statLock.release()
        return player

    def is_valid_id(self,id):
        self.statLock.acquire()
        value = id in self.players
        self.statLock.release()
        return value

    def clear_players(self,save_self=0):
        self.statLock.acquire()
        keys = list(self.players.keys())
        for k in keys:
            del self.players[k]
        self.statLock.release()

    def clear_groups(self):
        self.statLock.acquire()
        keys = list(self.groups.keys())
        for k in keys:
            del self.groups[k]
        self.statLock.release()

    def find_role(self,id):
        return self.players[id].role

    def boot_player(self,id,boot_pwd = ""):
        #self.send(BOOT_MSG,id)
        msg = '<boot boot_pwd="' + boot_pwd + '"/>'
        self.send(msg,id)

#---------------------------------------------------------
# [START] Snowdog Password/Room Name altering code 12/02
#---------------------------------------------------------

    def set_room_pass(self,npwd,pwd=""):
        self.outbox.put("<alter key=\"pwd\" val=\"" +npwd+ "\" bpw=\"" + pwd + "\" plr=\"" + self.id +"\" gid=\"" + self.group_id + "\" />")
        self.update()

    def set_room_name(self,name,pwd=""):
        loc = name.find("&")
        oldloc=0
        while loc > -1:
            loc = name.find("&",oldloc)
            if loc > -1:
                b = name[:loc]
                e = name[loc+1:]
                name = b + "&amp;" + e
                oldloc = loc+1
        loc = name.find('"')
        oldloc=0
        while loc > -1:
            loc = name.find('"',oldloc)
            if loc > -1:
                b = name[:loc]
                e = name[loc+1:]
                name = b + "&quot;" + e
                oldloc = loc+1
        loc = name.find("'")
        oldloc=0
        while loc > -1:
            loc = name.find("'",oldloc)
            if loc > -1:
                b = name[:loc]
                e = name[loc+1:]
                name = b + "&#39;" + e
                oldloc = loc+1
        self.outbox.put("<alter key=\"name\" val=\"" + name + "\" bpw=\"" + pwd + "\" plr=\"" + self.id +"\" gid=\"" + self.group_id + "\" />")
        self.update()

#---------------------------------------------------------
# [END] Snowdog Password/Room Name altering code  12/02
#---------------------------------------------------------

    def display_roles(self):
        self.outbox.put("<role action=\"display\" player=\"" + self.id +"\" group_id=\""+self.group_id + "\" />")

    def get_role(self):
        self.outbox.put("<role action=\"get\" player=\"" + self.id +"\" group_id=\""+self.group_id + "\" />")

    def set_role(self,player,role,pwd=""):
        self.outbox.put("<role action=\"set\" player=\"" + player + "\" role=\"" +role+ "\" boot_pwd=\"" + pwd + "\" group_id=\"" + self.group_id + "\" />")
        self.update()

    def send(self,msg,player="all"):
        if self.status == MPLAY_CONNECTED and player != self.id:
            self.outbox.put("<msg to='"+player+"' from='"+self.id+"' group_id='"+self.group_id+"' />"+msg)
        self.check_my_status()

    def send_create_group(self,name,pwd,boot_pwd,minversion):
        self.outbox.put("<create_group from=\""+self.id+"\" pwd=\""+pwd+"\" name=\""+
                        name+"\" boot_pwd=\""+boot_pwd+"\" min_version=\"" + minversion +"\" />")

    def send_join_group(self,group_id,pwd):
        if (group_id != 0):
            self.player.role = ROLE_LURKER
        self.outbox.put("<join_group from=\""+self.id+"\" pwd=\""+pwd+"\" group_id=\""+str(group_id)+"\" />")

    def poll(self, evt=None):
        try:
            msg = self.inbox.get_nowait()
        except:
            if self.get_status() != MPLAY_CONNECTED:
                self.check_my_status()
            return
        if msg == "":
            self.do_disconnect()
        else:
            try:
                self.pretranslate(msg)
            except Exception as e:
                print("The following  message: " + str(msg))
                print("created the following exception: ")
                traceback.print_exc()

    def add_msg_handler(self, tag, function, core=False):
        if not tag in self.msg_handlers:
            self.msg_handlers[tag] = function
            if core:
                self.core_msg_handlers.append(tag)
        else:
            print('XML Messages ' + tag + ' already has a handler')

    def remove_msg_handler(self, tag):
        if self.msg_handlers.has_key(tag) and not tag in self.core_msg_handlers:
            del self.msg_handlers[tag]
        else:
            print('XML Messages ' + tag + ' already deleted')

    def load_core_msg_handlers(self):
        self.add_msg_handler('msg', self.on_msg, True)
        self.add_msg_handler('ping', self.on_ping, True)
        self.add_msg_handler('group', self.on_group, True)
        self.add_msg_handler('role', self.on_role, True)
        self.add_msg_handler('player', self.on_player, True)
        self.add_msg_handler('password', self.on_password, True)

    def pretranslate(self,data):
        # Pre-qualify our data.  If we don't have atleast 5-bytes, then there is
        # no way we even have a valid message!
        if len(data) < 5:
            return
        end = data.find(">")
        head = data[:end+1]
        msg = data[end+1:]
        xml_dom = xmlutil.parseXml(head)
        xml_dom = xml_dom.documentElement
        tag_name = xml_dom.tagName
        id = xml_dom.getAttribute("from")
        if id == '':
            id = xml_dom.getAttribute("id")
        if tag_name in self.msg_handlers:
            self.msg_handlers[tag_name](id, data, xml_dom)
        else:
            # Ignoring unhandled message.
            pass
        if xml_dom:
            xml_dom.unlink()

    def on_msg(self, id, data, xml_dom):
        end = data.find(">")
        head = data[:end+1]
        msg = data[end+1:]
        if id == "0":
            self.on_receive(msg,None)      #  None get's interpreted in on_receive as the sys admin.
                                           #  Doing it this way makes it harder to impersonate the admin
        else:
            if self.is_valid_id(id):
                self.on_receive(msg,self.players[id])

    def on_ping(self, id, msg, xml_dom):
        #a REAL ping time implementation by Snowdog 8/03
        # recieves special server <ping time="###" /> command
        # where ### is a returning time from the clients ping command
        #get current time, pull old time from object and compare them
        # the difference is the latency between server and client * 2
        ct = time.clock()
        ot = xml_dom.getAttribute("time")
        latency = float(float(ct) - float(ot))
        latency = int( latency * 10000.0 )
        latency = float( latency) / 10.0
        ping_msg = "Ping Results: " + str(latency) + " ms (parsed message, round trip)"
        self.on_receive(ping_msg,None)

    def on_group(self, id, msg, xml_dom):
        name = xml_dom.getAttribute("name")
        players = xml_dom.getAttribute("players")
        act = xml_dom.getAttribute("action")
        has_pwd = xml_dom.getAttribute("pwd")
        has_admin_pwd = xmlutil.bool_attrib(xml_dom, "has_boot_pwd", True)

        group = Group(id, name, has_pwd, players, has_admin_pwd)

        if act == 'new':
            self.groups[id] = group
            self.on_group_event(mplay_event(GROUP_NEW, group))
        elif act == 'del':
            del self.groups[id]
            self.on_group_event(mplay_event(GROUP_DEL, group))
        elif act == 'update':
            self.groups[id] = group
            self.on_group_event(mplay_event(GROUP_UPDATE, group))

    def on_role(self, id, msg, xml_dom):
        act = xml_dom.getAttribute("action")
        role = role_from_string(xml_dom.getAttribute("role"))
        if (act == "set") or (act == "update"):
            try:
                self.players[id].role = role
                if id == self.id:
                    self.player.role = role
                self.on_player_event(mplay_event(PLAYER_UPDATE,self.players[id]))
            except KeyError:
                pass

    def on_player(self, id, msg, xml_dom):
        act = xml_dom.getAttribute("action")
        if act == "new":
            self.players[id] = Player.from_xml(xml_dom)
            self.on_player_event(mplay_event(PLAYER_NEW,self.players[id]))
        elif act == "group":
            self.group_id = xml_dom.getAttribute("group_id")
            self.clear_players()
            self.on_mplay_event(mplay_event(MPLAY_GROUP_CHANGE,self.groups[self.group_id]))
            self.players[self.id] = self.player
            self.on_player_event(mplay_event(PLAYER_NEW,self.players[self.id]))
        elif act == "failed":
            self.on_mplay_event(mplay_event(MPLAY_GROUP_CHANGE_F))
        elif act == "del":
            self.on_player_event(mplay_event(PLAYER_DEL,self.players[id]))
            if id in self.players:
                del self.players[id]
            if id == self.id:
                self.do_disconnect()
        elif act == "update":
            if id != self.id:
                self.players[id].update_from_xml(xml_dom)
            self.on_player_event(mplay_event(PLAYER_UPDATE, self.players[id]))

    def on_password(self, id, msg, xml_dom):
        signal = type = id = data = None
        id = xml_dom.getAttribute("id")
        type = xml_dom.getAttribute("type")
        signal = xml_dom.getAttribute("signal")
        data = xml_dom.getAttribute("data")
        self.on_password_signal( signal,type,id,data )

    def check_my_status(self):
        status = self.get_status()
        if status == MPLAY_DISCONNECTING:
            self.do_disconnect()

    def connect(self, addressport):
        """Connect to a server."""
        if self.is_connected():
            self.log_msg( "Client is already connected to a server?!?  Need to disconnect first." )
            return 0
        xml_dom = None
        self.inbox = mplay_queue.queue(self.window)
        self.outbox = Queue(0)
        addressport_ar = addressport.split(":")
        if len(addressport_ar) == 1:
            address = addressport_ar[0]
            port = OPENRPG_PORT
        else:
            address = addressport_ar[0]
            port = int(addressport_ar[1])
        self.host_server = addressport
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.sock.connect((address,port))
        except Exception as e:
            print(traceback.format_exc())
            self.log_msg(e)
            if xml_dom:
                xml_dom.unlink()
            return 0

        self.connected()

        # Request the client ID by sending a new player message with
        # id='0' and processing the response.
        self.outbox.put(self.toxml("new"))
        message = self.inbox.get(block=True)
        xml_dom = xmlutil.parseXml(message)
        xml_dom = xml_dom.documentElement
        self.player.id = xml_dom.getAttribute("id")
        self.group_id = xml_dom.getAttribute("group_id")

        # Start things rollings along
        self.on_mplay_event(mplay_event(MPLAY_CONNECTED))
        self.players[self.id] = self.player
        self.on_player_event(mplay_event(PLAYER_NEW, self.player))
        if xml_dom:
            xml_dom.unlink()
        return 1

    def start_disconnect(self):
        self.outbox.put(self.toxml("del"))
        self.do_disconnect(False)

    def do_disconnect(self, signal=True):
        client_base.disconnect(self)
        self.clear_players()
        self.clear_groups()
        self.useroles = False
        if signal:
            self.on_mplay_event(mplay_event(MPLAY_DISCONNECTED))

    def get_next_id(self):
        self.unique_cookie += 1
        return_str = self.id + "-" + str(self.unique_cookie)
        return return_str
