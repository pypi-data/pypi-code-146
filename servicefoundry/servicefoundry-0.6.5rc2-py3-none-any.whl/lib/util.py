import os
from typing import List, Optional, Tuple, TypeVar, Union

import questionary

from servicefoundry.cli.console import console
from servicefoundry.lib.clients.service_foundry_client import (
    ServiceFoundryServiceClient,
)
from servicefoundry.lib.const import (
    SFY_DEBUG_ENV_KEY,
    SFY_EXPERIMENTAL_ENV_KEY,
    SFY_INTERNAL_ENV_KEY,
)
from servicefoundry.lib.messages import PROMPT_USING_CLUSTER_CONTEXT
from servicefoundry.lib.model.entity import Cluster, Workspace

# TODO: Move type casting downwards into `ServiceFoundrySession` and `ServiceFoundryServiceClient`
# TODO: Abstract duplicated code across resolving different entities
T = TypeVar("T")


def is_debug_env_set() -> bool:
    return True if os.getenv(SFY_DEBUG_ENV_KEY) else False


def is_experimental_env_set() -> bool:
    # TODO (chiragjn): one of these need to be removed
    return (
        True
        if os.getenv(SFY_EXPERIMENTAL_ENV_KEY) or os.getenv(SFY_INTERNAL_ENV_KEY)
        else False
    )


def _filter_by_attr_match(
    instances: List[T],
    value: Optional[str],
    attrs: Tuple[str, ...] = ("name", "fqn", "id"),
) -> List[T]:
    found = instances
    if value:
        for attr in attrs:
            found = [i for i in instances if getattr(i, attr, None) == value]
            if found:
                break
    return found


def all_clusters(client: ServiceFoundryServiceClient) -> List[Cluster]:
    clusters = [Cluster.from_dict(c) for c in client.list_cluster()]
    return clusters


def all_workspaces(client: ServiceFoundryServiceClient) -> List[Workspace]:
    workspaces = [Workspace.from_dict(w) for w in client.list_workspace()]
    return workspaces


def get_cluster_from_context(client: ServiceFoundryServiceClient) -> Optional[Cluster]:
    cluster = client.session.get_cluster()
    if cluster:
        cluster = Cluster.from_dict(cluster)
    return cluster


def get_workspace_from_context(
    client: ServiceFoundryServiceClient,
) -> Optional[Workspace]:
    workspace = client.session.get_workspace()
    if workspace:
        workspace = Workspace.from_dict(workspace)
    return workspace


def resolve_clusters(
    client: ServiceFoundryServiceClient,
    name_or_id: Optional[str] = None,
    ignore_context: bool = False,
) -> List[Cluster]:
    if not ignore_context and not name_or_id:
        cluster = get_cluster_from_context(client=client)
        if cluster:
            return [cluster]

    clusters = all_clusters(client=client)
    return _filter_by_attr_match(
        instances=clusters, value=name_or_id, attrs=("name", "fqn", "id")
    )


def resolve_workspaces(
    client: ServiceFoundryServiceClient,
    name_or_id: Optional[str] = None,
    cluster_name_or_id: Optional[Union[Cluster, str]] = None,
    ignore_context: bool = False,
) -> List[Workspace]:
    if not ignore_context and not name_or_id:
        workspace = get_workspace_from_context(client=client)
        if workspace:
            return [workspace]

    if isinstance(cluster_name_or_id, Cluster):
        clusters = [cluster_name_or_id]
        cluster_name_or_id = clusters[0].id
    else:
        clusters = resolve_clusters(
            client=client, name_or_id=cluster_name_or_id, ignore_context=ignore_context
        )

    if not clusters:
        if cluster_name_or_id:
            raise ValueError(f"No cluster found with name or id {cluster_name_or_id!r}")
        else:
            raise ValueError("Unable to resolve clusters without a name or id")
    elif len(clusters) == 1:
        cluster = clusters[0]
        _workspaces = client.get_workspace_by_name(
            workspace_name="", cluster_id=cluster.id
        )
        workspaces = [Workspace.from_dict(w) for w in _workspaces]
    else:
        if cluster_name_or_id:
            raise ValueError(
                f"More than one cluster found with name or id {cluster_name_or_id!r}: {clusters!r}"
            )
        else:
            # TODO (chiragjn): optimize this, we have wasted a call to v1/cluster
            workspaces = all_workspaces(client=client)

    return _filter_by_attr_match(
        instances=workspaces, value=name_or_id, attrs=("name", "fqn", "id")
    )


