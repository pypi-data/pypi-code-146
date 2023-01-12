def test_fixed_subscription_is_read(server_calls):
    calls = server_calls["ObservablePropertyTest.Subscribe_FixedValue"]
    assert any(call for call in calls if len(call.result.streamed_responses) == 1)  # no update is sent -> cannot be > 1


def test_alternating_subscription_is_read_at_least_three_times(server_calls):
    calls = server_calls["ObservablePropertyTest.Subscribe_Alternating"]
    assert any(call for call in calls if len(call.result.streamed_responses) >= 3)


def test_editable_subscription_is_read_three_times(server_calls):
    calls = server_calls["ObservablePropertyTest.Subscribe_Editable"]
    assert any(
        call
        for call in calls
        if len(call.result.streamed_responses) >= 3  # updates are only sent via the command 'SetValue'
    )


def test_set_value_was_called_with_1_2_and_3(server_calls):
    calls = server_calls["ObservablePropertyTest.SetValue"]
    values: list[int] = [call.request.Value.value for call in calls]
    assert any(
        values[i : i + 3] == [1, 2, 3] for i in range(len(values) - 2)
    ), "SetValue was not called in sequence with the values 1, 2, and 3"
