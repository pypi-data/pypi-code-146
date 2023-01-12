"""Implementation of the h5py-like Bliss Data API with dynamic HDF5 files"""

from numbers import Number
from typing import Any, Iterator, Optional, Union

import h5py
from silx.io import h5py_utils

from . import types
from . import lima
from .hdf5_retry import retry_file_access
from .hdf5_retry import ignore_retry_timeout
from .hdf5_retry import RetryError, SoftRetryError


HDF5Item = Union[h5py.Dataset, h5py.Group, h5py.File, lima.LimaDataset, lima.LimaGroup]
HDF5Group = Union[h5py.Group, h5py.File, lima.LimaGroup]
HDF5Dataset = Union[h5py.Dataset, lima.LimaDataset]


SEP = "/"


class DynamicHDF5Handler:
    """Object to access an HDF5 file which is re-opened upon re-trying failed IO operations"""

    def __init__(
        self,
        file: str,
        retry_timeout: Optional[Number] = None,
        retry_period: Optional[Number] = None,
        **openargs,
    ):
        self._file = file
        self._openargs = openargs
        self._file_obj = None
        self._closed = False
        self._retry_period = retry_period
        self._retry_options = {
            "retry_timeout": retry_timeout,
            "retry_period": retry_period,
        }
        self._native_items = dict()

    def close(self) -> None:
        """Close the HDF5 file, cleanup all HDF5 objects and do not allow re-opening"""
        self._closed = True
        self._cleanup()

    def reset(self) -> None:
        """Close the HDF5 file, cleanup all HDF5 objects but allow re-opening"""
        self._cleanup()

    def _cleanup(self) -> None:
        """Close the HDF5 file, cleanup all HDF5 objects"""
        if self._file_obj is None:
            return
        self._file_obj.close()
        self._file_obj = None
        self._native_items = dict()

    @property
    def file_obj(self) -> h5py.File:
        if self._file_obj is None:
            if self._closed:
                raise RuntimeError("File was closed")
            try:
                self._file_obj = h5py_utils.File(self._file, **self._openargs)
            except FileNotFoundError:
                raise RetryError(f"File {self._file} does not exist (yet)")
        return self._file_obj

    def get_item(self, name: str) -> HDF5Item:
        return self._retry_get_item(name)

    def slice_dataset(self, name: str, idx: types.DataIndexType) -> types.DataType:
        return self._retry_slice_dataset(name, idx)

    def get_attr(self, name: str, key: str) -> Any:
        return self._retry_get_attr(name, key)

    @ignore_retry_timeout
    def iter_attrs(self, name: str) -> Iterator[str]:
        yield from self._retry_iter_attrs(name)

    @ignore_retry_timeout
    def len_attrs(self, name: str) -> int:
        return self._retry_len_attrs(name)

    @ignore_retry_timeout
    def iter_item(self, name: str) -> Iterator[Union[str, types.DataType]]:
        yield from self._retry_iter_item(name)

    @ignore_retry_timeout
    def len_item(self, name: str) -> int:
        return self._retry_len_item(name)

    def getattr_item(self, name: str, attr_name: str) -> Any:
        return self._retry_getattr_item(name, attr_name)

    @retry_file_access
    def _retry_get_item(self, name: str) -> HDF5Item:
        return self._get_item(name)

    @retry_file_access
    def _retry_slice_dataset(
        self, name: str, idx: types.DataIndexType
    ) -> types.DataType:
        return self._slice_dataset(name, idx)

    @retry_file_access
    def _retry_get_attr(self, name: str, key: str) -> Any:
        return self._get_attr(name, key)

    @retry_file_access
    def _retry_iter_attrs(self, name: str, start_index: int = 0) -> Iterator[str]:
        yield from self._iter_attrs(name, start_index=start_index)

    @retry_file_access
    def _retry_len_attrs(self, name: str) -> int:
        return self._len_attrs(name)

    @retry_file_access
    def _retry_iter_item(
        self, name: str, start_index: int = 0
    ) -> Iterator[Union[str, types.DataType]]:
        yield from self._iter_item(name, start_index=start_index)

    @retry_file_access
    def _retry_len_item(self, name: str) -> int:
        return self._len_item(name)

    @retry_file_access
    def _retry_getattr_item(self, name: str, attr_name: str) -> Any:
        return self._getattr_item(name, attr_name)

    def _get_item(self, name: str) -> HDF5Item:
        item = self._native_items.get(name)
        if item is not None:
            return item
        item = self.file_obj[name]
        self._native_items[name] = item
        return item

    def _slice_dataset(self, name: str, idx: types.DataIndexType) -> types.DataType:
        item = self._get_item(name)
        self._check_dataset_before_read(item)
        return item[idx]

    def _check_dataset_before_read(self, item: HDF5Dataset):
        pass

    def _get_attr(self, name: str, key: str) -> Any:
        item = self._get_item(name)
        return item.attrs[key]

    def _iter_attrs(self, name: str, start_index: int = 0) -> Iterator[str]:
        item = self._get_item(name)
        if start_index == 0:
            yield from item.attrs
        else:
            yield from list(item.attrs)[start_index:]
        if not self._is_initialized(item):
            raise RetryError("not fully initialized")

    def _len_attrs(self, name: str) -> int:
        item = self._get_item(name)
        return len(item.attrs)

    def _iter_item(
        self, name: str, start_index: int = 0
    ) -> Iterator[Union[str, types.DataType]]:
        item = self._get_item(name)
        self._check_dataset_before_read(item)
        if self.is_group(item):
            is_initialized = self._is_initialized(item)
            for key in self._iter_group(item, start_index):
                is_initialized = False
                yield key
            if not is_initialized:
                raise RetryError("not initialized")
        else:
            is_finished = self._is_finished(item)
            for data in self._iter_dataset(item, start_index):
                is_finished = False
                yield data
            if not is_finished:
                raise RetryError("not finished")

    @staticmethod
    def is_group(h5item: HDF5Item):
        return isinstance(h5item, (h5py.Group, h5py.File))

    def _iter_group(self, h5group: HDF5Group, start_index: int) -> Iterator[str]:
        try:
            if start_index == 0:
                yield from h5group
            else:
                yield from list(h5group.keys())[start_index:]
        except ValueError:
            raise SoftRetryError(f"Failed accessing group {h5group}")

    def _iter_dataset(
        self, h5dataset: HDF5Dataset, start_index: int
    ) -> Iterator[types.DataType]:
        try:
            if start_index == 0:
                yield from h5dataset
            else:
                for i in range(start_index, len(h5dataset)):
                    yield h5dataset[i]
        except ValueError:
            raise SoftRetryError(f"Failed accessing dataset {h5dataset}")

    def _len_item(self, name: str) -> int:
        item = self._get_item(name)
        return len(item)

    def _getattr_item(self, name: str, attr_name: str) -> Any:
        item = self._get_item(name)
        return getattr(item, attr_name)

    def _is_initialized(self, h5item: HDF5Item) -> bool:
        return True

    def _is_finished(self, h5item: HDF5Item) -> bool:
        return True
