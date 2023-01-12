from pathlib import Path

import click

from ...utils.cache import exec, open_cache
from . import DEFAULT_PREFIX, HELP_PREFIX


@click.command()
@click.option(
    "-p",
    "--prefix",
    "--path",
    type=click.Path(exists=True, file_okay=False, dir_okay=True),
    default=DEFAULT_PREFIX,
    help=HELP_PREFIX,
)
def main(prefix: str | Path):
    prefix = Path(prefix)
    with open_cache() as cache:
        exec(
            cache=cache,
            commands=[
                ["source", str(prefix / "etc" / "profile.d" / "conda.sh")],
                ["conda", "activate", "default"],
            ],
        )
