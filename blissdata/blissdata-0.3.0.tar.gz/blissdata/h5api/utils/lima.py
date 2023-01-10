import os
import re
from glob import glob
from collections import abc
from numbers import Integral
from typing import Optional, Tuple, Sequence, Iterator

import numpy
from numpy.typing import DTypeLike
from silx.utils.retry import RetryError
from silx.io import h5py_utils

from . import types

SEP = "/"


class LimaGroup(abc.Mapping):
    def __init__(self, name, *args, **kwargs) -> None:
        self._name = name
        self._dset_args = args
        self._dset_kwargs = kwargs
        self._dataset = None
        super().__init__()

    def close(self):
        if self._dataset is None:
            return
        self._dataset.close()
        self._dataset = None

    def reset(self):
        if self._dataset is None:
            return
        self._dataset.reset()

    @property
    def name(self) -> str:
        return self._name

    @property
    def attrs(self) -> dict:
        return {"type": "lima"}

    def __getitem__(self, key: str):
        if key == "data":
            if self._dataset is None:
                self._dataset = LimaDataset(
                    self.name + SEP + "data", *self._dset_args, **self._dset_kwargs
                )
            return self._dataset
        raise KeyError

    def __iter__(self):
        yield "data"

    def __len__(self) -> int:
        return 1


class LimaDataset(abc.Sequence):
    def __init__(
        self,
        name: str,
        dirname: str,
        url_template: Optional[str] = None,
        user_detector_name: Optional[str] = None,
        user_instrument_name: Optional[str] = None,
    ) -> None:
        parts = [s for s in name.split(SEP) if s]
        scan_number = int(parts[0].split(".")[0])
        bliss_detector_name = parts[-2]

        url_template = lima_url_template(
            dirname,
            scan_number,
            bliss_detector_name,
            url_template=url_template,
            user_detector_name=user_detector_name,
            user_instrument_name=user_instrument_name,
        )
        filename_template, self._path_in_file = url_template.split("::")
        self._search_pattern = filename_template.format(file_index="*")
        self._match_pattern = re.compile(
            os.path.basename(filename_template.format(file_index="([0-9]+)"))
        )
        self._files = list()

        self._first_shape = None
        self._points_per_file = None
        self._dtype = None
        self._shape = None

        self._active_filename = None
        self._active_file = None
        self._active_dset = None
        self._name = name

    @property
    def name(self) -> str:
        return self._name

    @property
    def attrs(self) -> dict:
        return dict()

    def reset(self):
        """Close the activate HDF5 file, cleanup all HDF5 objects and search for lima files"""
        self._cleanup()
        self.search()

    def close(self):
        """Close the activate HDF5 file and cleanup all HDF5 objects"""
        self._cleanup()

    def _cleanup(self):
        if self._active_file is None:
            return
        self._active_file.close()
        self._active_filename = None
        self._active_file = None
        self._active_dset = None

    def search(self):
        lima_files = glob(self._search_pattern)
        lima_nrs = [
            int(self._match_pattern.search(os.path.basename(s)).group(1))
            for s in lima_files
        ]
        self._files = [filename for _, filename in sorted(zip(lima_nrs, lima_files))]
        self._shape = None

    def _open(self, file_index: int):
        try:
            filename = self._files[file_index]
        except IndexError:
            raise RetryError(f"lima file {file_index} does not exist (yet)")
        if self._active_filename == filename:
            return
        self.close()
        # Lima has the file open until all images are written.
        # Lima does not flush which means the file is never readable while it is open.
        # To be sure about the later, try locking the file when reading.
        # If it succeeds it means lima is done with the file.
        self._active_file = h5py_utils.File(
            filename, mode="r"
        )  # , locking=h5py_utils.HAS_LOCKING_ARGUMENT)
        self._active_dset = self._active_file[self._path_in_file]
        self._active_filename = filename

    def __getitem__(self, idx: types.DataIndexType) -> types.DataType:
        if isinstance(idx, Tuple):
            idx0 = idx[0]
            idximage = idx[1:]
        else:
            idx0 = idx
            idximage = tuple()

        dim0scalar = False
        if isinstance(idx0, Integral):
            idx0 = numpy.asarray([idx0])
            dim0scalar = True
        elif isinstance(idx0, slice):
            idx0 = numpy.array(range(*idx0.indices(self.shape[0])))
        elif isinstance(idx0, Sequence):
            idx0 = numpy.asarray(idx0)
        elif idx0 is Ellipsis:
            idx0 = numpy.array(range(self.shape[0]))
        else:
            raise TypeError

        result = list()

        for scan_index in idx0:
            file_index = scan_index // self.point_per_file
            self._open(file_index)
            idx = (scan_index % self.point_per_file,) + idximage
            try:
                result.append(self._active_dset[idx])
            except IndexError:
                raise RetryError(f"Failed slice lima dataset {self._active_dset}")

        if dim0scalar:
            return result[0]
        else:
            return numpy.array(result)

    def __iter__(self) -> Iterator[types.DataType]:
        for file_index in range(len(self._files)):
            self._open(file_index)
            yield from iter(self._active_dset)

    def _cache_dataset_info(self):
        if not self._files:
            self.reset()
        try:
            filename = self._files[0]
        except IndexError:
            raise RetryError("no lima files exists (yet)")
        with h5py_utils.File(filename, mode="r") as f:
            dset = f[self._path_in_file]
            self._points_per_file = len(dset)
            self._first_shape = dset.shape
            self._dtype = dset.dtype

    def __len__(self) -> int:
        return self.shape[0]

    @property
    def point_per_file(self) -> int:
        if self._points_per_file is None:
            self._cache_dataset_info()
        return self._points_per_file

    @property
    def dtype(self) -> DTypeLike:
        if self._dtype is None:
            self._cache_dataset_info()
        return self._dtype

    @property
    def shape(self) -> Tuple[int]:
        if self._shape is not None:
            return self._shape
        if self._first_shape is None:
            self._cache_dataset_info()
        shape = list(self._first_shape)
        shape[0] *= len(self._files)
        self._shape = tuple(shape)
        return self._shape

    @property
    def size(self) -> int:
        return numpy.prod(self.shape, dtype=int)

    @property
    def ndim(self) -> int:
        return 3


