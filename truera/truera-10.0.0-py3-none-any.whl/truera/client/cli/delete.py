import os
import sys

import click

import truera.client.cli.cli_logger as cli_logger
from truera.client.cli.cli_utils import CLI_CONTEXT_SETTINGS
import truera.client.cli.cli_utils as cli_utils
from truera.client.cli.UncaughtExceptionHandler import UncaughtExceptionHandler
from truera.client.client_environment import connection_string_message
import truera.client.services.artifact_interaction_client as cl
from truera.client.services.artifactrepo_client import DeleteFailedException


@click.group(help="Commands for deleting artifacts in truera.")
def delete():
    pass


@delete.command(context_settings=CLI_CONTEXT_SETTINGS)
@click.option("--project_name", "-p", required=True)
@click.option(
    "--recursive",
    "-r",
    is_flag=True,
    help=
    "Delete child entities as well as the project: models, data collections, splits, etc. This will prompt with a list unless force is set."
)
@click.option(
    "--force",
    "-f",
    is_flag=True,
    help=
    "If recursive is set, delete recursively and do not prompt. Use with caution."
)
@click.option(
    "--connection_string", default=None, help=connection_string_message
)
@click.option("--log_level", default=None, help=cli_logger.log_level_message)
def project(project_name, recursive, force, connection_string, log_level):
    UncaughtExceptionHandler.wrap(
        _delete_project, project_name, recursive, force, connection_string,
        log_level
    )


def _delete_project(
    project_name, recursive, force, connection_string, log_level
):
    logger = cli_logger.create_cli_logger(log_level)
    ar_client = cli_utils.get_artifact_repo_client(connection_string, logger)
    ds_client = cli_utils.get_data_service_client(connection_string, logger)

    with cl.ArtifactInteractionClient(ar_client, ds_client, logger) as client:
        success, remaining_list = client.delete_project(project_name)

        if success:
            click.echo("Done")
        elif recursive:
            if not force:
                click.echo(
                    "WARNING: project is not empty. The following entities will be deleted if you proceed:"
                )
                click.echo(cli_utils.format_remaining_list(remaining_list))
                click.echo("")
                entered_project_name = input(
                    "To proceed please reenter project name (This cannot be undone):"
                )
                if not entered_project_name == project_name:
                    click.echo(
                        f"Project name does not match. Project was {project_name} vs. {entered_project_name} from confirmation."
                    )
                    sys.exit(1)

            client.delete_project(project_name, recursive)
            click.echo("Done")
        else:
            message = "WARNING: project is not empty. The following entities were found:"
            message += "\n"
            message += cli_utils.format_remaining_list(remaining_list)
            message += "\n"
            message += "Please delete these entities first, or call again with the recursive flag set."
            message += "\n"
            raise DeleteFailedException(message)


@delete.command(context_settings=CLI_CONTEXT_SETTINGS)
@click.option("--project_name", "-p", required=True)
@click.option("--model_name", "-m", required=True)
@click.option(
    "--recursive",
    "-r",
    is_flag=True,
    help=
    "Delete associated model tests. This will prompt for confirmation with a list of affected tests unless `force` flag is set."
)
@click.option(
    "--force",
    "-f",
    is_flag=True,
    help=
    "If recursive is set, delete recursively and do not prompt. Use with caution."
)
@click.option(
    "--connection_string", default=None, help=connection_string_message
)
@click.option("--log_level", default=None, help=cli_logger.log_level_message)
def model(
    project_name, model_name, recursive, force, connection_string, log_level
):
    UncaughtExceptionHandler.wrap(
        _delete_model, project_name, model_name, recursive, force,
        connection_string, log_level
    )


def _delete_model(
    project_name, model_name, recursive, force, connection_string, log_level
):
    logger = cli_logger.create_cli_logger(log_level)
    ar_client = cli_utils.get_artifact_repo_client(connection_string, logger)
    ds_client = cli_utils.get_data_service_client(connection_string, logger)

    with cl.ArtifactInteractionClient(ar_client, ds_client, logger) as client:
        success, remaining_list = client.delete_model(project_name, model_name)

        if success:
            click.echo("Done")

        elif recursive:
            if not force:
                click.echo(
                    "WARNING: model is used as reference model in the following model tests:"
                )
                click.echo(cli_utils.format_remaining_list(remaining_list))
                click.echo("")
                entered_model_name = input(
                    "To proceed please reenter model name (This cannot be undone):"
                )
                if not entered_model_name == model_name:
                    click.echo(
                        f"Entered model name does not match. Model was {model_name} vs. {entered_model_name} from confirmation."
                    )
                    sys.exit(1)

            client.delete_model(project_name, model_name, recursive=recursive)
            click.echo("Done")
        else:
            message = "WARNING: model is used as reference model in the following model tests:"
            message += "\n"
            message += cli_utils.format_remaining_list(remaining_list)
            message += "\n"
            message += "Please delete these entities first, or call again with the recursive flag set."
            message += "\n"
            raise DeleteFailedException(message)


