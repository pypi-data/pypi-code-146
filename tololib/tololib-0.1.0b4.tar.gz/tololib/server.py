import logging
import socket
from select import select
from threading import Thread
from typing import Any, Optional, Tuple, Union

from .command import Command
from .command_property_map import (
    GET_SETTINGS_COMMAND_PROPERTY_MAP,
    GET_STATUS_COMMAND_PROPERTY_MAP,
    SET_SETTINGS_COMMAND_PROPERTY_MAP,
    SET_STATUS_COMMAND_PROPERTY_MAP,
)
from .const import SettingsMessageLength, StatusMessageLength
from .message import Message
from .message_info import MessageInfo, SettingsInfo, StatusInfo

logger = logging.getLogger(__name__)


class ToloServer(object):
    def __init__(self, address: Optional[str] = None, port: int = 51500) -> None:
        self._address = address
        self._port = port

        self._socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._socket.bind((address, port))
        self._thread: Optional[Thread] = None
        self._keep_running = False

        self._status = StatusInfo()
        self._settings = SettingsInfo()

    def start(self) -> None:
        """Initialize and start the server loop thread.

        Initializes and starts a thread in the background, which handles incoming messages and updates local variables
        accordingly.
        """
        if self._thread is not None:
            raise RuntimeError("server thread already initialized!")

        self._thread = Thread(target=self._thread_loop)
        self._keep_running = True
        self._thread.start()

    def join(self, timeout: Optional[float] = None) -> None:
        """Join the background thread and wait until it is finished.

        Args:
            timeout (float): timeout in seconds
        """
        if self._thread is None:
            raise RuntimeError(
                "server does not have a running thread - did you call start() before?"
            )

        self._thread.join(timeout)

    def run(self) -> None:
        """Shortcut method calling start() and join()"""
        self.start()
        self.join()

    def receive_message(self) -> Tuple[Message, str]:
        """Receive, decode and return a single control message.

        Blocks until a message has received.

        Returns:
            A decoded Message object which contains the received control message.
        """
        raw_bytes, sender = self._socket.recvfrom(4096)
        return Message.from_bytes(raw_bytes), sender

    def send_message(
        self, message: Message, recipient: Union[Tuple[str, int], str]
    ) -> int:
        raw_bytes = bytes(message)
        return self._socket.sendto(raw_bytes, recipient)

    @staticmethod
    def _set_and_get_info(
        message: Message, property_name: Optional[str], info: MessageInfo
    ) -> Message:
        if property_name is None:
            raise ValueError("None value not allowed here")
        setattr(info, property_name, message.data)
        return Message(message.command, message.data, b"\x00")

    @staticmethod
    def _get_info(
        message: Message, property_name: Optional[str], info: MessageInfo
    ) -> Message:
        if property_name is None:
            raise ValueError("None value not allowed here")
        return Message(message.command, getattr(info, property_name), b"\x00")

    def _thread_loop(self) -> None:
        logger.debug("server thread loop started")
        while self._keep_running:
            incoming_data = select([self._socket], [], [], 0.2)
            if incoming_data[0]:
                message, sender = self.receive_message()
                logger.debug("received message %s" % str(message))

                # status request

                if message.command == Command.STATUS:
                    self.send_message(
                        Message(
                            Command.STATUS, StatusMessageLength.RESPONSE, self._status
                        ),
                        sender,
                    )

                # status change commands

                elif message.command in SET_STATUS_COMMAND_PROPERTY_MAP.keys():
                    self.send_message(
                        self._set_and_get_info(
                            message,
                            SET_STATUS_COMMAND_PROPERTY_MAP.get(message.command),
                            self._status,
                        ),
                        sender,
                    )

                # status getter commands

                elif message.command in GET_STATUS_COMMAND_PROPERTY_MAP.keys():
                    self.send_message(
                        self._get_info(
                            message,
                            GET_STATUS_COMMAND_PROPERTY_MAP.get(message.command),
                            self._status,
                        ),
                        sender,
                    )

                # settings request

                elif message.command == Command.SETTINGS:
                    self.send_message(
                        Message(
                            Command.SETTINGS,
                            SettingsMessageLength.RESPONSE,
                            self._settings,
                        ),
                        sender,
                    )

                # settings change commands

                elif message.command in SET_SETTINGS_COMMAND_PROPERTY_MAP.keys():
                    self.send_message(
                        self._set_and_get_info(
                            message,
                            SET_SETTINGS_COMMAND_PROPERTY_MAP.get(message.command),
                            self._settings,
                        ),
                        sender,
                    )

                # settings getter commands

                elif message.command in GET_SETTINGS_COMMAND_PROPERTY_MAP.keys():
                    self.send_message(
                        self._get_info(
                            message,
                            GET_SETTINGS_COMMAND_PROPERTY_MAP.get(message.command),
                            self._settings,
                        ),
                        sender,
                    )

                else:
                    logger.warning("unhandled message: %s" % str(message))

    def stop(self) -> None:
        self._keep_running = False

    def close(self) -> None:
        self._socket.close()

    def get_socket_info(self) -> Any:
        return self._socket.getsockname()

    @property
    def status(self) -> StatusInfo:
        return self._status

    @property
    def settings(self) -> SettingsInfo:
        return self._settings

    def __del__(self) -> None:
        self.close()
