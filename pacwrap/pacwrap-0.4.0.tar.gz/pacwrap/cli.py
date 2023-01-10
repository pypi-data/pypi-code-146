import sys
import types
from typing import AnyStr, NoReturn, Optional

import click
from click.core import Context

from pacwrap import VERSION
from pacwrap.mkhandler import create_handler

CONTEXT_SETTINGS = types.MappingProxyType({"help_option_names": ["-h", "--help"]})
LPACKAGE = "package"
KDEBUG = "debug"


@click.command(name="file")
@click.argument("filename", required=True, nargs=1)
@click.pass_context
def file_cmd(ctx: Context, filename: str) -> NoReturn:
    """Displays package if any that include the FILE."""
    options = ctx.obj.copy()
    if options[KDEBUG] > 0:
        print("file_cmd({0}, {1}) called!".format(ctx.obj, filename))
    phandler = create_handler(options)
    sys.exit(phandler.file_action(filename))


@click.command(name="list")
@click.argument(LPACKAGE, required=False, nargs=1)
@click.pass_context
def list_cmd(ctx: Context, package: Optional[str]) -> NoReturn:
    """Lists files in PACKAGE or installed packages when no PACKAGE specified."""
    options = ctx.obj.copy()
    if options[KDEBUG] > 0:
        print("list_cmd({0}, {1}) called!".format(ctx.obj, package))
    phandler = create_handler(options)
    if package is None:
        vrtn = phandler.list_packages()
    else:
        vrtn = phandler.list_package(package)
    sys.exit(vrtn)


@click.command(name="find")
@click.option(
    "--names-only/--no-names-only",
    default=False,
    help="specify search names only if packager supports it",
)
@click.argument(LPACKAGE, required=True, nargs=1)
@click.pass_context
def find_cmd(ctx: Context, names_only: bool, package: str) -> NoReturn:
    """Searches repositories for PACKAGE."""
    options = ctx.obj.copy()
    options["names_only"] = names_only
    if options[KDEBUG] > 0:
        print("find_cmd({0}, {1}) called!".format(ctx.obj, package))
    phandler = create_handler(options)
    sys.exit(phandler.find_action(package))


@click.command(name="info")
@click.argument(LPACKAGE, required=True, nargs=1)
@click.pass_context
def info_cmd(ctx: Context, package: str) -> NoReturn:
    """Display information about PACKAGE."""
    options = ctx.obj.copy()
    if options[KDEBUG] > 0:
        print("info_cmd({0}, {1}) called!".format(ctx.obj, package))
    phandler = create_handler(options)
    sys.exit(phandler.info_action(package))


@click.command()
@click.argument(LPACKAGE, required=True, nargs=1)
@click.pass_context
def install(ctx: Context, package: str) -> NoReturn:
    """Installs PACKAGE."""
    options = ctx.obj.copy()
    if options[KDEBUG] > 0:
        print("install({0}, {1}) called!".format(ctx.obj, package))
    phandler = create_handler(options)
    sys.exit(phandler.install_action(package))


@click.command()
@click.argument(LPACKAGE, required=True, nargs=1)
@click.pass_context
def uninstall(ctx: Context, package: str) -> NoReturn:
    """Unistalls PACKAGE."""
    options = ctx.obj.copy()
    if options[KDEBUG] > 0:
        print("uninstall({0}, {1}) called!".format(ctx.obj, package))
    phandler = create_handler(options)
    sys.exit(phandler.uninstall_action(package))


def print_version(ctx: Context, aparam: AnyStr, avalue: AnyStr) -> None:
    """Print package version and exit."""
    if not avalue or ctx.resilient_parsing:
        return
    print(VERSION)
    ctx.exit()


@click.group(context_settings=CONTEXT_SETTINGS)
@click.option("-d", "--debug", count=True, default=0, help="increment debug level")
@click.option("-o", "--out", "output", help="specify output file")
@click.option("-q", "--quiet/--no-quiet", default=False, help="specify quiet mode")
@click.option(
    "-r",
    "--refresh/--no-refresh",
    default=False,
    help="specify refresh synchronized package repository data",
)
@click.option("-t", "--test/--no-test", default=False, help="specify test mode")
@click.option(
    "-v",
    "--verbose",
    count=True,
    default=0,
    help="increment verbosity level",
)
@click.option(
    "-V",
    "--version",
    is_flag=True,
    expose_value=False,
    callback=print_version,
    is_eager=True,
    help="show version and exit",
)
@click.pass_context
def main(ctx, debug, output, quiet, refresh, test, verbose):
    """Provides single interface to several common Linux package managers."""
    ctx.ensure_object(dict)
    ctx.obj[KDEBUG] = debug
    ctx.obj["output"] = output
    ctx.obj["quiet"] = quiet
    ctx.obj["refresh"] = refresh
    ctx.obj["test"] = test
    ctx.obj["verbose"] = verbose


main.add_command(file_cmd, name="file")
main.add_command(list_cmd, name="list")
main.add_command(find_cmd, name="find")
main.add_command(info_cmd, name="info")
main.add_command(install)
main.add_command(uninstall)


if __name__ == "__main__":
    sys.exit(main(obj={}))  # pragma no cover
