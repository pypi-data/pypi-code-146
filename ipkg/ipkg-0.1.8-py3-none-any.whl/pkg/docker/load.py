import click

from ...utils.cache import export, open_cache


@click.command()
def main() -> None:
    with open_cache() as cache:
        export(cache=cache, env={"DOCKER_HOST": "unix:///run/user/1000/docker.sock"})
