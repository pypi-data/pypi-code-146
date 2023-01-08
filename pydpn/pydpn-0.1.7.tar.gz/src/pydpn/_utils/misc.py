from typing import Any
from re import match


def valid_ip(ip: str) -> bool:
    """check for a valid ipV4 input

    Args:
        ip (str): ip string

    Returns:
        bool: result
    """

    res = match(
        "^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$",
        ip,
    )
    if res:
        return True

    else:
        return False


def cut_slash(text):

    if text[-1] == "/":
        return text[:-1]

    else:
        return text


def pick(inDict: dict, key: str, defaultRet: Any = None) -> Any:

    if isinstance(inDict, dict):
        if key in inDict.keys():
            return inDict[key]

    return defaultRet
