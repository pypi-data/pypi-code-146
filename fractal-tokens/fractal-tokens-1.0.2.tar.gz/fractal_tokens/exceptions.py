class TokenInvalidException(Exception):
    ...

    def __init__(self, message=None):
        if not message:
            message = "The supplied token is invalid!"
        super(TokenInvalidException, self).__init__(message)


class TokenExpiredException(Exception):
    ...

    def __init__(self, message=None):
        if not message:
            message = "The supplied token is expired!"
        super(TokenExpiredException, self).__init__(message)


class NotAllowedException(Exception):
    ...


class InvalidPayloadException(Exception):
    ...


class NoPrivateKeyException(Exception):
    ...


class NoPublicKeyException(Exception):
    ...


class NotImplementedException(Exception):
    ...
