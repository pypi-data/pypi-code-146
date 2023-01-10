from typing import Any
from typing import Dict


def apply(hub, data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Reorganize the data by sorting by each state's unique tag
    """
    result = {}
    for tag in sorted(data.keys()):
        result[tag] = data[tag]
    return result