def lima_url_template(
    dirname: str,
    scan_number: int,
    bliss_detector_name: str,
    url_template: Optional[str] = None,
    user_detector_name: Optional[str] = None,
    user_instrument_name: Optional[str] = None,
) -> str:
    if not url_template:
        if user_instrument_name:
            url_template = os.path.join(
                "{dirname}",
                "scan{scan_number:04d}",
                "{bliss_detector_name}_{{file_index}}.h5",
            ) + SEP.join(
                (
                    "::",
                    "entry_0000",
                    "{user_instrument_name}",
                    "{user_detector_name}",
                    "data",
                )
            )
        else:
            url_template = os.path.join(
                "{dirname}",
                "scan{scan_number:04d}",
                "{bliss_detector_name}_{{file_index}}.h5",
            ) + SEP.join(("::", "entry_0000", "measurement", "data"))
    if not user_detector_name:
        user_detector_name = bliss_detector_name
    kw = dict()
    if dirname:
        kw["dirname"] = dirname
    if scan_number:
        kw["scan_number"] = scan_number
    if bliss_detector_name:
        kw["bliss_detector_name"] = bliss_detector_name
    if user_detector_name:
        kw["user_detector_name"] = user_detector_name
    if user_instrument_name:
        kw["user_instrument_name"] = user_instrument_name
    url_template = url_template.format(**kw)
    if "{file_index}" not in url_template:
        raise ValueError("A lima template URL needs '{{file_index}}'")
    return url_template
