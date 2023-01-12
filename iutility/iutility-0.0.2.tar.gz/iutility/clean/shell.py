from pathlib import Path

import click

from ..utils import remove

PATTERNS: list[str] = [
    ".profile",
    "*bash*",
    "*zcompdump*",
]


@click.command(name="shell")
def cmd() -> None:
    for pattern in PATTERNS:
        for path in Path.home().glob(pattern=pattern):
            remove(path=path, ask=False)
