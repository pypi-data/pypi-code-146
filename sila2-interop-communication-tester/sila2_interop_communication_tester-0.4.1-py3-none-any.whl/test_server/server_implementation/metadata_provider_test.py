import grpc

from sila2_interop_communication_tester.grpc_stubs import MetadataProvider_pb2, SiLAFramework_pb2
from sila2_interop_communication_tester.grpc_stubs.MetadataProvider_pb2_grpc import MetadataProviderServicer


class MetadataProviderImpl(MetadataProviderServicer):
    def Get_FCPAffectedByMetadata_StringMetadata(
        self,
        request: MetadataProvider_pb2.Get_FCPAffectedByMetadata_StringMetadata_Parameters,
        context: grpc.ServicerContext,
    ) -> MetadataProvider_pb2.Get_FCPAffectedByMetadata_StringMetadata_Responses:
        return MetadataProvider_pb2.Get_FCPAffectedByMetadata_StringMetadata_Responses(
            AffectedCalls=[SiLAFramework_pb2.String(value="org.silastandard/test/MetadataConsumerTest/v1")]
        )

    def Get_FCPAffectedByMetadata_TwoIntegersMetadata(
        self,
        request: MetadataProvider_pb2.Get_FCPAffectedByMetadata_TwoIntegersMetadata_Parameters,
        context: grpc.ServicerContext,
    ) -> MetadataProvider_pb2.Get_FCPAffectedByMetadata_TwoIntegersMetadata_Responses:
        return MetadataProvider_pb2.Get_FCPAffectedByMetadata_TwoIntegersMetadata_Responses(
            AffectedCalls=[
                SiLAFramework_pb2.String(value="org.silastandard/test/MetadataConsumerTest/v1/Command/UnpackMetadata")
            ]
        )
