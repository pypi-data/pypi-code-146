from typing import Any
from typing import Dict


def sig_apply(hub, data: Dict[str, Any]) -> Dict[str, Any]:
    """
    ret = {}
    for tag in data:
        state_ret = data[tag]
        comps = tag.split("_|-")
        state = comps[0]
        id_ = comps[1]
        fun = comps[3]
        result = state_ret.get("result")
        comment = state_ret.get("comment")
        changes = state_ret.get("changes", {})
        old_state = state_ret.get("old_state", {})
        new_state = state_ret.get("new_state", {})

        ret[tag] = data[tag]
    return ret
    """
