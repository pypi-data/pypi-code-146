from sila2_interop_communication_tester.grpc_stubs import MetadataProvider_pb2, SiLAFramework_pb2, SiLAService_pb2
from sila2_interop_communication_tester.test_client.helpers.error_handling import raises_no_metadata_allowed_error
from sila2_interop_communication_tester.test_client.helpers.utils import pack_metadata


def test_get_feature_definition_rejects_metadata(silaservice_stub):
    with raises_no_metadata_allowed_error():
        silaservice_stub.GetFeatureDefinition.with_call(
            request=SiLAService_pb2.GetFeatureDefinition_Parameters(
                FeatureIdentifier=SiLAFramework_pb2.String(value="org.silastandard/core/SiLAService/v1")
            ),
            metadata=pack_metadata(
                MetadataProvider_pb2.Metadata_StringMetadata(
                    StringMetadata=SiLAFramework_pb2.String(value="example-string")
                )
            ),
        )


def test_set_server_version_rejects_metadata(silaservice_stub):
    server_name = silaservice_stub.Get_ServerName(SiLAService_pb2.Get_ServerName_Parameters()).ServerName
    try:
        with raises_no_metadata_allowed_error():
            silaservice_stub.SetServerName.with_call(
                request=SiLAService_pb2.SetServerName_Parameters(ServerName=server_name),
                metadata=pack_metadata(
                    MetadataProvider_pb2.Metadata_StringMetadata(
                        StringMetadata=SiLAFramework_pb2.String(value="example-string")
                    )
                ),
            )
    finally:
        # reset ServerName in case the call was not rejected
        silaservice_stub.SetServerName(SiLAService_pb2.SetServerName_Parameters(ServerName=server_name))


def test_get_server_name_rejects_metadata(silaservice_stub):
    with raises_no_metadata_allowed_error():
        silaservice_stub.Get_ServerName.with_call(
            request=SiLAService_pb2.Get_ServerName_Parameters(),
            metadata=pack_metadata(
                MetadataProvider_pb2.Metadata_StringMetadata(
                    StringMetadata=SiLAFramework_pb2.String(value="example-string")
                )
            ),
        )


def test_get_server_type_rejects_metadata(silaservice_stub):
    with raises_no_metadata_allowed_error():
        silaservice_stub.Get_ServerType.with_call(
            request=SiLAService_pb2.Get_ServerType_Parameters(),
            metadata=pack_metadata(
                MetadataProvider_pb2.Metadata_StringMetadata(
                    StringMetadata=SiLAFramework_pb2.String(value="example-string")
                )
            ),
        )


def test_get_server_uuid_rejects_metadata(silaservice_stub):
    with raises_no_metadata_allowed_error():
        silaservice_stub.Get_ServerUUID.with_call(
            request=SiLAService_pb2.Get_ServerUUID_Parameters(),
            metadata=pack_metadata(
                MetadataProvider_pb2.Metadata_StringMetadata(
                    StringMetadata=SiLAFramework_pb2.String(value="example-string")
                )
            ),
        )


def test_get_server_description_rejects_metadata(silaservice_stub):
    with raises_no_metadata_allowed_error():
        silaservice_stub.Get_ServerDescription.with_call(
            request=SiLAService_pb2.Get_ServerDescription_Parameters(),
            metadata=pack_metadata(
                MetadataProvider_pb2.Metadata_StringMetadata(
                    StringMetadata=SiLAFramework_pb2.String(value="example-string")
                )
            ),
        )


def test_get_server_version_rejects_metadata(silaservice_stub):
    with raises_no_metadata_allowed_error():
        silaservice_stub.Get_ServerVersion.with_call(
            request=SiLAService_pb2.Get_ServerVersion_Parameters(),
            metadata=pack_metadata(
                MetadataProvider_pb2.Metadata_StringMetadata(
                    StringMetadata=SiLAFramework_pb2.String(value="example-string")
                )
            ),
        )


def test_get_server_vendor_url_rejects_metadata(silaservice_stub):
    with raises_no_metadata_allowed_error():
        silaservice_stub.Get_ServerVendorURL.with_call(
            request=SiLAService_pb2.Get_ServerVendorURL_Parameters(),
            metadata=pack_metadata(
                MetadataProvider_pb2.Metadata_StringMetadata(
                    StringMetadata=SiLAFramework_pb2.String(value="example-string")
                )
            ),
        )


def test_get_implemented_features_rejects_metadata(silaservice_stub):
    with raises_no_metadata_allowed_error():
        silaservice_stub.Get_ImplementedFeatures.with_call(
            request=SiLAService_pb2.Get_ImplementedFeatures_Parameters(),
            metadata=pack_metadata(
                MetadataProvider_pb2.Metadata_StringMetadata(
                    StringMetadata=SiLAFramework_pb2.String(value="example-string")
                )
            ),
        )
