#!/usr/bin/env python
#
# Copyright (c) 2022 Katonic Pty Ltd. All rights reserved.
#

from typing import Callable, Dict, Iterable, Optional, Tuple

from pyarrow._fs import FileSystem
from pyarrow.parquet import ParquetFile

from katonic.fs import type_map
from katonic.fs.data_format import FileFormat
from katonic.fs.data_source import DataSource, SourceType
from katonic.fs.repo_config import RepoConfig
from katonic.fs.value_type import ValueType


class FileSource(DataSource):
    def __init__(
        self,
        path: Optional[str] = None,
        file_format: FileFormat = None,
        event_timestamp_column: Optional[str] = "",
        created_timestamp_column: Optional[str] = "",
    ):
        """Create a FileSource from a file containing feature data. Parquet and CSV formats supported.

        Args:

            path: File path to file containing feature data. Must contain an event_timestamp column, entity columns and
                feature columns.
            file_format: Explicitly set the file format. Allows kfs to bypass inferring the file format.
            event_timestamp_column: Event timestamp column used for point in time joins of feature values.
            created_timestamp_column (optional): Timestamp column when row was created, used for deduplicating rows.

        Examples:
            >>> from katonic.fs import FileSource
            >>> file_source = FileSource(path="my_features.parquet", file_format="parquet", event_timestamp_column="event_timestamp")
        """

        if path is None:
            raise ValueError(
                'No "path" argument provided. Please set "path" to the location of your file source.'
            )

        self._file_options = FileOptions(
            file_format=file_format,
            file_url=path,
        )

        super().__init__(
            event_timestamp_column,
            created_timestamp_column,
        )

    def __eq__(self, other):
        if not isinstance(other, FileSource):
            raise TypeError(
                "Comparisons should only involve FileSource class objects.")

        return (
            self.file_options.file_url == other.file_options.file_url
            and self.file_options.file_format == other.file_options.file_format
            and self.event_timestamp_column == other.event_timestamp_column
            and self.created_timestamp_column == other.created_timestamp_column
        )

    @property
    def file_options(self):
        """
        Returns the file options of this data source
        """
        return self._file_options

    @file_options.setter
    def file_options(self, file_options):
        """
        Sets the file options of this data source
        """
        self._file_options = file_options

    @property
    def path(self):
        """
        Returns the file path of this feature data source
        """
        return self._file_options.file_url

    @classmethod
    def from_dict(cls, data_source: Dict):
        return FileSource(
            path=data_source["file_options"]["file_url"],
            file_format=data_source["file_options"]["file_format"],
            event_timestamp_column=data_source["event_timestamp_column"],
            created_timestamp_column=data_source["created_timestamp_column"],
        )

    # issue with types
    def to_dict(self) -> Dict:
        return {
            "type": SourceType.BATCH_FILE.name,
            "file_options": self.file_options.to_dict(),
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
        filesystem, path = FileSource.create_filesystem_and_path(
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


class FileOptions:
    """
    DataSource File options used to source features from a file
    """

    def __init__(
        self,
        file_format: Optional[FileFormat],
        file_url: Optional[str],
    ):
        """
        FileOptions initialization method

        Args:
            file_format (FileFormat, optional): file source format eg. parquet
            file_url (str, optional): file source url or local file
        """
        self._file_format = file_format
        self._file_url = file_url

    @property
    def file_format(self):
        """
        Returns the file format of this file
        """
        return self._file_format

    @file_format.setter
    def file_format(self, file_format):
        """
        Sets the file format of this file
        """
        self._file_format = file_format

    @property
    def file_url(self):
        """
        Returns the file url of this file
        """
        return self._file_url

    @file_url.setter
    def file_url(self, file_url):
        """
        Sets the file url of this file
        """
        self._file_url = file_url

    @classmethod
    def from_dict(cls, file_options_dict: Dict):
        """
        Creates a FileOptions from a Dictionary representation of a file option

        args:
            file_options_dict: a Dictionary representation of a datasource

        Returns:
            Returns a FileOptions object based on the file_options Dictionary
        """
        return cls(
            file_format=file_options_dict["file_format"],
            file_url=file_options_dict["file_url"],
        )

    def to_dict(self) -> Dict:
        """
        Converts an FileOptions Details to its Dictionary representation.

        Returns:
            FileOptions Dictionary format
        """

        return {
            "file_format": (
                None if self.file_format is None else self.file_format
            ),
            "file_url": self.file_url,
        }
