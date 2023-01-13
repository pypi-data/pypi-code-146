from typing import Union


def islevel_validator(lev: Union[str, int, float]) -> bool:
    """Numeric validation
    Checks whether a number or string passed as an argument can be converted to a number.

    Args:
        lev (Union[str, int, float]): Character to be checked

    Returns:
        bool: True if conversion is possible / False if conversion is not possible
    """
    if isinstance(lev, str):
        if not lev.isdigit():
            return False
    elif isinstance(lev, (int, float)):
        if lev < 0:
            return False
    else:
        return False

    return True
