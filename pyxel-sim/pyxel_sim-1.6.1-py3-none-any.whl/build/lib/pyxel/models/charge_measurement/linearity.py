#  Copyright (c) European Space Agency, 2017, 2018, 2019, 2020, 2021, 2022.
#
#  This file is subject to the terms and conditions defined in file 'LICENCE.txt', which
#  is part of this Pyxel package. No part of the package, including
#  this file, may be copied, modified, propagated, or distributed except according to
#  the terms contained in the file ‘LICENCE.txt’.

"""Linearity models."""

from typing import Sequence

import numpy as np
from astropy import constants as const

from pyxel.detectors import CMOS, Detector
from pyxel.models.charge_measurement.non_linearity_calculation import (
    euler,
    hgcdte_bandgap,
    ni_hansen,
)


def compute_poly_linearity(
    array_2d: np.ndarray,
    coefficients: Sequence[float],
) -> np.ndarray:
    """Add non-linearity to an array of values following a polynomial function.

    Parameters
    ----------
    array_2d : ndarray
        Input array.
    coefficients : list of float
        Coefficients of the polynomial function.

    Returns
    -------
    np.ndarray
        Signal.
    """
    polynomial_function = np.polynomial.polynomial.Polynomial(coefficients)

    non_linear_signal = polynomial_function(array_2d)

    return non_linear_signal


def output_node_linearity_poly(
    detector: Detector,
    coefficients: Sequence[float],
) -> None:
    """Add non-linearity to signal array to simulate the non-linearity of the output node circuit.

    The non-linearity is simulated by a polynomial function. The user specifies the polynomial coefficients.

    detector Signal unit: Volt

    Parameters
    ----------
    detector : Detector
        Pyxel Detector object.
    coefficients : list of float
        Coefficient of the polynomial function.
    """
    if len(coefficients) == 0:
        raise ValueError("Length of coefficient list should be more than 0.")

    signal_mean_array = detector.signal.array.astype("float64")
    signal_non_linear = compute_poly_linearity(
        array_2d=signal_mean_array, coefficients=coefficients
    )

    if np.any(signal_non_linear < 0):
        raise ValueError(
            "Signal array contains negative values after applying non-linearity model!"
        )

    detector.signal.array = signal_non_linear


def compute_simple_physical_non_linearity(
    array_2d: np.ndarray,
    temperature: float,  # Detector operating temperature
    v_bias: float,
    cutoff: float,
    n_acceptor: float,
    n_donor: float,
    diode_diameter: float,
) -> np.ndarray:
    """Compute simple physical non-linear signal.

    Parameters
    ----------
    array_2d : ndarray
        Input array.
    temperature
        Temperature. Unit: K.
    v_bias : float
        Initial bias voltage. Unit: V.
    cutoff : float
        Cutoff wavelength. unit: um
    n_acceptor : float
        Acceptor density. Unit: atoms/cm^3
    n_donor : float
        Donor density. Unit: atoms/cm^3
    diode_diameter : float
        Diode diameter. Unit: um

    Returns
    -------
    ndarray
        Output array.
    """
    # Derivation of Cd concentration in the alloy,  it depends on cutoff wavelength and targeted operating temperature
    # Here we are considering the case where the detector is operated at its nominal temperature,
    # it might not be always the case
    # cutoff = 2.1
    e_g_targeted = 1.24 / cutoff  # cutoff is um and Eg in eV
    xcd = np.linspace(0.2, 0.6, 1000)
    targeted_operating_temperature = temperature
    e_g_calculated = hgcdte_bandgap(
        xcd, targeted_operating_temperature
    )  # Expected bandgap
    index = np.where(e_g_calculated > e_g_targeted)[0][0]
    x_cd = xcd[index]  # Targeted cadmium concentration in the HgCdTe alloy

    if not (0.2 <= x_cd <= 0.6):
        raise ValueError(
            "Hansen bangap expression used out of its nominal application range. \
                x_cd must be between 0.2 and 0.6"
        )

    ni = ni_hansen(x_cd=x_cd, temperature=temperature)

    # Build in potential
    vbi = (
        const.k_B.value
        * temperature
        / const.e.value
        * np.log(n_acceptor * n_donor / ni**2)
    )

    # HgCdTe dielectric constant
    eps = 20.5 - 15.6 * x_cd + 5.7 * x_cd**2

    # Surface of the diode, assumed to be planar
    surface = (
        np.pi * (diode_diameter / 2.0 * 1e-6) ** 2
    )  # Surface of the diode, assumed to be circular

    # Initial value  of the diode capacitance
    co = surface * np.sqrt(
        (const.e.value * eps * const.eps0.value)
        / (2 * (vbi - v_bias))
        * ((n_acceptor * 1e6 * n_donor * 1e6) / (n_acceptor * 1e6 + n_donor * 1e6))
    )

    non_linear_signal = (
        1
        / (2 * vbi)
        * (const.e.value * array_2d / co) ** 2
        * (-1 + np.sqrt(1 + 4 * (co / (const.e.value * array_2d)) ** 2 * vbi**2))
    )

    return non_linear_signal


