from .credential import Credential
from .networkrequests import Requests


class Bilibili:
    def __init__(self, credential: Credential, proxies=None) -> None:
        self._credential = credential
        self._mid = self._credential.DedeUserID
        self._csrf = self._credential.bili_jct
        self._requests = Requests(credential, proxies).requests
