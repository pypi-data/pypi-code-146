import click

from ...utils.run import run


@click.command()
def main() -> None:
    run("sudo", "add-apt-repository", "ppa:obsproject/obs-studio")
    run("sudo", "apt", "update")
    run("sudo", "apt", "install", "ffmpeg", "obs-studio")
