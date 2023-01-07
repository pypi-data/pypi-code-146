"""client for AutomlServer"""
from __future__ import annotations

from typing import final

from ...apis.tag.v1.tag_service_pb2_grpc import TagServiceStub
from .._core import GrpcClient


@final
class TagClient(GrpcClient):

    def __init__(self):
        super().__init__()

    @property
    def tag(self) -> TagServiceStub:
        return self._stub(TagServiceStub)
