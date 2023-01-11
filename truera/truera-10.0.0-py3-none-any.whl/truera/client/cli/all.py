import click
from google.protobuf.json_format import MessageToJson

import truera.client.cli.cli_logger as cli_logger
from truera.client.cli.cli_utils import CLI_CONTEXT_SETTINGS
import truera.client.cli.cli_utils as cli_utils
from truera.client.cli.UncaughtExceptionHandler import UncaughtExceptionHandler
from truera.client.client_environment import connection_string_message
from truera.client.errors import AuthorizationDenied
from truera.client.services import user_manager_service_client
import truera.client.services.artifact_interaction_client as cl


@click.group(
    help="For command help, use <command> --help. Example: create-project --help."
)
def all():
    pass


@all.command(context_settings=CLI_CONTEXT_SETTINGS)
@click.option(
    "--connection_string", default=None, help=connection_string_message
)
@click.option("--log_level", default=None, help=cli_logger.log_level_message)
def projects(connection_string, log_level):
    logger = cli_logger.create_cli_logger(log_level)
    ar_client = cli_utils.get_artifact_repo_client(connection_string, logger)
    ds_client = cli_utils.get_data_service_client(connection_string, logger)

    with cl.ArtifactInteractionClient(ar_client, ds_client, logger) as client:
        click.echo(cli_utils._format_and_return_json(client.get_all_projects()))


@all.command(context_settings=CLI_CONTEXT_SETTINGS)
@click.option("--project_name", "-p", required=True)
@click.option(
    "--connection_string", default=None, help=connection_string_message
)
@click.option("--log_level", default=None, help=cli_logger.log_level_message)
def models(project_name, connection_string, log_level):
    logger = cli_logger.create_cli_logger(log_level)
    ar_client = cli_utils.get_artifact_repo_client(connection_string, logger)
    ds_client = cli_utils.get_data_service_client(connection_string, logger)

    with cl.ArtifactInteractionClient(ar_client, ds_client, logger) as client:
        click.echo(
            cli_utils._format_and_return_json(
                client.get_all_models_in_project(project_name)
            )
        )


@all.command(context_settings=CLI_CONTEXT_SETTINGS)
@click.option("--project_name", "-p", required=True)
@click.option("--data_collection_name", "-d", required=True)
@click.option(
    "--connection_string", default=None, help=connection_string_message
)
@click.option("--log_level", default=None, help=cli_logger.log_level_message)
def models_using_data_collection(
    project_name, data_collection_name, connection_string, log_level
):
    logger = cli_logger.create_cli_logger(log_level)
    ar_client = cli_utils.get_artifact_repo_client(connection_string, logger)
    ds_client = cli_utils.get_data_service_client(connection_string, logger)

    with cl.ArtifactInteractionClient(ar_client, ds_client, logger) as client:
        click.echo(
            cli_utils._format_and_return_json(
                client.get_all_models_in_project(
                    project_name, data_collection_name
                )
            )
        )


@all.command(context_settings=CLI_CONTEXT_SETTINGS)
@click.option("--project_name", "-p", required=True)
@click.option(
    "--connection_string", default=None, help=connection_string_message
)
@click.option("--log_level", default=None, help=cli_logger.log_level_message)
def data_collections(project_name, connection_string, log_level):
    logger = cli_logger.create_cli_logger(log_level)
    ar_client = cli_utils.get_artifact_repo_client(connection_string, logger)
    ds_client = cli_utils.get_data_service_client(connection_string, logger)

    with cl.ArtifactInteractionClient(ar_client, ds_client, logger) as client:
        click.echo(
            cli_utils._format_and_return_json(
                # TODO(AB#3454) This should be project id
                client.get_all_data_collections_in_project(project_name)
            )
        )


@all.command(context_settings=CLI_CONTEXT_SETTINGS)
@click.option("--project_name", "-p", required=True)
@click.option("--data_collection_name", "-d", required=True)
@click.option(
    "--connection_string", default=None, help=connection_string_message
)
@click.option("--log_level", default=None, help=cli_logger.log_level_message)
def splits(project_name, data_collection_name, connection_string, log_level):
    logger = cli_logger.create_cli_logger(log_level)
    ar_client = cli_utils.get_artifact_repo_client(connection_string, logger)
    ds_client = cli_utils.get_data_service_client(connection_string, logger)

    with cl.ArtifactInteractionClient(ar_client, ds_client, logger) as client:
        click.echo(
            cli_utils._format_and_return_json(
                client.get_all_datasplits_in_data_collection(
                    project_name, data_collection_name
                )
            )
        )


