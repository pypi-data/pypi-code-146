from __future__ import annotations

import collections.abc
import dataclasses
import enum
from datetime import date, datetime, timezone
from typing import TYPE_CHECKING, Any, List, Type, Union, cast, get_type_hints

import cattrs
import pendulum
import pyarrow
import pyarrow as pa
import pydantic
import pytz
from dateutil import parser
from pendulum.tz.timezone import Timezone
from pydantic import BaseModel
from pydantic.fields import ModelField
from typing_extensions import get_args, get_origin

from chalk.serialization.parsed_annotation import ParsedAnnotation
from chalk.streams import Windowed
from chalk.utils.enum import get_enum_value_type
from chalk.utils.log_with_context import get_logger
from chalk.utils.missing_dependency import missing_dependency_exception

if TYPE_CHECKING:
    import polars as pl

    from chalk.features import Feature

try:
    import attrs
except ImportError:
    # Imports not available. Attrs is not required.
    attrs = None

try:
    import pandas as pd
except ImportError:
    pd = None

try:
    import numpy as np
except ImportError:
    np = None

_log = get_logger(__name__)

_NoneType = type(None)


def _unwrap_optional_if_needed(typ: Any):
    if get_origin(typ) == Union and len(get_args(typ)) == 2:
        has_none = any(d == _NoneType for d in get_args(typ))
        if has_none:
            return next(m for m in get_args(typ) if m != _NoneType)

    return typ


def is_numeric(dtype: Union[pl.DataType, Type[pl.DataType]]) -> bool:
    # This function is used only by the engine
    import polars as pl

    return dtype in (
        pl.Float32,
        pl.Float64,
        pl.Int16,
        pl.Int8,
        pl.Int32,
        pl.Int64,
        pl.UInt8,
        pl.UInt16,
        pl.UInt32,
        pl.UInt64,
    )


def _is_namedtuple(value: Any, annotated: bool = False) -> bool:
    """Infer whether value is a NamedTuple."""
    # From https://github.com/pola-rs/polars/blob/5f3e332fb2a653064f083b02949c527e0ec0afda/py-polars/polars/internals/construction.py#L78
    if all(hasattr(value, attr) for attr in ("_fields", "_field_defaults", "_replace")):
        return len(value.__annotations__) == len(value._fields) if annotated else True
    return False


