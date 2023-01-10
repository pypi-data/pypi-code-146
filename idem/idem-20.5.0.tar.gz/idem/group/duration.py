from typing import Any
from typing import Dict


def apply(hub, data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Sort the output by the total seconds of the state's run time
    """
    ret = {}
    for tag in sorted(data, key=lambda k: data[k].get("total_seconds", 0)):
        ret[tag] = data[tag]
    return ret
