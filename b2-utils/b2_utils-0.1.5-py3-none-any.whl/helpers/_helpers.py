import random

__all__ = [
    "random_hex_color",
    "get_nested_attr",
]


def random_hex_color(min=0x000000, max=0xFFFFFF) -> str:
    """Returns a random hexadecimal color in range [min, max], including both end points.

    Parameters
    ---------
    min : int
        Minimum value for color (default 0x000000)
    max : int
        Maximum value for color (default 0xFFFFFF)

    Returns
    -------
    str
        A random color "#XXXXXX" that is between min and max values.
    """

    return "#%06x".upper() % random.randint(min, max)


def get_nested_attr(obj: any, path: str, raise_exception=False, default=None):
    """Gets nested object attributes, raising exceptions only when specified.

    Parameters
    ---------
    obj : any
        The object which attributes will be obtained
    path : str
        Attribute path separated with dots ('.') as usual
    raise_exception : bool = False
        If this value sets to True, an exception will be raised if an attribute cannot
        be obtained, even if default value is specified
    default : any = None
        A default value that's returned if the attribute can't be obtained. This
        parameter is ignored if raise_exception=True

    Returns
    -------
    any
        Attribute value or default value specified if any error occours while trying
        to get object attribute
    """

    for path_attr in path.split("."):
        if raise_exception:
            obj = getattr(obj, path_attr)
        else:
            obj = getattr(obj, path_attr, default)

    return obj
