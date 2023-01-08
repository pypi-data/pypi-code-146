from itertools import chain
from typing import Iterable, Optional, Type, Union

from ._typed_lists_ext import (
    BoolTypedList,
    FloatTypedList,
    IntTypedList,
    StringTypedList,
)

TYPE_MAPPING = {
    bool: BoolTypedList,
    float: FloatTypedList,
    int: IntTypedList,
    str: StringTypedList,
}


def TypedList(
    input: Optional[Union[Iterable, Type]], dtype: Optional[Type] = None
) -> Union[IntTypedList, FloatTypedList, StringTypedList]:
    """Create a typed list. Function name is capitalized to emulate a class.

    Allowed argument combinations:
        - input: iterable (non-empty), dtype: None (inferred from first element)
        - input: iterable, dtype: type (must match first element or be empty)
        - input: type, dtype: None (empty list of given type)

    Args:
        input: iterable or type
        dtype: type (optional)

    Returns:
        Union[BoolTypedList, IntTypedList, FloatTypedList, StringTypedList]

    """
    if isinstance(input, type):
        if input in TYPE_MAPPING:
            return TYPE_MAPPING[input]([])
        raise ValueError("Invalid type")
    elif isinstance(input, Iterable):
        # infer type from first element
        if dtype is None:
            _iter = iter(input)
            x = next(_iter)
            if type(x) in TYPE_MAPPING:
                return TYPE_MAPPING[type(x)](chain([x], _iter))
        elif dtype in TYPE_MAPPING:
            return TYPE_MAPPING[dtype](input)
    raise ValueError("Invalid input. Must be an iterable or a type")
