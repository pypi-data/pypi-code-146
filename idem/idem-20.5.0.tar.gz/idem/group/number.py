from typing import Any
from typing import Dict


def apply(hub, data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Sort the data by run number
    """
    result = {}
    for tag in sorted(data, key=lambda k: data[k].get("__run_num", 0)):
        result[tag] = data[tag]

    return result
