import click

from .apt import cmd as cmd_apt
from .brew import cmd as cmd_brew
from .cache import cmd as cmd_cache
from .npm import cmd as cmd_npm
from .pip import cmd as cmd_pip
from .shell import cmd as cmd_shell
from .tldr import cmd as cmd_tldr
from .tmp import cmd as cmd_tmp


@click.group(name="clean", invoke_without_command=True)
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
cmd.add_command(cmd=cmd_cache)
cmd.add_command(cmd=cmd_npm)
cmd.add_command(cmd=cmd_pip)
cmd.add_command(cmd=cmd_shell)
cmd.add_command(cmd=cmd_tldr)
cmd.add_command(cmd=cmd_tmp)
