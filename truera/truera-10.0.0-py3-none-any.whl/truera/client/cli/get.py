import tempfile

import click
from google.protobuf.json_format import MessageToJson

from truera.client.cli.all import all
import truera.client.cli.cli_logger as cli_logger
from truera.client.cli.cli_utils import CLI_CONTEXT_SETTINGS
import truera.client.cli.cli_utils as cli_utils
from truera.client.cli.config import config
from truera.client.cli.sample import sample
from truera.client.cli.status import status
from truera.client.cli.UncaughtExceptionHandler import UncaughtExceptionHandler
from truera.client.client_environment import connection_string_message
from truera.client.client_utils import rowset_status_to_str
from truera.client.errors import AuthorizationDenied
import truera.client.services.artifact_interaction_client as cl
from truera.client.services.artifactrepo_client import ArtifactMetaFetchMode
from truera.client.services.artifactrepo_client import ArtifactType


@click.group(help="Commands for getting information about artifacts in truera.")
def get():
    pass


get.add_command(config)
get.add_command(all)
get.add_command(sample)
get.add_command(status)


@get.command(
    help="Get the specified project's metadata.",
    context_settings=CLI_CONTEXT_SETTINGS
)
@click.option("--project_name", "-p", required=True)
@click.option(
    "--connection_string", default=None, help=connection_string_message
)
@click.option("--log_level", default=None, help=cli_logger.log_level_message)
def project_metadata(project_name, connection_string, log_level):
    UncaughtExceptionHandler.wrap(
        _get_project_metadata, project_name, connection_string, log_level
    )


def _get_project_metadata(project_name, connection_string, log_level):
    logger = cli_logger.create_cli_logger(log_level)
    ar_client = cli_utils.get_artifact_repo_client(connection_string, logger)
    ds_client = cli_utils.get_data_service_client(connection_string, logger)

    with cl.ArtifactInteractionClient(ar_client, ds_client, logger) as client:
        project_metadata = cli_utils._format_and_return_json(
            client.get_project_metadata(project_name)
        )
        click.echo(project_metadata)


@get.command(
    help="Get the specified model's metadata.",
    context_settings=CLI_CONTEXT_SETTINGS
)
@click.option("--project_name", "-p", required=True)
@click.option("--model_name", "-m", required=True)
@click.option(
    "--connection_string", default=None, help=connection_string_message
)
@click.option("--log_level", default=None, help=cli_logger.log_level_message)
def model_metadata(project_name, model_name, connection_string, log_level):
    UncaughtExceptionHandler.wrap(
        _get_model_metadata, project_name, model_name, connection_string,
        log_level
    )


def _get_model_metadata(project_name, model_name, connection_string, log_level):
    logger = cli_logger.create_cli_logger(log_level)
    ar_client = cli_utils.get_artifact_repo_client(connection_string, logger)
    ds_client = cli_utils.get_data_service_client(connection_string, logger)

    with cl.ArtifactInteractionClient(ar_client, ds_client, logger) as client:
        model_metadata = cli_utils._format_and_return_json(
            client.get_model_metadata(project_name, model_name)
        )
        click.echo(model_metadata)


@get.command(
    help="Get the specified data collection's metadata.",
    context_settings=CLI_CONTEXT_SETTINGS
)
@click.option("--project_name", "-p", required=True)
@click.option("--data_collection_name", "-d", required=True)
@click.option(
    "--connection_string", default=None, help=connection_string_message
)
@click.option("--log_level", default=None, help=cli_logger.log_level_message)
def data_collection_metadata(
    project_name, data_collection_name, connection_string, log_level
):
    UncaughtExceptionHandler.wrap(
        _get_data_collection_metadata, project_name, data_collection_name,
        connection_string, log_level
    )


def _get_data_collection_metadata(
    project_name, data_collection_name, connection_string, log_level
):
    logger = cli_logger.create_cli_logger(log_level)
    ar_client = cli_utils.get_artifact_repo_client(connection_string, logger)
    ds_client = cli_utils.get_data_service_client(connection_string, logger)

    with cl.ArtifactInteractionClient(ar_client, ds_client, logger) as client:
        data_collection_metadata = cli_utils._format_and_return_json(
            client.get_data_collection_metadata(
                project_name, data_collection_name
            )
        )
        click.echo(data_collection_metadata)


