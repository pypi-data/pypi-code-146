# coding: utf-8
# /*##########################################################################
#
# Copyright (c) 2016-2020 European Synchrotron Radiation Facility
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
# ###########################################################################*/

__authors__ = ["H. Payno"]
__license__ = "MIT"
__date__ = "05/07/2022"


from tomoscan.esrf.volume.hdf5volume import HDF5Volume as _HDF5Volume
from tomoscan.esrf.identifier.hdf5Identifier import (
    HDF5VolumeIdentifier as _HDF5VolumeIdentifier,
)
from tomwer.core.volume.volumebase import TomwerVolumeBase
from processview.core.dataset import DatasetIdentifier, Dataset
from urllib.parse import urlparse
from tomoscan.esrf.identifier.url_utils import (
    UrlSettings,
    split_path,
    split_query,
)


class HDF5VolumeIdentifier(_HDF5VolumeIdentifier, DatasetIdentifier):
    def __init__(self, object, hdf5_file, entry):
        super().__init__(object, hdf5_file, entry)
        DatasetIdentifier.__init__(self, data_builder=HDF5Volume.from_identifier)

    @staticmethod
    def from_str(identifier):
        info = urlparse(identifier)
        paths = split_path(info.path)
        if len(paths) == 1:
            hdf5_file = paths[0]
            tomo_type = None
        elif len(paths) == 2:
            tomo_type, hdf5_file = paths
        else:
            raise ValueError("Failed to parse path string:", info.path)
        if tomo_type is not None and tomo_type != HDF5VolumeIdentifier.TOMO_TYPE:
            raise TypeError(
                f"provided identifier fits {tomo_type} and not {HDF5VolumeIdentifier.TOMO_TYPE}"
            )

        queries = split_query(info.query)
        entry = queries.get(UrlSettings.DATA_PATH_KEY, None)
        if entry is None:
            raise ValueError("expects to get a data_path")
        return HDF5VolumeIdentifier(object=HDF5Volume, hdf5_file=hdf5_file, entry=entry)


class HDF5Volume(_HDF5Volume, TomwerVolumeBase, Dataset):
    @staticmethod
    def from_identifier(identifier):
        """Return the Dataset from a identifier"""
        if not isinstance(identifier, HDF5VolumeIdentifier):
            raise TypeError(
                f"identifier should be an instance of {HDF5VolumeIdentifier}"
            )
        return HDF5Volume(
            file_path=identifier.file_path,
            data_path=identifier.data_path,
        )

    def get_identifier(self) -> HDF5VolumeIdentifier:
        if self.url is None:
            raise ValueError("no file_path provided. Cannot provide an identifier")
        return HDF5VolumeIdentifier(
            object=self, hdf5_file=self.url.file_path(), entry=self.url.data_path()
        )
