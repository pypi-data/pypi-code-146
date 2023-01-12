import math
import time

from sila2_interop_communication_tester.grpc_stubs import UnobservablePropertyTest_pb2


def test_answer_to_everything(unobservablepropertytest_stub):
    answer = unobservablepropertytest_stub.Get_AnswerToEverything(
        UnobservablePropertyTest_pb2.Get_AnswerToEverything_Parameters()
    ).AnswerToEverything.value
    assert 42 == answer


def test_seconds_since_1970(unobservablepropertytest_stub):
    time_since_1970 = unobservablepropertytest_stub.Get_SecondsSince1970(
        UnobservablePropertyTest_pb2.Get_SecondsSince1970_Parameters()
    ).SecondsSince1970.value
    assert math.isclose(time.time(), time_since_1970, abs_tol=10)
