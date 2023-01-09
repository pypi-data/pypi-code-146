#  Copyright (c) European Space Agency, 2017, 2018, 2019, 2020, 2021, 2022.
#
#  This file is subject to the terms and conditions defined in file 'LICENCE.txt', which
#  is part of this Pyxel package. No part of the package, including
#  this file, may be copied, modified, propagated, or distributed except according to
#  the terms contained in the file ‘LICENCE.txt’.

import os
import re
from pathlib import Path
from typing import Optional, Union, no_type_check

import numpy as np
import pandas as pd
import pytest
from astropy.io import fits
from PIL import Image
from pytest_httpserver import HTTPServer  # pip install pytest-httpserver

import pyxel


@pytest.fixture
def valid_multiple_hdus() -> fits.HDUList:
    """Create a valid HDUList with one 'PrimaryHDU' and one 'ImageHDU'."""
    # Create a new image
    primary_2d = np.array([[5, 6], [7, 8]], dtype=np.uint16)
    secondary_2d = np.array([[9, 10], [11, 12]], dtype=np.uint16)

    hdu_primary = fits.PrimaryHDU(primary_2d)
    hdu_secondary = fits.ImageHDU(secondary_2d)
    hdu_lst = fits.HDUList([hdu_primary, hdu_secondary])

    return hdu_lst


@pytest.fixture
def valid_pil_image() -> Image.Image:
    """Create a valid RGB PIL image."""
    data_2d = np.array([[10, 20], [30, 40]], dtype="uint8")
    pil_image = Image.fromarray(data_2d).convert("RGB")

    return pil_image


@no_type_check
@pytest.fixture
def valid_data2d_http_hostname(
    tmp_path: Path,
    httpserver: HTTPServer,
    valid_pil_image: Image.Image,
    valid_multiple_hdus: fits.HDUList,
) -> str:
    """Create valid 2D files on a temporary folder and HTTP server."""
    # Get current folder
    current_folder: Path = Path().cwd()

    try:
        os.chdir(tmp_path)

        # Create folder 'data'
        Path("data").mkdir(parents=True, exist_ok=True)

        data_2d = np.array([[1, 2], [3, 4]], dtype=np.uint16)

        # Save 2d images
        fits.writeto("data/img.fits", data=data_2d)
        fits.writeto("data/img2.FITS", data=data_2d)
        valid_multiple_hdus.writeto("data/img_multiple.fits")
        valid_multiple_hdus.writeto("data/img_multiple2.FITS")
        np.save("data/img.npy", arr=data_2d)
        np.savetxt("data/img_tab.txt", X=data_2d, delimiter="\t")
        np.savetxt("data/img_space.txt", X=data_2d, delimiter=" ")
        np.savetxt("data/img_comma.txt", X=data_2d, delimiter=",")
        np.savetxt("data/img_pipe.txt", X=data_2d, delimiter="|")
        np.savetxt("data/img_semicolon.txt", X=data_2d, delimiter=";")

        valid_pil_image.save("data/img.jpg")
        valid_pil_image.save("data/img.jpeg")
        valid_pil_image.save("data/img.png")
        valid_pil_image.save("data/img2.PNG")
        valid_pil_image.save("data/img.tiff")
        valid_pil_image.save("data/img.tif")
        valid_pil_image.save("data/img.bmp")

        text_filenames = [
            "data/img_tab.txt",
            "data/img_space.txt",
            "data/img_comma.txt",
            "data/img_pipe.txt",
            "data/img_semicolon.txt",
        ]

        # Put text data in a fake HTTP server
        for filename in text_filenames:
            with open(filename) as fh:
                response_data: str = fh.read()
                httpserver.expect_request(f"/{filename}").respond_with_data(
                    response_data, content_type="text/plain"
                )

        binary_filenames = [
            ("data/img.fits", "text/plain"),  # TODO: Change this type
            ("data/img2.FITS", "text/plain"),  # TODO: Change this type
            ("data/img_multiple.fits", "text/plain"),  # TODO: Change this type
            ("data/img_multiple2.FITS", "text/plain"),  # TODO: Change this type
            ("data/img.npy", "text/plain"),  # TODO: Change this type
            ("data/img.jpg", "image/jpeg"),
            ("data/img.jpeg", "image/jpeg"),
            ("data/img.png", "image/png"),
            ("data/img2.PNG", "image/png"),
            ("data/img.tif", "image/tiff"),
            ("data/img.tiff", "image/tiff"),
            ("data/img.bmp", "image/bmp"),
        ]

        # Put binary data in a fake HTTP server
        for filename, content_type in binary_filenames:
            with open(filename, "rb") as fh:
                response_data_bytes: bytes = fh.read()
                httpserver.expect_request(f"/{filename}").respond_with_data(
                    response_data_bytes, content_type=content_type
                )

        # Extract an url (e.g. 'http://localhost:59226/)
        url: str = httpserver.url_for("")

        # Extract the hostname (e.g. 'localhost:59226')
        hostname: str = re.findall("http://(.*)/", url)[0]

        yield hostname

    finally:
        os.chdir(current_folder)


