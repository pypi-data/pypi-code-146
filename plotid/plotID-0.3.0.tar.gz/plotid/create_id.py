# -*- coding: utf-8 -*-
"""
Create an identifier to print it on a plot.

Functions:
    create_id(str) -> str
"""
import time
import uuid
import qrcode
from PIL import Image


def create_id(id_method: str) -> str:
    """
    Create an Identifier (str).

    Creates an (sometimes unique) identifier based on the selected method.

    Parameters
    ----------
    id_method : str
        id_method for creating the ID. Create an ID by Unix time is referenced
        as 'time', create a random ID with id_method='random'.

    Returns
    -------
    figure_id : str
    """
    match id_method:
        case "time":
            figure_id = hex(int(time.time()))  # convert UNIX Time to hexadecimal str
            time.sleep(1)  # break for avoiding duplicate IDs
        case "random":
            figure_id = str(uuid.uuid4())  # creates a random UUID
            figure_id = figure_id[0:8]  # only use first 8 numbers
        case _:
            raise ValueError(
                f'Your chosen ID method "{id_method}" is not supported.\n'
                "At the moment these methods are available:\n"
                '"time": Unix time converted to hexadecimal\n'
                '"random": Random UUID'
            )
    return figure_id


def create_qrcode(figure_id: str) -> Image:
    """
    Create a QR Code from an identifier.

    Parameters
    ----------
    figure_id : str
        Identifier which will be embedded in the qrcode.

    Returns
    -------
    QR Code as PilImage.
    """
    qrc = qrcode.QRCode(version=1, box_size=10, border=0)
    qrc.add_data(figure_id)
    qrc.make(fit=True)
    img = qrc.make_image(fill_color="black", back_color="white")

    return img