@delete.command(context_settings=CLI_CONTEXT_SETTINGS)
@click.option("--project_name", "-p", required=True)
@click.option("--data_collection_name", "-d", required=True)
@click.option(
    "--recursive",
    "-r",
    is_flag=True,
    help=
    "Delete child entities as well as the data collection: splits, feature list. This will prompt with a list unless force is set."
)
@click.option(
    "--force",
    "-f",
    is_flag=True,
    help=
    "If recursive is set, delete recursively, ignore models using this data collection, and do not prompt. Use with caution."
)
@click.option(
    "--connection_string", default=None, help=connection_string_message
)
@click.option(
    "--log_level",
    default=None,
    help=cli_logger.log_level_message,
)
def data_collection(
    project_name, data_collection_name, recursive, force, connection_string,
    log_level
):
    UncaughtExceptionHandler.wrap(
        _delete_data_collection, project_name, data_collection_name, recursive,
        force, connection_string, log_level
    )


def _delete_data_collection(
    project_name, data_collection_name, recursive, force, connection_string,
    log_level
):
    logger = cli_logger.create_cli_logger(log_level)
    ar_client = cli_utils.get_artifact_repo_client(connection_string, logger)
    ds_client = cli_utils.get_data_service_client(connection_string, logger)

    with cl.ArtifactInteractionClient(ar_client, ds_client, logger) as client:

        models_using_data_collection = client.get_all_models_in_project(
            project_name, data_collection_name
        )

        if len(models_using_data_collection) > 0 and not force:
            click.echo(
                f"ERROR: data collection is used by the following models: {models_using_data_collection}."
            )
            exit(1)

        success, remaining_list = client.delete_data_collection(
            project_name, data_collection_name
        )

        if success:
            click.echo("Done")
        elif recursive:
            if not force:
                click.echo(
                    "WARNING: data collection is not empty. The following entities were found:"
                )
                click.echo(cli_utils.format_remaining_list(remaining_list))
                click.echo("")
                entered_data_collection_name = input(
                    "To proceed please reenter data collection name (This cannot be undone):"
                )
                if not data_collection_name == data_collection_name:
                    click.echo(
                        f"Data collection name name does not match. Data collection was {data_collection_name} vs. {entered_data_collection_name} from confirmation."
                    )
                    sys.exit(1)

            client.delete_data_collection(
                project_name, data_collection_name, recursive
            )
            click.echo("Done")
        else:
            message = "WARNING: data collection is not empty. The following entities were found:"
            message += "\n"
            message += cli_utils.format_remaining_list(remaining_list)
            message += "\n"
            message += "Please delete these entities first, or call again with the recursive flag set."
            message += "\n"
            raise DeleteFailedException(message)


@delete.command(context_settings=CLI_CONTEXT_SETTINGS)
@click.option("--project_name", "-p", required=True)
@click.option("--data_collection_name", "-d", required=True)
@click.option("--split_name", "-s", required=True)
@click.option(
    "--recursive",
    "-r",
    is_flag=True,
    help=
    "Delete associated model tests. This will prompt for confirmation with a list of affected tests unless `force` flag is set."
)
@click.option(
    "--force",
    "-f",
    is_flag=True,
    help=
    "If recursive is set, delete recursively and do not prompt. Use with caution."
)
@click.option(
    "--connection_string", default=None, help=connection_string_message
)
@click.option("--log_level", default=None, help=cli_logger.log_level_message)
def split(
    project_name, data_collection_name, split_name, recursive, force,
    connection_string, log_level
):
    UncaughtExceptionHandler.wrap(
        _delete_split, project_name, data_collection_name, split_name,
        recursive, force, connection_string, log_level
    )


def _delete_split(
    project_name, data_collection_name, split_name, recursive, force,
    connection_string, log_level
):
    logger = cli_logger.create_cli_logger(log_level)
    ar_client = cli_utils.get_artifact_repo_client(connection_string, logger)
    ds_client = cli_utils.get_data_service_client(connection_string, logger)

    with cl.ArtifactInteractionClient(ar_client, ds_client, logger) as client:
        success, remaining_list = client.delete_data_split(
            project_name, data_collection_name, split_name
        )

        if success:
            click.echo("Done")
        elif recursive:
            if not force:
                click.echo(
                    "WARNING: data split is associated with the following model tests:"
                )
                click.echo(cli_utils.format_remaining_list(remaining_list))
                click.echo("")
                entered_data_split_name = input(
                    "To proceed please reenter data split name (This cannot be undone):"
                )
                if not entered_data_split_name == split_name:
                    click.echo(
                        f"Entered data split name does not match. Data split was {split_name} vs. {entered_data_split_name} from confirmation."
                    )
                    sys.exit(1)

            client.delete_data_split(
                project_name,
                data_collection_name,
                split_name,
                recursive=recursive
            )
            click.echo("Done")
        else:
            message = "WARNING: data split is associated with the following model tests:"
            message += "\n"
            message += cli_utils.format_remaining_list(remaining_list)
            message += "\n"
            message += "Please delete these entities first, or call again with the recursive flag set."
            message += "\n"
            raise DeleteFailedException(message)