@pytest.fixture
def invalid_data2d_hostname(tmp_path: Path, httpserver: HTTPServer) -> str:
    """Create invalid 2D files on a temporary folder and HTTP server."""
    # Get current folder
    current_folder: Path = Path().cwd()

    try:
        os.chdir(tmp_path)

        # Create folder 'data'
        Path("invalid_data").mkdir(parents=True, exist_ok=True)

        data_2d = np.array([[1, 2], [3, 4]], dtype=np.uint16)

        np.savetxt("invalid_data/img_X.txt", X=data_2d, delimiter="X")

        text_filenames = ["invalid_data/img_X.txt"]

        # Put text data in a fake HTTP server
        for filename in text_filenames:
            with open(filename) as fh:
                response_data: str = fh.read()
                httpserver.expect_request(f"/{filename}").respond_with_data(
                    response_data, content_type="text/plain"
                )

        # Extract an url (e.g. 'http://localhost:59226/)
        url: str = httpserver.url_for("")

        # Extract the hostname (e.g. 'localhost:59226')
        hostname: str = re.findall("http://(.*)/", url)[0]

        yield hostname

    finally:
        os.chdir(current_folder)


@pytest.fixture
def valid_table_http_hostname(tmp_path: Path, httpserver: HTTPServer) -> str:
    """Create valid tables locally and on a temporary HTTP server."""
    # Get current folder
    current_folder: Path = Path().cwd()

    try:
        os.chdir(tmp_path)

        # Create folder 'data'
        Path("data").mkdir(parents=True, exist_ok=True)

        df = pd.DataFrame(
            [[1, 2, 3], [4, 5, 6], [7, 8, 9]],
            columns=["col1", "col2", "col3"],
            dtype=float,
        )

        # Save tables
        df.to_csv("data/table_tab.txt", header=False, index=False, sep="\t")
        df.to_csv("data/table_space.TXT", header=False, index=False, sep=" ")
        df.to_csv("data/table_comma.data", header=False, index=False, sep=",")
        df.to_csv("data/table_pipe.txt", header=False, index=False, sep="|")
        df.to_csv("data/table_semicolon.txt", header=False, index=False, sep=";")

        df.to_csv("data/table_tab_with_header.txt", header=True, index=False, sep="\t")
        df.to_csv("data/table_space_with_header.TXT", header=True, index=False, sep=" ")
        df.to_csv(
            "data/table_comma_with_header.data", header=True, index=False, sep=","
        )
        df.to_csv("data/table_pipe_with_header.txt", header=True, index=False, sep="|")
        df.to_csv(
            "data/table_semicolon_with_header.txt", header=True, index=False, sep=";"
        )

        df.to_excel("data/table.xlsx", header=False, index=False)
        df.to_excel("data/table_with_header.xlsx", header=True, index=False)

        np.save("data/table.npy", arr=df.to_numpy())

        text_filenames = [
            "data/table_tab.txt",
            "data/table_space.TXT",
            "data/table_comma.data",
            "data/table_pipe.txt",
            "data/table_semicolon.txt",
            "data/table_tab_with_header.txt",
            "data/table_space_with_header.TXT",
            "data/table_comma_with_header.data",
            "data/table_pipe_with_header.txt",
            "data/table_semicolon_with_header.txt",
        ]

        # Put text data in a fake HTTP server
        for filename in text_filenames:
            with open(filename) as fh:
                response_data: str = fh.read()
                httpserver.expect_request(f"/{filename}").respond_with_data(
                    response_data, content_type="text/plain"
                )

        binary_filenames = [
            ("data/table.xlsx", "application/octet-stream"),
            ("data/table_with_header.xlsx", "application/octet-stream"),
            ("data/table.npy", "application/octet-stream"),
        ]

        # Put binary data in a fake HTTP server
        for filename, content_type in binary_filenames:
            with open(filename, "rb") as fh:
                response_data_bytes: bytes = fh.read()
                httpserver.expect_request(f"/{filename}").respond_with_data(
                    response_data_bytes, content_type=content_type
                )

        # Extract an url (e.g. 'http://localhost:59226/)
        url: str = httpserver.url_for("")

        # Extract the hostname (e.g. 'localhost:59226')
        hostname: str = re.findall("http://(.*)/", url)[0]

        yield hostname

    finally:
        os.chdir(current_folder)


