#  Copyright (c) European Space Agency, 2017, 2018, 2019, 2020, 2021, 2022.
#
#  This file is subject to the terms and conditions defined in file 'LICENCE.txt', which
#  is part of this Pyxel package. No part of the package, including
#  this file, may be copied, modified, propagated, or distributed except according to
#  the terms contained in the file ‘LICENCE.txt’.
#
#
"""Reset noise models."""

from typing import Optional, Tuple

import astropy.constants as const
import numpy as np

from pyxel.detectors import Detector
from pyxel.util import set_random_seed


def compute_ktc_noise(
    temperature: float, capacitance: float, shape: Tuple[int, int]
) -> np.ndarray:
    """Compute KTC noise array.

    Parameters
    ----------
    temperature : float
        Temperature. Unit: K
    capacitance : float
        Node capacitance. Unit: F
    shape : tuple
        Shape of the output array.

    Returns
    -------
    np.ndarray
    """

    rms = np.sqrt(const.k_B.value * temperature / capacitance)

    return np.random.normal(0, rms, shape)


def ktc_noise(
    detector: Detector,
    node_capacitance: Optional[float] = None,
    seed: Optional[int] = None,
) -> None:
    """Apply KTC reset noise to detector signal array.

    Parameters
    ----------
    detector : Detector
        Pyxel detector object.
    node_capacitance : float, optional
        Node capacitance. Unit: F
    seed : int, optional
        Random seed.
    """
    with set_random_seed(seed):
        if node_capacitance is not None:

            if node_capacitance <= 0:
                raise ValueError("Node capacitance should be larger than 0!")

            detector.signal.array += compute_ktc_noise(
                temperature=detector.environment.temperature,
                capacitance=node_capacitance,
                shape=detector.geometry.shape,
            )

        else:
            try:
                capacitance = detector.characteristics.node_capacitance

                detector.signal.array += compute_ktc_noise(
                    temperature=detector.environment.temperature,
                    capacitance=capacitance,
                    shape=detector.geometry.shape,
                )

            except AttributeError as ex:
                raise AttributeError(
                    "Characteristic node_capacitance not available for the detector used. "
                    "Please specify node_capacitance in the model argument!"
                ) from ex
