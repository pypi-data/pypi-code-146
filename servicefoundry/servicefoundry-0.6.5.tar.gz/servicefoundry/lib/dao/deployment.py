from typing import Optional

from servicefoundry.cli.console import console
from servicefoundry.lib.clients.service_foundry_client import (
    ServiceFoundryServiceClient,
)
from servicefoundry.lib.messages import PROMPT_USING_WORKSPACE_CONTEXT
from servicefoundry.lib.model.entity import NewDeployment


def list_deployments(
    workspace_fqn: Optional[str] = None,
    client: Optional[ServiceFoundryServiceClient] = None,
):
    # NOTES: this is horrible, needs refactoring
    from servicefoundry.lib.dao.workspace import get_workspace_by_fqn

    client = client or ServiceFoundryServiceClient()
    if not workspace_fqn:
        deployments = client.list_deployments()
    else:
        workspace = get_workspace_by_fqn(workspace_fqn)
        console.print(PROMPT_USING_WORKSPACE_CONTEXT.format(workspace.name))
        deployments = client.list_deployments(workspace.id)
    deployments = [NewDeployment.from_dict(d) for d in deployments]
    return deployments
