"""Pytest setup"""
from pytest import fixture

from ...grpc_stubs.MetadataConsumerTest_pb2_grpc import MetadataConsumerTestStub


@fixture(scope="session")
def metadataconsumertest_stub(channel) -> MetadataConsumerTestStub:
    return MetadataConsumerTestStub(channel)
