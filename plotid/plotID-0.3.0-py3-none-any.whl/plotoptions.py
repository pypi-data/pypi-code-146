#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Contains the PlotOptions and PlotIDTransfer classes."""

import os
from typing import Any, Literal, TypedDict, TypeVar
import matplotlib.pyplot as plt
from PIL.Image import Image


kwargs_types = TypedDict(
    "kwargs_types",
    {
        "prefix": str,
        "id_method": Literal["time", "random"],
        "qrcode": bool,
    },
)


class PlotOptions:
    """
    Container objects which include all plot options provided by plotid.

    Methods
    -------
    __init__
    validate_input
        Check if input is correct type.
    validate_list
        Check if all elements of a given list are of certain type.

    Attributes
    ----------
    figs :
        Figures that will be tagged.
    rotation :
        Rotation angle for the ID.
    position :
        Relative position of the ID on the plot (x,y).
    **kwargs : dict, optional
        Extra arguments for additional plot options.

    Other Parameters
    ----------------
    figure_ids: str or list of str
        IDs that the figures are tagged with.
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
        Font that will be used to print the ID. A path to an .otf or a .ttf
        file has to be given. To use already installed fonts, you can search for the
        standard path of fonts on your operating system and give then the path of the
        desired font file to this parameter.
    fontsize: int, optional
        Fontsize for the displayed ID. Default: 12.
    fontcolor: tuple, optional
        Fontcolor for the ID. Must be given as tuple containing three rgb values with
        each value between [0, 1]. Default: (0, 0, 0).
    """

    def __init__(
        self,
        figs: plt.Figure | Image | list[plt.Figure | Image],
        rotation: int,
        position: tuple[float, float],
        **kwargs: Any,
    ) -> None:

        self.figs = figs
        self.figure_ids = kwargs.get("figure_ids", [])
        self.rotation = rotation
        self.position = position
        self.prefix = kwargs.get("prefix", "")
        self.id_method = kwargs.get("id_method", "time")
        # Overwrite id_method if figure_ids were defined by the user
        if self.figure_ids:
            self.id_method = "custom"
        self.qrcode = kwargs.get("qrcode", False)
        self.qr_position = kwargs.get("qr_position", (1, 0))
        self.qr_size = kwargs.get("qr_size", 100)
        self.id_on_plot = kwargs.get("id_on_plot", True)
        self.font = kwargs.get("font", False)
        if self.font:
            self.font = os.path.abspath(self.font)
        self.fontsize = kwargs.get("fontsize", 12)
        self.fontcolor = kwargs.get("fontcolor", (0, 0, 0))

    def __str__(self) -> str:
        """Representation if an object of this class is printed."""
        return str(self.__class__) + ": " + str(self.__dict__)

    def validate_input(self) -> None:
        """
        Validate if input for PlotOptions is correct type.

        Raises
        ------
        TypeError
            TypeError is thrown if one of the attributes is not of correct
            type.

        Returns
        -------
        None.

        """
        # Input validation for figs is done in submodules tagplot_$engine.py
        if not isinstance(self.prefix, str):
            raise TypeError("Prefix is not a string.")

        if not isinstance(self.id_method, str):
            raise TypeError("The chosen id_method is not a string.")

        # Store figs in a list, even if it is only one.
        if not isinstance(self.figs, list):
            self.figs = [self.figs]


class PlotIDTransfer:
    """
    Container to transfer objects from tagplot() to publish().

    Methods
    -------
    __init__

    Attributes
    ----------
    figs :
        Tagged figures.
    figure_ids:
        IDs that the figures are tagged with.
    """

    def __init__(
        self, figs: plt.Figure | Image | list[plt.Figure | Image], figure_ids: list[str]
    ) -> None:
        self.figs = figs
        self.figure_ids = figure_ids
        self.figure_ids = validate_list(self.figure_ids)

    def __str__(self) -> str:
        """Representation if an object of this class is printed."""
        return str(self.__class__) + ": " + str(self.__dict__)


T = TypeVar("T")


def validate_list(
    list_var: T | list[T] | object, elt_type: type = str, is_file: bool = False
) -> list[T]:
    """
    Validate if contents of a list are of specific type.

    Parameters
    ----------
    list_var :
        List or single string which contents will be validated.
    elt_type : datatype, optional
        Datatype of which the list elements must be type of. Otherwise
        an Error will be raised. The default is str.
    is_file : boolean, optional
        Flag to indicate if the list contains paths to files. If True the
        strings will be checked if they correspond to an existing file.
        The default is False.

    Raises
    ------
    TypeError
        If one of the list elements is not of type elt_type.
    FileNotFoundError
        If strings are also checked for existing files and one of the files
        does not exist.

    Returns
    -------
    list_var as list

    """
    if isinstance(list_var, elt_type):
        list_var = [list_var]
    if isinstance(list_var, list):
        for elt in list_var:
            if not isinstance(elt, elt_type):
                raise TypeError(
                    f"The list of {list_var} contains an "
                    f"object which is not of type {elt_type}."
                )
            if is_file:
                # Check if directory and files exist
                if not os.path.exists(elt):  # type: ignore
                    raise FileNotFoundError(
                        "The specified directory" f"/file {elt} does not exist."
                    )
    else:
        raise TypeError(
            f"The specified {list_var} are neither a "
            f"{elt_type} nor a list of {elt_type}."
        )
    return list_var
