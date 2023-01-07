"""client for AutomlServer"""
from __future__ import annotations

from typing import final

from ...apis.echo.v1.greeting_service_pb2_grpc import GreetingServiceStub
from .._core import GrpcClient


@final
class EchoClient(GrpcClient):

    def __init__(self):
        super().__init__()

    @property
    def greeting(self) -> GreetingServiceStub:
        return self._stub(GreetingServiceStub)
