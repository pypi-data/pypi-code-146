import grpc

from sila2_interop_communication_tester.test_server.helpers.spy import ServerCall


def assert_init_and_result_call(command_id: str, server_calls: dict[str, list[ServerCall]]):
    """
    Assert an observable command was initiated and the result was requested afterwards

    :param command_id: FeatureIdentifier.CommandIdentifier, e.g. "GreetingProvider.SayHello"
    :param server_calls: The server calls, like the pytest fixture
    """
    init_calls = server_calls[command_id]
    execution_ids: list[str] = [call.result.commandExecutionUUID.value for call in init_calls]
    assert len(init_calls) > 0, f"Client did not call {command_id}"

    info_calls = server_calls[command_id + "_Result"]
    assert any(
        call.request.value in execution_ids for call in info_calls
    ), f"Client did not call {command_id}_Result with a valid execution UUID"


def test_raise_defined_execution_error_called(server_calls):
    assert server_calls["ErrorHandlingTest.RaiseDefinedExecutionError"]


def test_raise_defined_execution_error_observably_collected(server_calls):
    assert_init_and_result_call("ErrorHandlingTest.RaiseDefinedExecutionErrorObservably", server_calls)


def test_raise_undefined_execution_error_called(server_calls):
    assert server_calls["ErrorHandlingTest.RaiseUndefinedExecutionError"]


def test_raise_undefined_execution_error_observably_collected(server_calls):
    assert_init_and_result_call("ErrorHandlingTest.RaiseUndefinedExecutionErrorObservably", server_calls)


def test_raise_defined_execution_error_on_get_accessed(server_calls):
    assert server_calls["ErrorHandlingTest.Get_RaiseDefinedExecutionErrorOnGet"]


def test_raise_defined_execution_error_on_subscribe_subscribe(server_calls):
    assert server_calls["ErrorHandlingTest.Subscribe_RaiseDefinedExecutionErrorOnSubscribe"]


def test_raise_undefined_execution_error_on_get_accessed(server_calls):
    assert server_calls["ErrorHandlingTest.Get_RaiseUndefinedExecutionErrorOnGet"]


def test_raise_undefined_execution_error_on_subscribe_subscribe(server_calls):
    assert server_calls["ErrorHandlingTest.Subscribe_RaiseUndefinedExecutionErrorOnSubscribe"]


def test_raise_defined_execution_error_after_value_was_sent(server_calls):
    calls = server_calls["ErrorHandlingTest.Subscribe_RaiseDefinedExecutionErrorAfterValueWasSent"]
    assert any(
        call
        for call in calls
        if len(call.result.streamed_responses) == 1 and call.result.code == grpc.StatusCode.ABORTED
    )


def test_raise_undefined_execution_error_after_value_was_sent(server_calls):
    calls = server_calls["ErrorHandlingTest.Subscribe_RaiseUndefinedExecutionErrorAfterValueWasSent"]
    assert any(
        call
        for call in calls
        if len(call.result.streamed_responses) == 1 and call.result.code == grpc.StatusCode.ABORTED
    )
