# This is meant to hold experimental features - stuff that is provisional and allowed to break
# DO NOT import stuff from here globally. Always import it locally restricted to as smaller scope as possible
# Always guard the imports under servicefoundry.lib.util.is_experimental_env_set
import functools
from typing import Any, Dict, Sequence, Union

from servicefoundry.lib.clients.service_foundry_client import (
    ServiceFoundryServiceClient,
)
from servicefoundry.logger import logger


def _warn_on_call(fn):
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        logger.warning(
            f"Warning: This feature {fn.__name__} is in experimental stage. "
            f"As such there is no guarantees this will be maintained with backward compatibility "
            f"or even available moving forward"
        )
        return fn(*args, **kwargs)

    return wrapper


@_warn_on_call
def trigger_job(
    deployment_fqn: str, command: Union[str, Sequence[str]]
) -> Dict[str, Any]:
    client = ServiceFoundryServiceClient()
    deployment_info = client.get_deployment_info_by_fqn(deployment_fqn=deployment_fqn)
    deployment = client.get_deployment(
        application_id=deployment_info.applicationId,
        deployment_id=deployment_info.deploymentId,
    )
    application_info = client.get_application_info(
        application_id=deployment.applicationId
    )
    if deployment.version != application_info.activeVersion:
        raise Exception(
            f"The given `deployment_fqn` ({deployment_fqn!r}) belongs to an older version ({deployment.version}) "
            f"of the job. The latest active version is {application_info.activeVersion}. Triggering an older "
            f"version of the job is not supported. If you wish to run an older version, "
            f"you can redeploy the older version of the job first and then trigger that."
        )
    command_str = ""
    if command:
        if not isinstance(command, str):
            command_str = " ".join(command).strip()
        else:
            command_str = command.strip()
    command = command_str if command_str else None
    response = client._trigger_job(
        deployment_id=deployment_info.deploymentId,
        component_name=deployment.manifest["name"],
        command=command,
    )
    previous_runs_url = f"{client.base_url.strip('/')}/deployments/{deployment_info.applicationId}?tab=previousRuns"
    return {
        "status": response.get("message", "UNKNOWN"),
        "deployment_info": deployment_info,
        "previous_runs_url": previous_runs_url,
    }
