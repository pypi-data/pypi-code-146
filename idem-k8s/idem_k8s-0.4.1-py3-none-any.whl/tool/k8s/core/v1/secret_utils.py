from typing import Any
from typing import Dict


def convert_raw_secret_to_present(hub, secret) -> Dict[str, Any]:
    if not secret:
        return None

    result = {"resource_id": secret.metadata.name}
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
            k8s_object=secret,
            skip_attributes=skip_attributes,
            skip_empty_values=True,
        )
    )

    if result.get("immutable") is None:
        result["immutable"] = False

    return result
