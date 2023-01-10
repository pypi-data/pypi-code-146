from typing import Any
from typing import Dict


def run(
    hub,
    seq: Dict[int, Dict[str, Any]],
    low: Dict[str, Any],
    running: Dict[str, Any],
    options: Dict[str, Any],
) -> Dict[int, Dict[str, Any]]:
    """
    Process the requisites from ESM.
    A requisite can reference a state that is not present in the current run, but exists in ESM.
    This can happen when only subset of the resources are re-executed after the ESM was populated with
    Idem execution of the full set of the resources.
    In this case we want to look-up referenced state from the ESM for arg_bind and require requisites
    This function will check if requisites are present in this run
    If its present we do not do anything as requisites from the current
    run will already be added.
    If the requisite is not present in this run we check the ESM.
    if the resource is already run previously, and it exists in ESM,
    we prepare the requisite and add to the resource requisites.
    This applies to: arg_bind, require

    This function will only add requisites to resources if they are not present in current run and exists in ESM
    This will not modify the current running resources nor this will send any events.
    We only read a state from ESM to add to requisites. The state is not written back to ESM nor added to current run.
    """
    esm_enabled_req_types = ["arg_bind", "require"]
    for ind, data in seq.items():
        req_types_in_chunk = [
            req for req in esm_enabled_req_types if req in data["chunk"]
        ]
        if not req_types_in_chunk:
            continue
        chunk = data["chunk"]
        reqs = {}
        for type in req_types_in_chunk:
            reqs[type] = chunk.get(type)
        for req_type, rdefs in reqs.items():
            for rdef in rdefs:
                if not isinstance(rdef, dict):
                    data["errors"].append(f"{rdef} should be dictionary")
                    continue
                state = next(iter(rdef))
                if hasattr(hub.states, state):
                    if getattr(hub.states[state.split(".")[0]], "SKIP_ESM", False):
                        # This state doesn't use ESM
                        continue
                if isinstance(rdef[state], list):
                    name_defs = rdef[state]
                else:
                    name_defs = [{rdef[state]: []}]

                for name_def in name_defs:
                    if not isinstance(name_def, dict):
                        data["errors"].append(f"{name_def} should be dictionary")
                        continue
                    name = next(iter(name_def))
                    args = name_def[name]
                    r_chunks = hub.idem.tools.get_chunks(low, state, name)
                    if not r_chunks:
                        # If r_chunks is not found in current run check if its present in ESM
                        hub.log.debug(
                            f"Requisite {req_type} {state}:{name} not found in current run. checking in ESM for requisite"
                        )
                        r_chunks_from_esm = hub.tool.idem.esm.get_chunks_from_esm(
                            state, name
                        )
                        if not r_chunks_from_esm:
                            hub.log.debug(
                                f"Requisite {req_type} {state}:{name} not found in ESM."
                            )
                            data["errors"].append(
                                f"Requisite {req_type} {state}:{name} not found in ESM."
                            )
                        for r_chunk in r_chunks_from_esm:
                            reqret_esm = hub.tool.idem.esm.update_running_from_esm(
                                r_chunk
                            )
                            r_tag = hub.idem.tools.gen_chunk_func_tag(r_chunk)
                            reqret = {
                                "req": req_type,
                                "name": name,
                                "state": state,
                                "r_tag": r_tag,
                                "ret": reqret_esm,
                                "chunk": "r_chunk",
                                "args": args,
                            }
                            data["reqrets"].append(reqret)
    return seq
