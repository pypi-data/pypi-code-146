import threading
import time
import typing

import grpc

from sila2_interop_communication_tester.grpc_stubs import ObservablePropertyTest_pb2, SiLAFramework_pb2
from sila2_interop_communication_tester.grpc_stubs.ObservablePropertyTest_pb2_grpc import ObservablePropertyTestServicer
from sila2_interop_communication_tester.test_server.helpers.raise_error import raise_validation_error


class ObservablePropertyTestImpl(ObservablePropertyTestServicer):
    def __init__(self):
        self.current_value = 0
        self.value_update_cv = threading.Condition()

    def SetValue(
        self, request: ObservablePropertyTest_pb2.SetValue_Parameters, context: grpc.ServicerContext
    ) -> ObservablePropertyTest_pb2.SetValue_Responses:
        if not request.HasField("Value"):
            raise_validation_error(
                context,
                "org.silastandard/test/ObservablePropertyTest/v1/Command/SetValue/Parameter/Value",
                "Missing parameter: 'Value'",
            )
        self.current_value = request.Value.value
        with self.value_update_cv:
            self.value_update_cv.notify_all()
        return ObservablePropertyTest_pb2.SetValue_Responses()

    def Subscribe_FixedValue(
        self, request: ObservablePropertyTest_pb2.Subscribe_FixedValue_Parameters, context: grpc.ServicerContext
    ) -> typing.Iterator[ObservablePropertyTest_pb2.Subscribe_FixedValue_Responses]:
        yield ObservablePropertyTest_pb2.Subscribe_FixedValue_Responses(FixedValue=SiLAFramework_pb2.Integer(value=42))

    def Subscribe_Alternating(
        self, request: ObservablePropertyTest_pb2.Subscribe_Alternating_Parameters, context: grpc.ServicerContext
    ) -> typing.Iterator[ObservablePropertyTest_pb2.Subscribe_Alternating_Responses]:
        value: bool = True
        while context.is_active():
            yield ObservablePropertyTest_pb2.Subscribe_Alternating_Responses(
                Alternating=SiLAFramework_pb2.Boolean(value=value)
            )
            value = not value
            time.sleep(1)

    def Subscribe_Editable(
        self, request: ObservablePropertyTest_pb2.Subscribe_Editable_Parameters, context: grpc.ServicerContext
    ) -> typing.Iterator[ObservablePropertyTest_pb2.Subscribe_Editable_Responses]:
        yield ObservablePropertyTest_pb2.Subscribe_Editable_Responses(
            Editable=SiLAFramework_pb2.Integer(value=self.current_value)
        )
        while context.is_active():
            with self.value_update_cv:
                if self.value_update_cv.wait(timeout=0.1):
                    yield ObservablePropertyTest_pb2.Subscribe_Editable_Responses(
                        Editable=SiLAFramework_pb2.Integer(value=self.current_value)
                    )
