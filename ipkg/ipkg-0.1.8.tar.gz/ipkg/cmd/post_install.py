import importlib

import click

from ..utils.name import module_name


@click.command(name="post-install")
@click.pass_context
@click.argument("pkg")
@click.argument("args", nargs=-1)
def cmd_post_install(ctx: click.Context, pkg: str, args: tuple[str]):
    pkg_module_name: str = module_name(pkg)
    module = importlib.import_module(name=f"ipkg.pkg.{pkg_module_name}.post_install")
    cmd: click.Command = module.main
    cmd.invoke(
        cmd.make_context(
            info_name=f"{ctx.info_name} {pkg} --",
            args=list(args),
            parent=ctx.parent,
        )
    )
