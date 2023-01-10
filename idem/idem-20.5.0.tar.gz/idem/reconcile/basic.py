import asyncio
import copy
from typing import Any
from typing import Dict
from typing import List

import dict_tools.differ as differ


# Reconciliation loop stops after MAX_RERUNS_WO_CHANGE reruns without change.
# This is to make sure we do not retry forever on failures that cannot be fixed by
# reconciliation.
MAX_RERUNS_WO_CHANGE = 3
# Sleep time in seconds between re-runs
DEFAULT_RECONCILE_WAIT = 3
# Dictionary for the default static sleep time
DEFAULT_STATIC_RECONCILE_WAIT = {"static": {"wait_in_seconds": DEFAULT_RECONCILE_WAIT}}
# Dictionary keeping state's reconcile wait time in seconds
_state_to_sleep_map = {}


async def loop(
    hub,
    pending_plugin: str,
    name: str,
    apply_kwargs: Dict[str, Any],
):
    """
    This loop attempts to apply states.
    This function returns once all the states are successful or after MAX_RERUNS_WO_CHANGE, whichever occur first.
    The sleep time between each attempt will be determined by a "wait" plugin and might change between each iterations.
    Reconciliation is required if the state is "pending" as defined by the pending plugin.
    The default pending plugin defines pending state if result  is not 'True' or there are 'changes'.

    @param hub:
    @param pending_plugin: plugin name for checking if the state is pending based on the result
    @param name: name of the run
    @param apply_kwargs: possible addition arguments
    :return: dictionary { "re_runs_count": <number of re-runs that occurred> }
    """
    # Record the first run as following reconciliation re-runs will
    # include subset of pending states
    first_run = copy.deepcopy(hub.idem.RUNS[name]["running"])
    tag_to_reruns_wo_change_count = {}

    # Populate wait time algorithm and values for the different states
    # in this run. State has to define __reconciliation_wait__
    # with values such as:
    # { "exponential": {"wait_in_seconds": 2, "multiplier": 10} }
    # { "static": {"wait_in_seconds": 3} }
    # { "random": {"min_value": 1, "max_value": 10} }
    hub.reconcile.basic.populate_wait_times(first_run)

    # Populate old_state for pending tags
    tag_to_old_state = _populate_old_states(first_run)
    # Concatenate comments for pending tags
    tag_to_comments = hub.reconcile.basic.populate_comments(first_run)
    current_run = first_run

    count = 0
    while True:
        pending_tags = hub.reconcile.basic.get_pending_tags(
            pending_plugin=pending_plugin,
            runs=current_run,
            tag_to_reruns_wo_change_count=tag_to_reruns_wo_change_count,
            ctx=apply_kwargs.get("ctx"),
        )

        if not pending_tags:
            hub.reconcile.basic.update_result(
                name, first_run, current_run, tag_to_old_state, tag_to_comments
            )
            hub.log.debug(f"Reconciliation loop returns after {count} runs.")
            return {"re_runs_count": count}

        sleep_time_sec = get_max_wait_time(hub, count, pending_tags)
        hub.log.debug(f"Sleeping {sleep_time_sec} seconds for {name}")
        await asyncio.sleep(sleep_time_sec)

        count = count + 1
        hub.log.debug(f"Retry {count} for {name}")

        last_run = current_run

        # Re-run pending states
        await hub.idem.run.init.start(name, pending_tags)

        # This run will include only the pending tags
        current_run = hub.idem.RUNS[name]["running"]
        hub.reconcile.basic.populate_comments(current_run, tag_to_comments)
        hub.reconcile.basic.populate_no_changes_count(
            last_run, current_run, tag_to_reruns_wo_change_count
        )


def get_pending_tags(
    hub,
    pending_plugin: str,
    runs: Dict,
    tag_to_reruns_wo_change_count: Dict,
    ctx: Dict = None,
):
    # invoke pending plugin and populate pending tags
    pending_tags = []
    for tag in runs:
        if (
            "pending_kwargs"
            in hub.reconcile.pending[pending_plugin].is_pending.signature.parameters
        ):
            pending_kwargs = {
                "ctx": ctx,
                "reruns_wo_change_count": tag_to_reruns_wo_change_count.get(tag, 0),
            }
            if hub.reconcile.pending[pending_plugin].is_pending(
                ret=runs[tag],
                state=_tag_2_state(tag),
                **pending_kwargs,
            ):
                pending_tags.append(tag)
        elif hub.reconcile.pending[pending_plugin].is_pending(
            ret=runs[tag],
            state=_tag_2_state(tag),
        ):
            pending_tags.append(tag)

    return pending_tags


