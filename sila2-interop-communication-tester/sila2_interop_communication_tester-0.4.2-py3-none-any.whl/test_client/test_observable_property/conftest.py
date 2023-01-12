"""Pytest setup"""
from pytest import fixture

from ...grpc_stubs.ObservablePropertyTest_pb2_grpc import ObservablePropertyTestStub


@fixture(scope="session")
def observablepropertytest_stub(channel) -> ObservablePropertyTestStub:
    return ObservablePropertyTestStub(channel)