@delete.command(context_settings=CLI_CONTEXT_SETTINGS)
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
        _delete_feature_list, project_name, data_collection_name,
        connection_string, log_level
    )


def _delete_feature_list(
    project_name, data_collection_name, connection_string, log_level
):
    logger = cli_logger.create_cli_logger(log_level)
    ar_client = cli_utils.get_artifact_repo_client(connection_string, logger)
    ds_client = cli_utils.get_data_service_client(connection_string, logger)

    with cl.ArtifactInteractionClient(ar_client, ds_client, logger) as client:
        client.delete_feature_map(project_name, data_collection_name)
        click.echo("Done")


@delete.command(context_settings=CLI_CONTEXT_SETTINGS)
@click.option("--project_name", "-p", required=True)
@click.option("--name", "-n", required=True)
@click.option(
    "--connection_string", default=None, help=connection_string_message
)
@click.option("--log_level", default=None, help=cli_logger.log_level_message)
def data_source(project_name, name, connection_string, log_level):
    UncaughtExceptionHandler.wrap(
        _delete_data_source, project_name, name, connection_string, log_level
    )


def _delete_data_source(project_name, name, connection_string, log_level):
    logger = cli_logger.create_cli_logger(log_level)
    ar_client = cli_utils.get_artifact_repo_client(connection_string, logger)
    ds_client = cli_utils.get_data_service_client(connection_string, logger)

    with cl.ArtifactInteractionClient(ar_client, ds_client, logger) as client:
        client.delete_data_source(project_name, name)
        click.echo("Done")


@delete.command(context_settings=CLI_CONTEXT_SETTINGS)
@click.option("--id")
@click.option("--name", "-n")
@click.option(
    "--connection_string", default=None, help=connection_string_message
)
@click.option("--log_level", default=None, help=cli_logger.log_level_message)
def credential(id, name, connection_string, log_level):
    UncaughtExceptionHandler.wrap(
        _delete_credential, id, name, connection_string, log_level
    )


def _delete_credential(
    credential_id, credential_name, connection_string, log_level
):
    logger = cli_logger.create_cli_logger(log_level)
    ar_client = cli_utils.get_artifact_repo_client(connection_string, logger)
    ds_client = cli_utils.get_data_service_client(connection_string, logger)

    with cl.ArtifactInteractionClient(ar_client, ds_client, logger) as client:
        client.delete_credential(
            credential_id=credential_id, credential_name=credential_name
        )
        click.echo("Done")


@delete.command(
    help="Delete a schema by ID.",
    context_settings=CLI_CONTEXT_SETTINGS,
    hidden=cli_utils.feature_is_hidden("schema_apis")
)
@click.option("--schema_id")
@click.option(
    "--force",
    "-f",
    is_flag=True,
    help=
    "If set, will remove schema from all data collections using it. Use with caution."
)
@click.option(
    "--connection_string", default=None, help=connection_string_message
)
@click.option("--log_level", default=None, help=cli_logger.log_level_message)
def schema_by_id(schema_id, force, connection_string, log_level):
    UncaughtExceptionHandler.wrap(
        _delete_schema_by_id, schema_id, force, connection_string, log_level
    )


def _delete_schema_by_id(schema_id, force, connection_string, log_level):
    logger = cli_logger.create_cli_logger(log_level)
    ds_client = cli_utils.get_data_service_client(connection_string, logger)
    ds_client.delete_schema(schema_id, force=force)
    click.echo("Done")


@delete.command(
    help="Cleanup stale backups.", hidden=cli_utils.feature_is_hidden("admin")
)
@click.option(
    "--connection_string", default=None, help=connection_string_message
)
@click.option("--log_level", default=None, help=cli_logger.log_level_message)
def stale_backups(connection_string, log_level):
    UncaughtExceptionHandler.wrap(_clean_backup, connection_string, log_level)


def _clean_backup(connection_string, log_level):
    logger = cli_logger.create_cli_logger(log_level)
    backup_client = cli_utils.get_backup_client(connection_string, logger)
    response = backup_client.trigger_cleanup()
    output_dict = {
        "deleted_backups":
            [backup.backup_folder_path for backup in response.cleanup_backups]
    }
    click.echo(cli_utils._format_and_return_json(output_dict))


if __name__ == '__main__':
    delete()
