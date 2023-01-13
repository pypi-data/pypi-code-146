#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Export a plot figure to a picture file.

Functions:
    save_plot(figure, str) -> path-like
"""

import warnings
import matplotlib
import matplotlib.pyplot as plt
from PIL.Image import Image


def save_plot(
    figures: plt.Figure | Image, plot_names: str | list[str], extension: str = "png"
) -> list[str]:
    """
    Export plot(s).

    Parameters
    ----------
    figure :
        Figure that was tagged and now should be saved as picture.
    plot_name :
        Names of the files where the plots will be saved to.
    extension :
        File extension for the plot export.

    Returns
    -------
    plot_path :
        Names of the created pictures.
    """
    # Check if figs is a valid figure or a list of valid figures
    if isinstance(figures, matplotlib.figure.Figure):
        figures = [figures]
    # PIL has different classes for different file formats. Therefore, the
    # type is checked to contain 'PIL' and 'ImageFile'.
    if all(x in str(type(figures)) for x in ["PIL", "ImageFile"]):
        figures = [figures]
    if not isinstance(figures, list):
        raise TypeError("Figures are not given as list.")
    if isinstance(plot_names, str):
        plot_names = [plot_names]

    if len(plot_names) < len(figures):
        warnings.warn(
            "There are more figures than plot names. The first name"
            " will be taken for all plots with an appended number."
        )
        first_name = plot_names[0]
        plot_names = [""] * len(figures)
        for i, _ in enumerate(plot_names):
            plot_names[i] = first_name + f"{i+1}"
    elif len(plot_names) > len(figures):
        raise IndexError("There are more plot names than figures.")

    plot_path = []

    for i, fig in enumerate(figures):
        if isinstance(fig, matplotlib.figure.Figure):
            plt.figure(fig)
            plot_path.append(plot_names[i] + ".tmp." + extension)
            plt.savefig(plot_path[i])
        elif all(x in str(type(fig)) for x in ["PIL", "ImageFile"]):
            plot_path.append(plot_names[i] + ".tmp." + extension)
            fig.save(plot_path[i])
        else:
            raise TypeError(f"Figure number {i} is not a valid figure object.")

    return plot_path