@all.command(context_settings=CLI_CONTEXT_SETTINGS)
@click.option("--project_name", "-p", required=True)
@click.option(
    "--connection_string", default=None, help=connection_string_message
)
@click.option("--log_level", default=None, help=cli_logger.log_level_message)
def feature_maps(project_name, connection_string, log_level):
    logger = cli_logger.create_cli_logger(log_level)
    ar_client = cli_utils.get_artifact_repo_client(connection_string, logger)
    ds_client = cli_utils.get_data_service_client(connection_string, logger)

    with cl.ArtifactInteractionClient(ar_client, ds_client, logger) as client:
        click.echo(
            cli_utils._format_and_return_json(
                client.get_all_feature_maps_in_project(project_name)
            )
        )


@all.command(context_settings=CLI_CONTEXT_SETTINGS)
@click.option("--project_name", "-p", required=True)
@click.option(
    "--connection_string", default=None, help=connection_string_message
)
@click.option("--log_level", default=None, help=cli_logger.log_level_message)
def data_sources(project_name, connection_string, log_level):
    UncaughtExceptionHandler.wrap(
        _get_all_data_sources, project_name, connection_string, log_level
    )


def _get_all_data_sources(project_name, connection_string, log_level):
    logger = cli_logger.create_cli_logger(log_level)
    ar_client = cli_utils.get_artifact_repo_client(connection_string, logger)
    ds_client = cli_utils.get_data_service_client(connection_string, logger)

    with cl.ArtifactInteractionClient(ar_client, ds_client, logger) as client:
        project_id = client.get_project_id(project_name)
        click.echo(
            cli_utils._format_and_return_json(
                client.get_all_data_sources_in_project(project_id)
            )
        )


@all.command(
    help="List available backups.", hidden=cli_utils.feature_is_hidden("admin")
)
@click.option(
    "--connection_string", default=None, help=connection_string_message
)
@click.option("--log_level", default=None, help=cli_logger.log_level_message)
def backups(connection_string, log_level):
    UncaughtExceptionHandler.wrap(_list_backup, connection_string, log_level)


def _list_backup(connection_string, log_level):
    logger = cli_logger.create_cli_logger(log_level)
    backup_client = cli_utils.get_backup_client(connection_string, logger)
    response = backup_client.list_backup()
    output_dict = {
        "backup_list":
            [backup.backup_folder_path for backup in response.backups]
    }
    click.echo(cli_utils._format_and_return_json(output_dict))


@all.command(
    help="List available billing metrics",
    hidden=cli_utils.feature_is_hidden("admin")
)
@click.option(
    "--connection_string", default=None, help=connection_string_message
)
@click.option("--log_level", default=None, help=cli_logger.log_level_message)
def billing_metrics(connection_string, log_level):
    UncaughtExceptionHandler.wrap(
        _get_billing_metrics, connection_string, log_level
    )


def _get_billing_metrics(connection_string, log_level):
    logger = cli_logger.create_cli_logger(log_level)
    billing_client = cli_utils.get_billing_client(connection_string, logger)
    response = billing_client.list_billing_metrics()
    output_dict = {"metrics_list": response}
    click.echo(cli_utils._format_and_return_json(output_dict))


@all.command(
    help="List available credentials.",
    hidden=cli_utils.feature_is_hidden("admin")
)
@click.option("--project_name", "-p")
@click.option(
    "--last_key",
    help=
    "If thre are more than 50 credentials available, last key can be used to paginate."
)
@click.option(
    "--connection_string", default=None, help=connection_string_message
)
@click.option("--log_level", default=None, help=cli_logger.log_level_message)
def credentials(project_name, last_key, connection_string, log_level):
    UncaughtExceptionHandler.wrap(
        _get_credentials, project_name, last_key, connection_string, log_level
    )


def _get_credentials(project_name, last_key, connection_string, log_level):
    logger = cli_logger.create_cli_logger(log_level)
    ar_client = cli_utils.get_artifact_repo_client(connection_string, logger)
    ds_client = cli_utils.get_data_service_client(connection_string, logger)

    with cl.ArtifactInteractionClient(ar_client, ds_client, logger) as client:
        if project_name:
            project_id = client.get_project_id(project_name)
        else:
            project_id = ""
        md, has_more_data = client.get_all_credentials(project_id, last_key)
        click.echo(
            cli_utils._format_and_return_json(
                {
                    "has_more_data": has_more_data,
                    "credentials": md
                }
            )
        )


