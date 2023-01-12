import os
from pathlib import Path

import click

from ..utils import copy, execute
from .typed import SSH_TYPES


def export_gpg(prefix: Path) -> None:
    os.makedirs(name=prefix / "gpg", exist_ok=True)
    execute(
        "gpg",
        "--export-secret-keys",
        "--armor",
        "--output",
        prefix / "gpg" / "secret.asc",
    )


def export_ssh(prefix: Path) -> None:
    config_path: Path = Path.home() / ".ssh" / "config"
    if config_path.exists():
        copy(src=config_path, dst=prefix / "ssh" / "config")
    for ssh_type in SSH_TYPES:
        private_key_name: str = f"id_{ssh_type}"
        private_key_path: Path = Path.home() / ".ssh" / private_key_name
        if private_key_path.exists():
            copy(src=private_key_path, dst=prefix / "ssh" / private_key_name)
        public_key_name: str = f"id_{ssh_type}.pub"
        public_key_path: Path = Path.home() / ".ssh" / public_key_name
        if public_key_path.exists():
            copy(src=public_key_path, dst=prefix / "ssh" / public_key_name)


@click.command(name="export")
@click.option("-p", "--prefix", "--path", type=click.Path(), default=Path.cwd())
def cmd(prefix: str | Path) -> None:
    prefix = Path(prefix)
    export_gpg(prefix=prefix)
    export_ssh(prefix=prefix)
