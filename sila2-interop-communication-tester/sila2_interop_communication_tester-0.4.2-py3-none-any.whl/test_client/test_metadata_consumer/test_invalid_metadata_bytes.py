from sila2_interop_communication_tester.grpc_stubs import (
    MetadataConsumerTest_pb2,
    MetadataProvider_pb2,
    SiLAFramework_pb2,
)
from sila2_interop_communication_tester.test_client.helpers.error_handling import raises_invalid_metadata_error

INVALID_PROTO_BYTES = b"\x07\x00"  # hex 07 is an invalid first byte for the protobuf wire format
INVALID_STRING_METADATA = (
    "sila-org.silastandard-test-metadataprovider-v1-metadata-stringmetadata-bin",
    INVALID_PROTO_BYTES,
)
INVALID_TWO_INTEGERS_METADATA = (
    "sila-org.silastandard-test-metadataprovider-v1-metadata-twointegersmetadata-bin",
    INVALID_PROTO_BYTES,
)
VALID_STRING_METADATA = (
    "sila-org.silastandard-test-metadataprovider-v1-metadata-stringmetadata-bin",
    MetadataProvider_pb2.Metadata_StringMetadata(
        StringMetadata=SiLAFramework_pb2.String(value="abc")
    ).SerializeToString(),
)
VALID_TWO_INTEGERS_METADATA_METADATA = (
    "sila-org.silastandard-test-metadataprovider-v1-metadata-twointegersmetadata-bin",
    MetadataProvider_pb2.Metadata_TwoIntegersMetadata(
        TwoIntegersMetadata=MetadataProvider_pb2.Metadata_TwoIntegersMetadata.TwoIntegersMetadata_Struct(
            FirstInteger=SiLAFramework_pb2.Integer(value=123),
            SecondInteger=SiLAFramework_pb2.Integer(value=456),
        )
    ).SerializeToString(),
)


def test_invalid_string_metadata_bytes_are_rejected_by_echo_string_metadata(metadataconsumertest_stub):
    with raises_invalid_metadata_error():
        metadataconsumertest_stub.EchoStringMetadata.with_call(
            request=MetadataConsumerTest_pb2.EchoStringMetadata_Parameters(),
            metadata=(INVALID_STRING_METADATA,),
        )


def test_invalid_string_metadata_bytes_are_rejected_by_unpack_metadata(metadataconsumertest_stub):
    with raises_invalid_metadata_error():
        metadataconsumertest_stub.UnpackMetadata.with_call(
            request=MetadataConsumerTest_pb2.UnpackMetadata_Parameters(),
            metadata=(
                INVALID_STRING_METADATA,
                VALID_TWO_INTEGERS_METADATA_METADATA,
            ),
        )


def test_invalid_two_integers_metadata_bytes_are_rejected_by_unpack_metadata(metadataconsumertest_stub):
    with raises_invalid_metadata_error():
        metadataconsumertest_stub.UnpackMetadata.with_call(
            request=MetadataConsumerTest_pb2.UnpackMetadata_Parameters(),
            metadata=(
                VALID_STRING_METADATA,
                INVALID_TWO_INTEGERS_METADATA,
            ),
        )
