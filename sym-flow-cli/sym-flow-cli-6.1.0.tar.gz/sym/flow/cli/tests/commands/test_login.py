from typing import List, Union, cast
from unittest.mock import patch

import pytest
from sym.shared.cli.errors import CliError

from sym.flow.cli.errors import InvalidTokenError, LoginError
from sym.flow.cli.helpers.global_options import GlobalOptions
from sym.flow.cli.helpers.login.login_flow import LoginFlow
from sym.flow.cli.models import AuthToken, Organization
from sym.flow.cli.symflow import symflow as click_command
from sym.flow.cli.tests.conftest import get_mock_response

TEST_LOGIN_ORG_SLUG = "test"


def mock_login_flow(result: Union[AuthToken, CliError]):
    class MockLoginFlow(LoginFlow):
        def login(self, options: GlobalOptions, org: Organization) -> AuthToken:
            # TypedDict doesn't support isinstance
            if isinstance(result, dict):
                return result
            raise cast(CliError, result)

        def gen_browser_login_params(self, options: GlobalOptions, org: Organization):
            return ("", None, None)

    return MockLoginFlow()


@pytest.fixture
def login_flow(auth_token):
    return mock_login_flow(auth_token)


@pytest.fixture
def login_flow_login_error():
    return mock_login_flow(LoginError("test"))


@pytest.fixture
def login_flow_invalid_token_error():
    return mock_login_flow(InvalidTokenError("test"))


login_test_org = Organization(slug="test", client_id="12345abc")


@pytest.fixture
def login_tester(click_setup):
    def tester(
        login_flow: LoginFlow,
        org_slug: str,
        expected_output: List[str],
        success: bool = True,
    ):
        with patch("sym.flow.cli.commands.login.BrowserRedirectFlow", return_value=login_flow):
            with click_setup() as runner:
                result = runner.invoke(click_command, ["login", "--org-id", org_slug])
                print(result.output)
                for expected_str in expected_output:
                    assert expected_str in result.output
                if success:
                    assert result.exit_code == 0
                else:
                    assert result.exit_code != 0

    return tester


@patch(
    "sym.flow.cli.helpers.api.SymAPI.get_organization_from_slug",
    return_value=login_test_org,
)
def test_login_ok(mock_get_org, login_flow, login_tester):
    login_tester(
        login_flow=login_flow,
        org_slug=TEST_LOGIN_ORG_SLUG,
        success=True,
        expected_output=["Login succeeded"],
    )

    mock_get_org.assert_called_once_with(TEST_LOGIN_ORG_SLUG)


@patch(
    "sym.flow.cli.helpers.api.SymAPI.get_organization_from_slug",
    return_value=login_test_org,
)
def test_login_login_error(_, login_flow_login_error, login_tester):
    login_tester(
        login_flow=login_flow_login_error,
        org_slug=TEST_LOGIN_ORG_SLUG,
        success=False,
        expected_output=[f"Error logging in: {TEST_LOGIN_ORG_SLUG}"],
    )


@patch(
    "sym.flow.cli.helpers.api.SymAPI.get_organization_from_slug",
    return_value=login_test_org,
)
def test_login_invalid_token_error(_, login_flow_invalid_token_error, login_tester):
    login_tester(
        login_flow=login_flow_invalid_token_error,
        org_slug=TEST_LOGIN_ORG_SLUG,
        success=False,
        expected_output=[f"Unable to parse token: {TEST_LOGIN_ORG_SLUG}"],
    )


@patch(
    "requests.request",
    return_value=(
        get_mock_response(
            404,
            {"message": f"No Organization with the slug {TEST_LOGIN_ORG_SLUG} was found."},
        )
    ),
)
@patch("sym.flow.cli.helpers.rest.SymRESTClient.make_headers", return_value={})
def test_login_unknown_org(_, __, login_flow, login_tester):
    login_tester(
        login_flow=login_flow,
        org_slug=TEST_LOGIN_ORG_SLUG,
        success=False,
        expected_output=[f"No Organization with the slug {TEST_LOGIN_ORG_SLUG}"],
    )
