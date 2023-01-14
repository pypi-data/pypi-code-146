from typing import Callable

from reactivex import Observable, operators, compose
from ..models import CryptodotcomResponseMessage

from logging import getLogger

logger = getLogger(__name__)

def wait_for_response(
    message_id: int, timeout: float = 5.0
) -> Callable[
    [Observable[CryptodotcomResponseMessage]], Observable[CryptodotcomResponseMessage]
]:
    def is_match(m: CryptodotcomResponseMessage):
        return m.id == message_id

    return compose(
        operators.filter(is_match),
        operators.do_action(
            on_next=lambda x: logger.debug("[SOCKET] Received matching message %s", x)
        ),
        operators.take(1),
        operators.timeout(timeout),
    )


class RequestResponseError(Exception):
    pass


def _response_ok(response: CryptodotcomResponseMessage):
    if response.code > 40000:
        raise RequestResponseError(response.message)
    return response


def response_ok() -> Callable[
    [Observable[CryptodotcomResponseMessage]], Observable[CryptodotcomResponseMessage]
]:
    return operators.map(_response_ok)
