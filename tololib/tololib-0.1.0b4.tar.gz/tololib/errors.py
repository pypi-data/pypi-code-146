class CommandError(BaseException):
    pass


class CommandParseError(CommandError):
    pass


class ResponseTimedOutError(BaseException):
    pass
