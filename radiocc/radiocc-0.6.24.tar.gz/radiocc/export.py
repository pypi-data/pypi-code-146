#!/usr/bin/env python3

"""
Export the graphs and text output.
"""

from typing import Optional  # noqa

import numpy
from nptyping import NDArray
from pudb import set_trace as bp  # noqa

from radiocc.model import Export, L2Data, Scenario


def run(SCENARIO: Scenario, L2DATA: L2Data, OUT: Export) -> None:
    """Export results."""

    PATH_FILTER = f"{SCENARIO.BAND.name}-{SCENARIO.LAYER.name.upper()}-%d.txt"
    COUNT = len(list(OUT.DATA_PATH.glob(PATH_FILTER)))
    PATH_OUT = OUT.DATA_PATH / (PATH_FILTER % (COUNT + 1))

    output: NDArray = numpy.stack(
        (
            OUT.ET,
            OUT.DOPPLER,
            OUT.DOPPLER_DEBIAS,
            OUT.DOPPLER_BIAS_FIT,
            OUT.DISTANCE,
            OUT.ALTITUDE,
            OUT.REFRACTIVITY,
            OUT.NE,
            OUT.ERROR,
            OUT.ERROR_REFRAC,
            OUT.ERROR_ELEC,
            OUT.BEND_RADIUS,
        ),
        axis=1,
    )

    if OUT.TEC is not None:
        output = numpy.concatenate((output, OUT.TEC[:, None]), axis=1)

    if OUT.PT is not None:
        output = numpy.concatenate(
            (
                output,
                OUT.PT.P_low[:, None],
                OUT.PT.P_med[:, None],
                OUT.PT.P_upp[:, None],
                OUT.PT.T_low[:, None],
                OUT.PT.T_med[:, None],
                OUT.PT.T_upp[:, None],
            ),
            axis=1,
        )

    numpy.savetxt(
        PATH_OUT,
        output,
        fmt="%.18e",
        delimiter=" ",
        newline="\n",
        header="",
        footer="",
        comments="# ",
    )
