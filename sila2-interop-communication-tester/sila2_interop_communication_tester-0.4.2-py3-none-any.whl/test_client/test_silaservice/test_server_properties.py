import contextlib
import re

from sila2_interop_communication_tester.grpc_stubs import SiLAFramework_pb2, SiLAService_pb2
from sila2_interop_communication_tester.grpc_stubs.SiLAService_pb2_grpc import SiLAServiceStub
from sila2_interop_communication_tester.test_client.helpers.error_handling import raises_validation_error


@contextlib.contextmanager
def reset_server_name(stub: SiLAServiceStub):
    """Context manager which resets the SiLAService.ServerName property on exit"""
    old_server_name = stub.Get_ServerName(SiLAService_pb2.Get_ServerName_Parameters()).ServerName.value

    try:
        yield
    finally:
        stub.SetServerName(
            SiLAService_pb2.SetServerName_Parameters(ServerName=SiLAFramework_pb2.String(value=old_server_name))
        )


def test_get_server_name(silaservice_stub):
    server_name = silaservice_stub.Get_ServerName(SiLAService_pb2.Get_ServerName_Parameters()).ServerName.value
    assert len(server_name) > 0, "ServerName was empty"
    assert len(server_name) <= 255, "ServerName was too long (constraint: MaximalLength 255)"


def test_get_server_type(silaservice_stub):
    server_type = silaservice_stub.Get_ServerType(SiLAService_pb2.Get_ServerType_Parameters()).ServerType.value
    match = re.fullmatch(r"[A-Z][a-zA-Z\d]*", server_type)
    assert match is not None, "Invalid ServerType (constraint: Pattern '[A-Z][a-zA-Z0-9]*')"


def test_get_server_version(silaservice_stub):
    server_version = silaservice_stub.Get_ServerVersion(
        SiLAService_pb2.Get_ServerVersion_Parameters()
    ).ServerVersion.value
    match = re.fullmatch(r"(0|[1-9]\d*)\.(0|[1-9]\d*)(\.(0|[1-9]\d*))?(_\w+)?", server_version)
    assert match is not None, (
        r"Invalid ServerVersion "
        r"(constraint: Pattern '(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)(\.(0|[1-9][0-9]*))?(_[_a-zA-Z0-9]+)?', "
        r"examples: '0.1', '1.0.12', '13.3_beta_release2')"
    )


def test_get_server_vendor_url(silaservice_stub):
    server_vendor_url = silaservice_stub.Get_ServerVendorURL(
        SiLAService_pb2.Get_ServerVendorURL_Parameters()
    ).ServerVendorURL.value
    match = re.fullmatch(r"https?://.+", server_vendor_url)
    assert match is not None, "Invalid ServerVendorURL (constraint: Pattern 'https?://.+')"


def test_get_server_description(silaservice_stub):
    server_description = silaservice_stub.Get_ServerDescription(
        SiLAService_pb2.Get_ServerDescription_Parameters()
    ).ServerDescription.value
    assert len(server_description) > 0, "ServerDescription was empty"


def test_get_server_uuid(silaservice_stub):
    server_uuid = silaservice_stub.Get_ServerUUID(SiLAService_pb2.Get_ServerUUID_Parameters()).ServerUUID.value
    assert len(server_uuid) == 36, "Invalid ServerUUID (constraint: Length 36)"
    assert re.fullmatch(
        r"[\da-f]{8}-[\da-f]{4}-[\da-f]{4}-[\da-f]{4}-[\da-f]{12}", server_uuid
    ), r"Invalid ServerUUID (constraint: Pattern '[\da-f]{8}-[\da-f]{4}-[\da-f]{4}-[\da-f]{4}-[\da-f]{12}')"


def test_set_server_name_sets_name(silaservice_stub):
    with reset_server_name(silaservice_stub):
        old_name: str = silaservice_stub.Get_ServerName(SiLAService_pb2.Get_ServerName_Parameters()).ServerName.value
        new_name = "SiLA is Awesome"

        silaservice_stub.SetServerName(
            SiLAService_pb2.SetServerName_Parameters(ServerName=SiLAFramework_pb2.String(value=new_name))
        )

        assert (
            silaservice_stub.Get_ServerName(SiLAService_pb2.Get_ServerName_Parameters()).ServerName.value == new_name
        ), f"SetServerName did not set the ServerName property from {old_name!r} to {new_name!r}"


def test_set_server_name_with_too_long_parameter_raises_validation_error(silaservice_stub):
    with reset_server_name(silaservice_stub):
        with raises_validation_error("org.silastandard/core/SiLAService/v1/Command/SetServerName/Parameter/ServerName"):
            silaservice_stub.SetServerName(
                SiLAService_pb2.SetServerName_Parameters(ServerName=SiLAFramework_pb2.String(value="H" * 256))
            )


def test_set_server_name_with_empty_message_raises_validation_error(silaservice_stub):
    with reset_server_name(silaservice_stub):
        old_server_name = silaservice_stub.Get_ServerName(SiLAService_pb2.Get_ServerName_Parameters()).ServerName.value

        with raises_validation_error("org.silastandard/core/SiLAService/v1/Command/SetServerName/Parameter/ServerName"):
            silaservice_stub.SetServerName(SiLAService_pb2.SetServerName_Parameters())

        new_server_name = silaservice_stub.Get_ServerName(SiLAService_pb2.Get_ServerName_Parameters()).ServerName.value
        assert old_server_name == new_server_name, (
            "SetServerName changed the ServerName property to an illegal value "
            "before raising the correct ValidationError"
        )
