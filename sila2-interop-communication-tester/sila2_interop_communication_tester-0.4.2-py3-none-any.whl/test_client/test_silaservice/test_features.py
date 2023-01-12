import re

import xmlschema

from sila2_interop_communication_tester.grpc_stubs import SiLAFramework_pb2, SiLAService_pb2
from sila2_interop_communication_tester.grpc_stubs.SiLAService_pb2_grpc import SiLAServiceStub
from sila2_interop_communication_tester.test_client.helpers.error_handling import (
    raises_defined_execution_error,
    raises_validation_error,
)


def _get_implemented_features(silaservice_stub: SiLAServiceStub) -> list[str]:
    """Call SiLAService.Get_ImplementedFeatures, unpack responses"""
    raw_responses: SiLAService_pb2.Get_ImplementedFeatures_Responses = silaservice_stub.Get_ImplementedFeatures(
        SiLAService_pb2.Get_ImplementedFeatures_Parameters()
    )
    return [feature_id.value for feature_id in raw_responses.ImplementedFeatures]


def _get_feature_definition(silaservice_stub: SiLAServiceStub, feature_identifier: str) -> str:
    """Call SiLAService.GetFeatureDefinition(feature_identifier), unpack responses"""
    raw_feature_definition: SiLAService_pb2.GetFeatureDefinition_Responses = silaservice_stub.GetFeatureDefinition(
        SiLAService_pb2.GetFeatureDefinition_Parameters(
            FeatureIdentifier=SiLAFramework_pb2.String(value=feature_identifier)
        )
    )
    return raw_feature_definition.FeatureDefinition.value


def test_implemented_features_returns_fully_qualified_identifiers(silaservice_stub):
    originator = category = r"[a-z][a-z0-9\.]{0,254}"
    identifier = r"[A-Z][a-zA-Z0-9]*"
    major_version = r"v\d+"
    feature_id_regex = "/".join((originator, category, identifier, major_version))

    assert all(re.fullmatch(feature_id_regex, f) for f in _get_implemented_features(silaservice_stub))


def test_implemented_features_contains_silaservice(silaservice_stub):
    assert "org.silastandard/core/SiLAService/v1" in _get_implemented_features(silaservice_stub)


def test_get_feature_definition_knows_all_implemented_features(silaservice_stub):
    for feature_id in _get_implemented_features(silaservice_stub):
        _get_feature_definition(silaservice_stub, feature_id)


def test_get_feature_definition_returns_feature_definitions(silaservice_stub, feature_definition_xml_schema):
    for feature_id in _get_implemented_features(silaservice_stub):
        feature_definition = _get_feature_definition(silaservice_stub, feature_id)
        assert xmlschema.validate(feature_definition, feature_definition_xml_schema) is None


def test_get_feature_definition_validates_parameter(silaservice_stub):
    with raises_validation_error(
        "org.silastandard/core/SiLAService/v1/Command/GetFeatureDefinition/Parameter/FeatureIdentifier"
    ):
        _get_feature_definition(silaservice_stub, "SiLAService")


def test_get_feature_definition_with_unknown_feature_parameter_raises_unimplemented_feature(silaservice_stub):
    with raises_defined_execution_error(
        "org.silastandard/core/SiLAService/v1/DefinedExecutionError/UnimplementedFeature"
    ):
        _get_feature_definition(silaservice_stub, "org.silastandard/core/SiLAService/v2")


def test_get_feature_definition_with_empty_message_raises_validation_error(silaservice_stub):
    with raises_validation_error(
        "org.silastandard/core/SiLAService/v1/Command/GetFeatureDefinition/Parameter/FeatureIdentifier"
    ):
        silaservice_stub.GetFeatureDefinition(SiLAService_pb2.GetFeatureDefinition_Parameters())
