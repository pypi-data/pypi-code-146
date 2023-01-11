import os
import sys

import click

import truera.client.cli.cli_logger as cli_logger
from truera.client.cli.cli_utils import CLI_CONTEXT_SETTINGS
import truera.client.client_environment as env


@click.group(help="Commands for activating client side features.")
def activate():
    pass


@activate.command(
    help="""Activates the provided experimental command.""",
    context_settings=CLI_CONTEXT_SETTINGS
)
@click.argument("command", default=None)
# There is a very robust way to do this by using a custom group class and adding an active parameter
# to command. See https://stackoverflow.com/questions/55373759/feature-flag-for-python-click-commands
# This is not done today because we don't have any whole commands we'd like to conditionally turn on.
def command(command):
    click.echo(
        "Provided experimental command was not found: '{}'.".format(command)
    )
    sys.exit(0)


@activate.command(
    help="""Activates the provided experimental feature.""",
    context_settings=CLI_CONTEXT_SETTINGS
)
@click.argument("feature", default=None)
@click.option("--disable", "-d", is_flag=True, hidden=True)
def feature(feature, disable):
    allowed_features = [
        "timestamps_on_splits", "model_specific_output_type", "external_caches",
        "neural_network", "admin", "monitoring_lite", "delayed_label",
        "delayed_extra_data", "data_service_split_ingestion", "rbac_admin",
        "scheduled_ingestion", "create_model_tests_on_split_ingestion"
    ]
    if feature in allowed_features:
        context = env.LocalContextStorage.get_cli_env_context()
        context.set_feature_switch_value(
            feature, True if not disable else False
        )
        click.echo(
            "Changed experimental feature '{}' to {}.".format(
                feature, "off" if disable else "active"
            )
        )
    else:
        click.echo(
            "Provided experimental feature was not found: '{}'.".
            format(feature)
        )
        sys.exit(0)