@pytest.fixture
def invalid_table_http_hostname(tmp_path: Path, httpserver: HTTPServer) -> str:
    """Create invalid tables on temporary folder and HTTP server."""
    # Get current folder
    current_folder: Path = Path().cwd()

    try:
        os.chdir(tmp_path)

        # Create folder 'data'
        Path("invalid_data").mkdir(parents=True, exist_ok=True)

        df = pd.DataFrame([[1, 2, 3], [4, 5, 6], [7, 8, 9]], dtype=float)

        # Save tables
        df.to_csv("invalid_data/table_X.txt", header=False, index=False, sep="X")
        Path("invalid_data/table_empty.txt").touch()

        text_filenames = [
            "invalid_data/table_X.txt",
            "invalid_data/table_empty.txt",
        ]

        # Put text data in a fake HTTP server
        for filename in text_filenames:
            with open(filename) as fh:
                response_data: str = fh.read()
                httpserver.expect_request(f"/{filename}").respond_with_data(
                    response_data, content_type="text/plain"
                )

        # Extract an url (e.g. 'http://localhost:59226/)
        url: str = httpserver.url_for("")

        # Extract the hostname (e.g. 'localhost:59226')
        hostname: str = re.findall("http://(.*)/", url)[0]

        yield hostname

    finally:
        os.chdir(current_folder)


@pytest.mark.parametrize(
    "filename, exp_error, exp_message",
    [
        ("dummy", ValueError, "Image format not supported"),
        ("dummy.foo", ValueError, "Image format not supported"),
        ("unknown.fits", FileNotFoundError, None),
        (Path("unknown.fits"), FileNotFoundError, r"can not be found\.$"),
        ("https://domain/unknown.fits", FileNotFoundError, None),
        ("invalid_data/img_X.txt", ValueError, "Cannot find the separator"),
        (
            "http://{host}/invalid_data/img_X.txt",
            ValueError,
            "Cannot find the separator",
        ),
    ],
)
def test_invalid_filename(
    invalid_data2d_hostname: str,
    filename,
    exp_error: TypeError,
    exp_message: Optional[str],
):
    """Test invalid filenames."""
    if isinstance(filename, str):
        new_filename: str = filename.format(host=invalid_data2d_hostname)
    else:
        new_filename = filename

    with pytest.raises(exp_error, match=exp_message):
        _ = pyxel.load_image(new_filename)