class FeatureCodec:
    def __init__(self):
        self.converter = cattrs.Converter()
        self.converter.register_structure_hook(datetime, lambda v, _: parser.isoparse(v))
        self.converter.register_unstructure_hook(
            datetime,
            lambda v: (
                cast(datetime, v) if cast(datetime, v).tzinfo else pytz.utc.localize(cast(datetime, v))
            ).isoformat(),
        )

    def _default_encode(self, value: Any):
        if isinstance(value, set):
            return {self._default_encode(x) for x in value}
        if isinstance(value, list):
            return [self._default_encode(x) for x in value]
        if isinstance(value, (str, int, float)):
            return value
        if isinstance(value, enum.Enum):
            return self._default_encode(value.value)
        if isinstance(value, datetime):
            tz = value.tzinfo or (datetime.now(timezone.utc).astimezone().tzinfo)
            assert tz is not None
            return pendulum.instance(value, cast(Timezone, tz)).isoformat()
        if isinstance(value, date):
            return value.isoformat()
        if np is not None and isinstance(value, np.integer):
            return int(value)
        if np is not None and isinstance(value, np.floating):
            return float(value)
        if pd is not None and isinstance(value, pd.Timestamp):
            return pendulum.instance(value.to_pydatetime()).isoformat()
        if isinstance(value, pydantic.BaseModel):
            return value.dict()
        if (attrs is not None and attrs.has(type(value))) or dataclasses.is_dataclass(value):
            return self.converter.unstructure(value)
        if isinstance(value, collections.abc.Iterable):
            return [self._default_encode(x) for x in value]
        raise TypeError(f"Unable to encode value of type {type(value).__name__}")

    def encode(
        self,
        feature: Feature,
        value: Any,
    ):
        if value is None:
            return None

        if feature.encoder is not None:
            return feature.encoder(value)

        return self._default_encode(value)

    def encode_fqn(self, fqn: str, value: Any):
        from chalk.features import Feature

        return self.encode(Feature.from_root_fqn(fqn), value)

    def _to_polars_struct(self, fqn: str, value: BaseModel):
        try:
            import polars as pl
        except ImportError:
            raise missing_dependency_exception("chalkpy[polars]")

        return pl.DataFrame(
            data={
                field.alias or field.name: [getattr(value, field.alias or field.name)]
                for field in value.__fields__.values()
            },
            columns={
                field.alias
                or field.name: self._pa_to_pl(self._get_pa_dtype_for_type(field.type_, field.alias or field.name))
                for field in value.__fields__.values()
            },
        ).to_struct(fqn)

    def _default_decode_value(
        self,
        feature: Feature,
        value: Any,
    ):
        assert feature.typ is not None
        if isinstance(value, feature.typ.underlying):
            return value
        if issubclass(feature.typ.underlying, enum.Enum):
            value = feature.typ.underlying(value)
        if issubclass(feature.typ.underlying, datetime):
            value = parser.isoparse(value)
        elif issubclass(feature.typ.underlying, date):
            # note: datetime is a subclass of date, so we must be careful to decode accordingly
            value = date.fromisoformat(value)
        if issubclass(feature.typ.underlying, pydantic.BaseModel):
            return feature.typ.underlying(**value)
        elif (attrs is not None and attrs.has(feature.typ.underlying)) or dataclasses.is_dataclass(
            feature.typ.underlying
        ):
            return self.converter.structure(value, feature.typ.underlying)
        if not isinstance(value, feature.typ.underlying):
            raise TypeError(
                f"Unable to decode value {value} to type {feature.typ.underlying.__name__} for '{feature.root_fqn}'"
            )
        return value

    def _default_decode(
        self,
        feature: Feature,
        value: Any,
    ):
        assert feature.typ is not None
        if value is None:
            if feature.typ.is_nullable:
                return None
            else:
                raise ValueError(f"Value is none but feature {feature} is not nullable")
        if feature.typ.collection_type is not None and get_origin(feature.typ.collection_type) == set:
            if not isinstance(value, set):
                raise TypeError(f"Feature {feature} is a set but value {value} is not")
            return {self._default_decode_value(feature, x) for x in value}
        elif feature.typ.collection_type is not None and get_origin(feature.typ.collection_type) == list:
            if not isinstance(value, list):
                raise TypeError(f"Feature {feature} is a list but value {value} is not")
            return [self._default_decode_value(feature, x) for x in value]
        else:
            return self._default_decode_value(feature, value)

    def decode(
        self,
        feature: Feature,
        value: Any,
    ):
        if value is None:
            return None

        if feature.decoder is not None:
            return feature.decoder(value)

        return self._default_decode(feature, value)

    def decode_fqn(
        self,
        fqn: str,
        value: Any,
    ):
        from chalk.features import Feature

        try:
            f = Feature.from_root_fqn(fqn)
        except:
            return value

        return self.decode(f, value)

    def get_pandas_dtype(self, fqn: str) -> str:
        from chalk.features import Feature

        feature = Feature.from_root_fqn(fqn)
        typ = feature.typ
        assert typ is not None, "typ should be specified"
        underlying = typ.underlying
        if issubclass(underlying, enum.Enum):
            # For enums, require all members to have the same type
            underlying = get_enum_value_type(underlying)
        # See https://pandas.pydata.org/docs/user_guide/basics.html#basics-dtypes
        if issubclass(underlying, str):
            return "string"
        if issubclass(underlying, bool):
            return "boolean"
        if issubclass(underlying, int):
            return "Int64"
        if issubclass(underlying, float):
            return "Float64"
        if issubclass(underlying, datetime):
            # This assumes timezone-aware. For timezone-unaware the `pandas_dtype` must be set directly on the Feature
            return "datetime64[ns, utc]"
        _log.info(
            f"Defaulting to pandas type 'object' for fqn {fqn} of type {typ.underlying.__name__}. Set the `pandas_dtype` attribute for better specificity."
        )
        return "object"

    def get_polars_dtype(self, fqn: str) -> Union[pl.DataType, Type[pl.DataType]]:
        try:
            import polars as pl
        except ImportError:
            raise missing_dependency_exception("chalkpy[polars]")

        # BEGIN This should be replaced with a structification
        from chalk.features import Feature

        feature = Feature.from_root_fqn(fqn)
        # END structification workaround

        if feature.is_has_one or feature.is_has_many:
            return pl.Object
        pa_type = self.get_pyarrow_dtype(fqn)

        try:
            return self._pa_to_pl(pa_type)
        except Exception as exc:
            raise ValueError(
                f"Failed to determined type for feature {fqn}. Please set the pyarrow_dtype attribute directly."
            ) from exc

    def _pa_to_pl(self, pa_type: pa.DataType) -> Union[pl.DataType, Type[pl.DataType]]:
        try:
            import polars as pl
        except ImportError:
            raise missing_dependency_exception("chalkpy[polars]")

        """May throw"""
        # polars coerces pa.Date to pl.DateTime
        if pa_type == pa.date64():
            return pl.Date

        # To convert the dtypes, we'll create an empty pyarrow table, and then convert that to polars, and get the dtype
        pa_table = pa.Table.from_arrays(arrays=[[]], schema=pa.schema(fields={"col": pa_type}))

        df = pl.from_arrow(pa_table)
        assert isinstance(df, pl.DataFrame)
        return df.dtypes[0]

    def get_pyarrow_dtype(self, fqn: str) -> pa.DataType:
        from chalk.features import Feature

        feature = Feature.from_root_fqn(fqn)
        if feature.pyarrow_dtype is not None:
            return feature.pyarrow_dtype
        typ = feature.typ
        assert typ is not None, "typ should be specified"
        underlying = typ.underlying
        dtype = self._get_pa_dtype_for_type(underlying, fqn)
        if typ.collection_type is not None:
            dtype = pa.list_(dtype)
        return dtype

    def _get_pa_dtype_for_type(self, underlying: type | Windowed, fqn: str) -> pa.DataType:
        # Polars seems to allow optional for any dtype, so we ignore it when computing dtypes
        underlying = _unwrap_optional_if_needed(underlying)
        if isinstance(underlying, Windowed):
            # If the parent window feature appears in a dataframe, then it's likely in a streaming resolver
            # Use the underlying type for that windowed feature
            return self._get_pa_dtype_for_type(underlying._kind, fqn)
        if issubclass(underlying, enum.Enum):
            # For enums, require all members to have the same type
            underlying = get_enum_value_type(underlying)
        if issubclass(underlying, str):
            return pa.string()
        if issubclass(underlying, bool):
            return pa.bool_()
        if issubclass(underlying, int):
            return pa.int64()
        if issubclass(underlying, float):
            return pa.float64()
        if issubclass(underlying, datetime):
            return pa.timestamp("us", "UTC")
        if issubclass(underlying, date):
            return pa.date64()
        if dataclasses.is_dataclass(underlying) or _is_namedtuple(underlying, annotated=True):
            annotations = get_type_hints(underlying)
            fields: List[pa.Field] = []
            for field_name, type_annotation in annotations.items():
                parsed_annotation = ParsedAnnotation(underlying=type_annotation)
                if not parsed_annotation.is_scalar:
                    raise TypeError(f"{fqn} cannot be another Features class ")
                underlying_dtype = self._get_pa_dtype_for_type(parsed_annotation.underlying, f"{fqn}.{field_name}")
                if parsed_annotation.collection_type is None:
                    fields.append(
                        pa.field(
                            field_name,
                            underlying_dtype,
                        )
                    )
                else:
                    fields.append(pa.field(field_name, pa.list_(underlying_dtype)))
            return pa.struct(fields)
        if issubclass(underlying, BaseModel):
            fields: List[pa.Field] = []

            field: ModelField
            for field in underlying.__fields__.values():
                field_name = field.alias if field.alias is not None else field.name
                fields.append(
                    pyarrow.field(
                        metadata={"chalk_field_name": field.name},
                        name=field_name,
                        nullable=field.allow_none,  # noqa
                        # abusing fqn here
                        type=self._get_pa_dtype_for_type(field.type_, f"{fqn}.{field_name}"),
                    )
                )

            return pa.struct(fields)

        raise ValueError(
            f"Unable to determine the PyArrow type for feature {underlying.__name__}. Please set the `pyarrow_dtype` attribute."
        )


FEATURE_CODEC = FeatureCodec()
