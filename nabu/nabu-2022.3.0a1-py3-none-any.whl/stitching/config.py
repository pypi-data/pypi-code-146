# coding: utf-8
# /*##########################################################################
#
# Copyright (c) 2016-2017 European Synchrotron Radiation Facility
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
__date__ = "10/05/2022"


from dataclasses import dataclass
import numpy
from tomoscan.identifier import VolumeIdentifier
from tomoscan.identifier import ScanIdentifier
from tomoscan.nexus.paths import nxtomo
from silx.utils.enum import Enum as _Enum
from typing import Optional, Union
from nabu.pipeline.config_validators import (
    integer_validator,
    list_of_shift_validator,
    list_of_tomoscan_identifier,
    optional_directory_location_validator,
    boolean_validator,
    optional_positive_integer_validator,
    output_file_format_validator,
    optional_tuple_of_floats_validator,
    optional_file_name_validator,
)
from nabu.stitching.overlap import OverlapStichingStrategy
from nabu.utils import concatenate_dict, convert_str_to_tuple
from nabu.io.utils import get_output_volume
from tomoscan.factory import Factory


KEY_X_CROSS_CORRELATION_FUNC = "x_cross_correlation_function"

KEY_Y_CROSS_CORRELATION_FUNC = "y_cross_correlation_function"

KEY_CROSS_CORRELATION_SLICE = "do_slice_index_correlation_from_slice"

_DEFAULT_AUTO_REL_SHIFT_PARAMS = (
    f"{KEY_CROSS_CORRELATION_SLICE}=middle;{KEY_X_CROSS_CORRELATION_FUNC}=skimage;{KEY_Y_CROSS_CORRELATION_FUNC}=None"
)

_OUTPUT_SECTION = "output"

_INPUTS_SECTION = "inputs"

_INPUT_DATASETS_FIELD = "input_dataset"

_STITCHING_SECTION = "stitching"

_STITCHING_STRATEGY_FIELD = "stitching_strategy"

_STITCHING_TYPE_FIELD = "type"

_DATA_FILE_FIELD = "location"

_FILE_PREFIX_FIELD = "file_prefix"

_FILE_FORMAT_FIELD = "file_format"

_OVERWRITE_RESULTS_FIELD = "overwrite_results"

_DATA_PATH_FIELD = "data_path"

_X_RELATIVE_SHIFTS_FIELD = "x_relative_shifts_in_px"

_VERTICAL_OVERLAP_FIELD = "vertical_overlap_area_in_px"

_STITCHING_HEIGTH_FIELD = "stitching_height_in_px"

_AUTO_RELATIVE_SHIFT_PARAMS_FIELD = "auto_relative_shifts_params"

_NEXUS_VERSION_FIELD = "nexus_version"

_OUTPUT_DTYPE = "data_type"

_OUTPUT_VOLUME = "output_volume"


def _str_to_dict(my_str):
    """convert a string as key_1=value_2;key_2=value_2 to a dict"""
    res = {}
    for key_value in my_str.split(";"):
        key, value = key_value.split("=")
        res[key] = value
    return res


def _valid_relative_shift_params(my_dict):
    valid_keys = (
        KEY_CROSS_CORRELATION_SLICE,
        KEY_X_CROSS_CORRELATION_FUNC,
        KEY_Y_CROSS_CORRELATION_FUNC,
    )
    for key in my_dict.keys():
        if not key in valid_keys:
            raise KeyError(f"{key} is a unrecognized key")
    return my_dict


def _str_to_int_or_auto(my_str):
    ids = my_str.replace(" ", "").split(",")
    try:
        res = tuple([int(val) if val not in ("auto", "'auto'", '"auto"') else "auto" for val in ids])
    except ValueError:
        raise ValueError(f"Fail to convert {my_str} to a list of int or to 'auto'")
    else:
        if len(res) == 1:
            return res[0]


@dataclass
class _StitchingConfiguration:
    """
    bass class to define stitching configuration
    """

    overlap_height: Union[int, tuple]  # overlap area in pixel between each scan
    stitching_height: Union[None, int, tuple]  # height to take in the overlap to apply stitching
    stitching_strategy: OverlapStichingStrategy
    output_dtype: numpy.dtype
    overwrite_results: bool
    x_shifts: Union[str, tuple]

    def to_dict(self):
        """dump configuration to a dict. Must be serializable because might be dump to HDF5 file"""
        return {
            _STITCHING_SECTION: {
                _VERTICAL_OVERLAP_FIELD: self.overlap_height,
                _STITCHING_HEIGTH_FIELD: self.stitching_height,
                _STITCHING_STRATEGY_FIELD: OverlapStichingStrategy.from_value(self.stitching_strategy).value,
                _X_RELATIVE_SHIFTS_FIELD: self.x_shifts,
            },
            _OUTPUT_SECTION: {
                _OUTPUT_DTYPE: str(self.output_dtype),
                _OVERWRITE_RESULTS_FIELD: self.overwrite_results,
            },
        }


