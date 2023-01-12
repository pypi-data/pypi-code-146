from __future__ import annotations

import logging
from abc import ABCMeta, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from vectice.models.datasource.datawrapper.metadata import DatasetSourceUsage, FilesMetadata

_logger = logging.getLogger(__name__)


class DataWrapper(metaclass=ABCMeta):
    @abstractmethod
    def __init__(
        self,
        name: str,
        usage: DatasetSourceUsage | None = None,
        inputs: list[int] | None = None,
        capture_code: bool = True,
    ):
        """
        :param usage: The usage of the dataset
        :param name: The name of the :py:class:`DataWrapper`
        :param inputs: The list of dataset ids to create a new dataset from
        :param capture_code: Automatically capture active commit in .git folder
        """
        self._old_name = name
        self._name = name
        self._inputs = inputs
        self._usage = usage
        self._metadata = None
        self._data = None
        self._capture_code = capture_code

    @property
    def data(self) -> dict[str, bytes]:
        """Return the wrapper's data.

        :return: Dict[str, bytes]
        """
        if self._data is None:
            self._data = self._fetch_data()  # type: ignore[assignment]
        return self._data  # type: ignore[return-value]

    @abstractmethod
    def _fetch_data(self) -> dict[str, bytes]:
        pass

    @abstractmethod
    def _build_metadata(self) -> FilesMetadata:
        pass

    @property
    def name(self) -> str:
        """Return the wrapper's name.

        :return: str
        """
        return self._name

    @name.setter
    def name(self, value):
        """Set the wrapper's name."""
        self._name = value
        self._clear_data_and_metadata()

    @property
    def usage(self) -> DatasetSourceUsage | None:
        """Return the wrapper's usage.

        :return: Optional[DatasetSourceUsage]
        """
        return self._usage

    @property
    def inputs(self) -> list[int] | None:
        """Return the wrapper's inputs.

        :return: Optional[List[int]]
        """
        return self._inputs

    @property
    def metadata(self) -> FilesMetadata:
        """Return the wrapper's metadata.

        :return: FilesMetadata
        """
        if self._metadata is None:
            self.metadata = self._build_metadata()
        return self._metadata  # type: ignore[return-value]

    @metadata.setter
    def metadata(self, value):
        """Set the wrapper's metadata."""
        self._metadata = value

    @property
    def capture_code(self) -> bool:
        """Return if git commits should be captured at model assignment.

        If True and the current directory is managed by git, capture
        the SHA1 of the current commit and associate it with the model
        when the model is assigned.  If False, do not look for git
        data at model assignment time.

        :return: CodeSource
        """
        return self._capture_code

    def _clear_data_and_metadata(self):
        self._data = None
        self._metadata = None
