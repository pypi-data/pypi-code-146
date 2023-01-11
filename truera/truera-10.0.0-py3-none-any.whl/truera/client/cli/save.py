import os
import sys

import click

import truera.client.cli.cli_logger as cli_logger
from truera.client.cli.cli_utils import CLI_CONTEXT_SETTINGS
from truera.client.cli.UncaughtExceptionHandler import UncaughtExceptionHandler
import truera.client.client_environment as env
import truera.client.services.artifact_interaction_client as cl


@click.group(help="Commands for saving tru cli settings.")
def save():
    pass


@save.command(
    help=
    "Puts the connection in an environment variable for use in future commands.",
    context_settings=CLI_CONTEXT_SETTINGS
)
@click.argument("connection_string")
@click.option(
    "--connection_type",
    default="http",
    type=click.Choice(["grpc", "http"]),
    help="Use HTTP/gRPC protocol to communicate with the server."
)
@click.option("--log_level", default=None, help=cli_logger.log_level_message)
@click.option(
    "--disable_cert_verification",
    is_flag=True,
    help="Add to disable ssl cert verification"
)
def connection_string(
    connection_string, connection_type, log_level, disable_cert_verification
):
    use_http = connection_type == "http"
    if disable_cert_verification:
        verify_cert = False
    else:
        verify_cert = True
    UncaughtExceptionHandler.wrap(
        _set_connection_string, connection_string, use_http, log_level,
        verify_cert
    )


def _set_connection_string(connection_string, use_http, log_level, verify_cert):
    logger = cli_logger.create_cli_logger(log_level)
    context = env.LocalContextStorage.get_cli_env_context()

    context.connection_string = connection_string
    context.use_http = use_http
    context.verify_cert = verify_cert
    click.echo("Set connection string to Truera endpoint: " + connection_string)
    click.echo("Setting verify_cert to : " + str(verify_cert))


@save.command(
    help="Changes the grpc client timeout by passing a value in seconds.",
    context_settings=CLI_CONTEXT_SETTINGS,
    hidden=True
)
@click.argument("timeout")
@click.option("--log_level", default=None, help=cli_logger.log_level_message)
def grpc_client_timeout(timeout, log_level):
    UncaughtExceptionHandler.wrap(_grpc_client_timeout, timeout, log_level)


def _grpc_client_timeout(timeout, log_level):
    logger = cli_logger.create_cli_logger(log_level)
    context = env.LocalContextStorage.get_cli_env_context()

    context.grpc_client_timeout_sec = timeout
    click.echo("Set grpc client timeout to : " + timeout)


@save.command(
    help="Changes the maximum size of split that can be uploaded.",
    context_settings=CLI_CONTEXT_SETTINGS,
    hidden=True
)
@click.argument("new_size_in_bytes")
@click.option("--log_level", default=None, help=cli_logger.log_level_message)
def max_split_size(new_size_in_bytes, log_level):
    UncaughtExceptionHandler.wrap(
        _set_max_split_size, new_size_in_bytes, log_level
    )


def _set_max_split_size(new_size_in_bytes, log_level):
    logger = cli_logger.create_cli_logger(log_level)
    context = env.LocalContextStorage.get_cli_env_context()

    context.split_max_size = new_size_in_bytes
    click.echo(
        "Set maximum split size that can be uploaded to: " + new_size_in_bytes
    )


@save.command(
    help="Saves the authentication credentials.",
    context_settings=CLI_CONTEXT_SETTINGS
)
@click.option(
    "--username", "-u", help="User name for authentication.", required=False
)
@click.option(
    "--password", "-p", help="Password for authentication.", required=False
)
@click.option(
    "--token", "-t", help="Token for token authentication.", required=False
)
@click.option("--log_level", default=None, help=cli_logger.log_level_message)
def credentials(username, password, token, log_level):
    UncaughtExceptionHandler.wrap(
        _set_credentials, username, password, token, log_level
    )


def _set_credentials(username, password, token, log_level):
    logger = cli_logger.create_cli_logger(log_level)
    context = env.LocalContextStorage.get_cli_env_context()
    # TODO(AU) verify that the credentials work?
    if username:
        context.username = username
        if password:
            context.password = password
        else:
            raise click.UsageError(
                f"Please provide password associated with username {username} for authentication."
            )
    elif token:
        context.token = token
    else:
        raise click.UsageError(
            "Please provide username and password or token for authentication."
        )

    click.echo("Saved authentication details to context.")


@save.command(
    help=
    """Sets the logging level for the cli. Options are: 'Silent', 'Default' or 'Verbose'\b\n
    Silent  - Only display errors, json output.\n
    Default - Also display upload file progress, success messages.\n
    Verbose - Also display operation level info.""",
    context_settings=CLI_CONTEXT_SETTINGS
)
@click.argument("level", default="Default")
def log_level(level):
    context = env.LocalContextStorage.get_cli_env_context()
    context.log_level = level.lower()
    click.echo("Saved logging level as '{}'.".format(level))


if __name__ == '__main__':
    save()
