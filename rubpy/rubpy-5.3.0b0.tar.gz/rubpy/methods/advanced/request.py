from ...connections import HTTPSConnection
from .make_data import MakeData
from ...crypto import Crypto
from typing import Union

class Request:
    def __init__(self, key: Union[str, bytes]) -> None:
        if type(key) == bytes:
            key = str(key)
        self.__MakeData = MakeData(key)
        self.__Http = HTTPSConnection()
        self.__Crypto = Crypto(key)

    async def Make(self,
        method: Union[str, bytes],
        data: Union[str, dict],
        api_version: Union[str, int] = 5,
        client: Union[str, bytes] = 'android',
    ) -> str:
        json = await self.__MakeData.make_data(method, data, api_version, client)
        while True:
            response = await self.__Http.Post(json=json)
            if response.status == 200:
                response = response.content.decode('UTF-8')
                return await self.response(response, api_version)
            else:
                continue

    async def response(self, res: str, api_version: int) -> dict:
        res = self.__MakeData.JSONDecoder(res)
        if api_version == 5:
            res = self.__Crypto.decrypt(res.get('data_enc'))
            res = self.__MakeData.JSONDecoder(res)
            if res.get('status') == 'OK':
                return res.get('data')