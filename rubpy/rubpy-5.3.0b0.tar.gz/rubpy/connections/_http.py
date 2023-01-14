from httpcore import (
    AsyncConnectionPool as AsyncConnectionPool,
    RemoteProtocolError as RemoteProtocolError,
    Response as Response,
    ReadError as ReadError,
    ConnectError as ConnectError,
) # Python3.7+
from typing import (
    Union as Union,
    Optional as Optional,
    Mapping as Mapping,
)
from json.encoder import JSONEncoder
from random import randint


class HTTPSConnection:
    '''
    This class is used for HTTPS connections

    import asyncio

    Http = HTTPSConnection()

    async def Main():
        res = await Http.Get('https://example.com/')
            print(res)
        res = await Http.Post('https://example.com/', json={})
            print(res)
        res = await Http.Stream('GET', 'https://example.com/')
            print(res)

    asyncio.run(Main())
    '''

    __slots__ = (
        '__URL',
        '__HTTP',
        'json_encoder',
    )

    def __init__(self) -> None:
        URL = 'https://messengerg2c{}.iranlms.ir/'.format(randint(1, 200))
        self.__URL = URL
        self.__HTTP = AsyncConnectionPool()
        self.json_encoder = JSONEncoder(ensure_ascii=False).encode

    async def Get(self,
        url: Union[str, bytes],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Response:
        while True:
            try:
                return await self.__HTTP.request(
                    method='GET',
                    url=url,
                    headers=headers,
                )
            except ReadError:
                continue
            except ConnectError:
                continue
            except RemoteProtocolError:
                continue

    async def Post(self, json: Optional[dict] = None) -> Response:
        url = self.__URL
        content = self.json_encoder(o=json).encode(encoding='UTF-8')

        while True:
            try:
                res = await self.__HTTP.request(
                    method='POST',
                    url=url,
                    content=content,
                    headers={'Content-Type': 'application/json'},
                )
                return res
            except ReadError:
                self.updateURL()
                continue
            except ConnectError:
                self.updateURL()
                continue
            except RemoteProtocolError:
                self.updateURL()
                continue

    def updateURL(self) -> None:
        self.__URL = 'https://messengerg2c{}.iranlms.ir/'.format(randint(1, 200))

    async def Stream(self,
        method: Union[str, bytes],
        url: Union[str, bytes],
        headers: Optional[Mapping[str, str]] = None,
    ) -> bytes:
        while 1:
            try:
                async with self.__HTTP.stream(method=method, url=url, headers=headers) as response:
                    async for chunk in response.aiter_stream():
                        yield chunk
            except ReadError:
                continue
            except ConnectError:
                continue
            except RemoteProtocolError:
                continue