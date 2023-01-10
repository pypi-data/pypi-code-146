import asyncio
import re
from typing import Any
from typing import Dict

import jmespath
import pop.contract
import pop.hub
import pop.loader


async def run(
    hub,
    desc_glob: str = "*",
    acct_file: str = None,
    acct_key: str = None,
    acct_profile: str = None,
    progress: bool = False,
    search_path: str = None,
    hard_fail: bool = False,
) -> Dict[str, Dict[str, Any]]:
    """
    :param hub:
    :param desc_glob:
    :param acct_file:
    :param acct_key:
    :param acct_profile:
    :param progress:
    :return:
    """
    result = {}
    coros = [
        _
        async for _ in hub.idem.describe.recurse(
            hub.states, desc_glob, acct_file, acct_key, acct_profile
        )
    ]

    if len(coros) == 0:
        # The current approach is to recurse through all loaded resources types.
        # If it reaches here, it should have gone through all possible resource types when looking up
        # Do not fail but instead log it, do not return from here as there might be 'auto_state' to process
        hub.log.warning(
            f"Cannot find anything to describe for resource type(s) '{desc_glob}'"
        )

    # This is going through dynamically generated states for exec modules
    # implementing __contracts__ = ["auto_state"]
    async for coro in hub.idem.describe.recurse(
        hub.exec, desc_glob, acct_file, acct_key, acct_profile
    ):
        coros.append(coro)

    if len(coros) == 0:
        # If there is none to process including 'auto_state', there is no progress to show. Return empty result
        return result

    # Create the progress bar
    progress_bar = hub.tool.progress.init.create(coros)

    for ret in asyncio.as_completed(coros):
        hub.tool.progress.init.update(progress_bar)
        try:
            result.update(await ret)
        except Exception as e:
            hub.log.error(f"Error during describe: {e.__class__.__name__}: {e}")
            if hard_fail:
                raise
    if progress:
        progress_bar.close()
    if search_path:
        prepped = hub.output.jmespath.prepare(result)
        searched = jmespath.search(search_path, prepped)
        if hub.OPT.rend.get("output") == "jmespath":
            # Don't post-process the result, it's already in jmespath format
            return searched
        else:
            return hub.output.jmespath.revert(searched)
    return result


async def recurse(
    hub,
    mod: pop.loader.LoadedMod or pop.hub.Sub,
    glob: str,
    acct_file: str,
    acct_key: str,
    acct_profile: str,
    ref: str = "",
):
    if hasattr(mod, "_subs"):
        for sub in mod._subs:
            if ref:
                r = ".".join([ref, sub])
            else:
                r = sub
            async for c in hub.idem.describe.recurse(
                mod[sub], glob, acct_file, acct_key, acct_profile, r
            ):
                yield c
    if hasattr(mod, "_loaded"):
        for loaded in mod._loaded:
            if ref:
                r = ".".join([ref, loaded])
            else:
                r = loaded
            async for c in hub.idem.describe.recurse(
                mod[loaded], glob, acct_file, acct_key, acct_profile, r
            ):
                yield c

    # Only describe functions that implement the "describe" contract
    if hasattr(mod, "__contracts__"):
        if "auto_state" in mod.__contracts__:
            # Handle auto state describe functions
            ctx = await hub.idem.acct.ctx(
                path=glob,
                acct_file=acct_file,
                acct_key=acct_key,
                profile=acct_profile,
                hard_fail=True,
                validate=True,
            )
            ctx.exec_mod_ref = ref
            coro = hub.states.auto_state.describe(ctx)
            yield hub.pop.Loop.create_task(coro)
        elif "resource" in mod.__contracts__:
            if re.fullmatch(glob, ref):
                ctx = await hub.idem.acct.ctx(
                    path=ref,
                    acct_file=acct_file,
                    acct_key=acct_key,
                    profile=acct_profile,
                    hard_fail=True,
                    validate=True,
                )
                if isinstance(mod.describe, pop.contract.ContractedAsync):
                    coro = mod.describe(ctx)
                else:

                    async def _async_desc():
                        return mod.describe(ctx)

                    coro = _async_desc()
                yield hub.pop.Loop.create_task(coro)
    elif (
        hasattr(mod, "_funcs") and "describe" in mod._funcs and re.fullmatch(glob, ref)
    ):
        raise ValueError(f"Implement the resource contract for '{ref}'.")
