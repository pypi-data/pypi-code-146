from typing import Callable, Dict, List, cast, overload

from reactivex import Observable, compose, operators, timer

from bittrade_cryptodotcom_websocket.connection.bundle import WebsocketStatusBundle

from ..connection.connection_operators import filter_socket_status_only
from ..connection.generic import WEBSOCKET_MESSAGE, WEBSOCKET_STATUS, WebsocketBundle
from ..connection.status import Status
from ..development import debug_operator
from ..models import CryptodotcomResponseMessage, EnhancedWebsocket


def _is_message(message: WebsocketBundle) -> bool:
    return message[1] == WEBSOCKET_MESSAGE


def message_only() -> Callable[
    [Observable[WebsocketBundle] | Observable[WebsocketStatusBundle]],
    Observable[Status | dict],
]:
    return operators.map(lambda x: x[2])


def keep_messages_only() -> Callable[
    [Observable[WebsocketBundle]], Observable[CryptodotcomResponseMessage]
]:
    return compose(
        operators.filter(_is_message),
        message_only(),
        operators.map(lambda x: CryptodotcomResponseMessage(**cast(dict, x))),
    )


def keep_status_only() -> Callable[[Observable[WebsocketBundle]], Observable[Status]]:
    return compose(
        filter_socket_status_only(),
        message_only(),
    )  # type: ignore


def filter_new_socket_only() -> Callable[
    [Observable[WebsocketBundle]], Observable[EnhancedWebsocket]
]:
    def wait(x: EnhancedWebsocket):
        return timer(1.0).pipe(operators.map(lambda _: x))

    return compose(
        operators.map(lambda x: x[0]),
        operators.distinct_until_changed(),
        debug_operator("CONNECTION BEFORE WAIT"),
        operators.map(wait),
        operators.switch_latest(),
        debug_operator("CONNECTION AFTER WAIT"),
    )
