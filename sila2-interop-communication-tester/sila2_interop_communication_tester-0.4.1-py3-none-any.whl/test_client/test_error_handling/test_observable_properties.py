from sila2_interop_communication_tester.grpc_stubs import ErrorHandlingTest_pb2
from sila2_interop_communication_tester.test_client.helpers.error_handling import (
    raises_defined_execution_error,
    raises_undefined_execution_error,
)


def test_raise_defined_execution_error_on_subscribe(errorhandlingtest_stub):
    """
    - Subscribe to ErrorHandlingTest.Subscribe_RaiseDefinedExecutionErrorOnSubscribe
    - Expect that reading the first value fails with the Defined Execution Error 'TestError' and the error message
        "SiLA2_test_error_message"
    """
    stream = errorhandlingtest_stub.Subscribe_RaiseDefinedExecutionErrorOnSubscribe(
        ErrorHandlingTest_pb2.Subscribe_RaiseDefinedExecutionErrorOnSubscribe_Parameters()
    )
    with raises_defined_execution_error(
        "org.silastandard/test/ErrorHandlingTest/v1/DefinedExecutionError/TestError"
    ) as error:
        next(stream)
    assert error.error.message == "SiLA2_test_error_message"


def test_raise_undefined_execution_error_on_subscribe(errorhandlingtest_stub):
    """
    - Subscribe to ErrorHandlingTest.Subscribe_RaiseDefinedExecutionErrorOnSubscribe
    - Expect that reading the first value fails with an Undefined Execution Error and the error message
        "SiLA2_test_error_message"
    """
    stream = errorhandlingtest_stub.Subscribe_RaiseUndefinedExecutionErrorOnSubscribe(
        ErrorHandlingTest_pb2.Subscribe_RaiseUndefinedExecutionErrorOnSubscribe_Parameters()
    )
    with raises_undefined_execution_error() as error:
        next(stream)
    assert error.error.message == "SiLA2_test_error_message"


def test_raise_defined_execution_error_after_value_was_sent(errorhandlingtest_stub):
    """
    - Subscribe to ErrorHandlingTest.Subscribe_RaiseDefinedExecutionErrorAfterValueWasSent
    - Expect that reading the first value yields the integer 1
    - Expect that reading the second value fails with the Defined Execution Error 'TestError' and the error message
        "SiLA2_test_error_message"
    """
    stream = errorhandlingtest_stub.Subscribe_RaiseDefinedExecutionErrorAfterValueWasSent(
        ErrorHandlingTest_pb2.Subscribe_RaiseDefinedExecutionErrorAfterValueWasSent_Parameters()
    )
    assert next(stream).RaiseDefinedExecutionErrorAfterValueWasSent.value == 1

    with raises_defined_execution_error(
        "org.silastandard/test/ErrorHandlingTest/v1/DefinedExecutionError/TestError"
    ) as error:
        next(stream)
    assert error.error.message == "SiLA2_test_error_message"


def test_raise_undefined_execution_error_after_value_was_sent(errorhandlingtest_stub):
    """
    - Subscribe to ErrorHandlingTest.Subscribe_RaiseUndefinedExecutionErrorAfterValueWasSent
    - Expect that reading the first value yields the integer 1
    - Expect that reading the second value fails with an Undefined Execution Error and the error message
        "SiLA2_test_error_message"
    """
    stream = errorhandlingtest_stub.Subscribe_RaiseUndefinedExecutionErrorAfterValueWasSent(
        ErrorHandlingTest_pb2.Subscribe_RaiseUndefinedExecutionErrorAfterValueWasSent_Parameters()
    )
    assert next(stream).RaiseUndefinedExecutionErrorAfterValueWasSent.value == 1

    with raises_undefined_execution_error() as error:
        next(stream)
    assert error.error.message == "SiLA2_test_error_message"