def populate_wait_times(hub, runs):
    # Populate sleep times per state
    for tag in runs:
        state = _tag_2_state(tag)
        if state not in _state_to_sleep_map.keys():
            try:
                _state_to_sleep_map[state] = getattr(
                    hub.states[state],
                    "__reconcile_wait__",
                    DEFAULT_STATIC_RECONCILE_WAIT,
                )
            except Exception as e:
                hub.log.error(
                    f"Failed to retrieve sleep time for state {state}: {e.__class__.__name__}: {e}"
                )
                _state_to_sleep_map[state] = DEFAULT_STATIC_RECONCILE_WAIT


def get_max_wait_time(hub, run_count, pending_tags: List[str]):
    # Return the maximum wait time among the pending tags
    max_sleep_time = DEFAULT_RECONCILE_WAIT
    for tag in pending_tags:
        state_wait = _state_to_sleep_map.get(
            _tag_2_state(tag), DEFAULT_STATIC_RECONCILE_WAIT
        )
        wait_alg = list(state_wait.keys())[0]
        wait_val = state_wait[wait_alg]
        sleep_time = hub.reconcile.wait[wait_alg].get(**wait_val, run_count=run_count)
        if sleep_time > max_sleep_time:
            max_sleep_time = sleep_time

    return max_sleep_time


def update_result(
    hub,
    name,
    first_run,
    last_run,
    tag_to_old_state: Dict[str, dict],
    tag_to_comments: Dict[str, tuple],
):
    # Merge last_run results into first_run, recalculate changes
    # Update 'old_state' from the original run and recalculate 'changes' to reflect
    # all the changes that occurred during reconciliation:
    # the delta between original run's old_state and last_run 'new_state'
    # Update 'comment' with the cumulative comments from all runs (w/o duplicates)
    # Set that as the 'running' on the hub
    if not last_run:
        return

    first_run.update(last_run)
    for tag in last_run:
        orig_old_state = tag_to_old_state.get(tag, None)
        last_old_state = last_run[tag].get("old_state", None)
        if orig_old_state != last_old_state:
            hub.log.debug(
                f"Replacing 'old_state' for '{_tag_2_state(tag)}': {last_old_state} with {orig_old_state}"
            )

            first_run[tag]["old_state"] = orig_old_state

            # Only when replacing 'old_state' 'changes' have to be re-calculated
            first_run[tag]["changes"] = differ.deep_diff(
                last_run[tag].get("old_state") or {},
                last_run[tag].get("new_state") or {},
            )
        if tag_to_comments.get(tag):
            first_run[tag]["comment"] = tag_to_comments.get(tag)

    hub.idem.RUNS[name]["running"] = first_run


def populate_comments(
    hub, run, tag_to_comments: Dict[str, tuple] = None
) -> Dict[str, tuple]:
    # If tag_to_comments is empty populate it with the run comments.
    # Otherwise add comments to existing
    if not tag_to_comments:
        tag_to_comments = {}
    for tag in run:
        # We expect comments to be of type tuple
        if run[tag].get("comment"):
            comment = run[tag].get("comment")
            if isinstance(comment, str):
                hub.log.debug(
                    f"Expecting a comment of type tuple but got a str: {comment}"
                )
                comment = (comment,)
            elif isinstance(comment, list):
                hub.log.debug(
                    f"Expecting a comment of type tuple but got a list: {comment}"
                )
                comment = tuple(comment)
            elif not isinstance(comment, tuple):
                hub.log.warning(
                    f"Unsupported comment type: {type(comment)}, comment: {str(comment)}"
                )
                continue

            if tag_to_comments.get(tag) and not comment[0] in tag_to_comments.get(tag):
                tag_to_comments[tag] += comment
            else:
                tag_to_comments[tag] = comment

    return tag_to_comments


def populate_no_changes_count(
    hub, last_run, current_run, tag_to_reruns_wo_change_count: Dict[str, int] = None
):
    # If tag_to_comments is empty populate it with the run comments.
    # Otherwise add comments to existing
    if not last_run or not current_run:
        return
    for tag in current_run:
        if last_run.get(tag):
            if (
                last_run[tag]["result"] == current_run[tag]["result"]
                and last_run[tag]["changes"] == current_run[tag]["changes"]
            ):
                tag_to_reruns_wo_change_count[tag] = (
                    tag_to_reruns_wo_change_count.get(tag) + 1
                    if tag_to_reruns_wo_change_count.get(tag)
                    else 1
                )
            else:
                tag_to_reruns_wo_change_count[tag] = 0


def _populate_old_states(run):
    # Keep old_state per tag from the original run
    tag_to_old_state = {}
    for tag in run:
        if run[tag].get("old_state", None):
            tag_to_old_state[tag] = copy.deepcopy(run[tag]["old_state"])
    return tag_to_old_state


def _tag_2_state(tag):
    # Get state from the tag
    return tag[0 : tag.find("_|")]
