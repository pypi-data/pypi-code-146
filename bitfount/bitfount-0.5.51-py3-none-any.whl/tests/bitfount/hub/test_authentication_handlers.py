"""Tests for the authentication mechanism."""
from datetime import datetime, timedelta, timezone
import functools
from pathlib import Path
import re
from typing import Callable, Dict, Literal, Optional, Union, cast
from unittest.mock import Mock, PropertyMock, call

from _pytest.capture import CaptureFixture
from _pytest.logging import LogCaptureFixture
from dateutil.relativedelta import relativedelta
import jwt
import pytest
from pytest import fixture, raises
from pytest_lazyfixture import lazy_fixture
from pytest_mock import MockerFixture
import responses

from bitfount.hub.authentication_handlers import (
    _AUTHORIZATION_PENDING_ERROR,
    _DEFAULT_USERNAME,
    _DEVICE_CODE_GRANT_TYPE,
    _SLOW_DOWN_ERROR,
    _USERNAME_KEY,
    APIKeysHandler,
    DeviceCodeFlowHandler,
    ExternallyManagedJWTHandler,
)
from bitfount.hub.exceptions import AuthenticatedUserError
from bitfount.hub.types import (
    _DeviceAccessTokenRequestDict,
    _DeviceAccessTokenResponseJSON,
    _DeviceCodeRequestDict,
    _DeviceCodeResponseJSON,
    _TokenRefreshRequestDict,
)
from bitfount.utils import web_utils
from tests.utils.helper import get_warning_logs, unit_test


@fixture
def username() -> str:
    """Username."""
    return "someUsername"


@fixture
def auth_domain() -> str:
    """Authentication domain as fixture."""
    return "some.auth.domain.com"


@fixture
def client_id() -> str:
    """Auth token client ID fixture."""
    return "oljorknkjnio"


@fixture
def scopes() -> str:
    """Auth token scopes fixture."""
    return "spaced out list of scopes"


@fixture
def audience() -> str:
    """Auth token audience fixture."""
    return "some.api.domain.com"


@fixture
def user_storage_path(tmp_path: Path, username: str) -> Path:
    """Temporary directory to act as user's .bitfount directory."""
    user_storage_path = tmp_path / username
    user_storage_path.mkdir()
    return user_storage_path


@fixture
def token_file(user_storage_path: Path) -> Path:
    """Path to save/load tokens from."""
    return user_storage_path / ".token"


@fixture
def device_flow_handler_factory(
    audience: str,
    auth_domain: str,
    client_id: str,
    scopes: str,
    user_storage_path: Path,
    username: str,
) -> Callable[[], DeviceCodeFlowHandler]:
    """Factory to create and setup BitfountSession instance for tests."""

    def _factory() -> DeviceCodeFlowHandler:
        handler = DeviceCodeFlowHandler(
            auth_domain, client_id, scopes, audience, username
        )
        handler.user_storage_path = user_storage_path
        handler.token_file = user_storage_path / ".token"
        return handler

    return _factory


@fixture
def mock_webbrowser(mocker: MockerFixture) -> Mock:
    """Mock webbrowser import."""
    mock_webbrowser: Mock = mocker.patch(
        "bitfount.hub.authentication_handlers.webbrowser", autospec=True
    )
    return mock_webbrowser


@fixture
def mock_time(mocker: MockerFixture) -> Mock:
    """Mock time import."""
    mock_time: Mock = mocker.patch(
        "bitfount.hub.authentication_handlers.time", autospec=True
    )
    return mock_time


@fixture
def mock_datetime(mocker: MockerFixture) -> Mock:
    """Mock datetime import."""
    mock_datetime: Mock = mocker.patch(
        "bitfount.hub.authentication_handlers.datetime", autospec=True
    )
    return mock_datetime


