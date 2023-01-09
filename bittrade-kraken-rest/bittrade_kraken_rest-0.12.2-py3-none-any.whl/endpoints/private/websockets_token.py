from pydantic.dataclasses import dataclass

from bittrade_kraken_rest.connection.observable import prepare_private
from bittrade_kraken_rest.connection.result import send_and_map_to_result


@dataclass
class GetWebsocketsTokenResult:
    expires: int
    token: str


def get_websockets_token_request():
    """
    Get websockets token
    :return:
    """
    return prepare_private(url="/0/private/GetWebSocketsToken")


def get_websockets_token_result():
    return send_and_map_to_result(GetWebsocketsTokenResult)


__all__ = [
    "get_websockets_token_request",
    "get_websockets_token_result",
    "GetWebsocketsTokenResult",
]
