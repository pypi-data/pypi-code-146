from pathlib import Path

import click

from ..utils import copy, execute
from .typed import SSH_TYPES


def import_gpg(prefix: Path) -> None:
    execute("gpg", "--import", prefix / "gpg" / "secret.asc")
    signing_key: str = str(
        execute("git", "config", "user.signingKey", capture_output=True).stdout,
        encoding="utf-8",
    ).strip()
    execute("gpg", "--edit-key", signing_key, "trust")


def import_ssh(prefix: Path) -> None:
    config_path: Path = prefix / "ssh" / "config"
    if config_path.exists():
        copy(src=config_path, dst=Path.home() / ".ssh" / "config")
    for ssh_type in SSH_TYPES:
        private_key_name: str = f"id_{ssh_type}"
        private_key_path: Path = prefix / "ssh" / private_key_name
        if private_key_path.exists():
            copy(src=private_key_path, dst=Path.home() / ".ssh" / private_key_name)
        public_key_name: str = f"id_{ssh_type}.pub"
        public_key_path: Path = prefix / "ssh" / public_key_name
        if public_key_path.exists():
            copy(src=public_key_path, dst=Path.home() / ".ssh" / public_key_name)


@click.command(name="import")
@click.option("-p", "--prefix", "--path", type=click.Path(), default=Path.cwd())
def cmd(prefix: str | Path) -> None:
    prefix = Path(prefix)
    import_gpg(prefix=prefix)
    import_ssh(prefix=prefix)
