#  Copyright (c) European Space Agency, 2017, 2018, 2019, 2020, 2021, 2022.
#
#  This file is subject to the terms and conditions defined in file 'LICENCE.txt', which
#  is part of this Pyxel package. No part of the package, including
#  this file, may be copied, modified, propagated, or distributed except according to
#  the terms contained in the file ‘LICENCE.txt’.
#
#
#
#  This file is subject to the terms and conditions defined in file 'LICENCE.txt', which
#  is part of this Pyxel package. No part of the package, including
#  this file, may be copied, modified, propagated, or distributed except according to
#  the terms contained in the file ‘LICENCE.txt’.
"""Configuration loader."""

from dataclasses import dataclass
from pathlib import Path
from shutil import copy2
from typing import IO, TYPE_CHECKING, Any, Dict, Iterator, Optional, Sequence, Union

import yaml

from pyxel import __version__ as version
from pyxel.detectors import (
    APD,
    CCD,
    CMOS,
    MKID,
    APDCharacteristics,
    APDGeometry,
    CCDCharacteristics,
    CCDGeometry,
    CMOSCharacteristics,
    CMOSGeometry,
    Environment,
    MKIDCharacteristics,
    MKIDGeometry,
)
from pyxel.exposure import Exposure, Readout
from pyxel.observation import Observation, ParameterValues
from pyxel.outputs import CalibrationOutputs, ExposureOutputs, ObservationOutputs
from pyxel.pipelines import DetectionPipeline, FitnessFunction, ModelFunction

if TYPE_CHECKING:
    from pyxel.calibration import Algorithm, Calibration


@dataclass
class Configuration:
    """Configuration class."""

    pipeline: DetectionPipeline

    # Running modes
    exposure: Optional[Exposure] = None
    observation: Optional[Observation] = None
    calibration: Optional["Calibration"] = None

    # Detectors
    ccd_detector: Optional[CCD] = None
    cmos_detector: Optional[CMOS] = None
    mkid_detector: Optional[MKID] = None
    apd_detector: Optional[APD] = None

    def __post_init__(self):
        # Sanity checks
        running_modes = [self.exposure, self.observation, self.calibration]
        num_running_modes: int = sum(el is not None for el in running_modes)

        if num_running_modes != 1:
            raise ValueError(
                "Expecting only one running mode: "
                "'exposure', 'observation' or 'calibration'."
            )

        detectors = [
            self.ccd_detector,
            self.cmos_detector,
            self.mkid_detector,
            self.apd_detector,
        ]
        num_detectors = sum(el is not None for el in detectors)

        if num_detectors != 1:
            raise ValueError(
                "Expecting only one detector: 'ccd_detector', 'cmos_detector', 'mkid_detector' or 'apd_detector'."
            )

    @property
    def running_mode(self) -> Union[Exposure, Observation, "Calibration"]:
        """Get current running mode."""
        if self.exposure is not None:
            return self.exposure
        elif self.observation is not None:
            return self.observation
        elif self.calibration is not None:
            return self.calibration
        else:
            raise NotImplementedError

    @property
    def detector(self) -> Union[CCD, CMOS, MKID, APD]:
        """Get current detector."""
        if self.ccd_detector is not None:
            return self.ccd_detector
        elif self.cmos_detector is not None:
            return self.cmos_detector
        elif self.mkid_detector is not None:
            return self.mkid_detector
        elif self.apd_detector is not None:
            return self.apd_detector
        else:
            raise NotImplementedError


def load(yaml_file: Union[str, Path]) -> Configuration:
    """Load configuration from a ``YAML`` file.

    Parameters
    ----------
    yaml_file: str or Path

    Returns
    -------
    configuration: Configuration
    """
    filename = Path(yaml_file).resolve()
    if not filename.exists():
        raise FileNotFoundError(f"Cannot find configuration file '{filename}'.")
    with filename.open("r") as file_obj:
        dct = load_yaml(file_obj)

    return _build_configuration(dct)


