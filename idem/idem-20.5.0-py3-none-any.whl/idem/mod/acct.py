from typing import Any
from typing import Dict

from dict_tools.data import SafeNamespaceDict


async def modify(hub, name: str, chunk: Dict[str, Any]) -> Dict[str, Any]:
    """
    Check the state containing the target func and call the mod_creds
    function if present. Therefore gathering the list of creds systems
    to use
    """
    run_name = chunk["ctx"]["run_name"]

    # Get the acct_profile that is being used from the chunk and fallback to the acct_profile in the RUN
    profile = chunk.pop("acct_profile", hub.idem.RUNS[run_name]["acct_profile"])

    # Some idem tests or projects that call idem from pure python specify a sub other than "states" for state modules
    # Check for state modules being in alternate locations but default to "states"
    for sub in hub.idem.RUNS[run_name]["subs"]:
        try:
            # Get the keyword arguments of the state function that will be called
            function_parameters = hub[sub][chunk["state"]][
                chunk["fun"]
            ].signature.parameters
            break
        except AttributeError:
            ...
    else:
        function_parameters = {}

    # If the acct_profile was in the function parameters, then add back the acct_profile that is being used
    if "acct_profile" in function_parameters:
        chunk["acct_profile"] = profile

    # If acct_data was in the function parameters and in the chunk, then return the chunk without constructing ctx.acct
    # The function is going to decide what to do with the acct_data
    if "acct_data" in function_parameters and chunk.get("acct_data"):
        # Allow acct_data in the function parameters, but protect it from being exposed in events and logs
        chunk["acct_data"] = SafeNamespaceDict(chunk["acct_data"])
        return chunk

    # Retrieve the acct_data from the state chunk and fallback to the acct_data from the RUN
    acct_data = chunk.pop("acct_data", hub.idem.RUNS[run_name]["acct_data"])

    hub.log.debug(f"Loaded profile: {profile}")

    new_ctx = await hub.idem.acct.ctx(
        path=chunk["state"],
        profile=profile,
        acct_data=acct_data,
        hard_fail=True,
        validate=True,
    )
    chunk["ctx"]["acct"] = new_ctx["acct"]
    chunk["ctx"]["acct_details"] = new_ctx["acct_details"]

    return chunk
