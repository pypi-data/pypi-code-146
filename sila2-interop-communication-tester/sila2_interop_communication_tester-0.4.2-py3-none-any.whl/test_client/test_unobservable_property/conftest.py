"""Pytest setup"""
from pytest import fixture

from ...grpc_stubs.UnobservablePropertyTest_pb2_grpc import UnobservablePropertyTestStub


@fixture(scope="session")
def unobservablepropertytest_stub(channel) -> UnobservablePropertyTestStub:
    return UnobservablePropertyTestStub(channel)
