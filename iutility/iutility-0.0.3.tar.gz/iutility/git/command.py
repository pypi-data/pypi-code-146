import click

from .init import cmd as cmd_init
from .reset import cmd as cmd_reset
from .secret import cmd as cmd_secret


@click.group(name="git")
def cmd() -> None:
    pass


cmd.add_command(cmd=cmd_init)
cmd.add_command(cmd=cmd_reset)
cmd.add_command(cmd=cmd_secret)
