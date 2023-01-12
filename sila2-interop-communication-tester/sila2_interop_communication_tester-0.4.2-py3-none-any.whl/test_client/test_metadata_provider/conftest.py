"""Pytest setup"""
from pytest import fixture

from ...grpc_stubs.MetadataProvider_pb2_grpc import MetadataProviderStub


@fixture(scope="session")
def metadataprovider_stub(channel) -> MetadataProviderStub:
    return MetadataProviderStub(channel)
