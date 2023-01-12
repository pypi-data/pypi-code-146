import uuid

from sila2_interop_communication_tester.grpc_stubs import SiLAFramework_pb2
from sila2_interop_communication_tester.grpc_stubs.BinaryTransferTest_pb2 import (
    EchoBinaryAndMetadataString_Parameters,
    Get_FCPAffectedByMetadata_String_Parameters,
    Metadata_String,
)
from sila2_interop_communication_tester.grpc_stubs.SiLABinaryTransfer_pb2 import CreateBinaryRequest
from sila2_interop_communication_tester.test_client.helpers.binary_transfer import download_binary, upload_binary
from sila2_interop_communication_tester.test_client.helpers.error_handling import (
    raises_invalid_metadata_error,
    raises_validation_error,
)
from sila2_interop_communication_tester.test_client.helpers.utils import pack_metadata

INVALID_PROTO_BYTES = b"\x07\x00"  # hex 07 is an invalid first byte for the protobuf wire format
INVALID_STRING_METADATA = (
    "sila-org.silastandard-test-binarytransfertest-v1-metadata-string-bin",
    INVALID_PROTO_BYTES,
)


def test_string_metadata_affects_command(binarytransfertest_stub):
    """
    - Call BinaryTransferTest.Get_FCPAffectedByMetadata_String
    - Expect that the returned list contains the fully qualified identifier of the command
        BinaryTransferTest.EchoBinaryAndMetadataString
    """
    response = binarytransfertest_stub.Get_FCPAffectedByMetadata_String(Get_FCPAffectedByMetadata_String_Parameters())
    affected_calls = [call.value for call in response.AffectedCalls]
    assert "org.silastandard/test/BinaryTransferTest/v1/Command/EchoBinaryAndMetadataString" in affected_calls


def test_command_validates_metadata_before_parameter_validation(binarytransfertest_stub):
    """
    - Invoke BinaryTransferTest.EchoBinaryAndMetadataString with invalid parameters and without metadata
        - Metadata has to be checked before parameter validation -> Expect Invalid Metadata Error, not Validation Error
    - Parameter messages:
        - Empty Parameters message
        - Parameters message containing an empty Binary message
        - Parameters message containing a Binary message with a random (invalid) binary transfer UUID
    """
    with raises_invalid_metadata_error():
        binarytransfertest_stub.EchoBinaryAndMetadataString(EchoBinaryAndMetadataString_Parameters())
    with raises_invalid_metadata_error():
        binarytransfertest_stub.EchoBinaryAndMetadataString(
            EchoBinaryAndMetadataString_Parameters(Binary=SiLAFramework_pb2.Binary())
        )
    with raises_invalid_metadata_error():
        binarytransfertest_stub.EchoBinaryAndMetadataString(
            EchoBinaryAndMetadataString_Parameters(
                Binary=SiLAFramework_pb2.Binary(binaryTransferUUID=str(uuid.uuid4()))
            )
        )


def test_command_requires_metadata(binarytransfertest_stub):
    """
    - Invoke BinaryTransferTest.EchoBinaryAndMetadataString with a small binary parameter and missing metadata
    - Expect an Invalid Metadata error
    """
    with raises_invalid_metadata_error():
        binarytransfertest_stub.EchoBinaryAndMetadataString(
            EchoBinaryAndMetadataString_Parameters(Binary=SiLAFramework_pb2.Binary(value=b"abc"))
        )


def test_command_rejects_invalid_metadata_bytes(binarytransfertest_stub):
    """
    - Invoke BinaryTransferTest.EchoBinaryAndMetadataString with a small binary parameter and invalid metadata bytes
        for the String metadata
    - Expect an Invalid Metadata error
    """
    with raises_invalid_metadata_error():
        binarytransfertest_stub.EchoBinaryAndMetadataString.with_call(
            request=EchoBinaryAndMetadataString_Parameters(Binary=SiLAFramework_pb2.Binary(value=b"abc")),
            metadata=(INVALID_STRING_METADATA,),
        )


def test_command_rejects_invalid_metadata_bytes_before_parameter_validation(binarytransfertest_stub):
    """
    - Invoke BinaryTransferTest.EchoBinaryAndMetadataString with invalid parameters and invalid metadata bytes
        for the String metadata
        - Metadata has to be checked before parameter validation -> Expect Invalid Metadata Error, not Validation Error
    - Parameter messages:
        - Empty Parameters message
        - Parameters message containing an empty Binary message
        - Parameters message containing a Binary message with a random (invalid) binary transfer UUID
    """
    with raises_invalid_metadata_error():
        binarytransfertest_stub.EchoBinaryAndMetadataString.with_call(
            request=EchoBinaryAndMetadataString_Parameters(),
            metadata=(INVALID_STRING_METADATA,),
        )
    with raises_invalid_metadata_error():
        binarytransfertest_stub.EchoBinaryAndMetadataString.with_call(
            request=EchoBinaryAndMetadataString_Parameters(Binary=SiLAFramework_pb2.Binary()),
            metadata=(INVALID_STRING_METADATA,),
        )
    with raises_invalid_metadata_error():
        binarytransfertest_stub.EchoBinaryAndMetadataString.with_call(
            request=EchoBinaryAndMetadataString_Parameters(
                Binary=SiLAFramework_pb2.Binary(binaryTransferUUID=str(uuid.uuid4()))
            ),
            metadata=(INVALID_STRING_METADATA,),
        )


