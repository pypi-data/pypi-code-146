'''Assetto Corsa Websocket Server Class'''

import asyncio
import logging
import os
from typing import List
import websockets

from ac_websocket_server.connection import WebSocketConnection
from ac_websocket_server.debug import monitor_tasks
from ac_websocket_server.constants import HOST, PORT
from ac_websocket_server.error import WebsocketsServerError
from ac_websocket_server.game import GameServer
from ac_websocket_server.grid import Grid
from ac_websocket_server.handlers import handler
from ac_websocket_server.observer import Observer
from ac_websocket_server.protocol import Protocol
from ac_websocket_server.tracker import TrackerServer

EXTRA_DEBUG = False


class WebsocketsServer():
    '''Represents an Assetto Corsa WebSocket Server.

    Allows control of an Assetto Corsa server with a websockets interface.'''
    # pylint: disable=logging-fstring-interpolation

    def __init__(self,
                 server_directory: str = None,
                 host: str = HOST,
                 port: int = PORT
                 ) -> None:

        self._logger = logging.getLogger('ac-ws.ws-server')

        if EXTRA_DEBUG:
            asyncio.get_event_loop().create_task(monitor_tasks())

        self._connections: List[WebSocketConnection] = []

        self.host = host
        self.port = port

        if not server_directory:
            self.server_directory = os.getcwd()
        else:
            self.server_directory = server_directory

        try:
            self.game = GameServer(server_directory=self.server_directory)
        except WebsocketsServerError as error:
            self._logger.error(f'Fatal error {error}')
            raise

        try:
            self.tracker = TrackerServer(f'{self.server_directory}/stracker')
        except WebsocketsServerError as error:
            self._logger.error(f'Unable to start tracker: {error}')

        self.stop_server: asyncio.Future = None

    async def broadcast(self, msg: str):
        '''Broadcast message to all connected websockets.'''

        for connection in self._connections:
            await connection.send(msg)

    async def handler(self, websocket):
        '''ACWS handler function for websocket connection'''

        connection = WebSocketConnection(server=self, websocket=websocket)

        self._connections.append(connection)

        await connection.send(Protocol.success(
            msg=f'Welcome to the Assetto Corsa WebSocket server running at {self.host}:{self.port}'))

        await handler(websocket, connection.consumer, connection.producer)

        connection.close()

    async def start(self):
        '''Start the websocket server'''

        try:

            self._logger.info('Starting websocket server')

            self.stop_server = asyncio.Future()

            async with websockets.serve(self.handler, self.host, self.port):
                await self.stop_server

            self._logger.info('Stopping websocket server')

        except KeyboardInterrupt:
            self._logger.info('Interupting the server')

    async def stop(self):
        '''Stop the websocket server'''

        self.stop_server.set_result(True)

    async def shutdown(self, message: str = None, connection: id = None):
        '''
        Shutdown the ACWS server.

        Note that running AC servers and trackers will NOT be stopped.
        '''

        await self.broadcast(Protocol.success(
            msg=f'Shutting down the WebSocket server running at {self.host}:{self.port}'))

        self._logger.info('Shutting down the server')
        await self.stop()
