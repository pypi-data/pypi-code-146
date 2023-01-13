#!/usr/bin/env python
#
# Copyright (c) 2022 Katonic Pty Ltd. All rights reserved.
#

from abc import ABC, abstractmethod
from katonic.fs.errors import UnsupportedFileFormat


file_formats = ["parquet", "csv"]


class FileFormat(ABC):
    """
    Defines an abtract file format used to encode feature data in files
    """

    @abstractmethod
    def to_dict(self):
        """
        Convert this FileFormat into its Dictionary representation.
        """
        pass

    def __eq__(self, other):
        return self.to_dict() == other.to_dict()

    @staticmethod
    def from_dict(file_format):
        """
        Construct this FileFormat from its Dictionary representation.
        Raises NotImplementedError if FileFormat specified in given Dictionary is not supported.
        """
        fmt = file_format
        if fmt == "parquet":
            return ParquetFormat()
        elif fmt == "csv":
            return CSVFormat()
        if fmt is None:
            return None
        raise NotImplementedError(f"FileFormat is unsupported: {fmt}")

    def __str__(self):
        """
        String representation of the file format passed to spark
        """
        raise NotImplementedError()


class ParquetFormat(ABC):
    """
    Defines the Parquet data format
    """

    def __str__(self):
        return "parquet"


class CSVFormat(ABC):
    """
    Defines the CSV data format
    """

    def __str__(self):
        return "csv"
