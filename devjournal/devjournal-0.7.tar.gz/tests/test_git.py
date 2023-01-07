from typer.testing import CliRunner

from devjournal.__main__ import app

runner = CliRunner()


def test_git_error_message(config_file, mock_run_git_script):
    result = runner.invoke(app, ["find", "foo"], catch_exceptions=False)
    assert result.exit_code == 0
    assert (
        result.stdout
        == "Error: Git command 'git pull -v --rebase origin mybranch' failed with error "
        """\nmessage 'fatal: 'myrepo' does not appear to be a git repository
fatal: Could not read from remote repository.'
Config file:
  remote_repo_url = \"myrepo\"
  remote_branch = \"mybranch\"

"""
    )
