from typing import Any
from typing import Dict


def convert_raw_cluster_role_binding_to_present(
    hub, cluster_role_binding
) -> Dict[str, Any]:
    if not cluster_role_binding:
        return None

    result = {"resource_id": cluster_role_binding.metadata.name}
    skip_attributes = [
        "api_version",
        "kind",
        "metadata.creation_timestamp",
        "metadata.managed_fields",
        "metadata.resource_version",
        "metadata.uid",
    ]
    result.update(
        hub.tool.k8s.marshaller.marshal(
            k8s_object=cluster_role_binding,
            skip_attributes=skip_attributes,
            skip_empty_values=True,
        )
    )
    return result
