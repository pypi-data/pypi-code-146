from typing import Any
from typing import Dict


def convert_raw_service_to_present(hub, service) -> Dict[str, Any]:
    if not service:
        return None

    result = {"resource_id": service.metadata.name}
    skip_attributes = [
        "api_version",
        "kind",
        "metadata.creation_timestamp",
        "metadata.generation",
        "metadata.managed_fields",
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
            k8s_object=service,
            skip_attributes=skip_attributes,
            skip_empty_values=True,
        )
    )
    return result
