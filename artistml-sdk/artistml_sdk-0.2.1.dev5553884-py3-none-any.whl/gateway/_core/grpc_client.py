from __future__ import annotations

import abc
from typing import Type

from .grpc_channel import GrpcChannel
from .grpc_channel import StubClass


# The GrpcClient class is used to connect to the gRPC server.
# Extends GrpcClient to fill your ideas!
class GrpcClient:
    __metaclass__ = abc.ABCMeta

    __channel_holder: GrpcChannel

    def __init__(self, *args, **kwargs):
        self.__channel_holder = GrpcChannel()

    def set_endpoint(self, endpoint: str, *args, **kwargs) -> GrpcClient:
        self.__channel_holder.set_target(endpoint)
        return self

    def get_endpoint(self) -> str:
        """
        Get current endpoint
        :return: str.
        """
        return self.__channel_holder.get_target()

    def set_max_msg_length(self, max_msg_length: int) -> GrpcClient:
        self.__channel_holder.set_max_msg_length(max_msg_length)
        return self

    def get_max_msg_length(self) -> int:
        """
        Get current max_msg_length
        :return: int.
        """
        return self.__channel_holder.get_max_msg_length()

    def _stub(self, stub_class: Type[StubClass], *args, **kwargs) -> StubClass:
        return self.__channel_holder.with_stub(stub_class)
