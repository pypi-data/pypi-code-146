# coding: utf-8
# /*##########################################################################
# Copyright (C) 2016 European Synchrotron Radiation Facility
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
#############################################################################*/


__authors__ = ["H.Payno"]
__license__ = "MIT"
__date__ = "13/07/2022"


from urllib.parse import urlparse
from typing import Union
from tomoscan.factory import Factory as _oVolumeFactory
from tomoscan.esrf.identifier.url_utils import split_path
from tomoscan.identifier import BaseIdentifier, ScanIdentifier, VolumeIdentifier
from tomoscan import identifier as _identifier_mod
from tomwer.core.volume.edfvolume import EDFVolumeIdentifier
from tomwer.core.scan.edfscan import EDFTomoScanIdentifier
from tomwer.core.volume.hdf5volume import HDF5VolumeIdentifier
from tomwer.core.volume.jp2kvolume import JP2KVolumeIdentifier
from tomwer.core.volume.tiffvolume import (
    TIFFVolumeIdentifier,
    MultiTiffVolumeIdentifier,
)
from tomwer.core.volume.rawvolume import RawVolumeIdentifier
from tomwer.core.volume import (
    HDF5Volume,
    EDFVolume,
    MultiTIFFVolume,
    TIFFVolume,
    JP2KVolume,
    RawVolume,
)
from tomwer.core.scan.edfscan import EDFTomoScan
from tomwer.core.scan.hdf5scan import HDF5TomoScan
from tomwer.utils import docstring
import logging

_logger = logging.getLogger(__name__)


class VolumeFactory(_oVolumeFactory):
    @docstring(_oVolumeFactory.create_tomo_object_from_identifier)
    @staticmethod
    def create_tomo_object_from_identifier(identifier: Union[str, BaseIdentifier]):
        """

        :param TextIOWrapper scan_path: path to the scan directory or file
        :param entry: entry on the file. Requested for hdf5 files
        :param accept_bliss_scan: if True the factory can return some BlissScan
                                  But this is only compatible with the
                                  Tomomill processing.
        :return: TomwerScanBase instance fitting the scan folder or scan path
        :rtype: tomwer.core.scan.scanbase.TomwerScanBase
        :raises: ValueError if scan_path is not containing a scan
        """
        if not isinstance(identifier, (str, BaseIdentifier)):
            raise TypeError(
                f"identifier is expected to be a str or an instance of {BaseIdentifier} not {type(identifier)}"
            )

        # step 1: convert identifier to an instance of BaseIdentifier if necessary
        if isinstance(identifier, str):
            info = urlparse(identifier)
            paths = split_path(info.path)
            scheme = info.scheme
            if len(paths) == 1:
                # insure backward compatibility. Originally (until 0.8) there was only one type which was scan
                tomo_type = ScanIdentifier.TOMO_TYPE
            elif len(paths) == 2:
                tomo_type, _ = paths
            else:
                raise ValueError("Failed to parse path string:", info.path)

            if tomo_type == _identifier_mod.VolumeIdentifier.TOMO_TYPE:
                if scheme == "edf":
                    identifier = EDFVolumeIdentifier.from_str(identifier=identifier)
                elif scheme == "hdf5":
                    identifier = HDF5VolumeIdentifier.from_str(identifier=identifier)
                elif scheme == "tiff":
                    identifier = TIFFVolumeIdentifier.from_str(identifier=identifier)
                elif scheme == "tiff3d":
                    identifier = MultiTiffVolumeIdentifier.from_str(
                        identifier=identifier
                    )
                elif scheme == "jp2k":
                    identifier = JP2KVolumeIdentifier.from_str(identifier=identifier)
                elif scheme in ("raw", "vol"):
                    identifier = RawVolumeIdentifier.from_str(identifier=identifier)
                else:
                    raise ValueError(f"Scheme {scheme} is not recognized")

            elif tomo_type == _identifier_mod.ScanIdentifier.TOMO_TYPE:
                # otherwise consider this is a scan. Insure backward compatibility
                if scheme == "edf":
                    identifier = EDFTomoScanIdentifier.from_str(identifier=identifier)
                elif scheme == "hdf5":
                    identifier = HDF5VolumeIdentifier.from_str(identifier=identifier)
                else:
                    raise ValueError(f"Scheme {scheme} not recognized")
            else:
                raise ValueError(f"{tomo_type} is not an handled tomo type")

        # step 2: convert identifier to a TomoBaseObject
        assert isinstance(identifier, BaseIdentifier)
        scheme = identifier.scheme
        tomo_type = identifier.tomo_type

        if scheme == "edf":
            if tomo_type == VolumeIdentifier.TOMO_TYPE:
                return EDFVolume.from_identifier(identifier=identifier)
            elif tomo_type == ScanIdentifier.TOMO_TYPE:
                return EDFTomoScan.from_identifier(identifier=identifier)
            else:
                raise NotImplementedError()
        elif scheme == "hdf5":
            if tomo_type == VolumeIdentifier.TOMO_TYPE:
                return HDF5Volume.from_identifier(identifier=identifier)
            elif tomo_type == ScanIdentifier.TOMO_TYPE:
                return HDF5TomoScan.from_identifier(identifier=identifier)
            else:
                raise NotImplementedError()
        elif scheme == "jp2k":
            if tomo_type == VolumeIdentifier.TOMO_TYPE:
                return JP2KVolume.from_identifier(identifier=identifier)
            else:
                raise NotImplementedError
        elif scheme == "tiff":
            if tomo_type == VolumeIdentifier.TOMO_TYPE:
                return TIFFVolume.from_identifier(identifier=identifier)
            else:
                raise NotImplementedError
        elif scheme == "tiff3d":
            if tomo_type == VolumeIdentifier.TOMO_TYPE:
                return MultiTIFFVolume.from_identifier(identifier=identifier)
            else:
                raise NotImplementedError
        elif scheme in ("raw", "vol"):
            if tomo_type == VolumeIdentifier.TOMO_TYPE:
                return RawVolume.from_identifier(identifier=identifier)
            else:
                raise NotImplementedError
        else:
            raise ValueError(f"Scheme {scheme} not recognized")
