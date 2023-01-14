from logging import getLogger
from reactivex.subject import BehaviorSubject
import dataclasses

import orjson
import websocket

from .request import CryptodotcomRequestMessage

logger = getLogger(__name__)


class EnhancedWebsocket:
    socket: websocket.WebSocketApp
    _id = 0

    def __init__(self, socket: websocket.WebSocketApp):
        self.socket = socket

    def send_message(self, message: CryptodotcomRequestMessage) -> int:
        return self.send_json(dataclasses.asdict(message))

    def send_json(self, message: dict):
        self._id += 1
        if "params" in message and not message["params"]:
            del message["params"]
        if not message["id"]:
            message["id"] = self._id
        as_bytes = orjson.dumps(message)
        logger.debug("[SOCKET] Sending json to socket: %s", as_bytes)
        self.socket.send(as_bytes)
        return message["id"]

EnhancedWebsocketBehaviorSubject = BehaviorSubject[EnhancedWebsocket]

__all__ = [
    "EnhancedWebsocket",
    "EnhancedWebsocketBehaviorSubject",
]
