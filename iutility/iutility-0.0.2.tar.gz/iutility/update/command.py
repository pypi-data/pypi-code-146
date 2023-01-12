import click

from .apt import cmd as cmd_apt
from .brew import cmd as cmd_brew
from .snap import cmd as cmd_snap
from .tldr import cmd as cmd_tldr


@click.group(name="update", invoke_without_command=True)
@click.pass_context
def cmd(ctx: click.Context) -> None:
    if ctx.invoked_subcommand:
        return
    for _, sub_cmd in cmd.commands.items():
        try:
            sub_cmd.main(args=[], standalone_mode=False)
        except:
            pass


cmd.add_command(cmd=cmd_apt)
cmd.add_command(cmd=cmd_brew)
cmd.add_command(cmd=cmd_snap)
cmd.add_command(cmd=cmd_tldr)
