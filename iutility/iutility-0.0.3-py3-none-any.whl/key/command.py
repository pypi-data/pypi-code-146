import click

from ._import import cmd as cmd_import
from .export import cmd as cmd_export


@click.group(name="key")
def cmd() -> None:
    pass


cmd.add_command(cmd=cmd_export)
cmd.add_command(cmd=cmd_import)
