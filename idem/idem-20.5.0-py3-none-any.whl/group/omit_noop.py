from typing import Any
from typing import Dict

NOOP_TAG = "omit_noop_|-noop_count_|-_|-apply"


def apply(hub, data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Remove states that reported success without changes
    """
    ret = {}

    noop_count = 0

    for tag in data:
        state_ret = data[tag]
        result = state_ret.get("result")
        changes = state_ret.get("changes", {})

        if result and not changes:
            # If the state was successful but there were no changes, it's a no-op

            # Keep count of no-ops in a new key
            if NOOP_TAG not in ret:
                ret[NOOP_TAG] = {"count": 0, "result": True, "comment": ""}

            noop_count += 1
        else:
            # There were changes or a failure, keep it in the results
            ret[tag] = data[tag]

    if NOOP_TAG in ret:
        # Add a comment that supplies a total of passed no-op states
        ret[NOOP_TAG]["comment"] = f"Total no-op states: {noop_count}"

    return ret
