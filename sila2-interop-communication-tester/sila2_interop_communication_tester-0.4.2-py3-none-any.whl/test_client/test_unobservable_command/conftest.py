"""Pytest setup"""
from pytest import fixture

from ...grpc_stubs.UnobservableCommandTest_pb2_grpc import UnobservableCommandTestStub


@fixture(scope="session")
def unobservablecommandtest_stub(channel) -> UnobservableCommandTestStub:
    return UnobservableCommandTestStub(channel)
