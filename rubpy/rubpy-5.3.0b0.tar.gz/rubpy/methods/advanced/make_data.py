from json import JSONEncoder, JSONDecoder
from ...crypto import Crypto
from typing import Union

class clients:
    android = {
        'app_name': 'Main',
        'app_version': '3.0.9',
        'platform': 'Android',
        'package': 'app.rbmain.a',
        'lang_code': 'fa',
    }
    web = {
        'app_name': 'Main',
        'app_version': '4.1.11',
        'platform': 'Web',
        'package': 'web.rubika.ir',
        'lang_code': 'fa',
    }

class MakeData:
    __slots__ = (
        '__crypto',
        #'__Http',
        'JSONEncoder',
        'JSONDecoder',
        '__key',
    )

    def __init__(self, key: str) -> None:
        self.__crypto = Crypto(key=key)
        #self.__Http = HTTPSConnection()
        self.JSONEncoder = JSONEncoder(ensure_ascii=False).encode
        self.JSONDecoder = JSONDecoder().decode
        self.__key = key

    async def make_data(self,
        method: Union[str, bytes],
        data: Union[str, dict],
        api_version: Union[str, int] = 5,
        client: Union[str, bytes] = 'android',
    ) -> str:
        if type(method) == bytes:
            method = str(method)
        if type(data) == str:
            data = self.JSONDecoder(data)
        if type(api_version) == str:
            api_version = int(api_version)
        if type(client) == bytes:
            client = str(client).lower()
        else:
            client = client.lower()

        if api_version == 5:
            data = {
                'method': method,
                'input': data,
                'client': clients.web if client == 'web' else clients.android,
            }
            data = self.__crypto.encrypt(self.JSONEncoder(data))
            data = {
                'api_version': '5',
                'auth': self.__key,
                'data_enc': data,
            }
            return data

        elif api_version == 4:
            data_enc = self.__crypto.encrypt(self.JSONEncoder(data))
            data = {
                'api_version': '4',
                'auth': self.__key,
                'method': method,
                'client': clients.android if client == 'android' else clients.web,
                'data_enc': data_enc,
            }
            return data