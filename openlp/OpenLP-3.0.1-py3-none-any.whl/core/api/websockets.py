# -*- coding: utf-8 -*-

##########################################################################
# OpenLP - Open Source Lyrics Projection                                 #
# ---------------------------------------------------------------------- #
# Copyright (c) 2008-2023 OpenLP Developers                              #
# ---------------------------------------------------------------------- #
# This program is free software: you can redistribute it and/or modify   #
# it under the terms of the GNU General Public License as published by   #
# the Free Software Foundation, either version 3 of the License, or      #
# (at your option) any later version.                                    #
#                                                                        #
# This program is distributed in the hope that it will be useful,        #
# but WITHOUT ANY WARRANTY; without even the implied warranty of         #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the          #
# GNU General Public License for more details.                           #
#                                                                        #
# You should have received a copy of the GNU General Public License      #
# along with this program.  If not, see <https://www.gnu.org/licenses/>. #
##########################################################################
"""
The :mod:`websockets` module contains the websockets server. This is a server used by remotes to listen for stage
changes from within OpenLP. It uses JSON to communicate with the remotes.
"""
import asyncio
import json
import logging
import uuid

from PyQt5 import QtCore
import time

from websockets import serve

from openlp.core.common.mixins import LogMixin, RegistryProperties
from openlp.core.common.registry import Registry, RegistryBase
from openlp.core.threading import ThreadWorker, run_thread
from openlp.core.api.websocketspoll import WebSocketPoller

USERS = set()
poller = WebSocketPoller()


log = logging.getLogger(__name__)
# Disable DEBUG logs for the websockets lib
ws_logger = logging.getLogger('websockets')
ws_logger.setLevel(logging.ERROR)


class WebSocketWorker(ThreadWorker, RegistryProperties, LogMixin):
    """
    A special Qt thread class to allow the WebSockets server to run at the same time as the UI.
    """
    def start(self):
        """
        Run the worker.
        """
        settings = Registry().get('settings_thread')
        address = settings.value('api/ip address')
        port = settings.value('api/websocket port')
        # Start the event loop
        self.event_loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.event_loop)
        # Create the websocker server
        loop = 1
        self.server = None
        self.queues = set()
        while not self.server:
            try:
                self.server = serve(self.handle_websocket, address, port)
                log.debug('WebSocket server started on {addr}:{port}'.format(addr=address, port=port))
            except Exception:
                log.exception('Failed to start WebSocket server')
                loop += 1
                time.sleep(0.1)
            if not self.server and loop > 3:
                log.error('Unable to start WebSocket server {addr}:{port}, giving up'.format(addr=address, port=port))
        if self.server:
            # If the websocket server exists, start listening
            try:
                self.event_loop.run_until_complete(self.server)
                self.event_loop.run_forever()
            except Exception:
                log.exception('Failed to start WebSocket server')
            finally:
                self.event_loop.close()
        self.quit.emit()

    def stop(self):
        """
        Stop the websocket server
        """
        try:
            self.event_loop.call_soon_threadsafe(self.event_loop.stop)
        except BaseException:
            pass

    async def handle_websocket(self, websocket, path):
        """
        Handle web socket requests and return the state information
        Waits for information to come over queue

        :param websocket: request from client
        :param path: determines the endpoints supported - Not needed
        """
        client_id = uuid.uuid4() if log.getEffectiveLevel() == logging.DEBUG else 0
        log.debug(f'(client_id={client_id}) WebSocket handle_websocket connection')
        queue = asyncio.Queue()
        await self.register(websocket, client_id, queue)
        try:
            reply = poller.get_state()
            if reply:
                await self.send_reply(websocket, client_id, reply)
            while True:
                done, pending = await asyncio.wait(
                    [asyncio.create_task(queue.get()), asyncio.create_task(websocket.wait_closed())],
                    return_when=asyncio.FIRST_COMPLETED
                )
                for task in pending:
                    task.cancel()
                # If there is a new item in client's queue, await_result will contain an item, if the connection is
                # closed, it will be None.
                await_result = done.pop().result()
                if await_result is not None:
                    await self.send_reply(websocket, client_id, await_result)
                else:
                    break
        finally:
            await self.unregister(websocket, client_id, queue)

    async def register(self, websocket, client_id, queue):
        """
        Register Clients
        :param websocket: The client details
        :param queue: The Command Queue
        :return:
        """
        log.debug(f'(client_id={client_id}) WebSocket handler register')
        USERS.add(websocket)
        self.queues.add(queue)
        log.debug('WebSocket clients count: {client_count}'.format(client_count=len(USERS)))

    async def unregister(self, websocket, client_id, queue):
        """
        Unregister Clients
        :param websocket: The client details
        :return:
        """
        USERS.remove(websocket)
        self.queues.remove(queue)
        log.debug(f'(client_id={client_id}) WebSocket handler unregister')
        log.debug('WebSocket clients count: {client_count}'.format(client_count=len(USERS)))

    async def send_reply(self, websocket, client_id, reply):
        json_reply = json.dumps(reply).encode()
        await websocket.send(json_reply)
        log.debug(f'(client_id={client_id}) WebSocket send reply: {json_reply}')

    def add_state_to_queues(self, state):
        """
        Inserts the state in each connection message queue
        :param state: OpenLP State
        """
        for queue in self.queues.copy():
            self.event_loop.call_soon_threadsafe(queue.put_nowait, state)


class WebSocketServer(RegistryBase, RegistryProperties, QtCore.QObject, LogMixin):
    """
    Wrapper round a server instance
    """
    def __init__(self):
        """
        Initialise the WebSockets server
        """
        super(WebSocketServer, self).__init__()
        self.worker = None

    def bootstrap_post_set_up(self):
        self.start()

    def start(self):
        """
        Starts the WebSockets server
        """
        if self.worker is None and not Registry().get_flag('no_web_server'):
            self.worker = WebSocketWorker()
            run_thread(self.worker, 'websocket_server')
            poller.poller_changed.connect(self.handle_poller_signal)
            # Only hooking poller signals after all UI is available
            Registry().register_function('bootstrap_completion', self.try_poller_hook_signals)

    @QtCore.pyqtSlot()
    def handle_poller_signal(self):
        if self.worker is not None:
            self.worker.add_state_to_queues(poller.get_state())

    def try_poller_hook_signals(self):
        try:
            poller.hook_signals()
        except Exception:
            log.error('Failed to hook poller signals!')

    def close(self):
        """
        Closes the WebSocket server and detach associated signals
        """
        try:
            poller.poller_changed.disconnect(self.handle_poller_signal)
            poller.unhook_signals()
            self.worker.stop()
        finally:
            self.worker = None
