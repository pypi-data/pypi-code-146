from typing import Any
from typing import Dict


def convert_raw_daemon_set_to_present(hub, daemon_set) -> Dict[str, Any]:
    if not daemon_set:
        return None

    result = {"resource_id": daemon_set.metadata.name}
    skip_attributes = [
        "api_version",
        "kind",
        "metadata.annotations",
        "metadata.creation_timestamp",
        "metadata.generation",
        "metadata.managed_fields",
        "metadata.resource_version",
        "metadata.uid",
        "spec.revision_history_limit",
        "spec.template.spec.dns_policy",
        "spec.template.spec.scheduler_name",
        "spec.template.spec.termination_grace_period_seconds",
        "status",
    ]
    result.update(
        hub.tool.k8s.marshaller.marshal(
            k8s_object=daemon_set,
            skip_attributes=skip_attributes,
            skip_empty_values=True,
        )
    )
    return result
