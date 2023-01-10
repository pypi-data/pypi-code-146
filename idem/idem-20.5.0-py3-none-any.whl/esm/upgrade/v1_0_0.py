from typing import Any
from typing import Dict
from typing import Tuple


def previous_version(hub) -> Tuple[int, int, int]:
    return 0, 0, 0


def apply(hub, esm_cache: Dict[str, Any]) -> Dict[str, Any]:
    """
    Upgrade from esm version 0.0.0 to 1.0.0
    """
    # Get the metadata from the esm file cache
    metadata = esm_cache[hub.idem.managed.ESM_METADATA_KEY]

    # Modify the esm_version in the metadata
    metadata["version"] = (1, 0, 0)

    # Apply the change to the esm file cache
    esm_cache[hub.idem.managed.ESM_METADATA_KEY] = metadata

    return esm_cache
