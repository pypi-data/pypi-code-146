"""
Non-linearity models utility functions.

@author: tpichon
"""
import numpy as np
from numba import float64, njit
from numba.experimental import jitclass

spec = [
    ("m_electron", float64),
    ("k_b", float64),
    ("electron_charge", float64),
    ("eps_0", float64),
]


@jitclass(spec)
class Constants:
    """Constants class."""

    def __init__(self):
        self.m_electron = 9.10938356e-31  # kg
        self.k_b = 1.38064852e-23  #
        self.electron_charge = 1.60217662e-19
        self.eps_0 = 8.85418782e-12


@njit
def build_in_potential(
    temperature: float,
    n_acceptor: float,
    n_donor: float,
    n_intrinsic: float,
) -> float:
    """Built-in potential.

    Parameters
    ----------
    temperature : float
        Temperature.
    n_acceptor
        Acceptor concentration.
    n_donor
        Donor concentration.
    n_intrinsic : float
        Intrinsic carrier concentration.

    Returns
    -------
    float
    """

    const = Constants()

    return (
        const.k_b
        * temperature
        / const.electron_charge
        * np.log(n_acceptor * n_donor / n_intrinsic**2)
    )


@njit
def w_dep(
    v_bias: np.ndarray,
    epsilon: float,
    n_acceptor: float,
    n_donor: float,
    x_cd: float,
    temperature: float,
) -> np.ndarray:
    """Depletion width.

    Parameters
    ----------
    v_bias : ndarray
        Bias voltage.
    epsilon : float
        Dielectric constant of the material.
    n_acceptor : float
        Acceptor concentration.
    n_donor : float
        Donor concentration.
    x_cd
        Cadmium composition between 0 and 1.
    temperature : float
        Temperature.
    """

    const = Constants()

    # Calculation of build in potential
    v_bi = build_in_potential(
        temperature=temperature,
        n_acceptor=n_acceptor,
        n_donor=n_donor,
        n_intrinsic=ni_hansen(x_cd=x_cd, temperature=temperature),
    )

    return np.sqrt(
        2.0
        * epsilon
        * const.eps_0
        / const.electron_charge
        * (n_acceptor * 1e6 + n_donor * 1e6)
        / (n_acceptor * 1e6 * n_donor * 1e6)
        * (v_bi - v_bias)
    )


@njit
def hgcdte_bandgap(x_cd: float, temperature: float) -> float:
    """Band gap energy in HgCdTe.

    This expression of the Gap of HgCdTe is valid for a Cadmium concentration between 0.2 and 0.6.
    Over a wide range of temperature between 4K and 300K

    Ref : Hansen, G. L., Schmit, J. L., & Casselman, T. N. (1982).
          Energy gap versus alloy composition and temperature in Hg1− x Cd x Te.
          Journal of Applied Physics, 53(10), 7099-7101.

    Parameters
    ----------
    x_cd : float
        Cadmium composition between 0 and 1
    temperature : float
        Temperature.

    Returns
    -------
    float
        Bandgap energy. Unit: eV
    """

    return (
        -0.302
        + 1.93 * x_cd
        - 0.81 * x_cd**2
        + 0.832 * x_cd**3
        + 5.35 * 1e-4 * (1 - 2 * x_cd) * temperature
    )


@njit
def ni_hansen(x_cd: float, temperature: float) -> float:
    """Intrinsic carrier concentration for HgCdTe.

    Ref : G.L. Hansen and J.L. Schmit  J. Applied Physics, 54, 1639 (1983)

    Parameters
    ----------
    x_cd : float
        Cadmium composition between 0 and 1
    temperature : float
        Temperature.

    Returns
    -------
    float
        intrinsic carrier concentration
    """

    const = Constants()

    e_g = hgcdte_bandgap(x_cd=x_cd, temperature=temperature)

    return (
        (
            5.585
            - 3.820 * x_cd
            + 1.753 * 1e-3 * temperature
            - 1.364 * 1e-3 * temperature * x_cd
        )
        * 1e14
        * e_g**0.75
        * temperature**1.5
        * np.exp(-const.electron_charge * e_g / (2 * const.k_b * temperature))
    )


