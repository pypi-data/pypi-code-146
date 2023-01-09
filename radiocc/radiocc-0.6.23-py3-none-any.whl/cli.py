#!/usr/bin/env python3

"""
radiocc CLI.
"""

from typing import Any

import click
from pudb import set_trace as bp  # noqa: F401

import radiocc

CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"])


def version(ctx: Any, param: Any, value: Any) -> None:
    if not value or ctx.resilient_parsing:
        return
    click.echo(radiocc.__version__)
    ctx.exit()


@click.group(context_settings=CONTEXT_SETTINGS, invoke_without_command=True)
@click.pass_context
@click.option(
    "-v",
    "--version",
    is_flag=True,
    callback=version,
    expose_value=False,
    is_eager=True,
    help="Show version.",
)
@click.option(
    "--generate-config",
    is_flag=True,
    help="Generate a config file `config.yaml` in the current directory.",
)
@click.option(
    "--download-data",
    is_flag=True,
    help="Download input data",
)
def cli(ctx: click.Context, generate_config: bool, download_data: bool) -> None:
    """Radio occultations command-line entry point."""
    # Share default command options.
    ctx.ensure_object(dict)
    # ctx.obj["var"] = var

    if generate_config:
        radiocc.config.Cfg().generate_config()
        ctx.exit()

    radiocc.cfg.load_config_file()

    if download_data:
        radiocc.download_data.proceed()
        ctx.exit()

    if ctx.invoked_subcommand is None:
        click.echo(ctx.get_help())
        ctx.exit()


@cli.command()
@click.option(
    "-g", "--gui", is_flag=True, help="Start the program with the graphical interface."
)
@click.pass_context
def run(
    ctx: click.Context,
    gui: bool,
) -> None:
    """Run radiocc."""
    if gui:
        radiocc.cfg.graphical_interface = True

    radiocc.core.run()


def main() -> None:
    cli(prog_name="radiocc")


if __name__ == "__main__":
    main()
