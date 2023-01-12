from typing import Any
from typing import Dict


def convert_raw_persistent_volume_claim_to_present(
    hub, persistent_volume_claim
) -> Dict[str, Any]:
    if not persistent_volume_claim:
        return None

    result = {"resource_id": persistent_volume_claim.metadata.name}
    skip_attributes = [
        "api_version",
        "kind",
        "metadata.creation_timestamp",
        "metadata.generation",
        "metadata.managed_fields",
        "metadata.resource_version",
        "metadata.uid",
        "status",
    ]
    result.update(
        hub.tool.k8s.marshaller.marshal(
            k8s_object=persistent_volume_claim,
            skip_attributes=skip_attributes,
            skip_empty_values=True,
        )
    )
    return result
