from __future__ import annotations

from typing import final

from ...apis.assoc.v1.assoc_service_pb2_grpc import AssocServiceStub
from .._core import GrpcClient


@final
class AssocClient(GrpcClient):

    def __init__(self):
        super().__init__()

    @property
    def assoc(self) -> AssocServiceStub:
        return self._stub(AssocServiceStub)
