from typing import Any
from typing import Dict


def convert_raw_namespace_to_present(hub, namespace) -> Dict[str, Any]:
    if not namespace:
        return None

    result = {"resource_id": namespace.metadata.name}
    skip_attributes = [
        "api_version",
        "kind",
        "spec",
        "metadata.creation_timestamp",
        "metadata.managed_fields",
        "metadata.resource_version",
        "metadata.uid",
        "status",
    ]
    result.update(
        hub.tool.k8s.marshaller.marshal(
            k8s_object=namespace,
            skip_attributes=skip_attributes,
            skip_empty_values=True,
        )
    )
    return result
