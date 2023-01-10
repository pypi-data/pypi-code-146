import datetime
from typing import Any
from typing import Dict

import pop.loader


# These are keywords passed to state module functions which are to be used
# by idem in this state module and not on the actual state module function
STATE_REQUISITE_KEYWORDS = frozenset(
    [
        "onchanges",
        "onchanges_any",
        "onfail",
        "onfail_any",
        "onfail_all",
        "onfail_stop",
        "prereq",
        "prerequired",
        "watch",
        "watch_any",
        "require",
        "require_any",
        "listen",
        "arg_bind",
        "sensitive",
        "ignore_changes",
        "recreate_on_update",
    ]
)
STATE_REQUISITE_IN_KEYWORDS = frozenset(
    [
        "onchanges_in",
        "onfail_in",
        "prereq_in",
        "watch_in",
        "require_in",
        "listen_in",
    ]
)
STATE_RUNTIME_KEYWORDS = frozenset(
    [
        "fun",
        "state",
        "check_cmd",
        "failhard",
        "onlyif",
        "unless",
        "retry",
        "order",
        "parallel",
        "prereq",
        "prereq_in",
        "prerequired",
        "reload_modules",
        "reload_grains",
        "reload_pillar",
        "rerun_data",
        "runas",
        "runas_password",
        "fire_event",
        "saltenv",
        "use",
        "use_in",
        "__run_name",
        "__env__",
        "__sls__",
        "__id__",
        "__orchestration_jid__",
        "__pub_user",
        "__pub_arg",
        "__pub_jid",
        "__pub_fun",
        "__pub_tgt",
        "__pub_ret",
        "__pub_pid",
        "__pub_tgt_type",
        "__prereq__",
    ]
)

STATE_INTERNAL_KEYWORDS = STATE_REQUISITE_KEYWORDS.union(
    STATE_REQUISITE_IN_KEYWORDS
).union(STATE_RUNTIME_KEYWORDS)


def get_func(hub, name, chunk, fun=None):
    """
    Given the runtime name and the chunk in question, determine what function
    on the hub that can be run
    """
    if fun is None:
        fun = chunk["fun"]
    s_ref = chunk["state"]

    # Check if an auto_state exists for this ref
    try:
        if "auto_state" in hub.exec[s_ref].__contracts__:
            chunk["exec_mod_ref"] = s_ref
            return hub.states.auto_state[fun]
    except AttributeError or TypeError:
        ...
    for sub in hub.idem.RUNS[name]["subs"]:
        test = f"{sub}.{s_ref}.{fun}"
        try:
            func = getattr(hub, test)
        except AttributeError:
            continue
        if isinstance(func, pop.loader.LoadedMod):
            continue
        if func is None:
            continue
        return func
    return None


