from git.repo import Repo

from devjournal.constants import entries_directory
from devjournal.git_scripts.pull_rebase import pull_rebase

from ..config import get_config


def add(repo: Repo):
    repo = Repo(entries_directory())
    repo.git.add(".")


def commit(repo: Repo):
    if repo.index.diff("HEAD"):
        repo.git.commit(message="devjournal commit")


def push(repo: Repo):
    remote_branch = get_config().remote_branch
    repo = Repo(entries_directory())
    local_branch_name = repo.head.reference.name
    repo.git.push("--set-upstream", "origin", f"{local_branch_name}:{remote_branch}")


def add_commit_pull_rebase_push():
    repo = Repo(entries_directory())
    add(repo)
    commit(repo)
    pull_rebase()
    push(repo)


if __name__ == "__main__":
    add_commit_pull_rebase_push()
