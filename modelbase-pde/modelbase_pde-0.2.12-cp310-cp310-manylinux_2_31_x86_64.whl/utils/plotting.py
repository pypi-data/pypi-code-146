from __future__ import annotations

import math
from typing import Any

import matplotlib.patches as patches
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import animation
from matplotlib.animation import FuncAnimation
from matplotlib.axes import Axes
from matplotlib.figure import Figure
from numpy.typing import NDArray

from .coordinates import Oddq


def plot_leaf_axes(
    leaf: Any,
    figsize: tuple[float, float],
    ax: Axes | None = None,
) -> tuple[Figure, Axes]:
    if ax is None:
        fig, ax = plt.subplots(1, 1, figsize=figsize)
    else:
        fig = ax.get_figure()
    ax.set_aspect("equal")

    c, r = leaf.cells.shape
    x_lower = -1
    x_upper = 1 + 3 / 2 * (c - 1)
    y_lower = -math.sqrt(3) * 0.5
    y_upper = math.sqrt(3) * r
    ax.set_xlim(x_lower, x_upper)
    ax.set_ylim(y_lower, y_upper)
    ax.set_xticks([])
    ax.set_yticks([])
    return fig, ax


def plot_leaf_cells(
    leaf: Any,
    ax: Axes,
    concentrations: NDArray | None,
    min_conc: float | None = None,
    max_conc: float | None = None,
    alpha: float | None = None,
) -> Axes:
    if concentrations is None:
        concentrations = np.ones(leaf.gridsize)
        min_conc = 0
        max_conc = 1
    else:
        if min_conc is None:
            min_conc = np.min(
                concentrations[leaf.cells != 0]
            )  # Otherwise this is always 0
        if max_conc is None:
            max_conc = np.max(concentrations)
        assert min_conc is not None
        assert max_conc is not None
        if min_conc == max_conc:
            max_conc += 0.1

    normalized_concentrations = (concentrations - min_conc) / (
        max_conc - min_conc
    )

    def add_hexagon(
        c: float, r: float, color: str, alpha: float, ax: Axes = ax
    ) -> None:
        ax.add_patch(
            patches.RegularPolygon(
                Oddq(c, r).to_plot().coordinates,
                numVertices=6,
                radius=1,
                facecolor=color,
                alpha=alpha,
                orientation=np.radians(30),
                edgecolor="k",
            )
        )

    # Photosynthetic cells
    for c, r in zip(*np.where(leaf.cells == 1)):  # type: ignore
        if alpha is None:
            al = max(normalized_concentrations[c, r], 0.05)
        else:
            al = alpha
        add_hexagon(c, r, "green", al)

    # Veins
    for c, r in zip(*np.where(leaf.cells == 2)):  # type: ignore
        if alpha is None:
            al = max(normalized_concentrations[c, r], 0.05)
        else:
            al = alpha
        add_hexagon(c, r, "brown", al)

    # Stoma
    for c, r in zip(*np.where(leaf.cells == 3)):  # type: ignore
        if alpha is None:
            al = max(normalized_concentrations[c, r], 0.05)
        else:
            al = alpha
        add_hexagon(c, r, "blue", al)
    return ax


def plot_leaf_cell_annotations(
    leaf: Any,
    ax: Axes,
    concentrations: NDArray,
    **kwargs: dict[Any, Any],
):
    local_kwargs = {"ha": "center", "fontsize": 12}
    if kwargs:
        local_kwargs.update(kwargs)
    for c, r in zip(*np.where(leaf.cells != 0)):  # type: ignore
        ax.annotate(
            f"{concentrations[c, r]:.2g}",
            Oddq(c, r).to_plot().coordinates,
            **local_kwargs,
        )


def plot_leaf_cell_coordinates(
    leaf: Any,
    ax: Axes,
) -> None:
    for c, r in zip(*np.where(leaf.cells != 0)):  # type: ignore
        ax.annotate(f"{c, r}", Oddq(c, r).to_plot().coordinates, ha="center")


def plot_leaf(
    leaf: Any,
    concentrations: NDArray | None = None,
    min_conc: float | None = None,
    max_conc: float | None = None,
    figsize: tuple[float, float] = (10, 10),
    ax: Axes | None = None,
    annotate: bool = False,
    alpha: float | None = None,
    **kwargs,
):
    fig, ax = plot_leaf_axes(leaf, figsize=figsize, ax=ax)
    ax = plot_leaf_cells(
        leaf, ax, concentrations, min_conc, max_conc, alpha, **kwargs
    )
    if annotate:
        assert concentrations is not None
        ax = plot_leaf_cell_annotations(leaf, ax, concentrations, **kwargs)
    return fig, ax


def time_lapse(
    leaf: Any,
    y: list[NDArray],
    figsize: tuple[float, float] = (10, 10),
    ffmpeg_path: str = "/usr/bin/ffmpeg",
) -> FuncAnimation:
    plt.rcParams["animation.ffmpeg_path"] = ffmpeg_path
    fig, ax = plot_leaf_axes(leaf=leaf, figsize=figsize)
    plt.close()

    def init():
        ax.patches = []  # type: ignore
        return fig, ax

    def update_func(frame):
        ax.patches = []  # type: ignore
        ax.texts = []  # type: ignore
        y_current = y[frame]
        plot_leaf_cells(leaf=leaf, ax=ax, concentrations=y_current)
        plot_leaf_cell_annotations(leaf=leaf, ax=ax, concentrations=y_current)
        return None

    anim = animation.FuncAnimation(
        fig,
        update_func,
        frames=list(range(len(y) // 2)),
        init_func=init,
        repeat=False,
    )
    return anim
