"""Resize stretch mode"""
from typing import Callable
import numpy as np
from ...logger import logger

def image_resize_stretch(data: np.ndarray, height: int, width: int, interpolation: str, resize_fn: Callable, **kwargs):
    """
    Resize stretch mode
    Parameters:
        data Image (or any 2D/3D array)
        height Desired resulting height
        width Desired resulting width
        interpolation Interpolation method. Valid choices are specific to the library used for the resizing.
        resize_fn The library specific resize function
    Return: The resized image
    """
    current_height, current_width = data.shape[0], data.shape[1]
    # If we provide width only, height is infered to keep image scale
    assert (height is None) + (width is None) < 2, "Both width and height cannot be infered. Provide at least one."
    if height is None:
        assert not width is None
        height = current_height / current_width * width
        if height != int(height):
            logger.debug(f"Converting infered height from {height:.2f} to {int(height)}")
        height = int(height)

    if width is None:
        assert not height is None
        width = current_width / current_height * height
        if width != int(width):
            logger.debug(f"Converting infered width from {width:.2f} to {int(width)}")
        width = int(width)

    return resize_fn(data, height, width, interpolation, **kwargs)