class StitchingType(_Enum):
    Z_PREPROC = "z-preproc"
    Z_POSTPROC = "z-postproc"


@dataclass
class ZStitchingConfiguration(_StitchingConfiguration):
    """
    base class to define z-stitching parameters
    """

    auto_relative_shift_params: dict

    def to_dict(self):
        return concatenate_dict(
            super().to_dict(),
            {
                _STITCHING_SECTION: {
                    _AUTO_RELATIVE_SHIFT_PARAMS_FIELD: ";".join(
                        [f"{key}={value}" for key, value in self.auto_relative_shift_params.items()]
                    ),
                },
            },
        )


@dataclass
class PreProcessedZStitchingConfiguration(ZStitchingConfiguration):
    """
    base class to define z-stitching parameters
    """

    input_scans: tuple  # tuple of ScanBase
    output_file_path: str
    output_data_path: str
    output_nexus_version: Optional[float]

    def to_dict(self):
        return concatenate_dict(
            super().to_dict(),
            {
                _INPUTS_SECTION: {
                    _INPUT_DATASETS_FIELD: [str(scan.get_identifier()) for scan in self.input_scans],
                },
                _OUTPUT_SECTION: {
                    _DATA_FILE_FIELD: self.output_file_path,
                    _DATA_PATH_FIELD: self.output_data_path,
                    _NEXUS_VERSION_FIELD: self.output_nexus_version,
                },
            },
        )

    @staticmethod
    def from_dict(config: dict):
        if not isinstance(config, dict):
            raise TypeError(f"config is expected to be a dict and not {type(config)}")
        inputs_scans_str = config.get(_INPUTS_SECTION, {}).get(_INPUT_DATASETS_FIELD, None)
        if inputs_scans_str in (None, ""):
            input_scans = []
        else:
            input_scans = _get_identifiers(inputs_scans_str)

        output_file_path = config.get(_OUTPUT_SECTION, {}).get(_DATA_FILE_FIELD, None)
        if output_file_path is None:
            raise ValueError("output location not provided")

        nexus_version = config.get(_OUTPUT_SECTION, {}).get(_NEXUS_VERSION_FIELD, None)
        if nexus_version in (None, ""):
            nexus_version = nxtomo.LATEST_VERSION
        else:
            nexus_version = float(nexus_version)

        return PreProcessedZStitchingConfiguration(
            overlap_height=_str_to_int_or_auto(config[_STITCHING_SECTION][_VERTICAL_OVERLAP_FIELD]),
            stitching_height=_str_to_int_or_auto(config[_STITCHING_SECTION].get(_STITCHING_HEIGTH_FIELD, "auto")),
            stitching_strategy=OverlapStichingStrategy.from_value(
                config[_STITCHING_SECTION].get(
                    _STITCHING_STRATEGY_FIELD,
                    OverlapStichingStrategy.COSINUS_WEIGHTS,
                ),
            ),
            x_shifts=_str_to_int_or_auto(config[_STITCHING_SECTION][_X_RELATIVE_SHIFTS_FIELD]),
            auto_relative_shift_params=_valid_relative_shift_params(
                _str_to_dict(
                    config[_STITCHING_SECTION].get(
                        _AUTO_RELATIVE_SHIFT_PARAMS_FIELD,
                        _DEFAULT_AUTO_REL_SHIFT_PARAMS,
                    ),
                ),
            ),
            input_scans=input_scans,
            output_file_path=output_file_path,
            output_data_path=config.get(_OUTPUT_SECTION, {}).get(_DATA_PATH_FIELD, "entry_from_stitchig"),
            overwrite_results=config[_STITCHING_SECTION].get(_OVERWRITE_RESULTS_FIELD, True),
            output_nexus_version=nexus_version,
            output_dtype=config[_OUTPUT_SECTION].get(_OUTPUT_DTYPE, numpy.float32),
        )


