from dataclasses import dataclass


@dataclass(frozen=True)
class ElasticSearchConf:
    hosts: list[str]
    user: str
    password: str
    indicator: str
    isActive: bool = True
    maxConnection: int = 10
    sniffOnStart: bool = False
    sniffOnConnectionFail: bool = False
    snifferTimeout: float = 60
    sniffTimeout: float = 10
    isCriticalActive: bool = True
    isErrorActive: bool = True
    isWarningActive: bool = True
    isInfoActive: bool = True
    isDebugActive: bool = False

    def get(self) -> dict:
        return self.__conf()

    def __conf(self) -> dict:
        confDict: dict = self.__confDict()
        any(confDict.update({key: value}) for key, value in self.__dict__.items())
        return confDict

    @classmethod
    def __confDict(cls) -> dict:
        return {
            "hosts": ...,
            "http_auth": ...,
            "max_connection": ...,
            "sniff_on_start": ...,
            "sniff_on_connection_fail": ...,
            "snifferTimeout": ...,
            "sniffTimeout": ...
        }
