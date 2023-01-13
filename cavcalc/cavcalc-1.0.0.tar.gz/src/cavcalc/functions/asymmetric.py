"""
Physical geometric-like parameter functions associated with non-symmetric optical cavities. Most properties
here are expressed only in terms of the invididual g-factors of the cavity mirrors, as inter-dependent
relations between these properties are computed via target chaining in the core cavcalc code.

.. note::

    Whilst these underlying functions are publicly accessible, it is recommended that you
    instead use the single-function interface :func:`.calculate` for computing any
    of the cavity properties that you need; as that will result in a nice output
    object for accessing results.
"""

import numpy as np

from .. import ureg
from ._utils import check_physical, modesep_adjust


@check_physical()
@ureg.wraps(ureg.meter, (ureg.meter, ureg.meter, "", ""))
def w1_of_g1g2(L, wl, g1, g2):
    r"""Radius of the beam, of wavelength :math:`\lambda`, at the *first* mirror of a cavity
    of length :math:`L`, with mirror g-factors of :math:`g_1` and :math:`g_2`, respectively.

    .. math::
        w_1\left(L, \lambda, g_1, g_2\right) = \sqrt{
            \frac{L \lambda}{\pi} \sqrt{\frac{g_2}{g_1(1 - g_1 g_2)}}
        }
    """
    return np.sqrt(L * wl / np.pi * np.sqrt(g2 / (g1 * (1 - g1 * g2))))


@check_physical()
@ureg.wraps(ureg.meter, (ureg.meter, ureg.meter, "", ""))
def w2_of_g1g2(L, wl, g1, g2):
    r"""Radius of the beam, of wavelength :math:`\lambda`, at the *end* mirror of a cavity
    of length :math:`L`, with mirror g-factors of :math:`g_1` and :math:`g_2`, respectively.

    .. math::
        w_2\left(L, \lambda, g_1, g_2\right) = \sqrt{
            \frac{L \lambda}{\pi} \sqrt{\frac{g_1}{g_2(1 - g_1 g_2)}}
        }
    """
    return np.sqrt(L * wl / np.pi * np.sqrt(g1 / (g2 * (1 - g1 * g2))))


@check_physical()
@ureg.wraps(ureg.meter, (ureg.meter, ureg.meter, "", ""))
def w0_of_g1g2(L, wl, g1, g2):
    r"""Radius of the beam, of wavelength :math:`\lambda`, at the waist position of a cavity
    of length :math:`L`, with mirror g-factors of :math:`g_1` and :math:`g_2`, respectively.

    .. math::
        w_0\left(L, \lambda, g_1, g_2\right) = \sqrt{
            \frac{L \lambda}{\pi}
            \sqrt{\frac{g_1 g_2 (1 - g_1 g_2)}{(g_1 + g_2 - 2 g_1 g_2)^2}}
        }
    """
    return np.sqrt(L * wl / np.pi * np.sqrt(g1 * g2 * (1 - g1 * g2) / (g1 + g2 - 2 * g1 * g2) ** 2))


@check_physical()
@ureg.wraps(ureg.meter, (ureg.meter, "", ""))
def z0_of_g1g2(L, g1, g2):
    r"""Waist position of a beam in a cavity of length :math:`L`, with mirror g-factors of
    :math:`g_1` and :math:`g_2`, respectively.

    .. math::
        z_0(L, g_1, g_2) = \frac{L g_2 (1 - g_1)}{g_1 + g_2 - 2 g_1 g_2}
    """
    return L * g2 * (1 - g1) / (g1 + g2 - 2 * g1 * g2)


def _rtgouy_of_g1g2_base(g1, g2):
    return 2 * np.arccos(np.sign(g1 + g2) * np.sqrt(g1 * g2))


@check_physical()
@ureg.wraps(ureg.radians, ("", ""))
def rtgouy_of_g1g2(g1, g2):
    r"""Round-trip gouy phase of a cavity with mirror g-factors of :math:`g_1` and
    :math:`g_2`, respectively.

    .. math::
        \psi(g_1, g_2) = 2\arccos{ \mathrm{sgn}\left(g_1 + g_2\right) \sqrt{g_1 g_2} }
    """
    return _rtgouy_of_g1g2_base(g1, g2)