@get.command(
    help="Get the specified split's metadata.",
    context_settings=CLI_CONTEXT_SETTINGS
)
@click.option("--project_name", "-p", required=True)
@click.option("--data_collection_name", "-d", required=True)
@click.option("--split_name", "-s", required=True)
@click.option(
    "--connection_string", default=None, help=connection_string_message
)
@click.option("--log_level", default=None, help=cli_logger.log_level_message)
def split_metadata(
    project_name, data_collection_name, split_name, connection_string, log_level
):
    UncaughtExceptionHandler.wrap(
        _get_split_metadata, project_name, data_collection_name, split_name,
        connection_string, log_level
    )


def _get_split_metadata(
    project_name, data_collection_name, split_name, connection_string, log_level
):
    logger = cli_logger.create_cli_logger(log_level)
    ar_client = cli_utils.get_artifact_repo_client(connection_string, logger)
    ds_client = cli_utils.get_data_service_client(connection_string, logger)

    with cl.ArtifactInteractionClient(ar_client, ds_client, logger) as client:
        split_metadata = client.get_split_metadata(
            project_name, data_collection_name, split_name
        )

        click.echo(cli_utils._format_and_return_json(split_metadata))


@get.command(
    help="Get the specified feature list.",
    context_settings=CLI_CONTEXT_SETTINGS
)
@click.option("--project_name", "-p", required=True)
@click.option("--data_collection_name", "-d", required=True)
@click.option(
    "--connection_string", default=None, help=connection_string_message
)
@click.option("--log_level", default=None, help=cli_logger.log_level_message)
def feature_list(
    project_name, data_collection_name, connection_string, log_level
):
    UncaughtExceptionHandler.wrap(
        _get_feature_list, project_name, data_collection_name,
        connection_string, log_level
    )


def _get_feature_list(
    project_name, data_collection_name, connection_string, log_level
):
    logger = cli_logger.create_cli_logger(log_level)
    ar_client = cli_utils.get_artifact_repo_client(connection_string, logger)
    ds_client = cli_utils.get_data_service_client(connection_string, logger)

    with cl.ArtifactInteractionClient(ar_client, ds_client, logger) as client:
        feature_list = client.get_feature_list(
            project_name, data_collection_name
        )
        click.echo(cli_utils._format_and_return_json(feature_list))


@get.command(
    help="Get saved connection details.", context_settings=CLI_CONTEXT_SETTINGS
)
@click.option(
    "--show_password/--hide_password",
    default=False,
    help=cli_logger.log_level_message
)
@click.option("--log_level", default=None, help=cli_logger.log_level_message)
def connection_detail(log_level, show_password):
    UncaughtExceptionHandler.wrap(
        _get_connection_detail, show_password, log_level
    )


def _get_connection_detail(show_password, log_level):
    connection_string = cli_utils._get_connection_string(None)
    use_http = cli_utils._get_use_http()
    auth_details = None
    try:
        auth_details = cli_utils._get_auth_details()
    except click.UsageError:
        pass
    details = dict()
    details["connection_string"] = connection_string
    details["use_http"] = use_http
    if auth_details:
        details["username"] = auth_details.username
        if show_password:
            details["password"] = auth_details.password
        if auth_details.token:
            details["token"] = f"...{auth_details.token[-10:]}"

    click.echo(cli_utils._format_and_return_json(details))


@get.command(
    help="Get the columns in a given table.",
    context_settings=CLI_CONTEXT_SETTINGS
)
@click.option("--project_name", "-p", required=True)
@click.option("--table_id", "-t")
@click.option("--data_source_name", "--dsn")
@click.option(
    "--connection_string", default=None, help=connection_string_message
)
@click.option("--log_level", default=None, help=cli_logger.log_level_message)
def schema_of_table(
    project_name, table_id, data_source_name, connection_string, log_level
):
    UncaughtExceptionHandler.wrap(
        _get_schema_of_table, project_name, table_id, data_source_name,
        connection_string, log_level
    )


def _get_schema_of_table(
    project_name, table_id, data_source_name, connection_string, log_level
):
    logger = cli_logger.create_cli_logger(log_level)
    ar_client = cli_utils.get_artifact_repo_client(connection_string, logger)
    ds_client = cli_utils.get_data_service_client(connection_string, logger)

    with cl.ArtifactInteractionClient(ar_client, ds_client, logger) as client:
        project_id = client.get_project_id(project_name)
        columns, status, error = client.get_schema_of_rowset(
            project_id, table_id, data_source_name
        )
        status = rowset_status_to_str(status)
        click.echo(cli_utils.format_columns_output(columns, status, error))