@njit
def capa_pn_junction_cylindrical(
    v_bias: np.ndarray,
    phi_implant: float,
    d_implant: float,
    n_acceptor: float,
    n_donor: float,
    x_cd: float,
    temperature: float,
) -> np.ndarray:
    """Calculate the capacitance of the cylindrical pn junction.

    Parameters
    ----------
    v_bias : ndarray
    phi_implant : float
    d_implant : float
    n_acceptor : float
    n_donor : float
    x_cd : float
    temperature : float

    Returns
    -------
    ndarray
    """
    epsilon = (
        20.5 - 15.6 * x_cd + 5.7 * x_cd**2
    )  # Static dielectric constant, this value is ok for HgCdTe

    # Definition of the constants
    const = Constants()
    eps0 = const.eps_0

    # Calculation of w
    w = w_dep(
        v_bias=v_bias,
        epsilon=epsilon,
        n_acceptor=n_acceptor,
        n_donor=n_donor,
        x_cd=x_cd,
        temperature=temperature,
    )

    ao = np.pi * epsilon * eps0 * ((phi_implant / 2.0) ** 2 + d_implant * phi_implant)
    bo = np.pi * epsilon * eps0 * 2.0 * (d_implant + phi_implant)
    co = 3.0 * np.pi * epsilon * eps0
    return ao * 1.0 / w + bo + co * w


@njit
def dv_dt_cylindrical(
    v_bias: np.ndarray,
    photonic_current: np.ndarray,
    fixed_capacitance: float,
    sat_current: float,
    n: float,
    phi_implant: float,
    d_implant: float,
    n_acceptor: float,
    n_donor: float,
    x_cd: float,
    temperature: float,
) -> np.ndarray:
    """Use this diode discharge equation when considering a cylindrical diode.

    Parameters
    ----------
    v_bias : float,
        Diode polarisation
    photonic_current : float
        Photonic current
    fixed_capacitance : float
        Fixed capacitance
    sat_current : float
        Saturating current under dark conditions
    n : float
        Ideality factor
    phi_implant : float
        diameter of the implantation
    d_implant : float
        depth of the implantation
    n_acceptor : float
        density of acceptors
    n_donor : float
        density of donor
    x_cd : float
        cadmium concentrations
    temperature : float
        temperature of the sample

    Returns
    -------
    float
        Polarisation evolution per second.
    """
    const = Constants()
    e, k = const.electron_charge, const.k_b

    # Capacitance calculation as a function of Bias
    c = capa_pn_junction_cylindrical(
        v_bias=v_bias,
        phi_implant=phi_implant,
        d_implant=d_implant,
        n_acceptor=n_acceptor,
        n_donor=n_donor,
        x_cd=x_cd,
        temperature=temperature,
    )

    return -(
        e * sat_current * (np.exp(e * v_bias / (n * k * temperature)) - 1)
        - e * photonic_current
    ) / (fixed_capacitance + c)


@njit
def euler(
    time_step: float,
    nb_pts: int,
    v_bias: np.ndarray,
    phi_implant: float,
    d_implant: float,
    n_acceptor: float,
    n_donor: float,
    x_cd: float,
    temperature: float,
    photonic_current: np.ndarray,
    fixed_capacitance: float,
    sat_current: float,
    n: float,
):
    """Apply Euler method to solve the differential equation for detector non-linearity.

    Parameters
    ----------
    time_step : float
        Time step.
    nb_pts : float
        Number of points.
    v_bias : float
        Diode polarisation.
    phi_implant : float
        Diameter of the implantation.
    d_implant : float
        Depth of the implantation.
    n_acceptor : float
        Density of acceptors.
    n_donor : float
        Density of donor.
    x_cd : float
        Cadmium concentration.
    temperature : float
        Temperature of the sample.
    photonic_current : float
        Photonic current.
    fixed_capacitance : float
        Fixed capacitance.
    sat_current : float
        Saturating current under dark conditions.
    n : float
        Ideality factor.

    Returns
    -------
    ndarray:
        Voltage at the gate of the pixel SFD.
    """
    # Calculating step size
    h = time_step / nb_pts
    # Initialization of variables
    v = [v_bias]
    # ==============================
    #           SOLVE THE DIFFERENTIAL EQUATION
    # ==============================
    # EULER Method to solve the differential equation
    for _ in range(1, nb_pts):
        slope = dv_dt_cylindrical(
            v_bias=v[-1],
            photonic_current=photonic_current,
            fixed_capacitance=fixed_capacitance,
            sat_current=sat_current,
            n=n,
            phi_implant=phi_implant,
            d_implant=d_implant,
            n_acceptor=n_acceptor,
            n_donor=n_donor,
            x_cd=x_cd,
            temperature=temperature,
        )
        # Calculate new bias
        yn = v[-1] + h * slope
        # Saved the old bias
        v.append(yn)

    # Return bias evolution, capacitance and time
    return v[-1]
