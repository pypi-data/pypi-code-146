from contextlib import ExitStack
from unittest.mock import patch

import pytest

from sym.flow.cli.symflow import symflow as click_command
from sym.flow.cli.tests.factories.users import UserFactory


@patch("sym.flow.cli.helpers.rest.SymRESTClient.post")
class TestUsersSetRole:
    @pytest.fixture
    def user(self):
        yield UserFactory.create()

    @pytest.fixture(autouse=True)
    def mocks(self, user):
        with ExitStack() as stack:
            stack.enter_context(patch("sym.flow.cli.helpers.api.SymAPI.get_user", return_value=user))
            yield

    @pytest.mark.parametrize("role", ["admin", "member", "guest"])
    def test_set_role_with_option(self, mock_post, click_setup, user, role):
        with click_setup() as runner:
            result = runner.invoke(
                click_command,
                ["users", "set-role", user.sym_email, "--role", role],
            )
            assert result.exit_code == 0

        mock_post.assert_called_once_with(f"users/{user.id}/set-role", data={"role": role})

    @pytest.mark.parametrize("role", ["admin", "member", "guest"])
    @patch("inquirer.list_input", side_effect=["admin", "member", "guest"])
    def test_set_role_prompt(self, mock_inquirer, mock_post, click_setup, user, role):
        with click_setup() as runner:
            result = runner.invoke(
                click_command,
                ["users", "set-role", user.sym_email],
            )
            assert result.exit_code == 0

        mock_inquirer.assert_called_once_with("Which role?", choices=["admin", "guest", "member"])

    def test_set_role_invalid(self, user, click_setup):
        with click_setup() as runner:
            result = runner.invoke(
                click_command,
                ["users", "set-role", user.sym_email, "--role", "boo"],
            )
            assert result.exit_code != 0
            assert "Invalid input: 'boo'" in result.output
            assert "Try one of: admin, guest, member" in result.output
