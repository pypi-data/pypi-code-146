from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from vectice.models.datasource.datawrapper import DataWrapper
    from vectice.models.datasource.description import DataDescription


class DataSource:
    def __init__(self, data_wrapper: DataWrapper, data_description: DataDescription):
        self._data_wrapper = data_wrapper
        self._data_description = data_description

    @property
    def data_wrapper(self) -> DataWrapper:
        return self._data_wrapper

    @data_wrapper.setter
    def data_wrapper(self, value) -> None:
        self._data_wrapper = value

    @property
    def data_description(self) -> DataDescription:
        return self._data_description

    @data_description.setter
    def data_description(self, value) -> None:
        self._data_description = value
