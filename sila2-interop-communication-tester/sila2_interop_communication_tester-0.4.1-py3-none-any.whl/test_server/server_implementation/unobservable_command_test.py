import grpc

from sila2_interop_communication_tester.grpc_stubs import SiLAFramework_pb2, UnobservableCommandTest_pb2
from sila2_interop_communication_tester.grpc_stubs.UnobservableCommandTest_pb2_grpc import (
    UnobservableCommandTestServicer,
)
from sila2_interop_communication_tester.test_server.helpers.raise_error import raise_validation_error


class UnobservableCommandTestImpl(UnobservableCommandTestServicer):
    def CommandWithoutParametersAndResponses(
        self,
        request: UnobservableCommandTest_pb2.CommandWithoutParametersAndResponses_Parameters,
        context: grpc.ServicerContext,
    ) -> UnobservableCommandTest_pb2.CommandWithoutParametersAndResponses_Responses:
        return UnobservableCommandTest_pb2.CommandWithoutParametersAndResponses_Responses()

    def ConvertIntegerToString(
        self, request: UnobservableCommandTest_pb2.ConvertIntegerToString_Parameters, context: grpc.ServicerContext
    ) -> UnobservableCommandTest_pb2.ConvertIntegerToString_Responses:
        if not request.HasField("Integer"):
            raise_validation_error(
                context,
                "org.silastandard/test/UnobservableCommandTest/v1/Command/ConvertIntegerToString/Parameter/Integer",
                "Missing parameter 'Integer'",
            )
        return UnobservableCommandTest_pb2.ConvertIntegerToString_Responses(
            StringRepresentation=SiLAFramework_pb2.String(value=str(request.Integer.value))
        )

    def JoinIntegerAndString(
        self, request: UnobservableCommandTest_pb2.JoinIntegerAndString_Parameters, context: grpc.ServicerContext
    ) -> UnobservableCommandTest_pb2.JoinIntegerAndString_Responses:
        if not request.HasField("Integer"):
            raise_validation_error(
                context,
                "org.silastandard/test/UnobservableCommandTest/v1/Command/JoinIntegerAndString/Parameter/Integer",
                "Missing parameter 'Integer'",
            )
        if not request.HasField("String"):
            raise_validation_error(
                context,
                "org.silastandard/test/UnobservableCommandTest/v1/Command/JoinIntegerAndString/Parameter/String",
                "Missing parameter 'String'",
            )
        return UnobservableCommandTest_pb2.JoinIntegerAndString_Responses(
            JoinedParameters=SiLAFramework_pb2.String(value=f"{request.Integer.value}{request.String.value}")
        )

    def SplitStringAfterFirstCharacter(
        self,
        request: UnobservableCommandTest_pb2.SplitStringAfterFirstCharacter_Parameters,
        context: grpc.ServicerContext,
    ) -> UnobservableCommandTest_pb2.SplitStringAfterFirstCharacter_Responses:
        if not request.HasField("String"):
            raise_validation_error(
                context,
                (
                    "org.silastandard/test/UnobservableCommandTest/v1/Command/"
                    "SplitStringAfterFirstCharacter/Parameter/String"
                ),
                "Missing parameter 'String'",
            )
        return UnobservableCommandTest_pb2.SplitStringAfterFirstCharacter_Responses(
            FirstCharacter=SiLAFramework_pb2.String(value=request.String.value[:1]),
            Remainder=SiLAFramework_pb2.String(value=request.String.value[1:]),
        )
