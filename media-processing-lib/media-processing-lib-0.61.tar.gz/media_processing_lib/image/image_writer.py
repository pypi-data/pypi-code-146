"""Image writer module"""
from typing import Callable
import numpy as np

from .utils import get_available_image_libs
from ..logger import logger

from .libs.opencv import image_write as image_write_opencv
from .libs.pil import image_write as image_write_pil
from .libs.lycon import image_write as image_write_lycon
from .libs.skimage import image_write as image_write_skimage

def build_image_writer(img_lib: str) -> Callable:
    """build image writer function"""
    assert img_lib in get_available_image_libs(), f"Image library '{img_lib}' not in {get_available_image_libs()}"
    if img_lib == "opencv":
        return image_write_opencv
    if img_lib == "PIL":
        return image_write_pil
    if img_lib == "lycon":
        return image_write_lycon
    if img_lib == "skimage":
        return image_write_skimage
    return None

def image_write(file: np.ndarray, path: str, img_lib: str = "opencv", count: int = 5) -> None:
    """Write an image to a path"""
    path = str(path) if not isinstance(path, str) else path
    f_write = build_image_writer(img_lib)

    i = 0
    while True:
        try:
            return f_write(file, path)
        except Exception as e:
            logger.debug(f"Path: {path}. Exception: {e}")
            i += 1

            if i == count:
                raise Exception
