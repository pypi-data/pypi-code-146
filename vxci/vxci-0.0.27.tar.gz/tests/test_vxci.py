from click.testing import CliRunner
from vxci.commands.command import cli


def test_main():
    runner = CliRunner()
    result = runner.invoke(cli, [])
    assert result.exit_code == 0
