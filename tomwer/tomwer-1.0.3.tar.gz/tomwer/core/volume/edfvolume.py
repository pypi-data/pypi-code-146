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


from tomoscan.esrf.volume.edfvolume import EDFVolume as _EDFVolume
from tomwer.core.volume.volumebase import TomwerVolumeBase
from tomoscan.esrf.identifier.edfidentifier import (
    EDFVolumeIdentifier as _EDFVolumeIdentifier,
)
from processview.core.dataset import DatasetIdentifier, Dataset


class EDFVolumeIdentifier(_EDFVolumeIdentifier, DatasetIdentifier):
    def __init__(self, object, folder, file_prefix):
        super().__init__(object, folder, file_prefix)
        DatasetIdentifier.__init__(self, data_builder=EDFVolume.from_identifier)

    @staticmethod
    def from_str(identifier):
        return _EDFVolumeIdentifier._from_str_to_single_frame_identifier(
            identifier=identifier,
            SingleFrameIdentifierClass=EDFVolumeIdentifier,
            ObjClass=EDFVolume,
        )


class EDFVolume(_EDFVolume, TomwerVolumeBase, Dataset):
    @staticmethod
    def from_identifier(identifier):
        """Return the Dataset from a identifier"""
        if not isinstance(identifier, EDFVolumeIdentifier):
            raise TypeError(
                f"identifier should be an instance of {EDFVolumeIdentifier} and not {type(identifier)}"
            )
        return EDFVolume(
            folder=identifier.folder,
            volume_basename=identifier.file_prefix,
        )

    def get_identifier(self) -> EDFVolumeIdentifier:
        if self.url is None:
            raise ValueError("no file_path provided. Cannot provide an identifier")
        return EDFVolumeIdentifier(
            object=self, folder=self.url.file_path(), file_prefix=self._volume_basename
        )
