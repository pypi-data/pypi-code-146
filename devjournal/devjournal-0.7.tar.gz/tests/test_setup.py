from pathlib import Path

import pytest
from pytest import MonkeyPatch
from typer.testing import CliRunner

import devjournal.commands.setup
from devjournal.__main__ import app

runner = CliRunner()


class MockPrompt:
    def __init__(self) -> None:
        self.call_count = 0
        self.return_values = [
            "myrepo",
            "mybranch",
        ]

    def ask(self, *args, **kwargs):
        self.call_count += 1
        return self.return_values[self.call_count - 1]


@pytest.fixture
def mock_prompt(monkeypatch):
    monkeypatch.setattr(devjournal.commands.setup, "Prompt", MockPrompt())


def test_setup_command_writes_to_config_file(mock_devjournal_dir: Path, mock_prompt):
    runner.invoke(app, ["setup"], catch_exceptions=False)

    assert (
        mock_devjournal_dir / "config.toml"
    ).read_text() == 'remote_repo_url = "myrepo"\nremote_branch = "mybranch"'


def test_create_devjournal_directory_if_there_is_none(
    nonexisting_devjournal_dir, mock_prompt
):
    runner.invoke(app, ["setup"], catch_exceptions=False)

    assert (nonexisting_devjournal_dir / "config.toml").exists()
