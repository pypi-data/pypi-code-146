# FlexiRPG -- Server
#
# Copyright 2020 David Vrabel
# Copyright (C) 2000-2001 The OpenRPG Project
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.

"""
<msg to='' from='' group_id='' />
<player id='' ip='' group_id='' name='' action='new,del,group,update' status="" version=""/>
<group id='' name='' pwd='' players='' action='new,del,update' />
<create_group from='' pwd='' name='' />
<join_group from='' pwd='' group_id='' />
<role action='set,get,display' player='' group_id='' boot_pwd='' role=''/>
"""

import gc
import cgi
import queue
import sys
import string
import time
import urllib.request, urllib.parse, urllib.error
from orpg.mapper.map_msg import *
from threading import Event, Lock, RLock
from struct import pack, unpack, calcsize
import traceback
import re
import socket
import _thread
import zlib

from orpg.tools.paths import Paths
import orpg.mapper.image
import orpg.mapper.imagelibrary
import orpg.mapper.imageprovider
import orpg.lib.xmlutil as xmlutil
from orpg.version import *

from .client_base import (client_base, MPLAY_CONNECTED, MPLAY_DISCONNECTING,
                          MPLAY_DISCONNECTED, MPLAY_LENSIZE, OPENRPG_PORT)
from .roles import *


class game_group(object):
    def __init__( self, id, name, pwd, boot_pwd):
        self.id = id
        self.name = name
        self.players = []
        self.pwd = pwd
        self.boot_pwd = boot_pwd
        self.game_map = map_msg()

        if id == "0":
            map_file = Paths.config("Lobby_map.xml")
        else:
            map_file = Paths.template("default_map.xml")
        with open(map_file) as f:
            tree = f.read()
        self.game_map.init_from_xml(tree)

    def add_player(self, id):
        self.players.append(id)

    def remove_player(self, id):
        self.players.remove(id)

    def get_num_players(self):
        return len(self.players)

    def get_player_ids(self):
        return self.players

    def check_pwd(self, pwd):
        return pwd == self.pwd

    def check_boot_pwd(self, pwd):
        return pwd == self.boot_pwd

    def toxml(self,act="new"):
        #  Please don't add the boot_pwd to the xml, as this will give it away to players watching their console
        xml_data = "<group id=\"" + self.id
        xml_data += "\" action=\"" + act
        xml_data += "\" name=\"" + self.name
        xml_data += "\" pwd=\"" + str(self.pwd!="")
        xml_data += "\" has_boot_pwd=\"" + str(self.boot_pwd != "")
        xml_data += "\" players=\"" + str(self.get_num_players())
        xml_data += "\" />"
        return xml_data


class client_stub(client_base):
    def __init__(self,inbox,sock,props,log):
        client_base.__init__(self)
        self.player.id = props['id']
        self.player.name = props['name']
        self.player.role = props['role']
        self.player.status = props['text_status']
        self.ip = props['ip']
        self.group_id = props['group_id']
        self.version = props['version']
        self.protocol_version = props['protocol_version']
        self.client_string = props['client_string']
        self.inbox = inbox
        self.sock = sock
        self.log_console = log

        self.connected()

    @property
    def id(self):
        return self.player.id

    def send(self,msg,player,group):
        if self.get_status() == MPLAY_CONNECTED:
            self.outbox.put("<msg to='" + player + "' from='0' group_id='" + group + "' />" + msg)

    def change_group(self,group_id,groups):
        old_group_id = str(self.group_id)
        groups[group_id].add_player(self.id)
        groups[old_group_id].remove_player(self.id)
        self.group_id = group_id
        self.outbox.put(self.toxml('group'))
        msg = groups[group_id].game_map.get_all_xml()
        self.send(msg,self.id,group_id)
        return old_group_id

    def self_message(self,act):
        self.send(act,self.id,self.group_id)

    def take_dom(self,xml_dom):
        self.player.name = xml_dom.getAttribute("name")
        self.player.status = xml_dom.getAttribute("status")


######################################################################
######################################################################
##
##
##   MPLAY SERVER
##
##
######################################################################
######################################################################

