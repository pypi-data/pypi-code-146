class AuthException(Exception):
    """Raised on auth exception"""


class ServerException(Exception):
    """Raised on issue with server response"""

    def __init__(self, msg, args):
        super.__init__(args)
        self.msg = msg

    def __str__(self) -> str:
        return "There was an issue with the server response: \n\n{}".format(self.msg)


class BadResourceClass(Exception):
    """Raised when a bad resource class is pass"""

    def __init__(self, msg, args):
        super.__init__(args)
        self.msg = msg

    def __str__(self) -> str:
        return "Resource class must be one of [AR, AP, RN, LN, or AF]. Received: {}".format(
            self.msg
        )


class BadHttpMethod(Exception):
    """Raised when passed a bad http verb"""

    def __init__(self, msg: str, *args: object) -> None:
        super().__init__(*args)
        self.msg = msg

    def __str__(self) -> str:
        return f"Bad HTTP method passed, Received {msg}"


class ClientException(Exception):
    """Raised on 400 HTTP errors"""


class AuthorizationException(Exception):
    """Raised on 403 HTTP response"""


class NotFoundException(Exception):
    """Raised on 404 HTTP Response"""


class NoPrivateKey(Exception):
    """RAISED if RSA Key is required but not provided"""
