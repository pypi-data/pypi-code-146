import getpass
import os
from pathlib import Path

import click
from ishutils import remove, run


@click.command(name="reset")
def cmd() -> None:
    root: Path = Path(
        str(
            run("git", "rev-parse", "--show-toplevel", capture_output=True).stdout,
            encoding="utf-8",
        ).strip()
    )
    os.chdir(root)
    remove(path=".git")
    run("git", "init")
    run(
        "git",
        "remote",
        "add",
        "origin",
        f"https://github.com/{getpass.getuser()}/{root.name}.git",
    )
    run("pre-commit", "install", "--install-hooks")
    run("git", "add", "--all")
    run("pre-commit", "run", "--all-files")
    run("git", "add", "--all")
    run("git", "commit", "--message", "fix: initial commit")
    run("git", "push", "--force", "--set-upstream", "origin", "main")
