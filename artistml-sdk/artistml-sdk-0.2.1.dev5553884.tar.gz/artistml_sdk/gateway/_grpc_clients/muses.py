from __future__ import annotations

from typing import final

from ...apis.muses.v1.component_service_pb2_grpc import ComponentServiceStub
from ...apis.muses.v1.flow_service_pb2_grpc import FlowServiceStub
from ...apis.muses.v1.method_service_pb2_grpc import MethodServiceStub
from ...apis.muses.v1.run_service_pb2_grpc import RunServiceStub
from .._core import GrpcClient


@final
class MusesClient(GrpcClient):

    def __init__(self):
        super().__init__()

    @property
    def component(self) -> ComponentServiceStub:
        return self._stub(ComponentServiceStub)

    @property
    def method(self) -> MethodServiceStub:
        return self._stub(MethodServiceStub)

    @property
    def flow(self) -> FlowServiceStub:
        return self._stub(FlowServiceStub)

    @property
    def run(self) -> RunServiceStub:
        return self._stub(RunServiceStub)