@dataclass
class PostProcessedZStitchingConfiguration(ZStitchingConfiguration):
    """
    base class to define z-stitching parameters
    """

    input_volumes: tuple  # tuple of VolumeBase
    output_volume: VolumeIdentifier

    @staticmethod
    def from_dict(config: dict):
        if not isinstance(config, dict):
            raise TypeError(f"config is expected to be a dict and not {type(config)}")
        inputs_volumes_str = config.get(_INPUTS_SECTION, {}).get(_INPUT_DATASETS_FIELD, None)
        if inputs_volumes_str in (None, ""):
            input_volumes = []
        else:
            input_volumes = _get_identifiers(inputs_volumes_str)

        output_volume = get_output_volume(
            location=config.get(_OUTPUT_SECTION, {}).get(_DATA_FILE_FIELD, None),
            file_prefix=config.get(_OUTPUT_SECTION, {}).get(_FILE_PREFIX_FIELD, None),
            file_format=config.get(_OUTPUT_SECTION, {}).get(_FILE_FORMAT_FIELD, "hdf5"),
        )
        # on the next section the one with a default value qre the optionnal one
        return PostProcessedZStitchingConfiguration(
            overlap_height=config[_STITCHING_SECTION][_VERTICAL_OVERLAP_FIELD],
            stitching_height=config[_STITCHING_SECTION].get(_STITCHING_HEIGTH_FIELD, "auto"),
            stitching_strategy=OverlapStichingStrategy.from_value(
                config[_STITCHING_SECTION].get(
                    _STITCHING_STRATEGY_FIELD,
                    OverlapStichingStrategy.COSINUS_WEIGHTS,
                ),
            ),
            x_shifts=config[_STITCHING_SECTION][_X_RELATIVE_SHIFTS_FIELD],
            auto_relative_shift_params=_valid_relative_shift_params(
                _str_to_dict(
                    config[_STITCHING_SECTION].get(
                        _AUTO_RELATIVE_SHIFT_PARAMS_FIELD,
                        _DEFAULT_AUTO_REL_SHIFT_PARAMS,
                    ),
                ),
            ),
            input_volumes=input_volumes,
            output_volume=output_volume,
            overwrite_results=config[_STITCHING_SECTION].get(_OVERWRITE_RESULTS_FIELD, True),
            output_dtype=config[_OUTPUT_SECTION].get(_OUTPUT_DTYPE, numpy.float32),
        )

    def to_dict(self):
        return concatenate_dict(
            super().to_dict(),
            {
                _INPUTS_SECTION: {
                    _INPUT_DATASETS_FIELD: [str(volume.get_identifier()) for volume in self.input_volumes],
                },
                _OUTPUT_SECTION: {
                    _OUTPUT_VOLUME: self.output_volume,
                },
            },
        )


def _get_identifiers(list_identifiers_as_str: str) -> tuple:
    # convert str to a list of str that should represent identifiers
    identifiers_as_str = convert_str_to_tuple(list_identifiers_as_str)
    # convert identifiers as string to IdentifierType instances
    return [Factory.create_tomo_object_from_identifier(identifier_as_str) for identifier_as_str in identifiers_as_str]


def dict_to_config_obj(config: dict):
    if not isinstance(config, dict):
        raise TypeError
    stitching_type = config.get(_STITCHING_SECTION, {}).get(_STITCHING_TYPE_FIELD, None)
    if stitching_type is None:
        raise ValueError("Unagle to find stitching type from config dict")
    else:
        stitching_type = StitchingType.from_value(stitching_type)
        if stitching_type is StitchingType.Z_POSTPROC:
            return PostProcessedZStitchingConfiguration.from_dict(config)
        elif stitching_type is StitchingType.Z_PREPROC:
            return PreProcessedZStitchingConfiguration.from_dict(config)
        else:
            raise NotImplementedError(f"stitching type {stitching_type.value} not handled yet")


def get_default_stitching_config(stitching_type: Optional[Union[StitchingType, str]]) -> tuple:
    """
    Return a default configuration for doing stitching.

    :param stitching_type: if None then return a configuration were use can provide inputs for any
                           of the stitching.
                           Else return config dict dedicated to a particular stitching
    :return: (config, section comments)
    """
    if stitching_type is None:
        return concatenate_dict(z_postproc_stitching_config, z_preproc_stitching_config)

    stitching_type = StitchingType.from_value(stitching_type)
    if stitching_type is StitchingType.Z_POSTPROC:
        return z_postproc_stitching_config
    elif stitching_type is StitchingType.Z_PREPROC:
        return z_preproc_stitching_config
    else:
        raise NotImplementedError


