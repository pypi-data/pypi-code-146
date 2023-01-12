from pytest import fail

from sila2_interop_communication_tester.grpc_stubs.ObservableCommandTest_pb2 import Count_IntermediateResponses
from sila2_interop_communication_tester.grpc_stubs.SiLAFramework_pb2 import ExecutionInfo


def test_count_called_with_value_5_and_delay_1(server_calls):
    assert any(
        call
        for call in server_calls["ObservableCommandTest.Count"]
        if call.request.N.value == 5 and call.request.Delay.value == 1
    )


def test_count_info_read_from_start_to_end(server_calls):
    calls = server_calls["ObservableCommandTest.Count_Info"]
    assert calls

    for call in calls:
        infos: list[ExecutionInfo] = call.result.streamed_responses
        if len(infos) > 3 and infos[-1].commandStatus == ExecutionInfo.CommandStatus.finishedSuccessfully:
            return
    fail("Count_Info was never subscribed to, read for at least 3 seconds, and read until the end of execution")


def test_count_intermediate_read_from_start_to_end(server_calls):
    calls = server_calls["ObservableCommandTest.Count_Intermediate"]
    assert calls

    for call in calls:
        responses: list[Count_IntermediateResponses] = call.result.streamed_responses
        if len(responses) > 3 and responses[0].CurrentIteration.value in (0, 1):
            return
    fail("Count_Intermediate was never subscribed to and read from start to finish")


def test_count_result_was_collected(server_calls):
    assert any(call.successful for call in server_calls["ObservableCommandTest.Count_Result"])


def test_echo_value_after_delay_called_with_value_3_and_delay_5(server_calls):
    assert any(
        call
        for call in server_calls["ObservableCommandTest.EchoValueAfterDelay"]
        if call.request.Value.value == 3 and call.request.Delay.value == 5
    )


def test_echo_value_after_delay_info_read_from_start_to_end(server_calls):
    calls = server_calls["ObservableCommandTest.EchoValueAfterDelay_Info"]
    assert calls

    for call in calls:
        infos: list[ExecutionInfo] = call.result.streamed_responses
        if len(infos) > 3 and infos[-1].commandStatus == ExecutionInfo.CommandStatus.finishedSuccessfully:
            return
    fail(
        "EchoValueAfterDelay_Info was never subscribed to, read for at least 3 seconds, "
        "and read until the end of execution"
    )


def test_echo_value_after_delay_result_was_collected(server_calls):
    assert any(call.successful for call in server_calls["ObservableCommandTest.EchoValueAfterDelay_Result"])
