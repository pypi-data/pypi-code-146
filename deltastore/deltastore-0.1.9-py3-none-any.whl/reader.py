#
# Copyright (C) 2021 The Delta Lake Project Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import operator
from functools import reduce
from json import loads
from typing import Any, Callable, Dict, Optional, Sequence
from urllib.parse import urlparse

import fsspec
import pandas as pd
import pyarrow as pa
from deltastore.converter import PandasConverter, PyArrowConverter
from deltastore.helper import _parse_url
from deltastore.protocol import AddFile, DeltaSharingProfile, Table
from deltastore.rest_client import DataSharingRestClient


class DeltaSharingReader:
    def __init__(
        self,
        table: Table,
        rest_client: DataSharingRestClient,
        *,
        predicates: Optional[Sequence[str]] = None,
        columns: Optional[Sequence[str]] = None,
        limit: Optional[int] = None,
    ):
        self._table = table
        self._rest_client = rest_client

        self._predicates = predicates
        self._columns = columns

        if limit is not None:
            assert (
                isinstance(limit, int) and limit >= 0
            ), "'limit' must be a non-negative int"
        self._limit = limit

    @property
    def table(self) -> Table:
        return self._table

    def limit(self, limit: Optional[int]) -> "DeltaSharingReader":
        return self._copy(predicates=self._predicates, limit=limit)

    def to_predicates(self, filters):
        predicates = []
        for conjunction in filters:
            col, op, val = conjunction
            predicates.append(f"{col}{op}{val}")
        return predicates

    def to_expressions(self, filters, partitions):
        def convert_single_expression(col, op, val):
            field = pa.dataset.field(col)

            if op == "=" or op == "==":
                return field == val
            elif op == "!=":
                return field != val
            elif op == "<":
                return field < val
            elif op == ">":
                return field > val
            elif op == "<=":
                return field <= val
            elif op == ">=":
                return field >= val
            elif op == "in":
                return field.isin(val)
            elif op == "not in":
                return ~field.isin(val)
            else:
                raise ValueError(
                    '"{0}" is not a valid operator in predicates.'.format(
                        (col, op, val)
                    )
                )

        expressions = []
        for conjunction in filters:
            col, op, val = conjunction
            if col not in partitions:
                expression = convert_single_expression(col, op, val)
                expressions.append(expression)
        if len(expressions) > 0:
            return reduce(operator.and_, expressions)

    def to_pandas(self) -> pd.DataFrame:
        predicates = self.to_predicates(self._predicates)
        columns = self._columns
        limit = self._limit

        response = self._rest_client.list_files_in_table(
            self._table, predicateHints=predicates, limitHint=limit
        )

        expressions = self.to_expressions(
            self._predicates, response.metadata.partition_columns
        )

        schema_json = loads(response.metadata.schema_string)

        if len(response.add_files) == 0 or limit == 0:
            return PandasConverter.get_empty_table(schema_json)

        converters = PandasConverter.to_converters(schema_json)

        if limit is None:
            dataframes = []
            for file in response.add_files:
                dataframe = DeltaSharingReader._to_pandas(
                    file,
                    converters,
                    expressions,
                    columns,
                    response.metadata.partition_columns,
                    None,
                )
                if len(dataframe) > 0:
                    dataframes.append(dataframe)
        else:
            left = limit
            dataframes = []
            for file in response.add_files:
                dataframe = DeltaSharingReader._to_pandas(
                    file,
                    converters,
                    expressions,
                    columns,
                    response.metadata.partition_columns,
                    left,
                )
                dataframes.append(dataframe)
                left -= len(dataframe)
                assert (
                    left >= 0
                ), f"'_to_pandas' returned too many rows. Required: {left}, returned: {len(dataframe)}"
                if left == 0:
                    break

        if len(dataframes) == 0:
            return PandasConverter.get_empty_table(schema_json)
        return pd.concat(
            dataframes,
            axis=0,
            ignore_index=True,
            copy=False,
        )

    def to_arrow(self) -> pa.Table:
        predicates = self.to_predicates(self._predicates)
        columns = self._columns
        limit = self._limit

        response = self._rest_client.list_files_in_table(
            self._table, predicateHints=predicates, limitHint=limit
        )

        expressions = self.to_expressions(
            self._predicates, response.metadata.partition_columns
        )

        schema_json = loads(response.metadata.schema_string)

        if len(response.add_files) == 0 or limit == 0:
            return PyArrowConverter.get_empty_table(schema_json)

        converters = PyArrowConverter.to_converters(schema_json)

        if limit is None:
            tables = []
            for file in response.add_files:
                table = DeltaSharingReader._to_arrow(
                    file,
                    converters,
                    expressions,
                    columns,
                    response.metadata.partition_columns,
                    None,
                )
                if len(table) > 0:
                    tables.append(table)
        else:
            left = limit
            tables = []
            for file in response.add_files:
                table = DeltaSharingReader._to_arrow(
                    file,
                    converters,
                    expressions,
                    columns,
                    response.metadata.partition_columns,
                    left,
                )
                tables.append(table)
                left -= len(table)
                assert (
                    left >= 0
                ), f"'_to_arrow' returned too many rows. Required: {left}, returned: {len(table)}"
                if left == 0:
                    break

        if len(tables) == 0:
            return PyArrowConverter.get_empty_table(schema_json)
        return pa.concat_tables(tables)

    def _copy(
        self,
        *,
        predicates: Optional[Sequence[str]],
        columns: Optional[Sequence[str]],
        limit: Optional[int],
    ) -> "DeltaSharingReader":
        return DeltaSharingReader(
            table=self._table,
            rest_client=self._rest_client,
            predicates=predicates,
            columns=columns,
            limit=limit,
        )

    @staticmethod
    def _to_pandas(
        add_file: AddFile,
        converters: Dict[str, Callable[[str], Any]],
        filters: Optional[pa.compute.Expression],
        columns: Optional[str],
        partitions: Optional[str],
        limit: Optional[int],
    ) -> pd.DataFrame:
        url = urlparse(add_file.url)
        if "storage.googleapis.com" in (url.netloc.lower()):
            import deltastore._yarl_patch

        protocol = url.scheme
        filesystem = fsspec.filesystem(protocol)

        dataset = pa.dataset.dataset(
            source=add_file.url, format="parquet", filesystem=filesystem
        )
        table = (
            dataset.to_table(
                filter=filters,
                columns=list(filter(lambda c: c not in partitions, columns))
                if columns
                else None,
            ).slice(length=limit)
            if limit is not None
            else dataset.to_table(
                filter=filters,
                columns=list(filter(lambda c: c not in partitions, columns))
                if columns
                else None,
            )
        )
        dataframe = table.to_pandas(
            date_as_object=True,
            use_threads=False,
            split_blocks=True,
            self_destruct=True,
        )

        for col, converter in converters.items():
            if not columns or col in columns:
                if col not in dataframe.columns:
                    if col in add_file.partition_values:
                        if converter is not None:
                            dataframe[col] = converter(add_file.partition_values[col])
                        else:
                            raise ValueError(
                                "Cannot partition on binary or complex columns"
                            )
                    else:
                        dataframe[col] = None

        return dataframe

    @staticmethod
    def _to_arrow(
        add_file: AddFile,
        converters: Dict[str, Callable[[str], Any]],
        filters: Optional[pa.compute.Expression],
        columns: Optional[str],
        partitions: Optional[str],
        limit: Optional[int],
    ) -> pa.Table:
        url = urlparse(add_file.url)
        if "storage.googleapis.com" in (url.netloc.lower()):
            import deltastore._yarl_patch

        protocol = url.scheme
        filesystem = fsspec.filesystem(protocol)

        dataset = pa.dataset.dataset(
            source=add_file.url, format="parquet", filesystem=filesystem
        )
        table = (
            dataset.to_table(
                filter=filters,
                columns=list(filter(lambda c: c not in partitions, columns))
                if columns
                else None,
            ).slice(length=limit)
            if limit is not None
            else dataset.to_table(
                filter=filters,
                columns=list(filter(lambda c: c not in partitions, columns))
                if columns
                else None,
            )
        )

        for col, converter in converters.items():
            if not columns or col in columns:
                if col not in table.column_names:
                    if col in add_file.partition_values:
                        if converter is not None:
                            table = table.append_column(
                                col,
                                pa.array(
                                    [converter(add_file.partition_values[col])]
                                    * table.num_rows
                                ),
                            )
                        else:
                            raise ValueError(
                                "Cannot partition on binary or complex columns"
                            )

        return table


def load_as_pandas(url, predicates=None, columns=None, limit=None):
    profile_json, share, schema, table = _parse_url(url)
    profile = DeltaSharingProfile.read_from_file(profile_json)
    return DeltaSharingReader(
        table=Table(name=table, share=share, schema=schema),
        rest_client=DataSharingRestClient(profile),
        predicates=predicates,
        columns=columns,
        limit=limit,
    ).to_pandas()


def load_as_arrow(url, predicates=None, columns=None, limit=None):
    profile_json, share, schema, table = _parse_url(url)
    profile = DeltaSharingProfile.read_from_file(profile_json)
    return DeltaSharingReader(
        table=Table(name=table, share=share, schema=schema),
        rest_client=DataSharingRestClient(profile),
        predicates=predicates,
        columns=columns,
        limit=limit,
    ).to_arrow()
