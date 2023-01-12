import random
from datetime import datetime

from sila2_interop_communication_tester.grpc_stubs import ObservablePropertyTest_pb2, SiLAFramework_pb2
from sila2_interop_communication_tester.test_client.helpers.error_handling import raises_validation_error


def test_get_fixedvalue(observablepropertytest_stub):
    """The property ObservablePropertyTest should have the fixed value 42"""
    stream = observablepropertytest_stub.Subscribe_FixedValue(
        ObservablePropertyTest_pb2.Subscribe_FixedValue_Parameters()
    )
    assert next(stream).FixedValue.value == 42
    stream.cancel()


def test_subscribe_alternating_sends_alternating_booleans(observablepropertytest_stub):
    """The property ObservablePropertyTest.Alternating should alternate between True and False every second."""
    stream = iter(
        observablepropertytest_stub.Subscribe_Alternating(ObservablePropertyTest_pb2.Subscribe_Alternating_Parameters())
    )

    values = []
    start_timestamp = datetime.now()
    for _ in range(4):
        values.append(next(stream).Alternating.value)
    end_timestamp = datetime.now()

    assert values == [True, False, True, False] or values == [False, True, False, True]

    # first value is current value
    # second value can come with 0-1s delay
    # third to forth value should arrive with ~1s delay
    assert 2 < (end_timestamp - start_timestamp).total_seconds() < 4


def test_setvalue_and_editable_work_with_1_2_3(observablepropertytest_stub):
    """
    ObservablePropertyTest.Editable should reflect the values set by ObservablePropertyTest.SetValue.
    This test uses ObservablePropertyTest with the values 1, 2, and 3 and asserts that Editable reflects this.
    """
    observablepropertytest_stub.SetValue(
        ObservablePropertyTest_pb2.SetValue_Parameters(Value=SiLAFramework_pb2.Integer(value=1))
    )

    stream = iter(
        observablepropertytest_stub.Subscribe_Editable(ObservablePropertyTest_pb2.Subscribe_Editable_Parameters())
    )
    assert next(stream).Editable.value == 1, "First Editable value was not the set value"

    observablepropertytest_stub.SetValue(
        ObservablePropertyTest_pb2.SetValue_Parameters(Value=SiLAFramework_pb2.Integer(value=2))
    )
    assert next(stream).Editable.value == 2

    observablepropertytest_stub.SetValue(
        ObservablePropertyTest_pb2.SetValue_Parameters(Value=SiLAFramework_pb2.Integer(value=3))
    )
    assert next(stream).Editable.value == 3


def test_setvalue_and_editable_work_with_random_numbers(observablepropertytest_stub):
    """
    ObservablePropertyTest.Editable should reflect the values set by ObservablePropertyTest.SetValue.
    This test uses ObservablePropertyTest with random integers and asserts that Editable reflects this.
    """
    stream = iter(
        observablepropertytest_stub.Subscribe_Editable(ObservablePropertyTest_pb2.Subscribe_Editable_Parameters())
    )
    next(stream)  # read current value

    for number in [random.randint(-100, 100) for _ in range(10)]:
        observablepropertytest_stub.SetValue(
            ObservablePropertyTest_pb2.SetValue_Parameters(Value=SiLAFramework_pb2.Integer(value=number))
        )
        assert next(stream).Editable.value == number


def test_setvalue_rejects_missing_parameter(observablepropertytest_stub):
    """ObservablePropertyTest.SetValue should reject empty parameter messages with a Validation Error"""
    with raises_validation_error("org.silastandard/test/ObservablePropertyTest/v1/Command/SetValue/Parameter/Value"):
        observablepropertytest_stub.SetValue(ObservablePropertyTest_pb2.SetValue_Parameters())
