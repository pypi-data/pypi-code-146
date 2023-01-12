from typing import Any
from typing import Dict


def convert_raw_api_service_to_present(hub, api_service) -> Dict[str, Any]:
    if not api_service:
        return None

    result = {"resource_id": api_service.metadata.name}
    skip_attributes = [
        "api_version",
        "kind",
        "metadata.creation_timestamp",
        "metadata.generation",
        "metadata.managed_fields",
        "metadata.uid",
        "status",
    ]
    result.update(
        hub.tool.k8s.marshaller.marshal(
            k8s_object=api_service,
            skip_attributes=skip_attributes,
            skip_empty_values=True,
        )
    )
    return result
