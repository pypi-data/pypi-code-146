"""
The sls source is used to gather sls files, render them and return the initial
phase 1 highdata. This involves translating sls references into file paths,
downloading those sls files and then rendering them.

Once an sls file is rendered the include statements are resolved as well.
"""
import collections
from typing import Any
from typing import Dict
from typing import Generator
from typing import List
from typing import Set

__func_alias__ = {"iter_": "iter"}


def __init__(hub):
    hub.idem.resolve.init.HARD_FAIL = False


async def gather(hub, name: str, *sls, sources: List[str]) -> Dict[str, Any]:
    """
    Gather the named sls references

    :param hub:
    :param name: The state run name
    :param sls: sls locations within sources
    :param sources: sls-sources or params-sources
    """
    ret = {
        "state": {},
        "sls_refs": {},
        "blocks": {},
        "resolved": set(),
        "errors": [],
        "rendered": {},
        "order": [],
    }

    # Load sls content from sls files
    sls_content = collections.OrderedDict()
    sls_refs_map = {}
    for sls_relative_ref in sls:
        try:
            resolve_data = await hub.idem.get.ref(name, sls_relative_ref, sources)
            # TODO: This need to be discussed. The question is what to do when Idem sees the same sls file gets loaded
            #  again. The current behavior is, Idem doesn't fail, but it put this file to a later rendered order. See
            #  test_params_override_multiple_files test
            #  into a later order
            sls_ref = resolve_data["sls"]
            cfn = resolve_data["content"]

            if sls_ref in sls_content:
                sls_content.pop(sls_ref)
            sls_content[sls_ref] = cfn
            sls_refs_map[sls_ref] = sls_relative_ref
        except Exception as e:
            msg = f"Error while collecting blocks: {e.__class__.__name__}: {e}"
            hub.log.debug(msg)
            ret["errors"].append(msg)
            if hub.idem.resolve.init.HARD_FAIL:
                raise
            return ret

    # Render sls content into blocks
    block_data = await hub.idem.resolve.init.get_blocks(name, sls_content, sls_refs_map)
    ret.update(block_data)
    if ret["errors"]:
        return ret

    render_data = await hub.idem.resolve.init.render(
        name=name,
        blocks=block_data["blocks"],
        sls_refs=block_data["sls_refs"],
        resolved=block_data["resolved"],
    )
    unresolved_refs = render_data.pop("unresolved_refs", None)
    ret.update(render_data)

    if unresolved_refs:
        recurse = await hub.idem.resolve.init.gather(
            name, *unresolved_refs, sources=sources
        )
        ret["state"].update(recurse["state"])
        ret["rendered"].update(recurse["rendered"])
        ret["sls_refs"].update(recurse["sls_refs"])
        ret["blocks"].update(recurse["blocks"])
        ret["resolved"].update(recurse["resolved"])
        ret["errors"].extend(recurse["errors"])
        ret["order"].extend(recurse["order"])

    # Append the completely resolved sls files in order. This order is used for param override.
    ret["order"] += list(sls_content.keys())
    return ret


async def get_blocks(
    hub, name: str, sls_content: Dict, sls_ref_map: Dict
) -> Dict[str, Any]:
    """
    Returns the data from the SLS file if it can be found

    :param hub:
    :param name: The state run name
    :param sls_content: Unique sls_ref with sls file content in dict
    :param sls_ref_map: Map of the unique sls_ref to the relative sls file path within its source
    """
    ret = {"blocks": {}, "sls_refs": {}, "resolved": set(), "errors": []}
    for sls_ref, cfn in sls_content.items():
        if not cfn:
            msg = f"SLS ref '{sls_ref}' did not resolve"
            hub.log.debug(msg)
            ret["errors"].append(msg)
            return ret

        blocks = hub.rend.init.blocks(fn=sls_ref, content=cfn)
        if sls_ref in ret["sls_refs"]:
            msg = f"Discovered SLS ref collision between {ret['sls_refs']} and '{sls_ref}'. "
            hub.log.debug(msg)
            ret["errors"].append(msg)
            return ret
        ret["blocks"][sls_ref] = blocks
        ret["sls_refs"][sls_ref] = sls_ref_map[sls_ref]
        ret["resolved"].add(sls_ref)

    return ret