def simple_physical_non_linearity(
    detector: Detector,
    cutoff: float,
    n_acceptor: float,
    n_donor: float,
    diode_diameter: float,
    v_bias: float,
) -> None:
    """Apply simple physical non-linearity.

    Parameters
    ----------
    detector : Detector
        Pyxel detector object.
    cutoff : float
        Cutoff wavelength. unit: um
    n_donor : float
        Donor density. Unit: atoms/cm^3
    n_acceptor : float
        Acceptor density. Unit: atoms/cm^3
    diode_diameter : float
        Diode diameter. Unit: um
    v_bias : float
        Initial bias voltage. Unit: V.
    """

    if not (4 <= detector.environment.temperature <= 300):
        raise ValueError(
            "Hansen bangap expression used out of its nominal application range. \
                temperature must be between 4K and 300K"
        )

    if not isinstance(detector, CMOS):
        raise TypeError("Expecting a 'CMOS' detector object.")

    signal_mean_array = detector.charge.array.astype("float64")
    signal_non_linear = compute_simple_physical_non_linearity(
        array_2d=signal_mean_array,
        temperature=detector.environment.temperature,
        v_bias=v_bias,
        cutoff=cutoff,
        n_acceptor=n_acceptor,
        n_donor=n_donor,
        diode_diameter=diode_diameter,
    )

    detector.signal.array = signal_non_linear


def compute_physical_non_linearity(
    array_2d: np.ndarray,
    temperature: float,
    fixed_capacitance: float,
    v_bias: float,
    cutoff: float,
    n_acceptor: float,
    n_donor: float,
    diode_diameter: float,
) -> np.ndarray:
    """Compute physical non-linear signal.

    Parameters
    ----------
    array_2d : ndarray
        Input array.
    temperature
        Temperature. Unit: K.
    fixed_capacitance : float
        Additional fixed capacitance. Unit: F
    v_bias : float
        Initial bias voltage. Unit: V.
    cutoff : float
        Cutoff wavelength. unit: um
    n_acceptor : float
        Acceptor density. Unit: atoms/cm^3
    n_donor : float
        Donor density. Unit: atoms/cm^3
    diode_diameter : float
        Diode diameter. Unit: um

    Returns
    -------
    ndarray
        Output array.
    """
    # Derivation of Cd concentration in the alloy,  it depends on cutoff wavelength and targeted operating temperature
    # Here we are considering the case where the detector is operated at its nominal temperature,
    # it might not be always the case
    e_g_targeted = 1.24 / cutoff  # cutoff is um and Eg in eV
    xcd = np.linspace(0.2, 0.6, 1000)
    targeted_operating_temperature = temperature
    e_g_calculated = hgcdte_bandgap(
        xcd, targeted_operating_temperature
    )  # Expected band-gap
    index = np.where(e_g_calculated > e_g_targeted)[0][0]
    x_cd = xcd[index]  # Targeted cadmium concentration in the HgCdTe alloy

    if not (0.2 <= x_cd <= 0.6):
        raise ValueError(
            "Hansen bangap expression used out of its nominal application range. \
                x_cd must be between 0.2 and 0.6"
        )

    # Calculate the effective band-gap value at the temperature at which simulations are performed.
    ni = ni_hansen(x_cd=x_cd, temperature=temperature)

    # Build in potential
    vbi = (
        const.k_B.value
        * temperature
        / const.e.value
        * np.log(n_acceptor * n_donor / ni**2)
    )  # in V

    # HgCdTe dielectric constant
    eps = 20.5 - 15.6 * x_cd + 5.7 * x_cd**2  # without dimension

    # Surface of the diode, assumed to be planar
    surface = (
        np.pi * (diode_diameter / 2.0 * 1e-6) ** 2
    )  # Surface of the diode, assumed to be circular (in cm)

    # Initial value  of the diode capacitance
    co = surface * np.sqrt(
        (const.e.value * eps * const.eps0.value)
        / (2 * vbi)
        * ((n_acceptor * 1e6 * n_donor * 1e6) / (n_acceptor * 1e6 + n_donor * 1e6))
    )

    # Resolution of 2nd order equation
    b = -2.0 * co / fixed_capacitance
    a = -1.0
    c = (
        (1 - v_bias / vbi)
        + 2.0 * co / fixed_capacitance * np.sqrt(1.0 - v_bias / vbi)
        - array_2d * const.e.value / (fixed_capacitance * vbi)
    )
    discriminant = b**2 - 4.0 * c * a
    u1 = (-b - np.sqrt(discriminant)) / (2.0 * a)
    v1 = (1.0 - u1**2) * vbi - v_bias  # is subtracted it only deals with offset level

    array = np.copy(v1)  # unit if V, voltage at the gate of the pixel SFD
    non_linear_signal = array.astype("float64")

    return non_linear_signal


