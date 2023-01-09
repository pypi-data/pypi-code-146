import logging

import rich_click as click

from servicefoundry.cli.config import CliConfig
from servicefoundry.cli.console import console
from servicefoundry.cli.const import (
    COMMAND_CLS,
    ENABLE_CLUSTER_COMMANDS,
    ENABLE_SECRETS_COMMANDS,
    GROUP_CLS,
)
from servicefoundry.cli.display_util import print_json, print_obj
from servicefoundry.cli.util import handle_exception_wrapper
from servicefoundry.lib.clients.service_foundry_client import (
    ServiceFoundryServiceClient,
)
from servicefoundry.lib.dao import workspace as workspace_lib
from servicefoundry.lib.model.entity import Cluster, Secret, SecretGroup, Workspace

logger = logging.getLogger(__name__)

# TODO (chiragjn): --json should disable all non json console prints


@click.group(name="get", cls=GROUP_CLS)
def get_command():
    # TODO (chiragjn): Figure out a way to update supported resources based on ENABLE_* flags
    """
    Get servicefoundry resources

    \b
    Supported resources:
    - Workspace
    - Service
    - Deployment
    """
    pass


@click.command(name="cluster", cls=COMMAND_CLS, help="Get Cluster metadata")
@click.argument("cluster_id")
@handle_exception_wrapper
def get_cluster(cluster_id):
    tfs_client = ServiceFoundryServiceClient()
    cluster = tfs_client.get_cluster(cluster_id)
    if CliConfig.get("json"):
        print_json(data=cluster)
    else:
        print_obj("Cluster", cluster, columns=Cluster.get_display_columns)


@click.command(name="workspace", cls=COMMAND_CLS, help="Get Workspace metadata")
@click.argument("name", type=click.STRING)
@click.option(
    "-c",
    "--cluster",
    type=click.STRING,
    default=None,
    help="cluster to find this workspace in",
)
@click.option("--non-interactive", is_flag=True, default=False)
@handle_exception_wrapper
def get_workspace(name, cluster, non_interactive):
    workspace = workspace_lib.get_workspace(
        name_or_id=name,
        cluster_name_or_id=cluster,
        non_interactive=non_interactive,
    )
    if CliConfig.get("json"):
        print_json(data=workspace.to_dict())
    else:
        print_obj(
            "Workspace", workspace.to_dict(), columns=Workspace.get_display_columns
        )


@click.command(name="secret-group", cls=COMMAND_CLS, help="Get Secret Group")
@click.argument("secret_group_id")
@handle_exception_wrapper
def get_secret_group(secret_group_id):
    tfs_client = ServiceFoundryServiceClient()
    response = tfs_client.get_secret_group(secret_group_id)
    print_obj(f"Secret Group", response, columns=SecretGroup.get_display_columns)


@click.command(name="secret", cls=COMMAND_CLS, help="Get Secret")
@click.argument("secret_id")
@handle_exception_wrapper
def get_secret(secret_id):
    tfs_client = ServiceFoundryServiceClient()
    response = tfs_client.get_secret(secret_id)
    print_obj(response["id"], response, columns=Secret.get_display_columns)


@click.command(name="config", cls=COMMAND_CLS, help="Get current config (defaults)")
@handle_exception_wrapper
def get_current_context():
    tfs_client = ServiceFoundryServiceClient()
    cluster = tfs_client.session.get_cluster()
    workspace = tfs_client.session.get_workspace()
    console.print(f"API Server: {tfs_client.session.profile.server_config.api_server}")
    if workspace:
        console.print(f"Workspace: {workspace['name']} ({cluster['id']})")
    else:
        console.print(
            f"No workspace set as default. "
            f"Please use `sfy use workspace` to pick a default workspace"
        )


def get_get_command():
    get_command.add_command(get_workspace)
    get_command.add_command(get_current_context)
    # get_command.add_command(get_logs)

    if ENABLE_CLUSTER_COMMANDS:
        get_command.add_command(get_cluster)

    if ENABLE_SECRETS_COMMANDS:
        get_command.add_command(get_secret)
        get_command.add_command(get_secret_group)

    return get_command
