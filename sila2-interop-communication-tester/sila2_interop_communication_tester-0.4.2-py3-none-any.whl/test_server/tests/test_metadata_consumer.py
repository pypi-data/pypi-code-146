from sila2_interop_communication_tester.grpc_stubs import MetadataProvider_pb2


def test_echo_string_metadata_called_with_abc(server_calls):
    calls = server_calls["MetadataConsumerTest.EchoStringMetadata"]
    assert any(
        call.successful and call.metadata[MetadataProvider_pb2.Metadata_StringMetadata].StringMetadata.value == "abc"
        for call in calls
    )


def test_unpack_metadata_called_with_abc_123_456(server_calls):
    calls = server_calls["MetadataConsumerTest.UnpackMetadata"]
    assert any(
        call.successful
        and call.metadata[MetadataProvider_pb2.Metadata_StringMetadata].StringMetadata.value == "abc"
        and call.metadata[MetadataProvider_pb2.Metadata_TwoIntegersMetadata].TwoIntegersMetadata.FirstInteger.value
        == 123
        and call.metadata[MetadataProvider_pb2.Metadata_TwoIntegersMetadata].TwoIntegersMetadata.SecondInteger.value
        == 456
        for call in calls
    )
