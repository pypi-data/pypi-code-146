#!/usr/bin/env python3

"""
Radio occultation.
"""

import warnings
from pathlib import Path

from pudb import set_trace as bp  # noqa: F401

import radiocc
from radiocc import constants, export, old, process_parser, reconstruct
from radiocc.model import ResultsFolders, Scenario
from radiocc.old import R17_Plot_profiles


def enable_gui() -> None:
    """Run radiocc with graphical interface."""
    radiocc.gui = radiocc.interface.Interface()


def run() -> None:
    """Run radiocc."""
    if (
        radiocc.cfg.graphical_interface
        and radiocc.gui is None
        and not radiocc.cfg.quick_trace
    ):
        enable_gui()

    check_cfg()

    if radiocc.cfg.quick_trace:
        radiocc.cfg.bands = radiocc.cfg.bands[:1]
        radiocc.cfg.layers = radiocc.cfg.layers[:1]

    TO_PROCESS_DIRS = list(
        radiocc.utils.directories(
            radiocc.cfg.to_process,
            EXCLUDES=[
                ".*",
                "spice-maven",
                "spice-maven-old",
                "spice-maven-alternative",
                "temporary-download-location",
            ],
        )
    )

    if not len(TO_PROCESS_DIRS):
        warnings.warn(f"{radiocc.cfg.to_process} directory is empty.", Warning)

    for INDEX_PROCESS, PROCESS_PATH in enumerate(TO_PROCESS_DIRS):
        print(f"Reading {PROCESS_PATH.name}..")

        for BAND in radiocc.cfg.bands:
            print(f"  Band: {BAND.name}")

            for LAYER in radiocc.cfg.layers:
                print(f"    Layer: {LAYER.name}")

                SCENARIO = Scenario(PROCESS_PATH, BAND, LAYER, INDEX_PROCESS)

                run_scenario(SCENARIO)

            band_export(SCENARIO)

    if radiocc.gui is not None:
        radiocc.gui.label_data.set_label("FINISHED!")
        radiocc.gui.mainloop()


def run_scenario(SCENARIO: Scenario) -> None:
    """Run a scenario."""
    if radiocc.gui is not None:
        radiocc.gui.label_data.set_label(
            f"PROCESSING {SCENARIO.TO_PROCESS.name} "
            f"Band:{SCENARIO.BAND.value} Layer:{SCENARIO.LAYER.value}..."
        )
        radiocc.gui.draw()

    process_parser.prepare_directories(SCENARIO)
    FOLDER_TYPE = process_parser.detect_folder_type(SCENARIO.TO_PROCESS)

    if FOLDER_TYPE is None:
        return None

    process_parser.load_spice_kernels(SCENARIO, FOLDER_TYPE)
    L2_DATA = process_parser.read_L2_data(SCENARIO, FOLDER_TYPE)

    if L2_DATA is None:
        return None

    process_parser.show_info(L2_DATA)
    process_parser.filtering(L2_DATA)

    EXPORT = reconstruct.run(SCENARIO, L2_DATA)

    if not radiocc.cfg.quick_trace:
        export.run(SCENARIO, L2_DATA, EXPORT)


def band_export(SCENARIO: Scenario) -> None:
    """Finish the plots for the layers of a scenario."""
    if radiocc.cfg.quick_trace:
        return

    # Interface with old code.
    RESULTS = SCENARIO.results(radiocc.cfg.results)
    i_Profile = SCENARIO.INDEX_PROCESS
    DATA_PRO = str(SCENARIO.TO_PROCESS.parent)
    DATA_ID = str(SCENARIO.TO_PROCESS.resolve())
    CODE_DIR = str(Path(old.__file__).parent.resolve())
    DATA_DIR = str(SCENARIO.TO_PROCESS.parent.parent.resolve())
    PLOT_DIR = str((RESULTS / ResultsFolders.PLOTS.name).resolve())
    DATA_FINAL_DIR = str((RESULTS / ResultsFolders.DATA.name).resolve())

    R17_Plot_profiles.PLOT2(  # type: ignore [no-untyped-call]
        DATA_ID,
        i_Profile,
        DATA_PRO,
        CODE_DIR,
        SCENARIO.BAND.name,
        DATA_DIR,
        constants.Threshold_Cor,
        constants.Threshold_Surface,
        DATA_FINAL_DIR,
        PLOT_DIR,
        constants.Threshold_int,
    )


def check_cfg() -> None:
    """Check if cfg is correct."""
    # Check if to_process directory exists.
    if not radiocc.cfg.to_process.is_dir():
        raise FileNotFoundError(
            "You need to create a directory for the data to be processed. "
            "Please create a directory named `to_process`. You can also "
            "customise the name of the folder but you need to change it also "
            "in the config `radiocc.cfg`."
        )
