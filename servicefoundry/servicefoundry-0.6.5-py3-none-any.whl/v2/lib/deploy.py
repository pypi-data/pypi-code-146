import time
from typing import List, TypeVar

from pydantic import BaseModel
from rich.status import Status

from servicefoundry.auto_gen import models as auto_gen_models
from servicefoundry.lib.clients.service_foundry_client import (
    ServiceFoundryServiceClient,
)
from servicefoundry.lib.clients.utils import poll_for_function
from servicefoundry.lib.dao.workspace import get_workspace_by_fqn
from servicefoundry.lib.model.entity import Deployment, DeploymentTransitionStatus
from servicefoundry.logger import logger
from servicefoundry.v2.lib.models import BuildResponse
from servicefoundry.v2.lib.source import (
    local_source_to_image,
    local_source_to_remote_source,
)

Component = TypeVar("Component", bound=BaseModel)


def _handle_if_local_source(component: Component, workspace_fqn: str) -> Component:
    if (
        hasattr(component, "image")
        and isinstance(component.image, auto_gen_models.Build)
        and isinstance(component.image.build_source, auto_gen_models.LocalSource)
    ):
        new_component = component.copy(deep=True)
        if component.image.build_source.local_build:
            # We are to build the image locally, push and update `image` in spec
            logger.info("Building image for %s '%s'", component.type, component.name)
            new_component.image = local_source_to_image(
                build=component.image,
                docker_registry_fqn=component.image.docker_registry,
                workspace_fqn=workspace_fqn,
                component_name=component.name,
            )
        else:
            # We'll build image on Truefoundry servers, upload the source and update image.build_source
            logger.info("Uploading code for %s '%s'", component.type, component.name)
            new_component.image.build_source = local_source_to_remote_source(
                local_source=component.image.build_source,
                workspace_fqn=workspace_fqn,
                component_name=component.name,
            )
            logger.debug("Uploaded code for %s '%s'", component.type, component.name)
        return new_component
    return component


def _log_hosts_for_services(deployment: Deployment):
    base_domain_url = deployment.baseDomainURL
    workspace_name = deployment.workspace.get("name", "")

    component_name = deployment.manifest.get("name", "")
    component_type = deployment.manifest.get("type", "")

    if component_type != "service":
        return

    if not component_name:
        logger.debug("Cannot print service host as component name is empty")
        return

    url = f"https://{component_name}-{workspace_name}.{base_domain_url}"
    logger.info(
        "Service '%s' will be available at\n'%s'\nafter successful deployment",
        component_name,
        url,
    )


def _log_application_dashboard_url(deployment: Deployment, log_message: str):
    application_id = deployment.applicationId

    # TODO: is there any simpler way to get this? :cry
    client = ServiceFoundryServiceClient()

    url = f"{client.base_url.strip('/')}/applications/{application_id}?tab=deployments"
    logger.info(log_message, url)


def _tail_build_logs(build_responses: List[BuildResponse]) -> None:
    client = ServiceFoundryServiceClient()

    # TODO: Explore other options like,
    # https://rich.readthedocs.io/en/stable/live.html#live-display
    # How does docker/compose does multiple build logs?
    for build_response in build_responses:
        logger.info("Tailing build logs for '%s'", build_response.componentName)
        client.tail_build_logs(build_response=build_response, wait=True)


def _deploy_wait_handler(deployment: Deployment):
    _log_application_dashboard_url(
        deployment=deployment,
        log_message=(
            "You can track the progress below or on the dashboard:- '%s'\n"
            "You can press Ctrl + C to exit the tailing of build logs "
            "and deployment will continue on the server"
        ),
    )
    with Status(status="Polling for deployment status") as spinner:
        last_status_printed = None
        client = ServiceFoundryServiceClient()
        start_time = time.monotonic()
        total_timeout_time: int = 300
        poll_interval_seconds = 5
        time_elapsed = 0

        for deployment_statuses in poll_for_function(
            client.get_deployment_statuses,
            poll_after_secs=poll_interval_seconds,
            application_id=deployment.applicationId,
            deployment_id=deployment.id,
        ):
            if len(deployment_statuses) == 0:
                logger.warning("Did not receive any deployment status")
                continue

            latest_deployment_status = deployment_statuses[-1]

            status_to_print = (
                latest_deployment_status.transition or latest_deployment_status.status
            )
            spinner.update(status=f"Current state: {status_to_print}")
            if status_to_print != last_status_printed:
                if DeploymentTransitionStatus.is_failure_state(status_to_print):
                    logger.error("State: %r", status_to_print)
                else:
                    logger.info("State: %r", status_to_print)
                last_status_printed = status_to_print

            if latest_deployment_status.state.isTerminalState:
                break

            if (
                latest_deployment_status.transition
                == DeploymentTransitionStatus.BUILDING
            ):
                build_responses = client.get_deployment_build_response(
                    application_id=deployment.applicationId, deployment_id=deployment.id
                )
                _tail_build_logs(build_responses)

            time_elapsed = time.monotonic() - start_time
            if time_elapsed > total_timeout_time:
                logger.warning("Polled server for %s secs.", int(time_elapsed))
                break


def deploy_component(
    component: Component, workspace_fqn: str, wait: bool = True
) -> Deployment:
    workspace_id = get_workspace_by_fqn(workspace_fqn).id
    updated_component = _handle_if_local_source(
        component=component, workspace_fqn=workspace_fqn
    )

    client = ServiceFoundryServiceClient()
    response = client.deploy_application(
        workspace_id=workspace_id, application=updated_component
    )
    logger.info(
        "🚀 Deployment started for application '%s'. Deployment FQN is '%s'.",
        updated_component.name,
        response.fqn,
    )
    if wait:
        try:
            _deploy_wait_handler(deployment=response)
        except KeyboardInterrupt:
            logger.info("Ctrl-c executed. The deployment will still continue.")
    _log_application_dashboard_url(
        deployment=response,
        log_message="You can find the application on the dashboard:- '%s'",
    )
    return response
