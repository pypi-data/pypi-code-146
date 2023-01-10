"""
This file contains routines to get sls files from references
"""
import pathlib
import re
from typing import Any
from typing import Dict
from typing import List
from typing import Tuple

SOURCE_PATTERN = re.compile(
    r"^(?P<protocol_plugin>(?P<protocol>\w+)[\+\w+]*)://(?:(?P<profile>[-.\w]+)@)?(?P<data>.+)$"
)


def parse_source(hub, source: str) -> Tuple[str, str, str, str]:
    match = SOURCE_PATTERN.match(source)
    if not match:
        raise ValueError(f"SLS source is not a valid pattern: {source}")
    protocol = match.group("protocol")
    protocol_plugin = match.group("protocol_plugin")
    acct_profile = match.group("profile")
    data = match.group("data")
    return protocol, protocol_plugin, acct_profile, data


async def ref(hub, name: str, sls: str, sources: List[str]) -> Dict[str, Any]:
    """
    Cache the given file from the named reference point

    :param hub:
    :param name: The state run name
    :param sls: an SLS location within the given sources
    :param sources: sls-sources or params-sources

    :returns A file_name/identifier and encoded yaml content

    If the sls sources uses `acct` for authentication, then a profile is specified as part of the sls_source

    .. code-block::

        [proto]://[acct_profile]@[path]
    """
    acct_data = hub.idem.RUNS[name]["acct_data"]
    original_sls = sls

    # Find the total possible number of parent directories in this source
    possible_parents = 0
    contexts = {}
    datas = {}
    protocol = None
    protocol_plugin = None
    for source in sources:
        try:
            possibly_greater = len(re.split(r"[./\\]", source.split("://")[1]))
        except IndexError:
            continue
        if possibly_greater > possible_parents:
            possible_parents = possibly_greater

            # Save the context for this source
            protocol, protocol_plugin, acct_profile, data = hub.idem.get.parse_source(
                source
            )
            if not acct_profile:
                acct_profile = "default"
            datas[source] = data
            contexts[source] = await hub.idem.acct.ctx(
                protocol_plugin,
                profile=acct_profile,
                acct_data=acct_data,
            )

    # After each failure, imply a deeper level of relative parent
    for _ in range(possible_parents):
        # Search for the sls ref in each source (in the order the sources were defined) and return the first match
        for source in sources:
            try:
                ctx = contexts[source]
                data = datas[source]
            except KeyError:
                continue

            locs = hub.idem.get.locations(sls)

            # Try each possible location until we resolve the sls ref
            for location, actual_ref in locs:
                hub.log.debug(f"Trying to find ref '{actual_ref}' in '{location}'")
                processed_location, cache_data = await hub.source[
                    protocol_plugin
                ].cache(ctx, protocol=protocol, source=data, location=location)
                if cache_data:
                    # The reference was found and contained valid data
                    hub.log.debug(f"Found ref '{actual_ref}' in '{processed_location}'")
                    return {
                        "location": processed_location,
                        "sls": actual_ref,
                        "content": cache_data,
                    }
        # Try again with a relative source
        sls = f".{sls}"
    else:
        raise LookupError(f"Could not find SLS ref '{original_sls}' in sources")


def locations(hub, sls: str) -> List[Tuple[str, str]]:
    """
    Translate an sls ref into all possible posix-style and nt-style locations
    """
    # Try both posix and windows paths as the sls may be not be on the local filesystem
    de_normalize_ref = hub.idem.sls_source.init.de_normalize(sls)
    posix_path = pathlib.PurePosixPath(de_normalize_ref)
    nt_path = pathlib.PureWindowsPath(posix_path)

    return [
        # Append ".sls" to the tried paths
        (f"{posix_path}.sls", sls),
        (f"{nt_path}.sls", sls),
        # Append "init.sls" to the tried paths
        (str(posix_path.joinpath("init.sls")), f"{sls}.init"),
        (str(nt_path.joinpath("init.sls")), f"{sls}.init"),
        # Try the raw paths
        (str(posix_path), sls),
        (str(nt_path), sls),
        # try the de-normalized sls ref
        (de_normalize_ref, de_normalize_ref),
        (f"{de_normalize_ref}.init", f"{de_normalize_ref}.init"),
        # Try the unaltered sls
        (sls, sls),
        (f"{sls}.init", f"{sls}.init"),
    ]
