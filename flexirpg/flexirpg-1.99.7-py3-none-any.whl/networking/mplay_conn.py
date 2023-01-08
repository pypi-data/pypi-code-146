# FlexiRPG -- network connection to a peer
#
# Copyright (C) 2010 David Vrabel
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
import socket
import struct
import threading
import time
import zlib

MESSAGE_HEADER_LEN = struct.calcsize('i')

class connection(object):
    CONNECTED = 0
    DISCONNECTING = 1

    def __init__(self, sock, inbox, outbox):
        self._state      = self.CONNECTED
        self._peer_state = self.CONNECTED
        self.sock   = sock
        self.inbox  = inbox
        self.outbox = outbox

        self.connect_time      = time.time()
        self.last_message_time = self.connect_time

        self._recv_thread = recv_thread(self)
        self._send_thread = send_thread(self)

        self._recv_thread.start()
        self._send_thread.start()

    def disconnect(self):
        if self._state == self.CONNECTED:
            self._state = self.DISCONNECTING
            self.outbox.put("")

        self._send_thread.join()
        self._recv_thread.join()
        self.sock.close()

    def connected(self):
        return self._state == self.CONNECTED and self._peer_state == self.CONNECTED

    def _update_idle_time(self):
        self.last_message_time = time.time()

class recv_thread(threading.Thread):
    def __init__(self, conn):
        threading.Thread.__init__(self)
        self.conn = conn

    def run(self):
        try:
            self._recv_messages();
        except (IOError, socket.error):
            pass
        self.conn._peer_state = self.conn.DISCONNECTING
        self.conn.inbox.put("")

    def _recv_messages(self):
        while True:
            message = self._recv_message()
            self.conn.inbox.put(message)
            self.conn._update_idle_time()

    def _recv_message(self):
        """Receive a complete message."""
        header = self._recv(MESSAGE_HEADER_LEN)
        (length,) = struct.unpack('!i', header)
        body = self._recv(length)
        return zlib.decompress(body).decode('utf-8')

    def _recv(self, length):
        """Receive exactly 'length' bytes."""
        data = b""
        offset = 0
        while offset != length:
            frag = self.conn.sock.recv(length - offset)
            received = len(frag)
            if received <= 0:
                raise IOError("Remote closed the connection")
            offset += received
            data += frag
        return data

class send_thread(threading.Thread):
    def __init__(self, conn):
        threading.Thread.__init__(self)
        self.conn = conn

    def run(self):
        try:
            self._send_messages();
        except socket.error:
            pass
        try:
            self.conn.sock.shutdown(socket.SHUT_RDWR)
        except:
            pass

    def _send_messages(self):
        while True:
            message = self.conn.outbox.get(block=True);
            if message == "":
                break
            self._send_message(message)
            self.conn._update_idle_time()

    def _send_message(self, message):
        packet = zlib.compress(message.encode('utf-8'))
        packet = struct.pack('!i', len(packet)) + packet

        sent = 0
        while sent < len(packet):
            sent += self.conn.sock.send(packet[sent:])
