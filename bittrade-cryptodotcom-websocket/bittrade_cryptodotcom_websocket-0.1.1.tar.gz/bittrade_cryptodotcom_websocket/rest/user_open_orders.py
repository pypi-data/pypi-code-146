from ..connection import wait_for_response
from ..models import CryptodotcomResponseMessage, EnhancedWebsocket, CryptodotcomRequestMessage
from reactivex import Observable
from ..events import MethodName

from returns.curry import curry

@curry
def get_user_open_orders(messages: Observable[CryptodotcomResponseMessage], ws: EnhancedWebsocket, instrument: str = "") -> Observable[CryptodotcomResponseMessage]:
    params = {"instrument_name": instrument} if instrument else {}
    return messages.pipe(
        wait_for_response(
            ws.send_message(
                CryptodotcomRequestMessage(MethodName.GET_OPEN_ORDERS, params=params)
            )
        )
    )
