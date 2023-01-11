from sila2_interop_communication_tester.grpc_stubs import SiLAFramework_pb2, UnobservableCommandTest_pb2
from sila2_interop_communication_tester.test_client.helpers.error_handling import raises_validation_error


def _split_after_first_character(stub, string: str) -> tuple[str, str]:
    response = stub.SplitStringAfterFirstCharacter(
        UnobservableCommandTest_pb2.SplitStringAfterFirstCharacter_Parameters(
            String=SiLAFramework_pb2.String(value=string)
        )
    )
    return response.FirstCharacter.value, response.Remainder.value


def test_command_without_parameters_and_responses(unobservablecommandtest_stub):
    unobservablecommandtest_stub.CommandWithoutParametersAndResponses(
        UnobservableCommandTest_pb2.CommandWithoutParametersAndResponses_Parameters()
    )


def test_convert_integer_to_string(unobservablecommandtest_stub):
    response = unobservablecommandtest_stub.ConvertIntegerToString(
        UnobservableCommandTest_pb2.ConvertIntegerToString_Parameters(Integer=SiLAFramework_pb2.Integer(value=12345))
    )
    assert "12345" == response.StringRepresentation.value


def test_convert_integer_to_string_detects_missing_parameter(unobservablecommandtest_stub):
    with raises_validation_error(
        "org.silastandard/test/UnobservableCommandTest/v1/Command/ConvertIntegerToString/Parameter/Integer"
    ):
        unobservablecommandtest_stub.ConvertIntegerToString(
            UnobservableCommandTest_pb2.ConvertIntegerToString_Parameters()
        )


def test_join_integer_and_string(unobservablecommandtest_stub):
    response = unobservablecommandtest_stub.JoinIntegerAndString(
        UnobservableCommandTest_pb2.JoinIntegerAndString_Parameters(
            Integer=SiLAFramework_pb2.Integer(value=123), String=SiLAFramework_pb2.String(value="abc")
        )
    )
    assert "123abc" == response.JoinedParameters.value


def test_join_integer_and_string_detects_missing_parameters(unobservablecommandtest_stub):
    with raises_validation_error(
        "org.silastandard/test/UnobservableCommandTest/v1/Command/JoinIntegerAndString/Parameter/Integer"
    ):
        unobservablecommandtest_stub.JoinIntegerAndString(
            UnobservableCommandTest_pb2.JoinIntegerAndString_Parameters(String=SiLAFramework_pb2.String(value="abc"))
        )
    with raises_validation_error(
        "org.silastandard/test/UnobservableCommandTest/v1/Command/JoinIntegerAndString/Parameter/String"
    ):
        unobservablecommandtest_stub.JoinIntegerAndString(
            UnobservableCommandTest_pb2.JoinIntegerAndString_Parameters(Integer=SiLAFramework_pb2.Integer(value=123))
        )


def test_split_after_first_character_with_empty_string(unobservablecommandtest_stub):
    assert ("", "") == _split_after_first_character(unobservablecommandtest_stub, "")


def test_split_after_first_character_with_a(unobservablecommandtest_stub):
    assert ("a", "") == _split_after_first_character(unobservablecommandtest_stub, "a")


def test_split_after_first_character_with_ab(unobservablecommandtest_stub):
    assert ("a", "b") == _split_after_first_character(unobservablecommandtest_stub, "ab")


def test_split_after_first_character_with_abcde(unobservablecommandtest_stub):
    assert ("a", "bcde") == _split_after_first_character(unobservablecommandtest_stub, "abcde")


def test_split_after_first_character_detects_missing_parameters(unobservablecommandtest_stub):
    with raises_validation_error(
        "org.silastandard/test/UnobservableCommandTest/v1/Command/SplitStringAfterFirstCharacter/Parameter/String"
    ):
        unobservablecommandtest_stub.SplitStringAfterFirstCharacter(
            UnobservableCommandTest_pb2.SplitStringAfterFirstCharacter_Parameters()
        )
