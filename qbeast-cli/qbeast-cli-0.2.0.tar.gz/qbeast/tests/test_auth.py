from click.testing import CliRunner
from qbeast.auth import login


def test_login_command():
    runner = CliRunner()
    result = runner.invoke(login, ['XXXXX@qbeast.io', "XXXXXXXX"])
    assert result.exit_code == 0
