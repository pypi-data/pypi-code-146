"""Pytest setup"""
from pytest import fixture

from ...grpc_stubs.ErrorHandlingTest_pb2_grpc import ErrorHandlingTestStub


@fixture(scope="session")
def errorhandlingtest_stub(channel) -> ErrorHandlingTestStub:
    return ErrorHandlingTestStub(channel)
