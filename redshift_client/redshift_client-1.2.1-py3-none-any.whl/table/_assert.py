from fa_purity.frozen import (
    FrozenList,
)
from fa_purity.maybe import (
    Maybe,
)
from fa_purity.result import (
    Result,
    ResultE,
)
from fa_purity.utils import (
    raise_exception,
)
from redshift_client.column import (
    Column,
    ColumnId,
)
from redshift_client.data_type.decode import (
    decode_type,
)
from redshift_client.sql_client import (
    PrimitiveVal,
)
from typing import (
    Optional,
    Tuple,
)


def _assert_opt_int(val: PrimitiveVal) -> ResultE[Optional[int]]:
    if isinstance(val, (int, str)):
        try:
            return Result.success(int(val))
        except ValueError as err:
            return Result.failure(err)
    if val is None:
        return Result.success(None)
    return Result.failure(ValueError("not a int|str"))


def to_column(raw: FrozenList[PrimitiveVal]) -> Tuple[ColumnId, Column]:
    col = Column(
        decode_type(
            str(raw[2]),
            Maybe.from_optional(
                _assert_opt_int(raw[3]).alt(raise_exception).unwrap()
            ),
            Maybe.from_optional(
                _assert_opt_int(raw[4]).alt(raise_exception).unwrap()
            ),
        ),
        str(raw[5]).upper() == "YES",
        raw[6],
    )
    return (ColumnId(str(raw[1])), col)
