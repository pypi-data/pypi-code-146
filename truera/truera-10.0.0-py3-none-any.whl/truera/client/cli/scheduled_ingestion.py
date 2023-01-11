import json

import click
from google.protobuf.json_format import MessageToJson

import truera.client.cli.cli_logger as cli_logger
from truera.client.cli.cli_utils import CLI_CONTEXT_SETTINGS
import truera.client.cli.cli_utils as cli_utils
from truera.client.client_environment import connection_string_message


@click.group(
    help="Commands for scheduling period ingestion",
    hidden=cli_utils.feature_is_hidden("scheduled_ingestion")
)
def scheduled_ingestion():
    pass


@scheduled_ingestion.command(context_settings=CLI_CONTEXT_SETTINGS)
@click.option(
    "--project_name", "-p", help="Name of the project.", required=True
)
@click.option(
    "--data_collection_name",
    "-d",
    help="Name of the data_collection.",
    required=True
)
@click.option(
    "--existing_split_name",
    help="Name of the existing split from the data collection to use as a base.",
    required=True
)
@click.option(
    "--override_split_name",
    help=(
        "Name of the new splits created by periodic ingestion.  Can be templated, for more "
        "information see scheduled ingestion sdk docs."
    ),
    required=True
)
@click.option(
    "--schedule",
    help=
    "The unix cron schedule string.  Follows cron unix format.  For more information: https://en.wikipedia.org/wiki/Cron",
    required=True
)
@click.option(
    "--connection_string", default=None, help=connection_string_message
)
@click.option("--log_level", default=None, help=cli_logger.log_level_message)
def schedule_existing_split(
    project_name,
    data_collection_name,
    existing_split_name,
    schedule,
    connection_string,
    log_level,
    override_split_name: str = None,
    append: bool = True
):
    logger = cli_logger.create_cli_logger(log_level)

    ar_client = cli_utils.get_artifact_repo_client(connection_string, logger)
    ds_client = cli_utils.get_data_service_client(connection_string, logger)
    si_client = cli_utils.get_scheduled_ingestion_client(
        connection_string, logger
    )

    split_metadata = ar_client.get_datasplit_metadata(
        project_name,
        data_collection_name=data_collection_name,
        datasplit_name=existing_split_name,
        as_json=False
    )
    if not split_metadata.provenance.materialized_by_operation:
        raise click.UsageError(
            "Attempting to schedule a split that wasn't materialized by data layer"
        )
    materialize_operation_id = split_metadata.provenance.materialized_by_operation
    materialize_response = ds_client.get_materialize_data_status(
        split_metadata.project_id,
        materialize_operation_id,
        throw_on_error=True
    )
    if append:
        request_tree = si_client.build_request_tree(
            materialize_status_response=materialize_response,
            project_id=split_metadata.project_id,
            existing_split_id=split_metadata.id,
        )
    else:
        request_tree = si_client.build_request_tree(
            materialize_status_response=materialize_response,
            project_id=split_metadata.project_id,
            override_split_name=override_split_name,
        )
    workflow_id = si_client.schedule_new(
        tree=request_tree, schedule=si_client.serialize_schedule(schedule)
    )
    click.echo(json.dumps({"workflow_id": workflow_id}))


@scheduled_ingestion.command(context_settings=CLI_CONTEXT_SETTINGS)
@click.option("--workflow_id", help="Id of the workflow.", required=True)
@click.option(
    "--connection_string", default=None, help=connection_string_message
)
@click.option("--log_level", default=None, help=cli_logger.log_level_message)
def get(workflow_id, connection_string, log_level):
    logger = cli_logger.create_cli_logger(log_level)

    si_client = cli_utils.get_scheduled_ingestion_client(
        connection_string, logger
    )

    result = si_client.get(workflow_id)
    click.echo(MessageToJson(result))