def loads(yaml_string: str) -> Configuration:
    """Load configuration from a ``YAML`` string.

    Parameters
    ----------
    yaml_string: str

    Returns
    -------
    configuration: Configuration
    """
    dct = load_yaml(yaml_string)
    return _build_configuration(dct)


def load_yaml(stream: Union[str, IO]) -> Any:
    """Load a ``YAML`` document.

    Parameters
    ----------
    stream

    Returns
    -------
    result: dict

    """
    result = yaml.load(stream, Loader=yaml.SafeLoader)
    return result


def to_exposure_outputs(dct: dict) -> ExposureOutputs:
    """Create a ExposureOutputs class from a dictionary.

    Parameters
    ----------
    dct

    Returns
    -------
    ExposureOutputs
    """
    return ExposureOutputs(**dct)


def to_readout(dct: Optional[dict] = None) -> Readout:
    """Create a Readout class from a dictionary.

    Parameters
    ----------
    dct

    Returns
    -------
    Readout
    """
    if dct is None:
        dct = {}
    return Readout(**dct)


def to_exposure(dct: dict) -> Exposure:
    """Create a Exposure class from a dictionary.

    Parameters
    ----------
    dct

    Returns
    -------
    Single
    """
    dct.update({"outputs": to_exposure_outputs(dct["outputs"])})
    dct.update({"readout": to_readout(dct.get("readout"))})

    return Exposure(**dct)


def to_observation_outputs(dct: dict) -> ObservationOutputs:
    """Create a ObservationOutputs class from a dictionary.

    Parameters
    ----------
    dct

    Returns
    -------
    ObservationOutputs
    """
    return ObservationOutputs(**dct)


def to_parameters(dct: dict) -> ParameterValues:
    """Create a ParameterValues class from a dictionary.

    Parameters
    ----------
    dct

    Returns
    -------
    ParameterValues
    """
    return ParameterValues(**dct)


def to_observation(dct: dict) -> Observation:
    """Create a Parametric class from a dictionary.

    Parameters
    ----------
    dct

    Returns
    -------
    Observation
    """
    dct.update(
        {"parameters": [to_parameters(param_dict) for param_dict in dct["parameters"]]}
    )
    dct.update({"outputs": to_observation_outputs(dct["outputs"])})
    dct.update({"readout": to_readout(dct.get("readout"))})

    return Observation(**dct)


def to_calibration_outputs(dct: dict) -> CalibrationOutputs:
    """Create a CalibrationOutputs class from a dictionary.

    Parameters
    ----------
    dct

    Returns
    -------
    CalibrationOutputs
    """
    return CalibrationOutputs(**dct)


def to_algorithm(dct: dict) -> "Algorithm":
    """Create an Algorithm class from a dictionary.

    Parameters
    ----------
    dct

    Returns
    -------
    Algorithm
    """
    # Late import to speedup start-up time
    from pyxel.calibration import Algorithm

    return Algorithm(**dct)


def to_fitness_function(dct: dict) -> FitnessFunction:
    """Create a callable from a dictionary.

    Parameters
    ----------
    dct

    Returns
    -------
    callable
    """
    func: str = dct["func"]

    return FitnessFunction(func=func)


def to_calibration(dct: dict) -> "Calibration":
    """Create a Calibration class from a dictionary.

    Parameters
    ----------
    dct

    Returns
    -------
    Calibration
    """
    # Late import to speedup start-up time
    from pyxel.calibration import Calibration

    dct.update({"outputs": to_calibration_outputs(dct["outputs"])})
    dct.update({"fitness_function": to_fitness_function(dct["fitness_function"])})
    dct.update({"algorithm": to_algorithm(dct["algorithm"])})
    dct.update(
        {"parameters": [to_parameters(param_dict) for param_dict in dct["parameters"]]}
    )
    dct["result_input_arguments"] = [
        to_parameters(value) for value in dct.get("result_input_arguments", {})
    ]
    dct.update({"readout": to_readout(dct.get("readout"))})

    return Calibration(**dct)