def physical_non_linearity(
    detector: Detector,
    cutoff: float,
    n_acceptor: float,
    n_donor: float,
    diode_diameter: float,
    v_bias: float,
    fixed_capacitance: float,
) -> None:
    """Apply physical non-linearity.

    Parameters
    ----------
    detector : Detector
        Pyxel detector object.
    cutoff : float
        Cutoff wavelength. unit: um
    n_donor : float
        Donor density. Unit: atoms/cm^3
    n_acceptor : float
        Acceptor density. Unit: atoms/cm^3
    diode_diameter : float
        Diode diameter. Unit: um
    v_bias : float
        Initial bias voltage. Unit: V.
    fixed_capacitance : float
        Additional fixed capacitance. Unit: F
    """
    if not (4 <= detector.environment.temperature <= 300):
        raise ValueError(
            "Hansen bangap expression used out of its nominal application range. \
                temperature must be between 4K and 300K"
        )

    if not isinstance(detector, CMOS):
        raise TypeError("Expecting a 'CMOS' detector object.")

    signal_mean_array = detector.pixel.array.astype("float64")
    signal_non_linear = compute_physical_non_linearity(
        array_2d=signal_mean_array,
        temperature=detector.environment.temperature,
        fixed_capacitance=fixed_capacitance,
        v_bias=v_bias,
        cutoff=cutoff,
        n_acceptor=n_acceptor,
        n_donor=n_donor,
        diode_diameter=diode_diameter,
    )

    detector.signal.array = signal_non_linear


