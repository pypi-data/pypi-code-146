import uuid

from sila2_interop_communication_tester.grpc_stubs.BinaryTransferTest_pb2 import EchoBinaryValue_Parameters
from sila2_interop_communication_tester.grpc_stubs.SiLAFramework_pb2 import Binary
from sila2_interop_communication_tester.test_client.helpers.binary_transfer import download_binary, upload_binary
from sila2_interop_communication_tester.test_client.helpers.error_handling import raises_validation_error


def test_echo_binary_value_rejects_empty_parameter_message(binarytransfertest_stub):
    """BinaryTransferTest.EchoBinaryValue should fail with a Validation Error if the parameter message was empty"""
    with raises_validation_error(
        "org.silastandard/test/BinaryTransferTest/v1/Command/EchoBinaryValue/Parameter/BinaryValue"
    ):
        binarytransfertest_stub.EchoBinaryValue(EchoBinaryValue_Parameters())


def test_echo_binary_value_rejects_empty_binary_message(binarytransfertest_stub):
    """
    BinaryTransferTest.EchoBinaryValue should fail with a Validation Error if the parameter message contained an empty
    Binary message
    """
    with raises_validation_error(
        "org.silastandard/test/BinaryTransferTest/v1/Command/EchoBinaryValue/Parameter/BinaryValue"
    ):
        binarytransfertest_stub.EchoBinaryValue(EchoBinaryValue_Parameters(BinaryValue=Binary()))


def test_echo_binary_value_rejects_invalid_binary_transfer_uuid_string(
    binarytransfertest_stub,
):
    """
    BinaryTransferTest.EchoBinaryValue should fail with a Validation Error if the parameter message contained an Binary
    message with the `binaryTransferUUID` field set to a non-UUID string
    """
    with raises_validation_error(
        "org.silastandard/test/BinaryTransferTest/v1/Command/EchoBinaryValue/Parameter/BinaryValue"
    ):
        binarytransfertest_stub.EchoBinaryValue(
            EchoBinaryValue_Parameters(BinaryValue=Binary(binaryTransferUUID="abcde"))
        )


def test_echo_binary_value_rejects_unknown_binary_transfer_uuid(
    binarytransfertest_stub,
):
    """
    BinaryTransferTest.EchoBinaryValue should fail with a Validation Error if the parameter message contained an Binary
    message with the `binaryTransferUUID` field set to a randomly created UUID
    """
    with raises_validation_error(
        "org.silastandard/test/BinaryTransferTest/v1/Command/EchoBinaryValue/Parameter/BinaryValue"
    ):
        binarytransfertest_stub.EchoBinaryValue(
            EchoBinaryValue_Parameters(BinaryValue=Binary(binaryTransferUUID=str(uuid.uuid4())))
        )


def test_echo_binary_value_works_with_small_binary(binarytransfertest_stub):
    """
    BinaryTransferTest.EchoBinaryValue should work when provided with a binary < 2 MB using the `value` field of the
    Binary message
    """
    response = binarytransfertest_stub.EchoBinaryValue(EchoBinaryValue_Parameters(BinaryValue=Binary(value=b"abc")))
    assert response.ReceivedValue.value == b"abc"


def test_echo_binary_value_with_large_binary(binarytransfertest_stub, binary_upload_stub, binary_download_stub):
    """
    BinaryTransferTest.EchoBinaryValue should work when provided with a binary > 2 MB using Binary Upload
    """
    upload_id = upload_binary(
        binary_upload_stub,
        b"abc" * 1_000_000,
        "org.silastandard/test/BinaryTransferTest/v1/Command/EchoBinaryValue/Parameter/BinaryValue",
    )
    response = binarytransfertest_stub.EchoBinaryValue(
        EchoBinaryValue_Parameters(BinaryValue=Binary(binaryTransferUUID=str(upload_id)))
    )
    download_id = response.ReceivedValue.binaryTransferUUID
    downloaded_binary = download_binary(binary_download_stub, uuid.UUID(download_id))

    assert downloaded_binary == b"abc" * 1_000_000
