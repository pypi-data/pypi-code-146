from enum import StrEnum, auto

from aiosox.utils import CamelStrEnum


class ApiServerProtocol(StrEnum):

    WS = auto()
    WSS = auto()
    HTTP = auto()
    HTTPS = auto()
    SIO = auto()


class ApiSecuritySchemesType(CamelStrEnum):
    """
    https://www.asyncapi.com/docs/specifications/v2.3.0#securitySchemeObjectType
    """

    USER_PASSWORD = auto()
    API_KEY = auto()
    X509 = auto()
    SYMMETRIC_ENCRYPTION = auto()
    ASYMMETRIC_ENCRYPTION = auto()
    HTTP_API_KEY = auto()
    HTTP = auto()
    OAUTH2 = auto()
    OPENID_CONNECT = auto()
    PLAIN = auto()
    SCRAM_SHA256 = auto()
    SCRAM_SHA512 = auto()
    GSSAPI = auto()


class ApiSecuritySchemeLocation(CamelStrEnum):
    """
    https://www.asyncapi.com/docs/specifications/v2.3.0#securitySchemeObject
    """

    user = auto()
    password = auto()
    apiKey = auto()
    query = auto()
    header = auto()
    cookie = auto()
    httpApiKey = auto()


class JSONReference(StrEnum):
    LOCAL = auto()
    REMOTE = auto()
    URL = auto()


class HttpOperationBindingType(StrEnum):
    request = auto()
    response = auto()


class WebSocketsMethod(StrEnum):
    get = auto()
    post = auto()
