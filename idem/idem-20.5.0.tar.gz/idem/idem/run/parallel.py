import asyncio
import copy
from typing import Dict

DEFAULT_BATCH_SIZE = 50


async def runtime(
    hub,
    name: str,
    ctx: Dict,
    seq: Dict,
    low: Dict,
    running: Dict,
    managed_state: Dict,
    progress,
):
    """
    Execute the runtime in parallel mode
    """
    inds = []
    for ind in seq:
        if seq[ind].get("unmet"):
            # Requisites are unmet, skip this one
            continue
        inds.append(ind)
    if not inds:
        # Nothing can be run, we have hit recursive requisite,
        # or we are done
        pass

    if not hub.OPT or not hub.OPT.get("idem"):
        batch_size = DEFAULT_BATCH_SIZE
    else:
        batch_size = hub.OPT.idem.get("batch_size", DEFAULT_BATCH_SIZE)

    coros = []
    for ind in inds:
        coros.append(
            hub.idem.rules.init.run(
                name,
                # every state run should use unique ctx so that ctx.acct retains correct information during whole state execution.
                copy.deepcopy(ctx),
                low,
                seq[ind],
                running,
                hub.idem.RUNS[name]["run_num"],
                managed_state,
                seq,  # need this object in recreate_on_update rule check, to find the dependents for current seq comp.
            )
        )
        hub.idem.RUNS[name]["run_num"] += 1

    if batch_size <= 0:
        # this is running all of them in parallel
        batch_size = len(coros)
    else:
        hub.log.debug(
            f"{str(batch_size)} will be used as batch size for executing {str(len(inds))} states."
        )

    # Run groups of <batch_size> of the coroutines until they all have been processed
    while coros:
        # Grab the next group of <batch_size>
        chunk = coros[:batch_size]
        # Run the coroutines in parallel with this <batch_size>, updating the progress bar as necessary
        for fut in asyncio.as_completed(chunk):
            await fut
            # Update the progress bar once per function return
            hub.tool.progress.init.update(progress)

        # Remove those <batch_size> from the main body of coroutines
        coros = coros[batch_size:]
