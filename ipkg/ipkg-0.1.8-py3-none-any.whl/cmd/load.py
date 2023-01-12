import importlib

import click

from ..utils import cache
from ..utils.name import module_name


@click.command(name="load")
@click.pass_context
@click.option("--dry-run", is_flag=True)
@click.argument("pkg")
@click.argument("args", nargs=-1)
def cmd_load(ctx: click.Context, dry_run: bool, pkg: str, args: tuple[str]):
    cache.DRY_RUN = dry_run
    pkg_module_name = module_name(pkg)
    module = importlib.import_module(name=f"ipkg.pkg.{pkg_module_name}.{ctx.info_name}")
    cmd: click.Command = module.main
    cmd.invoke(
        cmd.make_context(
            info_name=f"{ctx.info_name} {pkg} --",
            args=list(args),
            parent=ctx.parent,
        )
    )
