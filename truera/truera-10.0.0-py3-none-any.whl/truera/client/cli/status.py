import os

import click

import truera.client.cli.cli_logger as cli_logger
from truera.client.cli.cli_utils import CLI_CONTEXT_SETTINGS
import truera.client.cli.cli_utils as cli_utils
from truera.client.cli.UncaughtExceptionHandler import UncaughtExceptionHandler
from truera.client.client_environment import connection_string_message
import truera.client.services.artifact_interaction_client as cl


@click.group(help="Get the status of a connection or operation.")
def status():
    pass


@status.command(context_settings=CLI_CONTEXT_SETTINGS)
@click.option("--project_name", "-p", required=True)
@click.option("--data_source_name", "--dsn", help="Name of a data source.")
@click.option("--table_id", help="Id of the table.")
@click.option(
    "--connection_string", default=None, help=connection_string_message
)
@click.option("--log_level", default=None, help=cli_logger.log_level_message)
def table(
    project_name, data_source_name, table_id, connection_string, log_level
):
    UncaughtExceptionHandler.wrap(
        _get_table_status, project_name, data_source_name, table_id,
        connection_string, log_level
    )


def _get_table_status(
    project_name, data_source_name, table_id, connection_string, log_level
):
    logger = cli_logger.create_cli_logger(log_level)
    ar_client = cli_utils.get_artifact_repo_client(connection_string, logger)
    ds_client = cli_utils.get_data_service_client(connection_string, logger)

    with cl.ArtifactInteractionClient(ar_client, ds_client, logger) as client:
        project_id = client.get_project_id(project_name)
        status, error = client.get_rowset_status(
            project_id, data_source_name, table_id
        )
        output_dict = {"data_source_status": status}
        if error or status == "FAILED":
            output_dict["error"] = error
        click.echo(cli_utils._format_and_return_json(output_dict))


@status.command(context_settings=CLI_CONTEXT_SETTINGS)
@click.option("--project_name", "-p", required=True)
@click.option(
    "--operation_id", help="Id of the materialize operation.", required=True
)
@click.option(
    "--connection_string", default=None, help=connection_string_message
)
@click.option("--log_level", default=None, help=cli_logger.log_level_message)
def materialize_operation(
    project_name, operation_id, connection_string, log_level
):
    UncaughtExceptionHandler.wrap(
        _get_materialize_operation_status, project_name, operation_id,
        connection_string, log_level
    )


def _get_materialize_operation_status(
    project_name, operation_id, connection_string, log_level
):
    logger = cli_logger.create_cli_logger(log_level)
    ar_client = cli_utils.get_artifact_repo_client(connection_string, logger)
    ds_client = cli_utils.get_data_service_client(connection_string, logger)

    with cl.ArtifactInteractionClient(ar_client, ds_client, logger) as client:
        project_id = client.get_project_id(project_name)
        status, error = client.get_materialize_operation_status(
            project_id, operation_id
        )
        output_dict = {"materialize_status": status}
        if error:
            output_dict["error"] = error
        click.echo(cli_utils._format_and_return_json(output_dict))
