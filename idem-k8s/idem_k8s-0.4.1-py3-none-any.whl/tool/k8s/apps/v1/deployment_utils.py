from typing import Any
from typing import Dict


def convert_raw_deployment_to_present(hub, deployment) -> Dict[str, Any]:
    if not deployment:
        return None

    result = {"resource_id": deployment.metadata.name}
    skip_attributes = [
        "api_version",
        "kind",
        "metadata.annotations.deployment.kubernetes.io/revision",
        "metadata.creation_timestamp",
        "metadata.generation",
        "metadata.managed_fields",
        "metadata.resource_version",
        "metadata.uid",
        "spec.progress_deadline_seconds",
        "spec.revision_history_limit",
        "spec.template.spec.dns_policy",
        "spec.template.spec.scheduler_name",
        "spec.template.spec.termination_grace_period_seconds",
        "status",
    ]
    result.update(
        hub.tool.k8s.marshaller.marshal(
            k8s_object=deployment,
            skip_attributes=skip_attributes,
            skip_empty_values=True,
        )
    )

    if result["spec"].get("template"):
        pod_template = result["spec"].get("template")
        if pod_template["spec"]["containers"][0].get("security_context"):
            security_context = pod_template["spec"]["containers"][0].get(
                "security_context"
            )
            if not security_context.get("allow_privilege_escalation"):
                security_context["allow_privilege_escalation"] = False

    if result["spec"].get("strategy"):
        strategy = result["spec"].get("strategy")
        if strategy.get("rolling_update"):
            rolling_update = strategy.get("rolling_update")
            if not rolling_update.get("max_unavailable"):
                rolling_update["max_unavailable"] = 0
            if not rolling_update.get("max_surge"):
                rolling_update["max_surge"] = 0

    return result


def handle_default_values(hub, desired_state) -> Dict[str, Any]:
    if desired_state["spec"].get("strategy") is None:
        strategy = {
            "type": "RollingUpdate",
            "rolling_update": {"max_surge": "25%", "max_unavailable": "25%"},
        }
        desired_state["spec"]["strategy"] = strategy
    if desired_state["spec"].get("template"):
        pod_template = desired_state["spec"].get("template")
        if pod_template["spec"].get("restart_policy") is None:
            pod_template["spec"]["restart_policy"] = "Always"

        pod_containers = desired_state["spec"]["template"]["spec"].get("containers")
        for container in pod_containers:
            if container.get("image_pull_policy") is None:
                image = container.get("image")
                container["image_pull_policy"] = (
                    "Always" if ":latest" in image else "IfNotPresent"
                )

            if container.get("termination_message_policy") is None:
                container["termination_message_policy"] = "File"

            if container.get("termination_message_path") is None:
                container["termination_message_path"] = "/dev/termination-log"

    return desired_state
