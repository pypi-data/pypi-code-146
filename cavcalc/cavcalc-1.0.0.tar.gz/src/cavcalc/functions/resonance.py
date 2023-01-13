"""
Optical resonance type properties of a Fabry-Perot cavity.

.. note::

    Whilst these underlying functions are publicly accessible, it is recommended that you
    instead use the single-function interface :func:`.calculate` for computing any
    of the cavity properties that you need; as that will result in a nice output
    object for accessing results.
"""

import numpy as np

from .. import ureg
from ._utils import check_physical


_C_LIGHT = 299792458.0


def _fsr_base(L):
    return 0.5 * _C_LIGHT / L


@check_physical()
@ureg.wraps(ureg.hertz, ureg.meter)
def fsr(L):
    r"""Free Spectral Range (FSR) of a cavity of length :math:`L`.

    In the equation below, :math:`c` is the speed of light in a vacuum.

    .. math::
        \nu(L) = \frac{c}{2L}
    """
    return _fsr_base(L)


@check_physical()
@ureg.wraps("", ("", ""))
def R1_of_T1L1(T1, L1):
    r"""Reflectivity of the first cavity mirror, where this mirror has
    a transmission of :math:`T_1` and a loss value of :math:`L_1`.

    .. math::
        R_1 = 1 - T_1 - L_1
    """
    return 1 - T1 - L1


@check_physical()
@ureg.wraps("", ("", ""))
def T1_of_R1L1(R1, L1):
    r"""Transmission of the first cavity mirror, where this mirror has
    a reflectivity of :math:`R_1` and a loss value of :math:`L_1`.

    .. math::
        T_1 = 1 - R_1 - L_1
    """
    return 1 - R1 - L1


@check_physical()
@ureg.wraps("", ("", ""))
def R2_of_T2L2(T2, L2):
    r"""Reflectivity of the second cavity mirror, where this mirror has
    a transmission of :math:`T_2` and a loss value of :math:`L_2`.

    .. math::
        R_2 = 1 - T_2 - L_2
    """
    return 1 - T2 - L2


@check_physical()
@ureg.wraps("", ("", ""))
def T2_of_R2L2(R2, L2):
    r"""Transmission of the second cavity mirror, where this mirror has
    a reflectivity of :math:`R_2` and a loss value of :math:`L_2`.

    .. math::
        T_2 = 1 - R_2 - L_2
    """
    return 1 - R2 - L2


def _finesse_base(R1, R2):
    return 0.5 * np.pi / np.arcsin(0.5 * (1 - np.sqrt(R1 * R2)) / (R1 * R2) ** 0.25)


@check_physical()
@ureg.wraps("", ("", ""))
def finesse(R1, R2):
    r"""Finesse of a cavity where the first mirror has (power) reflectivity :math:`R_1`
    and the second mirror has reflectivity :math:`R_2`.

    .. math::
        \mathcal{F}(R_1, R_2) = \frac{\pi}{
            2 \arcsin{
                \left( \frac{1 - \sqrt{R_1 R_2}}{2 (R_1 R_2)^{1/4}} \right)
            }
        }
    """
    return _finesse_base(R1, R2)


@check_physical()
@ureg.wraps(ureg.hertz, (ureg.meter, "", ""))
def fwhm(L, R1, R2):
    r"""Full-Width at Half-Maximum (FWHM) frequency of a cavity of length :math:`L`, where
    the first mirror has (power) reflectivity :math:`R_1` and the second mirror has
    reflectivity :math:`R_2`.

    In the equation below, :math:`\nu(L)` is the FSR, and :math:`\mathcal{F}(R_1,R_2)` is
    the finesse.

    .. math::
        \mathrm{FWHM}(L, R_1, R_2) = \frac{\nu(L)}{\mathcal{F}(R_1, R_2)}
    """
    return _fsr_base(L) / _finesse_base(R1, R2)


@check_physical()
@ureg.wraps(ureg.hertz, (ureg.meter, "", ""))
def pole(L, R1, R2):
    r"""The pole frequency of a cavity of length :math:`L`, where the first mirror has (power)
    reflectivity :math:`R_1` and the second mirror has reflectivity :math:`R_2`.

    In the equation below, :math:`\nu(L)` is the FSR, and :math:`\mathcal{F}(R_1,R_2)` is
    the finesse.

    .. math::
        \mathrm{FWHM}(L, R_1, R_2) = \frac{\nu(L)}{2\mathcal{F}(R_1, R_2)}
    """
    return 0.5 * _fsr_base(L) / _finesse_base(R1, R2)
