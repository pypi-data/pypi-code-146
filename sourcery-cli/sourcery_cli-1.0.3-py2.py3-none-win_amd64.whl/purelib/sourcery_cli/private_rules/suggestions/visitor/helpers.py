import typing

from sourcery.ast import Constant, Name, Starred, Subscript
from sourcery.ast.nodes import Expression


def find_duplicate_key_indices(
    keys: typing.Tuple[typing.Optional[Expression], ...],
    values: typing.Tuple[Expression, ...],
) -> typing.List[int]:
    """Helper function to find duplicate keys in sets and dictionaries.

    Returns a list of integers containing the duplicate indices.

    For instance, for the set `{'a', 'b', 'a', 'c', 'b'}`, this function will return
    `[2, 4]`, since the elements in positions 2 ('a') and 4 ('b') are duplicates.


    Args:
        keys: the dictionary keys or the set elements (as in `d.keys` or `s.elts`)
        values: the dictionary values or the set elements (as in `d.values` or `s.elts`)
    """
    last_seen: typing.Dict[str, int] = {}
    redundant_indices: typing.List[int] = []
    for i, (k, v) in enumerate(zip(keys, values)):
        if k is None:
            # this is the case where we unpack dictionaries, as in `{**a, **b}`. The
            # key is `None`, and the value is `a` (or `b`).
            k = v

        if not isinstance(k, (Constant, Name, Subscript, Starred)):
            continue

        if isinstance(k, (Subscript, Starred)) and not isinstance(k.value, Name):
            continue

        key_str = k.unparse()

        if key_str in last_seen:
            redundant_indices.append(last_seen[key_str])

        last_seen[key_str] = i

    return redundant_indices
