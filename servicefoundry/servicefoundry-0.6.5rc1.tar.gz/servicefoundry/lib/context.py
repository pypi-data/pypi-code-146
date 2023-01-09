# TODO: rename this file to config.py

from typing import Optional

from servicefoundry.cli.console import console
from servicefoundry.lib.clients.service_foundry_client import (
    ServiceFoundryServiceClient,
)
from servicefoundry.lib.messages import (
    PROMPT_SETTING_CLUSTER_CONTEXT,
    PROMPT_SETTING_WORKSPACE_CONTEXT,
)
from servicefoundry.lib.model.entity import Cluster, Workspace
from servicefoundry.lib.util import resolve_cluster_or_error, resolve_workspace_or_error


def use_cluster(
    name_or_id: Optional[str] = None,
    non_interactive: bool = True,
    client: Optional[ServiceFoundryServiceClient] = None,
) -> Cluster:
    client = client or ServiceFoundryServiceClient()
    cluster = resolve_cluster_or_error(
        name_or_id=name_or_id,
        non_interactive=non_interactive,
        ignore_context=True,
        client=client,
    )
    client.session.set_cluster(cluster.to_dict_for_session())
    console.print(PROMPT_SETTING_CLUSTER_CONTEXT.format(cluster.name))
    client.session.save_session()
    return cluster


def use_workspace(
    name_or_id: Optional[str] = None,
    cluster_name_or_id: Optional[str] = None,
    non_interactive: bool = True,
    client: Optional[ServiceFoundryServiceClient] = None,
) -> Workspace:
    client = client or ServiceFoundryServiceClient()
    if non_interactive:
        if not name_or_id:
            raise ValueError("workspace name or id cannot be null")

    cluster = resolve_cluster_or_error(
        name_or_id=cluster_name_or_id,
        ignore_context=False,
        non_interactive=non_interactive,
        client=client,
    )

    workspace, cluster = resolve_workspace_or_error(
        name_or_id=name_or_id,
        cluster_name_or_id=cluster,
        ignore_context=True,
        non_interactive=non_interactive,
        client=client,
    )
    client.session.set_workspace(workspace.to_dict_for_session())
    console.print(PROMPT_SETTING_WORKSPACE_CONTEXT.format(workspace.name))
    client.session.set_cluster(cluster.to_dict_for_session())
    console.print(PROMPT_SETTING_CLUSTER_CONTEXT.format(cluster.name))
    client.session.save_session()
    return workspace


def clear_context(
    non_interactive: bool = True,
    client: Optional[ServiceFoundryServiceClient] = None,
):
    client = client or ServiceFoundryServiceClient()
    client.session.set_cluster(None)
    client.session.set_workspace(None)
    client.session.save_session()
