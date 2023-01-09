#   Copyright (c) European Space Agency, 2017, 2018, 2019, 2020, 2021, 2022.
#  #
#   This file is subject to the terms and conditions defined in file 'LICENCE.txt', which
#   is part of this Pyxel package. No part of the package, including
#   this file, may be copied, modified, propagated, or distributed except according to
#   the terms contained in the file ‘LICENCE.txt’.

"""Models to generate charge due to dark current process."""
import warnings
from typing import Optional, Tuple

import numpy as np
from astropy import constants as const

from pyxel.detectors import APD, Detector
from pyxel.util import set_random_seed


def calculate_band_gap(
    band_gap_0: float, alpha: float, beta: float, temperature: float
) -> float:
    """Return band gap based on Varshni empirical expression.

    Parameters
    ----------
    band_gap_0 : float
        Parameter E_0. Unit: eV
    alpha : float
        Alpha parameter. Unit: eV/K
    beta : float
        Beta parameter. Unit: K
    temperature :
        Temperature. Unit K

    Returns
    -------
    float
        Band gap value. Unit: eV
    """

    gap = band_gap_0 - (alpha * temperature**2) / (temperature + beta)

    return gap


def band_gap_silicon(temperature: float) -> float:
    """Return band gap in Silicon based on Varshni empirical expression.

    Parameters
    ----------
    temperature : float
        Temperature. Unit: K

    Returns
    -------
    float
        Band gap value. Unit: eV
    """

    band_gap_0 = 1.1557  # eV
    alpha = 7.021e-4  # ev/K
    beta = 1108.0  # K

    return calculate_band_gap(
        band_gap_0=band_gap_0, alpha=alpha, beta=beta, temperature=temperature
    )


def average_dark_current(
    temperature: float,
    pixel_area: float,
    figure_of_merit: float,
    band_gap: float,
    band_gap_room_temperature: float,
) -> float:
    """Compute average dark current.

    Parameters
    ----------
    temperature : float
        Temperature. Unit: K
    pixel_area
        Pixel area. Unit: cm^2
    figure_of_merit : float
        Dark current figure of merit. Unit: nA/cm^2
    band_gap : float
        Semiconductor band_gap. Unit: eV
    band_gap_room_temperature : float
        Semiconductor band gap at 300K. If none, the one for silicon is used. Unit: eV

    Returns
    -------
    float
        Average dark current. Unit: e-/pixel/s
    """

    k_b = const.k_B.value
    e_0 = const.e.value

    room_temperature = 300

    room_temperature_factor = room_temperature ** (3 / 2) * np.exp(
        -band_gap_room_temperature * e_0 / (2 * k_b * room_temperature)
    )

    avg_dark_current = (
        pixel_area  # in cm^2
        * figure_of_merit  # in nA/cm^2
        * 1e-9  # conversion to A/cm^2
        * (1 / e_0)  # conversion to e-/s/cm^2
        * temperature ** (3 / 2)
        * np.exp(-band_gap * e_0 / (2 * k_b * temperature))
        * (1 / room_temperature_factor)
    )  # Unit: e-/s/pixel

    return avg_dark_current


