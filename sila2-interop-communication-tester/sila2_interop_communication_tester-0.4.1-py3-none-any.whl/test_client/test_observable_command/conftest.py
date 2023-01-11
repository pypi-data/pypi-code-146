"""Pytest setup"""
from pytest import fixture

from ...grpc_stubs.ObservableCommandTest_pb2_grpc import ObservableCommandTestStub


@fixture(scope="session")
def observablecommandtest_stub(channel) -> ObservableCommandTestStub:
    return ObservableCommandTestStub(channel)