def to_ccd_geometry(dct: dict) -> CCDGeometry:
    """Create a CCDGeometry class from a dictionary.

    Parameters
    ----------
    dct

    Returns
    -------
    CCDGeometry
    """

    return CCDGeometry(**dct)


def to_cmos_geometry(dct: dict) -> CMOSGeometry:
    """Create a CMOSGeometry class from a dictionary.

    Parameters
    ----------
    dct

    Returns
    -------
    CMOSGeometry
    """
    return CMOSGeometry(**dct)


def to_mkid_geometry(dct: dict) -> MKIDGeometry:
    """Create a MKIDGeometry class from a dictionary.

    Parameters
    ----------
    dct

    Returns
    -------
    MKIDGeometry
    """
    return MKIDGeometry(**dct)


def to_apd_geometry(dct: dict) -> APDGeometry:
    """Create a APDGeometry class from a dictionary.

    Parameters
    ----------
    dct

    Returns
    -------
    APDGeometry
    """
    return APDGeometry(**dct)


def to_environment(dct: Optional[dict]) -> Environment:
    """Create an Environment class from a dictionary.

    Parameters
    ----------
    dct

    Returns
    -------
    Environment
    """
    if dct is None:
        dct = {}
    return Environment(**dct)


def to_ccd_characteristics(dct: Optional[dict]) -> CCDCharacteristics:
    """Create a CCDCharacteristics class from a dictionary.

    Parameters
    ----------
    dct

    Returns
    -------
    CCDCharacteristics
    """
    if dct is None:
        dct = {}
    return CCDCharacteristics(**dct)


def to_cmos_characteristics(dct: Optional[dict]) -> CMOSCharacteristics:
    """Create a CMOSCharacteristics class from a dictionary.

    Parameters
    ----------
    dct

    Returns
    -------
    CMOSCharacteristics
    """
    if dct is None:
        dct = {}
    return CMOSCharacteristics(**dct)


def to_mkid_characteristics(dct: Optional[dict]) -> MKIDCharacteristics:
    """Create a MKIDCharacteristics class from a dictionary.

    Parameters
    ----------
    dct

    Returns
    -------
    MKIDCharacteristics
    """
    if dct is None:
        dct = {}
    return MKIDCharacteristics(**dct)


def to_apd_characteristics(dct: Optional[dict]) -> APDCharacteristics:
    """Create a APDCharacteristics class from a dictionary.

    Parameters
    ----------
    dct

    Returns
    -------
    APDCharacteristics
    """
    if dct is None:
        dct = {}
    return APDCharacteristics(**dct)


def to_ccd(dct: dict) -> CCD:
    """Create a CCD class from a dictionary.

    Parameters
    ----------
    dct

    Returns
    -------
    CCD
    """
    return CCD(
        geometry=to_ccd_geometry(dct["geometry"]),
        environment=to_environment(dct["environment"]),
        characteristics=to_ccd_characteristics(dct["characteristics"]),
    )


def to_cmos(dct: dict) -> CMOS:
    """Create a :term:`CMOS` class from a dictionary.

    Parameters
    ----------
    dct

    Returns
    -------
    CMOS
    """
    return CMOS(
        geometry=to_cmos_geometry(dct["geometry"]),
        environment=to_environment(dct["environment"]),
        characteristics=to_cmos_characteristics(dct["characteristics"]),
    )


def to_mkid_array(dct: dict) -> MKID:
    """Create an MKIDarray class from a dictionary.

    Parameters
    ----------
    dct

    Returns
    -------
    MKID-array
    """
    return MKID(
        geometry=to_mkid_geometry(dct["geometry"]),
        environment=to_environment(dct["environment"]),
        characteristics=to_mkid_characteristics(dct["characteristics"]),
    )


