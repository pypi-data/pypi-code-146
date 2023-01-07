'''Assetto Corsa Game Server Class'''

import asyncio
import configparser
import hashlib
import json
import logging
import os
import sys
from dataclasses import dataclass, field
from datetime import datetime
import subprocess
from typing import Dict, List

from ac_websocket_server.entries import EntryList
from ac_websocket_server.error import WebsocketsServerError
from ac_websocket_server.grid import Grid
from ac_websocket_server.objects import (DriverInfo, EnhancedJSONEncoder,
                                         EntryInfo, LobbyInfo, SessionInfo)
from ac_websocket_server.lobby import Lobby
from ac_websocket_server.observer import ObserverNotifier
from ac_websocket_server.protocol import Protocol
from ac_websocket_server.watcher import Watcher


@dataclass
class GameServer(ObserverNotifier):
    '''Represents an Assetto Corsa Server.'''
    # pylint: disable=logging-fstring-interpolation, invalid-name

    server_directory: str

    version: str = field(default='n/a', init=False)
    timestamp: str = field(default='n/a', init=False)
    name: str = field(init=False)
    track: str = field(init=False)
    cars: str = field(init=False)
    http_port: int = field(init=False)
    tcp_port: int = field(init=False)
    udp_port: int = field(init=False)
    drivers: Dict[str, DriverInfo] = field(init=False)
    entries: Dict[int, EntryInfo] = field(init=False)
    sessions: Dict[str, SessionInfo] = field(init=False)
    lobby: Lobby = field(init=False)

    def __post_init__(self):

        super().__init__()

        self.__logger = logging.getLogger('ac-ws.game')

        self.drivers = {}
        self.entries = {}
        self.sessions = {}
        self.lobby = None

        if os.path.exists(f'{self.server_directory}/acServer.py'):
            self.__cwd = None
            self.__exe = f'{self.server_directory}/acServer.py'
            self.__hash = None
        else:
            self.__cwd = self.server_directory
            if sys.platform == 'linux':
                self.__exe = f'{self.server_directory}/acServer'
                self.__hash = 'f781ddfe02e68adfa170b28d0eccbbdc'
            else:
                self.__exe = f'{self.server_directory}/acServer.exe'
                self.__hash = '357e1f1fd8451eac2d567e154f5ee537'

        self.parse_server_cfg()
        self.parse_entry_list()

        self.grid = Grid(server_directory=self.server_directory,
                         track=self.track,
                         entry_list=self.entry_list)

        self.lobby = Lobby()

        self.__logfile_stdout: str
        self.__logfile_stderr: str

        self.__watcher_stdout: Watcher

        self.__process: asyncio.subprocess.Process

        self.running = False

    async def consumer(self, message_words: List[str], connection: id = None):
        '''Consume args destined for the server'''

        message_funcs = {'drivers': self.__drivers,
                         'entries': self.__entries,
                         'info': self.__info,
                         'sessions': self.__sessions,
                         'start': self.start,
                         'stop': self.stop,
                         'restart': self.restart}

        if message_funcs.get(message_words[0]):
            await message_funcs[message_words[0]]()

    async def __drivers(self):
        '''Show game drivers info as part of a JSON reply'''
        await self.put(Protocol.success({'drivers': self.drivers}))

    async def __entries(self):
        '''Show game entries info as part of a JSON reply'''
        await self.put(Protocol.success({'entries': self.entries}))

    async def __info(self):
        '''Show game server info as a JSON string'''
        await self.put(Protocol.success({'server': self}))

    async def notify(self, notifier):
        '''Receive a notification of a new message from log watcher or lobby.'''

        message = await notifier.get(self)

        try:
            item = json.loads(message)

            if not item.get('type', None):
                if item.get('data', None):
                    await self.put(Protocol.success(item['data']))
                if item.get('error', None):
                    await self.put(Protocol.error(item['error']))
                return

            if item['type'] == 'LobbyInfo':
                await self.lobby.update(item['body'])
                await self.put(Protocol.success({'lobby': item['body']}))

            if item['type'] == 'ServerInfo':
                self.version = item['body']['version']
                self.timestamp = item['body']['timestamp']
                self.track = item['body']['track']
                self.cars = item['body']['cars']

                await self.put(Protocol.success({'server': item['body']}))

            if item['type'] == 'DriverInfo' and item['body']['msg'] == 'joining':

                body = item['body']
                name = body['name']

                driver_info = DriverInfo()

                driver_info.name = name
                driver_info.host = body['host']
                driver_info.port = body['port']
                driver_info.car = body['car']
                driver_info.guid = body['guid']
                driver_info.ballast = body['ballast']
                driver_info.restrictor = body['restrictor']
                driver_info.msg = body['msg']

                self.drivers[driver_info.name] = driver_info

                self.__logger.debug(f'Driver {name} joining')
                await self.put(Protocol.success({'driver': item['body']}))

            if item['type'] == 'DriverInfo' and item['body']['msg'] == 'leaving':
                body = item['body']
                name = body['name']
                del self.drivers[name]

                self.__logger.debug(f'Driver {name} leaving')
                await self.put(Protocol.success({'driver': item['body']}))

            if item['type'] == 'SessionInfo':

                body = item['body']
                session_type = body['type']

                session_info = SessionInfo()

                session_info.type = session_type
                session_info.laps = body['laps']
                session_info.time = body['time']

                self.sessions[session_type] = session_info

                await self.put(Protocol.success({'sessions': session_info}))

        except json.JSONDecodeError:
            pass

        # await self.put(message)

    def parse_entry_list(self):
        '''Parse entry list file and update attributes'''

        entry_list_file_name = f'{self.server_directory}/cfg/entry_list.ini'

        if not os.path.exists(entry_list_file_name):
            error_message = f'Missing entry_list.ini file in {self.server_directory}'
            self.__logger.error(error_message)
            raise WebsocketsServerError(error_message)

        self.entry_list = EntryList(entry_list_file_name)
        self.entries = self.entry_list.entries

    def parse_server_cfg(self):
        '''Parse server config file and update attributes'''

        server_cfg_file_name = f'{self.server_directory}/cfg/server_cfg.ini'

        if not os.path.exists(server_cfg_file_name):
            error_message = f'Missing server_cfg.ini file in {self.server_directory}'
            self.__logger.error(error_message)
            raise WebsocketsServerError(error_message)

        cfg = configparser.ConfigParser()
        try:
            cfg.read(server_cfg_file_name)

            self.name = cfg['SERVER']['NAME']
            self.cars = cfg['SERVER']['CARS']
            self.track = cfg['SERVER']['TRACK']
            self.http_port = cfg['SERVER']['HTTP_PORT']
            self.tcp_port = cfg['SERVER']['TCP_PORT']
            self.udp_port = cfg['SERVER']['UDP_PORT']

            for session in ['PRACTICE', 'QUALIFY', 'RACE']:
                if cfg.has_section(session):
                    name = cfg[session].get('NAME')
                    time = cfg[session].get('TIME', 0)
                    laps = cfg[session].get('LAPS', 0)
                    self.sessions[name] = SessionInfo(
                        name, laps=laps, time=time)

        except configparser.Error as e:
            raise WebsocketsServerError(e) from e

    async def restart(self):
        ''''Re-start the game server'''
        self.__logger.info('Re-starting game server')
        await self.stop()
        await self.start()

    async def __sessions(self):
        '''Show game sessions info as a JSON string'''
        await self.put(Protocol.success({'sessions': self.sessions}))

    async def start(self):
        '''Start the game server.'''

        # Parse and update status before start (for re-start post __init__)
        try:
            self.parse_server_cfg()
            self.parse_entry_list()
            self.grid.track = self.track
        except WebsocketsServerError as e:
            self.__logger.error('Command failed - configuration error')
            await self.put(Protocol.error(
                msg=f'start command failed - configuration error: {e}'))
            return

        if self.running:
            self.__logger.info('Command ignored - already running')
            await self.put(Protocol.error(
                msg='start command ignored - game already running'))
            return

        if self.__hash:
            try:
                with open(self.__exe, 'rb') as file_to_check:
                    data = file_to_check.read()
                    if self.__hash != hashlib.md5(data).hexdigest():
                        raise WebsocketsServerError(
                            f'{self.__exe} checksum mismatch')
            except FileNotFoundError as e:
                raise WebsocketsServerError(
                    f'{self.__exe} missing') from e

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        self.__logger.info('Starting game server')

        os.makedirs(f'{self.server_directory}/logs/session', exist_ok=True)
        os.makedirs(f'{self.server_directory}/logs/error', exist_ok=True)

        self.__logfile_stdout = f'{self.server_directory}/logs/session/output{timestamp}.log'
        self.__logfile_stderr = f'{self.server_directory}/logs/error/error{timestamp}.log'

        session_file = open(self.__logfile_stdout, 'w', encoding='utf-8')
        error_file = open(self.__logfile_stderr, 'w', encoding='utf-8')

        # Set platform specific options to start process in seperate process group
        kwargs = {}
        if sys.platform.startswith('win'):
            kwargs['creationflags'] = subprocess.CREATE_NEW_PROCESS_GROUP | subprocess.DETACHED_PROCESS | subprocess.CREATE_BREAKAWAY_FROM_JOB
        else:
            kwargs['start_new_session'] = True

        try:
            self.__process = await asyncio.create_subprocess_exec(
                self.__exe, cwd=self.__cwd, stdout=session_file, stderr=error_file, **kwargs)

            self.running = True

            self.__logger.info(f'Process pid is: {self.__process.pid}')
            await self.put(Protocol.success(
                msg='Assetto Corsa server started'))

            self.lobby.subscribe(self)

            self.__watcher_stdout = Watcher(self.__logfile_stdout)
            self.__watcher_stdout.subscribe(self)
            await self.__watcher_stdout.start()

        except PermissionError as e:
            self.__logger.error(f'Process did not start: {e}')
            await self.put(Protocol.error(
                msg='Assetto Corsa server did not start'))
            raise WebsocketsServerError(e) from e

    async def stop(self):
        '''Stop the game server'''

        if not self.running:
            self.__logger.info('Command ignored - not running')
            await self.put(Protocol.error(
                msg='stop command ignored - game not running'))
            return

        self.__logger.info('Stopping game server')

        try:
            self.__process.terminate()

            status_code = await asyncio.wait_for(self.__process.wait(), None)
            self.__logger.info(f'Game server exited with {status_code}')
        except ProcessLookupError as e:
            self.__logger.error('Game server already exited')

        await self.put(Protocol.success(
            msg='Assetto Corsa server stopped'))

        await self.__watcher_stdout.stop()
        self.__watcher_stdout.unsubscribe(self)

        self.lobby.unsubscribe(self)

        self.running = False
