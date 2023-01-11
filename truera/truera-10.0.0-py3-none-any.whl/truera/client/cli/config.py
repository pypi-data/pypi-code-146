import json
import os
import sys

import click

import truera.client.cli.cli_logger as cli_logger
from truera.client.cli.cli_utils import CLI_CONTEXT_SETTINGS
import truera.client.cli.cli_utils as cli_utils
from truera.client.cli.UncaughtExceptionHandler import UncaughtExceptionHandler
import truera.client.client_environment as env
import truera.client.services.artifact_interaction_client as cl


@click.group(
    help="For command help, use <command> --help. Example: create-project --help."
)
def config():
    pass


@config.command(context_settings=CLI_CONTEXT_SETTINGS)
def connection_string():
    context = env.LocalContextStorage.get_cli_env_context()
    connection_string = context.connection_string
    click.echo("Current connection string: " + (connection_string or "Not set"))


@config.command(context_settings=CLI_CONTEXT_SETTINGS)
def log_level():
    context = env.LocalContextStorage.get_cli_env_context()
    click.echo("Current log level: " + context.log_level)


@config.command(context_settings=CLI_CONTEXT_SETTINGS)
def auth_type():
    context = env.LocalContextStorage.get_cli_env_context()
    auth_type = context.auth_type
    click.echo("Current auth type: " + (auth_type or "Not set"))


@config.command(context_settings=CLI_CONTEXT_SETTINGS)
def feature_switch_values():
    context = env.LocalContextStorage.get_cli_env_context()
    click.echo(json.dumps(context.feature_switches, indent=4, sort_keys=True))
