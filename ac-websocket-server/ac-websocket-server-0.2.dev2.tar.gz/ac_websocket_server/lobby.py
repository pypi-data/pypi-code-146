'''Assetto Corsa Lobby Class'''

import aiohttp
import asyncio
import logging
import os
import sys
from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List

from ac_websocket_server.objects import LobbyInfo
from ac_websocket_server.observer import Notifier
from ac_websocket_server.protocol import Protocol


@dataclass
class Lobby(Notifier):
    '''Represents an Assetto Corsa Lobby'''

    connected: bool = field(default=False, init=False)
    since: datetime = field(default=None, init=False)
    url_register: str = field(default=None, init=False)
    url_ping: str = field(default=None, init=False)

    def __post_init__(self):

        super().__init__()

        self._logger = logging.getLogger('ac-ws.lobby')

    async def consumer(self, message_words: List[str], connection: id = None):
        '''Consume args destined for the lobby'''

        message_funcs = {'info': self._info,
                         'restart': self._restart}

        if message_funcs.get(message_words[0]):
            await message_funcs[message_words[0]]()

    async def _info(self):
        '''Send lobby information'''
        await self.put(Protocol.success({'lobby': self}))

    async def _restart(self):
        '''Re-start the lobby connection'''

        self._logger.info('Re-regestering to lobby')
        async with aiohttp.ClientSession() as session:

            async with session.get(self.url_register) as resp:
                text = await resp.text()
                if resp.status == 200 and 'ERROR' not in text:
                    self._logger.info('Successfully re-registered to lobby')
                    await self.put(Protocol.success(msg=text))
                else:
                    self._logger.error(
                        f'Failed attempt to re-register with lobby: {text}')
                    await self.put(Protocol.error(msg=text))

    async def update(self, lobby_info: LobbyInfo):
        '''Update lobby info'''

        if lobby_info['connected'] and not self.connected:
            self.connected = True
            self.since = datetime.now()

        if not lobby_info['connected'] and self.connected:
            self.connected = False
            self.since = datetime.now()
            await self._restart()

        if lobby_info['url_register']:
            self.url_register = lobby_info['url_register']

        if lobby_info['url_ping']:
            self.url_ping = lobby_info['url_ping']
