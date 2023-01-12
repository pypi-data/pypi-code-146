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


import os
from tomoscan.esrf.volume.tiffvolume import (
    TIFFVolume as _TIFFVolume,
    MultiTIFFVolume as _MultiTIFFVolume,
)
from tomwer.core.volume.volumebase import TomwerVolumeBase
from tomoscan.esrf.identifier.tiffidentifier import (
    MultiTiffVolumeIdentifier as _MultiTiffVolumeIdentifier,
    TIFFVolumeIdentifier as _TIFFVolumeIdentifier,
)
from processview.core.dataset import DatasetIdentifier, Dataset


class TIFFVolumeIdentifier(_TIFFVolumeIdentifier, DatasetIdentifier):
    def __init__(self, object, folder, file_prefix):
        super().__init__(object, folder, file_prefix)
        DatasetIdentifier.__init__(self, TIFFVolume.from_identifier)

    @staticmethod
    def from_str(identifier):
        return _TIFFVolumeIdentifier._from_str_to_single_frame_identifier(
            identifier=identifier,
            SingleFrameIdentifierClass=TIFFVolumeIdentifier,
            ObjClass=TIFFVolume,
        )


class MultiTiffVolumeIdentifier(_MultiTiffVolumeIdentifier, DatasetIdentifier):
    def __init__(self, object, tiff_file):
        super().__init__(object, tiff_file)
        DatasetIdentifier.__init__(self, TIFFVolume.from_identifier)

    @staticmethod
    def from_str(identifier):
        identifier_no_scheme = identifier.split(":")[-1]
        tiff_file = identifier_no_scheme
        return MultiTiffVolumeIdentifier(object=TIFFVolume, tiff_file=tiff_file)


class TIFFVolume(_TIFFVolume, TomwerVolumeBase, Dataset):
    @staticmethod
    def from_identifier(identifier):
        """Return the Dataset from a identifier"""
        if not isinstance(identifier, TIFFVolumeIdentifier):
            raise TypeError(
                f"identifier should be an instance of {TIFFVolumeIdentifier} not {type(identifier)}"
            )
        return TIFFVolume(
            folder=identifier.folder,
            volume_basename=identifier.file_prefix,
        )

    def get_identifier(self) -> TIFFVolumeIdentifier:
        if self.url is None:
            raise ValueError("no file_path provided. Cannot provide an identifier")
        return TIFFVolumeIdentifier(
            object=self, folder=self.url.file_path(), file_prefix=self._volume_basename
        )

    def volume_data_parent_folder(self):
        if self.data_url is None:
            raise ValueError("data_url doesn't exists")
        else:
            return os.path.dirname(self.data_url.file_path())


class MultiTIFFVolume(_MultiTIFFVolume, TomwerVolumeBase, Dataset):
    @staticmethod
    def from_identifier(identifier):
        """Return the Dataset from a identifier"""
        if not isinstance(identifier, MultiTiffVolumeIdentifier):
            raise TypeError(
                f"identifier should be an instance of {MultiTiffVolumeIdentifier}"
            )
        return MultiTIFFVolume(
            file_path=identifier.file_path,
        )

    def get_identifier(self) -> MultiTiffVolumeIdentifier:
        if self.url is None:
            raise ValueError("no file_path provided. Cannot provide an identifier")
        return MultiTiffVolumeIdentifier(object=self, tiff_file=self.url.file_path())

    def volume_data_parent_folder(self):
        if self.data_url is None:
            raise ValueError("data_url doesn't exists")
        else:
            return os.path.dirname(self.data_url.file_path())