def ask_pick_cluster(clusters: List[Cluster]) -> Cluster:
    choices = [
        questionary.Choice(title=f"{c.name} ({c.fqn})", value=c) for c in clusters
    ]
    return questionary.select("Pick a cluster", choices=choices).ask()


def maybe_ask_pick_cluster(clusters: List[Cluster]) -> Cluster:
    if len(clusters) == 1:
        return clusters[0]
    return ask_pick_cluster(clusters=clusters)


def ask_pick_workspace(workspaces: List[Workspace]) -> Workspace:
    choices = [
        questionary.Choice(title=f"{w.name} ({w.fqn})", value=w) for w in workspaces
    ]
    return questionary.select("Pick a workspace", choices=choices).ask()


def maybe_ask_pick_workspace(workspaces: List[Workspace]) -> Workspace:
    if len(workspaces) == 1:
        return workspaces[0]
    return ask_pick_workspace(workspaces=workspaces)


def resolve_cluster_or_error(
    name_or_id: Optional[str] = None,
    ignore_context: bool = False,
    non_interactive: bool = True,
    client: Optional[ServiceFoundryServiceClient] = None,
) -> Cluster:
    if non_interactive:
        if ignore_context and not name_or_id:
            raise ValueError("cluster name or id cannot be null")

    clusters = resolve_clusters(
        client=client, name_or_id=name_or_id, ignore_context=ignore_context
    )

    if not clusters:
        if name_or_id:
            raise ValueError(f"No cluster found with name or id {name_or_id!r}")
        else:
            raise ValueError(f"No clusters found!")
    else:
        if non_interactive:
            if len(clusters) > 1:
                raise ValueError(
                    f"More than one cluster found with name or id {name_or_id!r}: {clusters!r}"
                )
            else:
                cluster = clusters[0]
        else:
            cluster = maybe_ask_pick_cluster(clusters=clusters)
    return cluster


def resolve_workspace_or_error(
    name_or_id: Optional[str] = None,
    cluster_name_or_id: Optional[Union[Cluster, str]] = None,
    ignore_context: bool = False,
    non_interactive: bool = True,
    client: Optional[ServiceFoundryServiceClient] = None,
) -> Tuple[Workspace, Cluster]:
    if non_interactive:
        if ignore_context and not name_or_id:
            raise ValueError("workspace name or id cannot be null")

    if isinstance(cluster_name_or_id, Cluster):
        cluster = cluster_name_or_id
    else:
        cluster = resolve_cluster_or_error(
            name_or_id=cluster_name_or_id,
            non_interactive=non_interactive,
            ignore_context=ignore_context,
            client=client,
        )

    console.print(PROMPT_USING_CLUSTER_CONTEXT.format(cluster.name))

    workspaces = resolve_workspaces(
        client=client,
        name_or_id=name_or_id,
        cluster_name_or_id=cluster,
        ignore_context=ignore_context,
    )
    if not workspaces:
        if name_or_id:
            raise ValueError(
                f"No workspace found with name or id {name_or_id!r} in cluster {cluster.name!r}"
            )
        else:
            raise ValueError(f"No workspaces found!")
    else:
        if non_interactive:
            if len(workspaces) > 1:
                raise ValueError(
                    f"More than one workspace found with name or id {name_or_id!r}: {workspaces!r}"
                )
            else:
                workspace = workspaces[0]
        else:
            workspace = maybe_ask_pick_workspace(workspaces=workspaces)
    return workspace, cluster