def compute_physical_non_linearity_with_saturation(
    signal_array_2d: np.ndarray,
    photon_array_2d: np.ndarray,
    time_step: float,
    temperature: float,
    cutoff: float,
    n_donor: float,
    n_acceptor: float,
    phi_implant: float,
    d_implant: float,
    saturation_current: float,
    ideality_factor: float,
    v_reset: float,
    d_sub: float,
    fixed_capacitance: float,
    euler_points: int,
) -> np.ndarray:
    """Compute physical non-linear signal with saturation.

    Parameters
    ----------
    signal_array_2d : ndarray
        Input signal array.
    photon_array_2d : ndarray
        Input photon array.
    time_step
        Time step. Unit: s.
    temperature : float
        Temperature. Unit: K.
    cutoff : float
        Cutoff wavelength. unit: um.
    n_donor : float
        Donor density. Unit: atoms/cm^3.
    n_acceptor : float
        Acceptor density. Unit: atoms/cm^3.
    phi_implant : float
        Diameter of the implantation. Unit: um.
    d_implant : float
        Depth of the implamantation. Unit: um.
    saturation_current : float
        Saturation current: e-/s/pix..
    ideality_factor : float
        Ideality factor.
    v_reset : float
        VRESET. Unit: V.
    d_sub : float
        DSUB. Unit: V.
    fixed_capacitance : float
        Additional fixed capacitance. Unit: F.
    euler_points : int
        Number of points in the euler method.

    Returns
    -------
    ndarray
        Output array containing non-linear signal. Unit: V.
    """
    # Derivation of Cd concentration in the alloy,  it depends on cutoff wavelength and targeted operating temperature
    # Here we are considering the case where the detector is operated at its nominal temperature,
    # it might not be always the case
    e_g_targeted = 1.24 / cutoff  # cutoff is um and Eg in eV
    xcd = np.linspace(0.2, 0.6, 1000)
    # targeted_operating_temperature = temperature
    e_g_calculated = hgcdte_bandgap(xcd, temperature)  # Expected bandgap
    index = np.where(e_g_calculated > e_g_targeted)[0][0]
    x_cd = xcd[index]  # Targeted cadmium concentration in the HgCdTe alloy
    # Calculate the effective bandgap value at the temperature at which simulations are performed.

    if not (0.2 <= x_cd <= 0.6):
        raise ValueError(
            "Hansen bangap expression used out of its nominal application range. \
                x_cd must be between 0.2 and 0.6"
        )

    row, col = signal_array_2d.shape

    phi_implant = phi_implant * 1e-6  # in m
    d_implant = d_implant * 1e-6  # in m

    if signal_array_2d[3, 3] == 0:
        signal_array_2d = v_reset * np.ones((row, col))

    # detector.signal.array should be expressed in unit of mV. It is the bias at the gate of the pixel SFD ????
    det_polar = euler(
        time_step=time_step,
        nb_pts=euler_points,
        v_bias=np.ravel(signal_array_2d) - d_sub,
        phi_implant=phi_implant,
        d_implant=d_implant,
        n_acceptor=n_acceptor,
        n_donor=n_donor,
        x_cd=x_cd,
        temperature=temperature,
        photonic_current=np.ravel(photon_array_2d) / time_step,
        fixed_capacitance=fixed_capacitance,
        sat_current=saturation_current,
        n=ideality_factor,
    )

    array = np.reshape(det_polar + d_sub, (row, col))
    non_linear_signal = array.astype("float64")

    return non_linear_signal


def physical_non_linearity_with_saturation(
    detector: Detector,
    cutoff: float,
    n_donor: float,
    n_acceptor: float,
    phi_implant: float,
    d_implant: float,
    saturation_current: float,
    ideality_factor: float,
    v_reset: float,
    d_sub: float,
    fixed_capacitance: float,
    euler_points: int,
) -> None:
    """Apply physical non-linearity with saturation.

    Parameters
    ----------
    detector : Detector
        Pyxel detector object.
    cutoff : float
        Cutoff wavelength. unit: um
    n_donor : float
        Donor density. Unit: atoms/cm^3
    n_acceptor : float
        Acceptor density. Unit: atoms/cm^3
    phi_implant : float
        Diameter of the implantation. Unit: um
    d_implant : float
        Depth of the implamantation. Unit: um
    saturation_current : float
        Saturation current: e-/s/pix.
    ideality_factor : float
        Ideality factor.
    v_reset : float
        VRESET. Unit: V.
    d_sub : float
        DSUB. Unit: V.
    fixed_capacitance : float
        Additional fixed capacitance. Unit: F.
    euler_points : int
        Number of points in the euler method.
    """
    if not (4 <= detector.environment.temperature <= 300):
        raise ValueError(
            "Hansen bangap expression used out of its nominal application range. \
                temperature must be between 4K and 300K"
        )

    if not isinstance(detector, CMOS):
        raise TypeError("Expecting a 'CMOS' detector object.")

    signal_non_linear = compute_physical_non_linearity_with_saturation(
        signal_array_2d=detector.signal.array,
        photon_array_2d=detector.photon.array,
        time_step=detector.time_step,
        temperature=detector.environment.temperature,
        cutoff=cutoff,
        n_donor=n_donor,
        n_acceptor=n_acceptor,
        phi_implant=phi_implant,
        d_implant=d_implant,
        saturation_current=saturation_current,
        ideality_factor=ideality_factor,
        v_reset=v_reset,
        d_sub=d_sub,
        fixed_capacitance=fixed_capacitance,
        euler_points=euler_points,
    )

    detector.signal.array = signal_non_linear
