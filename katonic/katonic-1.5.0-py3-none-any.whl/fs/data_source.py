#!/usr/bin/env python
#
# Copyright (c) 2022 Katonic Pty Ltd. All rights reserved.
#

import enum
from abc import ABC, abstractmethod
from typing import Any, Callable, Dict, Iterable, Optional, Tuple

from katonic.fs.repo_config import KfsConfigBaseModel, RepoConfig, get_data_source_class_from_type
from katonic.fs.value_type import ValueType


class SourceType(enum.Enum):
    """
    DataSource value type. Used to define source types in DataSource.
    """

    UNKNOWN = 0
    BATCH_FILE = 1
    BATCH_BIGQUERY = 2
    STREAM_KAFKA = 3
    STREAM_KINESIS = 4


class DataSourceConfig(KfsConfigBaseModel):
    file_format: str
    file_path: str
    event_timestamp_column: str
    created_timestamp_column: str
    type: str
    file_options: Dict[str, str]
    data_source_class_type: str


class DataSource(ABC):
    """
    DataSource that can be used to source features.

    Args:
        event_timestamp_column (optional): Event timestamp column used for point in time
            joins of feature values.
        created_timestamp_column (optional): Timestamp column indicating when the row
            was created, used for deduplicating rows.
        field_mapping (optional): A dictionary mapping of column names in this data
            source to feature names in a feature table or view. Only used for feature
            columns, not entity or timestamp columns.
        date_partition_column (optional): Timestamp column used for partitioning.
    """

    _event_timestamp_column: str
    _created_timestamp_column: str

    def __init__(
        self,
        event_timestamp_column: Optional[str] = None,
        created_timestamp_column: Optional[str] = None,
    ):
        """Creates a DataSource object."""
        self._event_timestamp_column = event_timestamp_column or ""
        self._created_timestamp_column = created_timestamp_column or ""

    def __eq__(self, other):
        if not isinstance(other, DataSource):
            raise TypeError(
                "Comparisons should only involve DataSource class objects.")

        return (
            self.event_timestamp_column == other.event_timestamp_column
            and self.created_timestamp_column == other.created_timestamp_column
        )

    @property
    def event_timestamp_column(self) -> str:
        """
        Returns the event timestamp column of this data source.
        """
        return self._event_timestamp_column

    @event_timestamp_column.setter
    def event_timestamp_column(self, event_timestamp_column):
        """
        Sets the event timestamp column of this data source.
        """
        self._event_timestamp_column = event_timestamp_column

    @property
    def created_timestamp_column(self) -> str:
        """
        Returns the created timestamp column of this data source.
        """
        return self._created_timestamp_column

    @created_timestamp_column.setter
    def created_timestamp_column(self, created_timestamp_column):
        """
        Sets the created timestamp column of this data source.
        """
        self._created_timestamp_column = created_timestamp_column

    @staticmethod
    def from_dict(data_source: Dict) -> Any:    # DataSourceConfig
        """
        Converts data source config in FeatureTable spec to a DataSource class object.

        Args:
            data_source: A Dictionary representation of a DataSource.

        Returns:
            A DataSource class object.

        Raises:
            ValueError: The type of DataSource could not be identified.
        """
        if data_source["data_source_class_type"]:
            cls = get_data_source_class_from_type(
                data_source["data_source_class_type"])
            return cls.from_dict(data_source)

        if (
            not data_source["file_options"]["file_format"]
            or not data_source["file_options"]["file_url"]
        ):
            raise ValueError("Could not identify the source type being added.")

        from katonic.fs.core.offline_stores.file_source import FileSource

        return FileSource.from_dict(data_source)

    @abstractmethod
    def to_dict(self) -> Dict:  # issue with protbuf
        """
        Converts an DataSource object to its Dictionary representation.
        """
        raise NotImplementedError

    def validate(self, config: RepoConfig):
        """
        Validates the underlying data source.

        Args:
            config: Configuration object used to configure a feature store.
        """
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def source_datatype_to_kfs_value_type() -> Callable[[str], ValueType]:
        """
        Returns the callable method that returns kfs type given the raw column type.
        """
        raise NotImplementedError

    def get_table_column_names_and_types(
        self, config: RepoConfig
    ) -> Iterable[Tuple[str, str]]:
        """
        Returns the list of column names and raw column types.

        Args:
            config: Configuration object used to configure a feature store.
        """
        raise NotImplementedError

    def get_table_query_string(self) -> str:
        """
        Returns a string that can directly be used to reference this table in SQL.
        """
        raise NotImplementedError
