from __future__ import annotations

import typing as t

import pandas as pd
import pyarrow as pa

from sarus_data_spec.constants import DATA, PUBLIC, USER_COLUMN, WEIGHTS
import sarus_data_spec.protobuf as sp
import sarus_data_spec.typing as st


class ExternalOpImplementation:
    """External PEP op implementation class.

    This class wraps together several elements of an external op
    implementation:
        - `data_fn` is the function that computes the output value from the
          input(s) value(s).
    """

    def __init__(
        self,
        data_fn: t.Callable,
        dp_equivalent: t.Optional[DPImplementation] = None,
        transform_id: t.Optional[str] = None,
    ):
        self.data_fn = data_fn
        self._dp_equivalent = dp_equivalent
        self.transform_id = transform_id

    def is_pep_transform(self) -> bool:
        return False

    def is_dp_transform(self) -> bool:
        return False

    def dp_equivalent(self) -> t.Optional[DPImplementation]:
        return self._dp_equivalent


class PEPImplementation(ExternalOpImplementation):
    """External PEP op implementation class.

    This class wraps together several elements of an external op
    implementation `data_fn` is the function that computes the output value
    from the input(s) value(s).

    The `allowed_pep_args` is a list of combinations of arguments' names which
    are managed by the Op. The result of the Op will be PEP only if the set of
    PEP arguments passed to the Op are in this list.

    For instance, if we have an op that takes 3 arguments `a`, `b` and `c` and
    the `allowed_pep_args` are [{'a'}, {'b'}, {'a','b'}] then the following
    combinations will yield a PEP output:
        - `a` is a PEP dataspec, `b` and `c` are either not dataspecs or public
          dataspecs
        - `b` is a PEP dataspec, `a` and `c` are either not dataspecs or public
          dataspecs
        - `a` and `b` are PEP dataspecs, `c` is either not a dataspec or a
          public dataspec

    The `is_token_preserving` attribute is a function that takes as input the
    non-evaluated arguments and returns a boolean of whether the PEP output
    token is the same as the PEP input token. An Op that changes the number or
    order of the rows is not token preserving.
    """

    def __init__(
        self,
        data_fn: t.Callable,
        allowed_pep_args: t.List[t.Set[str]],
        is_token_preserving: t.Optional[t.Callable[..., bool]] = None,
    ):
        super().__init__(data_fn)
        self.allowed_pep_args = allowed_pep_args
        if is_token_preserving is None:
            self.is_token_preserving = lambda *args, **kwargs: False
        else:
            self.is_token_preserving = is_token_preserving

    def is_pep_transform(self) -> bool:
        return True


class DPImplementation(ExternalOpImplementation):
    def __init__(
        self,
        data_fn: t.Callable,
        allowed_pep_args: t.List[t.Set[str]],
    ):
        super().__init__(data_fn)
        self.allowed_pep_args = allowed_pep_args

    def is_dp_transform(self) -> bool:
        return True


def dp_transform(allowed_pep_args: t.List[t.Set[str]]) -> t.Callable:
    """Parametrizable decorator to create a DP external implementation."""

    def external_op_builder(data_fn: t.Callable) -> DPImplementation:
        return DPImplementation(
            data_fn=data_fn,
            allowed_pep_args=allowed_pep_args,
        )

    return external_op_builder


def dp_equivalent(dp_transform_id: str) -> t.Callable:
    """Parametrizable decorator to link a DP implementation."""

    def external_op_builder(data_fn: t.Callable) -> ExternalOpImplementation:
        from .external_op import transform_implementation

        try:
            external_implementation = transform_implementation(dp_transform_id)
            dp_implementation = t.cast(
                DPImplementation, external_implementation
            )
        except AttributeError:
            # TODO clean this exception when merging new ops formalism
            dp_implementation = t.cast(DPImplementation, None)

        return ExternalOpImplementation(
            data_fn=data_fn,
            dp_equivalent=dp_implementation,
        )

    return external_op_builder


def pep_transform(
    allowed_pep_args: t.List[t.Set[str]] = [],
    is_token_preserving: bool = False,
) -> t.Callable:
    """Parametrizable decorator to create a PEP external implementation."""

    def external_op_builder(data_fn: t.Callable) -> PEPImplementation:

        is_token_preserving_fn: t.Optional[t.Callable] = None
        if is_token_preserving:

            def is_token_preserving_fn(*args: t.Any, **kwargs: t.Any) -> bool:
                return True

        return PEPImplementation(
            data_fn=data_fn,
            allowed_pep_args=allowed_pep_args,
            is_token_preserving=is_token_preserving_fn,
        )

    return external_op_builder


async def extract_data_from_pe(
    x: t.Union[t.Any, st.DataSpec]
) -> t.Tuple[t.Any, t.Optional[pd.DataFrame]]:
    """Compute the value of a DataSpec and extract its PE.

    Return None for the PE if it is not defined for the argument.
    """
    if not isinstance(x, st.DataSpec):
        return x, None
    if x.prototype() == sp.Dataset:
        dataset = t.cast(st.Dataset, x)
        raw_data = await dataset.async_to_pandas()
        return pandas_extract_pe(raw_data)
    else:
        scalar = t.cast(st.Scalar, x)
        return await scalar.async_value(), None


def pandas_extract_pe(
    raw_data: pd.DataFrame,
) -> t.Tuple[pd.DataFrame, t.Optional[pd.DataFrame]]:
    """Extract the protected entity from a pd.DataFrame.

    Return None for the PE is no PE is found on the DataFrame.
    """
    # TODO use `dataset.is_protected()` but we need the schema
    # for that, and it is not yet available in the SDK
    is_protected = set(raw_data.columns) == {
        PUBLIC,
        USER_COLUMN,
        WEIGHTS,
        DATA,
    }
    if is_protected:
        data = pd.DataFrame.from_records(
            raw_data[DATA].values, index=raw_data.index
        )
        pe = raw_data[[PUBLIC, USER_COLUMN, WEIGHTS]]
    else:
        data = raw_data
        pe = None
    return data, pe


def pandas_merge_pe(
    data: pd.DataFrame, pe: t.Optional[pd.DataFrame]
) -> pa.Table:
    """Merge a protection and its data in pandas.

    NB: we return directly the pa.Table otherwise the data column order is lost
    when doing pa.Table.from_pandas(df).to_pandas(). Another solution to
    preserve the column order would be to also return the Table schema and pass
    it as argument to pa.Table.from_pandas(df, schema)
    """
    if pe is not None:
        # Work with Arrow to preserve column order (vs Python dict)
        pe_table = pa.Table.from_pandas(pe)
        data_table = pa.Table.from_pandas(data)
        data_arrays = [
            chunked_array.combine_chunks()
            for chunked_array in data_table.columns
        ]
        data_array = pa.StructArray.from_arrays(
            data_arrays, names=data_table.column_names
        )
        result = pe_table.append_column(DATA, data_array)
    else:
        # TODO also wrap the data in an empty protection
        result = pa.Table.from_pandas(data)
    return result
