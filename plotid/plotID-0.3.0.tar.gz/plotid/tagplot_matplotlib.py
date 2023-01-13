# -*- coding: utf-8 -*-
"""Tag your matplotlib plot with an ID."""

from importlib.resources import files
import matplotlib
import matplotlib.pyplot as plt
from PIL import Image
from plotid.create_id import create_id, create_qrcode
from plotid.plotoptions import PlotOptions, PlotIDTransfer


def tagplot_matplotlib(plotid_object: PlotOptions) -> PlotIDTransfer:
    """
    Add IDs to figures with matplotlib.

    The ID is placed visual on the figure window and returned as string in a
    list together with the figures.

    Parameters
    ----------
    plotid_object :
        Object containing the figures and all additional options.

    Returns
    -------
    PlotIDTransfer object
    """
    # Check if plotid_object is a valid instance of PlotOptions
    if not isinstance(plotid_object, PlotOptions):
        raise TypeError(
            "The given options container is not an instance of PlotOptions."
        )

    # Check if figs is a list of valid figures
    for figure in plotid_object.figs:
        if not isinstance(figure, matplotlib.figure.Figure):
            raise TypeError("Figure is not a valid matplotlib-figure.")

    if plotid_object.font:
        # Load custom font into matplotlib
        matplotlib.font_manager.fontManager.addfont(plotid_object.font)
        font = matplotlib.font_manager.FontProperties(fname=plotid_object.font)
    else:
        font = (
            files("plotid.resources")
            .joinpath("OpenSans")
            .joinpath("OpenSans-Regular.ttf")
        )
        matplotlib.font_manager.fontManager.addfont(str(font))
        font = matplotlib.font_manager.FontProperties(fname=font)

    # Loop to create and position the IDs
    for j, fig in enumerate(plotid_object.figs):
        if plotid_object.id_method == "custom":
            # If IDs were given by the user, use them
            fig_id: str = str(plotid_object.figure_ids[j])
        else:
            # Create ID with given method
            fig_id = create_id(plotid_object.id_method)
            fig_id = plotid_object.prefix + fig_id
            plotid_object.figure_ids.append(fig_id)
        plt.figure(fig)

        if plotid_object.id_on_plot:

            plt.figtext(
                x=plotid_object.position[0],
                y=plotid_object.position[1],
                s=fig_id,
                rotation=plotid_object.rotation,
                fontsize=plotid_object.fontsize,
                color=plotid_object.fontcolor,
                font=font,
            )

        if plotid_object.qrcode:
            qrcode = create_qrcode(fig_id)
            qrcode.thumbnail(
                (plotid_object.qr_size, plotid_object.qr_size), Image.ANTIALIAS
            )
            fig.figimage(
                qrcode,
                fig.bbox.xmax * plotid_object.qr_position[0] - plotid_object.qr_size,
                fig.bbox.ymax * plotid_object.qr_position[1],
                cmap="bone",
            )
            fig.tight_layout()

    figs_and_ids = PlotIDTransfer(plotid_object.figs, plotid_object.figure_ids)
    return figs_and_ids