@all.command(help="List available tables within a project along with status.")
@click.option("--project_name", "-p", required=True)
@click.option("--root_table_id")
@click.option("--only_root_tables", is_flag=True)
@click.option(
    "--include_system_requested", is_flag=True, hidden=True, default=False
)
@click.option(
    "--last_key",
    help=
    "If thre are more than 50 credentials available, last key can be used to paginate."
)
@click.option(
    "--connection_string", default=None, help=connection_string_message
)
@click.option("--log_level", default=None, help=cli_logger.log_level_message)
def tables(
    project_name, root_table_id, only_root_tables, last_key,
    include_system_requested, connection_string, log_level
):
    UncaughtExceptionHandler.wrap(
        _get_tables, project_name, root_table_id, only_root_tables, last_key,
        include_system_requested, connection_string, log_level
    )


def _get_tables(
    project_name, root_table_id, only_root_tables, last_key,
    include_system_requested, connection_string, log_level
):
    logger = cli_logger.create_cli_logger(log_level)
    ar_client = cli_utils.get_artifact_repo_client(connection_string, logger)
    ds_client = cli_utils.get_data_service_client(connection_string, logger)

    with cl.ArtifactInteractionClient(ar_client, ds_client, logger) as client:
        if project_name:
            project_id = client.get_project_id(project_name)
        else:
            project_id = ""
        md, has_more_data = client.get_all_rowsets(
            project_id,
            root_table_id,
            only_root_tables,
            last_key,
            include_system_requested=include_system_requested
        )
        click.echo(
            cli_utils._format_and_return_json(
                {
                    "has_more_data": has_more_data,
                    "tables": md
                }
            )
        )


@all.command(
    help="List materialize operations within a project along with status."
)
@click.option("--project_name", "-p", required=True)
@click.option(
    "--last_key",
    help=
    "If thre are more than 50 credentials available, last key can be used to paginate."
)
@click.option(
    "--connection_string", default=None, help=connection_string_message
)
@click.option("--log_level", default=None, help=cli_logger.log_level_message)
def materialize_operations(
    project_name, last_key, connection_string, log_level
):
    UncaughtExceptionHandler.wrap(
        _get_materialize_operations, project_name, last_key, connection_string,
        log_level
    )


def _get_materialize_operations(
    project_name, last_key, connection_string, log_level
):
    logger = cli_logger.create_cli_logger(log_level)
    ar_client = cli_utils.get_artifact_repo_client(connection_string, logger)
    ds_client = cli_utils.get_data_service_client(connection_string, logger)

    with cl.ArtifactInteractionClient(ar_client, ds_client, logger) as client:
        if project_name:
            project_id = client.get_project_id(project_name)
        else:
            project_id = ""
        md, has_more_data = client.get_materialize_operations(
            project_id, last_key
        )
        click.echo(
            cli_utils._format_and_return_json(
                {
                    "has_more_data": has_more_data,
                    "materialize-operations": md
                }
            )
        )


@all.command(
    context_settings=CLI_CONTEXT_SETTINGS,
    hidden=cli_utils.feature_is_hidden("rbac_admin")
)
@click.option(
    "--connection_string", default=None, help=connection_string_message
)
@click.option("--log_level", default=None, help=cli_logger.log_level_message)
def users(connection_string, log_level):
    UncaughtExceptionHandler.wrap(_users, connection_string, log_level)


def _users(connection_string, log_level):
    logger = cli_logger.create_cli_logger(log_level)
    user_manager_client = cli_utils.get_user_manager_service_client(
        connection_string, logger
    )
    rbac_client = cli_utils.get_rbac_service_client(connection_string, logger)
    current_user = user_manager_client.get_current_user()
    if not rbac_client.is_user_admin(current_user.id):
        raise AuthorizationDenied("this method can be accessed by admins only")
    click.echo(MessageToJson(user_manager_client.get_users()))


@all.command(
    help="List available audit summary metrics",
    hidden=cli_utils.feature_is_hidden("admin")
)
@click.option(
    "--connection_string", default=None, help=connection_string_message
)
@click.option("--log_level", default=None, help=cli_logger.log_level_message)
def audit_summary_metrics(connection_string, log_level):
    UncaughtExceptionHandler.wrap(
        _get_audit_summary_metrics, connection_string, log_level
    )


def _get_audit_summary_metrics(connection_string, log_level):
    logger = cli_logger.create_cli_logger(log_level)
    billing_client = cli_utils.get_billing_client(connection_string, logger)
    response = billing_client.list_audit_summary_metrics()
    output_dict = {"metrics_list": response}
    click.echo(cli_utils._format_and_return_json(output_dict))


if __name__ == '__main__':
    all()