@pytest.mark.parametrize("with_caching", [False, True])
@pytest.mark.parametrize(
    "filename, exp_data",
    [
        # FITS files
        ("data/img.fits", np.array([[1, 2], [3, 4]], np.uint16)),
        ("data/img2.FITS", np.array([[1, 2], [3, 4]], np.uint16)),
        ("data/img_multiple.fits", np.array([[5, 6], [7, 8]], np.uint16)),
        ("data/img_multiple2.FITS", np.array([[5, 6], [7, 8]], np.uint16)),
        (Path("data/img.fits"), np.array([[1, 2], [3, 4]], np.uint16)),
        (Path("./data/img.fits"), np.array([[1, 2], [3, 4]], np.uint16)),
        (Path("data/img_multiple.fits"), np.array([[5, 6], [7, 8]], np.uint16)),
        ("http://{host}/data/img.fits", np.array([[1, 2], [3, 4]], np.uint16)),
        ("http://{host}/data/img_multiple.fits", np.array([[5, 6], [7, 8]], np.uint16)),
        (
            "http://{host}/data/img_multiple2.FITS",
            np.array([[5, 6], [7, 8]], np.uint16),
        ),
        # Numpy binary files
        ("data/img.npy", np.array([[1, 2], [3, 4]], np.uint16)),
        (Path("data/img.npy"), np.array([[1, 2], [3, 4]], np.uint16)),
        ("http://{host}/data/img.npy", np.array([[1, 2], [3, 4]], np.uint16)),
        # Numpy text files
        ("data/img_tab.txt", np.array([[1, 2], [3, 4]], np.uint16)),
        ("data/img_space.txt", np.array([[1, 2], [3, 4]], np.uint16)),
        ("data/img_comma.txt", np.array([[1, 2], [3, 4]], np.uint16)),
        ("data/img_pipe.txt", np.array([[1, 2], [3, 4]], np.uint16)),
        ("data/img_semicolon.txt", np.array([[1, 2], [3, 4]], np.uint16)),
        (Path("data/img_tab.txt"), np.array([[1, 2], [3, 4]], np.uint16)),
        (Path("data/img_space.txt"), np.array([[1, 2], [3, 4]], np.uint16)),
        (Path("data/img_comma.txt"), np.array([[1, 2], [3, 4]], np.uint16)),
        (Path("data/img_pipe.txt"), np.array([[1, 2], [3, 4]], np.uint16)),
        (Path("data/img_semicolon.txt"), np.array([[1, 2], [3, 4]], np.uint16)),
        ("http://{host}/data/img_tab.txt", np.array([[1, 2], [3, 4]], np.uint16)),
        ("http://{host}/data/img_space.txt", np.array([[1, 2], [3, 4]], np.uint16)),
        ("http://{host}/data/img_comma.txt", np.array([[1, 2], [3, 4]], np.uint16)),
        ("http://{host}/data/img_pipe.txt", np.array([[1, 2], [3, 4]], np.uint16)),
        ("http://{host}/data/img_semicolon.txt", np.array([[1, 2], [3, 4]], np.uint16)),
        # JPG files
        ("data/img.jpg", np.array([[13, 19], [28, 34]])),
        ("data/img.jpeg", np.array([[13, 19], [28, 34]])),
        ("http://{host}/data/img.jpg", np.array([[13, 19], [28, 34]])),
        ("http://{host}/data/img.jpeg", np.array([[13, 19], [28, 34]])),
        # PNG files
        ("data/img.png", np.array([[10, 20], [30, 40]])),
        ("data/img2.PNG", np.array([[10, 20], [30, 40]])),
        ("http://{host}/data/img.png", np.array([[10, 20], [30, 40]])),
        ("http://{host}/data/img2.PNG", np.array([[10, 20], [30, 40]])),
        # TIFF files
        ("data/img.tif", np.array([[10, 20], [30, 40]])),
        ("data/img.tiff", np.array([[10, 20], [30, 40]])),
        ("http://{host}/data/img.tif", np.array([[10, 20], [30, 40]])),
        ("http://{host}/data/img.tiff", np.array([[10, 20], [30, 40]])),
        # BMP files
        ("data/img.bmp", np.array([[10, 20], [30, 40]])),
    ],
)
def test_load_image(
    with_caching: bool,
    valid_data2d_http_hostname: str,
    filename: Union[str, Path],
    exp_data: np.ndarray,
):
    """Test function 'load_image' with local and remote files."""
    with pyxel.set_options(cache_enabled=with_caching):
        if isinstance(filename, Path):
            # Load data
            data_2d = pyxel.load_image(filename)
        else:
            full_url: str = filename.format(host=valid_data2d_http_hostname)

            # Load data
            data_2d = pyxel.load_image(full_url)

        # Check 'data_2d
        np.testing.assert_equal(data_2d, exp_data)


