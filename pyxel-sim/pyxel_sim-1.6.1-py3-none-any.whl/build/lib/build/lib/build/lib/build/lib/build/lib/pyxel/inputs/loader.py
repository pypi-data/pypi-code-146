#  Copyright (c) European Space Agency, 2017, 2018, 2019, 2020, 2021, 2022.
#
#  This file is subject to the terms and conditions defined in file 'LICENCE.txt', which
#  is part of this Pyxel package. No part of the package, including
#  this file, may be copied, modified, propagated, or distributed except according to
#  the terms contained in the file ‘LICENCE.txt’.

"""Subpackage to load images and tables."""

from contextlib import suppress
from io import BytesIO
from pathlib import Path
from typing import TYPE_CHECKING, Union

import fsspec
import numpy as np
from PIL import Image

from pyxel.options import global_options

if TYPE_CHECKING:
    import pandas as pd


def load_image(filename: Union[str, Path]) -> np.ndarray:
    """Load a 2D image.

    Parameters
    ----------
    filename : str or Path
        Filename to read an image.
        {.npy, .fits, .txt, .data, .jpg, .jpeg, .bmp, .png, .tiff} are accepted.

    Returns
    -------
    array : ndarray
        A 2D array.

    Raises
    ------
    FileNotFoundError
        If an image is not found.
    ValueError
        When the extension of the filename is unknown or separator is not found.

    Examples
    --------
    >>> from pyxel import load_image
    >>> load_image("frame.fits")
    array([[-0.66328494, -0.63205819, ...]])

    >>> load_image("https://hostname/folder/frame.fits")
    array([[-0.66328494, -0.63205819, ...]])

    >>> load_image("another_frame.npy")
    array([[-1.10136521, -0.93890239, ...]])

    >>> load_image("rgb_frame.jpg")
    array([[234, 211, ...]])
    """
    # Extract suffix (e.g. '.txt', '.fits'...)
    suffix: str = Path(filename).suffix.lower()

    if isinstance(filename, Path):
        full_filename: Path = filename.expanduser().resolve()
        if not full_filename.exists():
            raise FileNotFoundError(f"Input file '{full_filename}' can not be found.")

        url_path: str = str(full_filename)

    else:
        url_path = filename

    # Define extra parameters to use with 'fsspec'
    extras = {}
    if global_options.cache_enabled:
        url_path = f"simplecache::{url_path}"

        if global_options.cache_folder:
            extras["simplecache"] = {"cache_storage": global_options.cache_folder}

    if suffix.startswith(".fits"):
        with fsspec.open(url_path, mode="rb", **extras) as file_handler:

            from astropy.io import fits  # Late import to speed-up general import time

            with BytesIO(file_handler.read()) as content:
                data_2d: np.ndarray = fits.getdata(content)

    elif suffix.startswith(".npy"):
        with fsspec.open(url_path, mode="rb", **extras) as file_handler:
            data_2d = np.load(file_handler)

    elif suffix.startswith((".txt", ".data")):
        for sep in ("\t", " ", ",", "|", ";"):
            with suppress(ValueError):
                with fsspec.open(url_path, mode="r", **extras) as file_handler:
                    data_2d = np.loadtxt(file_handler, delimiter=sep, ndmin=2)
                break
        else:
            raise ValueError(f"Cannot find the separator for filename '{url_path}'.")

    elif suffix.startswith((".jpg", ".jpeg", ".png", ".bmp", ".tiff", ".tif")):
        with fsspec.open(url_path, mode="rb", **extras) as file_handler:
            image_2d = Image.open(file_handler)
            image_2d_converted = image_2d.convert("LA")  # RGB to grayscale conversion

        data_2d = np.array(image_2d_converted)[:, :, 0]

    else:
        raise ValueError(
            "Image format not supported. List of supported image formats: "
            ".npy, .fits, .txt, .data, .jpg, .jpeg, .bmp, .png, .tiff, .tif."
        )

    return data_2d


