import logging

import rich_click as click

from servicefoundry import logger
from servicefoundry.cli.commands import (
    deploy_v2_command,
    get_build_command,
    get_list_command,
    get_login_command,
    get_logout_command,
    get_logs_command,
    get_set_command,
)
from servicefoundry.cli.config import CliConfig
from servicefoundry.cli.const import GROUP_CLS
from servicefoundry.cli.util import setup_rich_click
from servicefoundry.lib.util import is_debug_env_set, is_experimental_env_set
from servicefoundry.version import __version__


def _add_experimental_commands(cli):
    from servicefoundry.cli.commands.infra_bootstrap import get_infra_command
    from servicefoundry.cli.commands.trigger_command import get_trigger_command

    cli.add_command(get_infra_command())
    cli.add_command(get_trigger_command())


def create_service_foundry_cli():
    """Generates CLI by combining all subcommands into a main CLI and returns in

    Returns:
        function: main CLI functions will all added sub-commands
    """
    _cli = service_foundry_cli
    _cli.add_command(get_login_command())
    # _cli.add_command(get_get_command())
    _cli.add_command(get_list_command())
    # _cli.add_command(get_delete_command())
    # _cli.add_command(get_create_command())
    _cli.add_command(get_logout_command())
    _cli.add_command(get_set_command())
    _cli.add_command(get_build_command())
    _cli.add_command(deploy_v2_command)
    _cli.add_command(get_logs_command())
    if is_experimental_env_set():
        _add_experimental_commands(_cli)
    return _cli


CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"])


@click.group(
    cls=GROUP_CLS, context_settings=CONTEXT_SETTINGS, invoke_without_command=True
)
@click.option(
    "--json",
    is_flag=True,
    help="Output entities in json format instead of formatted tables",
)
@click.option(
    "--debug",
    is_flag=True,
    default=is_debug_env_set,
    help="Set logging level to Debug. Can also be set using environment variable. E.g. SFY_DEBUG=1",
)
@click.version_option(__version__)
@click.pass_context
def service_foundry_cli(ctx, json, debug):
    """
    Servicefoundry provides an easy way to deploy your services, jobs and models.
    \b

    To start, login to your Truefoundry account with `sfy login`

    Then start deploying with `sfy deploy`

    Deploy a Service: https://docs.truefoundry.com/docs/deploying-your-first-service

    Deploy a Job: https://docs.truefoundry.com/docs/jobs-quickstart

    Deploy a Model: https://docs.truefoundry.com/docs/scikit-learn
    """
    setup_rich_click()
    # TODO (chiragjn): Change this to -o json|yaml|table|pager
    CliConfig.set("json", json)
    if ctx.invoked_subcommand is None:
        click.echo(ctx.get_help())
    logger.add_cli_handler(level=logging.DEBUG if debug else logging.INFO)
