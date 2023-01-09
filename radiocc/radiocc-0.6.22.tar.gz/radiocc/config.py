#!/usr/bin/env python3

"""
Configurate parameters.
"""

from pathlib import Path
from typing import Any, Dict, Optional

import arrow
import yaml
from dotmap import DotMap
from pudb import set_trace as bp  # noqa: F401

import radiocc
from radiocc.model import Bands, KernelVersion, Layers, ProcessType, RadioDataType


class Cfg:
    """Structure representation of the configurable parameters."""

    __KEYS_ORDER = [
        "to_process",
        "results",
        "bands",
        "layers",
        "graphical_interface",
        "quick_trace",
        "filter",
        "skip_correction_guess",
        "interactive_download",
        "mission",
        "kernel_version",
        "radio_data_type",
        "datefmt",
        "date",
    ]

    # Configurable parameters default values.
    __DEFAULT_TO_PROCESS = Path("./to_process")
    __DEFAULT_RESULTS = Path("./results")
    __DEFAULT_MISSION = ProcessType.MAVEN
    __DEFAULT_BANDS = [
        Bands.X,
    ]
    __DEFAULT_LAYERS = [Layers.Iono, Layers.Atmo]
    __DEFAULT_DATEFMT = "YYYY-MMM-DD HH:mm:ss"
    __DEFAULT_DATE = arrow.get("2017-Jan-06 21:13:01", __DEFAULT_DATEFMT)
    __DEFAULT_INTERACTIVE_DOWNLOAD = True
    __DEFAULT_KERNEL_VERSION = KernelVersion.LATEST
    __DEFAULT_RADIO_DATA_TYPE = RadioDataType.INGRESS
    __DEFAULT_GRAPHICAL_INTERFACE = False
    __DEFAULT_QUICK_TRACE = False
    __DEFAULT_FILTER = False
    __DEFAULT_SKIP_CORRECTION_GUESS = False

    # Path to the folder containing the data to be processed.
    __to_process = __DEFAULT_TO_PROCESS

    # Path to the folder where you want the outputs to be saved.
    __results = __DEFAULT_RESULTS

    # Type of the mission.
    __mission = __DEFAULT_MISSION

    # Bands.
    __bands = __DEFAULT_BANDS

    # Layers.
    __layers = __DEFAULT_LAYERS

    # Date format.
    __datefmt = __DEFAULT_DATEFMT

    # Date.
    __date = __DEFAULT_DATE

    # Whether the download of the data should be done interactively.
    __interactive_download = __DEFAULT_INTERACTIVE_DOWNLOAD

    # kernel version mode.
    __kernel_version = __DEFAULT_KERNEL_VERSION

    # Type of the radio data.
    __radio_data_type = __DEFAULT_RADIO_DATA_TYPE

    # Whether to use the graphical interface.
    __graphical_interface = __DEFAULT_GRAPHICAL_INTERFACE

    # Whether to run the code to compute quick trace.
    __quick_trace = __DEFAULT_QUICK_TRACE

    # Whether data should be filtered.
    __filter = __DEFAULT_FILTER

    # Whether the first correction guess should be skipped.
    __skip_correction_guess = __DEFAULT_SKIP_CORRECTION_GUESS

    def __init__(self) -> None:
        pass

    def load_config_file(self) -> None:
        """Load the config file."""
        if radiocc.CFG_PATH.is_file():
            CFG_FILE = radiocc.utils.read_yaml(radiocc.CFG_PATH)
            self.__parse_config_file(CFG_FILE)

    def __parse_config_file(self, CFG_FILE: DotMap) -> None:  # noqa: C901
        """Apply variables from the config to the actual config."""
        if CFG_FILE["to_process"] not in (None, DotMap()):
            self.to_process = Path(CFG_FILE["to_process"])

        if CFG_FILE["results"] not in (None, DotMap()):
            self.results = Path(CFG_FILE["results"])

        if CFG_FILE["mission"] not in (None, DotMap()):
            self.mission = ProcessType(CFG_FILE["mission"])

        if CFG_FILE["bands"] not in (None, DotMap()):
            self.bands = [Bands(BAND) for BAND in CFG_FILE["bands"]]

        if CFG_FILE["layers"] not in (None, DotMap()):
            self.layers = [Layers(LAYER) for LAYER in CFG_FILE["layers"]]

        if CFG_FILE["datefmt"] not in (None, DotMap()):
            self.datefmt = CFG_FILE["datefmt"]

        if CFG_FILE["date"] not in (None, DotMap()):
            self.date = arrow.get(CFG_FILE["date"], self.datefmt)

        if CFG_FILE["interactive_download"] not in (None, DotMap()):
            self.interactive_download = CFG_FILE["interactive_download"]

        if CFG_FILE["kernel_version"] not in (None, DotMap()):
            self.kernel_version = KernelVersion(CFG_FILE["kernel_version"])

        if CFG_FILE["radio_data_type"] not in (None, DotMap()):
            self.radio_data_type = RadioDataType(CFG_FILE["radio_data_type"])

        if CFG_FILE["graphical_interface"] not in (None, DotMap()):
            self.graphical_interface = CFG_FILE["graphical_interface"]

        if CFG_FILE["quick_trace"] not in (None, DotMap()):
            self.quick_trace = CFG_FILE["quick_trace"]

        if CFG_FILE["filter"] not in (None, DotMap()):
            self.filter = CFG_FILE["filter"]

        if CFG_FILE["skip_correction_guess"] not in (None, DotMap()):
            self.skip_correction_guess = CFG_FILE["skip_correction_guess"]

    def to_dict(self, DEFAULT_ARE_NONE: bool = False) -> Dict[str, Optional[Any]]:
        """Convert config to hashmap."""
        if DEFAULT_ARE_NONE:
            return dict(
                to_process=None,
                results=None,
                mission=None,
                bands=None,
                layers=None,
                datefmt=None,
                date=None,
                interactive_download=None,
                kernel_version=None,
                radio_data_type=None,
                graphical_interface=None,
                quick_trace=None,
                filter=None,
                skip_correction_guess=None,
            )
        else:
            return dict(
                to_process=str(self.to_process),
                results=str(self.results),
                mission=self.mission.name,
                bands=[BAND.name for BAND in self.bands],
                layers=[LAYER.name for LAYER in self.layers],
                datefmt=self.datefmt,
                date=self.date.format(self.datefmt),
                interactive_download=self.interactive_download,
                kernel_version=self.kernel_version.name,
                radio_data_type=self.radio_data_type.name,
                graphical_interface=self.graphical_interface,
                quick_trace=self.quick_trace,
                filter=self.filter,
                skip_correction_guess=self.skip_correction_guess,
            )

    @property
    def to_process(self) -> Path:
        """Get to_process folder path."""
        return self.__to_process

    @to_process.setter
    def to_process(self, PATH: Path) -> None:
        """Set to_process folder path."""
        self.__to_process = PATH

    @property
    def results(self) -> Path:
        """Get results folder path."""
        return self.__results

    @results.setter
    def results(self, PATH: Path) -> None:
        """Set results folder path."""
        self.__results = PATH

    @property
    def mission(self) -> ProcessType:
        """Get mission type."""
        return self.__mission

    @mission.setter
    def mission(self, TYPE: ProcessType) -> None:
        """Set mission type."""
        self.__mission = TYPE

    @property
    def bands(self) -> list[Bands]:
        """Get bands."""
        return self.__bands

    @bands.setter
    def bands(self, BANDS: list[Bands]) -> None:
        """Set bands."""
        self.__bands = BANDS

    @property
    def layers(self) -> list[Layers]:
        """Get layers."""
        return self.__layers

    @layers.setter
    def layers(self, LAYERS: list[Layers]) -> None:
        """Set layers."""
        self.__layers = LAYERS

    @property
    def datefmt(self) -> str:
        """Get date format."""
        return self.__datefmt

    @datefmt.setter
    def datefmt(self, FMT: str) -> None:
        """Set date format."""
        self.__datefmt = FMT

    @property
    def date(self) -> arrow.Arrow:
        """Get date folder path."""
        return self.__date

    @date.setter
    def date(self, DATE: arrow.Arrow) -> None:
        """Set date folder path."""
        self.__date = DATE

    @property
    def interactive_download(self) -> bool:
        """Get whether the download of the data should be done interactively."""
        return self.__interactive_download

    @interactive_download.setter
    def interactive_download(self, DO_INTERACTIVE: bool) -> None:
        """Set whether the download of the data should be done interactively."""
        self.__interactive_download = DO_INTERACTIVE

    @property
    def kernel_version(self) -> KernelVersion:
        """Get kernel_version mode."""
        return self.__kernel_version

    @kernel_version.setter
    def kernel_version(self, MODE: KernelVersion) -> None:
        """Set kernel_version mode."""
        self.__kernel_version = MODE

    @property
    def radio_data_type(self) -> RadioDataType:
        """Get radio data type."""
        return self.__radio_data_type

    @radio_data_type.setter
    def radio_data_type(self, TYPE: RadioDataType) -> None:
        """Set radio data type."""
        self.__radio_data_type = TYPE

    @property
    def graphical_interface(self) -> bool:
        """Get whether the graphical interface is used."""
        return self.__graphical_interface

    @graphical_interface.setter
    def graphical_interface(self, VALUE: bool) -> None:
        """Set whether to use the graphical interface."""
        self.__graphical_interface = VALUE

    @property
    def quick_trace(self) -> bool:
        """Get whether to run the code to compute quick trace."""
        return self.__quick_trace

    @quick_trace.setter
    def quick_trace(self, VALUE: bool) -> None:
        """Set whether to run the code to compute quick trace."""
        self.__quick_trace = VALUE

    @property
    def filter(self) -> bool:
        """Get whether data should be filtered."""
        return self.__filter

    @filter.setter
    def filter(self, VALUE: bool) -> None:
        """Set whether data should be filtered."""
        self.__filter = VALUE

    @property
    def skip_correction_guess(self) -> bool:
        """Get whether the correction guess should be skipped."""
        return self.__skip_correction_guess

    @skip_correction_guess.setter
    def skip_correction_guess(self, VALUE: bool) -> None:
        """Set whether the correction guess should be skipped."""
        self.__skip_correction_guess = VALUE

    def generate_config(self, FORCE_OVERWRITE: bool = False) -> None:
        """Generate a config file `radiocc.yaml` in the current directory."""
        # Create empty config as dict of nones.
        CFG = self.to_dict()

        # Change all None to empty.
        radiocc.utils.yaml_add_representer_none()

        # Check whether config should be saved.
        save = True
        if radiocc.CFG_PATH.is_file() and not FORCE_OVERWRITE:
            save = radiocc.utils.form_yes_or_no(f"Overwrite {radiocc.CFG_PATH}?")

        # Save as a new config file.
        if save:
            for INDEX, KEY in enumerate(self.__KEYS_ORDER):
                with open(radiocc.CFG_PATH, "w" if INDEX == 0 else "a") as fp:
                    yaml.dump({KEY: CFG[KEY]}, fp)
