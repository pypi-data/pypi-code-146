"""Tests for the authentication mechanism."""
from typing import Callable, Dict, List, Tuple, cast
from unittest.mock import PropertyMock, create_autospec

from _pytest.monkeypatch import MonkeyPatch
import pytest
from pytest import fixture
from pytest_lazyfixture import lazy_fixture
import responses

from bitfount.config import (
    _DEVELOPMENT_ENVIRONMENT,
    _PRODUCTION_ENVIRONMENT,
    _STAGING_ENVIRONMENT,
)
from bitfount.hub.authentication_flow import (
    _DEVELOPMENT_AUTH_DOMAIN,
    _DEVELOPMENT_CLIENT_ID,
    _PRODUCTION_AUTH_DOMAIN,
    _PRODUCTION_CLIENT_ID,
    _STAGING_AUTH_DOMAIN,
    _STAGING_CLIENT_ID,
    BitfountSession,
    _AuthEnv,
    _get_auth_environment,
)
from bitfount.hub.authentication_handlers import AuthenticationHandler
from tests.utils.helper import unit_test


@fixture
def username() -> str:
    """Username."""
    return "someUsername"


@fixture
def hub_request_metadata() -> Dict:
    """Access token."""
    return {"authorization": "someHubAccessToken"}


@fixture
def am_request_metadata() -> Dict:
    """Access token."""
    return {"authorization": "someAMAccessToken"}


@fixture
def message_service_metadata() -> List[Tuple[str, str]]:
    """Auth for message service."""
    return [("token", "someAccessToken")]


@fixture
def bitfount_session_factory(
    hub_request_metadata: Dict,
    am_request_metadata: Dict,
    message_service_metadata: List[Tuple[str, str]],
    username: str,
) -> Callable[[], BitfountSession]:
    """Factory to create and setup BitfountSession instance for tests."""

    def _factory() -> BitfountSession:
        handler = create_autospec(AuthenticationHandler)
        handler.am_request_headers = am_request_metadata
        handler.hub_request_headers = hub_request_metadata
        handler.message_service_request_metadata = message_service_metadata
        handler.authenticated = PropertyMock(return_value=True)
        session = BitfountSession(handler)
        return session

    return _factory


@fixture
def bitfount_session(
    bitfount_session_factory: Callable[[], BitfountSession]
) -> BitfountSession:
    """Bitfount session instance as fixture."""
    return bitfount_session_factory()


