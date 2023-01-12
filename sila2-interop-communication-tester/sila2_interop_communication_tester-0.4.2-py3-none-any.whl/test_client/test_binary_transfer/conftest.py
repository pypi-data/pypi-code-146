"""Pytest setup"""
from pytest import fixture

from ...grpc_stubs.BinaryTransferTest_pb2_grpc import BinaryTransferTestStub


@fixture(scope="session")
def binarytransfertest_stub(channel) -> BinaryTransferTestStub:
    return BinaryTransferTestStub(channel)
