from typing import Any
from typing import Dict


def convert_raw_cluster_role_to_present(hub, cluster_role) -> Dict[str, Any]:
    if not cluster_role:
        return None

    result = {"resource_id": cluster_role.metadata.name}
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
            k8s_object=cluster_role,
            skip_attributes=skip_attributes,
            skip_empty_values=True,
            include_empty_string_keys=["api_groups"],
        )
    )
    return result
