# SPDX-FileCopyrightText: 2023-present Waylon S. Walker <waylon@waylonwalker.com>
#
# SPDX-License-Identifier: MIT
import click

from ..__about__ import __version__
from ..creeper import main


@click.group(
    context_settings={"help_option_names": ["-h", "--help"]},
    invoke_without_command=True,
)
@click.version_option(version=__version__, prog_name="creeper-adventure")
@click.pass_context
@click.option("--debug", is_flag=True, help="start with the debug menu open")
def creeper_adventure(ctx: click.Context, debug):
    main(debug)