def test_parameters_are_validated_when_metadata_is_received(binarytransfertest_stub):
    """
    - Invoke BinaryTransferTest.EchoBinaryAndMetadataString with invalid parameters and valid String metadata
        - Expect Validation Errors
    - Parameter messages:
        - Empty Parameters message
        - Parameters message containing an empty Binary message
        - Parameters message containing a Binary message with a random (invalid) binary transfer UUID
    """
    with raises_validation_error(
        "org.silastandard/test/BinaryTransferTest/v1/Command/EchoBinaryAndMetadataString/Parameter/Binary"
    ):
        binarytransfertest_stub.EchoBinaryAndMetadataString.with_call(
            request=EchoBinaryAndMetadataString_Parameters(),
            metadata=pack_metadata(Metadata_String(String=SiLAFramework_pb2.String(value="abc"))),
        )
    with raises_validation_error(
        "org.silastandard/test/BinaryTransferTest/v1/Command/EchoBinaryAndMetadataString/Parameter/Binary"
    ):
        binarytransfertest_stub.EchoBinaryAndMetadataString.with_call(
            request=EchoBinaryAndMetadataString_Parameters(Binary=SiLAFramework_pb2.Binary()),
            metadata=pack_metadata(Metadata_String(String=SiLAFramework_pb2.String(value="abc"))),
        )
    with raises_validation_error(
        "org.silastandard/test/BinaryTransferTest/v1/Command/EchoBinaryAndMetadataString/Parameter/Binary"
    ):
        binarytransfertest_stub.EchoBinaryAndMetadataString.with_call(
            request=EchoBinaryAndMetadataString_Parameters(
                Binary=SiLAFramework_pb2.Binary(binaryTransferUUID=str(uuid.uuid4()))
            ),
            metadata=pack_metadata(Metadata_String(String=SiLAFramework_pb2.String(value="abc"))),
        )


def test_command_works_with_small_binary(binarytransfertest_stub, binary_download_stub):
    """
    - Invoke BinaryTransferTest.EchoBinaryAndMetadataString with the small binary 'abc' and valid String metadata 'abc'
    - Expect that the response echoes both values
    """
    response, _ = binarytransfertest_stub.EchoBinaryAndMetadataString.with_call(
        request=EchoBinaryAndMetadataString_Parameters(Binary=SiLAFramework_pb2.Binary(value=b"abc")),
        metadata=pack_metadata(Metadata_String(String=SiLAFramework_pb2.String(value="abc"))),
    )

    assert response.StringMetadata.value == "abc"
    if response.Binary.HasField("value"):
        assert response.Binary.value == b"abc"
    else:
        assert download_binary(binary_download_stub, response.Binary.binaryTransferUUID) == b"abc"


def test_create_binary_requires_metadata(binary_upload_stub):
    """
    - Invoke BinaryUpload.CreateBinary for the parameter EchoBinaryAndMetadataString.Binary without metadata
    - Expect an Invalid Metadata error
    """
    with raises_invalid_metadata_error():
        binary_upload_stub.CreateBinary.with_call(
            CreateBinaryRequest(
                binarySize=3 * 1_000_000,
                chunkCount=3,
                parameterIdentifier=(
                    "org.silastandard/test/BinaryTransferTest/v1/Command/EchoBinaryAndMetadataString/Parameter/Binary"
                ),
            )
        )


def test_command_works_with_large_binary(binary_upload_stub, binarytransfertest_stub, binary_download_stub):
    """
    - Upload a binary with value 'abc' repeated 1,000,000 times for the parameter EchoBinaryAndMetadataString.Binary and
        the String metadata 'abc'
    - Call the command BinaryTransferTest.EchoBinaryAndMetadataString with this binary and the String metadata 'abc'
    - Expect that the response echoes both values
    """
    upload_id = upload_binary(
        binary_upload_stub,
        b"abc" * 1_000_000,
        "org.silastandard/test/BinaryTransferTest/v1/Command/EchoBinaryAndMetadataString/Parameter/Binary",
        metadata=[Metadata_String(String=SiLAFramework_pb2.String(value="abc"))],
    )
    response, _ = binarytransfertest_stub.EchoBinaryAndMetadataString.with_call(
        request=EchoBinaryAndMetadataString_Parameters(
            Binary=SiLAFramework_pb2.Binary(binaryTransferUUID=str(upload_id))
        ),
        metadata=pack_metadata(Metadata_String(String=SiLAFramework_pb2.String(value="abc"))),
    )

    assert response.StringMetadata.value == "abc"
    assert download_binary(binary_download_stub, response.Binary.binaryTransferUUID) == b"abc" * 1_000_000


def test_command_is_rejected_with_missing_metadata_after_successful_upload_with_metadata(
    binary_upload_stub, binarytransfertest_stub
):
    """
    - Upload a binary with value 'abc' repeated 1,000,000 times for the parameter EchoBinaryAndMetadataString.Binary and
        the String metadata 'abc'
    - Invoke the command BinaryTransferTest.EchoBinaryAndMetadataString with this binary and the string parameter 'abc'
        without metadata
    - Expect an Invalid Metadata error
    """
    upload_id = upload_binary(
        binary_upload_stub,
        b"abc" * 1_000_000,
        "org.silastandard/test/BinaryTransferTest/v1/Command/EchoBinaryAndMetadataString/Parameter/Binary",
        metadata=[Metadata_String(String=SiLAFramework_pb2.String(value="abc"))],
    )
    with raises_invalid_metadata_error():
        binarytransfertest_stub.EchoBinaryAndMetadataString(
            EchoBinaryAndMetadataString_Parameters(Binary=SiLAFramework_pb2.Binary(binaryTransferUUID=str(upload_id))),
        )
