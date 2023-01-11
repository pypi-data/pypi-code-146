from sila2_interop_communication_tester.grpc_stubs import ErrorHandlingTest_pb2
from sila2_interop_communication_tester.test_client.helpers.error_handling import (
    raises_defined_execution_error,
    raises_undefined_execution_error,
)


def test_raise_defined_execution_error(errorhandlingtest_stub):
    """
    Expect that executing ErrorHandlingTest.RaiseDefinedExecutionError fails with the Defined Execution Error
    'TestError' and the error message "SiLA2_test_error_message"
    """
    with raises_defined_execution_error(
        "org.silastandard/test/ErrorHandlingTest/v1/DefinedExecutionError/TestError"
    ) as error:
        errorhandlingtest_stub.RaiseDefinedExecutionError(ErrorHandlingTest_pb2.RaiseDefinedExecutionError_Parameters())
    assert error.error.message == "SiLA2_test_error_message"


def test_raise_undefined_execution_error(errorhandlingtest_stub):
    """
    Expect that executing ErrorHandlingTest.RaiseUndefinedExecutionError fails with an Undefined Execution Error
    and the error message "SiLA2_test_error_message"
    """
    with raises_undefined_execution_error() as error:
        errorhandlingtest_stub.RaiseUndefinedExecutionError(
            ErrorHandlingTest_pb2.RaiseUndefinedExecutionError_Parameters()
        )
    assert error.error.message == "SiLA2_test_error_message"
