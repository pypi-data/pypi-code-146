from typing import Any
from typing import Dict


def apply(hub, data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Apply all group plugins specified in config
    """
    # Read groups from the config
    groups = hub.OPT.get("idem", {}).get("group")

    if not groups:
        return data

    # Run each of the group plugins from config, separated by a pipe
    for group_plugin in groups.split("|"):
        if group_plugin == "init":
            continue
        if group_plugin not in hub.group:
            hub.log.error(f"No group plugin '{group_plugin}'")
            continue
        data = hub.group[group_plugin].apply(data)

    return data
