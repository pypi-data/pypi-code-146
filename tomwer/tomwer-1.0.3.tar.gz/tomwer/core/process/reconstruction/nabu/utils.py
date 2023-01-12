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
__date__ = "06/08/2020"


from tomwer.core.scan.edfscan import EDFTomoScan
from tomwer.core.scan.scanbase import TomwerScanBase
from tomwer.core.scan.hdf5scan import HDF5TomoScan
import tomwer.version
from silx.utils.enum import Enum as _Enum
from contextlib import AbstractContextManager
import logging
import datetime
import typing
import os
from tomwer.core.volume.hdf5volume import HDF5Volume
from tomwer.core.volume.edfvolume import EDFVolume
from tomwer.core.volume.jp2kvolume import JP2KVolume
from tomwer.core.volume.tiffvolume import TIFFVolume
from tomwer.core.volume.rawvolume import RawVolume
from nabu.pipeline.fullfield.nabu_config import (
    nabu_config as nabu_fullfield_default_config,
)
from nabu.pipeline.config import generate_nabu_configfile, parse_nabu_config_file

_logger = logging.getLogger(__name__)


class TomwerInfo(AbstractContextManager):
    """Simple context manager to add tomwer metadata to a dict before
    writing it"""

    def __init__(self, config_dict):
        self.config = config_dict

    def __enter__(self):
        self.config["other"] = {
            "tomwer_version": tomwer.version.version,
            "date": datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        }
        return self.config

    def __exit__(self, exc_type, exc_val, exc_tb):
        del self.config["other"]["tomwer_version"]
        del self.config["other"]["date"]


def retrieve_lst_of_value_from_str(my_string: str, type_) -> tuple:
    """
    Return a list of value from a string like '12,23' or '(12, 23)',
    '[12;23]', '12;23' or with the pattern from:to:step like '0:10:1'

    :param str mystring:
    :return: list of single value
    """
    assert type(my_string) is str, "work on string only"
    res = []
    my_string = my_string.replace("(", "")
    my_string = my_string.replace(")", "")
    my_string = my_string.replace("[", "")
    my_string = my_string.replace("]", "")
    if my_string.count(":") == 2:
        _from, _to, _step = my_string.split(":")
        _from, _to, _step = float(_from), float(_to), float(_step)
        if _from > _to:
            tmp = _to
            _to = _from
            _from = tmp
        while _from <= _to:
            res.append(_from)
            _from += _step
        return tuple(res)
    else:
        vals = my_string.replace(" ", "")
        vals = vals.replace("_", "")
        vals = vals.replace(";", ",").split(",")
        for val in vals:
            try:
                res.append(type_(val))
            except Exception:
                pass
        return tuple(res)


def get_nabu_resources_desc(scan: TomwerScanBase, method, workers=1) -> dict:
    """
    Create the descriptor of nabu's resources

    :param TomwerScanBase scan:
    :param str method:
    :return: nabu's description of resources to be used
    """
    assert isinstance(scan, TomwerScanBase)
    res = {
        "method": method,
        "cpu_workers": workers,
        "partition": "gpu",
        "memory_per_node": "90%",
        "threads_per_node": "100%",
        "walltime": "01:00:00",
    }
    return res


def get_nabu_about_desc(overwrite) -> dict:
    """
    Create the description for nabu's about

    :param self:
    :return:
    """
    return {"overwrite_results": str(bool(overwrite))}


def get_recons_volume_identifier(
    file_prefix: str,
    location: str,
    file_format: str,
    scan: TomwerScanBase,
    slice_index: typing.Union[int, None],
    start_z: typing.Union[int, None],
    end_z: typing.Union[int, None],
    expects_single_slice: bool,
) -> tuple:
    """
    return tuple of DataUrl for existings slices
    """
    file_format = file_format.lower()
    if file_format in ("hdf5", "h5", "hdf"):
        if slice_index is not None:
            # case of a single hdf5 file
            file_name = "_".join((file_prefix, str(slice_index).zfill(4)))
        else:
            file_name = file_prefix
        file_name = ".".join((file_name, file_format))
        file_path = os.path.join(location, file_name)

        if isinstance(scan, HDF5TomoScan):
            entry = scan.entry
        elif isinstance(scan, EDFTomoScan):
            entry = "entry"

        volumes = (
            HDF5Volume(
                file_path=file_path,
                data_path="/".join([entry, "reconstruction"]),
            ),
        )
    elif file_format in ("vol", "raw"):
        if slice_index is not None:
            # case of a single hdf5 file
            file_name = "_".join((file_prefix, str(slice_index).zfill(4)))
        else:
            file_name = file_prefix
        volumes = (RawVolume(file_path=file_path),)
    elif file_format in ("jp2", "jp2k", "edf", "tiff"):
        if file_format in ("jp2k", "jp2"):
            constructor = JP2KVolume
        elif file_format == "edf":
            constructor = EDFVolume
        elif file_format == "tiff":
            constructor = TIFFVolume
        else:
            raise NotImplementedError
        output_extension = file_format
        basename = file_prefix

        if slice_index is None and start_z is None and end_z is None:
            # if this is a single slice
            file_path = ".".join(
                (
                    os.path.join(location, file_prefix, file_prefix),
                    output_extension,
                )
            )
            # TODO: in the future we might want to provide data_slice according to z values
            volumes = (
                constructor(
                    folder=os.path.join(location, file_prefix),
                    volume_basename=basename,
                ),
            )
        else:
            volumes = (
                constructor(
                    folder=os.path.join(location, file_prefix),
                    volume_basename=basename,
                ),
            )
    # case of the multitiff. Not handled by tomwer
    # elif file_format == "tiff":
    #     # for single frame tiff nabu uses another convention by saving it 'directly'.
    #     volumes = (
    #         MultiTIFFVolume(
    #             file_path=os.path.join(
    #                 location,
    #                 file_prefix,
    #                 ".".join([file_prefix, file_format]),
    #             ),
    #         ),
    #     )

    else:
        raise ValueError("file format not managed: {}".format(file_format))

    return tuple([volume.get_identifier() for volume in volumes])


