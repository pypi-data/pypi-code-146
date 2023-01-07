'''
Assetto Corsa Log Watcher.

Ideas and code from: https://github.com/kuralabs/logserver/blob/master/server/server.py
'''

import asyncio
import json
import logging
import re

import aiofiles

from ac_websocket_server.objects import DriverInfo, EnhancedJSONEncoder, LobbyInfo, ServerInfo, SessionInfo, Message, MessageType
from ac_websocket_server.observer import Notifier
from ac_websocket_server.task_logger import create_task

TAIL_DELAY = 1


class Watcher(Notifier):
    '''Represents a watcher for AC logfiles.
    Parses log files and sends messages to send_queue.'''

    def __init__(self, filename: str) -> None:
        '''Create Watcher instance for filename.'''

        self._logger = logging.getLogger('ac-ws.watcher')

        self._filename = filename

        self._readlines_task: asyncio.Task

        self._lobby_info = LobbyInfo()
        self._driver_info = DriverInfo()
        self._server_info = ServerInfo()
        self._session_info = SessionInfo()

        super().__init__()

    async def parse_lines(self, _file, lines):
        '''Parse lines of logfile and send messages to observer.'''
        # pylint: disable=invalid-name, pointless-string-statement

        for line in lines:

            '''Parse for server info - see tests/watcher_test.py for details.'''

            m = re.compile(
                r'^Assetto Corsa Dedicated Server (.*)').match(line)
            if m:
                self._server_info.version = m.group(1)

            m = re.compile(
                r'^(\d{4}-\d{2}-\d{2} .*)$').match(line)
            if m:
                self._server_info.timestamp = m.group(1)

            m = re.compile(
                r'^TRACK=(.*)').match(line)
            if m:
                self._server_info.track = m.group(1)

            m = re.compile(
                r'^CARS=(.*)').match(line)
            if m:
                self._server_info.cars = m.group(1)
                await self.put(json.dumps(Message(type=MessageType.SERVER_INFO,
                                                  body=self._server_info),
                                          cls=EnhancedJSONEncoder))
                continue

            '''Parse for session info - see tests/watcher_test.py for details.'''

            m = re.compile(
                r'^SENDING session name : (.*)').match(line)
            if m:
                self._session_info.type = m.group(1)

            m = re.compile(
                r'^SENDING session time : (.*)').match(line)
            if m:
                self._session_info.time = int(m.group(1))

            m = re.compile(
                r'^SENDING session laps : (.*)').match(line)
            if m:
                self._session_info.laps = int(m.group(1))
                await self.put(json.dumps(Message(type=MessageType.SESSION_INFO,
                                                  body=self._session_info),
                                          cls=EnhancedJSONEncoder))
                continue

            '''Parse for driver info - see tests/watcher_test.py for details.'''

            m = re.compile(
                r'^NEW PICKUP CONNECTION from  (.*):(\d*)').match(line)
            if m:
                self._driver_info = DriverInfo()
                self._driver_info.host = m.group(1)
                self._driver_info.port = int(m.group(2))

            m = re.compile(
                r'^Looking for available slot by name for GUID (\d*) (.*)').match(line)
            if m:
                self._driver_info.guid = m.group(1)
                self._driver_info.car = m.group(2)

            m = re.compile(
                r'^Slot found at index (\d*)').match(line)
            if m:
                self._driver_info.slot = int(m.group(1))

            m = re.compile(
                r'^DRIVER: (.*) \[.*$').match(line)
            if m:
                self._driver_info.name = m.group(1)
                self._driver_info.msg = 'joining'
                await self.put(json.dumps(Message(type=MessageType.DRIVER_INFO,
                                                  body=self._driver_info),
                                          cls=EnhancedJSONEncoder))
                continue

            '''Parse for driver info - see tests/watcher_test.py for details.'''

            m = re.compile(
                r'^Clean exit, driver disconnected:  (.*) \[.*$').match(line)
            if m:
                self._driver_info = DriverInfo(name=m.group(1), msg='leaving')
                await self.put(json.dumps(Message(type=MessageType.DRIVER_INFO,
                                                  body=self._driver_info),
                                          cls=EnhancedJSONEncoder))
                continue

            '''
            CALLING http://93.57.10.21/lobby.ashx/register?name=SNRL+AC+%231&port=9601&tcp_port=9601&max_clients=12&track=rt_autodrom_most&cars=ks_mazda_mx5_cup&timeofday=-16&sessions=1,2,3&durations=7200,600,8&password=1&version=202&pickup=1&autoclutch=1&abs=1&tc=1&stability=0&legal_tyres=&fixed_setup=0&timed=0&extra=0&pit=0&inverted=0
            '''
            m = re.compile(
                r'^CALLING (.*)$').match(line)
            if m:

                self._lobby_info = LobbyInfo(url_register=m.group(1))
                await self.put(json.dumps(Message(type=MessageType.LOBBY_INFO,
                                                  body=self._lobby_info),
                                          cls=EnhancedJSONEncoder))
                continue

            '''
            CONNECTED TO LOBBY
            '''
            m = re.compile(
                r'^CONNECTED TO LOBBY$').match(line)
            if m:
                self._lobby_info.connected = True
                await self.put(json.dumps(Message(type=MessageType.LOBBY_INFO,
                                                  body=self._lobby_info),
                                          cls=EnhancedJSONEncoder))

            '''
            SENDING http://93.57.10.21/lobby.ashx/ping?session=2&timeleft=600&port=9601&clients=0&track=rt_autodrom_most&pickup=1
            '''
            m = re.compile(
                r'^SENDING (.*lobby.ashx\/ping.*)$').match(line)
            if m:
                self._lobby_info.url_ping = m.group(1)
                await self.put(json.dumps(Message(type=MessageType.LOBBY_INFO,
                                                  body=self._lobby_info),
                                          cls=EnhancedJSONEncoder))
                continue
            '''
            ERROR,SERVER NOT REGISTERED WITH LOBBY - PLEASE RESTART
            ERROR - RESTART YOUR SERVER TO REGISTER WITH THE LOBBY
            '''

            m = re.compile(
                r'^ERROR.*REGISTER.*LOBBY$').match(line)
            if m:
                self._lobby_info.connected = False
                await self.put(json.dumps(Message(type=MessageType.LOBBY_INFO,
                                                  body=self._lobby_info),
                                          cls=EnhancedJSONEncoder))

    async def readlines(self):
        '''Co-routine to be run as a task to read lines from logfile.'''
        # pylint: disable=invalid-name, logging-fstring-interpolation

        self._logger.debug(f'Started watching {self._filename}: ')

        async with aiofiles.open(self._filename, mode='r') as f:

            while True:
                line = await f.readline()
                if line:
                    await self.parse_lines(self._filename, [line])
                else:
                    await asyncio.sleep(TAIL_DELAY)

        self._logger.debug(f'Stopped watching {self._filename}: ')

    async def start(self):
        '''Start monitoring logfile'''

        self._readlines_task = create_task(self.readlines(),
                                           logger=self._logger,
                                           message='readlines() raised an exception')

    async def stop(self):
        '''Stop monitoring logfile'''

        self._readlines_task.cancel()
