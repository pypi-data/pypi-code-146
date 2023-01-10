# NOTES
# This is a VERY simple outputter for idem, it does not do everything the
# Salt highstate outputter does, and nor should it! This outputter should
# not become hyper complicated, things like terse should be another
# outputter, this should really just get things like errors added
from typing import Dict

try:
    import colorama

    HAS_LIBS = (True,)
except ImportError as e:
    HAS_LIBS = False, str(e)


def __virtual__(hub):
    return HAS_LIBS


def display(hub, data):
    """
    Display the data from an idem run
    """
    if not isinstance(data, dict):
        return hub.output.nested.display(data)

    endc = colorama.Fore.RESET
    strs = []
    fun_count = {}
    for tag in data:
        ret = data[tag]
        comps = tag.split("_|-")
        state = comps[0]
        id_ = comps[1]
        fun = comps[3]
        result = ret.get("result")
        comment = ret.get("comment", [])

        # when the current chunk's execution is halted due to recreation flow, we can skip that output from display.
        if comment and "will be recreated" in comment:
            hub.log.debug(
                f"The output of state {id_} will be skipped from display, as it just states that resource will be recreated."
            )
            continue

        changes = hub.output.nested.display(ret.get("changes", {}))
        if result is True and changes:
            tcolor = colorama.Fore.CYAN
        elif result is True:
            tcolor = colorama.Fore.GREEN
        elif result is None:
            tcolor = colorama.Fore.LIGHTYELLOW_EX
        elif result is False:
            tcolor = colorama.Fore.LIGHTRED_EX
        else:
            tcolor = colorama.Fore.RESET

        strs.append(f"{tcolor}--------{endc}")
        strs.append(f"{tcolor}      ID: {id_}{endc}")
        strs.append(f"{tcolor}Function: {state}.{fun}{endc}")
        strs.append(f"{tcolor}  Result: {result}{endc}")
        strs.append(f"{tcolor} Comment: {comment}{endc}")
        strs.append(f"{tcolor} Changes:\n{changes}{endc}")

        # Calculate counts for each function and result
        _increment_count(fun_count, fun, result)

        # Get granularity for successful result
        if result:
            if not ret.get("old_state"):
                _increment_count(fun_count, fun, "no_old_state")
            elif ret["changes"]:
                _increment_count(fun_count, fun, "with_changes")

    strs = strs + _format_fun_counts(fun_count)
    return "\n".join(strs)


def _format_fun_counts(fun_map: Dict[str, Dict[str, int]]) -> []:
    # Format counts for each function
    # Sample output:
    #  present: 1 successful
    #  present: 2 failed
    strs = ["\n"]

    for fun, result_and_count in fun_map.items():
        if result_and_count.get(True, 0) > 0:
            if fun == "present":
                if result_and_count.get("no_old_state", 0) > 0:
                    strs.append(
                        f"{fun}: {result_and_count['no_old_state']} created successfully"
                    )
                if result_and_count.get("with_changes", 0) > 0:
                    strs.append(
                        f"{fun}: {result_and_count['with_changes']} updated successfully"
                    )
                no_op_count = (
                    result_and_count[True]
                    - result_and_count.get("no_old_state", 0)
                    - result_and_count.get("with_changes", 0)
                )
                if no_op_count > 0:
                    strs.append(f"{fun}: {no_op_count} no-op")

            elif fun == "absent":
                if result_and_count.get("no_old_state", 0) > 0:
                    strs.append(f"{fun}: {result_and_count['no_old_state']} no-op")
                deletion_count = result_and_count[True] - result_and_count.get(
                    "no_old_state", 0
                )
                if deletion_count > 0:
                    strs.append(f"{fun}: {deletion_count} deleted successfully")

            else:
                strs.append(f"{fun}: {result_and_count[True]} successful")

        if result_and_count.get(False, 0) > 0:
            strs.append(f"{fun}: {result_and_count[False]} failed")

    return strs


def _increment_count(map, key1, key2):
    if map.get(key1) is None:
        map[key1] = {key2: 1}
    elif map[key1].get(key2) is None:
        map[key1][key2] = 1
    else:
        map[key1][key2] += 1