async def run(
    hub, name, ctx, low, seq_comp, running, run_num, managed_state, execution_seq
):
    """
    All requisites have been met for this low chunk.
    """
    chunk = seq_comp["chunk"]
    tag = hub.idem.tools.gen_chunk_func_tag(chunk)
    esm_tag = hub.idem.tools.gen_chunk_esm_tag(chunk)
    start_time = datetime.datetime.now()
    skip_check = ["resolver"]
    rdats = {}
    running[tag] = {
        "tag": tag,
        "name": chunk["name"],
        "__id__": chunk["__id__"],
        "changes": {},
        "new_state": None,
        "old_state": None,
        "comment": None,
        "rerun_data": None,
        "result": False,
        "esm_tag": esm_tag,
        "__run_num": run_num,
        "start_time": str(start_time),
        "total_seconds": 0,
        "sls_meta": hub.idem.RUNS[name]["meta"],
    }

    ctx["tag"] = tag
    ctx["rerun_data"] = chunk.get("rerun_data")

    errors = seq_comp.get("errors", [])
    for reqret in seq_comp.get("reqrets", []):
        req = reqret["req"]
        if req not in rdats:
            rdats[req] = []
        rules = hub.idem.RMAP[req]
        for rule in rules:
            if rule in skip_check:
                continue
            if hasattr(hub.idem.rules, rule):
                rdat = hub.idem.rules[rule].check(
                    name,
                    ctx,
                    rules[rule],
                    reqret,
                    chunk,
                    managed_state,
                    execution_seq,
                )
                rdats[req].append(rdat)

    # Get the function to be called as early as possible
    func = hub.idem.rules.init.get_func(name, chunk)
    ref = None
    if func:
        ref = f"{func.ref}.{func.__name__}"

    errors += hub.idem.resolver.init.resolve(rdats)
    if errors:
        running[tag]["comment"] = "\n".join(errors)
        running[tag]["total_seconds"] = (
            datetime.datetime.now() - start_time
        ).total_seconds()
        await hub.idem.event.put(
            profile="idem-run",
            body=running[tag],
            tags={
                "ref": ref,
                "type": "state-result",
                "acct_details": None,
            },
        )
        return

    # if the requisite `recreate_on_update` is processed and `create_before_destroy=false`
    # we will halt the current chunk from execution as the chunks
    # for destroying old resource and creating new resource will be executed in next run.

    if chunk.get("halt_current_execution", False):
        msg = f"The resource {chunk['__id__']} will be recreated."
        hub.log.debug(msg)
        running[tag]["comment"] = msg
        running[tag]["result"] = True
        running[tag]["total_seconds"] = (
            datetime.datetime.now() - start_time
        ).total_seconds()
        await hub.idem.event.put(
            profile="idem-run",
            body=running[tag],
            tags={
                "ref": ref,
                "type": "state-result",
                "acct_details": None,
            },
        )

        # Update the result for reconciliation
        hub.idem.RUNS[name]["running"][tag]["comment"] = msg
        hub.idem.RUNS[name]["running"][tag]["result"] = True
        return

    await hub.idem.event.put(
        profile="idem-chunk",
        body=chunk,
        tags={
            "ref": ref,
            "type": "state-chunk",
        },
    )
    if func is None:
        running[tag]["comment"] = (
            f'Could not find function to enforce {chunk["state"]}. '
            f"Please make sure that the corresponding plugin is loaded."
        )
        running[tag]["total_seconds"] = (
            datetime.datetime.now() - start_time
        ).total_seconds()
        await hub.idem.event.put(
            profile="idem-run",
            body=running[tag],
            tags={
                "ref": ref,
                "type": "state-result",
                "acct_details": None,
            },
        )
        return
    chunk["ctx"] = ctx
    chunk = await hub.idem.mod.init.modify(name, chunk)
    call_kwargs = hub.idem.tools.format_call(
        fun=func,
        data=chunk,
        ignore_changes=chunk.get("ignore_changes"),
        expected_extra_kws=STATE_INTERNAL_KEYWORDS,
        enforced_state=hub.idem.tools.get_enforced_state(chunk, managed_state),
    )
    for req, rlist in rdats.items():
        for rdat in rlist:
            if "pre" in rdat:
                ret = rdat["pre"](**call_kwargs)
                await hub.pop.loop.unwrap(ret)
    # This is when the state is actually called
    ret = func(**call_kwargs)
    ret = await hub.pop.loop.unwrap(ret)

    # Update ESM under the following conditions:
    # ESM will be updated when Idem ran with "refresh" subcommand (which implies the `test` flag).
    # Or, when Idem state is not running with --test
    # When the above rule is met, one of the following conditions need to be met:
    # - "force_save" is True (This implies the plugin state has insisted Idem to save a resource state)
    # - "result" is True (This implies the Idem state operation is successful)
    # - "old_state" doesn't exist but "new_state" exists. This implies a creation operation during the
    #    Idem state run. The "new_state" will be saved even if the operation failed ("result" is False).
    if (
        (getattr(hub, "SUBPARSER", None) == "refresh" or not ctx.get("test"))
        and (
            ret.get("result")
            or ret.get("force_save", False)
            or ((not ret.get("old_state")) and ret.get("new_state"))
        )
        and not chunk["ctx"].get("skip_esm", False)
    ):
        new_state = ret.get("new_state")
        if new_state:
            # Changes were made, update the cache
            managed_state[esm_tag] = new_state
        else:
            # The successful new_state shows a deleted resource, remove it from the cache
            managed_state.pop(esm_tag, None)

    # Remove force_save from ret as it has been used and does not need to be kept in ret
    ret.pop("force_save", None)

    for req, rlist in rdats.items():
        for rdat in rlist:
            if "post" in rdat:
                ret = rdat["post"](**call_kwargs)
                ret = await hub.pop.loop.unwrap(ret)

    # Update the result for reconciliation
    # if the current executing chunk is for recreating a resource, then update it in ret also
    if chunk.get("recreation_flow", False):
        ret["recreation_flow"] = True

    hub.idem.RUNS[name]["running"][tag].update(ret)

    running[tag].update(ret)
    running[tag]["total_seconds"] = (
        datetime.datetime.now() - start_time
    ).total_seconds()

    await hub.idem.event.put(
        profile="idem-run",
        body=running[tag],
        tags={
            "ref": ref,
            "type": "state-result",
            "acct_details": chunk["ctx"].get("acct_details"),
        },
    )


def check(
    hub,
    name: str,
    ctx: Dict[str, Any],
    condition: Any,
    reqret: Dict[str, Any],
    chunk: Dict[str, Any],
    managed_state: Dict[str, Any],
    execution_seq: Dict,
) -> Dict[str, Any]:
    ...
