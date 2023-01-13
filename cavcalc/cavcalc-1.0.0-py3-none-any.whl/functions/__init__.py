"""
The underlying functions used by cavcalc for computing the optical
resonator properties.

.. note::

    Whilst the underlying functions in this sub-package are publicly accessible, it is
    recommended that you instead use the single-function interface :func:`.calculate` for
    computing any of the cavity properties that you need; as that will result in a nice output
    object for accessing results.

    If, for whatever reason, you do choose to use any of the functions listed in the
    sub-modules below, please note that all of these *require* that the arguments passed to
    them are ``pint.Quantity`` instances.
"""

from . import resonance
from . import symmetric
from . import asymmetric
