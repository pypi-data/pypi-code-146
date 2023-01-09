from dataclasses import dataclass


@dataclass(frozen=True)
class FmtConf:
    fromat: str = ...
    asctime: bool = True
    created: bool = True
    exc_info: bool = True
    filename: bool = True
    funcName: bool = True
    levelname: bool = True
    levelno: bool = True
    lineno: bool = True
    message: bool = True
    module: bool = True
    msecs: bool = True
    msg: bool = True
    name: bool = True
    pathname: bool = True
    process: bool = True
    processName: bool = True
    relativeCreated: bool = True
    stack_info: bool = True
    thread: bool = True
    threadName: bool = True

    def get(self) -> str:
        if bool(self.fromat):
            return self.fromat

        else:
            return self.__createConfStr()

    def __createConfStr(self) -> str:
        loggerFormat = ''

        for key, value in self.__dict__.items():
            if self.__isValid(key, value):
                loggerFormat += '' + f'%({key})s'

        return loggerFormat

    @classmethod
    def __isValid(cls, key, value):
        if key == 'format':
            return None

        return key if bool(value) else None
