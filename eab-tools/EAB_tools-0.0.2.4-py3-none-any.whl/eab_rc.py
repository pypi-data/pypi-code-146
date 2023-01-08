"""Default values used throughout the package."""

from collections import defaultdict
from typing import Any

eab_rc: defaultdict[str, Any] = defaultdict(
    default_factory=lambda: None,  # By default, return None
    hash_len=7,  # Optional[int]
)
