import asyncio
import datetime
import http
import json
import logging
import typing
from asyncio import Future
from contextlib import asynccontextmanager
from enum import Enum
from http.client import HTTPException
from json import JSONDecodeError

import aiohttp
import munch
from aiohttp import ClientConnectionError, WSMessage, WSServerHandshakeError

from . import model

HOSTNAME = 'sm3.2proof.co.il'
BASE_URL = f'https://{HOSTNAME}'
AUTH_URL = 'https://api.2proof.co.il/oauth/token'
WS_URL = f'wss://{HOSTNAME}/imclient'
DEVICE_URL = f'{BASE_URL}/api/device'

_LOGGER = logging.getLogger(__name__)


class Command(Enum):
    PING = 0
    ACK = 1
    LOGIN = 2
    BYE = 3
    MESSAGE = 4
    REQUEST = 5
    EVENT = 6
    SYNC = 6


class State(Enum):
    INVALID = 0
    LOGOUT = 1
    CLOSED = 2
    CONNECTING = 3
    CONNECT_ERROR = 4
    CONNECTED = 5
    LOGIN_SENT = 6
    LOGIN_ERROR = 7
    LOGGED_IN = 8


class Client:
    def __init__(self, username: str, password: str):
        self._username = username
        self._password = password

        self._token_info = model.TokenInfo(
            access_token='',
            refresh_token='',
            expires_in=0,
        )

        self._devices: typing.Dict[str, model.Device] = dict()
        self._token_expiration = datetime.datetime.now() + datetime.timedelta(seconds=self._token_info.expires_in)

        self._ws = None
        self._state: State = State.INVALID
        self._seq = 0
        self._callback_cache = {}
        self._ping_future: Future = None

        # OAuth params
        self._grant_type = 'password'
        self._scope = 'SCOPE_READ'
        self._client_id = 'app'
        self._client_secret = 'api1234'

    async def authenticate(self):
        try:
            params = {
                'grant_type': self._grant_type,
                'client_id': self._client_id,
                'client_secret': self._client_secret,
                'scope': self._scope,
                'username': self._username,
                'password': self._password,
            }
            async with aiohttp.ClientSession() as session:
                async with session.get(AUTH_URL, params=params) as resp:
                    if resp.status != http.HTTPStatus.OK:
                        text = await resp.text()
                        raise HTTPException(text)

                    data = munch.Munch(await resp.json())
                    self._token_info = model.TokenInfo(
                        access_token=data.access_token,
                        refresh_token=data.refresh_token,
                        expires_in=data.expires_in,
                    )
                    self._token_expiration = datetime.datetime.now() + datetime.timedelta(seconds=self._token_info.expires_in)
                    _LOGGER.debug(f'Token refreshed; valid until {self._token_expiration}')
                    return True
        except HTTPException:
            return False

    async def refresh_device_list(self):
        """Refresh the device list associated with the Client's account"""
        async with self._get_session() as session:
            async with session.get(DEVICE_URL, params=self._auth_params) as resp:
                if resp.status == http.HTTPStatus.OK:
                    data = munch.munchify(await resp.json())

                    for item in data['items']:
                        if item.id not in self._devices:
                            device = model.Device(
                                id=item.status.did,
                                imsi=item.stats.imsi,
                                name=item.name,
                                fw_version=item.stats.fwver,
                                model=item.type,
                                states=item.status.states,
                            )

                            self._devices[item.id] = device

    @property
    def devices(self):
        return self._devices

    async def websocket_close(self):
        if self._ping_future:
            self._ping_future.cancel()
        await self._ws.close()

    async def websocket_updates(self):
        try:
            self._state = State.CONNECTING
            async with aiohttp.ClientSession() as session:
                async with session.ws_connect(WS_URL, params=self._auth_params) as self._ws:
                    self._state = State.CONNECTED

                    await self._ws_login()

                    msg: WSMessage
                    async for msg in self._ws:
                        if msg.type == aiohttp.WSMsgType.TEXT:
                            if msg.data == 'close cmd':
                                await self._ws.close()
                                break
                            else:
                                try:
                                    packet = munch.munchify(json.loads(msg.data))
                                    _LOGGER.debug(f'INCOMING: {packet}')
                                    command = Command(packet[0])
                                    seq = packet[1]
                                    if command == Command.ACK:
                                        if f'seq_{seq}' in self._callback_cache:
                                            callback = self._callback_cache.pop(f'seq_{seq}')
                                            await callback()
                                    elif command == Command.EVENT:
                                        data = packet[2]
                                        device_id = data[1]
                                        device = self._devices.get(device_id)
                                        device.states = data[2].status.states
                                        device.gps = model.GpsData(**data[2].status.gps)
                                        # TODO : change to inner "states[]"
                                    elif command == Command.BYE:
                                        self._state = State.LOGOUT
                                        break
                                except JSONDecodeError as err:
                                    _LOGGER.warning(f'Could not parse JSON: {msg.data}')
                        elif msg.type == aiohttp.WSMsgType.ERROR:
                            break
        except WSServerHandshakeError as err:
            pass
        except ClientConnectionError as err:
            raise err

    @asynccontextmanager
    async def _get_session(self):
        if self._token_expiration <= datetime.datetime.now():
            # If we know token is expired, try to refresh it
            await self.authenticate()

        # Create a session with the fresh access token
        session = aiohttp.ClientSession()
        try:
            yield session
        finally:
            await session.close()

    @property
    def _auth_params(self):
        return {
            'access_token': self._token_info.access_token
        }

    async def _ws_send(self, command, message, callback=None):
        if self._state in [
                State.CONNECTING,
                State.CONNECTED,
                State.LOGIN_SENT,
                State.LOGIN_ERROR,
                State.LOGGED_IN,
        ]:
            packet = [command.value, self._seq, message]
            _LOGGER.debug(f'OUTGOING: {packet}')
            await self._ws.send_json(packet)
            if callback:
                self._callback_cache[f'seq_{self._seq}'] = callback
            self._seq += 1

    async def _ws_login(self):
        async def login_successful():
            await self._ws_subscribe()
            self._state = State.LOGGED_IN
            self._ping_future = asyncio.ensure_future(self._ws_ping())

        try:
            await self._ws_send(Command.LOGIN, {'token': self._token_info.access_token}, login_successful)
            self._state = State.LOGIN_SENT
        except ConnectionResetError:
            self._state = State.LOGIN_ERROR

    async def _ws_ping(self):
        async def pong():
            pass

        await asyncio.sleep(3)
        await self._ws_send(Command.PING, 1, pong)
        if self._state == State.LOGGED_IN:
            self._ping_future = asyncio.ensure_future(self._ws_ping())

    async def _ws_subscribe(self):
        async def subscribed():
            pass

        device_ids = [*self._devices.keys()]
        await self._ws_send(Command.REQUEST, ["u.sub", device_ids], subscribed)
