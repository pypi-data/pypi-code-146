# Copyright (C) 2018 David Vrabel
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.

import queue
import socket
from struct import calcsize
from threading import Lock
import time
from xml.sax.saxutils import escape

import orpg.networking.mplay_conn as mplay_conn
from orpg.version import *
from .player import Player
from .roles import *

MPLAY_LENSIZE = calcsize('i')
MPLAY_DISCONNECTED = 0
MPLAY_CONNECTED = 1
MPLAY_DISCONNECTING = 3

# This should be configurable
OPENRPG_PORT = 6774

class client_base:

    # Player role definitions
    def __init__(self):
        self.outbox = queue.Queue(0)
        self.inbox = queue.Queue(0)
        self.group_id = "0"
        self.player = Player("")
        self.status = MPLAY_DISCONNECTED
        self.log_console = None
        self.sock = None
        self.text_status = "Idle"
        self.statLock = Lock()

    @property
    def id(self):
        return self.player.id

    @property
    def name(self):
        return self.player.name

    @property
    def role(self):
        return self.player.role

    def allowed(self, required_role):
        """Does this player have 'required_role' or better?"""
        if not self.is_connected():
            return True
        if required_role == ROLE_GM:
            return self.role == ROLE_GM
        if required_role == ROLE_PLAYER:
            return self.role == ROLE_GM or self.role == ROLE_PLAYER
        if require_role == ROLE_LURKER:
            return True
        return False

    def denied(self, required_role):
        """Does this player lack 'required_role' permissions?"""
        return not self.allowed(required_role)

    def connected(self):
        self.set_status(MPLAY_CONNECTED)
        self.conn = mplay_conn.connection(self.sock, self.inbox, self.outbox)

    def disconnect(self):
        if self.get_status() == MPLAY_CONNECTED:
            self.set_status(MPLAY_DISCONNECTING)
            self.conn.disconnect()
            self.set_status(MPLAY_DISCONNECTED)

    def reset(self, sock):
        self.disconnect()
        self.sock = sock
        self.connected()

    def toxml(self,action):
        xml_data = '<player name="' + escape(self.name, {"\"":""}) + '"'
        xml_data += ' action="' + action + '"'
        xml_data += ' id="' + self.id + '"'
        xml_data += ' group_id="' + self.group_id + '"'
        xml_data += ' status="' + self.player.status + '"'
        xml_data += ' typing="' + ("1" if self.player.typing else "0") + '"'
        xml_data += ' version="' + self.player.version + '"'
        xml_data += ' protocol_version="' + self.player.protocol_version + '"'
        xml_data += ' client_string="' + self.player.client_string + '"'
        xml_data += ' />'
        return xml_data

    def log_msg(self,msg):
        if self.log_console:
            self.log_console(msg)

    def get_status(self):
        self.statLock.acquire()
        status = self.status
        self.statLock.release()
        return status

    def set_status(self,status):
        self.statLock.acquire()
        self.status = status
        self.statLock.release()

    def __str__(self):
        return "%s(%s)\nIP:%s\ngroup_id:%s\n" % (self.name, self.id, self.group_id)

    def idle_time(self):
        curtime = time.time()
        idletime = curtime - self.conn.last_message_time
        return idletime

    def idle_status(self):
        idletime = self.idle_time()
        idlemins = idletime / 60
        status = "Unknown"
        if idlemins < 3:
            status = "Active"
        elif idlemins < 10:
            status = "Idle ("+str(int(idlemins))+" mins)"
        else:
            status = "Inactive ("+str(int(idlemins))+" mins)"
        return status

    def is_connected(self):
        return self.status == MPLAY_CONNECTED

    def connected_time(self):
        curtime = time.time()
        timeoffset = curtime - self.conn.connect_time
        return timeoffset

    def connected_time_string(self):
        "returns the time client has been connected as a formated time string"
        ct = self.connected_time()
        d = int(ct/86400)
        h = int( (ct-(86400*d))/3600 )
        m = int( (ct-(86400*d)-(3600*h))/60)
        s = int( (ct-(86400*d)-(3600*h)-(60*m)) )
        return f"{d:02}:{h:02}:{m:02}:{s:02}"
