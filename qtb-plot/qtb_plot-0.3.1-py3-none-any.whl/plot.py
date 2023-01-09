from __future__ import annotations

import itertools
import warnings
from contextlib import contextmanager
from typing import Any, Generator

import cycler
import matplotlib.pyplot as plt

from . import colors

# Matplotlib issues quite a lot of DeprecationWarnings when calling
# rcParams, as some of the parameters are going to be deprecated.
# However, since none of the parameters is used here, I just filter them out
warnings.simplefilter("ignore")


def set_style(context: str = "notebook", colorscheme: str = "mpl") -> None:

    base_context = {
        # Figure
        "figure.facecolor": "white",
        # Axes
        "axes.labelcolor": colors.dark_gray,
        "axes.facecolor": "white",
        "axes.edgecolor": "white",
        "axes.linewidth": 1,
        # Axis
        "axes.axisbelow": True,
        "xtick.direction": "out",
        "ytick.direction": "out",
        "xtick.color": colors.dark_gray,
        "ytick.color": colors.dark_gray,
        # Grid
        "axes.grid": True,
        "grid.color": colors.light_gray,
        "grid.linestyle": "-",
        "grid.linewidth": 1,
        # Text
        "text.color": colors.dark_gray,
        "font.family": ["sans-serif"],
        "font.sans-serif": [
            "Arial",
            "DejaVu Sans",
            "Liberation Sans",
            "Bitstream Vera Sans",
            "sans-serif",
        ],
        # Legend
        "legend.frameon": False,
        "legend.numpoints": 1,
        "legend.scatterpoints": 1,
        "legend.borderaxespad": 0,
        "legend.loc": "upper left",
        # Lines
        "lines.solid_capstyle": "round",
        "lines.markersize": 7,
        "lines.markeredgewidth": 0,
        "lines.linewidth": 2,
        # Colormap
        "image.cmap": "viridis",
        # Ticks
        "xtick.major.size": 6,
        "ytick.major.size": 6,
        "xtick.minor.size": 3,
        "ytick.minor.size": 3,
        "xtick.major.width": 1,
        "ytick.major.width": 1,
        "xtick.minor.width": 0.5,
        "ytick.minor.width": 0.5,
        "xtick.major.pad": 7,
        "ytick.major.pad": 7,
        # Patches
        "patch.linewidth": 0.3,
    }

    contexts = {
        "notebook": {
            "figure.figsize": (8, 6),
            "font.size": 14,
            "axes.labelsize": 14,
            "axes.titlesize": 18,
            "xtick.labelsize": 12,
            "ytick.labelsize": 12,
            "legend.fontsize": 12,
            "lines.linewidth": 3,
        },
        "presentation": {
            "figure.figsize": (16, 9),
            "figure.dpi": 150.0,
            "savefig.bbox": "tight",
            "font.size": 16,
            "axes.titlesize": 26,
            "axes.labelsize": 18,
            "legend.fontsize": 16,
            "xtick.labelsize": 18,
            "ytick.labelsize": 18,
            "lines.linewidth": 4,
        },
    }

    clrs = colors.colorschemes[colorscheme]
    linestyles = ("-", "--", "-.", ":")
    ls = []
    for i in linestyles:
        for j in itertools.repeat(i, len(clrs)):
            ls.append(j)

    base_context.update(
        {
            "axes.prop_cycle": cycler.cycler("color", clrs) * len(linestyles)
            + cycler.cycler("linestyle", ls)
        }
    )

    plt.rcParams.update(base_context)
    plt.rcParams.update(contexts[context])


@contextmanager
def plotting_context(
    context: str = "notebook",
    colorscheme: str = "mpl",
    *args: Any,
    **kwargs: Any,
) -> Generator:
    rc_orig = plt.rcParams.copy()
    try:
        set_style(context=context, colorscheme=colorscheme)
        yield None
    finally:
        plt.rcParams.update(rc_orig)
