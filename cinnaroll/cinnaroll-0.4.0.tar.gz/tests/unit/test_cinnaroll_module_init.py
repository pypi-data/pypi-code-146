import os
from unittest.mock import MagicMock

import pytest
from unittest import mock

import requests

import cinnaroll_internal.environment_check


@mock.patch("cinnaroll_internal.environment_check.requests.get")  # todo: uncomment
@mock.patch.dict(os.environ, {"CINNAROLL_API_KEY": ""})
def test_module_import_without_api_key(mock_get: MagicMock) -> None:  # todo: add mock_get: MagicMock to args
    with mock.patch("builtins.open", mock.mock_open()):
        with pytest.raises(
            cinnaroll_internal.environment_check.CinnarollEnvironmentConfigurationError
        ):
            mock_get.return_value.status_code = requests.status_codes.codes.ok   # todo: uncomment
            import cinnaroll


@mock.patch("cinnaroll_internal.environment_check.requests.get")  # todo: uncomment
@mock.patch.dict(os.environ, {"CINNAROLL_API_KEY": "abc123"})
def test_module_import_with_api_key_in_env(mock_get: MagicMock) -> None:  # todo: add mock_get: MagicMock to args
    with mock.patch("builtins.open", mock.mock_open()):
        mock_get.return_value.status_code = requests.status_codes.codes.ok  # todo: uncomment
        import cinnaroll
