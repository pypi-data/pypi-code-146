import getpass
import os
from pathlib import Path

import click

from ..utils import execute, remove


@click.command(name="reset")
def cmd() -> None:
    root: Path = Path(
        str(
            execute("git", "rev-parse", "--show-toplevel", capture_output=True).stdout,
            encoding="utf-8",
        ).strip()
    )
    os.chdir(root)
    remove(path=".git")
    execute("git", "init")
    execute(
        "git",
        "remote",
        "add",
        "origin",
        f"https://github.com/{getpass.getuser()}/{root.name}.git",
    )
    execute("pre-commit", "install", "--install-hooks")
    execute("git", "add", "--all")
    execute("pre-commit", "run", "--all-files")
    execute("git", "add", "--all")
    execute("git", "commit", "--message", "fix: initial commit")
    execute("git", "push", "--force", "--set-upstream", "origin", "main")
