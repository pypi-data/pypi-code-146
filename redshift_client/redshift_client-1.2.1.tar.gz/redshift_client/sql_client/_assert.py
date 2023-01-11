from fa_purity.frozen import (
    FrozenList,
)
from fa_purity.result import (
    ResultE,
)
from fa_purity.utils import (
    raise_exception,
)
from redshift_client.sql_client.primitive import (
    PrimitiveVal,
    to_list_of,
    to_prim_val,
)
from typing import (
    Callable,
    Optional,
    TypeVar,
)

_T = TypeVar("_T")
_R = TypeVar("_R")


def assert_fetch_one(
    result: Optional[_T],
) -> Optional[FrozenList[PrimitiveVal]]:
    if result is None:
        return result
    if isinstance(result, tuple):
        return to_list_of(result, to_prim_val).alt(raise_exception).unwrap()
    raise TypeError(f"Unexpected fetch_one result; got {type(result)}")


def assert_fetch_list(result: _T) -> FrozenList[FrozenList[PrimitiveVal]]:
    _assert: Callable[
        [_R], ResultE[FrozenList[PrimitiveVal]]
    ] = lambda l: to_list_of(l, to_prim_val)
    if isinstance(result, tuple):
        return to_list_of(result, _assert).alt(raise_exception).unwrap()
    raise TypeError(f"Unexpected fetch_all result; got {type(result)}")