@unit_test
class TestBitfountSession:
    """Tests for the custom BitfountSession."""

    def test_get_message_service_auth_metadata(
        self,
        bitfount_session: BitfountSession,
        message_service_metadata: List[Tuple[str, str]],
    ) -> None:
        """Test metadata for message service is retrieved from handler."""
        assert bitfount_session.message_service_metadata == message_service_metadata

    def test_get_message_service_auth_metadata_without_authentication(
        self,
        bitfount_session: BitfountSession,
        message_service_metadata: List[Tuple[str, str]],
    ) -> None:
        """Test message service metadata is retrieved after authenticating."""
        bitfount_session.authentication_handler.authenticated = False  # type: ignore[misc] # Reason: handler is a mock # noqa: B950

        assert bitfount_session.message_service_metadata == message_service_metadata
        bitfount_session.authentication_handler.authenticate.assert_called()  # type: ignore[attr-defined] # Reason: handler is a mock # noqa: B950

    def test_get_username(self, bitfount_session: BitfountSession) -> None:
        """Test username retrieved from auth handler."""
        expected_username = "someUser"
        bitfount_session.authentication_handler.username = expected_username  # type: ignore[misc] # Reason: handler is a mock # noqa: B950

        assert bitfount_session.username == expected_username

    @pytest.mark.parametrize(
        "url, expected_output",
        [
            ("https://hub.bitfount.com", True),
            ("https://hub.bitfount.com/api/blah", True),
            ("https://hub.staging.bitfount.com", True),
            ("https://am.hub.bitfount.com", False),
            ("http://hub.bitfount.com", False),  # HTTP is not allowed
        ],
    )
    def test_is_hub_url(
        self, bitfount_session: BitfountSession, expected_output: bool, url: str
    ) -> None:
        """Tests that the is_hub_url method returns the expected output."""
        assert bitfount_session._is_hub_url(url) == expected_output

    @pytest.mark.parametrize(
        "url, expected_output",
        [
            ("https://am.hub.bitfount.com", True),
            ("https://am.hub.bitfount.com/api/blah", True),
            ("https://am.hub.staging.bitfount.com", True),
            ("https://hub.bitfount.com", False),
            ("http://am.hub.bitfount.com", False),  # HTTP is not allowed
        ],
    )
    def test_is_am_url(
        self, bitfount_session: BitfountSession, expected_output: bool, url: str
    ) -> None:
        """Tests that the is_am_url method returns the expected output."""
        assert bitfount_session._is_am_url(url) == expected_output

    def test_authenticate_calls_authentication_handler(
        self, bitfount_session: BitfountSession
    ) -> None:
        """Tests that `authenticate()` is called on authentication handler."""
        bitfount_session.authenticate()

        bitfount_session.authentication_handler.authenticate.assert_called()  # type: ignore[attr-defined] # Reason: handler is a mock # noqa: B950

    @responses.activate
    @pytest.mark.parametrize("authenticated", [True, False])
    @pytest.mark.parametrize(
        "url,expected_auth_header,would_authenticate_be_called",
        [
            (
                "https://hub.bitfount.com",
                lazy_fixture("hub_request_metadata"),
                True,
            ),  # Hub URL
            (
                "https://am.hub.bitfount.com",
                lazy_fixture("am_request_metadata"),
                True,
            ),  # AM URL
            (
                "https://some.api.url/goes/here",
                {"authorization": None},
                False,
            ),  # Other URL
        ],
    )
    def test_bitfount_session_request_provides_token_to_hub(
        self,
        hub_request_metadata: Dict,
        am_request_metadata: Dict,
        bitfount_session: BitfountSession,
        url: str,
        expected_auth_header: Dict,
        authenticated: bool,
        would_authenticate_be_called: bool,
    ) -> None:
        """Checks that `request()` call provides token."""
        responses.add(
            responses.POST,
            url,
        )
        bitfount_session.authentication_handler.authenticated = authenticated  # type: ignore[misc] # Reason: handler is a mock # noqa: B950

        # Send request
        bitfount_session.request("POST", url)

        # Check request had access token
        first_call: responses.Call = cast(responses.Call, responses.calls[0])
        assert (
            first_call.request.headers.get("authorization", None)
            == expected_auth_header["authorization"]
        )
        if would_authenticate_be_called and not authenticated:
            bitfount_session.authentication_handler.authenticate.assert_called()  # type: ignore[attr-defined] # Reason: handler is a mock # noqa: B950


@unit_test
@pytest.mark.parametrize(
    argnames=(
        "environment",
        "expected_name",
        "expected_auth_domain",
        "expected_client_id",
    ),
    argvalues=(
        pytest.param(
            _STAGING_ENVIRONMENT,
            "staging",
            _STAGING_AUTH_DOMAIN,
            _STAGING_CLIENT_ID,
            id="staging",
        ),
        pytest.param(
            _DEVELOPMENT_ENVIRONMENT,
            "development",
            _DEVELOPMENT_AUTH_DOMAIN,
            _DEVELOPMENT_CLIENT_ID,
            id="development",
        ),
        pytest.param(
            _PRODUCTION_ENVIRONMENT,
            "production",
            _PRODUCTION_AUTH_DOMAIN,
            _PRODUCTION_CLIENT_ID,
            id="production",
        ),
    ),
)
def test_get_auth_environment(
    environment: str,
    expected_auth_domain: str,
    expected_client_id: str,
    expected_name: str,
    monkeypatch: MonkeyPatch,
) -> None:
    """Tests _get_auth_environment with various envvar values."""
    # Patch out environment variable
    monkeypatch.setenv("BITFOUNT_ENVIRONMENT", environment)

    # Check return
    assert _get_auth_environment() == _AuthEnv(
        expected_name, expected_auth_domain, expected_client_id
    )
