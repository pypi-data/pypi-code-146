import click

from ...utils.cache import open_cache, unset


@click.command()
def main() -> None:
    with open_cache() as cache:
        unset(cache=cache, names=["LD_LIBRARY_PATH"])
