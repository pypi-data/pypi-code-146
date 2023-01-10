import pathlib
import re
from typing import Any
from typing import Dict
from typing import List


def get_refs(hub, *, sources: List[str], refs: List[str]) -> Dict[str, List[str]]:
    """
    Determine where the sls sources are

    :param hub:
    :param sources: sls-sources or params-sources
    :param refs: References to sls within the given sources
    """
    sls_sources = []
    slses = []
    for ref in refs:
        hub.idem.sls_source.init.process(sls_sources, slses, ref)

    sls_sources.extend(sources)

    return {"sls_sources": sls_sources, "sls": slses}


def process(hub, sources: List[str], slses: List[str], ref: str):
    """
    If an SLS ref represents a local file, then make sure its location is added to sources

    :param sources: sls-sources or params-sources
    :param slses: sls locations within sources
    :param ref: A reference to an sls within the given sources
    """
    # Normalize the sls ref to be all dots
    normalized_ref = hub.idem.sls_source.init.normalize(ref)
    # Check if this is a local file path that exists
    de_normalized_ref = hub.idem.sls_source.init.de_normalize(ref)

    # Check if the sls input was a file
    path = pathlib.Path(de_normalized_ref)

    # If multiple SLS were passed with "init" as the final name, imply a source without the init to avoid collisions
    if path.stem == "init":
        path = path.parent

    for loc, _ in hub.idem.get.locations(ref):
        loc_path = pathlib.Path(loc)
        if loc_path.is_file():
            slses.append(normalized_ref)
            implied = f"file://{loc_path.parent.resolve().absolute()}"
            if implied not in sources:
                sources.append(implied)
                return
    else:
        # Input is not a file
        slses.append(normalized_ref)


async def gather(hub, name: str, *sls):
    """
    Gather the named sls references into the RUNS structure

    :param hub:
    :param name: The state run name
    :param sls: sls locations within sources
    """
    sources = hub.idem.RUNS[name]["sls_sources"]
    gather_data = await hub.idem.resolve.init.gather(name, *sls, sources=sources)
    await hub.idem.sls_source.init.update(name, gather_data)


async def update(hub, name: str, gather_data: Dict[str, Any]):
    """
    Update the RUNS dictionary with the output of the render process

    :param hub:
    :param name: The state run name
    :param gather_data: The output of hub.idem.resolve.init.gather/render

    """
    if gather_data.get("errors"):
        hub.idem.RUNS[name]["errors"] = gather_data["errors"]
        return
    if gather_data.get("blocks"):
        hub.idem.RUNS[name]["blocks"] = gather_data["blocks"]
    if gather_data.get("sls_refs"):
        hub.idem.RUNS[name]["sls_refs"] = gather_data["sls_refs"]
    if gather_data.get("resolved"):
        hub.idem.RUNS[name]["resolved"].update(gather_data["resolved"])

    for sls_ref, high_state in gather_data.get("state", {}).items():
        hub.idem.sls_source.init.decls(name, high_state, sls_ref)
        if hub.idem.RUNS[name]["errors"]:
            return

        # Check for duplicate state ids
        # This may occur when an SLS includes other SLSs -- the renderer can't catch these kinds of duplicates
        duplicates = set(high_state).intersection(hub.idem.RUNS[name]["high"])
        if duplicates:
            hub.idem.RUNS[name]["errors"].append(
                f"Duplicate state declarations found in SLS tree: {' '.join(duplicates)}"
            )
            return

        # Fire an event with the new high data
        await hub.idem.event.put(
            profile="idem-high",
            body=high_state,
            tags={"type": "state-high-data", "ref": "idem.sls_source.init.gather"},
        )
        hub.idem.RUNS[name]["high"].update(high_state)


def decls(
    hub,
    name: str,
    state: Dict[str, Any],
    sls_ref: str,
):
    """
    Resolve state formatting and data insertion

    :param hub:
    :param name: The state run name
    :param state: A rendered block from the sls
    :param sls_ref: A reference to another sls within the given sources
    """
    for id_ in hub.idem.resolve.init.iter(state):
        if not isinstance(state[id_], Dict):
            if isinstance(state[id_], str):
                # Is this is a short state, it needs to be padded
                if "." in state[id_]:
                    comps = state[id_].split(".")
                    state_ref = ".".join(comps[:-1])
                    state[id_] = {
                        "__sls__": sls_ref,
                        state_ref: [comps[-1]],
                    }
                    continue

            hub.idem.RUNS[name]["errors"].append(
                f"ID {id_} in SLS {sls_ref} is not a dictionary"
            )
            continue

        skeys = set()
        for key in list(state[id_]):
            if key.startswith("_"):
                continue
            if not isinstance(state[id_][key], List):
                continue
            if "." in key:
                comps = key.split(".")
                # Idem doesn't support state files such as:
                #
                #     /etc/redis/redis.conf:
                #       file.managed:
                #         - user: redis
                #         - group: redis
                #         - mode: 644
                #       file.comment:
                #           - regex: ^requirepass
                ref = ".".join(comps[:-1])
                if ref in skeys:
                    hub.idem.RUNS[name]["errors"].append(
                        f'ID "{id_}" in SLS "{sls_ref}" contains multiple state declarations from the same sub: {ref}'
                    )
                    continue
                state[id_][ref] = state[id_].pop(key)
                state[id_][ref].append(comps[-1])
                skeys.add(ref)
                continue
            skeys.add(key)

        if "__sls__" not in state[id_]:
            state[id_]["__sls__"] = sls_ref


def normalize(hub, path: str) -> str:
    """
    Transform a file path to a normalized SLS ref

    - Replace dots with \b and replace / with .
    - The existing dots may be part of a file name

    I.E
    "foo.bar/baz.bop.sls" will become "foo\bbar.baz\bbop"
    """
    p = pathlib.PurePosixPath(path)
    if "\b" in str(p) or "/" not in str(p):
        # We already have null characters or no "/"s in a pure posix path -- we can assume it is already normalized
        return path
    last_ref_name = p.stem if p.suffix == ".sls" else p.name
    normalized_ref = (
        str(pathlib.PurePosixPath(p.parent).joinpath(last_ref_name))
        # Double backs will temporarily be replaced with a backspace \0
        .replace("../", "\0")
        .replace(".", "\b")
        .replace("/", ".")
        # Swap the null character for a regular "."
        .replace("\0", ".")
    )
    return normalized_ref


def de_normalize(hub, path: str) -> str:
    """
    Transform an sls ref back into a file path for lookups

    I.E
    "foo\bbar.baz\bbop" will become "foo.bar/baz.bop"
    """
    if "/" in path:
        # Already denormalized
        return path

    # Replace leading dots with ../
    # I.E. ..ref.nest with ../../ref/nest
    match = re.match(r"^(\.*)(.*)$", path)
    levels, ref = match.groups()
    prepend = ""

    for _ in levels:
        # For each "." add a "../" to the de-normalized path
        prepend = f"../{prepend}"

    denormalized = ref.replace(".", "/").replace("\b", ".")

    return prepend + denormalized