def compute_dark_current(
    shape: Tuple[int, int],
    time_step: float,
    temperature: float,
    pixel_area: float,
    figure_of_merit: float,
    band_gap: float,
    band_gap_room_temperature: float,
    spatial_noise_factor: Optional[float] = None,
    temporal_noise: bool = True,
) -> np.ndarray:
    """Compute dark current.

    Based on:
    Konnik, Mikhail V. and James S. Welsh.
    “High-level numerical simulations of noise in CCD and CMOS photosensors: review and tutorial.”
    ArXiv abs/1412.4031 (2014): n. pag.

    Parameters
    ----------
    shape : tuple
        Output array shape.
    time_step : float
        Time step. Unit: s
    temperature : float
        Temperature. Unit: K
    pixel_area
        Pixel area. Unit: cm^2
    figure_of_merit : float
        Dark current figure of merit. Unit: nA/cm^2
    band_gap : float
        Semiconductor band_gap. Unit: eV
    band_gap_room_temperature : float
        Semiconductor band gap at 300K. If none, the one for silicon is used. Unit: eV
    spatial_noise_factor: float
        Dark current fixed pattern noise factor.
    temporal_noise: bool
        Shot noise.

    Returns
    -------
    ndarray
        Dark current values. Unit: e-
    """

    avg_dark_current = average_dark_current(
        temperature=temperature,
        pixel_area=pixel_area,
        figure_of_merit=figure_of_merit,
        band_gap=band_gap,
        band_gap_room_temperature=band_gap_room_temperature,
    )

    if temporal_noise:
        dark_signal_2d = np.ones(shape) * avg_dark_current * time_step
        dark_current_shot_noise_2d = np.random.poisson(
            dark_signal_2d
        )  # dark current shot noise
        dark_current_2d = dark_current_shot_noise_2d.astype(float)
    else:
        dark_signal_2d = np.ones(shape) * avg_dark_current * time_step
        dark_current_2d = dark_signal_2d

    if spatial_noise_factor is not None:
        dark_current_fpn_sigma = (
            time_step * avg_dark_current * spatial_noise_factor
        )  # sigma of fpn distribution

        dark_current_2d = dark_current_2d * (
            1 + np.random.lognormal(sigma=dark_current_fpn_sigma, size=shape)
        )

    if np.isinf(dark_current_2d).any():
        warnings.warn(
            "Unphysical high value for dark current from fixed pattern noise distribution"
            " will result in inf values. Enable a FWC model to ensure a physical limit.",
            RuntimeWarning,
        )

    return dark_current_2d


def dark_current(
    detector: Detector,
    figure_of_merit: float,
    spatial_noise_factor: Optional[float] = None,
    band_gap: Optional[float] = None,
    band_gap_room_temperature: Optional[float] = None,
    seed: Optional[int] = None,
    temporal_noise: bool = True,
) -> None:
    """Add dark current to the detector charge.

    Based on:
    Konnik, Mikhail V. and James S. Welsh.
    “High-level numerical simulations of noise in CCD and CMOS photosensors: review and tutorial.”
    ArXiv abs/1412.4031 (2014): n. pag.

    Parameters
    ----------
    detector : Detector
        Pyxel detector object.
    figure_of_merit : float
        Dark current figure of merit. Unit: nA/cm^2
    spatial_noise_factor : float
        Dark current fixed pattern noise factor.
    band_gap : float, optional
        Semiconductor band_gap. If none, the one for silicon is used. Unit: eV
    band_gap_room_temperature : float, optional
        Semiconductor band gap at 300K. If none, the one for silicon is used. Unit: eV
    seed : int, optional
        Random seed.
    temporal_noise : bool, optional
        Shot noise.
    """
    geo = detector.geometry
    pixel_area = geo.pixel_vert_size * 1e-4 * geo.pixel_horz_size * 1e-4  # in cm^2
    temperature = detector.environment.temperature
    time_step = detector.time_step

    if band_gap and band_gap_room_temperature:
        final_band_gap = band_gap
        final_band_gap_room_temperature = band_gap_room_temperature
    elif band_gap or band_gap_room_temperature:
        raise ValueError(
            "Both parameters band_gap and band_gap_room_temperature have to be defined."
        )
    else:
        final_band_gap = band_gap_silicon(temperature)
        final_band_gap_room_temperature = band_gap_silicon(temperature=300)

    with set_random_seed(seed):
        dark_current_array = compute_dark_current(
            shape=geo.shape,
            time_step=time_step,
            temperature=temperature,
            pixel_area=pixel_area,
            figure_of_merit=figure_of_merit,
            band_gap=final_band_gap,
            band_gap_room_temperature=final_band_gap_room_temperature,
            spatial_noise_factor=spatial_noise_factor,
            temporal_noise=temporal_noise,
        )

    detector.charge.add_charge_array(dark_current_array)


