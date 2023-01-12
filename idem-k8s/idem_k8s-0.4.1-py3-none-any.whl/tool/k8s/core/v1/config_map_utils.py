from typing import Any
from typing import Dict


def convert_raw_config_map_to_present(hub, config_map) -> Dict[str, Any]:
    if not config_map:
        return None

    result = {"resource_id": config_map.metadata.name}
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
            k8s_object=config_map,
            skip_attributes=skip_attributes,
            skip_empty_values=True,
        )
    )

    if result.get("immutable") is None:
        result["immutable"] = False

    return result
