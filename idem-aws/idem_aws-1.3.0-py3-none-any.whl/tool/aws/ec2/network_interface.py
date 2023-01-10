from typing import Any
from typing import Dict


def convert_to_present(
    hub, ctx, describe_network_interfaces: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Convert the Network Interface to present
    """
    result = {}

    for network_interface in describe_network_interfaces.get("NetworkInterfaces", ()):
        resource_id = network_interface.get("NetworkInterfaceId")

        result[resource_id] = dict(
            name=resource_id,
            resource_id=resource_id,
            attachment_id=network_interface.get("Attachment", {}).get("AttachmentId"),
        )

    return result
