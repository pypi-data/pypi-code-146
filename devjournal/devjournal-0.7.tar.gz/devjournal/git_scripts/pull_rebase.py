from git import GitCommandError
from git.repo import Repo
from rich import print

from devjournal.constants import entries_directory

from ..config import get_config


def get_origin(remote_repo_url: str):
    repo = Repo.init(entries_directory())
    if repo.remotes:
        repo.delete_remote(repo.remotes[0])
    return repo.create_remote("origin", remote_repo_url)


def _indent(text: str, spaces=2):
    return " " * spaces + text.replace("\n", "\n" + " " * spaces)


def pull_rebase():
    config = get_config()
    remote_branch = config.remote_branch
    remote_repo_url = config.remote_repo_url
    try:
        get_origin(remote_repo_url).pull(rebase=True, refspec=remote_branch)
    except GitCommandError as e:
        command = " ".join(e.command)
        message = e.stderr.replace("stderr:", "").strip()
        print(
            f"[red]Error:[/red] Git command '{command}' failed with error message {message}"
        )
        print("[blue]Config file:[/blue]")
        print(_indent(config.text))


if __name__ == "__main__":
    pull_rebase()