@get.command(
    help="Get the metadata for a given data source.",
    context_settings=CLI_CONTEXT_SETTINGS
)
@click.option("--project_name", "-p")
@click.option("--data_source_name", "--dsn")
@click.option(
    "--connection_string", default=None, help=connection_string_message
)
@click.option("--log_level", default=None, help=cli_logger.log_level_message)
def data_source_metadata(
    project_name, data_source_name, connection_string, log_level
):
    UncaughtExceptionHandler.wrap(
        _get_data_source_metadata, project_name, data_source_name,
        connection_string, log_level
    )


@get.command(
    help="Get a schema by ID.",
    context_settings=CLI_CONTEXT_SETTINGS,
    hidden=cli_utils.feature_is_hidden("schema_apis")
)
@click.option("--schema_id")
@click.option(
    "--connection_string", default=None, help=connection_string_message
)
@click.option("--log_level", default=None, help=cli_logger.log_level_message)
def schema_by_id(schema_id, connection_string, log_level):
    UncaughtExceptionHandler.wrap(
        _get_schema_by_id, schema_id, connection_string, log_level
    )


def _get_schema_by_id(schema_id, connection_string, log_level):
    logger = cli_logger.create_cli_logger(log_level)
    ds_client = cli_utils.get_data_service_client(connection_string, logger)
    schema_md = ds_client.get_schema(schema_id, as_json=True)
    click.echo(cli_utils._format_and_return_json(schema_md))


def _get_data_source_metadata(
    project_name, data_source_name, connection_string, log_level
):
    logger = cli_logger.create_cli_logger(log_level)
    ar_client = cli_utils.get_artifact_repo_client(connection_string, logger)
    ds_client = cli_utils.get_data_service_client(connection_string, logger)

    with cl.ArtifactInteractionClient(ar_client, ds_client, logger) as client:
        project_id = client.get_project_id(project_name)
        rowset_id = client.get_root_rowset_by_name(project_id, data_source_name)
        md = client.get_rowset_metadata(rowset_id)
        click.echo(cli_utils._format_and_return_json(md))


@get.command(context_settings=CLI_CONTEXT_SETTINGS)
@click.option("--id")
@click.option("--name", "-n")
@click.option(
    "--connection_string", default=None, help=connection_string_message
)
@click.option("--log_level", default=None, help=cli_logger.log_level_message)
def credential_metadata(id, name, connection_string, log_level):
    UncaughtExceptionHandler.wrap(
        _get_credential_metadata, id, name, connection_string, log_level
    )


def _get_credential_metadata(
    credential_id, credential_name, connection_string, log_level
):
    logger = cli_logger.create_cli_logger(log_level)
    ar_client = cli_utils.get_artifact_repo_client(connection_string, logger)
    ds_client = cli_utils.get_data_service_client(connection_string, logger)

    with cl.ArtifactInteractionClient(ar_client, ds_client, logger) as client:
        credential_metadata = client.get_credential_metadata(
            credential_id=credential_id, credential_name=credential_name
        )
        del credential_metadata["storage_key"]
        click.echo(cli_utils._format_and_return_json(credential_metadata))


@get.command(
    help="Generate usage metrics report.",
    hidden=cli_utils.feature_is_hidden("admin")
)
@click.option(
    "--start_date",
    help="Start date to generate report in MM-DD-YYYY format, in UTC timezone"
)
@click.option(
    "--end_date",
    help="End date to generate report in MM-DD-YYYY format, in UTC timezone"
)
@click.option(
    "--connection_string", default=None, help=connection_string_message
)
@click.option("--log_level", default=None, help=cli_logger.log_level_message)
def usage_report(start_date, end_date, connection_string, log_level):
    UncaughtExceptionHandler.wrap(
        _get_usage_report, start_date, end_date, connection_string, log_level
    )


def _get_usage_report(start_date, end_date, connection_string, log_level):
    logger = cli_logger.create_cli_logger(log_level)
    billing_client = cli_utils.get_billing_client(connection_string, logger)
    response = billing_client.generate_report(
        start_date_str=start_date, end_date_str=end_date
    )
    json_response = MessageToJson(
        response,
        including_default_value_fields=True,
        preserving_proto_field_name=True
    )
    click.echo(json_response)


