import re

from typer.testing import CliRunner

from devjournal.__main__ import app

runner = CliRunner()


class TestWithArguments:
    def test_file_is_created(self, mock_devjournal_dir):
        result = runner.invoke(app, ["add", "hello", "world"], catch_exceptions=False)
        assert result.exit_code == 0

        entry_files = list(mock_devjournal_dir.glob("entries/*"))
        assert len(entry_files) == 1
        assert re.match("20..-..-.._..-..-.........", entry_files[0].name)

    def test_text_is_added_to_entry_file(self, mock_devjournal_dir):
        runner.invoke(app, ["add", "hello", "world"], catch_exceptions=False)

        entry_files = list(mock_devjournal_dir.glob("entries/*"))
        assert "hello world" in entry_files[0].read_text()


class TestWithoutArguments:
    def test_text_is_added_to_entry_file(self, mock_devjournal_dir, mock_popen):
        mock_popen("hello world")
        runner.invoke(app, ["add"], catch_exceptions=False)

        entry_files = list(mock_devjournal_dir.glob("entries/*"))
        assert "hello world" in entry_files[0].read_text()

    def test_abort_with_error_message_if_no_text_entered(
        self, mock_devjournal_dir, mock_popen
    ):
        mock_popen("")
        result = runner.invoke(app, ["add"], catch_exceptions=False)

        entry_files = list(mock_devjournal_dir.glob("entries/*"))
        assert not entry_files
        assert result.output == "File empty, entry aborted.\n"


class TestGit:
    def test_add_pulls_and_then_pushes_to_git_if_config_file(
        self, config_file, mock_repo, mock_run_git_script
    ):
        result = runner.invoke(app, ["add", "hello", "world"], catch_exceptions=False)
        assert result.exit_code == 0
        assert mock_repo.origin.pull_called
        assert mock_repo.git.push_called