SECTIONS_COMMENTS = {
    _STITCHING_SECTION: "section dedicated to stich parameters\n",
    _OUTPUT_SECTION: "section dedicated to output parameters\n",
    _INPUTS_SECTION: "section dedicated to inputs\n",
}


_stitching_config = {
    _STITCHING_SECTION: {
        _VERTICAL_OVERLAP_FIELD: {
            "default": "auto",
            "help": "Overlap area between two scans in pixel. Can be an int or a list of int. If 'auto' will try to deduce it from the magnification and z_translations value",
            "type": "required",
            "validator": list_of_shift_validator,
        },
        _STITCHING_HEIGTH_FIELD: {
            "default": "auto",
            "help": "Height of the stich to apply on the overlap region. If set to 'auto' then will take the largest one possible (equal overlap height)",
            "type": "advanced",
            "validator": list_of_shift_validator,
        },
        _STITCHING_STRATEGY_FIELD: {
            "default": "cosinus weights",
            "help": f"Policy to apply to compute the overlap area. Must be in {OverlapStichingStrategy.values()}.",
            "type": "required",
        },
    },
    _OUTPUT_SECTION: {
        _OVERWRITE_RESULTS_FIELD: {
            "default": "1",
            "help": "What to do in the case where the output file exists.\nBy default, the output data is never overwritten and the process is interrupted if the file already exists.\nSet this option to 1 if you want to overwrite the output files.",
            "validator": boolean_validator,
            "type": "required",
        },
    },
    _INPUTS_SECTION: {
        _INPUT_DATASETS_FIELD: {
            "default": "",
            "help": f"Dataset to stitch together. Must be volume for {StitchingType.Z_PREPROC.value} and NXtomo for {StitchingType.Z_POSTPROC.value}",
            "type": "required",
        },
    },
}

_z_stitching_config = concatenate_dict(
    _stitching_config,
    {
        _STITCHING_SECTION: {
            _X_RELATIVE_SHIFTS_FIELD: {
                "default": "auto",
                "help": "relative shift between two set of frames or volumes.",
                "type": "required",
                "validator": list_of_shift_validator,
            },
            _AUTO_RELATIVE_SHIFT_PARAMS_FIELD: {
                "default": _DEFAULT_AUTO_REL_SHIFT_PARAMS,
                "help": "options to find shift automatically",
                "type": "advanced",
            },
        },
    },
)


z_preproc_stitching_config = concatenate_dict(
    {
        _STITCHING_SECTION: {
            _STITCHING_TYPE_FIELD: {
                "default": StitchingType.Z_PREPROC.value,
                "help": f"Which type of stitching to do. Must be in {StitchingType.values}",
                "type": "required",
            },
        },
        _OUTPUT_SECTION: {
            _DATA_FILE_FIELD: {
                "default": "",
                "help": "HDF5 file to save the generated NXtomo (.nx extension recommanded).",
                "validator": optional_directory_location_validator,
                "type": "required",
            },
            _FILE_FORMAT_FIELD: {
                "default": "hdf5",
                "help": "Output file format. Available are: hdf5, tiff, jp2, edf",
                "validator": output_file_format_validator,
                "type": "optional",
            },
            _NEXUS_VERSION_FIELD: {
                "default": "",
                "help": "output NXtomo version to use for saving stitched NXtomo. If not provided will take the latest version available.",
                "type": "optional",
            },
        },
    },
    _z_stitching_config,
)


z_postproc_stitching_config = concatenate_dict(
    {
        _STITCHING_SECTION: {
            _STITCHING_TYPE_FIELD: {
                "default": StitchingType.Z_POSTPROC.value,
                "help": f"Which type of stitching to do. Must be in {StitchingType.values}",
                "type": "required",
            },
        },
        _OUTPUT_SECTION: {
            _DATA_FILE_FIELD: {
                "default": "",
                "help": "Directory where the output reconstruction is stored.",
                "validator": optional_directory_location_validator,
                "type": "required",
            },
            _FILE_PREFIX_FIELD: {
                "default": "",
                "help": "File prefix. Optional, by default it is inferred from the scanned dataset.",
                "validator": optional_file_name_validator,
                "type": "optional",
            },
            _FILE_FORMAT_FIELD: {
                "default": "hdf5",
                "help": "Output file format. Available are: hdf5, tiff, jp2, edf",
                "validator": output_file_format_validator,
                "type": "optional",
            },
        },
    },
    _z_stitching_config,
)