@unit_test
class TestAuthenticationHandlers:
    """Tests for the custom BitfountSession."""

    @fixture
    def device_code_request(
        self, audience: str, client_id: str, scopes: str
    ) -> _DeviceCodeRequestDict:
        """Expected request data for /oauth/device/code."""
        return {"audience": audience, "scope": scopes, "client_id": client_id}

    @fixture
    def device_code_response(self) -> _DeviceCodeResponseJSON:
        """Expected response from /oauth/device/code."""
        return {
            "device_code": "Ag_EE...ko1p",
            "user_code": "QTZL-MCBW",
            "verification_uri": "https://accounts.acmetest.org/activate",
            "verification_uri_complete": "https://accounts.acmetest.org"
            "/activate?user_code=QTZL-MCBW",
            "expires_in": 900,
            "interval": 5,
        }

    @fixture
    def device_code(self) -> str:
        """Device code."""
        return "someDeviceCode"

    @fixture
    def access_token(self) -> str:
        """Access token."""
        return "someAccessToken"

    @fixture
    def token_request(
        self, client_id: str, device_code: str
    ) -> _DeviceAccessTokenRequestDict:
        """Expected request data for /oauth/token."""
        return {
            "client_id": client_id,
            "grant_type": _DEVICE_CODE_GRANT_TYPE,
            "device_code": device_code,
        }

    @fixture
    def token_response(self) -> _DeviceAccessTokenResponseJSON:
        """Expected response data from /oauth/token."""
        return {
            "access_token": "eyJz93a...k4laUWw",
            "id_token": "eyJ...0NE",
            "refresh_token": "eyJ...MoQ",
            "scope": "...",
            "expires_in": 86400,
            "token_type": "Bearer",
        }

    @fixture
    def refresh_token(self) -> str:
        """Refresh token."""
        return "someRefreshToken"

    @fixture
    def token_refresh_request(
        self, client_id: str, refresh_token: str
    ) -> _TokenRefreshRequestDict:
        """Expected request data for refresh request to /oauth/token."""
        return {
            "client_id": client_id,
            "grant_type": "refresh_token",
            "refresh_token": refresh_token,
        }

    @fixture
    def id_token_for_username(self, username: str) -> str:
        """The JWT ID token for username."""
        return jwt.encode({_USERNAME_KEY: username}, "Secret key", algorithm="HS256")

    @fixture
    def wrong_username(self) -> str:
        """An incorrect username to test validation logic with."""
        return "wrong_username"

    @fixture
    def id_token_for_wrong_username(self, wrong_username: str) -> str:
        """The JWT ID token for the wrong username."""
        return jwt.encode(
            {_USERNAME_KEY: wrong_username}, "Secret key", algorithm="HS256"
        )

    def test_api_keys_and_default_username_raises_error(
        self,
        username: str,
    ) -> None:
        """Tests that if using API keys username cannot be the default."""
        # Ensure session creation is done post-envvar setting
        with pytest.raises(
            AuthenticatedUserError, match="Must specify a username when using API Keys."
        ):
            APIKeysHandler(
                api_key_id="someApiKeyId",
                api_key="someApiKey",
                username=_DEFAULT_USERNAME,
            )

    @pytest.mark.parametrize(
        argnames=("error_expected", "id_token"),
        argvalues=(
            pytest.param(
                True,
                lazy_fixture("id_token_for_wrong_username"),
                id="wrong_user_authenticated",
            ),
            pytest.param(
                False,
                lazy_fixture("id_token_for_username"),
                id="correct_user_authenticated",
            ),
        ),
    )
    def test_username_property_validates_username(
        self,
        error_expected: bool,
        id_token: str,
        username: str,
    ) -> None:
        """Test that authenticated user is validated when retrieving username."""
        handler = DeviceCodeFlowHandler(username=username)
        handler.id_token = id_token

        if error_expected:
            with pytest.raises(AuthenticatedUserError):
                _ = handler.username
        else:
            assert handler.username == username

    def test_username_gets_username_from_token_if_default_username_provided(
        self,
        id_token_for_username: str,
        username: str,
    ) -> None:
        """Test that authenticated user is validated when retrieving username."""
        handler = DeviceCodeFlowHandler()
        handler.id_token = id_token_for_username

        assert handler.username == username

    def test_token_file_path(
        self,
        audience: str,
        auth_domain: str,
        client_id: str,
        scopes: str,
        username: str,
    ) -> None:
        """Tests that token file is in provided path."""
        session = DeviceCodeFlowHandler(
            auth_domain, client_id, scopes, audience, username
        )
        # Token file is the path provided with the token file specified
        assert session.token_file == session.user_storage_path / ".token"

    @responses.activate
    def test_fetch_device_code_stores_and_returns_required_values(
        self,
        auth_domain: str,
        device_code_request: _DeviceCodeRequestDict,
        device_code_response: _DeviceCodeResponseJSON,
        device_flow_handler_factory: Callable[[], DeviceCodeFlowHandler],
    ) -> None:
        """Checks that the needed attributes are stored from device code."""
        responses.add(
            responses.POST,
            f"https://{auth_domain}/oauth/device/code",
            json=device_code_response,
            match=[
                responses.matchers.urlencoded_params_matcher(
                    cast(Dict[str, str], device_code_request)
                )
            ],
        )

        handler = device_flow_handler_factory()
        user_code, verification_uri = handler._fetch_device_code()

        assert handler.device_code == device_code_response.get("device_code")
        assert handler.device_code_arrival_time is not None
        assert handler.device_code_expires_in == device_code_response.get("expires_in")
        assert handler.token_request_interval == device_code_response.get("interval")
        assert user_code == device_code_response["user_code"]
        assert verification_uri == device_code_response["verification_uri_complete"]

    def test_do_verification_opens_browser_correctly(
        self,
        mock_webbrowser: Mock,
        device_flow_handler_factory: Callable[[], DeviceCodeFlowHandler],
    ) -> None:
        """Checks that request to open browser works."""
        handler = device_flow_handler_factory()
        handler._do_verification("hello", "world")
        mock_webbrowser.open.assert_called_once_with("world")

    @responses.activate
    def test_exchange_device_code_for_token_eventually_receives_tokens(
        self,
        auth_domain: str,
        device_code: str,
        mock_time: Mock,
        token_request: _DeviceAccessTokenRequestDict,
        token_response: _DeviceAccessTokenResponseJSON,
        device_flow_handler_factory: Callable[[], DeviceCodeFlowHandler],
    ) -> None:
        """Checks that device code successfully exchanged for token."""
        handler = device_flow_handler_factory()
        handler.device_code = device_code
        handler.device_code_arrival_time = datetime.now(timezone.utc)
        handler.device_code_expires_in = 2
        handler.token_request_interval = 1

        responses.add(
            responses.POST,
            f"https://{auth_domain}/oauth/token",
            json={"error": _AUTHORIZATION_PENDING_ERROR},
            status=400,
            match=[
                responses.matchers.urlencoded_params_matcher(
                    cast(Dict[str, str], token_request)
                )
            ],
        )
        responses.add(
            responses.POST,
            f"https://{auth_domain}/oauth/token",
            json=token_response,
            status=200,
            match=[
                responses.matchers.urlencoded_params_matcher(
                    cast(Dict[str, str], token_request)
                )
            ],
        )

        handler._exchange_device_code_for_token()

        assert len(responses.calls) == 2
        assert handler._access_token == token_response["access_token"]
        assert handler.refresh_token == token_response["refresh_token"]
        assert handler.id_token == token_response["id_token"]

        assert handler.access_token_expires_at is not None
        assert handler.access_token_expires_at > datetime.now(timezone.utc)
        mock_time.sleep.assert_called_once_with(1)

    @responses.activate
    def test_exchange_device_code_for_token_eventually_receives_error(
        self,
        auth_domain: str,
        device_code: str,
        mock_time: Mock,
        token_request: _DeviceAccessTokenRequestDict,
        device_flow_handler_factory: Callable[[], DeviceCodeFlowHandler],
    ) -> None:
        """The token endpoint here eventually informs us that the user denied access."""
        handler = device_flow_handler_factory()
        handler.device_code = device_code
        handler.device_code_arrival_time = datetime.now(timezone.utc)
        handler.device_code_expires_in = 2
        handler.token_request_interval = 1

        responses.add(
            responses.POST,
            f"https://{auth_domain}/oauth/token",
            json={"error": _AUTHORIZATION_PENDING_ERROR},
            status=400,
            match=[
                responses.matchers.urlencoded_params_matcher(
                    cast(Dict[str, str], token_request)
                )
            ],
        )
        responses.add(
            responses.POST,
            f"https://{auth_domain}/oauth/token",
            json={"error": "access_denied"},
            status=400,
            match=[
                responses.matchers.urlencoded_params_matcher(
                    cast(Dict[str, str], token_request)
                )
            ],
        )

        with raises(ConnectionError):
            handler._exchange_device_code_for_token()

        assert len(responses.calls) == 2
        assert handler._access_token is None
        assert handler.refresh_token is None
        assert handler.id_token is None
        assert handler.access_token_expires_at is None
        assert all(map(lambda x: x == call(1), mock_time.sleep.call_args_list))

    @responses.activate
    def test_exchange_device_code_for_token_never_receives_tokens(
        self,
        auth_domain: str,
        device_code: str,
        mock_datetime: Mock,
        mock_time: Mock,
        token_request: _DeviceAccessTokenRequestDict,
        device_flow_handler_factory: Callable[[], DeviceCodeFlowHandler],
    ) -> None:
        """The token endpoint here never issues tokens, so the device code expires."""
        handler = device_flow_handler_factory()
        handler.device_code = device_code
        handler.device_code_arrival_time = datetime(2020, 1, 14, tzinfo=timezone.utc)
        handler.device_code_expires_in = 300
        handler.token_request_interval = 1

        mock_datetime.now.side_effect = [
            datetime(2020, 1, 14, minute=x, tzinfo=timezone.utc)
            for x in range(0, 60, 2)
        ]

        auth_server_response = {"error": _AUTHORIZATION_PENDING_ERROR}

        responses.add(
            responses.POST,
            f"https://{auth_domain}/oauth/token",
            json=auth_server_response,
            status=400,
            match=[
                responses.matchers.urlencoded_params_matcher(
                    cast(Dict[str, str], token_request)
                )
            ],
        )

        with raises(ConnectionError):
            handler._exchange_device_code_for_token()

        assert len(responses.calls) == 3

        assert all(map(lambda x: x == call(1), mock_time.sleep.call_args_list))
        assert len(mock_time.sleep.call_args_list) == 3

        assert handler._access_token is None
        assert handler.refresh_token is None
        assert handler.id_token is None
        assert handler.access_token_expires_at is None

    @responses.activate
    def test_exchange_device_code_for_token_receives_slow_down(
        self,
        auth_domain: str,
        caplog: LogCaptureFixture,
        capsys: CaptureFixture,
        device_code: str,
        mock_time: Mock,
        token_request: _DeviceAccessTokenRequestDict,
        token_response: _DeviceAccessTokenResponseJSON,
        device_flow_handler_factory: Callable[[], DeviceCodeFlowHandler],
    ) -> None:
        """Test interval increased if receive slow down response."""
        handler = device_flow_handler_factory()
        # Set relevant attributes on session
        handler.device_code = device_code
        handler.device_code_arrival_time = datetime.now(timezone.utc)
        handler.device_code_expires_in = 300
        handler.token_request_interval = 1

        # First and second responses are "slow down"
        for _ in range(2):
            responses.add(
                responses.POST,
                f"https://{auth_domain}/oauth/token",
                json={"error": _SLOW_DOWN_ERROR},
                status=400,
                match=[
                    responses.matchers.urlencoded_params_matcher(
                        cast(Dict[str, str], token_request)
                    )
                ],
            )
        # Final response is correct response
        responses.add(
            responses.POST,
            f"https://{auth_domain}/oauth/token",
            json=token_response,
            status=200,
            match=[
                responses.matchers.urlencoded_params_matcher(
                    cast(Dict[str, str], token_request)
                )
            ],
        )

        handler._exchange_device_code_for_token()

        # Check warning logs for interval notes
        warning_logs = get_warning_logs(caplog)
        assert (
            "Polling too quickly; increasing interval from 1 to 2 seconds"
            in warning_logs
        )
        assert (
            "Polling too quickly; increasing interval from 2 to 3 seconds"
            in warning_logs
        )
        # Check stdout for increased interval waits
        stdout = capsys.readouterr().out
        assert (
            "Awaiting authentication in browser. Will check again in 1 seconds."
            not in stdout
        )
        assert (
            "Awaiting authentication in browser. Will check again in 2 seconds."
            in stdout
        )
        assert (
            "Awaiting authentication in browser. Will check again in 3 seconds."
            in stdout
        )

        # Check correct number of requests made
        assert len(responses.calls) == 3

        # Check sleep called with updated intervals
        assert mock_time.sleep.call_args_list == [call(2), call(3)]

    @pytest.mark.parametrize(
        argnames=("content_type", "content_value", "expected_error_msg", "in_stdout"),
        argvalues=(
            pytest.param(
                "json",
                {},
                'An unexpected error occurred: status code: 404; "{}"',
                True,
                id="incorrect json",
            ),
            pytest.param(
                "body",
                "error but not necessarily json",
                (
                    "Received 404 status response, but JSON is invalid: "
                    '"error but not necessarily json"'
                ),
                False,
                id="non-json response",
            ),
        ),
    )
    @responses.activate
    def test_exchange_device_code_for_token_receives_non_400_error(
        self,
        auth_domain: str,
        caplog: LogCaptureFixture,
        capsys: CaptureFixture,
        content_type: Literal["json", "body"],
        content_value: Union[dict, str],
        device_code: str,
        expected_error_msg: str,
        in_stdout: bool,
        mock_time: Mock,
        remove_web_retry_backoff_sleep: Optional[Mock],
        token_request: _DeviceAccessTokenRequestDict,
        token_response: _DeviceAccessTokenResponseJSON,
        device_flow_handler_factory: Callable[[], DeviceCodeFlowHandler],
    ) -> None:
        """Test error raised if receive non-400 error response."""
        # Check retry backoff is patched
        assert remove_web_retry_backoff_sleep is not None

        handler = device_flow_handler_factory()

        # Set relevant attributes on session
        handler.device_code = device_code
        handler.device_code_arrival_time = datetime.now(timezone.utc)
        handler.device_code_expires_in = 300
        handler.token_request_interval = 1

        partial_response_add = functools.partial(
            responses.add,
            responses.POST,
            f"https://{auth_domain}/oauth/token",
            status=404,
            match=[
                responses.matchers.urlencoded_params_matcher(
                    cast(Dict[str, str], token_request)
                )
            ],
        )
        if content_type == "json":
            partial_response_add(json=content_value)
        else:
            partial_response_add(body=content_value)

        with pytest.raises(
            ConnectionError,
            match="Failed to retrieve a device code from the authentication server",
        ):
            handler._exchange_device_code_for_token()

        # Check logger/stdout for errors
        assert expected_error_msg in caplog.text
        if in_stdout:
            assert expected_error_msg in capsys.readouterr().out

        # Check retries occurred
        assert (
            remove_web_retry_backoff_sleep.call_count == web_utils._DEFAULT_MAX_RETRIES
        )

    def test_device_flow_handler_authenticates_when_no_token_loaded(
        self,
        mocker: MockerFixture,
        username: str,
        device_flow_handler_factory: Callable[[], DeviceCodeFlowHandler],
    ) -> None:
        """Checks that token requested and saved when none exists to load."""
        handler = device_flow_handler_factory()
        mock_fetch_device_code = mocker.patch.object(
            handler, "_fetch_device_code", return_value=(1, 2)
        )
        mock_do_verification = mocker.patch.object(handler, "_do_verification")
        mock_exchange_device_code = mocker.patch.object(
            handler, "_exchange_device_code_for_token"
        )
        mock_save_token = mocker.patch.object(handler, "_save_token_to_file")
        mocker.patch.object(
            handler, "_get_username_from_id_token", return_value=username
        )

        handler.authenticate()

        mock_fetch_device_code.assert_called_once()
        mock_do_verification.assert_called_once_with(1, 2)
        mock_exchange_device_code.assert_called_once()
        mock_save_token.assert_called_once_with(handler.token_file)

    def test_authenticate_validates_username(
        self,
        id_token_for_wrong_username: str,
        mocker: MockerFixture,
        username: str,
        wrong_username: str,
        device_flow_handler_factory: Callable[[], DeviceCodeFlowHandler],
    ) -> None:
        """Test that authenticate() validates username against authenticated user."""
        handler = device_flow_handler_factory()
        mock_fetch_device_code = mocker.patch.object(
            handler, "_fetch_device_code", autospec=True, return_value=(1, 2)
        )
        mock_do_verification = mocker.patch.object(
            handler, "_do_verification", autospec=True
        )

        # Make it so the call to _exchange_device_code_for_token()
        # sets the _wrong_ id token
        def _set_id_token() -> None:
            handler.id_token = id_token_for_wrong_username

        mock_exchange_device_code = mocker.patch.object(
            handler,
            "_exchange_device_code_for_token",
            autospec=True,
            side_effect=lambda: _set_id_token(),
        )

        with pytest.raises(
            AuthenticatedUserError,
            match=(
                f"DeviceCodeFlowHandler object was created for {username}"
                f" but authentication was done against {wrong_username}"
            ),
        ):
            handler.authenticate()

        mock_fetch_device_code.assert_called_once()
        mock_do_verification.assert_called_once_with(1, 2)
        mock_exchange_device_code.assert_called_once()

    def test_device_code_flow_handler_authenticates_when_token_loaded_but_expired(
        self,
        access_token: str,
        id_token_for_username: str,
        mocker: MockerFixture,
        refresh_token: str,
        token_file: Path,
        device_flow_handler_factory: Callable[[], DeviceCodeFlowHandler],
    ) -> None:
        """Checks that a new token is fetched via the login flow.

        This is the case where the loaded token has expired completely.
        """
        handler = device_flow_handler_factory()
        # Create saved token
        handler._access_token = access_token
        handler.access_token_expires_at = datetime(
            year=2000, month=6, day=13, tzinfo=timezone.utc
        )
        handler.id_token = id_token_for_username
        handler.refresh_token = refresh_token
        handler._save_token_to_file(token_file)

        # Reset handler to initial state
        handler._access_token = None
        handler.access_token_expires_at = None
        handler.id_token = None
        handler.refresh_token = None

        mocker.patch.object(handler, "_refresh_access_token", return_value=False)
        mock_fetch_device_code = mocker.patch.object(
            handler, "_fetch_device_code", return_value=(1, 2)
        )
        mock_do_verification = mocker.patch.object(handler, "_do_verification")
        mock_exchange_device_code = mocker.patch.object(
            handler, "_exchange_device_code_for_token"
        )

        handler.authenticate()

        mock_fetch_device_code.assert_called_once()
        mock_do_verification.assert_called_once_with(1, 2)
        mock_exchange_device_code.assert_called_once()

    def test_device_code_flow_handler_refreshes_when_token_loaded_but_expired(
        self,
        access_token: str,
        id_token_for_username: str,
        mocker: MockerFixture,
        refresh_token: str,
        token_file: Path,
        device_flow_handler_factory: Callable[[], DeviceCodeFlowHandler],
    ) -> None:
        """Checks that a new token is fetched using the refresh mechanism.

        This is for when the loaded token has expired,
        but the refresh token is still valid
        """
        handler = device_flow_handler_factory()
        # Create saved token
        handler._access_token = access_token
        handler.access_token_expires_at = datetime(
            year=2000, month=6, day=13, tzinfo=timezone.utc
        )
        handler.id_token = id_token_for_username
        handler.refresh_token = refresh_token
        handler._save_token_to_file(token_file)

        # Reset handler to initial state
        handler._access_token = None
        handler.access_token_expires_at = None
        handler.id_token = None
        handler.refresh_token = None

        mock_refresh_access_token = mocker.patch.object(
            handler, "_refresh_access_token"
        )
        mock_fetch_device_code = mocker.patch.object(handler, "_fetch_device_code")
        mock_do_verification = mocker.patch.object(handler, "_do_verification")
        mock_exchange_device_code = mocker.patch.object(
            handler, "_exchange_device_code_for_token"
        )

        handler.authenticate()

        # Ensure refresh was called
        mock_refresh_access_token.assert_called_once()
        # Ensure manual login flow is not run
        mock_fetch_device_code.assert_not_called()
        mock_do_verification.assert_not_called()
        mock_exchange_device_code.assert_not_called()

    def test_device_code_flow_handler_authenticated_when_valid_token_loaded(
        self,
        access_token: str,
        id_token_for_username: str,
        mocker: MockerFixture,
        refresh_token: str,
        token_file: Path,
        device_flow_handler_factory: Callable[[], DeviceCodeFlowHandler],
    ) -> None:
        """Checks that authentication is successful when token loaded from file."""
        handler = device_flow_handler_factory()
        # Create saved token
        handler._access_token = access_token
        # Timestamp for 1 month from now
        handler.access_token_expires_at = datetime.now(timezone.utc) + relativedelta(
            months=1
        )
        handler.id_token = id_token_for_username
        handler.refresh_token = refresh_token
        handler._save_token_to_file(token_file)

        # Reset handler to initial state
        handler._access_token = None
        handler.access_token_expires_at = None
        handler.id_token = None
        handler.refresh_token = None

        mock_fetch_device_code = mocker.patch.object(handler, "_fetch_device_code")
        mock_exchange_device_code = mocker.patch.object(
            handler, "_exchange_device_code_for_token"
        )

        handler.authenticate()

        mock_fetch_device_code.assert_not_called()
        mock_exchange_device_code.assert_not_called()

    def test_device_code_flow_handler_doesnt_use_loaded_token_when_metadata_differs(
        self,
        access_token: str,
        id_token_for_username: str,
        mocker: MockerFixture,
        refresh_token: str,
        token_file: Path,
        user_storage_path: Path,
        device_flow_handler_factory: Callable[[], DeviceCodeFlowHandler],
    ) -> None:
        """Test handler will create & save a new token when different."""
        handler = device_flow_handler_factory()

        # Create saved token
        old_handler_configuration = DeviceCodeFlowHandler(
            "someOtherDomain.com",
            "not our client id",
            "someUsername",
            "not our scopes",
            "someOtherAudience",
        )
        old_handler_configuration.user_storage_path = user_storage_path
        old_handler_configuration._access_token = access_token
        # Timestamp for 1 month from now
        old_handler_configuration.access_token_expires_at = datetime.now(
            timezone.utc
        ) + relativedelta(months=1)
        handler.id_token = id_token_for_username
        old_handler_configuration.refresh_token = refresh_token
        old_handler_configuration._save_token_to_file(token_file)

        mock_fetch_device_code = mocker.patch.object(
            handler, "_fetch_device_code", return_value=(1, 2)
        )
        mock_do_verification = mocker.patch.object(handler, "_do_verification")
        mock_exchange_device_code = mocker.patch.object(
            handler, "_exchange_device_code_for_token"
        )
        mock_save_token = mocker.patch.object(handler, "_save_token_to_file")

        handler.authenticate()

        mock_fetch_device_code.assert_called_once()
        mock_do_verification.assert_called_once_with(1, 2)
        mock_exchange_device_code.assert_called_once()
        mock_save_token.assert_called_once_with(token_file)

    @responses.activate
    def test_send_token_request_to_refresh_expired_token(
        self,
        auth_domain: str,
        refresh_token: str,
        token_refresh_request: _TokenRefreshRequestDict,
        device_flow_handler_factory: Callable[[], DeviceCodeFlowHandler],
    ) -> None:
        """Checks _send_token_request works with refresh=True."""
        handler = device_flow_handler_factory()
        handler.refresh_token = refresh_token

        auth_server_response = {"some": "response"}

        responses.add(
            responses.POST,
            f"https://{auth_domain}/oauth/token",
            json=auth_server_response,
            match=[
                responses.matchers.urlencoded_params_matcher(
                    cast(Dict[str, str], token_refresh_request)
                )
            ],
        )

        response = handler._send_token_request(refresh=True)

        assert response.json() == auth_server_response

    @responses.activate
    def test_send_token_request_as_device_code(
        self,
        auth_domain: str,
        client_id: str,
        device_code: str,
        token_request: _DeviceAccessTokenRequestDict,
        device_flow_handler_factory: Callable[[], DeviceCodeFlowHandler],
    ) -> None:
        """Checks that _send_token_request works correctly."""
        handler = device_flow_handler_factory()
        handler.device_code = device_code

        auth_server_response = {"some": "response"}

        responses.add(
            responses.POST,
            f"https://{auth_domain}/oauth/token",
            json=auth_server_response,
            match=[
                responses.matchers.urlencoded_params_matcher(
                    cast(Dict[str, str], token_request)
                )
            ],
        )

        response = handler._send_token_request()

        assert response.json() == auth_server_response

    def test_get_username_from_id_token(
        self,
        id_token_for_username: str,
        username: str,
        device_flow_handler_factory: Callable[[], DeviceCodeFlowHandler],
    ) -> None:
        """Tests username can be extracted from ID Token."""
        handler = device_flow_handler_factory()
        handler.id_token = id_token_for_username

        assert handler._get_username_from_id_token() == username

    def test_get_username_from_id_token_raises_error_if_no_id_token(
        self, device_flow_handler_factory: Callable[[], DeviceCodeFlowHandler]
    ) -> None:
        """Tests error raised if no id token when trying to extract username."""
        handler = device_flow_handler_factory()

        with pytest.raises(
            AuthenticatedUserError,
            match=re.escape(
                "User not authenticated yet,"
                " call authenticate() before accessing the ID token"
            ),
        ):
            handler._get_username_from_id_token()

    @pytest.mark.parametrize(
        "_username, assertion_error",
        [(lazy_fixture("username"), False), ("not-real-username", True)],
    )
    def test__verify_user_storage_path(
        self,
        _username: str,
        assertion_error: bool,
        mocker: MockerFixture,
        device_flow_handler_factory: Callable[[], DeviceCodeFlowHandler],
    ) -> None:
        """Tests that token won't be saved in a directory with a different username."""
        handler = device_flow_handler_factory()

        mocker.patch.object(
            DeviceCodeFlowHandler, "username", PropertyMock(return_value=_username)
        )

        if assertion_error:
            with pytest.raises(AuthenticatedUserError):
                handler._verify_user_storage_path()
        else:
            handler._verify_user_storage_path()

    def test_hub_request_headers_returns_token(
        self, device_flow_handler_factory: Callable[[], DeviceCodeFlowHandler]
    ) -> None:
        """Tests that the Hub request headers are in the correct format."""
        expected_access_token = "someAccessToken"
        handler = device_flow_handler_factory()
        handler._access_token = expected_access_token

        assert handler.hub_request_headers == {
            "authorization": f"Bearer {expected_access_token}"
        }

    def test_am_request_headers_returns_token(
        self, device_flow_handler_factory: Callable[[], DeviceCodeFlowHandler]
    ) -> None:
        """Tests that the AM request headers are in the correct format."""
        expected_access_token = "someAccessToken"
        handler = device_flow_handler_factory()
        handler._access_token = expected_access_token

        assert handler.am_request_headers == {
            "authorization": f"Bearer {expected_access_token}"
        }

    def test_message_service_request_metadata_returns_token(
        self, device_flow_handler_factory: Callable[[], DeviceCodeFlowHandler]
    ) -> None:
        """Tests that the message service request metadata is in the correct format."""
        expected_access_token = "someAccessToken"
        handler = device_flow_handler_factory()
        handler._access_token = expected_access_token

        assert handler.message_service_request_metadata == [
            ("token", expected_access_token)
        ]


