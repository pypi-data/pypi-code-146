from typing import Optional

import typer

from .commands.add import add as add_command
from .commands.delete import delete as delete_command
from .commands.edit import edit as edit_command
from .commands.find import find as find_command
from .commands.log import log as log_command
from .commands.setup import setup as setup_command
from .config import is_repo_defined
from .git import run_git_script

app = typer.Typer(no_args_is_help=True)


@app.command()
def setup():
    """Set up Git repo synchronization"""
    setup_command()


@app.command()
def add(text: Optional[list[str]] = typer.Argument(None)):
    """Add a new entry"""
    if text:
        add_command(" ".join(text))
    else:
        add_command()
    if is_repo_defined():
        run_git_script("add_commit_pull_rebase_push")


@app.command()
def delete(id_: int):
    """Delete an entry"""
    delete_command(id_)
    if is_repo_defined():
        run_git_script("add_commit_pull_rebase_push")  # pragma: no cov


@app.command()
def amend():
    """Amend the last entry"""
    edit_command(0)
    if is_repo_defined():
        run_git_script("add_commit_pull_rebase_push")  # pragma: no cov


@app.command()
def edit(id_: int = typer.Argument(0)):
    """Edit an entry"""
    edit_command(id_)
    if is_repo_defined():
        run_git_script("add_commit_pull_rebase_push")  # pragma: no cov


@app.command()
def log():
    """List all entries"""
    if is_repo_defined():
        run_git_script("pull_rebase")
    log_command()


@app.command()
def find(words: list[str]):
    """Search for entry containing text"""
    if is_repo_defined():
        run_git_script("pull_rebase")
    find_command(words)


if __name__ == "__main__":
    app()
