from typing import Dict
from typing import List

import dict_tools.data as data


def __init__(hub):
    # Keep track of the number of times the idem runtime is called for the progress bar
    hub.idem.run.init.RUNTIME_ITERATIONS = 0


async def start(hub, name, pending_tags: List = None, target: str = None):
    """
    Called only after the named run has compiled low data. If no low data
    is present an exception will be raised
    pending_tags: list of state tags to re-run, passed from reconciliation.
                  If None all states are executed.
    """
    if not hub.idem.RUNS[name].get("low"):
        raise ValueError(f"No low data for '{name}' in RUNS")
    ctx = data.NamespaceDict({"run_name": name, "test": hub.idem.RUNS[name]["test"]})

    rtime = hub.idem.RUNS[name]["runtime"]
    low = hub.idem.RUNS[name].get("low")
    # Add metadata to second run

    # Fire an event with all the pre-rendered low-data for all states
    await hub.idem.event.put(
        profile="idem-low",
        body=low,
        tags={"ref": "idem.run.init.start", "type": "state-low-data"},
    )
    old_seq = {}
    old_seq_len = -1
    needs_post_low = True
    options = {"invert_state": hub.idem.RUNS[name]["invert_state"]}
    low_declaration_ids = [item.get("__id__") for item in low]

    if pending_tags:
        # During reconciliation, gather pending resources and their requisites to re-run.
        low = await hub.reconcile.rerun.init.gather(low, name, pending_tags)

    if target:
        # If target is specified - identify all its dependencies
        low_items = []
        gather_target_and_reqs(low, [target], low_items)
        if len(low_items) < 1:
            raise ValueError(
                f"Invalid 'target' for run '{name}': {target}. 'target' should be a declaration ID."
            )

        declaration_ids = [item.get("__id__") for item in low_items]
        hub.idem.RUNS[name]["high"] = {
            key: item
            for (key, item) in hub.idem.RUNS[name]["high"].items()
            if key in declaration_ids
        }
        low = low_items

    while True:
        seq = hub.idem.req.seq.init.run(
            None, low, hub.idem.RUNS[name]["running"], options
        )
        if seq == old_seq:
            unmet_reqs = {chunk["tag"]: chunk["unmet"] for chunk in seq.values()}
            if len(unmet_reqs) == 0:
                raise Exception(f"Invalid syntax for '{name}'")
            raise Exception(f"No sequence changed for '{name}': {unmet_reqs}")

        # Initialize the progress bar
        progress_bar = hub.tool.progress.init.create(
            seq,
            desc=f"idem runtime: {hub.idem.run.init.RUNTIME_ITERATIONS}",
            unit="states",
        )
        # Increment the runtime iteration number after using it for the progress bar
        hub.idem.run.init.RUNTIME_ITERATIONS += 1

        await hub.idem.run[rtime].runtime(
            name,
            ctx,
            seq,
            low,
            hub.idem.RUNS[name]["running"],
            hub.idem.RUNS[name]["managed_state"],
            progress=progress_bar,
        )

        render_data = await hub.idem.resolve.init.render(
            name,
            blocks=hub.idem.RUNS[name]["blocks"],
            sls_refs=hub.idem.RUNS[name]["sls_refs"],
            resolved=hub.idem.RUNS[name]["resolved"],
        )
        await hub.idem.sls_source.init.update(name, render_data)

        await hub.idem.state.compile(name)

        extend_low(hub, name, low, low_declaration_ids)

        await hub.idem.event.put(
            profile="idem-low",
            body=low,
            tags={"ref": "idem.run.init.start", "type": "state-low-data"},
        )
        if len(low) <= len(hub.idem.RUNS[name]["running"]):
            if hub.idem.RUNS[name]["post_low"] and needs_post_low:
                hub.idem.RUNS[name]["low"].extend(hub.idem.RUNS[name]["post_low"])
                needs_post_low = False
                extend_low(hub, name, low, low_declaration_ids)
                continue
            else:
                break
        if len(seq) == old_seq_len:
            # check if the sequence chunks are same or not.
            # if same then throw RecursionError else proceed with the flow.
            # this is because, when we add chunk to delete old_resource as part of recreate_on_update requisite
            # length of old_seq and seq are same, but with different sequence components.
            # so we need to compare the chunks of seq and old_seq.

            # generate the tags for old chunks
            old_tags = {
                hub.idem.tools.gen_chunk_func_tag(old_seq.get(index).get("chunk"))
                for index in old_seq
            }

            # generate the tags for current chunks
            current_tags = {
                hub.idem.tools.gen_chunk_func_tag(seq.get(index).get("chunk"))
                for index in seq
            }

            # if old_tags and current_tags are same, then throw RecursionError
            if len(old_tags - current_tags) == 0:
                raise RecursionError(
                    f"No progress made on '{name}', Recursive Requisite!"
                )
        old_seq = seq
        old_seq_len = len(seq)


def gather_target_and_reqs(low: List[Dict], reqs: List[str], low_items: List[Dict]):
    """
    Recursively gather low items of target(s) and their pre-requisites.
    Any reqs - declaration ID might be resolved to multiple resources,
    in case there are multiple resources under the same declaration id.
    :param low: low data
    :param reqs: list of declaration ids of requisites ('require')
    :param low_items: gathered required low items
    :return: low data to execute
    """
    if not reqs:
        return
    for req in reqs:
        req_items = [item for item in low if item.get("__id__") == req]
        # Start filtering only after first iteration, where original item(s) are added
        if len(req_items) < 1:
            continue
        low_items.extend(req_items)
        for req_item in req_items:
            if req_item.get("require"):
                for required in req_item.get("require"):
                    gather_target_and_reqs(low, list(required.values()), low_items)


def extend_low(hub, name, low, low_declaration_ids):
    # If new chunks were added to "low" (post_low etc)
    # Add them in case low was modified by 'pending_tags' or 'target'
    new_low_items = [
        item
        for item in hub.idem.RUNS[name].get("low")
        if item.get("__id__") not in low_declaration_ids
    ]
    low.extend(new_low_items)
    low_declaration_ids += [item.get("__id__") for item in new_low_items]
