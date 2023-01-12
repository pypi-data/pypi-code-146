import re
import uuid
from typing import Optional
from xml.etree import ElementTree

import grpc

from sila2_interop_communication_tester.grpc_stubs import SiLAFramework_pb2, SiLAService_pb2
from sila2_interop_communication_tester.grpc_stubs.SiLAService_pb2_grpc import SiLAServiceServicer
from sila2_interop_communication_tester.helpers.fdl_tools import fdl_dir
from sila2_interop_communication_tester.test_server.helpers.raise_error import (
    raise_defined_execution_error,
    raise_no_metadata_allowed_error,
    raise_validation_error,
)
from sila2_interop_communication_tester.test_server.helpers.spy import extract_metadata


class SiLAServiceImpl(SiLAServiceServicer):
    def __init__(self, server_uuid: Optional[uuid.UUID] = None):
        super().__init__()
        self.name = "Test Server"
        self.uuid = uuid.uuid4() if server_uuid is None else server_uuid
        self.implemented_features = self.__get_implemented_features()

    def GetFeatureDefinition(
        self, request: SiLAService_pb2.GetFeatureDefinition_Parameters, context: grpc.ServicerContext
    ) -> SiLAService_pb2.GetFeatureDefinition_Responses:
        if extract_metadata(context):
            raise_no_metadata_allowed_error(context, "SiLAService.GetFeatureDefinition received metadata")
        if not request.HasField("FeatureIdentifier"):
            raise_validation_error(
                context,
                "org.silastandard/core/SiLAService/v1/Command/GetFeatureDefinition/Parameter/FeatureIdentifier",
                "Missing parameter",
            )

        feature_id = request.FeatureIdentifier.value
        if not re.fullmatch(r"[a-z][a-z.]*/[a-z][a-z.]*/[A-Z][a-zA-Z\d]*/v\d+", feature_id):
            raise_validation_error(
                context,
                "org.silastandard/core/SiLAService/v1/Command/GetFeatureDefinition/Parameter/FeatureIdentifier",
                f"Not a fully qualified feature identifier: {feature_id!r}",
            )

        if feature_id not in self.implemented_features:
            raise_defined_execution_error(
                context,
                "org.silastandard/core/SiLAService/v1/DefinedExecutionError/UnimplementedFeature",
                f"Feature is not implemented: {feature_id!r}",
            )

        return SiLAService_pb2.GetFeatureDefinition_Responses(
            FeatureDefinition=SiLAFramework_pb2.String(value=self.implemented_features[feature_id])
        )

    def SetServerName(
        self, request: SiLAService_pb2.SetServerName_Parameters, context: grpc.ServicerContext
    ) -> SiLAService_pb2.SetServerName_Responses:
        if extract_metadata(context):
            raise_no_metadata_allowed_error(context, "SiLAService.SetServerName received metadata")
        if not request.HasField("ServerName"):
            raise_validation_error(
                context,
                "org.silastandard/core/SiLAService/v1/Command/SetServerName/Parameter/ServerName",
                "Missing parameter",
            )

        server_name = request.ServerName.value
        if not server_name or len(server_name) > 255:
            raise_validation_error(
                context,
                "org.silastandard/core/SiLAService/v1/Command/SetServerName/Parameter/ServerName",
                "Invalid name, must be non-empty and <= 255 characters long",
            )

        self.name = request.ServerName.value
        return SiLAService_pb2.SetServerName_Responses()

    def Get_ServerName(
        self, request: SiLAService_pb2.Get_ServerName_Parameters, context: grpc.ServicerContext
    ) -> SiLAService_pb2.Get_ServerName_Responses:
        if extract_metadata(context):
            raise_no_metadata_allowed_error(context, "SiLAService.ServerName requested with metadata")
        return SiLAService_pb2.Get_ServerName_Responses(ServerName=SiLAFramework_pb2.String(value=self.name))

    def Get_ServerType(
        self, request: SiLAService_pb2.Get_ServerType_Parameters, context: grpc.ServicerContext
    ) -> SiLAService_pb2.Get_ServerType_Responses:
        if extract_metadata(context):
            raise_no_metadata_allowed_error(context, "SiLAService.ServerType requested with metadata")
        return SiLAService_pb2.Get_ServerType_Responses(ServerType=SiLAFramework_pb2.String(value="TestServer"))

    def Get_ServerUUID(
        self, request: SiLAService_pb2.Get_ServerUUID_Parameters, context: grpc.ServicerContext
    ) -> SiLAService_pb2.Get_ServerUUID_Responses:
        if extract_metadata(context):
            raise_no_metadata_allowed_error(context, "SiLAService.ServerUUID requested with metadata")
        return SiLAService_pb2.Get_ServerUUID_Responses(ServerUUID=SiLAFramework_pb2.String(value=str(self.uuid)))

    def Get_ServerDescription(
        self, request: SiLAService_pb2.Get_ServerDescription_Parameters, context: grpc.ServicerContext
    ) -> SiLAService_pb2.Get_ServerDescription_Responses:
        if extract_metadata(context):
            raise_no_metadata_allowed_error(context, "SiLAService.ServerDescription requested with metadata")
        return SiLAService_pb2.Get_ServerDescription_Responses(
            ServerDescription=SiLAFramework_pb2.String(value="This is a test server")
        )

    def Get_ServerVersion(
        self, request: SiLAService_pb2.Get_ServerVersion_Parameters, context: grpc.ServicerContext
    ) -> SiLAService_pb2.Get_ServerVersion_Responses:
        if extract_metadata(context):
            raise_no_metadata_allowed_error(context, "SiLAService.ServerVersion requested with metadata")
        return SiLAService_pb2.Get_ServerVersion_Responses(ServerVersion=SiLAFramework_pb2.String(value="0.1"))

    def Get_ServerVendorURL(
        self, request: SiLAService_pb2.Get_ServerVendorURL_Parameters, context: grpc.ServicerContext
    ) -> SiLAService_pb2.Get_ServerVendorURL_Responses:
        if extract_metadata(context):
            raise_no_metadata_allowed_error(context, "SiLAService.ServerVendorURL requested with metadata")
        return SiLAService_pb2.Get_ServerVendorURL_Responses(
            ServerVendorURL=SiLAFramework_pb2.String(value="https://gitlab.com/SiLA2/sila_interoperability")
        )

    def Get_ImplementedFeatures(
        self, request: SiLAService_pb2.Get_ImplementedFeatures_Parameters, context: grpc.ServicerContext
    ) -> SiLAService_pb2.Get_ImplementedFeatures_Responses:
        if extract_metadata(context):
            raise_no_metadata_allowed_error(context, "SiLAService.ImplementedFeatures requested with metadata")
        return SiLAService_pb2.Get_ImplementedFeatures_Responses(
            ImplementedFeatures=[SiLAFramework_pb2.String(value=feature_id) for feature_id in self.implemented_features]
        )

    @staticmethod
    def __get_implemented_features() -> dict[str, str]:
        implemented_features = {}

        for fdl_filename in fdl_dir.absolute().glob("*.sila.xml"):
            fdl_root = ElementTree.parse(fdl_filename).getroot()
            originator: str = fdl_root.attrib["Originator"]
            version: str = "v" + fdl_root.attrib["FeatureVersion"].split(".")[0]
            category: str = fdl_root.attrib["Category"]
            identifier: str = fdl_root[0].text

            fully_qualified_id = "/".join((originator, category, identifier, version))

            with open(fdl_filename, encoding="utf-8") as fp:
                implemented_features[fully_qualified_id] = fp.read()

        return implemented_features
