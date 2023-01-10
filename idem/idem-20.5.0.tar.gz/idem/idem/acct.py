from typing import Any
from typing import Dict
from typing import Iterable

import aiofiles
import dict_tools.data

__func_alias__ = {"ctx_": "ctx"}


async def ctx_(
    hub,
    path: str,
    profile: str,
    acct_file: str = None,
    acct_key: str = None,
    acct_blob: bytes = None,
    acct_data: Dict = None,
    hard_fail: bool = False,
    validate: bool = False,
):
    """
    :param hub:
    :param path: The reference on the hub to the function that needs authentication
    :param profile: The profile to use for this operation
    :param acct_file:
    :param acct_key:
    :param acct_blob:
    :param acct_data:
    :param hard_fail: Raise an error if there are any issues while collecting a profile
    :param validate: Raise an error if the function needs a ctx and the named profile does not exist
    :return:
    """
    ctx = dict_tools.data.NamespaceDict(test=False, acct=None, acct_details=None)

    parts = path.split(".")
    if parts[0] in ("exec", "states", "esm"):
        parts = parts[1:]
    elif parts[0] in ("idem",) and parts[1] in ("sls",):
        parts = parts[2:]

    if not parts:
        return ctx

    sname = parts[0]

    acct_paths = (
        f"exec.{sname}.ACCT",
        f"states.{sname}.ACCT",
        f"tool.{sname}.ACCT",
        f"esm.{sname}.ACCT",
        f"source.{sname}.ACCT",
        f"{sname}.ACCT",
    )

    if acct_data is None:
        acct_data = {}
    # Read encrypted profiles from an acct_file or acct_blob
    if acct_key:
        if acct_file:
            async with aiofiles.open(acct_file, "rb") as fh:
                acct_blob = await fh.read()
        if acct_blob:
            if acct_key:
                new_data = await hub.acct.init.unlock_blob(
                    acct_blob, acct_key=acct_key, hard_fail=hard_fail
                )
                acct_data.update(new_data)
    # read plaintext credentials from the acct_file
    elif acct_file:
        if "profiles" not in acct_data:
            acct_data["profiles"] = {}

        new_data = await hub.acct.init.profiles(acct_file, hard_fail=hard_fail)
        acct_data["profiles"].update(new_data)

    subs = set()
    for name in acct_paths:
        sub = getattr(hub, name, None)
        if not sub:
            continue
        if isinstance(sub, Iterable):
            subs.update(sub)

    acct = await hub.acct.init.gather(
        subs,
        profile,
        profiles=acct_data.get("profiles", {}),
        hard_fail=hard_fail,
    )

    if validate and profile and subs and not acct:
        # Validate that the specified acct_profile is specified is within the profiles
        profiles = set()
        for s in subs:
            profiles.update(acct_data.get("profiles", {}).get(s, {}).keys())

        if not profiles:
            raise ConnectionError(f"No profiles found for '{path}'")
        if profile not in profiles:
            raise ConnectionError(
                f"Could not find '{path}' profile '{profile}' in: {', '.join(profiles)}"
            )

    # The SafeNamespaceDict will not print its values, only keys
    ctx.acct = dict_tools.data.SafeNamespaceDict(acct)

    # Get metadata for the profile
    ctx.acct_details = await hub.acct.metadata.init.gather(
        profile=acct,
        providers=subs,
    )

    return ctx


async def data(hub, acct_key: str, acct_file: str, acct_blob: bytes) -> Dict[str, Any]:
    """
    Return a raw dictionary with all the profiles from an encrypted acct
    """
    acct_data = {}
    if acct_file:
        async with aiofiles.open(acct_file, "rb") as fh:
            acct_blob = await fh.read()
    if acct_blob:
        if acct_key:
            acct_data = await hub.acct.init.unlock_blob(acct_blob, acct_key=acct_key)
        else:
            if "profiles" not in acct_data:
                acct_data["profiles"] = {}
            acct_data["profiles"].update(await hub.acct.init.profiles(acct_file))
    return acct_data
