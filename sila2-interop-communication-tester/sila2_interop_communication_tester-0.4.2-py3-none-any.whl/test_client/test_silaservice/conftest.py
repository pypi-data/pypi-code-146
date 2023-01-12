"""Pytest setup"""
from os.path import dirname, join

from pytest import fixture
from xmlschema import XMLSchema

from ...grpc_stubs.SiLAService_pb2_grpc import SiLAServiceStub


@fixture(scope="session")
def silaservice_stub(channel) -> SiLAServiceStub:
    return SiLAServiceStub(channel)


@fixture(scope="session")
def feature_definition_xml_schema() -> XMLSchema:
    return XMLSchema(join(dirname(__file__), "..", "..", "resources", "xsd", "FeatureDefinition.xsd"))
