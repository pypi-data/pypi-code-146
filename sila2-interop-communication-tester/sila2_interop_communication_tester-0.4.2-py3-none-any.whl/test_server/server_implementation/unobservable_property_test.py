import time

import grpc

from sila2_interop_communication_tester.grpc_stubs import SiLAFramework_pb2, UnobservablePropertyTest_pb2
from sila2_interop_communication_tester.grpc_stubs.UnobservablePropertyTest_pb2_grpc import (
    UnobservablePropertyTestServicer,
)


class UnobservablePropertyTestImpl(UnobservablePropertyTestServicer):
    def Get_AnswerToEverything(
        self, request: UnobservablePropertyTest_pb2.Get_AnswerToEverything_Parameters, context: grpc.ServicerContext
    ) -> UnobservablePropertyTest_pb2.Get_AnswerToEverything_Responses:
        return UnobservablePropertyTest_pb2.Get_AnswerToEverything_Responses(
            AnswerToEverything=SiLAFramework_pb2.Integer(value=42)
        )

    def Get_SecondsSince1970(
        self, request: UnobservablePropertyTest_pb2.Get_SecondsSince1970_Parameters, context: grpc.ServicerContext
    ) -> UnobservablePropertyTest_pb2.Get_SecondsSince1970_Responses:
        return UnobservablePropertyTest_pb2.Get_SecondsSince1970_Responses(
            SecondsSince1970=SiLAFramework_pb2.Integer(value=int(time.time()))
        )
