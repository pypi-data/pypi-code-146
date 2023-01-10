from typing import Any
from typing import Dict
from typing import Tuple


def sig_previous_version(hub) -> Tuple[int, int, int]:
    """
    Return the ESM version that this plugin upgrades from
    """


def sig_apply(hub, esm_cache: Dict[str, Any]) -> Dict[str, Any]:
    """
    Upgrade the esm_cache from the previous version to the new version
    """
