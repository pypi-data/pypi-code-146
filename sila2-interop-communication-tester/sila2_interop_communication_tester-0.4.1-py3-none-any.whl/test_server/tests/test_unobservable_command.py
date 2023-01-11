def test_command_without_parameters_and_responses_called(server_calls):
    calls = server_calls["UnobservableCommandTest.CommandWithoutParametersAndResponses"]
    assert any(call.successful for call in calls)


def test_convert_integer_to_string_called_with_12345(server_calls):
    calls = server_calls["UnobservableCommandTest.ConvertIntegerToString"]
    assert any(call.request.Integer.value == 12345 for call in calls)


def test_join_integer_and_string_called_with_123_and_abc(server_calls):
    calls = server_calls["UnobservableCommandTest.JoinIntegerAndString"]
    assert any(call.request.Integer.value == 123 and call.request.String.value == "abc" for call in calls)


def test_split_string_after_first_character_called_with_empty_string(server_calls):
    calls = server_calls["UnobservableCommandTest.SplitStringAfterFirstCharacter"]
    assert any(call.request.String.value == "" for call in calls)


def test_split_string_after_first_character_called_with_a(server_calls):
    calls = server_calls["UnobservableCommandTest.SplitStringAfterFirstCharacter"]
    assert any(call.request.String.value == "a" for call in calls)


def test_split_string_after_first_character_called_with_ab(server_calls):
    calls = server_calls["UnobservableCommandTest.SplitStringAfterFirstCharacter"]
    assert any(call.request.String.value == "ab" for call in calls)


def test_split_string_after_first_character_called_with_abcde(server_calls):
    calls = server_calls["UnobservableCommandTest.SplitStringAfterFirstCharacter"]
    assert any(call.request.String.value == "abcde" for call in calls)
