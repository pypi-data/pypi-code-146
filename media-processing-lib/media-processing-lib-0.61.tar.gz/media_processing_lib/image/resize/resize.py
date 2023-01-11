"""Resize module for images"""
from typing import Callable
import numpy as np
from ...logger import logger
from ..utils import get_available_image_libs
from ..libs.skimage import image_resize as image_resize_skimage
from ..libs.pil import image_resize as image_resize_pil
from ..libs.lycon import image_resize as image_resize_lycon
from ..libs.opencv import image_resize as image_resize_opencv
from .resize_stretch import image_resize_stretch
from .resize_black_bars import image_resize_black_bars

def build_resize_fn(resize_lib) -> Callable:
    """Builds the resize fn"""
    assert resize_lib in get_available_image_libs(), \
        f"Image library '{resize_lib}' not in {get_available_image_libs()}"
    if resize_lib == "skimage":
        return image_resize_skimage
    if resize_lib == "lycon":
        return image_resize_lycon
    if resize_lib == "PIL":
        return image_resize_pil
    if resize_lib == "opencv":
        return image_resize_opencv
    return None

def build_resize_mode_fn(mode):
    """builds the resize mode fn"""
    assert mode in ("stretch", "black_bars")
    if mode == "stretch":
        return image_resize_stretch
    if mode == "black_bars":
        return image_resize_black_bars
    return None

def image_resize(data: np.ndarray, height: int, width: int, interpolation: str = "bilinear",
                 mode: str = "stretch", resize_lib: str = "opencv", only_uint8: bool = True, **kwargs) -> np.ndarray:
    """
    Image resize function
    Generic function to resize ONE 2D image of shape (H, W) or 3D of shape (H, W, D) into (height, width [, D])
    Parameters:
        data Image (or any 2D/3D array)
        height Desired resulting height
        width Desired resulting width
        interpolation Interpolation method. Valid choices are specific to the library used for the resizing.
        mode Whether to stretch the image or apply black bars around it to preserve scaling.
        resize_lib The library used for resizing
        only_uint8 If true, only [0-255] images are allowed. Otherwise, let the resize_lib work the provided dtype.
    Returns: Resized image.
    """
    assert len(data.shape) in (2, 3)
    if data.shape[0] == height and data.shape[1] == width:
        logger.debug2("Width and height are already to the desired shape. Returning early.")
        return data.copy()
    if only_uint8 is True:
        assert data.dtype == np.uint8, f"Data dtype: {data.dtype}. Use only_uint8=False."

    f_resize_mode = build_resize_mode_fn(mode)
    f_resize = build_resize_fn(resize_lib)
    resized_data = f_resize_mode(data, height, width, interpolation, f_resize, **kwargs)
    return resized_data

def image_resize_batch(data: np.ndarray, height: int, width: int, interpolation: str = "bilinear",
                       mode: str = "stretch", resize_lib: str="opencv",
                       only_uint8: bool = True, **kwargs) -> np.ndarray:
    """
    Batch version of image_reisze
    Generic function to resize a batch of images of shape BxHxW(xD) to a desired shape of BxdWxdH(xD)
    Paramaeters
        data batch of images (or any 2D/3D array)
        height Desired resulting height
        width Desired resulting width
        interpolation Interpolation method. Valid choices are specific to the library used for the resizing.
        mode Whether to stretch the image or apply black bars around it to preserve scaling.
        resize_lib The library used for resizing
        only_uint8 If true, only [0-255] images are allowed. Otherwise, let the resize_lib work the provided dtype.
    Returns: Resized batch of image.
    """
    N = len(data)
    assert N > 0

    # Let the img_resize infer the height/width if not provided (i.e. autosclaing for img_resize)
    first_result = image_resize(data[0], height=height, width=width, interpolation=interpolation,
                                mode=mode, resize_lib=resize_lib, only_uint8=only_uint8, **kwargs)
    new_data = np.zeros((N, *first_result.shape), dtype=data[0].dtype)
    new_data[0] = first_result
    for i in range(1, N):
        result = image_resize(data[i], height=height, width=width, interpolation=interpolation,
                              mode=mode, resize_lib=resize_lib, only_uint8=only_uint8, **kwargs)
        new_data[i] = result
    return new_data
