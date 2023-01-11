from abc import ABC
from abc import abstractmethod
from datetime import datetime
import logging
import os
import threading
from typing import Any, Mapping, Optional, Sequence

import numpy as np
import pandas as pd


class CacheColumnMismatchError(ValueError):

    def __init__(self, expected_columns, actual_columns):
        message = "Column mismatch: missing columns {}\nExtra columns {}.".format(
            expected_columns.difference(actual_columns),
            actual_columns.difference(expected_columns)
        )
        super().__init__(self, message)
        self.expected_columns = expected_columns
        self.actual_columns = actual_columns


class CacheColumnDTypeError(ValueError):

    def __init__(self, non_numeric_columns):
        message = "Non-numeric data in computed output, this is likely an internal "
        "TruEra error. Please contact TruEra support for help.\nColumns {}.".format(
            non_numeric_columns
        )
        super().__init__(self, message)
        self.non_numeric_columns = non_numeric_columns


class NumericTableCache(ABC):

    def __init__(
        self,
        columns: Sequence[str],
        unique_id_column: Optional[str] = None,
        timestamp_column_name: Optional[str] = None
    ):
        self.logger = logging.getLogger('ailens.NumericTableCache')
        assert len(columns) > 0, "Columns should be non empty."
        # Cache should contain entries in the range [_index_start, _index_end).
        self._index_start = 0
        self._index_end = 0

        # The columns.
        # To ensure system/runtime independence, they are always stored in sorted order.
        self._columns = sorted([column for column in columns])
        self.unique_id_column = unique_id_column
        self.timestamp_column_name = timestamp_column_name
        self.logger.debug("columns: %s", self.columns)

        # The actual data, as a pandas DataFrame
        # The values are stored in the same order as self._columns.
        # If unique IDs are present, stored as the index of the dataframe.
        self._data: pd.DataFrame = None
        self._system_data: pd.DataFrame = None
        self._dirty: bool = False
        self._updated_on: datetime = datetime.min

        self._update_lock = threading.Lock()

    @property
    def update_lock(self):
        return self._update_lock

    @property
    def dirty(self) -> bool:
        return self._dirty

    @property
    def columns(self) -> Sequence[str]:
        return self._columns

    def is_empty(self):
        return self._index_end == self._index_start

    def len(self):
        return self._index_end - self._index_start

    def contains_index(self, index) -> bool:
        return index >= self._index_start and index < self._index_end

    def contains_index_range(self, start, stop) -> bool:
        return start >= self._index_start and stop <= self._index_end

    def _assert_contains_index(self, index):
        assert self.contains_index(index
                                  ), "Index {} not in range ({}, {})".format(
                                      index, self._index_start, self._index_end
                                  )

    def _assert_right_arr_length(self):
        assert self._data.shape[
            0
        ] == self._index_end - self._index_start, "Expected {}-{} items in array, shape is {}".format(
            self._index_end, self._index_start, self._data.shape
        )

    def set_updated_on(self, updated_on: Optional[datetime] = None):
        self._updated_on = updated_on

    def get_updated_on(self) -> datetime:
        return self._updated_on

    def get_value(
        self, index: int, include_system_data: bool = False
    ) -> pd.Series:
        self._assert_contains_index(index)
        data = self._data.iloc[index - self._index_start, :].copy()
        if include_system_data and self.timestamp_column_name:
            data[self.timestamp_column_name
                ] = self._system_data.iloc[index - self._index_start]
        return data

    def get_value_map(self, index: int) -> Mapping[str, float]:
        return self.get_value(index).to_dict()

    def get_values_df(
        self,
        start: int,
        stop: int,
        include_system_data: bool = False
    ) -> pd.DataFrame:
        self._assert_contains_index(start)
        self._assert_contains_index(stop - 1)
        data = self._data.iloc[(start - self._index_start
                               ):(stop - self._index_start), :].copy()
        if include_system_data and self.timestamp_column_name:
            data[self.timestamp_column_name
                ] = self._system_data.iloc[(start - self._index_start
                                           ):(stop - self._index_start)]
        return data

    def load(self, filename, offset=0, format=None, drop_columns=None):
        extension = os.path.splitext(filename)[1]
        if drop_columns is None:
            drop_columns = []
        if self.unique_id_column:
            drop_columns.append(self.unique_id_column)
        if self.timestamp_column_name:
            drop_columns.append(self.timestamp_column_name)

        if extension == ".csv" or format == "CSV":
            self._load_csv_to_dataframe(
                filename, index_start=offset, drop_columns=drop_columns
            )
        else:
            raise ValueError("Unknown file type: " + extension)
        assert self._data.shape[1] == len(
            self.columns
        ), "Loaded cache of shape {} from {} but expected {} columns: {}. ".format(
            self._data.shape,
            filename,
            len(self.columns),
            self.columns,
        )
        self._index_start = offset
        self._index_end = self._index_start + self._data.shape[0]
        self._dirty = False

    def _load_csv_to_dataframe(
        self,
        filename: str,
        index_start: int,
        drop_columns: Optional[Sequence[str]] = None
    ):
        self.logger.debug("Reading cache from filename: %s", filename)
        table: pd.DataFrame = pd.read_csv(filename, keep_default_na=True)
        self.logger.debug(
            "Read shape and columns: %s, %s", table.shape, table.columns
        )
        if self.unique_id_column:
            table[self.unique_id_column
                 ] = table[self.unique_id_column].astype(str)
            table.set_index(self.unique_id_column, inplace=True)
        else:
            table.set_index(np.arange(index_start, index_start + len(table)))

        if self.timestamp_column_name:
            self._system_data = table[self.timestamp_column_name]

        if drop_columns:
            actual_columns_to_drop = [
                column for column in drop_columns if column in table.columns
            ]
            table.drop(columns=actual_columns_to_drop, inplace=True)
        if self.columns and len(self.columns) > 1:
            expected_columns = set(self.columns)
            actual_columns = set(table.columns)
            if expected_columns != actual_columns:
                raise CacheColumnMismatchError(expected_columns, actual_columns)
            # Reorder columns.
            table = table[self.columns]
        else:
            table.columns = self.columns  # Rename single-dimensional column.
        all_columns = set(table.columns)
        numeric_columns = set(table.select_dtypes(include=[np.number]).columns)
        if all_columns != numeric_columns:
            raise CacheColumnDTypeError(all_columns - numeric_columns)
        self._data = table


class ReadOnlyNumericTableCache(NumericTableCache):
    """Read-Only implementation of `NumericTableCache`.
    This implementation allows reading data generated by
    model runner as cache for AIQ.
    
    """
    pass


class RWNumericTableCache(NumericTableCache):
    """A Read/Write implementation of `NumericTableCache`.
    This implementation allows building the cache in AIQ.

    """

    def save(self, filename):
        extension = os.path.splitext(filename)[1]
        assert extension == ".npy", "Not supported: " + extension
        dirname = os.path.dirname(filename)
        os.makedirs(dirname, exist_ok=True)
        with open(filename, "w+") as f:
            np.save(filename, self._data)
            self._dirty = False