@unit_test
class TestAPIKeyAuthenticationHandler:
    """Tests the API Key authentication handler."""

    @fixture
    def hub_api_key_id(self) -> str:
        """Mock Hub API Key ID."""
        return "HubApiID"

    @fixture
    def api_key_id(self, hub_api_key_id: str) -> str:
        """Mock API Key ID."""
        return f"{hub_api_key_id}:AMApiKeyID"

    @fixture
    def hub_api_key(self) -> str:
        """Mock Hub API Key."""
        return "HubApiKey"

    @fixture
    def api_key(self, hub_api_key: str) -> str:
        """Mock API Key."""
        return f"{hub_api_key}:AMApiKey"

    def test_get_hub_request_headers(
        self,
        api_key_id: str,
        api_key: str,
        username: str,
        hub_api_key_id: str,
        hub_api_key: str,
    ) -> None:
        """Test Hub request headers are formatted correctly."""
        handler = APIKeysHandler(api_key_id, api_key, username)

        assert handler.hub_request_headers == {
            "x-api-key-id": hub_api_key_id,
            "x-api-key": hub_api_key,
        }

    def test_get_am_request_headers(
        self, api_key_id: str, api_key: str, username: str
    ) -> None:
        """Test AM request headers are formatted correctly."""
        handler = APIKeysHandler(api_key_id, api_key, username)

        assert handler.am_request_headers == {
            "x-api-key-id": api_key_id,
            "x-api-key": api_key,
        }

    def test_get_message_service_request_metadata(
        self,
        api_key_id: str,
        api_key: str,
        username: str,
        hub_api_key_id: str,
        hub_api_key: str,
    ) -> None:
        """Test message service request metadata are formatted correctly."""
        handler = APIKeysHandler(api_key_id, api_key, username)

        assert handler.message_service_request_metadata == [
            ("x-api-key-id", hub_api_key_id),
            ("x-api-key", hub_api_key),
        ]

    def test_authenticated_returns_true_always(
        self, api_key_id: str, api_key: str, username: str
    ) -> None:
        """Tests authenticated returns True."""
        handler = APIKeysHandler(api_key_id, api_key, username)

        assert handler.authenticated is True

    def test_username_returns_set_username(
        self, api_key_id: str, api_key: str, username: str
    ) -> None:
        """Tests username can be retrieved."""
        handler = APIKeysHandler(api_key_id, api_key, username)

        assert handler.username == username


