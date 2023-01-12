import os
import tempfile
from pathlib import Path

import click

from ...utils.remove import remove
from ...utils.run import run
from .. import SHELL
from . import (
    HOMEBREW_BOTTLE_DOMAIN,
    HOMEBREW_BREW_GIT_REMOTE,
    HOMEBREW_BREW_INSTALL_GIT_REMOTE,
    HOMEBREW_CORE_GIT_REMOTE,
)


@click.command()
def main():
    tmpdir: Path = Path(tempfile.mkdtemp())
    run("git", "clone", "--depth", "1", HOMEBREW_BREW_INSTALL_GIT_REMOTE, str(tmpdir))
    os.environ["HOMEBREW_BREW_GIT_REMOTE"] = HOMEBREW_BREW_GIT_REMOTE
    os.environ["HOMEBREW_CORE_GIT_REMOTE"] = HOMEBREW_CORE_GIT_REMOTE
    os.environ["HOMEBREW_BOTTLE_DOMAIN"] = HOMEBREW_BOTTLE_DOMAIN
    run(str(SHELL), str(tmpdir / "install.sh"))
    remove(tmpdir)
