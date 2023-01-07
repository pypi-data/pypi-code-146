from .user import User as User
from .utils import Credential
from .video import Video as Video
from .dynamic import Dynamic as Dynamic


class Anbiliapi:
    def __init__(self, credential: Credential, proxies=None) -> None:
        self.__credential = credential
        self.__proxies = proxies

    def get_user(self, proxies=None) -> User:
        return User(credential=self.__credential, proxies=self.__get_proxies(proxies))

    def get_video(self, aid: int = None, bid: str = None, proxies=None) -> Video:
        return Video(credential=self.__credential, bid=bid, aid=aid, proxies=self.__get_proxies(proxies))

    def get_dynamic(self, did: int, proxies=None, ):
        return Dynamic(self.__credential, did=did, proxies=self.__get_proxies(proxies))

    def __get_proxies(self, proxies):
        return self.__proxies if proxies else proxies