@check_physical()
@ureg.wraps("", (ureg.meter, ureg.meter))
def g1_of_Rc1(L, Rc1):
    r"""Stability factor of the *first* mirror of a cavity of length :math:`L`, where
    this mirror has radius of curvature :math:`R_{C,1}`.

    .. math::
        g_1(L, R_{C,1}) = 1 - \frac{L}{R_{C,1}}
    """
    return 1 - L / Rc1


@check_physical()
@ureg.wraps("", (ureg.meter, ureg.meter))
def g2_of_Rc2(L, Rc2):
    r"""Stability factor of the *end* mirror of a cavity of length :math:`L`, where
    this mirror has radius of curvature :math:`R_{C,2}`.

    .. math::
        g_2(L, R_{C,2}) = 1 - \frac{L}{R_{C,2}}
    """
    return 1 - L / Rc2


@check_physical()
@ureg.wraps("", (ureg.meter, ureg.meter, ureg.meter, ureg.meter))
def g1_of_w1w2(L, wl, w1, w2):
    r"""Stability factor of the *first* mirror of a cavity of length :math:`L`, with
    beam radii at the mirrors of :math:`w_1` and :math:`w_2`, respectively; where the
    wavelength of the beam is :math:`\lambda`.

    .. math::
        g_1(L, \lambda, w_1, w_2) = \pm \frac{w_2}{w_1} \sqrt{
            1 - \left( \frac{L\lambda}{\pi w_1 w_2} \right)^2
        }
    """
    mag = np.sqrt(1 - ((L * wl / np.pi) / (w1 * w2)) ** 2)
    return (w2 / w1) * np.array([-mag, mag])


@check_physical()
@ureg.wraps("", (ureg.meter, ureg.meter, ureg.meter, ureg.meter))
def g2_of_w1w2(L, wl, w1, w2):
    r"""Stability factor of the *end* mirror of a cavity of length :math:`L`, with
    beam radii at the mirrors of :math:`w_1` and :math:`w_2`, respectively; where the
    wavelength of the beam is :math:`\lambda`.

    .. math::
        g_1(L, \lambda, w_1, w_2) = \pm \frac{w_1}{w_2} \sqrt{
            1 - \left( \frac{L\lambda}{\pi w_1 w_2} \right)^2
        }
    """
    mag = np.sqrt(1 - ((L * wl / np.pi) / (w1 * w2)) ** 2)
    return (w1 / w2) * np.array([-mag, mag])


@check_physical()
@ureg.wraps("", ("", ""))
def g_of_g1g2(g1, g2):
    r"""Stability factor of a cavity given mirror g-factors of :math:`g_1`
    and :math:`g_2`, respectively.

    .. math::
        g(g_1, g_2) = g_1 g_2
    """
    return g1 * g2


@check_physical()
@ureg.wraps(ureg.meter, (ureg.meter, ""))
def Rc1_of_g1(L, g1):
    r"""Radius of curvature of *first* mirror of a cavity of length :math:`L`,
    with the g-factor of this mirror being :math:`g_1`.

    .. math::
        R_{C,1} = \frac{L}{1 - g_1}
    """
    return L / (1 - g1)


@check_physical()
@ureg.wraps(ureg.meter, (ureg.meter, ""))
def Rc2_of_g2(L, g2):
    r"""Radius of curvature of *end* mirror of a cavity of length :math:`L`,
    with the g-factor of this mirror being :math:`g_2`.

    .. math::
        R_{C,2} = \frac{L}{1 - g_2}
    """
    return L / (1 - g2)


@check_physical()
@ureg.wraps(ureg.hertz, (ureg.meter, "", ""))
def modesep_of_g1g2(L, g1, g2):
    r"""Mode separation frequency of a cavity of length :math:`L`, with
    mirror g-factors of :math:`g_1` and :math:`g_2`, respectively.

    In the equation below, :math:`\nu(L)` is the FSR of the cavity, and :math:`\psi(g_1, g_2)`
    is the round-trip gouy phase.

    .. math::
        \delta f(L, g_1, g_2) = \begin{cases}
            \frac{\psi(g_1, g_2)}{2\pi}\,\nu(L) \quad \text{if }\, \psi < \pi,\\
            \nu(L)\left(1 - \frac{\psi(g_1, g_2)}{2\pi}\right) \quad \text{otherwise}
        \end{cases}
    """
    rtgouy = _rtgouy_of_g1g2_base(g1, g2)
    return modesep_adjust(rtgouy, L)
