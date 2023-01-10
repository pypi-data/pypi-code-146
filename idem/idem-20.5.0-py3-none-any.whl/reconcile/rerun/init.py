from typing import Dict
from typing import List

REQUIRE_FILTER_OUT = [{"fun": "absent"}, {"fun": "present"}]
ARG_BIND_FILTER_IN = [{"state": "exec"}]


async def gather(hub, ctx, name: str, pending_tags: List = None):
    low = hub.idem.RUNS[name].get("low")

    # Getting 'rerun_data' from all tags.
    # 'rerun_data' is a metadata passed between re-runs.
    rerun_data_map = {}
    for tag in hub.idem.RUNS[name]["running"]:
        if hub.idem.RUNS[name]["running"][tag].get("rerun_data"):
            rerun_data_map[tag.split("_|-")[1]] = hub.idem.RUNS[name]["running"][
                tag
            ].get("rerun_data")

    # Clearing previous running data.
    hub.idem.RUNS[name]["running"] = {}
    pending_declaration_ids = [tag.split("_|-")[1] for tag in pending_tags]

    # Gather the states that are corresponding to the pending tags,
    # and the 'require' dependencies that are not resources:
    # such as time.sleep or data.write or exec.
    low_items = []
    populate_low_items(
        low,
        pending_declaration_ids,
        low_items,
        filter_out=REQUIRE_FILTER_OUT,
        filter_in=ARG_BIND_FILTER_IN,
    )

    for key, rerun_data in rerun_data_map.items():
        for item in low_items:
            if item.get("__id__") == key:
                item["rerun_data"] = rerun_data

    return low_items


def populate_low_items(
    low: List[Dict],
    reqs: List[str],
    low_items: List[Dict],
    filter_out: List = None,
    filter_in: List = None,
):
    """
    Recursively gather low items of target(s) and their pre-requisites.
    Any reqs - declaration ID might be resolved to multiple resources,
    in case there are multiple resources under the same declaration id.
    :param low:  low data
    :param reqs: list of declaration ids of requisites ('require')
    :param low_items: gathered required low items
    :param filter_out: filter to filter out low items (exclude)
    :param filter_in: filter to include low items
    """
    if not reqs:
        return
    for req in reqs:
        req_items = [item for item in low if item.get("__id__") == req]
        # Start filtering only after first iteration, where original item(s) are added
        if len(low_items) > 0 and filter_out:
            req_items = filter_out_(req_items, filters=filter_out)
        elif len(low_items) > 0 and filter_in:
            req_items = filter_in_(req_items, filters=filter_in)
        if len(req_items) < 1:
            continue
        low_items.extend(req_items)
        for req_item in req_items:
            if req_item.get("require"):
                for required in req_item.get("require"):
                    populate_low_items(
                        low,
                        list(required.values()),
                        low_items,
                        filter_out=REQUIRE_FILTER_OUT,
                    )
            if req_item.get("arg_bind"):
                req_ids = []
                for arg_bind in req_item.get("arg_bind"):
                    for key, values in arg_bind.items():
                        for value in values:
                            for req_id, val in value.items():
                                req_ids.append(req_id)
                populate_low_items(
                    low, list(req_ids), low_items, filter_in=ARG_BIND_FILTER_IN
                )


def filter_out_(low_items: List[Dict], filters: List[Dict]) -> List[Dict]:
    # Filter out required low items that are resources (present/absent)
    # as those will be retrieved from the ESM. But any others exec/sleep/script
    # required will be executed
    if not low_items or not filters:
        return low_items

    new_low_items = []
    for item in low_items:
        match = False
        for f in filters:
            for key, value in f.items():
                if item.get(key) == value:
                    match = True
        if not match:
            new_low_items.append(item)

    return new_low_items


def filter_in_(low_items: List[Dict], filters: List[Dict]) -> List[Dict]:
    # Find low items that match the filter criteria
    if not low_items or not filters:
        return low_items

    new_low_items = []
    for item in low_items:
        for f in filters:
            for key, value in f.items():
                if item.get(key) == value:
                    new_low_items.append(item)

    return new_low_items
