from typing import Any
from typing import Dict
from typing import Tuple


def previous_version(hub) -> Tuple[int, int, int]:
    ...


def apply(hub, esm_cache: Dict[str, Any]) -> Dict[str, Any]:
    """
    Upgrade the esm_cache from the previous version to the newest version
    """
    metadata = esm_cache[hub.idem.managed.ESM_METADATA_KEY]
    esm_version = tuple(metadata.get("version", (1, 0, 0)))

    # This is the base case for following the recursive upgrade call
    if esm_version == hub.esm.VERSION:
        hub.log.info(f"ESM cache version {esm_version} is supported by idem")
        # No work to do, the versions match
        return esm_cache

    for esm_upgrade_plugin in hub.esm.upgrade:
        prev_version = esm_upgrade_plugin.previous_version()
        if prev_version == esm_version:
            hub.log.info(f"Upgrading from ESM version {prev_version} to {esm_version}")
            esm_cache = esm_upgrade_plugin.apply(esm_cache)

            # Recursively upgrade to the next version as needed
            esm_cache = hub.esm.upgrade.init.apply(esm_cache)
            break
    else:
        # The break point of the for loop wasn't reached, throw an error
        old_version_str = ".".join(str(i) for i in esm_version)
        new_version_str = ".".join(str(i) for i in hub.esm.VERSION)
        raise RuntimeError(
            f"No ESM upgrade plugin for '{old_version_str}' to '{new_version_str}'"
        )

    return esm_cache
