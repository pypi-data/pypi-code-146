from fa_purity.maybe import (
    Maybe,
)
from fa_purity.utils import (
    raise_exception,
)
from redshift_client.data_type.alias import (
    NON_STC_ALIAS_MAP,
    STC_ALIAS_MAP,
)
from redshift_client.data_type.core import (
    DataType,
    DecimalType,
    NonStcDataTypes,
    PrecisionType,
    PrecisionTypes,
    ScaleTypes,
    StaticTypes,
)
from typing import (
    Callable,
    TypeVar,
)

_T = TypeVar("_T")
_R = TypeVar("_R")


def _get_enum(cast: Callable[[_T], _R], val: _T) -> Maybe[_R]:
    try:
        return Maybe.from_value(cast(val))
    except ValueError:
        return Maybe.empty()


def decode_type(
    raw: str, precision: Maybe[int], scale: Maybe[int]
) -> DataType:
    _raw = raw.upper()
    dtype: Maybe[DataType] = Maybe.from_optional(STC_ALIAS_MAP.get(_raw)).lash(
        lambda: _get_enum(StaticTypes, _raw).map(DataType)
    )
    if dtype.value_or(None):
        return dtype.unwrap()
    incomplete_type: NonStcDataTypes = (
        Maybe.from_optional(NON_STC_ALIAS_MAP.get(_raw))
        .lash(lambda: _get_enum(PrecisionTypes, _raw).map(NonStcDataTypes))
        .lash(lambda: _get_enum(ScaleTypes, _raw).map(NonStcDataTypes))
        .or_else_call(
            lambda: raise_exception(ValueError(f"Unknown data type: {_raw}"))
        )
    )
    if isinstance(incomplete_type.value, PrecisionTypes):
        p_result = PrecisionType(incomplete_type.value, precision.unwrap())
        return DataType(p_result)
    d_result = DecimalType(precision.unwrap(), scale.unwrap())
    return DataType(d_result)
