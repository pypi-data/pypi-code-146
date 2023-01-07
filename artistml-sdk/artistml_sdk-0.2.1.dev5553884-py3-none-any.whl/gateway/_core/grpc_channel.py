"""base grpc client / servicer class"""
from __future__ import annotations

from threading import Lock
from typing import Any
from typing import Dict
from typing import Final
from typing import Text
from typing import Type
from typing import TypeVar
from typing import final

import grpc

from ...logger import get_logger

StubClass = TypeVar('StubClass')
LOGGER = get_logger()


@final
class GrpcChannel:
    """GrpcChannel holds gRPC channel to a server and provides the stubs for different services."""
    LOG_TYPE_MODIFY: Final[Text] = "Modify"
    LOG_TYPE_CONNECT: Final[Text] = "Connect"

    __lock: Lock

    __target: Text
    __max_msg_length: int

    __channel: Any
    __stub_pool: Dict[Type, Any]

    def __init__(self):
        self.__lock = Lock()

        self.__target = ""
        self.__max_msg_length = 100 * 2**20
        self.__channel = None
        self.__stub_pool = dict()

    def set_target(self, target: Text) -> GrpcChannel:
        """
        Set target of the channel
        :param target: The target is the hostname and port of the gRPC server you want to connect to
        :type target: Text
        :return: Nothing.
        """
        self.__target = target
        self._on_modified()
        return self

    def get_target(self) -> Text:
        """
        Get current target
        :return: Text.
        """
        return self.__target

    def set_max_msg_length(self, max_msg_length: int) -> GrpcChannel:
        """
        Sets the maximum message length for the channel
        :param max_msg_length: The maximum message length in bytes
        :type max_msg_length: int
        :return: Nothing.
        """
        self.__max_msg_length = max_msg_length
        self._on_modified()
        return self

    def get_max_msg_length(self) -> int:
        """
        Get current max_msg_length
        :return: int.
        """
        return self.__max_msg_length

    def with_stub(self, stub_class: Type[StubClass]) -> StubClass:
        """
        Thread safely obtains the stub corresponding to the channel
        :param stub_class: The stub class that you want to use
        :type stub_class: Type[StubClass]
        :return: A stub class.
        """
        with self.__lock:
            if not self.__stub_pool.__contains__(stub_class):
                if self.__channel is None:
                    self._log(self.LOG_TYPE_CONNECT)
                    self.__channel = grpc.insecure_channel(
                        target=self.__target,
                        options=[
                            ("grpc.max_send_message_length",
                             self.__max_msg_length),
                            ("grpc.max_receive_message_length",
                             self.__max_msg_length),
                        ],
                    )
                self.__stub_pool[stub_class] = stub_class(
                    self.__channel)  # type: ignore
            return self.__stub_pool.get(stub_class)  # type: ignore

    def _on_modified(self):
        """On modified, reset the channel and corresponded stubs"""
        with self.__lock:
            self._log(self.LOG_TYPE_MODIFY)
            self.__channel = None
            self.__stub_pool = dict()

    def _log(self, log_type: Text):
        """
        Log info with type
        :param log_type: The type of log message
        :type log_type: Text
        """
        LOGGER.debug(
            f"{log_type} Server channel {self.__target} [max_msg_length={self.__max_msg_length}]"
        )
