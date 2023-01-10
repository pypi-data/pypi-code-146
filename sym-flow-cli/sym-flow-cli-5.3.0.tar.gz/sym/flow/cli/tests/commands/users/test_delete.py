from unittest.mock import patch

from sym.flow.cli.symflow import symflow as click_command


class TestUsersDelete:
    @patch("sym.flow.cli.helpers.api.SymAPI.delete_user")
    def test_delete(self, mock_delete_user, click_setup):
        with click_setup() as runner:
            result = runner.invoke(click_command, ["users", "delete", "user@symops.io"])
            assert result.exit_code == 0

        mock_delete_user.assert_called_once()

    @patch("sym.flow.cli.helpers.api.SymAPI.delete_user")
    def test_delete_missing_arguments(self, _, click_setup):
        with click_setup() as runner:
            result = runner.invoke(click_command, ["users", "delete"])
            assert result.exit_code == 2
