from typing import Any
from ..models.enhanced_websocket import EnhancedWebsocket, CryptodotcomRequestMessage
from .message_types import MessageTypes
from .status import Status


WebsocketBundle = tuple[EnhancedWebsocket, MessageTypes, Status | CryptodotcomRequestMessage]
WebsocketStatusBundle = tuple[EnhancedWebsocket, MessageTypes, Status]
WebsocketMessageBundle = tuple[EnhancedWebsocket, MessageTypes, CryptodotcomRequestMessage]