class mplay_server:
    def __init__(self, log_console=None, name=None):
        self.log_to_console = 1
        self.log_console = log_console
        self.alive = 1
        self.players = {}
        self.listen_event = Event()
        self.incoming_event = Event()
        self.incoming = queue.Queue(0)
        self.server_lock = Lock()
        self.next_player_id = 1
        self.next_group_id = 100
        self.boot_pwd = None
        self.minClientVersion = SERVER_MIN_CLIENT_VERSION
        self.maxSendSize = 1024
        self.server_port = OPENRPG_PORT

    def initServer(self, **kwargs):
        self.initServerConfig()
        self.listen_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.listen_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.listen_thread = _thread.start_new_thread(self.listenAcceptThread, (0,))
        self.in_thread = _thread.start_new_thread(self.message_handler,(0,))

        self.svrcmds = {}
        self.initsvrcmds()

        self.image_library = orpg.mapper.imagelibrary.ImageLibrary(orpg.mapper.image.ServerImage)
        self.image_library.register_provider(orpg.mapper.imageprovider.ImageProviderCache())
        self.image_library.register_provider(orpg.mapper.imageprovider.ImageProviderServer(self))

    def addsvrcmd(self, cmd, function):
        if cmd not in self.svrcmds:
            self.svrcmds[cmd] = {}
            self.svrcmds[cmd]['function'] = function

    def initsvrcmds(self):
        self.addsvrcmd('msg', self.incoming_msg_handler)
        self.addsvrcmd('player', self.incoming_player_handler)
        self.addsvrcmd('alter', self.do_alter)
        self.addsvrcmd('role', self.do_role)
        self.addsvrcmd('ping', self.do_ping)
        self.addsvrcmd('join_group', self.join_group)
        self.addsvrcmd('create_group', self.create_group)

    # This method reads in the server's configuration file and reconfigs the server
    # as needed, over-riding any default values as requested.
    def initServerConfig(self):
        server_ini = Paths.config("server_ini.xml")
        self.log_msg(f"Using configuration from {server_ini}")
        try:
            self.configDoc = xmlutil.parse_file(server_ini)
            self.configDom = self.configDoc.documentElement
            # Obtain the lobby/server password if it's been specified
            if self.configDom.hasAttribute("admin"):
                self.boot_pwd = self.configDom.getAttribute("admin")
            elif self.configDom.hasAttribute("boot"):
                self.boot_pwd = self.configDom.getAttribute("boot")
            if self.configDom.hasAttribute("lobbyname"):
                lobby_name = self.configDom.getAttribute("lobbyname")
            else:
                lobby_name = "Lobby"
            if self.configDom.hasAttribute("default_role"):
                self.default_role = role_from_string(self.configDom.getAttribute("default_role"))
            else:
                self.default_role = ROLE_PLAYER

            # Add the lobby.
            self.groups = {
                '0': game_group("0", lobby_name, "", self.boot_pwd),
            }

            # set ip or dns name to send to meta server
            service_node = self.configDom.getElementsByTagName("service")[0]
            if service_node.hasAttribute("port"):
                self.server_port = int(service_node.getAttribute("port"))

            self.log_msg("Server Configuration File: Processing Completed.")

        except Exception as e:
            traceback.print_exc()
            self.log_msg("Exception in initServerConfig() " + str(e))

    def recvData( self, sock, readSize ):
        """Simple socket receive method.  This method will only return when the exact
        byte count has been read from the connection, if remote terminates our
        connection or we get some other socket exception."""

        data = b""
        offset = 0
        try:
            while offset != readSize:
                frag = sock.recv( readSize - offset )

                # See if we've been disconnected
                rs = len( frag )
                if rs <= 0:
                    # Loudly raise an exception because we've been disconnected!
                    raise IOError("Remote closed the connection!")

                else:
                    # Continue to build complete message
                    offset += rs
                    data += frag

        except socket.error as e:
            self.log_msg("Socket Error: recvData(): " +  e )
            data = ""

        return data

    def recvMsg(self, sock):
        """This method now expects to receive a message having a 4-byte prefix length.  It will ONLY read
        completed messages.  In the event that the remote's connection is terminated, it will throw an
        exception which should allow for the caller to more gracefully handles this exception event.

        Because we use strictly reading ONLY based on the length that is told to use, we no longer have to
        worry about partially adjusting for fragmented buffers starting somewhere within a buffer that we've
        read.  Rather, it will get ONLY a whole message and nothing more.  Everything else will remain buffered
        with the OS until we attempt to read the next complete message."""

        msgData = ""
        try:
            lenData = self.recvData( sock, MPLAY_LENSIZE )

            # Now, convert to a usable form
            (length,) = unpack('!i', lenData)

            # Read exactly the remaining amount of data
            msgData = self.recvData( sock, length )
            msgData = zlib.decompress(msgData).decode('utf-8')
        except Exception as e:
            self.log_msg( "Exception: recvMsg(): " + str(e) )

        return msgData



    def kill_server(self):
        self.alive = 0
        self.log_msg("Server stopping...")
        for p in self.players.values():
            p.disconnect()
        self.incoming.put("")

        # Wake up the listen thread with a connection attempt.
        try:
            ip = socket.gethostbyname(socket.gethostname())
            kill = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            kill.connect((ip, self.server_port))
            kill.close()
        except:
            pass

        self.listen_sock.close()
        self.listen_event.wait(10)
        self.incoming_event.wait(10)
        self.log_msg("Server stopped!")

    def log_msg(self,msg):
        if self.log_to_console:
            if self.log_console:
                self.log_console(msg)
            else:
                print(str(msg))

    def console_log(self):
        if self.log_to_console == 1:
            print("console logging now off")
            self.log_to_console = 0
        else:
            print("console logging now on")
            self.log_to_console = 1


    def groups_list(self):
        self.server_lock.acquire()
        try:
            keys = list(self.groups.keys())
            for k in keys:
                pw = "-"
                pr = " -"
                if self.groups[k].pwd != "":
                    pw = "P"
                print("Group: " + k + pw + '  Name: ' + self.groups[k].name)
            print()

        except Exception as e:
            self.log_msg(str(e))

        self.server_lock.release()

    def group_dump(self,k):
        self.server_lock.acquire()
        try:
            print("Group: " + k)
            print("    Name:  %s" % self.groups[k].name)
            print("    Desc:  %s" % self.groups[k].desc)
            print("    Pass:  %s" % self.groups[k].pwd)
            print("    Boot:  %s" % self.groups[k].boot_pwd)
            print("    Map:  %s" % self.groups[k].game_map.get_all_xml())
            print()
        except Exception as e:
            self.log_msg(str(e))
        self.server_lock.release()

    def player_list(self):
        "display a condensed list of players on the server"
        self.server_lock.acquire()
        try:
            keys = list(self.groups.keys())
            keys.sort(key=int)
            for k in keys:
                groupstring = "Group " + str(k)  + ": " +  self.groups[k].name
                if self.groups[k].pwd != "":
                    groupstring += " (Pass: \"" + self.groups[k].pwd + "\" )"
                print(groupstring)
                ids = self.groups[k].get_player_ids()
                ids.sort(key=int)
                for id in ids:
                    if id in self.players:
                        print("  (%s)%s %s [IP: %s] %s (%s)" % (
                            self.players[id].id, self.players[id].name,
                            self.players[id].role,
                            self.players[id].ip, self.players[id].idle_status(),
                            self.players[id].connected_time_string()))
                    else:
                        self.groups[k].remove_player(id)
                        print("Bad Player Ref (#" + id + ") in group")
                if len(ids) > 0: print("")
        finally:
            self.server_lock.release()


    def update_request(self,newsock,xml_dom):
        # handle reconnects

        self.log_msg( "update_request() has been called." )

        # get player id
        id = xml_dom.getAttribute("id")
        group_id = xml_dom.getAttribute("group_id")

        if id in self.players:
            self.players[id].reset(newsock)
            self.players[id].outbox.put(self.players[id].toxml("update"))
            self.players[id].clear_timeout()
            need_new = 0
        else:
            need_new = 1

        if need_new:
            self.new_request(newsock,xml_dom)
        else:
            msg = self.groups[group_id].game_map.get_all_xml()
            self.send(msg,id,group_id)


    def new_request(self,newsock,xml_dom,LOBBY_ID='0'):
        #build client stub
        props = {}
        # Don't trust what the client tells us...trust what they connected as!
        props['ip'] = socket.gethostbyname( newsock.getpeername()[0] )

        try:
            props['role'] = role_from_string(xml_dom.getAttribute("role"))
        except:
            props['role'] = ROLE_GM

        props['name'] = xml_dom.getAttribute("name")
        props['group_id'] = LOBBY_ID
        props['id'] = str(self.next_player_id)
        props['text_status'] = xml_dom.getAttribute("status")
        props['version'] = xml_dom.getAttribute("version")
        props['protocol_version'] = xml_dom.getAttribute("protocol_version")
        props['client_string'] = xml_dom.getAttribute("client_string")
        self.next_player_id += 1
        new_stub = client_stub(self.incoming,newsock,props,self.log_console)

        new_stub.outbox.put(new_stub.toxml("new"))

        #start threads and store player

        allowed = True
        version_string = ""

        if props['protocol_version'] != PROTOCOL_VERSION:
            version_string = "Client protocol version (%s) is incompatible with server (%s).<br/>" % (
                props['protocol_version'], PROTOCOL_VERSION)
            allowed = False

        if not self.checkClientVersion(props['version']):
            version_string = "Client version (%s) is older than the minimum version supported by the server (%s).<br/>" % (props['version'], self.minClientVersion)
            allowed = False

        if not allowed:
            new_stub.outbox.put("<msg to='" + props['id'] + "' from='0' group_id='0' />"
                                + version_string)
            self.log_msg("Connection terminating due to version incompatibility with client (ver: " + props['version'] + "  protocol: " + props['protocol_version'] + ")" )
            new_stub.disconnect()
            return None

        #
        # Send current player and group lists, lobby message, lobby
        # map, and current player roles.
        #
        self.players[props['id']] = new_stub
        self.groups[LOBBY_ID].add_player(props['id']) #always add to lobby on connection.
        self.send_group_list(props['id'])
        self.send_player_list(props['id'],LOBBY_ID)

        self.SendLobbyMessage(props['id'])

        msg = self.groups[LOBBY_ID].game_map.get_all_xml()
        self.send(msg,props['id'],LOBBY_ID)
        self.send_to_group(props['id'],LOBBY_ID,self.players[props['id']].toxml('new'))
        self.return_room_roles(props['id'],LOBBY_ID)

        # Re-initialize the role for this player incase they came from a different server
        self.handle_role("set", props['id'], ROLE_GM, self.groups[LOBBY_ID].boot_pwd, LOBBY_ID)

        cmsg = "Client Connect: (" + str(props['id']) + ") " + str(props['name']) + " [" + str(props['ip']) + "]"
        self.log_msg(cmsg)


    def checkClientVersion(self, clientversion):
        minv = self.minClientVersion.split('.')
        cver = clientversion.split('.')
        for i in range(min(len(minv),len(cver))):
            c = int(cver[i])
            s = int(minv[i])
            if c > s:
                return True
            if c < s:
                return False
        if len(minv) > len(cver):
            return False
        return True

    def SendLobbyMessage(self, player_id):
        with open(Paths.config("LobbyMessage.html")) as f:
            lobby_msg = f.read()
        if lobby_msg:
            self.send(lobby_msg, player_id, "0")

    def listenAcceptThread(self,arg):
        #  Set up the socket to listen on.
        try:
            self.listen_sock.bind(('', self.server_port))
            self.listen_sock.listen(5)

        except Exception as e:
            self.log_msg(("Error binding request socket!", e))
            self.alive = 0


        while True:
            #  Block on the socket waiting for a new connection
            try:
                (newsock, addr) = self.listen_sock.accept()
                if not self.alive:
                    break;

                # Now that we've accepted a new connection, we must immediately spawn a new
                # thread to handle it...otherwise we run the risk of having a DoS shoved into
                # our face!  :O  After words, this thread is dead ready for another connection
                # accept to come in.
                _thread.start_new_thread(self.acceptedNewConnectionThread, ( newsock, addr ))

            except:
                print("The following exception caught accepting new connection:")
                traceback.print_exc()

        #  At this point, we're done and cleaning up.
        self.listen_event.set()


    def acceptedNewConnectionThread(self, newsock, addr):
        """Once a new connection comes in and is accepted, this thread starts up to handle it."""

        # Initialize xml_dom
        xml_dom = None
        data = None

        # get client info and send othe client info
        # If this receive fails, this thread should exit without even attempting to process it
        self.log_msg("Connection from " + str(addr) + " has been accepted.  Waiting for data...")

        data = self.recvMsg(newsock)

        if data=="" or data == None:
            self.log_msg("Connection from " + str(addr) + " failed. Closing connection.")
            try:
                newsock.close()
            except Exception as e:
                self.log_msg( str(e) )
                print(str(e))
            return #returning causes connection thread instance to terminate

        #  Parse the XML received from the connecting client
        try:
            xml_dom = xmlutil.parseXml(data)
            xml_dom = xml_dom.documentElement

        except:
            try:
                newsock.close()
            except:
                pass
            self.log_msg( "Error in parse found from " + str(addr) + ".  Disconnected.")
            self.log_msg("  Offending data(" + str(len(data)) + "bytes)=" + data)
            self.log_msg( "Exception:")
            traceback.print_exc()
            return #returning causes connection thread instance to terminate

        self.server_lock.acquire()

        #  Determine the correct action and execute it
        try:
            # get action
            action = xml_dom.getAttribute("action")

            # Figure out what type of connection we have going on now
            if action == "new":
                self.new_request(newsock,xml_dom)
            elif action == "update":
                self.update_request(newsock,xml_dom)
            else:
                self.log_msg("Unknown Join Request!")
        except Exception as e:
            print("The following  message: " + str(data))
            print("from " + str(addr) + " created the following exception: ")
            traceback.print_exc()

        self.server_lock.release()

        if xml_dom:
            xml_dom.unlink()

    def message_handler(self,arg):
        while True:
            data = self.incoming.get(block=True)
            if not self.alive:
                break;

            self.server_lock.acquire()

            if data == "":
                self.cleanup_disconnected_clients()
            else:
                self.parse_incoming_dom(data)

            self.server_lock.release()

        self.incoming_event.set()

    def parse_incoming_dom(self,data):
        end = data.find(">") #locate end of first element of message
        head = data[:end+1]
        #self.log_msg(head)
        xml_dom = None
        try:
            xml_dom = xmlutil.parseXml(head)
            xml_dom = xml_dom.documentElement
            self.message_action(xml_dom,data)

        except Exception as e:
            print("Error in parse of inbound message. Ignoring message.")
            print("  Offending data(" + str(len(data)) + "bytes)=" + data)
            print("Exception=" + str(e))

        if xml_dom: xml_dom.unlink()


    def message_action(self, xml_dom, data):
        tag_name = xml_dom.tagName
        if tag_name in self.svrcmds:
            self.svrcmds[tag_name]['function'](xml_dom,data)
        else:
            raise Exception("Not a valid header!")
        #Message Action thread expires and closes here.
        return


    def do_alter(self, xml_dom, data):
        target = xml_dom.getAttribute("key")
        value = xml_dom.getAttribute("val")
        player = xml_dom.getAttribute("plr")
        group_id = xml_dom.getAttribute("gid")
        boot_pwd = xml_dom.getAttribute("bpw")
        actual_boot_pwd = self.groups[group_id].boot_pwd

        if boot_pwd == actual_boot_pwd:
            if target == "pwd":
                lmessage = "Room password changed to from \"" + self.groups[group_id].pwd + "\" to \"" + value  + "\" by " + player
                self.groups[group_id].pwd = value
                msg ="<msg to='" + player + "' from='0' group_id='0' /> Room password changed to \"" +  value + "\"."
                self.players[player].outbox.put(msg)
                self.log_msg(lmessage)
                self.send_to_all('0',self.groups[group_id].toxml('update'))
            elif target == "name":
                # Check for & in name.  We want to allow this because of its common
                # use in d&d games
                result = self.change_group_name(group_id,value,player)
                msg ="<msg to='" + player + "' from='0' group_id='0' />" + result
                self.players[player].outbox.put(msg)
        else:
            msg ="<msg to='" + player + "' from='0' group_id='0'>Invalid Administrator Password."
            self.players[player].outbox.put(msg)


    def do_role(self, xml_dom, data):
        role = ROLE_LURKER
        boot_pwd = ""
        act = xml_dom.getAttribute("action")
        player = xml_dom.getAttribute("player")
        group_id = xml_dom.getAttribute("group_id")
        if act == "set":
            role = role_from_string(xml_dom.getAttribute("role"))
            boot_pwd = xml_dom.getAttribute("boot_pwd")
        if group_id != "0":
            self.handle_role(act, player, role, boot_pwd, group_id)
            self.log_msg(("role", (player, role)))

    def do_ping(self, xml_dom, data):
        player = xml_dom.getAttribute("player")
        group_id = xml_dom.getAttribute("group_id")
        sent_time = ""
        msg = ""
        try:
            sent_time = xml_dom.getAttribute("time")
        except:
            pass

        if sent_time != "":
            #because a time was sent return a ping response
            msg ="<ping time='" + str(sent_time) + "' />"
        else:
            msg ="<msg to='" + player + "' from='" + player + "' group_id='" + group_id + "'><font color='#FF0000'>PONG!?!</font>"

        self.players[player].outbox.put(msg)

    def join_group(self,xml_dom,data):
        try:
            from_id = xml_dom.getAttribute("from")
            pwd = xml_dom.getAttribute("pwd")
            group_id = xml_dom.getAttribute("group_id")
            ver = self.players[from_id].version
            allowed = 1

            if not self.groups[group_id].check_pwd(pwd):
                allowed = 0

                #tell the clients password manager the password failed -- SD 8/03
                pm = "<password signal=\"fail\" type=\"room\" id=\"" +  group_id  + "\" data=\"\"/>"
                self.players[from_id].outbox.put(pm)

                msg = 'failed - incorrect room password'

            if not allowed:
                self.players[from_id].self_message(msg)
                #the following line makes sure that their role is reset to normal,
                #since it is briefly set to lurker when they even TRY to change
                #rooms
                msg = "<role action=\"update\" id=\"" + from_id  + "\" role=\"" + self.players[from_id].role + "\" />"
                self.players[from_id].outbox.put(msg)
                return

            #move the player into their new group.
            self.move_player(from_id, group_id)

        except Exception as e:
            self.log_msg(str(e))

    def move_player(self, from_id, group_id ):
        "move a player from one group to another"
        try:
            try:
                if group_id == "0":
                    self.players[from_id].player.role = ROLE_GM
                else:
                    self.players[from_id].player.role = self.default_role
            except Exception as e:
                print("exception in move_player() ")
                traceback.print_exc()

            old_group_id = self.players[from_id].change_group(group_id,self.groups)
            self.send_to_group(from_id,old_group_id,self.players[from_id].toxml('del'))
            self.send_to_group(from_id,group_id,self.players[from_id].toxml('new'))
            self.check_group(from_id, old_group_id)

            # Now, tell everyone that we've arrived
            self.send_to_all('0', self.groups[group_id].toxml('update'))

            # this line sends a handle role message to change the players role
            self.send_player_list(from_id,group_id)

            #notify user about others in the room
            self.return_room_roles(from_id,group_id)
            self.log_msg(("join_group", (from_id, group_id)))
            self.handle_role("set", from_id, self.players[from_id].role, self.groups[group_id].boot_pwd, group_id)

        except Exception as e:
            self.log_msg(str(e))

    def return_room_roles(self,from_id,group_id):
        for m in list(self.players.keys()):
            if self.players[m].group_id == group_id:
                msg = ("<role action=\"update\" id=\"" + self.players[m].player.id
                       + "\" role=\"" + self.players[m].role + "\" />")
                self.players[from_id].outbox.put(msg)

    def change_group_name(self,gid,name,pid):
        "Change the name of a group"
        # Check for & in name.  We want to allow this because of its common
        # use in d&d games.
        try:
            loc = name.find("&")
            oldloc = 0
            while loc > -1:
                loc = name.find("&",oldloc)
                if loc > -1:
                    b = name[:loc]
                    e = name[loc+1:]
                    value = b + "&amp;" + e
                    oldloc = loc+1

            loc = name.find("'")
            oldloc = 0
            while loc > -1:
                loc = name.find("'",oldloc)
                if loc > -1:
                    b = name[:loc]
                    e = name[loc+1:]
                    name = b + "&#39;" + e
                    oldloc = loc+1

            loc = name.find('"')
            oldloc = 0
            while loc > -1:
                loc = name.find('"',oldloc)
                if loc > -1:
                    b = name[:loc]
                    e = name[loc+1:]
                    name = b + "&quot;" + e
                    oldloc = loc+1

            oldroomname = self.groups[gid].name
            self.groups[gid].name = str(name)
            lmessage = "Room name changed to from \"" + oldroomname + "\" to \"" + name + "\""
            self.log_msg(lmessage  + " by " + str(pid) )
            self.send_to_all('0',self.groups[gid].toxml('update'))
            return lmessage
        except:
            return "An error occured during rename of room!"


    def create_group(self,xml_dom,data):
        try:
            from_id = xml_dom.getAttribute("from")
            pwd = xml_dom.getAttribute("pwd")
            name = xml_dom.getAttribute("name")
            boot_pwd = xml_dom.getAttribute("boot_pwd")

            #
            # Check for & in name.  We want to allow this because of its common
            # use in d&d games.

            loc = name.find("&")
            oldloc = 0
            while loc > -1:
                loc = name.find("&",oldloc)
                if loc > -1:
                    b = name[:loc]
                    e = name[loc+1:]
                    name = b + "&amp;" + e
                    oldloc = loc+1

            loc = name.find("'")
            oldloc = 0
            while loc > -1:
                loc = name.find("'",oldloc)
                if loc > -1:
                    b = name[:loc]
                    e = name[loc+1:]
                    name = b + "&#39;" + e
                    oldloc = loc+1

            loc = name.find('"')
            oldloc = 0
            while loc > -1:
                loc = name.find('"',oldloc)
                if loc > -1:
                    b = name[:loc]
                    e = name[loc+1:]
                    name = b + "&quot;" + e
                    oldloc = loc+1


            group_id = str(self.next_group_id)
            self.next_group_id += 1
            self.groups[group_id] = game_group(group_id, name, pwd, boot_pwd)
            self.players[from_id].outbox.put(self.groups[group_id].toxml('new'))
            old_group_id = self.players[from_id].change_group(group_id,self.groups)
            self.send_to_group(from_id,old_group_id,self.players[from_id].toxml('del'))
            self.check_group(from_id, old_group_id)
            self.send_to_all(from_id,self.groups[group_id].toxml('new'))
            self.send_to_all('0',self.groups[group_id].toxml('update'))
            self.handle_role("set",from_id, ROLE_GM, boot_pwd, group_id)
            lmsg = "Creating Group... (" + str(group_id) + ") " + str(name)
            self.log_msg( lmsg )
            jmsg = "moving to room " + str(group_id) + "."
            self.log_msg( jmsg )

        except Exception as e:
            self.log_msg( "Exception: create_group(): " + str(e))


    def check_group(self, from_id, group_id):
        if group_id not in self.groups:
            return
        # Delete non-lobby groups if they have no players.
        if group_id != "0" and self.groups[group_id].get_num_players() == 0:
            self.send_to_all("0", self.groups[group_id].toxml('del'))
            del self.groups[group_id]
            self.log_msg(("delete_group", (from_id, group_id)))
        else:
            self.send_to_all("0", self.groups[group_id].toxml('update'))

    def del_player(self,id,group_id):
        try:
            dmsg = "Client Disconnect: (" + str(id) + ") " + str(self.players[id].name)
            self.players[id].disconnect()
            self.groups[group_id].remove_player(id)
            del self.players[id]
            self.log_msg(dmsg)
        except Exception as e:
            self.log_msg(str(e))

        self.log_msg("Explicit garbage collection shows %s undeletable items." % str(gc.collect()))



    def incoming_player_handler(self,xml_dom,data):
        id = xml_dom.getAttribute("id")
        act = xml_dom.getAttribute("action")
        #group_id = xml_dom.getAttribute("group_id")
        group_id = self.players[id].group_id
        ip = self.players[id].ip
        self.log_msg("Player with IP: " + str(ip) + " joined.")

        self.send_to_group(id,group_id,data)
        if act=="new":
            try:
                self.send_player_list(id,group_id)
                self.send_group_list(id)
            except Exception as e:
                traceback.print_exc()
        elif act=="del":
            #print "del player"
            self.del_player(id,group_id)
            self.check_group(id, group_id)
        elif act=="update":
            self.players[id].take_dom(xml_dom)
            self.log_msg(("update", {"id": id,
                                     "name": xml_dom.getAttribute("name"),
                                     "status": xml_dom.getAttribute("status"),
                                     "ip":  str(ip),
                                     "group": xml_dom.getAttribute("group_id"),
                                     "room": xml_dom.getAttribute("name"),
                                     "boot": xml_dom.getAttribute("rm_boot"),
                                     "version": xml_dom.getAttribute("version"),
                                     "ping": xml_dom.getAttribute("time") \
                                     }))


    def strip_body_tags(self, string):
        try:
            bodytag_regex = re.compile('&lt;\/?body(.*?)&gt;')
            string = bodytag_regex.sub('', string)
        except:
            pass
        return string

    def msgTooLong(self, length):
        if length > self.maxSendSize and not self.maxSendSize == 0:
            return True
        return False

    def incoming_msg_handler(self,xml_dom,data):
        to_id = xml_dom.getAttribute("to")
        from_id = xml_dom.getAttribute("from")
        group_id = xml_dom.getAttribute("group_id")
        end = data.find(">")
        msg = data[end+1:]

        if from_id == "0" or len(from_id) == 0:
            print("WARNING!! Message received with an invalid from_id.  Message dropped.")
            return None

        #
        # check for < body to prevent someone from changing the background
        #

        data = self.strip_body_tags(data)

        if group_id == '0' and self.msgTooLong(len(msg) and msg[:5] == '<chat'):
            self.send("Your message was too long, break it up into smaller parts please", from_id, group_id)
            self.log_msg('Message Blocked from Player: ' + self.players[from_id].name + ' attempting to send a message longer then ' + str(self.maxSendSize))
            return

        if msg[:4] == '<map':
            if group_id == '0':
                #attempt to change lobby map. Illegal operation.
                self.players[from_id].self_message('The lobby map may not be altered.')
            elif to_id.lower() == 'all':
                #valid map for all players that is not the lobby.
                self.send_to_group(from_id,group_id,data)
                self.groups[group_id].game_map.init_from_xml(msg)
            else:
                #attempting to send map to specific individuals which is not supported.
                self.players[from_id].self_message('Invalid map message. Message not sent to others.')

        elif msg[:6] == '<boot ':
            self.handle_boot(from_id,to_id,group_id,msg)

        else:
            if to_id == 'all':
                self.send_to_group(from_id,group_id,data)
            else:
                self.players[to_id].outbox.put(data)

    def handle_role(self, act, player, role, given_boot_pwd, group_id):
        if act == "display":
            msg = "<msg to=\"" + player + "\" from=\"0\" group_id=\"" + group_id + "\" />"
            msg += "Displaying Roles<br /><br /><u>Role</u>&nbsp&nbsp&nbsp<u>Player</u><br />"
            keys = list(self.players.keys())
            for m in keys:
                if self.players[m].group_id == group_id:
                    msg += self.players[m].role + " " + self.players[m].name + "<br />"
            self.send(msg,player,group_id)
        elif act == "set":
            try:
                actual_boot_pwd = self.groups[group_id].boot_pwd
                if self.players[player].group_id == group_id:
                    if actual_boot_pwd == given_boot_pwd:
                        self.log_msg( "Administrator passwords match -- changing role")

                        #  Send update role event to all
                        msg = "<role action=\"update\" id=\"" + player  + "\" role=\"" + role + "\" />"
                        self.send_to_group("0", group_id, msg)
                        self.players[player].player.role = role
                    else:
                        #tell the clients password manager the password failed -- SD 8/03
                        pm = "<password signal=\"fail\" type=\"admin\" id=\"" + group_id + "\" data=\"\"/>"
                        self.players[player].outbox.put(pm)
                        self.log_msg( "Administrator passwords did not match")
            except Exception as e:
                print(e)
                print("Error executing the role change")
                print("due to the following exception:")
                traceback.print_exc()
                print("Ignoring boot message")

    def handle_boot(self,from_id,to_id,group_id,msg):
        xml_dom = None
        try:
            given_boot_pwd = None
            try:
                xml_dom = xmlutil.parseXml(msg)
                xml_dom = xml_dom.documentElement
                given_boot_pwd = xml_dom.getAttribute("boot_pwd")

            except:
                print("Error in parse of boot message, Ignoring.")
                print("Exception: ")
                traceback.print_exc()

            try:
                actual_boot_pwd = self.groups[group_id].boot_pwd
                server_admin_pwd = self.groups["0"].boot_pwd

                self.log_msg("Actual boot pwd = " + actual_boot_pwd)
                self.log_msg("Given boot pwd = " + given_boot_pwd)

                if self.players[to_id].group_id == group_id:

                    ### ---CHANGES BY SNOWDOG 4/03 ---
                    ### added boot to lobby code.
                    ### if boot comes from lobby dump player from the server
                    ### any user in-room boot will dump to lobby instead
                    if given_boot_pwd == server_admin_pwd:
                        # Send a message to everyone in the room, letting them know someone has been booted
                        boot_msg = "<msg to='all' from='%s' group_id='%s'/><font color='#FF0000'>Booting '(%s) %s' from server...</font>" % (from_id, group_id, to_id, self.players[to_id].name)

                        self.log_msg("boot_msg:" + boot_msg)

                        self.send_to_group( "0", group_id, boot_msg )
                        time.sleep( 1 )

                        self.log_msg("Booting player " + str(to_id) + " from server.")

                        #  Send delete player event to all
                        self.send_to_group("0",group_id,self.players[to_id].toxml("del"))

                        #  Remove the player from local data structures
                        self.del_player(to_id,group_id)

                        #  Refresh the group data
                        self.check_group(to_id, group_id)

                    elif actual_boot_pwd == given_boot_pwd:
                        # Send a message to everyone in the room, letting them know someone has been booted
                        boot_msg = "<msg to='all' from='%s' group_id='%s'/><font color='#FF0000'>Booting '(%s) %s' from room...</font>" % (from_id, group_id, to_id, self.players[to_id].name)

                        self.log_msg("boot_msg:" + boot_msg)

                        self.send_to_group( "0", group_id, boot_msg )
                        time.sleep( 1 )

                        #dump player into the lobby
                        self.move_player(to_id,"0")

                        #  Refresh the group data
                        self.check_group(to_id, group_id)
                    else:
                        #tell the clients password manager the password failed -- SD 8/03
                        pm = "<password signal=\"fail\" type=\"admin\" id=\"" + group_id + "\" data=\"\"/>"
                        self.players[from_id].outbox.put(pm)
                        print("boot passwords did not match")

            except Exception as e:
                traceback.print_exc()
                self.log_msg('Exception in handle_boot() ' + str(e))

        finally:
            try:
                if xml_dom:
                    xml_dom.unlink()
            except Exception as e:
                traceback.print_exc()
                self.log_msg('Exception in xml_dom.unlink() ' + str(e))


    def admin_kick(self, id, message=""):
        "Kick a player from a server from the console"

        with self.server_lock:
            group_id = self.players[id].group_id
            # Send a message to everyone in the victim's room, letting them know someone has been booted
            boot_msg = "<msg to='all' from='0' group_id='%s'/><font color='#FF0000'>Kicking '(%s) %s' from server... %s</font>" % ( group_id, id, self.players[id].name, str(message))
            self.log_msg("boot_msg:" + boot_msg)
            self.send_to_group( "0", group_id, boot_msg )

            self.log_msg("kicking player " + str(id) + " from server.")
            #  Send delete player event to all
            self.send_to_group("0",group_id,self.players[id].toxml("del"))

            #  Remove the player from local data structures
            self.del_player(id,group_id)

            #  Refresh the group data
            self.check_group(id, group_id)

    def admin_setSendSize(self, sendlen):
        self.maxSendSize = sendlen
        self.log_msg('Max Send Size was set to ' + str(sendlen))

    def remove_room(self, group):
        "removes a group and boots all occupants"
        #check that group id exists
        if group not in self.groups:
            return "Invalid Room Id. Ignoring remove request."

        try:
            keys = self.groups[group].get_player_ids()
            for k in keys:
                self.del_player(k, str(group))
            self.check_group("0", str(group))
        except:
            pass

    def send(self,msg,player,group):
        self.players[player].send(msg,player,group)

    def send_to_all(self,from_id,data):
        try:
            keys = list(self.players.keys())
            for k in keys:
                if k != from_id:
                    self.players[k].outbox.put(data)
        except Exception as e:
            traceback.print_exc()
            self.log_msg("Exception: send_to_all(): " + str(e))

    def send_to_group(self, from_id, group_id, data):
        try:
            keys = self.groups[group_id].get_player_ids()
            for k in keys:
                if k != from_id:
                    self.players[k].outbox.put(data)
        except Exception as e:
            traceback.print_exc()
            self.log_msg("Exception: send_to_group(): " + str(e))

    def send_player_list(self,to_id,group_id):
        try:
            keys = self.groups[group_id].get_player_ids()
            for k in keys:
                if k != to_id:
                    data = self.players[k].toxml('new')
                    self.players[to_id].outbox.put(data)
        except Exception as e:
            traceback.print_exc()
            self.log_msg("Exception: send_player_list(): " + str(e))

    def send_group_list(self, to_id, action="new"):
        try:
            for key in self.groups:
                xml = self.groups[key].toxml(action)
                self.players[to_id].outbox.put(xml)
        except Exception as e:
            self.log_msg("Exception: send_group_list(): (client #"+to_id+") : " + str(e))
            traceback.print_exc()

    def cleanup_disconnected_clients(self):
        """Remove any clients that did not disconnect cleanly."""
        for g in list(self.groups.keys()):
            for p in self.groups[g].get_player_ids():
                if not self.players[p].conn.connected():
                    self.send_to_group(p, g, self.players[p].toxml("del"))
                    self.del_player(p, g)
                    self.check_group(p, g)
