"""
MIT License

Copyright (c) 2020 DashIO-Connect

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
import logging
import threading
import time

import shortuuid
import zmq

from .constants import CONNECTION_PUB_URL
from .device import Device


class Connection(threading.Thread):
    """Base Connection"""

    def add_device(self, device: Device):
        """Add a device to the connection

        Parameters
        ----------
        device : dashio.Device
            Add a device to the connection.
        """
        pass
        #self.rx_zmq_sub.setsockopt_string(zmq.SUBSCRIBE, device.zmq_pub_id)

    
    def __init__(self, connection_type: str, context: zmq.Context=None):
        """
        """

        threading.Thread.__init__(self, daemon=True)
        self.context = context or zmq.Context.instance()
        self.connection_uuid = shortuuid.uuid()
        self.b_connection_uuid = self.connection_uuid.encode('utf-8')

        self.running = True

        self.start()
        threading.Thread(target=self._zconf_start_zmq).start()
        time.sleep(1)

    def close(self):
        """Close the connection."""
        self.running = False

    def _connect_remote_device(self, msg: dict):
        pass

    def _disconnect_remote_device(self, msg: dict):
        pass
    
    def _service_internal_messaging(self, msg: dict):
        pass
        

    def _service_external_messages(self,  msg: dict):
        pass

    def run(self):
        self.tcpsocket = self.context.socket(zmq.STREAM)

        tx_zmq_pub = self.context.socket(zmq.PUB)
        tx_zmq_pub.bind(CONNECTION_PUB_URL.format(id=self.connection_uuid))

        self.rx_zmq_sub = self.context.socket(zmq.SUB)
        # Subscribe on ALL, and my connection
        self.rx_zmq_sub.setsockopt_string(zmq.SUBSCRIBE, "ALL")
        self.rx_zmq_sub.setsockopt_string(zmq.SUBSCRIBE, "DVCE_CNCT")
        self.rx_zmq_sub.setsockopt_string(zmq.SUBSCRIBE, "DVCE_DCNCT")
        self.rx_zmq_sub.setsockopt_string(zmq.SUBSCRIBE, self.connection_uuid)
        # rx_zmq_sub.setsockopt_string(zmq.SUBSCRIBE, "ANNOUNCE")

        self.tcpsocket.bind(self.ext_url)
        self.tcpsocket.set(zmq.SNDTIMEO, 5)

        rx_zconf_pull = self.context.socket(zmq.PULL)
        rx_zconf_pull.bind("inproc://zconf")

        poller = zmq.Poller()
        poller.register(self.tcpsocket, zmq.POLLIN)
        poller.register(self.rx_zmq_sub, zmq.POLLIN)
        poller.register(rx_zconf_pull, zmq.POLLIN)

    
        logging.debug("TCP Send Announce")
        tx_zmq_pub.send_multipart([b'COMMAND', b'1', b"send_announce"])
        #tcp_id = self.tcpsocket.recv(flags=zmq.NOBLOCK)
        #self.tcpsocket.recv(flags=zmq.NOBLOCK)  # empty data here

        while self.running:
            try:
                socks = dict(poller.poll(50))
            except zmq.error.ContextTerminated:
                break
            if self.tcpsocket in socks:
                self._service_tcp_messages(tx_zmq_pub)
            if self.rx_zmq_sub in socks:
                self._service_device_messaging()
            if rx_zconf_pull in socks:
                self._service_zconf_message(rx_zconf_pull)

        for tcp_id in self.socket_ids:
            self.tcpsocket.send(tcp_id, zmq.SNDMORE)
            self.tcpsocket.send(b'', zmq.NOBLOCK)

        self.tcpsocket.close()
        tx_zmq_pub.close()
        self.rx_zmq_sub.close()
        rx_zconf_pull.close()
