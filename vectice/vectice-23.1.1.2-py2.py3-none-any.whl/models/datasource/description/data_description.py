from __future__ import annotations

from enum import Enum


class DataDescription:
    """
    This class allows to describe a dataset and its columns.
    """

    def __init__(self, columns: list[DataDescriptionColumn], summary: str):
        """
        :param columns: the described columns of the dataset
        :param summary: a brief summary for the dataset
        """
        self._columns = columns
        self._summary = summary

    @property
    def columns(self) -> list[DataDescriptionColumn]:
        """
        Gets the columns description of the dataset.
        :return: List[DataDescriptionColumn]
        """
        return self._columns

    @columns.setter
    def columns(self, columns: list[DataDescriptionColumn]):
        """
        Sets the columns description of the dataset.
        :param: the columns description of the dataset
        """
        self._columns = columns

    @property
    def summary(self) -> str:
        """
        Gets the summary of the dataset.
        :return: str
        """
        return self._summary

    @summary.setter
    def summary(self, summary: str):
        """
        Sets the summary of the dataset.
        :param summary: the summary of the dataset
        """
        self._summary = summary


class DataDescriptionColumn(dict):
    """
    Class used to describe dataset columns.
    """

    def __init__(self, column_name: str, column_description: str, column_data_type: ColumnDataType):
        """
        :param column_name: the name of the column
        :param column_description: a brief description of the column
        :param column_data_type: the type of data contained in the column
        """
        super(DataDescriptionColumn, self).__init__()
        self.column_name = column_name
        self.column_description = column_description
        self.column_type = column_data_type


class ColumnDataType(Enum):
    # TODO: complete this list with other common data types
    OBJECT = "OBJECT"
    INT64 = "INT64"
    FLOAT64 = "FLOAT64"
    BOOL = "BOOL"
    DATETIME64 = "DATETIME64"
    TIMEDELTA = "TIMEDELTA"
    CATEGORY = "CATEGORY"
    OTHER = "OTHER"
