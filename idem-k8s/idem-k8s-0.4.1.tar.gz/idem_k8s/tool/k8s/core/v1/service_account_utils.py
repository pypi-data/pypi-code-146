from typing import Any
from typing import Dict


def convert_raw_service_account_to_present(hub, service_account) -> Dict[str, Any]:
    if not service_account:
        return None

    result = {"resource_id": service_account.metadata.name}
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
            k8s_object=service_account,
            skip_attributes=skip_attributes,
            skip_empty_values=True,
        )
    )

    if not result.get("automount_service_account_token"):
        result["automount_service_account_token"] = False

    return result
