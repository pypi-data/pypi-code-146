import enum
from typing import List


class Severity(enum.Enum):
    information = 1
    warning = 2
    error = 3
    user_error = 4


class TcError(Exception):
    def __init__(self, message: str, code: int, level: Severity, inner_exceptions: List['InnerException'] = ()):
        self.message = message
        self.code = code
        self.level = level
        self.inner_exceptions = inner_exceptions
        super(TcError, self).__init__()

    def __str__(self):
        return f"[{self.level.name}] Code {self.code} - {self.message}"


class ServiceException(TcError):
    pass


class InvalidCredentialsException(TcError):
    pass


class InternalServerException(TcError):
    pass


class InnerException(TcError):
    pass
