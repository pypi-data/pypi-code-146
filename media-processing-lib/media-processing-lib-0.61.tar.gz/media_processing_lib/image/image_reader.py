"""Image reader module"""
from typing import Callable
from pathlib import Path
import numpy as np

from ..logger import logger
from .utils import get_available_image_libs
from .libs.opencv import image_read as image_read_opencv
from .libs.pil import image_read as image_read_pil
from .libs.lycon import image_read as image_read_lycon
from .libs.skimage import image_read as image_read_skimage


def build_image_reader(img_lib: str) -> Callable:
    """Build the image reader function"""
    assert img_lib in get_available_image_libs(), f"Image library '{img_lib}' not in {get_available_image_libs()}"
    if img_lib == "opencv":
        return image_read_opencv
    if img_lib == "PIL":
        return image_read_pil
    if img_lib == "lycon":
        return image_read_lycon
    if img_lib == "skimage":
        return image_read_skimage
    return None


def image_read(path: str, img_lib: str = "opencv", count: int = 5) -> np.ndarray:
    """Read an image from a path given a library"""
    f_read = build_image_reader(img_lib)
    path = str(path) if isinstance(path, Path) else path

    i = 0
    while True:
        try:
            return f_read(path)
        except Exception as e:
            logger.debug(f"Path: {path}. Exception: {e}")
            i += 1

            if i == count:
                raise Exception(e)
