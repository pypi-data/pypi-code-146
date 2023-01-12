import click

from ...utils.download import download
from ...utils.run import run
from .. import DOWNLOADS, SHELL
from . import KEY_PATH, KEY_URL, NAME, SOURCES_LIST, SOURCES_LIST_PATH


@click.command()
def main() -> None:
    key_filename: str = NAME + ".asc"
    key_filepath = DOWNLOADS / key_filename
    download(url=KEY_URL, output=key_filepath)
    run("sudo", "cp", str(key_filepath), str(KEY_PATH))
    run("sudo", str(SHELL), "-c", f'echo "{SOURCES_LIST}" > "{SOURCES_LIST_PATH}"')
    run("sudo", "apt", "update")
    run("sudo", "apt", "install", NAME)
