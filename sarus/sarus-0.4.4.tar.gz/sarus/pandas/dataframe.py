from __future__ import annotations

import logging
from typing import Any, cast

import pandas as pd
import sarus_data_spec.protobuf as sp
import sarus_data_spec.typing as st

from sarus.dataspec_wrapper import DataSpecVariant, DataSpecWrapper
from sarus.utils import (
    create_op,
    register_ops,
    sarus_init,
    sarus_method,
    sarus_property,
)

logger = logging.getLogger(__name__)
from sarus.typing import SPECIAL_WRAPPER_ATTRIBUTES


class DataFrame(DataSpecWrapper[pd.DataFrame]):
    @sarus_init("pandas.PD_DATAFRAME")
    def __init__(
        self, data=None, index=None, columns=None, dtype=None, copy=None
    ):
        ...

    @sarus_method("std.SETITEM", inplace=True)
    def __setitem__(self, key, newvalue):
        ...

    @sarus_property("pandas.PD_COLUMNS")
    def columns(self):
        ...

    @sarus_property("pandas.PD_AXES")
    def axes(self):
        ...

    @sarus_property("pandas.PD_DTYPES")
    def dtypes(self):
        ...

    @sarus_property("pandas.PD_INDEX")
    def index(self):
        ...

    @sarus_property("pandas.PD_SHAPE")
    def shape(self):
        ...

    @sarus_property("pandas.PD_NDIM")
    def ndim(self):
        ...

    @sarus_property("pandas.PD_SIZE")
    def size(self):
        ...

    @sarus_property("pandas.PD_VALUES")
    def values(self):
        ...

    @property
    def loc(self) -> _SarusLocIndexer:
        return _SarusLocIndexer(self)

    @property
    def iloc(self) -> _SarusLocIndexer:
        return _SarusILocIndexer(self)

    def __getattr__(self, name):
        # Overload __getattr__ to enable indexing by column name
        if name in SPECIAL_WRAPPER_ATTRIBUTES:
            return super().__getattr__(name=name)

        if name in self.__sarus_eval__().columns:
            return self.loc[:, name]

        return super().__getattr__(name=name)

    def __setattr__(self, name: str, value: Any) -> None:
        # Overload __setattr__ to enable setting by column name
        if name in SPECIAL_WRAPPER_ATTRIBUTES:
            return super().__setattr__(name, value)

        if name in self.__sarus_eval__().columns:
            key = (slice(None, None), name)
            new_df = pd_set_loc(self, key, value)
            self._set_dataspec(new_df._dataspec)
            return

        return super().__setattr__(name, value)

    def copy(self, deep: bool = False) -> DataFrame:
        return DataFrame.from_dataspec(
            self.dataspec(kind=DataSpecVariant.USER_DEFINED)
        )


pd_loc = create_op("pandas.PD_LOC")
pd_iloc = create_op("pandas.PD_ILOC")
pd_set_loc = create_op("pandas.PD_SET_LOC")
pd_set_iloc = create_op("pandas.PD_SET_ILOC")


class _SarusLocIndexer:
    def __init__(self, df: DataFrame) -> None:
        self.df = df

    def __getitem__(self, key) -> DataFrame:
        return pd_loc(self.df, key)

    def __setitem__(self, key, newvalue) -> None:
        new_df = pd_set_loc(self.df, key, newvalue)
        self.df._set_dataspec(new_df._dataspec)


class _SarusILocIndexer:
    def __init__(self, df: DataFrame) -> None:
        self.df = df

    def __getitem__(self, key) -> DataFrame:
        return pd_iloc(self.df, key)

    def __setitem__(self, key, newvalue) -> None:
        new_df = pd_set_iloc(self.df, key, newvalue)
        self.df._set_dataspec(new_df._dataspec)


class Series(DataSpecWrapper[pd.Series]):
    @sarus_init("pandas.PD_SERIES")
    def __init__(
        data=None,
        index=None,
        dtype=None,
        name=None,
        copy=False,
        fastpath=False,
    ):
        ...

    @sarus_method("std.SETITEM", inplace=True)
    def __setitem__(self, key, newvalue):
        ...

    @sarus_property("pandas.PD_INDEX")
    def index(self):
        ...

    @sarus_property("pandas.PD_DTYPE")
    def dtype(self):
        ...

    @sarus_property("pandas.PD_SHAPE")
    def shape(self):
        ...

    @sarus_property("pandas.PD_NDIM")
    def ndim(self):
        ...

    @sarus_property("pandas.PD_SIZE")
    def size(self):
        ...

    @sarus_property("pandas.PD_NAME")
    def name(self):
        ...

    @sarus_property("pandas.PD_VALUES")
    def values(self):
        ...

    def copy(self, deep: bool = False) -> Series:
        return Series.from_dataspec(
            self.dataspec(kind=DataSpecVariant.USER_DEFINED)
        )

    def __sarus_eval__(self) -> pd.Series:
        """Return value of the alternative variant."""
        dataspec = self.dataspec(kind=DataSpecVariant.ALTERNATIVE)

        if dataspec.prototype() == sp.Dataset:
            dataset = cast(st.Dataset, dataspec)
            value = dataset.to_pandas()
            if isinstance(value, pd.DataFrame):
                value = value.squeeze()
            return value
        else:
            scalar = cast(st.Scalar, dataspec)
            return cast(pd.Series, scalar.value())


register_ops()
