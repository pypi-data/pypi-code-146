#  Copyright (c) European Space Agency, 2017, 2018, 2019, 2020, 2021, 2022.
#
#  This file is subject to the terms and conditions defined in file 'LICENCE.txt', which
#  is part of this Pyxel package. No part of the package, including
#  this file, may be copied, modified, propagated, or distributed except according to
#  the terms contained in the file ‘LICENCE.txt’.

"""Simple models to generate charge due to dark current process."""
import warnings
from typing import Optional, Tuple

import numpy as np

from pyxel.detectors import CMOS
from pyxel.util import set_random_seed


def lambda_e(lambda_cutoff: float) -> float:
    """Compute lambda_e.

    Parameters
    ----------
    lambda_cutoff : int
        Cut-off wavelength of the detector.

    Returns
    -------
    le: float
    """
    lambda_scale = 0.200847413  # um
    lambda_threshold = 4.635136423  # um
    pwr = 0.544071282
    if lambda_cutoff < lambda_threshold:
        le = lambda_cutoff / (
            1
            - ((lambda_scale / lambda_cutoff) - (lambda_scale / lambda_threshold))
            ** pwr
        )
    else:
        le = lambda_cutoff
    return le


def average_dark_current_rule07(
    pitch: float,
    temperature: float,
    cut_off: float,
) -> float:
    """Compute dark current.

    Parameters
    ----------
    pitch : float
        the x and y dimension of the pixel in micrometer
    temperature : float
        the devices temperature
    cut_off : float
        the detector wavelength cut-off in micrometer

    Returns
    -------
    float
        Dark current values. Unit: e-/pixel/s.
    """
    c = 1.16  # activation energy factor
    q = 1.602e-19  # Charge of one electron, unit= A.s
    k = 1.3806504e-23  # Constant of Boltzmann, unit = m2.kg/s2/K

    j0 = 8367  # obtained through fit of experimental data, see paper

    e_c = 1.24 / lambda_e(
        cut_off
    )  # [eV] the optical gap extracted from the mid response cutoff

    rule07 = j0 * np.exp(-c * q * e_c / (k * temperature))  # A/cm3

    amp_to_eps = 6.242e18  # e-/s
    um2_to_cm2 = 1.0e-8
    factor = amp_to_eps * pitch * pitch * um2_to_cm2  # to convert Amp/cm2 in e/pixel/s
    avg_dark_current_rule07 = rule07 * factor

    return avg_dark_current_rule07


def compute_mct_dark_rule07(
    shape: Tuple[int, int],
    pitch: float,
    time_step: float,
    temperature: float,
    cut_off: float,
    spatial_noise_factor: Optional[float] = None,
    temporal_noise: bool = True,
) -> np.ndarray:
    """Compute dark current.

    Parameters
    ----------
    shape : tuple
        Output array shape.
    pitch : float
        the x and y dimension of the pixel in micrometer
    time_step : float
        Time step. Unit: s
    temperature : float
        the devices temperature
    cut_off : float
        the detector wavelength cut-off in micrometer
    spatial_noise_factor : float
        Dark current fixed pattern noise factor.
    temporal_noise: bool
        Shot noise.

    Returns
    -------
    ndarray
        Dark current values. Unit: e-
    """

    avg_dark_current_rule07 = average_dark_current_rule07(
        pitch=pitch,
        temperature=temperature,
        cut_off=cut_off,
    )

    if temporal_noise:
        dark_signal_2d_rule07 = np.ones(shape) * avg_dark_current_rule07 * time_step
        dark_current_shot_noise_2d_rule07 = np.random.poisson(
            dark_signal_2d_rule07
        )  # dark current shot noise
        dark_current_2d_rule07 = dark_current_shot_noise_2d_rule07.astype(float)
    else:
        # The number of charge generated with Poisson distribution using rule07 empiric law for lambda
        dark_signal_2d_rule07 = np.ones(shape) * avg_dark_current_rule07 * time_step
        dark_current_2d_rule07 = dark_signal_2d_rule07

    if spatial_noise_factor is not None:
        dark_current_fpn_sigma_rule07 = (
            time_step * avg_dark_current_rule07 * spatial_noise_factor
        )  # sigma of fpn distribution

        dark_current_2d_rule07 = dark_current_2d_rule07 * (
            1 + np.random.lognormal(sigma=dark_current_fpn_sigma_rule07, size=shape)
        )

    if np.isinf(dark_current_2d_rule07).any():
        warnings.warn(
            "Unphysical high value for dark current from fixed pattern noise distribution"
            " will result in inf values. Enable a FWC model to ensure a physical limit.",
            RuntimeWarning,
        )

    return dark_current_2d_rule07


def dark_current_rule07(
    detector: CMOS,
    cutoff_wavelength: float = 2.5,  # unit: um
    spatial_noise_factor: Optional[float] = None,
    seed: Optional[int] = None,
    temporal_noise: bool = True,
) -> None:
    """Generate charge from dark current process.

    Based on Rule07 paper by W.E. Tennant Journal of Electronic Materials volume 37, pages1406–1410 (2008).

    Parameters
    ----------
    detector : Detector
    cutoff_wavelength : float
        Cutoff wavelength. Unit: um
    spatial_noise_factor : float
        Dark current fixed pattern noise factor.
    seed : int, optional
    temporal_noise : bool, optional
        Shot noise.
    """
    # TODO: investigate on the knee of rule07 for higher 1/le*T values
    if not isinstance(detector, CMOS):
        raise TypeError("Expecting a CMOS object for detector.")
    if not (1.7 <= cutoff_wavelength <= 15.0):
        raise ValueError("'cutoff' must be between 1.7 and 15.0.")

    geo = detector.geometry

    pitch = geo.pixel_vert_size  # assumes a square pitch
    temperature = detector.environment.temperature
    time_step = detector.time_step

    with set_random_seed(seed):
        dark_current_array_rule07 = compute_mct_dark_rule07(
            pitch=pitch,
            temperature=temperature,
            cut_off=cutoff_wavelength,
            shape=geo.shape,
            time_step=time_step,
            spatial_noise_factor=spatial_noise_factor,
            temporal_noise=temporal_noise,
        )

    detector.charge.add_charge_array(dark_current_array_rule07)
