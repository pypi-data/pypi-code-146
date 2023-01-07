import subprocess
from pathlib import Path

import pytest
from pytest import MonkeyPatch

import devjournal.entry
import devjournal.git_scripts.add_commit_pull_rebase_push
import devjournal.git_scripts.pull_rebase
from devjournal import __main__
from devjournal.entry import Entry
from devjournal.git_scripts.add_commit_pull_rebase_push import (
    add_commit_pull_rebase_push,
)
from devjournal.git_scripts.pull_rebase import pull_rebase


class MockPrintIdsAndEntries:
    def __call__(self, ids_and_entries: list[tuple[int, Entry]]):
        self.entries = [entry for _, entry in ids_and_entries]


class MockRepoReturner:
    def __init__(self) -> None:
        self.repo = MockRepo()

    def init(self, *args, **kwargs):
        return self.repo

    def __call__(self, *args, **kwargs):
        return self.repo


class MockRepo:
    class MockGit:
        def add(self, *args, **kwargs):
            pass

        def commit(self, *args, **kwargs):
            pass

        def push(self, *args, **kwargs):
            self.push_called = True

    class MockOrigin:
        def pull(self, *args, **kwargs):
            self.pull_called = True

    class MockHead:
        class MockReference:
            name = "myname"

        reference = MockReference

    class MockIndex:
        def diff(self, *args, **kwargs):
            return True

    def __init__(self, *args, **kwargs) -> None:
        self.git = self.MockGit()
        self.git.push_called = False
        self.origin = self.MockOrigin()
        self.origin.pull_called = False
        self.remotes = ["myremote"]
        self.head = self.MockHead
        self.index = self.MockIndex()

    def create_remote(self, *args, **kwargs):
        return self.origin

    def delete_remote(self, *args, **kwargs):
        pass


@pytest.fixture
def mock_repo(monkeypatch: MonkeyPatch):
    mock_repo_returner = MockRepoReturner()
    monkeypatch.setattr(devjournal.git_scripts.pull_rebase, "Repo", mock_repo_returner)
    monkeypatch.setattr(
        devjournal.git_scripts.add_commit_pull_rebase_push, "Repo", mock_repo_returner
    )
    return mock_repo_returner.repo


@pytest.fixture(autouse=True)
def mock_devjournal_dir(monkeypatch: MonkeyPatch, tmp_path):
    monkeypatch.setenv("DEVJOURNAL_DIR", str(tmp_path))
    return tmp_path


@pytest.fixture
def nonexisting_devjournal_dir(monkeypatch: MonkeyPatch, tmp_path):
    path = tmp_path / ".devjournal"
    monkeypatch.setenv("DEVJOURNAL_DIR", str(path))
    return path


@pytest.fixture
def config_file(mock_devjournal_dir: Path):
    (mock_devjournal_dir / "config.toml").write_text(
        'remote_repo_url = "myrepo"\nremote_branch = "mybranch"'
    )


@pytest.fixture()
def mock_print_ids_and_entries(monkeypatch: MonkeyPatch):

    return_value = MockPrintIdsAndEntries()
    monkeypatch.setattr(devjournal.entry, "print_ids_and_entries", return_value)

    return return_value


class MockProcess:
    def wait(self):
        return


@pytest.fixture
def mock_popen(monkeypatch):
    def do_mock(output_text: str):
        def MockPopen(output_text: str):
            def inner(command, **kwargs):
                Path(command[-1]).write_text(output_text)
                return MockProcess()

            return inner

        monkeypatch.setattr(subprocess, "Popen", MockPopen(output_text=output_text))

    return do_mock


def _mock_run_git_script(name):
    if name == "pull_rebase":
        pull_rebase()
    elif name == "add_commit_pull_rebase_push":
        add_commit_pull_rebase_push()


@pytest.fixture
def mock_run_git_script(monkeypatch):
    """Mock run_git_script to run in the same process instead of in a new one"""
    monkeypatch.setattr(__main__, "run_git_script", _mock_run_git_script)