async def render(
    hub, name: str, blocks: Dict[str, Any], sls_refs: Dict[str, str], resolved: Set[str]
) -> Dict[str, Any]:
    """
    Pop the available blocks and render them if they have satisfied requisites

    :param hub:
    :param name: The state run name
    :param blocks: A mapping of sls refs to raw byte data representing a state
    :param sls_refs: References to sls within the given sources
    :param resolved: The names of SLSs that have been resolved
    """
    ret = {"rendered": {}, "state": {}, "unresolved_refs": []}
    for sls_ref, block in blocks.items():
        ret["state"][sls_ref] = {}
        cfn = sls_refs[sls_ref]
        for bname, chunk in block.items():
            clear = True
            for key, val in chunk.get("keys", {}).items():
                # If there is a render requisite plugin for this key then run its "check" method
                if key in hub.idem.resolve.requisite:
                    clear &= hub.idem.resolve.requisite[key].check(name, val)
                else:
                    clear = False

            if not clear:
                continue

            try:
                state = await hub.rend.init.parse_bytes(
                    chunk,
                    hub.idem.RUNS[name]["render"],
                    params=hub.idem.RUNS[name]["params"],
                )
            except Exception as e:
                msg = f"Error while parsing '{cfn}': {e}"
                hub.log.debug(msg)
                e.args = (msg,)
                raise e

            ret["rendered"][sls_ref] = bname
            if state is None:
                msg = f"SLS ref '{sls_ref}' is not resolved to any state."
                # if a rendered sls file turns to be empty
                hub.log.info(msg)
                continue
            # Process the state through the resolve plugins
            unresolved_refs = await hub.idem.resolve.init.apply(
                name=name,
                state=state,
                sls_ref=sls_ref,
                cfn=cfn,
                resolved=resolved,
            )
            ret["unresolved_refs"].extend(unresolved_refs)
            ret["state"][sls_ref].update(state)

    for sls_ref, bname in ret["rendered"].items():
        blocks[sls_ref].pop(bname, None)
    return ret


async def apply(
    hub,
    name: str,
    state: Dict[str, Any],
    sls_ref: str,
    cfn: str,
    resolved: Set[str],
) -> List[str]:
    """
    Introduce the raw state into the running dataset

    :param hub:
    :param name: The state run name
    :param state: A rendered block from the sls
    :param sls_ref: A reference to another sls within the given sources
    :param cfn: The cache file name, or the location of sls within the given sources
    :param resolved: a set of refs that have already been resolved
    """
    unresolved_refs = []
    if not isinstance(state, Dict):
        hub.idem.RUNS[name]["errors"].append(
            f"SLS {sls_ref} is not formed as a dict but as a {type(state)}"
        )
        return unresolved_refs

    for top_level_resolver in hub.idem.resolve._loaded:
        if top_level_resolver == "init":
            # We are currently in resolve.init.apply, avoid infinite recursion
            continue
        ret = await hub.idem.resolve[top_level_resolver].apply(
            name=name,
            state=state,
            sls_ref=sls_ref,
            cfn=cfn,
            resolved=resolved,
        )
        unresolved_refs.extend(ret)
    return unresolved_refs


def iter_(hub, state: Dict[str, Any]) -> Generator:
    """
    iterate over a state, skipping known keywords

    :param hub:
    :param state: A rendered block from the sls
    """
    for id_ in state:
        if any(id_ in getattr(plugin, "KEYWORDS", []) for plugin in hub.idem.resolve):
            continue
        yield id_
