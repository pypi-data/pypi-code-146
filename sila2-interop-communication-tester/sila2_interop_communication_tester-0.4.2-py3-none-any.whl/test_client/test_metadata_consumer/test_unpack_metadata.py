from sila2_interop_communication_tester.grpc_stubs import SiLAFramework_pb2
from sila2_interop_communication_tester.grpc_stubs.MetadataConsumerTest_pb2 import UnpackMetadata_Parameters
from sila2_interop_communication_tester.grpc_stubs.MetadataProvider_pb2 import (
    Metadata_StringMetadata,
    Metadata_TwoIntegersMetadata,
)
from sila2_interop_communication_tester.test_client.helpers.error_handling import raises_invalid_metadata_error
from sila2_interop_communication_tester.test_client.helpers.utils import pack_metadata


def test_unpack_metadata_fails_without_metadata(metadataconsumertest_stub):
    with raises_invalid_metadata_error():
        metadataconsumertest_stub.UnpackMetadata(UnpackMetadata_Parameters())


def test_unpack_metadata_fails_without_two_integers_metadata(metadataconsumertest_stub):
    with raises_invalid_metadata_error():
        metadataconsumertest_stub.UnpackMetadata.with_call(
            request=UnpackMetadata_Parameters(),
            metadata=pack_metadata(Metadata_StringMetadata(StringMetadata=SiLAFramework_pb2.String(value="abc"))),
        )


def test_unpack_metadata_fails_without_string_metadata(metadataconsumertest_stub):
    with raises_invalid_metadata_error():
        metadataconsumertest_stub.UnpackMetadata.with_call(
            request=UnpackMetadata_Parameters(),
            metadata=pack_metadata(
                Metadata_TwoIntegersMetadata(
                    TwoIntegersMetadata=Metadata_TwoIntegersMetadata.TwoIntegersMetadata_Struct(
                        FirstInteger=SiLAFramework_pb2.Integer(value=123),
                        SecondInteger=SiLAFramework_pb2.Integer(value=456),
                    )
                )
            ),
        )


def test_unpack_metadata_fails_with_empty_string_metadata(metadataconsumertest_stub):
    with raises_invalid_metadata_error():
        metadataconsumertest_stub.UnpackMetadata.with_call(
            request=UnpackMetadata_Parameters(),
            metadata=pack_metadata(
                Metadata_StringMetadata(),
                Metadata_TwoIntegersMetadata(
                    TwoIntegersMetadata=Metadata_TwoIntegersMetadata.TwoIntegersMetadata_Struct(
                        FirstInteger=SiLAFramework_pb2.Integer(value=123),
                        SecondInteger=SiLAFramework_pb2.Integer(value=456),
                    )
                ),
            ),
        )


def test_unpack_metadata_fails_with_empty_two_integers_metadata(metadataconsumertest_stub):
    with raises_invalid_metadata_error():
        metadataconsumertest_stub.UnpackMetadata.with_call(
            request=UnpackMetadata_Parameters(),
            metadata=pack_metadata(
                Metadata_StringMetadata(StringMetadata=SiLAFramework_pb2.String(value="abc")),
                Metadata_TwoIntegersMetadata(),
            ),
        )


def test_unpack_metadata_fails_with_missing_integers_metadata(metadataconsumertest_stub):
    with raises_invalid_metadata_error():
        metadataconsumertest_stub.UnpackMetadata.with_call(
            request=UnpackMetadata_Parameters(),
            metadata=pack_metadata(
                Metadata_StringMetadata(StringMetadata=SiLAFramework_pb2.String(value="abc")),
                Metadata_TwoIntegersMetadata(
                    TwoIntegersMetadata=Metadata_TwoIntegersMetadata.TwoIntegersMetadata_Struct()
                ),
            ),
        )


def test_unpack_metadata_fails_with_missing_first_integer_metadata(metadataconsumertest_stub):
    with raises_invalid_metadata_error():
        metadataconsumertest_stub.UnpackMetadata.with_call(
            request=UnpackMetadata_Parameters(),
            metadata=pack_metadata(
                Metadata_StringMetadata(StringMetadata=SiLAFramework_pb2.String(value="abc")),
                Metadata_TwoIntegersMetadata(
                    TwoIntegersMetadata=Metadata_TwoIntegersMetadata.TwoIntegersMetadata_Struct(
                        SecondInteger=SiLAFramework_pb2.Integer(value=456),
                    )
                ),
            ),
        )


def test_unpack_metadata_fails_with_missing_second_integer_metadata(metadataconsumertest_stub):
    with raises_invalid_metadata_error():
        metadataconsumertest_stub.UnpackMetadata.with_call(
            request=UnpackMetadata_Parameters(),
            metadata=pack_metadata(
                Metadata_StringMetadata(StringMetadata=SiLAFramework_pb2.String(value="abc")),
                Metadata_TwoIntegersMetadata(
                    TwoIntegersMetadata=Metadata_TwoIntegersMetadata.TwoIntegersMetadata_Struct(
                        FirstInteger=SiLAFramework_pb2.Integer(value=123),
                    )
                ),
            ),
        )


def test_unpack_metadata_works_with_string_and_two_integers_metadata(metadataconsumertest_stub):
    response, call = metadataconsumertest_stub.UnpackMetadata.with_call(
        request=UnpackMetadata_Parameters(),
        metadata=pack_metadata(
            Metadata_StringMetadata(StringMetadata=SiLAFramework_pb2.String(value="abc")),
            Metadata_TwoIntegersMetadata(
                TwoIntegersMetadata=Metadata_TwoIntegersMetadata.TwoIntegersMetadata_Struct(
                    FirstInteger=SiLAFramework_pb2.Integer(value=123),
                    SecondInteger=SiLAFramework_pb2.Integer(value=456),
                )
            ),
        ),
    )

    assert response.ReceivedString.value == "abc"
    assert response.FirstReceivedInteger.value == 123
    assert response.SecondReceivedInteger.value == 456
