# coding: utf-8
# /*##########################################################################
#
# Copyright (c) 2016-2022 European Synchrotron Radiation Facility
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
"""module defining utils for an hdf5 volume"""


__authors__ = ["H. Payno", "P. Paleo"]
__license__ = "MIT"
__date__ = "10/01/2023"


import sys
import os
from xml.dom.minidom import parseString as parse_xml_string
import logging
from typing import Optional
import numpy
import h5py
from dicttoxml import dicttoxml
from silx.io.url import DataUrl
from silx.io.dictdump import dicttoini
from tomoscan.scanbase import TomoScanBase
from tomoscan.volumebase import VolumeBase
from tomoscan.esrf.identifier.rawidentifier import RawVolumeIdentifier
from tomoscan.utils import docstring

_logger = logging.getLogger(__name__)


class RawVolume(VolumeBase):
    """
    Volume where data si saved under .vol binary file and metadata are saved in .vol.info and or .vol.xml
    Note: for now reading information from the .xml is not managed. We expect to write one or both and read from the text file (.vol.info)
    Warning: meant as legacy for pyhst .vol file and existing post processing tool. We mostly expect software to write .vol file.
    """

    DEFAULT_DATA_SCHEME = "raw"

    DEFAULT_DATA_EXTENSION = "vol"

    DEFAULT_METADATA_SCHEME = "info"

    DEFAULT_METADATA_EXTENSION = "vol.info"

    def __init__(
        self,
        file_path: Optional[str] = None,
        data: Optional[numpy.ndarray] = None,
        source_scan: Optional[TomoScanBase] = None,
        metadata: Optional[dict] = None,
        data_url: Optional[DataUrl] = None,
        metadata_url: Optional[DataUrl] = None,
        overwrite: bool = False,
        append: bool = False,
        data_extension=DEFAULT_DATA_EXTENSION,
        metadata_extension=DEFAULT_METADATA_EXTENSION,
    ) -> None:
        if file_path is not None:
            url = DataUrl(file_path=file_path, data_path=None, scheme="raw")

        self._file_path = file_path
        super().__init__(
            url=url,
            data=data,
            source_scan=source_scan,
            metadata=metadata,
            data_url=data_url,
            metadata_url=metadata_url,
            overwrite=overwrite,
            data_extension=data_extension,
            metadata_extension=metadata_extension,
        )
        self.append = append

    @property
    def data_extension(self):
        if self.data_url is not None and self.data_url.file_path() is not None:
            return os.path.splitext(self.data_url.file_path())[1]

    @property
    def metadata_extension(self):
        if self.metadata_url is not None and self.metadata_url.file_path() is not None:
            return os.path.splitext(self.metadata_url.file_path())[1]

    @VolumeBase.data.setter
    def data(self, data):
        if not isinstance(data, (numpy.ndarray, type(None), h5py.VirtualLayout)):
            raise TypeError(
                f"data is expected to be None or a numpy array not {type(data)}"
            )
        if isinstance(data, numpy.ndarray) and data.ndim != 3:
            raise ValueError(f"data is expected to be 3D and not {data.ndim}D.")
        self._data = data

    @property
    def file_path(self):
        return self._file_path

    @file_path.setter
    def file_path(self, file_path: Optional[str]):
        if not (file_path is None or isinstance(file_path, str)):
            raise TypeError
        self._file_path = file_path
        self.url = DataUrl(file_path=file_path, data_path=None, scheme="raw")

    @docstring(VolumeBase)
    def deduce_data_and_metadata_urls(self, url: Optional[DataUrl]) -> tuple:
        if url is None:
            return None, None
        else:
            if url.data_slice() is not None:
                raise ValueError(f"data_slice is not handled by the {RawVolume}")
            file_path = url.file_path()
            data_path = url.data_path()
            if data_path is not None:
                raise ValueError("data_path is not handle by the .vol volume.")
            scheme = url.scheme() or "raw"
            metadata_info_file = os.path.splitext(url.file_path())[0] + ".vol.info"
            return (
                # data url
                DataUrl(
                    file_path=file_path,
                    data_path=None,
                    scheme=scheme,
                ),
                # medata url
                DataUrl(
                    file_path=metadata_info_file,
                    data_path=None,
                    scheme=self.DEFAULT_METADATA_SCHEME,
                ),
            )

    @docstring(VolumeBase)
    def save_data(self, url: Optional[DataUrl] = None, **kwargs) -> None:
        if self.data is None:
            return
        url = url or self.data_url
        if url is None:
            raise ValueError(
                "Cannot get data_url. An url should be provided. Don't know where to save this."
            )

        if url.scheme() != "raw":
            raise ValueError("Unsupported scheme - please use scheme='raw'")
        if url.data_path() is not None:
            raise ValueError("No data path expected. Unagleto save data")

        _logger.info(f"save data to {url.path()}")

        if self.data.dtype != numpy.float32:
            raise TypeError(".vol format only takes float32 as data type")

        # check endianness: make sure data is lowbytefirst
        if self.data.dtype.byteorder == ">" or (
            self.data.dtype.byteorder == "=" and sys.byteorder != "little"
        ):
            # lowbytefirst
            raise TypeError("data is expected to be byteorder: low byte first")

        if self.data.ndim == 3:
            data = self.data
        elif self.data.ndim == 2:
            data = self.data.reshape(1, self.data.shape[0], self.data.shape[1])
        else:
            raise ValueError(f"data should be 3D and not {self.data.ndim}D")

        file_mode = "ab" if self.append else "wb"
        with open(url.file_path(), file_mode) as fdesc:
            if self.append:
                n_bytes = os.path.getsize(url.file_path())
                fdesc.seek(n_bytes)
            data.tofile(fdesc)

    @docstring(VolumeBase)
    def load_data(self, url: Optional[DataUrl] = None, store: bool = True) -> None:
        url = url or self.data_url
        if url is None:
            raise ValueError(
                "Cannot get data_url. An url should be provided. Don't know where to save this."
            )

        if self.metadata is None:
            # for .vol file we need metadata to get shape - expected in a .vol.info file
            metadata = self.load_metadata(store=False)
        else:
            metadata = self.metadata

        dimX = metadata.get("NUM_X", None)
        dimY = metadata.get("NUM_Y", None)
        dimZ = metadata.get("NUM_Z", None)
        byte_order = metadata.get("BYTEORDER", "LOWBYTEFIRST")
        if byte_order.lower() == "highbytefirst":
            byte_order = ">"
        elif byte_order.lower() == "lowbytefirst":
            byte_order = "<"
        else:
            raise ValueError(f"Unable to interpret byte order value: {byte_order}")

        if dimX is None or dimY is None or dimZ is None:
            _logger.error(f"Unable to get volume shape (get: {dimZ, dimY, dimZ} )")
            data = None
        else:
            shape = (int(dimZ), int(dimY), int(dimX))
            try:
                data_type = numpy.dtype(byte_order + "f")
                data = numpy.fromfile(
                    url.file_path(), dtype=data_type, count=-1, sep=""
                )
            except Exception as e:
                _logger.warning(
                    f"Fail to load data from {url.file_path()}. Error is {e}."
                )
                data = None
            else:
                data = data.reshape(shape)
                if store is True:
                    self.data = data
        return data

    @docstring(VolumeBase)
    def save_metadata(self, url: Optional[DataUrl] = None, store: bool = True) -> None:
        """
        :raises KeyError: if data path already exists and overwrite set to False
        :raises ValueError: if data is None
        """
        if self.metadata is None:
            raise ValueError("No metadata to be saved")
        url = url or self.metadata_url
        if url is None:
            raise ValueError(
                "Cannot get metadata_url. An url should be provided. Don't know where to save this."
            )
        _logger.info(f"save metadata to {url.path()}")
        if url.scheme() == "info":
            metadata_file = url.file_path()
            _logger.info(f"save data to {metadata_file}")
            if len(self.metadata) > 0:
                # same as ini but no section. Write works but read fails
                dicttoini(self.metadata, metadata_file)
        elif url.scheme() == "lxml":
            metadata_file = url.file_path()
            _logger.info(f"save data to {metadata_file}")
            if len(self.metadata) > 0:
                # Format metadata to a XML file, with a format that can be read by imagej.
                # Does not make sense to you ? For us neither!
                size_xyz = [
                    int(self.metadata.get(key, 0))
                    for key in ["NUM_X", "NUM_Y", "NUM_Z"]
                ]
                if size_xyz == 0:
                    _logger.error(
                        "Something wrong with NUM_X, NUM_Y or NUM_X: missing or zero ?"
                    )
                metadata_for_xml = {
                    "reconstruction": {
                        "idAc": "N_A_",
                        "listSubVolume": {
                            "subVolume": {
                                "SUBVOLUME_NAME": os.path.basename(
                                    self.data_url.file_path()
                                ),
                                "SIZEX": size_xyz[0],
                                "SIZEY": size_xyz[1],
                                "SIZEZ": size_xyz[2],
                                "ORIGINX": 1,
                                "ORIGINY": 1,
                                "ORIGINZ": 1,
                                "DIM_REC": numpy.prod(size_xyz),
                                "BYTE_ORDER": "LOWBYTEFIRST",  # !
                            }
                        },
                    }
                }
                for what in ["voxelSize", "ValMin", "ValMax", "s1", "s2", "S1", "S2"]:
                    metadata_for_xml["reconstruction"]["listSubVolume"]["subVolume"][
                        what
                    ] = float(self.metadata.get(what, 0.0))

                xml_str = dicttoxml(
                    metadata_for_xml,
                    custom_root="tomodb2",
                    xml_declaration=False,
                    attr_type=False,
                    return_bytes=False,
                )
                xml_str_pretty = parse_xml_string(xml_str).toprettyxml(indent="  ")

                with open(metadata_file, mode="w") as file_:
                    file_.write(xml_str_pretty)
        else:
            raise ValueError(f"scheme {url.scheme()} is not handled")

    @docstring(VolumeBase)
    def load_metadata(self, url: Optional[DataUrl] = None, store: bool = True) -> dict:
        url = url or self.metadata_url
        if url is None:
            raise ValueError(
                "Cannot get metadata_url. An url should be provided. Don't know where to save this."
            )
        if url.scheme() == "info":

            def info_file_to_dict(info_file):
                ddict = {}
                with open(info_file, "r") as _file:
                    lines = _file.readlines()
                    for line in lines:
                        if "=" not in line:
                            continue
                        _line = line.rstrip().replace(" ", "")
                        _line = _line.split("#")[0]
                        key, value = _line.split("=")
                        ddict[key] = value
                return ddict

            metadata_file = url.file_path()
            if url.data_path() is not None:
                raise ValueError("data_path is not handled by ini scheme")
            else:
                try:
                    metadata = info_file_to_dict(metadata_file)
                except FileNotFoundError:
                    _logger.warning(f"unable to load metadata from {metadata_file}")
                    metadata = {}
        else:
            raise ValueError(f"scheme {url.scheme()} is not handled")
        if store:
            self.metadata = metadata
        return metadata

    @docstring(VolumeBase)
    def data_file_saver_generator(
        self, n_frames, data_url: DataUrl, overwrite: bool, mode: str = "a", **kwargs
    ):
        """
        warning: the file will be open until the generator exists
        """

        class _FrameDumper:
            """
            will not work for VirtualLayout
            """

            Dataset = None
            # shared dataset

            def __init__(
                self,
                fid,
            ) -> None:
                self._fid = fid

            def __setitem__(self, key, value):
                if key != slice(None, None, None):
                    raise ValueError("item setting only handle ':' for now")
                if not isinstance(value, numpy.ndarray):
                    raise TypeError(
                        "value is expected to be an instance of numpy.ndarray"
                    )
                value.tofile(self._fid)

        if (
            data_url.file_path() is not None
            and os.path.dirname(data_url.file_path()) != ""
        ):
            os.makedirs(os.path.dirname(data_url.file_path()), exist_ok=True)

        with open(self.data_url.file_path(), "wb") as fid:
            for _ in range(n_frames):
                yield _FrameDumper(fid=fid)

    @staticmethod
    @docstring(VolumeBase)
    def from_identifier(identifier):
        """Return the Dataset from a identifier"""
        if not isinstance(identifier, RawVolumeIdentifier):
            raise TypeError(
                f"identifier should be an instance of {RawVolumeIdentifier}"
            )
        return RawVolume(
            file_path=identifier.file_path,
        )

    @docstring(VolumeBase)
    def get_identifier(self) -> RawVolumeIdentifier:
        if self.url is None:
            raise ValueError("no file_path provided. Cannot provide an identifier")
        return RawVolumeIdentifier(object=self, file_path=self.url.file_path())

    @staticmethod
    def example_defined_from_str_identifier() -> str:
        """example as string to explain how users can defined identifiers from a string"""
        return " ; ".join(
            [
                f"{RawVolume(file_path='/path/to/my/my_volume.vol').get_identifier().to_str()}",
            ]
        )
