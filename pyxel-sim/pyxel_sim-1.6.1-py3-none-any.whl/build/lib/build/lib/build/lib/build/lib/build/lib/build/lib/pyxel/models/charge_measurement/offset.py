#  Copyright (c) European Space Agency, 2017, 2018, 2019, 2020, 2021, 2022.
#
#  This file is subject to the terms and conditions defined in file 'LICENCE.txt', which
#  is part of this Pyxel package. No part of the package, including
#  this file, may be copied, modified, propagated, or distributed except according to
#  the terms contained in the file ‘LICENCE.txt’.
#
#
"""Voltage offset models."""

from typing import Tuple

import numpy as np

from pyxel.detectors import APD, Detector


def compute_dc_offset(offset: float, shape: Tuple[int, int]) -> np.ndarray:
    """Compute DC offset voltage array.

    Parameters
    ----------
    offset : float
        DC voltage offset. Unit: V
    shape : tuple
        Shape of the output array.

    Returns
    -------
    np.ndarray
    """
    return np.ones(shape) * offset


def dc_offset(detector: Detector, offset: float) -> None:
    """Apply DC voltage to the detector.

    Parameters
    ----------
    detector : Detector
        Pyxel Detector object.
    offset : float
        DC offset voltage. Unit: V
    """

    if (
        not min(detector.characteristics.adc_voltage_range)
        < offset
        < max(detector.characteristics.adc_voltage_range)
    ):
        raise ValueError("Parameter 'offset' out of bonds of the ADC voltage range.")

    detector.signal.array += compute_dc_offset(offset, detector.geometry.shape)


def compute_output_pixel_reset_voltage_apd(
    roic_drop: float,
    roic_gain: float,
    pixel_reset_voltage: float,
    shape: Tuple[int, int],
) -> np.ndarray:
    """Compute output pixel reset voltage.

    Parameters
    ----------
    roic_drop : float
        Readout circuit drop voltage. Unit: V
    roic_gain : float
        Readout circuit gain.
    pixel_reset_voltage
        Pixel reset voltage. Unit: V
    shape : tuple
        Shape of output array.

    Returns
    -------
    np.ndarray
    """

    value = (roic_gain * pixel_reset_voltage) - (
        roic_drop * roic_gain
    )  # Reproduces linear plot of PRV vs. output voltage

    return np.ones(shape) * value


def output_pixel_reset_voltage_apd(detector: APD, roic_drop: float) -> None:
    """Apply output pixel reset voltage to APD detector.

    Parameters
    ----------
    detector : APD
        Pyxel APD object.
    roic_drop : float
        Readout circuit drop voltage. Unit: V
    """
    if not isinstance(detector, APD):
        raise TypeError("Expecting a 'APD' detector object.")

    ch = detector.characteristics
    shape = detector.geometry.shape

    offset = compute_output_pixel_reset_voltage_apd(
        roic_drop=roic_drop,
        roic_gain=ch.roic_gain,
        pixel_reset_voltage=ch.pixel_reset_voltage,
        shape=shape,
    )

    if (
        not min(detector.characteristics.adc_voltage_range)
        < offset[0, 0]
        < max(detector.characteristics.adc_voltage_range)
    ):
        raise ValueError(
            "Output pixel reset voltage out of bonds of the ADC voltage range."
        )

    detector.signal.array += max(ch.adc_voltage_range) - offset
