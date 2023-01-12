import click

from .export import cmd as cmd_export
from .import_ import cmd as cmd_import


@click.group(name="key")
def cmd() -> None:
    pass


cmd.add_command(cmd=cmd_export)
cmd.add_command(cmd=cmd_import)
