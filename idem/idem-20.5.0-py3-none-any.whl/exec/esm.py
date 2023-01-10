from typing import Any
from typing import Dict


async def unlock(
    hub,
    ctx,
    provider: str = None,
    profile: str = None,
    acct_data: Dict[str, Any] = None,
):
    """
    Remove the lock from the esm profile based on the provider and profile name.
    """
    # Get the acct data from the kwargs and fallback to the acct_data in the current runtime
    if acct_data is None:
        acct_data = await hub.idem.acct.data(
            acct_key=hub.OPT.acct.get("acct_key"),
            acct_file=hub.OPT.acct.get("acct_file"),
            acct_blob=hub.OPT.acct.get("acct_blob"),
        )

    # Get the ESM ctx
    # copied from https://gitlab.com/vmware/idem/idem/-/blob/master/idem/idem/managed.py#L33
    ctx = await hub.idem.acct.ctx(
        f"esm.{provider}",
        profile=profile,
        acct_data=acct_data,
    )
    hub.log.info(f"Unlocking state run on provider {provider} using profile {profile}")
    try:
        await hub.esm[provider].exit_(ctx, None, None)
    except Exception as e:
        return {
            "comment": [f"{e.__class__.__name__}: {e}"],
            "result": False,
            "ret": None,
        }
    return {"result": True, "comment": None, "ret": {}}


def version(hub):
    """
    Get the latest supported esm version from idem
    """
    return {
        "result": True,
        "comment": None,
        "ret": ".".join(str(x) for x in hub.esm.VERSION),
    }
