import click

import truera.client.cli.cli_logger as cli_logger
from truera.client.cli.cli_utils import CLI_CONTEXT_SETTINGS
import truera.client.cli.cli_utils as cli_utils
from truera.client.cli.UncaughtExceptionHandler import UncaughtExceptionHandler
from truera.client.client_environment import connection_string_message
import truera.client.services.artifact_interaction_client as cl


@click.group(help="Commands for adding credentials.")
def credential():
    pass


@credential.command(
    context_settings=CLI_CONTEXT_SETTINGS,
    help="""
Add a secret to the specified project which can be used to attach to data sources.
The following are required for data source types:
    MYSQL db   - username / password in identity and secret respectively.
    JDBC db    - username / password in identity and secret respectively.
    S3 Bucket  - Access key id and secret access key in identity and secret respectively.
    WASB blobs - Secret only containing the storage account key."""
)
@click.option(
    "--project_name",
    "-p",
    help=
    "Id of the project the data source resides in, and split should be created in.",
    required=True
)
@click.option(
    "--credential_name",
    required=True,
    help="Name of the external data credential."
)
@click.option(
    "--identity",
    help="Identity portion of the secret. Not needed in all cases."
)
@click.option("--secret", required=True, help="Secret value.")
@click.option(
    "--connection_string", default=None, help=connection_string_message
)
@click.option("--log_level", default=None, help=cli_logger.log_level_message)
def data_source(
    project_name, credential_name, identity, secret, connection_string,
    log_level
):
    UncaughtExceptionHandler.wrap(
        _add_data_source_credential, project_name, credential_name, identity,
        secret, connection_string, log_level
    )


def _add_data_source_credential(
    project_name, credential_name, identity, secret, connection_string,
    log_level
):
    logger = cli_logger.create_cli_logger(log_level)
    ar_client = cli_utils.get_artifact_repo_client(connection_string, logger)
    ds_client = cli_utils.get_data_service_client(connection_string, logger)

    with cl.ArtifactInteractionClient(ar_client, ds_client, logger) as client:
        project_id = client.get_project_id(project_name)

        cred_id = client.add_data_source_cred(
            project_id, credential_name, identity, secret
        )
        output_dict = {
            "project_name": project_name,
            "credential_name": credential_name,
            "credential_id": cred_id
        }
        click.echo(cli_utils._format_and_return_json(output_dict))
