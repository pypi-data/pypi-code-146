from __future__ import annotations

import math as _math
from typing import TypeAlias

import matplotlib.pyplot as _plt
from matplotlib.axes import Axes as Axis
from matplotlib.figure import Figure

from .plot import plotting_context, set_style

# FIXME: matplotlib gives Axes the list[list[Axis]] type
# even though it is an Array. Wait until matplotlib fixes this
Axes: TypeAlias = list[list[Axis]]


__all__ = [
    "axs_layout",
    "plotting_context",
    "format_xticklabels",
    "set_style",
]


def format_xticklabels(
    ax: Axis, rotation: float | None = None, ha: str | None = None
) -> None:
    ax.set_xticks(
        ax.get_xticks(), ax.get_xticklabels(), rotation=rotation, ha=ha
    )


def axs_layout(
    n: int,
    ncols: int,
    colwidth: int = 4,
    rowheight: int = 4,
    sharex: bool = True,
    sharey: bool = True,
) -> tuple[Figure, Axes]:
    nrows = _math.ceil(n / ncols)
    fig, axs = _plt.subplots(
        nrows,
        ncols,
        figsize=(ncols * colwidth, nrows * rowheight),
        sharex=sharex,
        sharey=sharey,
        squeeze=False,
    )
    return fig, axs
