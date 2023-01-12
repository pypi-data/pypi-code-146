# coding: utf-8
# /*##########################################################################
#
# Copyright (c) 2016-2023 European Synchrotron Radiation Facility
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
__date__ = "11/01/2023"


from tomoscan.esrf.volume.rawvolume import RawVolume as _RawVolume
from tomwer.core.volume.volumebase import TomwerVolumeBase
from tomoscan.esrf.identifier.rawidentifier import (
    RawVolumeIdentifier as _RawVolumeIdentifier,
)
from processview.core.dataset import DatasetIdentifier, Dataset


class RawVolumeIdentifier(_RawVolumeIdentifier, DatasetIdentifier):
    """Identifier specific to .vol volume"""

    def __init__(self, object, file_path):
        super().__init__(object, file_path)
        DatasetIdentifier.__init__(self, RawVolume.from_identifier)

    @staticmethod
    def from_str(identifier):
        return _RawVolumeIdentifier._from_str_to_single_frame_identifier(
            identifier=identifier,
            SingleFrameIdentifierClass=RawVolumeIdentifier,
            ObjClass=RawVolume,
        )


class RawVolume(_RawVolume, TomwerVolumeBase, Dataset):
    @staticmethod
    def from_identifier(identifier):
        """Return the Dataset from a identifier"""
        if not isinstance(identifier, RawVolumeIdentifier):
            raise TypeError(
                f"identifier should be an instance of {RawVolumeIdentifier}"
            )
        return RawVolume(
            file_path=identifier.file_path,
        )

    def get_identifier(self) -> RawVolumeIdentifier:
        if self.url is None:
            raise ValueError("no file_path provided. Cannot provide an identifier")
        return RawVolumeIdentifier(
            object=self,
            file_path=self.url.file_path(),
        )
