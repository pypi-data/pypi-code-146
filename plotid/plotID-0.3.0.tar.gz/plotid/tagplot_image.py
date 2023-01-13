# -*- coding: utf-8 -*-
"""Tag your picture with an ID."""
import os
import warnings
from importlib.resources import files
from PIL import Image, ImageDraw, ImageFont
from plotid.create_id import create_id, create_qrcode
from plotid.plotoptions import PlotOptions, PlotIDTransfer


def tagplot_image(plotid_object: PlotOptions) -> PlotIDTransfer:
    """
    Add IDs to images/pictures with pillow.

    The ID is placed visual on the figure window and returned as string in a
    list together with the figures.

    Parameters
    ----------
    plotid_object : instance of PlotOptions

    Returns
    -------
    PlotIDTransfer object
    """
    # Check if plotid_object is a valid instance of PlotOptions
    if not isinstance(plotid_object, PlotOptions):
        raise TypeError(
            "The given options container is not an instance of PlotOptions."
        )

    # Check if figs is a list of files
    for img in plotid_object.figs:
        if not isinstance(img, str):
            raise TypeError("Name of the image is not a string.")
        if not os.path.isfile(img):
            raise TypeError(f"Image '{img}' does not exist.")
            # Check if figs is a valid file is done by pillow internally

    color = tuple(rgb_value * 255 for rgb_value in plotid_object.fontcolor)
    # font = ImageFont.load_default()
    font_path = (
        files("plotid.resources").joinpath("OpenSans").joinpath("OpenSans-Regular.ttf")
    )
    font = ImageFont.truetype(str(font_path), plotid_object.fontsize)

    if plotid_object.font:
        try:
            # Absolute path to font file (.ttf or .otf) has to be given
            font = ImageFont.truetype(plotid_object.font, plotid_object.fontsize)
        except OSError:
            warnings.warn("Font was not found.\nplotID continues with fallback font.")

    if plotid_object.font:
        try:
            # Absolute path to font file (.ttf or .otf) has to be given
            font = ImageFont.truetype(plotid_object.font, plotid_object.fontsize)
        except OSError:
            warnings.warn("Font was not found.\nplotID continues with fallback font.")

    for j, img in enumerate(plotid_object.figs):
        if plotid_object.id_method == "custom":
            # If IDs were given by the user, use them
            img_id: str = str(plotid_object.figure_ids[j])
        else:
            # Create ID with given method
            img_id = plotid_object.prefix + create_id(plotid_object.id_method)
            plotid_object.figure_ids.append(img_id)

        img = Image.open(img)

        if plotid_object.id_on_plot:
            # Create temporary PIL image to get correct textsize
            tmp_img = Image.new("L", (100, 100))
            tmp_draw = ImageDraw.Draw(tmp_img)
            textsize = tmp_draw.textsize(img_id, font)

            # Create new image with white background and the size of the textbox
            img_txt = Image.new("RGBA", textsize, color=(255, 255, 255, 0))
            draw_txt = ImageDraw.Draw(img_txt)
            draw_txt.text((0, 0), img_id, font=font, fill=color)
            # Rotate the image by the given angle
            txt = img_txt.rotate(plotid_object.rotation, expand=1)

            # Paste the txt/ID image with transparent background onto the original image
            img.paste(
                txt,
                (
                    int(img.width * plotid_object.position[0]),
                    int(img.height * (1 - plotid_object.position[1]) - txt.height),
                ),
                txt,
            )

        if plotid_object.qrcode:
            qrcode = create_qrcode(img_id)
            qrcode.thumbnail(
                (plotid_object.qr_size, plotid_object.qr_size), Image.ANTIALIAS
            )
            img.paste(
                qrcode,
                box=(
                    int(
                        img.width * plotid_object.qr_position[0] - plotid_object.qr_size
                    ),
                    int(
                        img.height * (1 - plotid_object.qr_position[1])
                        - plotid_object.qr_size
                    ),
                ),
            )
        plotid_object.figs[j] = img

    figs_and_ids = PlotIDTransfer(plotid_object.figs, plotid_object.figure_ids)
    return figs_and_ids