@pytest.mark.parametrize(
    "filename, exp_error, exp_message",
    [
        ("dummy", ValueError, r"^Only (.*) implemented.$"),
        (
            Path("unknown.txt"),
            FileNotFoundError,
            r"^Input file (.*) can not be found\.$",
        ),
        ("unknown.txt", FileNotFoundError, None),
        ("invalid_data/table_X.txt", ValueError, "Cannot find the separator"),
        (
            "http://{host}/invalid_data/table_X.txt",
            ValueError,
            "Cannot find the separator",
        ),
        ("invalid_data/table_empty.txt", ValueError, "Cannot find the separator"),
        (
            "http://{host}/invalid_data/table_empty.txt",
            ValueError,
            "Cannot find the separator",
        ),
    ],
)
def test_load_table_invalid_filename(
    invalid_table_http_hostname: str,
    filename,
    exp_error: TypeError,
    exp_message: Optional[str],
):
    """Test function 'load_table' with invalid filenames."""
    if isinstance(filename, str):
        filename = filename.format(host=invalid_table_http_hostname)

    with pytest.raises(exp_error, match=exp_message):
        _ = pyxel.load_table(filename)


@pytest.mark.parametrize("with_caching", [False, True])
@pytest.mark.parametrize(
    "filename, with_header",
    [
        ("data/table_tab.txt", False),
        ("data/table_space.TXT", False),
        ("data/table_comma.data", False),
        ("data/table_pipe.txt", False),
        ("data/table_semicolon.txt", False),
        ("data/table.xlsx", False),
        ("data/table.npy", False),
        (Path("data/table_tab.txt"), False),
        (Path("data/table_space.TXT"), False),
        (Path("data/table_comma.data"), False),
        (Path("data/table_pipe.txt"), False),
        (Path("data/table_semicolon.txt"), False),
        (Path("data/table.xlsx"), False),
        (Path("data/table.npy"), False),
        ("http://{host}/data/table_tab.txt", False),
        ("http://{host}/data/table_space.TXT", False),
        ("http://{host}/data/table_comma.data", False),
        ("http://{host}/data/table_pipe.txt", False),
        ("http://{host}/data/table_semicolon.txt", False),
        ("http://{host}/data/table.xlsx", False),
        ("http://{host}/data/table.npy", False),
        ("data/table_tab_with_header.txt", True),
        ("data/table_space_with_header.TXT", True),
        ("data/table_comma_with_header.data", True),
        ("data/table_pipe_with_header.txt", True),
        ("data/table_semicolon_with_header.txt", True),
        ("data/table_with_header.xlsx", True),
        (Path("data/table_tab_with_header.txt"), True),
        (Path("data/table_space_with_header.TXT"), True),
        (Path("data/table_comma_with_header.data"), True),
        (Path("data/table_pipe_with_header.txt"), True),
        (Path("data/table_semicolon_with_header.txt"), True),
        (Path("data/table_with_header.xlsx"), True),
        ("http://{host}/data/table_tab_with_header.txt", True),
        ("http://{host}/data/table_space_with_header.TXT", True),
        ("http://{host}/data/table_comma_with_header.data", True),
        ("http://{host}/data/table_pipe_with_header.txt", True),
        ("http://{host}/data/table_semicolon_with_header.txt", True),
        ("http://{host}/data/table_with_header.xlsx", True),
    ],
)
def test_load_table(
    with_caching: bool, valid_table_http_hostname: str, filename, with_header: bool
):
    """Test function 'load_table'."""
    with pyxel.set_options(cache_enabled=with_caching):
        if isinstance(filename, Path):
            # Load data
            table = pyxel.load_table(filename, header=with_header)
        else:
            full_url: str = filename.format(host=valid_table_http_hostname)

            # Load data
            table = pyxel.load_table(full_url, header=with_header)

        if not with_header:
            exp_table = pd.DataFrame([[1, 2, 3], [4, 5, 6], [7, 8, 9]], dtype=float)
        else:
            exp_table = pd.DataFrame(
                [[1, 2, 3], [4, 5, 6], [7, 8, 9]],
                columns=["col1", "col2", "col3"],
                dtype=float,
            )
        pd.testing.assert_frame_equal(table, exp_table)


@pytest.mark.parametrize("filename", ["dummy.foo"])
def test_load_table_invalid_format(tmp_path: Path, filename: str):
    # Create an empty file
    full_filename: Path = tmp_path.joinpath(filename)
    full_filename.touch()

    with pytest.raises(ValueError):
        _ = pyxel.load_table(full_filename)