@get.command(
    context_settings=CLI_CONTEXT_SETTINGS,
    hidden=cli_utils.feature_is_hidden("rbac_admin")
)
@click.option(
    "--connection_string", default=None, help=connection_string_message
)
@click.option("--log_level", default=None, help=cli_logger.log_level_message)
def user_project_matrix(connection_string, log_level):
    UncaughtExceptionHandler.wrap(
        _user_project_matrix, connection_string, log_level
    )


def _user_project_matrix(connection_string, log_level):
    logger = cli_logger.create_cli_logger(log_level)
    ar_client = cli_utils.get_artifact_repo_client(connection_string, logger)
    um_client = cli_utils.get_user_manager_service_client(
        connection_string, logger
    )
    rbac_client = cli_utils.get_rbac_service_client(connection_string, logger)
    current_user = um_client.get_current_user()
    if not rbac_client.is_user_admin(current_user.id):
        raise AuthorizationDenied("this method can be accessed by admins only")
    projects = ar_client.list_all(
        artifact_type=ArtifactType.project,
        ar_meta_fetch_mode=ArtifactMetaFetchMode.ALL
    )
    project_name_ids = {p["id"]: p["name"] for p in projects["name_id_pairs"]}
    users = um_client.get_users().users
    click.echo(
        cli_utils._format_and_return_json(
            [
                entry.__dict__ for entry in
                rbac_client.get_user_project_matrix(project_name_ids, users)
            ]
        )
    )


@get.command(
    help="Generate audit summary metrics report.",
    hidden=cli_utils.feature_is_hidden("admin")
)
@click.option(
    "--metrics",
    default=None,
    help=
    "Comma seperated metric names as obtained from tru get all audit-summary-metrics, if not supplied then report will be generated for all audit summary metrics"
)
@click.option(
    "--start_datetime",
    required=True,
    help=
    "Start datetime to generate report in \"mm-dd-YYYY HH:MM\" format, in UTC timezone"
)
@click.option(
    "--end_datetime",
    required=True,
    help=
    "End datetime to generate report in \"mm-dd-YYYY HH:MM\" format, in UTC timezone"
)
@click.option(
    "--connection_string", default=None, help=connection_string_message
)
@click.option("--log_level", default=None, help=cli_logger.log_level_message)
def audit_summary_report(
    metrics, start_datetime, end_datetime, connection_string, log_level
):
    UncaughtExceptionHandler.wrap(
        _get_audit_summary_report, metrics, start_datetime, end_datetime,
        connection_string, log_level
    )


def _get_audit_summary_report(
    metrics_str, start_datetime, end_datetime, connection_string, log_level
):
    logger = cli_logger.create_cli_logger(log_level)
    billing_client = cli_utils.get_billing_client(connection_string, logger)
    metrics_list = [] if metrics_str is None or len(
        metrics_str
    ) == 0 else metrics_str.split(",")
    response = billing_client.generate_audit_summary_report(
        metrics=metrics_list,
        start_datetime_str=start_datetime,
        end_datetime_str=end_datetime
    )
    json_response = MessageToJson(
        response,
        including_default_value_fields=True,
        preserving_proto_field_name=True
    )
    click.echo(json_response)


@get.command(
    help="Get Druid tables list.", hidden=cli_utils.feature_is_hidden("admin")
)
@click.option("--project_name", "-p", required=True)
@click.option(
    "--connection_string", default=None, help=connection_string_message
)
@click.option("--log_level", default=None, help=cli_logger.log_level_message)
def monitoring_tables(project_name, connection_string, log_level):
    UncaughtExceptionHandler.wrap(
        _get_monitoring_tables, project_name, connection_string, log_level
    )


def _get_monitoring_tables(project_name, connection_string, log_level):
    logger = cli_logger.create_cli_logger(log_level)
    monitoring_control_client = cli_utils.get_monitoring_control_plane_client(
        connection_string, logger
    )
    ar_client = cli_utils.get_artifact_repo_client(connection_string, logger)
    ds_client = cli_utils.get_data_service_client(connection_string, logger)

    with cl.ArtifactInteractionClient(ar_client, ds_client, logger) as client:
        project_id = client.get_project_id(project_name)
        response = monitoring_control_client.list_druid_tables(
            project_id=project_id
        )
        json_response = MessageToJson(
            response,
            including_default_value_fields=True,
            preserving_proto_field_name=True
        )
        click.echo(json_response)


if __name__ == '__main__':
    get()
