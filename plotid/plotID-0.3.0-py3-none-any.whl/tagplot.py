#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tag your plot with an ID.

For publishing the tagged plot along your research data have a look at the
module publish.
"""

import warnings
from typing import Any, Literal
import matplotlib.pyplot as plt
from PIL.Image import Image

from plotid.plotoptions import PlotOptions, PlotIDTransfer
from plotid.tagplot_matplotlib import tagplot_matplotlib
from plotid.tagplot_image import tagplot_image


def tagplot(
    figs: plt.Figure | Image | list[plt.Figure | Image],
    engine: Literal["matplotlib", "image"],
    **kwargs: Any,
) -> PlotIDTransfer:
    """
    Tag your figure/plot with an ID.

    After determining the plot engine, tagplot calls the corresponding
    function which tags the plot.

    Parameters
    ----------
    figs :
        Figures that should be tagged.
    engine :
        Plot engine which should be used to tag the plot.
    **kwargs : dict, optional
        Extra arguments for additional plot options.

    Other Parameters
    ----------------
    figure_ids: list of str, optional
        IDs that will be printed on the plot. If empty, IDs will be generated for each
        plot. If this option is used, an ID for each plot has to be specified.
        Default: [].
    location : str, optional
        Location for ID to be displayed on the plot. Default is "east".
    rotation: float or int, optional
        Rotation of the printed ID in degree. Overwrites the value defined by location.
    position: tuple of float, optional
        Position of the ID given as (x,y). x and y are relative coordinates in respect
        to the figure size and must be in the intervall [0,1]. Overwrites the value
        defined by location.
    prefix : str, optional
        Will be added as prefix to the ID.
    id_method : str, optional
        id_method for creating the ID. Create an ID by Unix time is referenced
        as "time", create a random ID with id_method="random". The default is "time".
    qrcode : bool, optional
         Encode the ID in a QR code on the exported plot. Default: False.
    qr_position : tuple, optional
        Position of the bottom right corner of the QR Code on the plot in relative
        (x, y) coordinates. Default: (1, 0).
    qr_size: int or float, optional
        Size of the QR code in arbitrary units. Default: 100.
    id_on_plot: bool, optional
         Print ID on the plot. Default: True.
    font: str, optional
        Font that will be used to print the ID. An absolute path to an .otf or a .ttf
        file has to be given. To use already installed fonts, you can search for the
        standard path of fonts on your operating system and give then the path of the
        desired font file to this parameter.
    fontsize: int, optional
        Fontsize for the displayed ID. Default: 12.
    fontcolor: tuple, optional
        Fontcolor for the ID. Must be given as tuple containing three rgb values with
        each value between [0, 1]. Default: (0, 0, 0).

    Raises
    ------
    TypeError
        If specified location is not given as string.
        If rotation was not given as number.
        If position was not given as tuple containing two floats.
    ValueError
        If an unsupported plot engine is given.
        If position tuple does not contain two items.

    Returns
    -------
    list
        The resulting list contains two lists each with as many entries as
        figures were given. The first list contains the tagged figures.
        The second list contains the corresponding IDs as strings.
    """
    location = kwargs.get("location", "east")
    if not isinstance(location, str):
        raise TypeError("Location is not a string.")

    match location:
        case "north":
            rotation = 0
            position = (0.35, 0.975)
        case "east":
            rotation = 90
            position = (0.95, 0.35)
        case "south":
            rotation = 0
            position = (0.35, 0.015)
        case "west":
            rotation = 90
            position = (0.025, 0.35)
        case "southeast":
            rotation = 0
            position = (0.75, 0.015)
        case _:
            warnings.warn(
                f'Location "{location}" is not a defined '
                'location, TagPlot uses location "east" '
                "instead."
            )
            rotation = 90
            position = (0.975, 0.35)

    if "rotation" in kwargs:
        rotation = kwargs.pop("rotation")
        if not isinstance(rotation, (int, float)):
            raise TypeError("Rotation is not a float or integer.")
    if "position" in kwargs:
        position = kwargs.pop("position")
        if not isinstance(position, tuple):
            raise TypeError("Position is not a tuple of floats.")
        if not len(position) == 2:
            raise ValueError("Position does not contain two items.")
        if not all(isinstance(item, float) for item in position):
            raise TypeError("Position is not a tuple of floats.")

    option_container = PlotOptions(figs, rotation, position, **kwargs)
    option_container.validate_input()

    match engine:
        case "matplotlib" | "pyplot":
            return tagplot_matplotlib(option_container)
        case "image" | "fallback":
            return tagplot_image(option_container)
        case _:
            raise ValueError(f'The plot engine "{engine}" is not supported.')
