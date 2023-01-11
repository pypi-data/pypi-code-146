from sila2_interop_communication_tester.grpc_stubs import MetadataProvider_pb2


def test_string_metadata_affects_consumer_feature(metadataprovider_stub):
    raw_affected_calls = metadataprovider_stub.Get_FCPAffectedByMetadata_StringMetadata(
        MetadataProvider_pb2.Get_FCPAffectedByMetadata_StringMetadata_Parameters()
    )
    affected_calls = {call.value for call in raw_affected_calls.AffectedCalls}
    assert "org.silastandard/test/MetadataConsumerTest/v1" in affected_calls or (
        "org.silastandard/test/MetadataConsumerTest/v1/Command/EchoStringMetadata" in affected_calls
        and "org.silastandard/test/MetadataConsumerTest/v1/Command/UnpackMetadata" in affected_calls
    )


def test_two_integers_metadata_affects_unpack_metadata(metadataprovider_stub):
    raw_affected_calls = metadataprovider_stub.Get_FCPAffectedByMetadata_TwoIntegersMetadata(
        MetadataProvider_pb2.Get_FCPAffectedByMetadata_TwoIntegersMetadata_Parameters()
    )
    affected_calls = {call.value for call in raw_affected_calls.AffectedCalls}
    assert "org.silastandard/test/MetadataConsumerTest/v1/Command/UnpackMetadata" in affected_calls