def to_apd(dct: dict) -> APD:
    """Create an APDarray class from a dictionary.

    Parameters
    ----------
    dct

    Returns
    -------
    MKID-array
    """
    return APD(
        geometry=to_apd_geometry(dct["geometry"]),
        environment=to_environment(dct["environment"]),
        characteristics=to_apd_characteristics(dct["characteristics"]),
    )


def to_model_function(dct: dict) -> ModelFunction:
    """Create a ModelFunction class from a dictionary.

    Parameters
    ----------
    dct

    Returns
    -------
    ModelFunction
    """
    return ModelFunction(**dct)


def to_pipeline(dct: dict) -> DetectionPipeline:
    """Create a DetectionPipeline class from a dictionary.

    Parameters
    ----------
    dct

    Returns
    -------
    DetectionPipeline
    """
    for model_group_name in dct.keys():
        models_list: Optional[Sequence[dict]] = dct[model_group_name]

        if models_list is None:
            models: Optional[Sequence[ModelFunction]] = None
        else:
            models = [to_model_function(model_dict) for model_dict in models_list]

        dct.update({model_group_name: models})
    return DetectionPipeline(**dct)


def _build_configuration(dct: dict) -> Configuration:
    """Create a Configuration class from a dictionary.

    Parameters
    ----------
    dct

    Returns
    -------
    Configuration
    """
    pipeline: DetectionPipeline = to_pipeline(dct["pipeline"])

    # Sanity checks
    keys_running_mode: Sequence[str] = [
        "exposure",
        "observation",
        "calibration",
    ]
    num_running_modes: int = sum(key in dct for key in keys_running_mode)
    if num_running_modes != 1:
        keys = ", ".join(map(repr, keys_running_mode))
        raise ValueError(f"Expecting only one running mode: {keys}")

    keys_detectors: Sequence[str] = [
        "ccd_detector",
        "cmos_detector",
        "mkid_detector",
        "apd_detector",
    ]
    num_detector: int = sum(key in dct for key in keys_detectors)
    if num_detector != 1:
        keys = ", ".join(map(repr, keys_detectors))
        raise ValueError(f"Expecting only one detector: {keys}")

    running_mode: Dict[str, Union[Exposure, Observation, "Calibration"]] = {}
    if "exposure" in dct:
        running_mode["exposure"] = to_exposure(dct["exposure"])
    elif "observation" in dct:
        running_mode["observation"] = to_observation(dct["observation"])
    elif "calibration" in dct:
        running_mode["calibration"] = to_calibration(dct["calibration"])
    else:
        raise ValueError("No mode configuration provided.")

    detector: Dict[str, Union[CCD, CMOS, MKID, APD]] = {}
    if "ccd_detector" in dct:
        detector["ccd_detector"] = to_ccd(dct["ccd_detector"])
    elif "cmos_detector" in dct:
        detector["cmos_detector"] = to_cmos(dct["cmos_detector"])
    elif "mkid_detector" in dct:
        detector["mkid_detector"] = to_mkid_array(dct["mkid_detector"])
    elif "apd_detector" in dct:
        detector["apd_detector"] = to_apd(dct["apd_detector"])
    else:
        raise ValueError("No detector configuration provided.")

    configuration: Configuration = Configuration(
        pipeline=pipeline,
        **running_mode,  # type: ignore
        **detector,  # type: ignore
    )

    return configuration


def save(input_filename: Union[str, Path], output_dir: Path) -> Path:
    """Save a copy of the input ``YAML`` file to output directory.

    Parameters
    ----------
    input_filename: str or Path
    output_dir: Path

    Returns
    -------
    copied_input_file: Path
    """

    input_file = Path(input_filename)
    copy2(input_file, output_dir)

    # TODO: sort filenames ?
    copied_input_file_it: Iterator[Path] = output_dir.glob("*.yaml")
    copied_input_file: Path = next(copied_input_file_it)

    with copied_input_file.open("a") as file:
        file.write("\n#########")
        file.write(f"\n# Pyxel version: {version}")
        file.write("\n#########")

    return copied_input_file
