"""Local environment settings modification for cavcalc."""

import os
import warnings

from . import _CONFIG
from .errors import CavCalcError


class _ConfigureContext:
    def __init__(self, previous_units: dict[str, str], original_rc_params: dict):
        self.__prev = previous_units
        self.__orig_rc = original_rc_params

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        _CONFIG["units"].update(self.__prev)
        if self.__orig_rc:
            import matplotlib.pyplot as plt

            dict.update(plt.rcParams, self.__orig_rc)


def configure(plt_style=None, **param_units):
    """Configure cavcalc plotting style, and parameter unit overrides.

    This function can be used both regularly, and via context-managed scopes using
    the ``with`` statement. In the latter case, any changes made via these configuration
    options will be reset on exit from the context-managed block.

    Parameters
    ----------
    plt_style : (str | dict | Path | list)
        The style-sheet to use, see :func:`matplotlib.pyplot.style.use` for details. Note
        that, in addition to the options specified in the linked matplotlib documentation,
        one can set this to ``"cavcalc"`` to use the default style-sheet that this package
        provides. This argument defaults to ``None``, such that no style modification
        is performed (and matplotlib not imported); this way, the default behaviour of
        this function is to have as minimal impact on the users' development workflow
        as possible.

    **param_units : dict
        Keyword arguments specifying overrides for the units of any cavcalc parameter or
        parameter category. The names of these correspond exactly to those in the units
        section of a ``cavcalc.ini`` config file.

    Examples
    --------
    If you simply want to set-up the plotting style to be the same as the default
    behaviour when running cavcalc from the command line, then do::

        import cavcalc as cc
        cc.configure(plt_style="cavcalc")

    or, if you only want to use this style-sheet temporarily::

        import numpy as np

        with cc.configure(plt_style="cavcalc"):
            # do stuff with cavcalc, e.g:
            cc.calculate("w", L=1, Rc=np.linspace(1, 5, 101)).plot()
    """
    if plt_style:
        import matplotlib.pyplot as plt

        if isinstance(plt_style, str) and plt_style.casefold() == "cavcalc":
            here, _ = os.path.split(os.path.realpath(__file__))
            cc_style_file = os.path.join(here, "_default.mplstyle")
            if not os.path.isfile(cc_style_file):
                raise CavCalcError("Could not locate cavcalc package style-sheet file!")

            plt_style = cc_style_file

        orig_rc = dict(plt.rcParams.copy())
        plt.style.use(plt_style)
    else:
        orig_rc = None

    children_map = {
        "angles": ("div",),
        "beamsizes": ("w", "w1", "w2", "w0"),
        "rocs": ("Rc", "Rc1", "Rc2"),
        "distances": ("L", "z0"),
        "frequencies": ("FSR", "FWHM", "modesep", "pole"),
        "phases": ("gouy",),
        "waves": ("wl",),
    }
    for pcat, params in children_map.items():
        if pcat_units := param_units.get(pcat):
            for p in params:
                # Only use category override if specific units
                # override is *not* also in the kwargs
                param_units.setdefault(p, pcat_units)

            del param_units[pcat]

    cfg_units = _CONFIG["units"]
    prev = {}
    for p, units in param_units.items():
        if curr_units := cfg_units.get(p):
            prev[p] = curr_units
            cfg_units[p] = units
        else:
            warnings.warn(f"Ignoring units override for invalid parameter name: {p}")

    return _ConfigureContext(prev, orig_rc)
