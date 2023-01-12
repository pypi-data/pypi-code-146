from __future__ import annotations

import datetime
from enum import IntEnum, auto
from typing import Any

from PyQt5.QtCore import QAbstractTableModel, QModelIndex, QObject, Qt


class ProtocolRecord(QObject):
    """
    The Protocol Record

    A class containing all information containing in a line of the microscopy protocol list.

    """

    def __init__(self):
        super().__init__()
        # not in attributes
        self._msg_id = None
        self._url = None
        self._experiment_filename = None

        # attributes
        self.microscope = None
        self.protocol_id = None
        self.creation_date = None
        self.operator = None
        self.requesting_unit = None
        self.requesting_user = None
        self.sample_description = None
        self.analysis_status = None

    @classmethod
    def from_elog_attributes(cls, attributes: dict):
        """
        Build a Protocol Record starting from the attributes returned by the elog search.

        Parameters
        ----------
        attributes: dict
            A dictionary containing the attributes of an elog entry.

        Returns
        -------
        A ProtocolRecord class instance
        """
        record = cls()
        record.protocol_id = attributes.get('Protocol number', None)
        record.creation_date = attributes.get('Creation date', None)
        record.microscope = attributes.get('Microscope', None)
        record.operator = attributes.get('Operator', None)
        record.requesting_user = attributes.get('Requesting user', None)
        record.requesting_unit = attributes.get('Requesting unit', None)
        record.sample_description = attributes.get('Sample description', None)
        record.analysis_status = attributes.get('Analysis status', None)
        return record

    @classmethod
    def from_tuple(cls, attributes: tuple):
        record = cls()
        record.protocol_id = attributes[0]
        record.creation_date = attributes[1]
        record.microscope = attributes[2]
        record.operator = attributes[3]
        record.requesting_user = attributes[4]
        record.requesting_unit = attributes[5]
        record.sample_description = attributes[6]
        record.analysis_status = attributes[7]
        return record

    def to_tuple(self) -> tuple:
        """
        Return a tuple with all Record parameters

        Returns
        -------
        A tuple with the protocol record values
        """
        return (self.protocol_id,
                self.creation_date,
                self.microscope,
                self.operator,
                self.requesting_user,
                self.requesting_unit,
                self.sample_description,
                self.analysis_status)

    @staticmethod
    def header_tuple() -> tuple:
        """
        Return a tuple with all the record parameter names.

        It is to be used as header in the data view.

        Returns
        -------
        A tuple with the parameter names
        """
        return ('Protocol ID',
                'Creation date',
                'Microscope',
                'Operator',
                'User',
                'Unit',
                'Description',
                'Analysis status'
                )

    @property
    def msg_id(self) -> int:
        """The message id property"""
        return self._msg_id

    @msg_id.setter
    def msg_id(self, value):
        self._msg_id = value

    @property
    def url(self) -> str:
        return self._url

    @url.setter
    def url(self, url: str):
        self._url = url

    @property
    def experiment_filename(self) -> str:
        return self._experiment_filename

    @experiment_filename.setter
    def experiment_filename(self, filename: str):
        self._experiment_filename = filename

    @staticmethod
    def no_of_column() -> int:
        """The number of elements in the header tuple"""
        return len(ProtocolRecord.header_tuple())


class SearchResultsModel(QAbstractTableModel):
    """Subclass of the Abstract Table Model to contain the protocol list search result"""

    class UserRole(IntEnum):
        """
        User Role enumerator

        MSG_ID is used to store the msg_id of the item. We store in a different field because we don't show this value in
        the table.

        """

        @staticmethod
        def _generate_next_value_(name: str, start: int, count: int, last_values: list[Any]) -> Any:
            return IntEnum._generate_next_value_(name, Qt.UserRole + 1, count, last_values)

        MSG_ID = auto()
        URL = auto()
        EXPERIMENT_FILE = auto()
        MICROSCOPE = auto()
        TUPLE = auto()

    def __init__(self, results: list[ProtocolRecord] = None):
        super(SearchResultsModel, self).__init__(results)
        self.results = list()
        if results:
            self.results = results

    def set_search_results(self, results: list[ProtocolRecord]):
        """
        Set the search results.

        Parameters
        ----------
        results: list[ProtocolRecord]
            A list of protocol record to be transferred to the model
        """
        self.beginResetModel()
        self.results = results
        self.endResetModel()

    def headerData(self, section: int, orientation: Qt.Orientation, role: int = ...) -> Any:
        """
        Return the header data of the model.

        For the current model, we show headers only for the Qt.DisplayRole and horizontal orientation.
        """
        if role != Qt.DisplayRole:
            return
        if orientation == Qt.Orientation.Horizontal:
            return ProtocolRecord.header_tuple()[section]
        else:
            return

    def index(self, row: int, column: int, parent: QModelIndex = ...) -> QModelIndex:
        """
        Reimplement the index method.

        Parameters
        ----------
        row: int
            Row number
        column: int
            Column number
        parent: QModelIndex
            parent index

        Returns
        -------
        QModelIndex:
            The model index.
        """
        if not self.hasIndex(row, column, parent):
            return QModelIndex()
        return self.createIndex(row, column, None)

    def rowCount(self, parent: QModelIndex = ...) -> int:
        """Return the total number of rows in the model."""
        return len(self.results)

    def columnCount(self, parent: QModelIndex = ...) -> int:
        """Return the total number of columns in the model."""
        return ProtocolRecord.no_of_column()

    def data(self, index: QModelIndex, role: int = ...) -> Any:
        """
        Return the data of the index for the role.

        Parameters
        ----------
        index: QModelIndex
            An index of the model
        role: int
            A data role. For this model we have the Qt.DisplayRole and some user defined roles:
                UserRole.MSG_ID containing the MSG_ID
                UserRole.URL containing the elog url of the record
                UserRole.EXPERIMENT_FILE containing the experiment file of the record
                UserRole.MICROSCOPE containing the microscope type. This is a duplicate for simplicity
        Returns
        -------

        """
        if not index.isValid():
            return

        all_roles = [role for role in SearchResultsModel.UserRole]
        all_roles.append(Qt.DisplayRole)

        if role not in all_roles:
            return

        if role == SearchResultsModel.UserRole.MSG_ID:
            return self.results[index.row()].msg_id

        if role == SearchResultsModel.UserRole.URL:
            return self.results[index.row()].url

        if role == SearchResultsModel.UserRole.EXPERIMENT_FILE:
            return self.results[index.row()].experiment_filename

        if role == SearchResultsModel.UserRole.MICROSCOPE:
            return self.results[index.row()].microscope

        if role == SearchResultsModel.UserRole.TUPLE:
            return self.results[index.row()].to_tuple()

        if role == Qt.DisplayRole:
            record = self.results[index.row()]
            if index.column() == 1:
                return datetime.datetime.fromtimestamp(float(record.to_tuple()[index.column()])).strftime('%d-%m-%Y')
            else:
                return record.to_tuple()[index.column()]
