import webbrowser

from sym.flow.cli.helpers.constants import SYM_DOCUMENTATION_URL
from sym.flow.cli.symflow import symflow as click_command


def test_docs(click_setup):
    with click_setup() as runner:
        result = runner.invoke(click_command, ["docs"])
        assert f"Opening a link to Sym documentation: {SYM_DOCUMENTATION_URL}" in result.output
        webbrowser.open.assert_called_once_with(SYM_DOCUMENTATION_URL)
        assert result.exit_code == 0
