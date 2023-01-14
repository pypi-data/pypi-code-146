from ..connection import wait_for_response
from ..models import CryptodotcomResponseMessage, EnhancedWebsocket, CryptodotcomRequestMessage
from reactivex import Observable
from ..events import MethodName

from returns.curry import curry

@curry
def get_user_balance(messages: Observable[CryptodotcomResponseMessage], ws: EnhancedWebsocket) -> Observable[CryptodotcomResponseMessage]:
    return messages.pipe(
        wait_for_response(
            ws.send_message(
                CryptodotcomRequestMessage(MethodName.USER_BALANCE)
            ),
            2.0
        )
    )