class _NabuMode(_Enum):
    FULL_FIELD = "standard acquisition"
    HALF_ACQ = "half acquisition"


class _NabuStages(_Enum):
    INI = "initialization"
    PRE = "pre-processing"
    PHASE = "phase"
    PROC = "processing"
    POST = "post-processing"
    VOLUME = "volume"

    @staticmethod
    def getStagesOrder():
        return (
            _NabuStages.INI,
            _NabuStages.PRE,
            _NabuStages.PHASE,
            _NabuStages.PROC,
            _NabuStages.POST,
        )

    @staticmethod
    def getProcessEnum(stage):
        """Return the process Enum associated to the stage"""
        stage = _NabuStages.from_value(stage)
        if stage is _NabuStages.INI:
            raise NotImplementedError()
        elif stage is _NabuStages.PRE:
            return _NabuPreprocessing
        elif stage is _NabuStages.PHASE:
            return _NabuPhase
        elif stage is _NabuStages.PROC:
            return _NabuProcessing
        elif stage is _NabuStages.POST:
            return _NabuPostProcessing
        raise NotImplementedError()


class _NabuPreprocessing(_Enum):
    """Define all the preprocessing action possible and the order they
    are applied on"""

    FLAT_FIELD_NORMALIZATION = "flat field normalization"
    CCD_FILTER = "hot spot correction"

    @staticmethod
    def getPreProcessOrder():
        return (
            _NabuPreprocessing.FLAT_FIELD_NORMALIZATION,
            _NabuPreprocessing.CCD_FILTER,
        )


class _NabuPhase(_Enum):
    """Define all the phase action possible and the order they
    are applied on"""

    PHASE = "phase retrieval"
    UNSHARP_MASK = "unsharp mask"
    LOGARITHM = "logarithm"

    @staticmethod
    def getPreProcessOrder():
        return (_NabuPhase.PHASE, _NabuPhase.UNSHARP_MASK, _NabuPhase.LOGARITHM)


class _NabuProcessing(_Enum):
    """Define all the processing action possible"""

    RECONSTRUCTION = "reconstruction"

    @staticmethod
    def getProcessOrder():
        return (_NabuProcessing.RECONSTRUCTION,)


class ConfigurationLevel(_Enum):
    REQUIRED = "required"
    OPTIONAL = "optional"
    ADVANCED = "advanced"

    def _get_num_value(self) -> int:
        if self is self.REQUIRED:
            return 0
        elif self is self.OPTIONAL:
            return 1
        elif self is self.ADVANCED:
            return 2

    def __le__(self, other):
        assert isinstance(other, ConfigurationLevel)
        return self._get_num_value() <= other._get_num_value()


class _NabuPostProcessing(_Enum):
    """Define all the post processing action available"""

    SAVE_DATA = "save"

    @staticmethod
    def getProcessOrder():
        return (_NabuPostProcessing.SAVE_DATA,)


class _NabuReconstructionMethods(_Enum):
    FBP = "FBP"


class _NabuPhaseMethod(_Enum):
    """
    Nabu phase method
    """

    PAGANIN = "Paganin"
    NONE = "None"

    @classmethod
    def from_value(cls, value):
        if value in (None, ""):
            return _NabuPhaseMethod.NONE
        else:
            return super().from_value(value=value)


class _NabuFBPFilterType(_Enum):
    RAMLAK = "ramlak"
    SHEPP_LOGAN = "shepp-logan"
    COSINE = "cosine"
    HAMMING = "hamming"
    HANN = "hann"
    TUKEY = "tukey"
    LANCZOS = "lanczos"
    HILBERT = "hilbert"


class _NabuPaddingType(_Enum):
    ZEROS = "zeros"
    EDGES = "edges"


class _RingCorrectionMethod(_Enum):
    NONE = "None"
    MUNCH = "munch"


def nabu_std_err_has_error(errs: typing.Optional[bytes]):
    """
    small util to parse stderr where some warning can exists.
    But I don't think we want to catch all warnings from nabu so this is a (bad) concession
    This will disapear when execution will be done directly from a tomwer thread instead of a subprocess
    """

    def ignore(line) -> bool:
        return "warning" in line or "Warning" in line or line.replace(" ", "") == ""

    if errs is None:
        return False
    else:
        for line in errs.decode("UTF-8").split("\n"):
            if not ignore(line):
                return True
    return False


def update_cfg_file_after_transfer(config_file_path, old_path, new_path):
    """
    update nabu configuration file path from /lbsram/data to /data
    """
    if old_path is None or new_path is None:
        return

    # load configucation file
    config_as_dict = parse_nabu_config_file(config_file_path)
    assert isinstance(config_as_dict, dict)

    # update paths
    paths_to_update = (
        ("dataset", "location"),
        ("output", "location"),
        ("pipeline", "steps_file"),
    )
    for section, field in paths_to_update:
        # update dataset location and output location
        if section in config_as_dict:
            location = config_as_dict[section].get(field, None)
            if location is not None:
                config_as_dict[section][field] = location.replace(old_path, new_path, 1)
    # overwrite file
    generate_nabu_configfile(
        fname=config_file_path,
        default_config=nabu_fullfield_default_config,
        config=config_as_dict,
        options_level="advanced",
    )
