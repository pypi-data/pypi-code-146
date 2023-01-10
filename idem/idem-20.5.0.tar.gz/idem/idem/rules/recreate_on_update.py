import copy
from typing import Any
from typing import Dict

from dict_tools import differ


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
    """
    Check to see if the recreate_on_update can be applied.
    """
    if condition != "recreate_on_update":
        return {"errors": [f'"{condition}" is not recreate_on_update requisite.']}

    if "recreate_on_update" in chunk:
        hub.log.debug(
            f"Start applying recreate_on_update requisite for the resource {chunk['__id__']}"
        )

        if not isinstance(chunk["recreate_on_update"], dict):
            return {
                "errors": [
                    f'recreate_on_update requisite should contain a dict of parameters, not {chunk["recreate_on_update"]}'
                ]
            }

        enforced_state = hub.idem.tools.get_enforced_state(chunk, managed_state)

        if (not enforced_state) or (
            enforced_state
            and chunk.get("resource_id")
            and enforced_state.get("resource_id") != chunk.get("resource_id")
        ):
            enforced_state = None
            for key, state in managed_state.items():
                if chunk.get("resource_id") == state.get("resource_id"):
                    enforced_state = state
                    break

        # if creation flow, then skip the process.
        if not bool(enforced_state):
            hub.log.debug(
                f"As the resource {chunk['__id__']} does not exist, recreate_on_update requisite will be ignored and the resource will be created."
            )
            return {}

        hub.log.debug(
            f"Resource {chunk['__id__']} exists, check if recreation is needed."
        )

        # check whether recreation is needed or not.
        needs_recreation = hub.idem.rules.recreate_on_update.is_recreation_required(
            name, chunk, enforced_state
        )
        if not needs_recreation:
            hub.log.debug(f"No changes detected for the resource {chunk['__id__']}")
            return {}

        hub.log.debug(
            f"Start processing recreation flow for the resource {chunk['__id__']}"
        )

        create_before_destroy = chunk["recreate_on_update"].get(
            "create_before_destroy", False
        )

        if create_before_destroy:
            # create new resource, update the dependent resources and then delete old resource.
            hub.log.debug(
                f"Create the new resource for {chunk['__id__']}, update the dependent resources and destroy the old resource."
            )

            # find the dependencies
            # iterate through the execution_seq object and
            # find the dependent resources for current executing chunk.
            dependent_chunks = []
            tag = hub.idem.tools.gen_chunk_func_tag(chunk)
            for ind in execution_seq:
                seq_obj = execution_seq.get(ind)
                if seq_obj.get("unmet") and tag in seq_obj.get("unmet"):
                    dependent_chunks.append(seq_obj.get("chunk"))

            # form require requisite for the dependent chunks and
            # inject this `require` requisite to deletion chunk,
            # so that absent will wait until the update operation of dependent resources is completed.
            require_req = []
            for dependent in dependent_chunks:
                require = {dependent["state"]: dependent["__id__"]}
                require_req.append(require)

            # chunk for deletion of old resource.
            delete_chunk = hub.idem.rules.recreate_on_update.get_deletion_chunk(
                name, chunk, enforced_state
            )
            delete_chunk["require"] = require_req
            hub.idem.RUNS[name].get("add_low").append(delete_chunk)

            # marking the current chunk's resource_id as None, so that
            # this will be considered as new resource creation.
            chunk["resource_id"] = None
            chunk["recreation_flow"] = True
        else:
            # destroy old resource and then create new resource
            hub.log.debug(
                f"Destroy the old resource for {chunk['__id__']} and then create the new resource."
            )

            # chunk for deletion of old resource
            delete_chunk = hub.idem.rules.recreate_on_update.get_deletion_chunk(
                name, chunk, enforced_state
            )
            delete_chunk["recreation_flow"] = True
            hub.idem.RUNS[name].get("add_low").append(delete_chunk)

            # chunk for creating new resource
            # inject `require` requisite with deletion chunk, so that
            # the creation of new resource waits until the old resource is destroyed.
            create_chunk = copy.deepcopy(chunk)
            create_chunk["__id__"] = f"{chunk['__id__']}_create_new"
            create_chunk["resource_id"] = None
            create_chunk["require"] = [{delete_chunk["state"]: delete_chunk["__id__"]}]
            create_chunk.pop("recreate_on_update")
            create_chunk["recreation_flow"] = True
            hub.idem.RUNS[name].get("add_low").append(create_chunk)

            # Mark the current chunk to be halted from current execution.
            chunk["halt_current_execution"] = True

        hub.log.debug(
            f"End processing recreation flow for the resource {chunk['__id__']}"
        )
    return {}


def get_deletion_chunk(hub, name, chunk, enforced_state):
    delete_chunk = {
        "__id__": f"{chunk['__id__']}_delete_old",
        "name": f"{chunk['__id__']}_delete_old",
        "fun": "absent",
        "state": chunk["state"],
    }
    absent_func = hub.idem.rules.init.get_func(name, delete_chunk)
    sig = absent_func.signature
    for param_name in sig.parameters:
        if param_name == "hub" or param_name == "name":
            continue
        delete_chunk[param_name] = (
            chunk.get(param_name)
            if chunk.get(param_name)
            else enforced_state.get(param_name)
        )

    return delete_chunk


def is_recreation_required(hub, name, chunk, enforced_state):
    ignore_keys = []
    ignore_keys.extend(chunk.get("ignore_changes", []))

    # we should compare only the parameters defined for present function of the resource
    # and ignore all other parameters.
    present_func = hub.idem.rules.init.get_func(name, chunk)
    ignore_params = chunk.keys() - present_func.signature.parameters
    ignore_keys.extend(list(ignore_params))

    # when the `name` is formed with `name_prefix`, we should ignore `name` for comparison
    if chunk.get("name_prefix") and chunk.get("name_prefix") in chunk["name"]:
        ignore_keys.append("name")

    desired_state = copy.deepcopy(chunk)

    # some resources need special handling for desired state,
    # so define the `pre_process_desired_state` in
    # the corresponding resource implementation.
    if callable(getattr(hub.states[chunk["state"]], "pre_process_desired_state", None)):
        desired_state = hub.states[chunk["state"]].pre_process_desired_state(
            chunk=desired_state
        )

    # compare the enforced state and desired state.
    desired_state = _handle_null(
        desired_state=desired_state, enforced_state=enforced_state
    )
    diff = differ.deep_diff(old=enforced_state, new=desired_state, ignore=ignore_keys)
    hub.log.debug(f"difference in states: {diff} for the resource {chunk['__id__']}")

    needs_recreation = False
    if diff:
        new = diff.get("new", {})
        for key in new:
            if new[key]:
                needs_recreation = True
            elif type(new[key]) is bool and enforced_state.get(key, False) != new[key]:
                needs_recreation = True

    return needs_recreation


def _handle_null(desired_state: Dict[str, Any], enforced_state: Dict[str, Any]):
    """
    Populates items in desired_state from the enforced_state if it does not exist.
    If exists and is None, then override it with the value from enforced_state.
    """
    if isinstance(enforced_state, dict):
        for key, value in enforced_state.items():
            if key in desired_state:
                desired_value = desired_state.get(key)
                if desired_value is None:
                    desired_state[key] = value
                elif isinstance(desired_value, dict):
                    desired_state[key] = _handle_null(desired_value, value)
            else:
                desired_state[key] = value

    return desired_state
