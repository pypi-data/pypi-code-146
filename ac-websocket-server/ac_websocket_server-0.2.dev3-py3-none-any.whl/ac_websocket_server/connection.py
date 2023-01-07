'''Assetto Corsa Websocket Connection Class'''

import asyncio
import logging
import os
from typing import Any
import websockets

from ac_websocket_server.observer import Observer, ObserverNotifier
from ac_websocket_server.protocol import Protocol

EXTRA_DEBUG = False


class WebSocketConnection(ObserverNotifier):
    '''Represents an individual webscocket connection'''

    def __init__(self, server: Any = None, websocket: Any = None) -> None:

        super().__init__()

        self._logger = logging.getLogger('ac-ws.ws-connection')

        self._server = server

        if self._server.game:
            self._server.game.subscribe(self)
            self._server.game.grid.subscribe(self)
        if self._server.tracker:
            self._server.tracker.subscribe(self)

        self.websocket = websocket

    def close(self):
        '''Close and cleanup subscriptions'''
        if self._server.game:
            self._server.game.unsubscribe(self)
            self._server.game.grid.unsubscribe(self)
        if self._server.tracker:
            self._server.tracker.unsubscribe(self)

    async def consumer(self, message):
        '''ACWS consumer function for all received messages from client'''
        # pylint: disable=logging-fstring-interpolation, line-too-long

        if message == b'\n':
            return

        self._logger.debug(f'Received message: {message}')

        if isinstance(message, bytes):
            message_string = str(message.strip(), 'utf-8')
        else:
            message_string = message.strip()

        message_words = message_string.split()
        message_funcs = {'grid': self._server.game.grid.consumer,
                         'lobby': self._server.game.lobby.consumer,
                         'server': self._server.game.consumer,
                         'shutdown': self._server.shutdown,
                         'tracker': self._server.tracker.consumer}

        if message_funcs.get(message_words[0]) and len(message_words) > 1:
            await message_funcs[message_words[0]](message_words[1:], connection=self)
            return

        await self.send(Protocol.error(
            msg=f'Received unrecognised message: {message}'))

    async def producer(self):
        '''Pull a message off the queue and send on websocket'''
        # pylint: disable=logging-fstring-interpolation

        data = await self._notifier_queue.get()
        self._logger.debug(f'Sending message: {data}')
        if data:
            return data
        return ''

    async def send(self, msg: str):
        '''Send a message on the websocket by pushing it to notify queue'''

        await self._notifier_queue.put(msg)
