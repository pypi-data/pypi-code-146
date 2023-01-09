import uuid
from contextlib import ExitStack
from unittest.mock import patch

import pytest

from sym.flow.cli.models import Organization
from sym.flow.cli.symflow import symflow as click_command


class TestDomains:
    @pytest.fixture(autouse=True)
    def mocks(self):
        mock_org = Organization(id=str(uuid.uuid4()), slug="test", domains=["test.invalid", "blah.symops.com"])

        with ExitStack() as stack:
            stack.enter_context(
                patch(
                    "sym.flow.cli.helpers.api.SymAPI.get_current_organization",
                    return_value=mock_org,
                )
            )
            yield

    @patch("sym.flow.cli.helpers.rest.SymRESTClient.post")
    def test_domains_add(self, _, click_setup):
        with click_setup() as runner:
            result = runner.invoke(
                click_command,
                ["domains", "add", "test.invalid"],
            )
            assert result.exit_code == 0
            assert result.output == "test.invalid successfully added as a domain.\n"

    @patch("sym.flow.cli.helpers.rest.SymRESTClient.post")
    def test_domains_remove(self, _, click_setup):
        with click_setup() as runner:
            result = runner.invoke(
                click_command,
                ["domains", "remove", "test.invalid"],
            )
            assert result.exit_code == 0
            assert result.output == "test.invalid successfully removed as a domain.\n"

    def test_domains_list(self, click_setup):
        with click_setup() as runner:
            result = runner.invoke(
                click_command,
                ["domains", "list"],
            )
            assert result.exit_code == 0
            assert "- test.invalid\n- blah.symops.com\n" in result.output
