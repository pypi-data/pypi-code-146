import gc
import os
import math
import time

# need __version__, is there a better way than importing the whole package?
import remotemanager


def ensure_list(inp=None) -> list:
    """
    Ensure that `inp` is list-type

    Args:
        inp:
            list, string, object to be processed

    Returns (list):
        Either inserts the object into a list, or returns the list-like inp
    """
    if inp is None:
        return []
    elif isinstance(inp, (list, tuple, set)):
        return list(inp)
    elif isinstance(inp, str):
        return [inp]
    return list(inp)


def ensure_filetype(file, target_type):
    """
    Ensure that `file` is of type `type`

    Args:
        file (str):
            filename
        target_type (str):
            filetype to enforce

    Returns (str):
        filename of type `type`
    """
    fname, ftype = os.path.splitext(file)

    target_type = target_type.strip('.')

    return f'{fname}.{target_type}'


def ensure_dir(dir):
    """
    Ensure that string path to `dir` is correctly formatted
    ONLY ensures that the folder name ends with a "/", does not produce an
    abspath

    Args:
        dir (str):
            path to dir

    Returns (str):
        ensured dir path
    """
    if not isinstance(dir, str):
        dir = str(dir)

    return os.path.join(dir, ' ').strip()


def safe_divide(a: [float, int],
                b: [float, int]) -> [float, int]:
    """
    Always-fit division. Rounds up after division, returns >= 1

    Args:
        a (num):
            numerator
        b (num):
            denominator

    Returns:
        result of a/b division, unless result returns <1, else 1
    """
    if b == 0:
        return 1
    r = math.ceil(a / b)
    return max(r, 1)


def get_version() -> str:
    """
    Gets the current package version from __init__.py
    """
    return remotemanager.__version__


def recursive_dict_update(d1: dict,
                          d2: dict) -> dict:
    """
    Update d1 with all the keys of d2

    Args:
        d1 (dict):
            dictionary to be updated
        d2 (dict):
            dictionary to update with

    Returns (dict):
        updated d1
    """
    if not isinstance(d1, dict):
        return d2

    for k, v in d2.items():
        if isinstance(v, dict) and k in d1:
            d1[k] = recursive_dict_update(d1[k], d2[k])
        else:
            d1[k] = v

    return d1


def reverse_index(inplist: list,
                  term):
    """
    return index of last occurrence of `term` in `inplist`

    Args:
        inplist (list):
            list to index
        term:
            object to index

    Returns (int):
        forward index of item
    """
    return len(inplist) - inplist[::-1].index(term) - 1


def integer_time_wait(offset: float = 0.0) -> None:
    """
    wait for an integer unix time + offset

    This function exists to increase the reproducibility of the tests

    Args:
        offset (float):
            extra offset to wait for
    """

    t0 = time.time()

    wait = 1 - math.fmod(t0, 1)

    time.sleep(wait + offset)

    return None


def object_from_uuid(uuid: str, name: str):
    """
    Search the memory heap for an object of uuid `uuid` and classname
    `name`

    for example;

    >>> recovered_dataset = object_from_uuid('<uuid>', 'Dataset')

    Args:
        uuid:
            uuid target
        name:
            classname to search for

    Returns:
        object instance matching input, if it exists
    """

    for obj in gc.get_objects():
        try:
            if obj.__class__.__name__ == name:
                if obj.uuid == uuid:
                    return obj
        except AttributeError:
            pass

    raise ValueError(
        f'could not find {object} in memory with UUID {uuid}')
