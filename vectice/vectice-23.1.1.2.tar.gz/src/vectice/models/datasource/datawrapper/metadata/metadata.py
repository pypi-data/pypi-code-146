from __future__ import annotations

from enum import Enum


class DatasetSourceUsage(Enum):
    """
    Enumeration that defines the usage of the dataset.
    """

    TRAINING = "TRAINING"
    TESTING = "TESTING"
    VALIDATION = "VALIDATION"


class SourceOrigin(Enum):
    """
    Enumeration that defines where the data comes from.
    """

    S3 = "S3"
    REDSHIFT = "REDSHIFT"
    GCS = "GCS"
    BIGQUERY = "BIGQUERY"
    SNOWFLAKE = "SNOWFLAKE"
    OTHER = "OTHER"


class Metadata:
    """
    This class describes the metadata of a file.
    """

    def __init__(
        self,
        size: int,
        type: str,
        origin: str,
        usage: DatasetSourceUsage | None = None,
    ):
        """
        :param size: the size of the file.
        :param origin: the origin of the file.
        :param type: the type of data, database or files.
        :param usage: the usage of the file.
        """
        self.origin = origin
        self.size = size
        self.usage = usage
        self.type = type


class SourceType(Enum):
    """
    Enumeration that defines the type of the source the data comes from.
    """

    DB = "DB"
    FILES = "FILES"


class SourceUsage(Enum):
    """
    Enumeration that defines the usage of the data source.
    """

    ORIGIN = "ORIGIN"
    CLEAN = "CLEAN"
    VALIDATION = "VALIDATION"
    MODELING = "MODELING"