def load_table(filename: Union[str, Path], header: bool = False) -> "pd.DataFrame":
    """Load a table from a file and returns a pandas dataframe. No header is expected in xlsx.

    Parameters
    ----------
    filename : str or Path
        Filename to read the table.
        {.npy, .xlsx, .csv, .txt., .data} are accepted.
    header : bool, default: False
        Remove the header.

    Returns
    -------
    DataFrame

    Raises
    ------
    FileNotFoundError
        If an image is not found.
    ValueError
        When the extension of the filename is unknown or separator is not found.
    """
    # Late import to speedup start-up time
    import pandas as pd

    suffix: str = Path(filename).suffix.lower()

    if isinstance(filename, Path):
        full_filename = Path(filename).expanduser().resolve()
        if not full_filename.exists():
            raise FileNotFoundError(f"Input file '{full_filename}' can not be found.")

        url_path: str = str(full_filename)
    else:
        url_path = filename

    # Define extra parameters to use with 'fsspec'
    extras = {}
    if global_options.cache_enabled:
        url_path = f"simplecache::{url_path}"

        if global_options.cache_folder:
            extras["simplecache"] = {"cache_storage": global_options.cache_folder}

    if suffix.startswith(".npy"):
        with fsspec.open(url_path, mode="rb", **extras) as file_handler:
            table = pd.DataFrame(np.load(file_handler), dtype="float")

    elif suffix.startswith(".xlsx"):
        with fsspec.open(url_path, mode="rb", **extras) as file_handler:
            table = pd.read_excel(
                file_handler,
                header=0 if header else None,
                convert_float=False,
            )

    elif suffix.startswith(".csv"):
        for sep in ("\t", " ", ",", "|", ";"):
            with suppress(ValueError):
                # numpy will return ValueError with a wrong delimiter
                with fsspec.open(url_path, mode="r", **extras) as file_handler:
                    table = pd.read_csv(
                        file_handler,
                        delimiter=sep,
                        header=0 if header else None,
                        dtype="float",
                    )
                    break
        else:
            raise ValueError("Cannot find the separator.")

    elif suffix.startswith((".txt", ".data")):
        for sep in ("\t", " ", ",", "|", ";"):
            with suppress(ValueError):
                with fsspec.open(url_path, mode="r", **extras) as file_handler:
                    table = pd.read_table(
                        file_handler,
                        delimiter=sep,
                        header=0 if header else None,
                        dtype="float",
                    )
                    break
        else:
            raise ValueError("Cannot find the separator.")

    else:
        raise ValueError("Only .npy, .xlsx, .csv, .txt and .data implemented.")

    return table


def load_datacube(filename: Union[str, Path]) -> np.ndarray:
    """Load a 3D datacube.

    Parameters
    ----------
    filename : str or Path
        Filename to read a datacube.
        {.npy} are accepted.

    Returns
    -------
    array : ndarray
        A 3D array.

    Raises
    ------
    FileNotFoundError
        If an image is not found.
    ValueError
        When the extension of the filename is unknown or separator is not found.
    """
    # Extract suffix (e.g. '.txt', '.fits'...)
    suffix: str = Path(filename).suffix.lower()

    if isinstance(filename, Path):
        full_filename: Path = filename.expanduser().resolve()
        if not full_filename.exists():
            raise FileNotFoundError(f"Input file '{full_filename}' can not be found.")

        url_path: str = str(full_filename)

    else:
        url_path = filename

    # Define extra parameters to use with 'fsspec'
    extras = {}
    if global_options.cache_enabled:
        url_path = f"simplecache::{url_path}"

        if global_options.cache_folder:
            extras["simplecache"] = {"cache_storage": global_options.cache_folder}

    if suffix.startswith(".npy"):
        with fsspec.open(url_path, mode="rb", **extras) as file_handler:
            data_3d: np.ndarray = np.load(file_handler)
        if np.ndim(data_3d) != 3:
            raise ValueError("Input datacube is not 3-dimensional!")

    else:
        raise ValueError(
            "Image format not supported. List of supported image formats: .npy"
        )

    return data_3d
