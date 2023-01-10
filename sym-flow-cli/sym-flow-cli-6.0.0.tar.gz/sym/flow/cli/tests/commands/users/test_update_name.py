from contextlib import ExitStack
from unittest.mock import patch

import pytest

from sym.flow.cli.models.service_type import ServiceType
from sym.flow.cli.symflow import symflow as click_command
from sym.flow.cli.tests.factories.users import UserFactory


class TestUsersUpdateIdentity:
    @pytest.fixture
    def users(self):
        yield UserFactory.create_batch(1)

    @pytest.fixture
    def services(self, users):
        # User Factory creates the same services for each user
        yield [i.service for i in users[0].identities if i.service.service_type == ServiceType.SYM.type_name]

    @pytest.fixture(autouse=True)
    def patchypatch(self, users, services):
        with ExitStack() as stack:
            stack.enter_context(patch("sym.flow.cli.helpers.api.SymAPI.get_users", return_value=[users[0]]))
            stack.enter_context(patch("sym.flow.cli.helpers.api.SymAPI.get_services", return_value=services))
            stack.enter_context(patch("sym.flow.cli.helpers.api_operations.OperationHelper.handle_update_users"))
            yield

    def test_update_2_part_name(self, click_setup, users):
        with click_setup() as runner:
            result = runner.invoke(
                click_command,
                [
                    "users",
                    "update-name",
                    users[0].sym_email,
                    "Dummy Name",
                ],
            )
            assert result.exit_code == 0

    def test_update_1_part_name(self, click_setup, users):
        with click_setup() as runner:
            result = runner.invoke(
                click_command,
                [
                    "users",
                    "update-name",
                    users[0].sym_email,
                    "Dummy",
                ],
            )
            assert result.exit_code == 0

    def test_update_3_part_name(self, click_setup, users):
        with click_setup() as runner:
            result = runner.invoke(
                click_command,
                [
                    "users",
                    "update-name",
                    users[0].sym_email,
                    "Dummy Name Test",
                ],
            )
            assert result.exit_code == 0

    @patch("sym.flow.cli.helpers.api.SymAPI.get_users", return_value=[])
    def test_update_name_unknown_email(
        self,
        _,
        click_setup,
    ):
        with click_setup() as runner:
            result = runner.invoke(
                click_command,
                ["users", "update-name", "someone@symops.io", "Dummy Name"],
            )
            assert "Unknown user for email: someone@symops.io" in result.output

    @patch("sym.flow.cli.helpers.api.SymAPI.get_users", return_value=[])
    def test_update_name_missing_full_name(
        self,
        _,
        click_setup,
    ):
        with click_setup() as runner:
            result = runner.invoke(
                click_command,
                ["users", "update-name", "someone@symops.io"],
            )
            assert "Error: Missing argument 'FULL_NAME...'." in result.output