def calculate_simple_dark_current(
    num_rows: int, num_cols: int, current: float, exposure_time: float
) -> np.ndarray:
    """Simulate dark current in a :term:`CCD`.

    Parameters
    ----------
    num_rows : int
        Number of rows for the generated image.
    num_cols : int
        Number of columns for the generated image.
    current : float
        Dark current, in electrons/pixel/second
    exposure_time : float
        Length of the simulated exposure, in seconds.

    Returns
    -------
    ndarray
        An array the same shape and dtype as the input containing dark counts
        in units of charge (e-).
    """
    # dark current for every pixel
    mean_dark_charge = current * exposure_time

    # This random number generation should change on each call.
    dark_im_array_2d = np.random.poisson(mean_dark_charge, size=(num_rows, num_cols))
    return dark_im_array_2d


def simple_dark_current(
    detector: Detector, dark_rate: float, seed: Optional[int] = None
) -> None:
    """Simulate dark current in a detector.

    Parameters
    ----------
    detector : Detector
        Any detector object.
    dark_rate : float
        Dark current, in electrons/pixel/second, which is the way
        manufacturers typically report it.
    seed : int, optional
    """

    exposure_time = detector.time_step
    geo = detector.geometry

    with set_random_seed(seed):
        dark_current_array: np.ndarray = calculate_simple_dark_current(
            num_rows=geo.row,
            num_cols=geo.col,
            current=dark_rate,
            exposure_time=exposure_time,
        ).astype(float)

    detector.charge.add_charge_array(dark_current_array)


def calculate_dark_current_saphira(
    temperature: float,
    avalanche_gain: float,
    shape: Tuple[int, int],
    exposure_time: float,
) -> np.ndarray:
    """Simulate dark current in a Saphira :term:`APD`.

    From: I. M. Baker et al., Linear-mode avalanche photodiode arrays in HgCdTe at Leonardo, UK: the
    current status, in Image Sensing Technologies: Materials, Devices, Systems, and Applications VI,
    2019, vol. 10980, no. May, p. 20.

    Parameters
    ----------
    temperature
    avalanche_gain
    shape
    exposure_time : float
        Length of the simulated exposure, in seconds.

    Returns
    -------
    ndarray
        An array the same shape and dtype as the input containing dark counts
        in units of charge (e-).
    """

    # We can split the dark current vs. gain vs. temp plot ([5] Fig. 3) into three linear
    # 'regimes': 1) low-gain, low dark current; 2) nominal; and 3) trap-assisted tunneling.
    # The following ignores (1) for now since this only applies at gains less than ~2.

    dark_nominal = (15.6e-12 * np.exp(0.2996 * temperature)) * (
        avalanche_gain
        ** ((-5.43e-4 * (temperature**2)) + (0.0669 * temperature) - 1.1577)
    )
    dark_tunnel = 3e-5 * (avalanche_gain**3.2896)

    # The value we want is the maximum of the two regimes (see the plot):
    dark = max(dark_nominal, dark_tunnel)

    # dark current for every pixel
    mean_dark_charge = dark * exposure_time

    # This random number generation should change on each call.
    dark_im_array_2d = np.random.poisson(mean_dark_charge, size=shape)

    return dark_im_array_2d


def dark_current_saphira(detector: APD, seed: Optional[int] = None) -> None:
    """Simulate dark current in a Saphira APD detector.

    Reference: I. M. Baker et al., Linear-mode avalanche photodiode arrays in HgCdTe at Leonardo, UK: the
    current status, in Image Sensing Technologies: Materials, Devices, Systems, and Applications VI,
    2019, vol. 10980, no. May, p. 20.

    Parameters
    ----------
    detector : APD
        An APD detector object.
    seed : int, optional
    """

    if not isinstance(detector, APD):
        raise TypeError("Expecting an APD object for detector.")
    if detector.environment.temperature > 100:
        raise ValueError(
            "Dark current estimation is inaccurate for temperatures more than 100 K!"
        )
    if detector.characteristics.avalanche_gain < 2:
        raise ValueError("Dark current is inaccurate for avalanche gains less than 2!")

    exposure_time = detector.time_step

    with set_random_seed(seed):
        dark_current_array: np.ndarray = calculate_dark_current_saphira(
            temperature=detector.environment.temperature,
            avalanche_gain=detector.characteristics.avalanche_gain,
            shape=detector.geometry.shape,
            exposure_time=exposure_time,
        ).astype(float)

    detector.charge.add_charge_array(dark_current_array)
