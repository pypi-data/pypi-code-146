import re
from typing import List


def to_snake_case(name: str):
    name = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", name)
    name = re.sub("__([A-Z])", r"_\1", name)
    name = re.sub("([a-z0-9])([A-Z])", r"\1_\2", name)
    return name.lower()


def removeprefix(text: str, prefix: str):
    """
    This functionality is available in Python 3.9 as text.removeprefix(prefix),
    but we're supporting down to 3.8, where it is not available.
    """
    return text[len(prefix) :] if text.startswith(prefix) else text


def comma_whitespace_split(value: str):
    return re.split(r"\s*,\s*", value)


def normalize_string_for_matching(name: str) -> str:
    """
    1. Case-insensitive
    2. Strip everything except alphanumeric or periods, so e.g. `first_name` matches `firstname`
    """
    return re.sub(r"[^0-9a-z\.]", "", name.lower())


def to_camel_case(snake_str: str):
    components = [c for c in snake_str.split("_") if c != ""]
    return components[0].lower() + "".join(x.title() for x in components[1:])


def to_title_case(snake_str: str):
    cameled = to_camel_case(snake_str)
    return cameled[0].upper() + cameled[1:] if len(cameled) > 0 else cameled


def oxford_comma_list(lst: List[str]) -> str:
    if len(lst) == 0:
        return ""
    elif len(lst) == 1:
        return lst[0]
    elif len(lst) == 2:
        return f"{lst[0]} and {lst[1]}"

    return ", ".join(lst[:-1]) + f", and {lst[-1]}"
