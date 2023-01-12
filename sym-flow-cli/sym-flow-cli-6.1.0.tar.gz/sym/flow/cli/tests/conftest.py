from contextlib import ExitStack, contextmanager
from pathlib import Path
from typing import Optional, Union
from unittest.mock import patch

import pytest
from requests import Response
from sym.shared.cli.helpers.config import init
from sym.shared.cli.helpers.contexts import push_env
from sym.shared.cli.tests.conftest import capture_command, wrapped_cli_runner  # noqa

from sym.flow.cli.helpers.constants import DEFAULT_API_URL
from sym.flow.cli.helpers.jwt import JWT
from sym.flow.cli.models import AuthToken, Organization
from sym.flow.cli.tests.helpers.sandbox import Sandbox


@pytest.fixture
def click_setup(sandbox, wrapped_cli_runner):
    @contextmanager
    def context():
        with wrapped_cli_runner.isolated_filesystem():
            with sandbox.push_xdg_config_home():
                with sandbox.push_exec_path():
                    with push_env("SYM_API_URL", DEFAULT_API_URL):
                        yield wrapped_cli_runner

    return context


@pytest.fixture
def sandbox(tmp_path: Path) -> Sandbox:
    return Sandbox(tmp_path)


@pytest.fixture
def test_org() -> Organization:
    return Organization(slug="test", client_id="12345abc")


@pytest.fixture
def auth_token():
    return AuthToken(
        access_token="access",
        refresh_token="refresh",
        token_type="type",
        expires_in=86400,
        scope="scopes",
    )


@pytest.fixture(autouse=True)
def init_cli():
    init("symflow")


@pytest.fixture
def global_options():
    from sym.flow.cli.helpers.global_options import GlobalOptions

    options = GlobalOptions()
    options.debug = False
    options.api_url = "https://api.com"
    options.auth_url = "https://auth.com"
    return options


@pytest.fixture
def mock_jwt():
    return JWT(
        client_id="12345",  # type: ignore
        connection_strategy="google-oauth2",  # type: ignore
        connection_name="google-oauth2",  # type: ignore
        email="test@symops.io",  # type: ignore
        name="Test User",  # type: ignore
    )


@pytest.fixture(autouse=True)
def global_mocks(request, mock_jwt):
    if "skip_global_mocks" not in request.keywords:
        with ExitStack() as stack:
            stack.enter_context(patch("sym.flow.cli.helpers.version.get_latest_version", return_value=None))
            stack.enter_context(
                patch(
                    "sym.flow.cli.helpers.jwt.JWT.from_access_token",
                    return_value=mock_jwt,
                )
            )
            stack.enter_context(patch("webbrowser.open"))
            yield


class MockResponse(Response):
    def __init__(self, data: Optional[Union[dict, list]] = None):
        super().__init__()

        if data is None:
            data = {}

        self.data = data

    def json(self):
        return self.data


def get_mock_response(
    status_code: int, data: Optional[Union[dict, list]] = None, url: Optional[str] = None
) -> Response:
    response = MockResponse(data)
    response.status_code = status_code

    if url:
        response.url = url

    return response
