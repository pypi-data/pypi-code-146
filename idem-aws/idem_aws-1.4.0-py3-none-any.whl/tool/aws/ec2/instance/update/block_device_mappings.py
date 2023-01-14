from typing import Dict
from typing import List


async def apply(
    hub,
    ctx,
    resource,
    *,
    old_value: List[Dict[str, str]],
    new_value: List[Dict[str, str]],
    comments: List[str],
) -> bool:
    """
    This attribute can only be modified on creation of an instance
    """
    return True
