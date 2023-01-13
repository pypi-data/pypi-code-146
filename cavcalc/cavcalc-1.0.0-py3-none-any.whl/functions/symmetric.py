"""
Physical geometric-like parameter functions associated with symmetric optical cavities. Most properties
here are expressed only in terms of the g-factor of the cavity mirrors, as inter-dependent relations
between these properties are computed via target chaining in the core cavcalc code.

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
@ureg.wraps(ureg.meter, (ureg.meter, ureg.meter, ""))
def w_of_gsingle(L, wl, gsingle):
    r"""Radius of a beam, of wavelength :math:`\lambda`, on both mirrors of a symmetric cavity
    of length :math:`L` with mirror g-factors of :math:`g_s`.

    .. math::
        w\left(L, \lambda, g_s\right) = \sqrt{
            \frac{L \lambda}{\pi} \sqrt{\frac{1}{1 - g_s^2}}
        }
    """
    return np.sqrt(L * wl / np.pi * np.sqrt(1 / (1 - gsingle * gsingle)))


@check_physical()
@ureg.wraps(ureg.meter, (ureg.meter, ureg.meter, ""))
def w0_of_gsingle(L, wl, gsingle):
    r"""Radius of a beam, of wavelength :math:`\lambda`, at the waist position of a symmetric
    cavity of length :math:`L` with mirror g-factors of :math:`g_s`.

    .. math::
        w_0\left(L, \lambda, g_s\right) = \sqrt{
            \frac{L \lambda}{2\pi} \sqrt{\frac{1 + g_s}{1 - g_s}}
        }
    """
    return np.sqrt(0.5 * L * wl / np.pi * np.sqrt((1 + gsingle) / (1 - gsingle)))


@check_physical()
@ureg.wraps(ureg.meter, ureg.meter)
def z0_symmetric(L):
    r"""Waist position of a beam in a symmetric cavity of length :math:`L`.

    .. math::
        z_0(L) = \frac{L}{2}
    """
    return 0.5 * L


@check_physical()
@ureg.wraps(ureg.meter, (ureg.meter, ""))
def roc_of_gsingle(L, gsingle):
    r"""Radius of curvature of both cavity mirrors in a symmetric cavity of length :math:`L`,
    with mirror g-factors of :math:`g_s`.

    .. math::
        R_C(L, g_s) = \frac{L}{1 - g_s}
    """
    return L / (1 - gsingle)


@check_physical()
@ureg.wraps("", (ureg.meter, ureg.meter))
def gsingle_of_roc(L, Rc):
    r"""Mirror stability factor given radius of curvature :math:`R_C`, in a symmetric cavity
    of length :math:`L`.

    .. math::
        g_s(L, R_C) = 1 - \frac{L}{R_C}
    """
    return 1 - L / Rc


@check_physical()
@ureg.wraps("", (ureg.meter, ureg.meter, ureg.meter))
def gsingle_of_w(L, wl, w):
    r"""Mirror stability factor given beam radius (on both mirrors) of :math:`w`, in a symmetric
    cavity of length :math:`L`; where the beam has wavelength :math:`\lambda`.

    .. math::
        g_s(L, \lambda, w) = \pm \sqrt{
            1 - \left( \frac{L\lambda}{\pi w^2} \right)^2
        }
    """
    mag = np.sqrt(1 - (L * wl / (np.pi * w * w)) ** 2)
    return np.array([-mag, mag])


@check_physical()
@ureg.wraps("", ureg.radians)
def gsingle_of_rtgouy(rtgouy):
    r"""Mirror stability factor given round-trip gouy phase of :math:`\psi`, of a symmetric cavity.

    .. math::
        g_s(\psi) = \cos{\left(\frac{\psi}{2}\right)}
    """
    return np.cos(0.5 * rtgouy)


@check_physical()
@ureg.wraps("", (ureg.meter, ureg.meter, ureg.radians))
def gsingle_of_divang(L, wl, theta):
    r"""Mirror stability factor for a symmetric cavity of length :math:`L` with an eigenmode
    with divergence angle :math:`\theta`; where the beam has wavelength :math:`\lambda`.

    .. math::
        g_s(L, \lambda, \theta) = \frac{
            1 - \left(\frac{L\pi}{2\lambda}\right)^2 \tan^4{\theta}
        }{
            1 + \left(\frac{L\pi}{2\lambda}\right)^2 \tan^4{\theta}
        }
    """
    factor_L_wl = (L * np.pi / (2 * wl)) ** 2 * np.power(np.tan(theta), 4)
    return (1 - factor_L_wl) / (1 + factor_L_wl)


@check_physical()
@ureg.wraps("", (""))
def gsingle_of_gcav(gcav):
    r"""Mirror stability factor for a symmetric cavity with overall g-factor :math:`g`.

    .. math::
        g_s(g) = \pm \sqrt{g}
    """
    mag = np.sqrt(gcav)
    return np.array([-mag, mag])


@check_physical()
@ureg.wraps("", "")
def gcav_of_gsingle(gsingle):
    r"""Symmetric cavity stability factor given mirror g-factors of :math:`g_s`.

    .. math::
        g(g_s) = g_s^2
    """
    return gsingle * gsingle


def _rtgouy_of_gsingle_base(gsingle):
    return 2 * np.arccos(gsingle)


@check_physical()
@ureg.wraps(ureg.radians, "")
def rtgouy_of_gsingle(gsingle):
    r"""Round-trip gouy phase of a symmetric cavity with mirror g-factors of :math:`g_s`.

    .. math::
        \psi(g_s) = 2 \arccos{g_s}
    """
    return _rtgouy_of_gsingle_base(gsingle)


@check_physical()
@ureg.wraps(ureg.radians, (ureg.meter, ureg.meter, ""))
def divang_of_gsingle(L, wl, gsingle):
    r"""Divergence angle of the beam in a symmetric cavity of length :math:`L`, with
    mirror g-factors of :math:`g_s`; where the beam has wavelength :math:`\lambda`.

    .. math::
        \theta(L, \lambda, g_s) = \sqrt{
            \frac{2\lambda}{L\pi}
            \sqrt{\frac{1 - g_s}{1 + g_s}}
        }
    """
    return np.sqrt(2 * wl / (L * np.pi) * np.sqrt((1 - gsingle) / (1 + gsingle)))


@check_physical()
@ureg.wraps(ureg.hertz, (ureg.meter, ""))
def modesep_of_gsingle(L, gsingle):
    r"""Mode separation frequency for a symmetric cavity of length :math:`L`, with
    mirror g-factors of :math:`g_s`.

    In the equation below, :math:`\nu(L)` is the FSR of the cavity, and :math:`\psi(g_s)`
    is the round-trip gouy phase.

    .. math::
        \delta f(L, g_s) = \begin{cases}
            \frac{\psi(g_s)}{2\pi}\,\nu(L) \quad \text{if }\, \psi < \pi,\\
            \nu(L)\left(1 - \frac{\psi(g_s)}{2\pi}\right) \quad \text{otherwise}
        \end{cases}
    """
    rtgouy = _rtgouy_of_gsingle_base(gsingle)
    return modesep_adjust(rtgouy, L)
