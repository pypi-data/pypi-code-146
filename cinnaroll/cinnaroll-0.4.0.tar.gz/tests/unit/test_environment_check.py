import os
from typing import Optional

import pytest
from unittest import mock

import requests

from cinnaroll_internal import environment_check

get_api_key_from_file_cases = [
    ["[default]\n" '"API Key" = "123abc"', "123abc"],
    ["", ""],
    ["[123]\n" '"API Key" = "123abc"', ""],
]


@pytest.mark.parametrize(
    "input_file_content, expected_output", get_api_key_from_file_cases
)
def test_get_api_key_from_toml_file_content(
    input_file_content: str, expected_output: str
) -> None:
    with mock.patch("builtins.open", mock.mock_open(read_data=input_file_content)):
        actual_output = environment_check.get_api_key_from_toml_file_content(
            input_file_content
        )
        assert expected_output == actual_output


# todo: check if any of this is still useful and uncomment
@mock.patch.dict(os.environ, {"CINNAROLL_API_KEY": "abc123"})
@mock.patch("cinnaroll_internal.environment_check.requests.get")
def test_find_api_key_error_when_key_is_present_and_api_returned_401(mock_get: mock.MagicMock) -> None:
    mock_get.return_value.status_code = requests.status_codes.codes.unauthorized
    err: Optional[Exception] = environment_check.find_api_key_error()
    assert isinstance(err, environment_check.WrongAPIKeyError)


@mock.patch.dict(os.environ, {"CINNAROLL_API_KEY": "abc123"})
@mock.patch("cinnaroll_internal.environment_check.requests.get")
def test_find_api_key_error_when_key_is_present_and_api_returned_200(mock_get: mock.MagicMock) -> None:
    mock_get.return_value.status_code = requests.status_codes.codes.ok
    err: Optional[Exception] = environment_check.find_api_key_error()
    assert err is None


@mock.patch.dict(os.environ, {"CINNAROLL_API_KEY": "abc123"})
@mock.patch("cinnaroll_internal.environment_check.requests.get")
def test_find_api_key_error_when_key_is_present_and_request_error_happened(mock_get: mock.MagicMock) -> None:
    mock_get.side_effect = requests.ConnectTimeout()
    err: Optional[Exception] = environment_check.find_api_key_error()
    assert err is None


# todo: move this back to the end of file
# @mock.patch.dict(os.environ, {"CINNAROLL_API_KEY": "abc123"})
# @mock.patch("cinnaroll_internal.environment_check.requests.get")
# def test_find_environment_errors_when_multiple_errors_should_be_raised(mock_get: mock.MagicMock) -> None:
#     with mock.patch('builtins.open', mock.mock_open()) as mock_file:
#         mock_file.side_effect = PermissionError()
#         mock_get.return_value.status_code = requests.status_codes.codes.unauthorized
#
#         errors = environment_check.find_environment_errors()
#         expected_errors = [
#             environment_check.DisallowedWriteError(
#                 f"Can’t save files in current working directory ({os.getcwd()}). "
#                 f"Ensure you have write permissions to it."),
#             environment_check.WrongAPIKeyError('API Key is wrong. Has it been pasted correctly?')
#         ]
#
#         utils.assert_contains_exceptions(expected_errors, errors)


# @mock.patch("os.access")
# def test_find_disallowed_write_error_when_cwd_is_not_writable(
#     mock_access: MagicMock,
# ) -> None:
#     mock_access.return_value = False
#     err = environment_check.find_disallowed_write_error()
#     assert isinstance(err, environment_check.DisallowedWriteError)
#
#
# @mock.patch("os.access")
# def test_find_disallowed_write_error_when_cwd_is_writable(
#     mock_access: MagicMock,
# ) -> None:
#     mock_access.return_value = True
#     err = environment_check.find_disallowed_write_error()
#     assert err is None