@unit_test
class TestExternallyManagedJWTHandler:
    """Tests external JWT authentication handler."""

    @fixture
    def jwt(self) -> str:
        """Mocked JWT."""
        return "totallyAJWT"

    @fixture
    def expires(self) -> datetime:
        """Mocked token expiry."""
        return datetime.now()

    def test_creation_with_default_username_throws_error(
        self, jwt: str, expires: datetime
    ) -> None:
        """Tests specific username must be provided."""
        with pytest.raises(AuthenticatedUserError):
            ExternallyManagedJWTHandler(
                jwt, expires, lambda: (jwt, expires), _DEFAULT_USERNAME
            )

    def test_hub_request_headers(
        self, jwt: str, expires: datetime, username: str
    ) -> None:
        """Tests hub request headers are correctly formatted."""
        handler = ExternallyManagedJWTHandler(
            jwt, expires, lambda: (jwt, expires), username
        )

        assert handler.hub_request_headers == {"authorization": f"Bearer {jwt}"}

    def test_am_request_headers(
        self, jwt: str, expires: datetime, username: str
    ) -> None:
        """Tests am request headers are correctly formatted."""
        handler = ExternallyManagedJWTHandler(
            jwt, expires, lambda: (jwt, expires), username
        )

        assert handler.am_request_headers == {"authorization": f"Bearer {jwt}"}

    def test_message_service_request_metadata(
        self, jwt: str, expires: datetime, username: str
    ) -> None:
        """Tests message service request metadata is correctly formatted."""
        handler = ExternallyManagedJWTHandler(
            jwt, expires, lambda: (jwt, expires), username
        )

        assert handler.message_service_request_metadata == [("token", jwt)]

    def test_get_set_username(self, jwt: str, expires: datetime, username: str) -> None:
        """Tests username can be retrieved."""
        handler = ExternallyManagedJWTHandler(
            jwt, expires, lambda: (jwt, expires), username
        )

        assert handler.username == username

    def test_authenticate_calls_get_token_hook(
        self, jwt: str, expires: datetime, username: str
    ) -> None:
        """Tests new token requested when existing one expired.."""
        new_jwt = "newJWT"
        new_expiry = datetime.now()
        hook = Mock(return_value=(new_jwt, new_expiry))
        handler = ExternallyManagedJWTHandler(jwt, expires, hook, username)

        handler.authenticate()

        hook.assert_called_once()
        assert handler._jwt == new_jwt
        assert handler._expires == new_expiry

    @pytest.mark.parametrize(
        "expiry,authenticated",
        [
            (datetime.now(timezone.utc) + timedelta(days=1), True),
            (datetime.now(timezone.utc) - timedelta(days=1), False),
        ],
    )
    def test_token_expiry(
        self, jwt: str, username: str, expiry: datetime, authenticated: bool
    ) -> None:
        """Tests authenticated property."""
        handler = ExternallyManagedJWTHandler(
            jwt, expiry, lambda: (jwt, expiry), username
        )

        assert handler.authenticated == authenticated
