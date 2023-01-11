from sila2_interop_communication_tester.grpc_stubs import (
    MetadataConsumerTest_pb2,
    MetadataProvider_pb2,
    SiLAFramework_pb2,
)
from sila2_interop_communication_tester.test_client.helpers.error_handling import raises_invalid_metadata_error
from sila2_interop_communication_tester.test_client.helpers.utils import pack_metadata


def test_echo_string_metadata_fails_without_string_metadata(metadataconsumertest_stub):
    with raises_invalid_metadata_error():
        metadataconsumertest_stub.EchoStringMetadata(MetadataConsumerTest_pb2.EchoStringMetadata_Parameters())


def test_echo_string_metadata_fails_with_empty_string_metadata_message(metadataconsumertest_stub):
    with raises_invalid_metadata_error():
        metadataconsumertest_stub.EchoStringMetadata.with_call(
            request=MetadataConsumerTest_pb2.EchoStringMetadata_Parameters(),
            metadata=pack_metadata(
                MetadataProvider_pb2.Metadata_StringMetadata(),
            ),
        )


def test_echo_string_metadata_works_with_string_metadata(metadataconsumertest_stub):
    response, call = metadataconsumertest_stub.EchoStringMetadata.with_call(
        request=MetadataConsumerTest_pb2.EchoStringMetadata_Parameters(),
        metadata=pack_metadata(
            MetadataProvider_pb2.Metadata_StringMetadata(StringMetadata=SiLAFramework_pb2.String(value="abc"))
        ),
    )

    assert response.ReceivedStringMetadata.value == "abc"
