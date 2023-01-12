import grpc

from sila2_interop_communication_tester.grpc_stubs import (
    MetadataConsumerTest_pb2,
    MetadataProvider_pb2,
    SiLAFramework_pb2,
)
from sila2_interop_communication_tester.grpc_stubs.MetadataConsumerTest_pb2_grpc import MetadataConsumerTestServicer
from sila2_interop_communication_tester.test_server.helpers.raise_error import raise_invalid_metadata_error
from sila2_interop_communication_tester.test_server.helpers.spy import extract_metadata


class MetadataConsumerTestImpl(MetadataConsumerTestServicer):
    def EchoStringMetadata(
        self, request: MetadataConsumerTest_pb2.EchoStringMetadata_Parameters, context: grpc.ServicerContext
    ) -> MetadataConsumerTest_pb2.EchoStringMetadata_Responses:
        try:
            metadata = extract_metadata(context)
        except BaseException as ex:
            raise_invalid_metadata_error(context, f"Failed to parse received metadata: {ex!r}")

        try:
            string_metadata = metadata[MetadataProvider_pb2.Metadata_StringMetadata]
        except KeyError:
            raise_invalid_metadata_error(
                context,
                "Missing metadata, expected 'org.silastandard/test/MetadataProvider/v1/Metadata/StringMetadata'",
            )

        if not string_metadata.HasField("StringMetadata"):
            raise_invalid_metadata_error(context, "Received StringMetadata message was empty")

        return MetadataConsumerTest_pb2.EchoStringMetadata_Responses(
            ReceivedStringMetadata=SiLAFramework_pb2.String(value=string_metadata.StringMetadata.value)
        )

    def UnpackMetadata(
        self, request: MetadataConsumerTest_pb2.UnpackMetadata_Parameters, context: grpc.ServicerContext
    ) -> MetadataConsumerTest_pb2.UnpackMetadata_Responses:
        try:
            metadata = extract_metadata(context)
        except BaseException as ex:
            raise_invalid_metadata_error(context, f"Failed to parse received metadata: {ex!r}")

        try:
            string_metadata = metadata[MetadataProvider_pb2.Metadata_StringMetadata]
            two_integers_metadata = metadata[MetadataProvider_pb2.Metadata_TwoIntegersMetadata]
        except KeyError:
            raise_invalid_metadata_error(
                context,
                "Missing metadata, expected 'org.silastandard/test/MetadataProvider/v1/Metadata/StringMetadata' "
                "and 'org.silastandard/test/MetadataProvider/v1/Metadata/TwoIntegersMetadata'",
            )

        if not string_metadata.HasField("StringMetadata"):
            raise_invalid_metadata_error(context, "Received StringMetadata message was empty")

        if not two_integers_metadata.HasField("TwoIntegersMetadata"):
            raise_invalid_metadata_error(context, "Received TwoIntegersMetadata message was empty")
        if not two_integers_metadata.TwoIntegersMetadata.HasField("FirstInteger"):
            raise_invalid_metadata_error(context, "Received TwoIntegersMetadata has empty field FirstInteger")
        if not two_integers_metadata.TwoIntegersMetadata.HasField("SecondInteger"):
            raise_invalid_metadata_error(context, "Received TwoIntegersMetadata has empty field SecondInteger")

        return MetadataConsumerTest_pb2.UnpackMetadata_Responses(
            ReceivedString=SiLAFramework_pb2.String(value=string_metadata.StringMetadata.value),
            FirstReceivedInteger=SiLAFramework_pb2.Integer(
                value=two_integers_metadata.TwoIntegersMetadata.FirstInteger.value
            ),
            SecondReceivedInteger=SiLAFramework_pb2.Integer(
                value=two_integers_metadata.TwoIntegersMetadata.SecondInteger.value
            ),
        )
