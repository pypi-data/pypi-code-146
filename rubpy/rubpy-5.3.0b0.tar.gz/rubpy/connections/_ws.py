from websockets import (
    connect as connect,
    ConnectionClosed as ConnectionClosed,
)
from json import (
    JSONEncoder as JSONEncoder,
    JSONDecoder as JSONDecoder,
)
from typing import AsyncGenerator
from ..crypto import Crypto
from random import choice


class WebSocket:
    __slots__ = (
        'JSONEncoder',
        'JSONDecoder',
        'crypto',
        '__data',
    )

    def __init__(self, key: str) -> None:
        self.JSONEncoder = JSONEncoder().encode
        self.JSONDecoder = JSONDecoder().decode
        self.crypto = Crypto(key)
        self.__data = {'api_version': '5'}
        self.__data['auth'] = key

    async def handSnake(self) -> AsyncGenerator:
        URI = await self.URI()
        data = self.__data
        data['data'] = ''
        data['method'] = 'handShake'
        async with connect(URI) as websocket:
            await websocket.send(self.JSONEncoder(data).encode('UTF-8'))
            async for message in websocket:
                await websocket.send(b'{}')
                recv = self.JSONDecoder(message)
                if recv.get('status') == 'OK':
                    continue
                else:
                    recv['data_enc'] = self.JSONDecoder(self.crypto.decrypt(recv.get('data_enc')))
                    yield recv

    async def URI(self) -> str:
        URIS = (
            'wss://jsocket5.iranlms.ir:80',
            'wss://msocket1.iranlms.ir:80',
            'wss://jsocket1.iranlms.ir:80',
            'wss://jsocket2.iranlms.ir:80',
            'wss://jsocket3.iranlms.ir:80',
            'wss://jsocket4.iranlms.ir:80',
            'wss://nsocket6.iranlms.ir:80',
            'wss://nsocket7.iranlms.ir:80',
            'wss://nsocket8.iranlms.ir:80',
            'wss://nsocket9.iranlms.ir:80',
            'wss://nsocket10.iranlms.ir:80',
            'wss://nsocket11.iranlms.ir:80',
            'wss://nsocket12.iranlms.ir:80',
            'wss://nsocket13.iranlms.ir:80',
        )
        return choice(URIS)