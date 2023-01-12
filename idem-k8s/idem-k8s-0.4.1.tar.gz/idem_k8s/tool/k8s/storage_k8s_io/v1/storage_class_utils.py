from typing import Any
from typing import Dict


def convert_raw_storage_class_to_present(hub, storage_class) -> Dict[str, Any]:
    if not storage_class:
        return None

    result = {"resource_id": storage_class.metadata.name}
    skip_attributes = [
        "api_version",
        "kind",
        "metadata.annotations",
        "metadata.creation_timestamp",
        "metadata.generation",
        "metadata.managed_fields",
        "metadata.resource_version",
        "metadata.uid",
        "metadata.self_link",
    ]
    result.update(
        hub.tool.k8s.marshaller.marshal(
            k8s_object=storage_class,
            skip_attributes=skip_attributes,
            skip_empty_values=True,
        )
    )

    if result.get("allow_volume_expansion") is None:
        result["allow_volume_expansion"] = False

    return result
