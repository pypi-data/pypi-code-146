#!/usr/bin/env python
#
# Copyright (c) 2022 Katonic Pty Ltd. All rights reserved.
#

from typing import Callable, Dict, Iterable, Optional, Tuple, Union

import pandas as pd
import pyspark
from pyarrow._fs import FileSystem
from pyarrow.parquet import ParquetFile

from katonic.fs import type_map
from katonic.fs.data_source import DataSource, SourceType
from katonic.fs.repo_config import RepoConfig
from katonic.fs.value_type import ValueType


class DataFrameSource(DataSource):

    data_df: Union[pd.DataFrame, pyspark.sql.DataFrame]

    def __init__(
        self,
        df: Union[pyspark.sql.DataFrame, pd.DataFrame],
        mode: Optional[str] = None,
        # df_format: str, # Optional[str] = None,  pandas or spark
        event_timestamp_column: str = "",
        created_timestamp_column: Optional[str] = "",
    ):
        """Create a DataFrameSource from a dataframe containing feature data. Pandas & Spark supported.

        Args:

            df: DataFrame containing feature data. Must contain an event_timestamp column, entity columns and
                feature columns.
            mode (optional): Explicitly set the file format. Allows kfs to bypass inferring the file format.
            event_timestamp_column: Event timestamp column used for point in time joins of feature values.
            created_timestamp_column (optional): Timestamp column when row was created, used for deduplicating rows.

        Examples:
            >>> from katonic.fs import DataFrameSource
            >>> dataframe_source = DataFrameSource(df=data_df, event_timestamp_column="event_timestamp")
        """

        if df is None:
            raise ValueError(
                'No "df" provided. Please set "df" to the pandas or spark DataFrame of your DataFrame source.'
            )

        if mode is None and isinstance(df, pyspark.sql.DataFrame):
            mode = 'append'

        self._data_df = df

        self._df_options = DataFrameOptions(
            # df_format=df_format,
            mode=mode,
        )

        super().__init__(
            event_timestamp_column,
            created_timestamp_column,
        )

    def __eq__(self, other):
        if not isinstance(other, DataFrameSource):
            raise TypeError(
                "Comparisons should only involve DataFrameSource class objects.")

        return (
            # self.df_options.df_format == other.df_options.df_format
            self.df_options.mode == other.df_options.mode
            and self.event_timestamp_column == other.event_timestamp_column
            and self.created_timestamp_column == other.created_timestamp_column
        )

    @property
    def df_options(self):
        """
        Returns the file options of this data source
        """
        return self._df_options

    @df_options.setter
    def df_options(self, df_options):
        """
        Sets the file options of this data source
        """
        self._df_options = df_options

    @property
    def data_df(self):
        """
        Returns the dataframe of this feature data source
        """
        return self._data_df

    @classmethod
    def from_dict(cls, data_source: Dict):
        return DataFrameSource(
            df=data_source["df"],
            mode=data_source["df_options"]["mode"],
            event_timestamp_column=data_source["event_timestamp_column"],
            created_timestamp_column=data_source["created_timestamp_column"],
        )

    # issue with types
    def to_dict(self) -> Dict:
        return {
            "type": SourceType.BATCH_FILE.name,
            "df": self.data_df.__class__.__name__ if type(self.data_df) is not str else self.data_df,
            "df_options": self.df_options.to_dict(),
            "event_timestamp_column": self.event_timestamp_column,
            "created_timestamp_column": self.created_timestamp_column,
        }

    def validate(self, config: RepoConfig):
        # TODO: validate a FileSource
        pass

    @staticmethod
    def source_datatype_to_kfs_value_type() -> Callable[[str], ValueType]:
        return type_map.pa_to_kfs_value_type

    def get_table_column_names_and_types(
        self, config: RepoConfig
    ) -> Iterable[Tuple[str, str]]:
        filesystem, path = DataFrameSource.create_filesystem_and_path(
            self.path
        )
        schema = ParquetFile(
            path if filesystem is None else filesystem.open_input_file(path)
        ).schema_arrow
        return zip(schema.names, map(str, schema.types))

    @staticmethod
    def create_filesystem_and_path(
        path: str
    ) -> Tuple[Optional[FileSystem], str]:
        return None, path


class DataFrameOptions:
    """
    DataSource File options used to source features from a file
    """

    def __init__(
        self,
        # df_format: Optional[FileFormat],
        mode: Optional[str],
    ):
        """
        FileOptions initialization method

        Args:
            file_format (FileFormat, optional): file source format eg. parquet
            file_url (str, optional): file source url or local file
        """
        # self._df_format = df_format
        self._mode = mode

    # @property
    # def df_format(self):
    #     """
    #     Returns the file format of this file
    #     """
    #     return self._df_format

    # @df_format.setter
    # def df_format(self, df_format):
    #     """
    #     Sets the file format of this file
    #     """
    #     self._df_format = df_format

    @property
    def mode(self):
        """
        Returns the file url of this file
        """
        return self._mode

    @mode.setter
    def mode(self, mode):
        """
        Sets the file url of this file
        """
        self._mode = mode

    @classmethod
    def from_dict(cls, df_options_dict: Dict):
        """
        Creates a FileOptions from a Dictionary representation of a file option

        args:
            df_options_dict: a Dictionary representation of a datasource

        Returns:
            Returns a FileOptions object based on the df_options dict
        """
        return cls(
            # df_format=df_options_dict["df_format"],
            mode=df_options_dict["mode"],
        )

    def to_dict(self) -> Dict:
        """
        Converts an FileOptions Details to its Dictionary representation.

        Returns:
            FileOptions Dictionary
        """

        return {
            # "df_format":(
            #     None if self.df_format is None else self.df_format
            # ),
            "mode": self.mode,
        }
