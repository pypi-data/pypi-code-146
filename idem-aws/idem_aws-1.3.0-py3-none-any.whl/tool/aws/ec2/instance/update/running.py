from typing import List


async def apply(
    hub, ctx, resource, *, old_value, new_value, comments: List[str]
) -> bool:
    """
    This is attribute is modified by the meta "init" function
    """
    return True
