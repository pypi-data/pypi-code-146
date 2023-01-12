def test_answer_to_everything_requested(server_calls):
    calls = server_calls["UnobservablePropertyTest.Get_AnswerToEverything"]
    assert any(call.successful for call in calls)


def test_seconds_since_1970_requested(server_calls):
    calls = server_calls["UnobservablePropertyTest.Get_SecondsSince1970"]
    assert any(call.successful for call in calls)
