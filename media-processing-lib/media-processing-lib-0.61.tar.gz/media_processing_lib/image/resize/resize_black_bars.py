"""Resize black bars mode"""
from typing import Callable
import numpy as np

def image_resize_black_bars(data: np.ndarray, height: int, width: int, interpolation: str,
                            resize_fn: Callable, return_coordinates: bool=False, **kwargs) -> np.ndarray:
    """
    Resize black bars mode
    Parameters:
        data Image (or any 2D/3D array)
        height Desired resulting height
        width Desired resulting width
        interpolation Interpolation method. Valid choices are specific to the library used for the resizing.
        resize_fn The library specific resize function
        return_coordinates If true, will return the coordinates where the black bars start
    Return: The resized image and, optionally, the black bars coordinates

    """
    desired_shape = (height, width) if len(data.shape) == 2 else (height, width, data.shape[-1])

    img_h, img_w = data.shape[0 : 2]
    desired_h, desired_w = desired_shape[0 : 2]

    # Find the rapports between the img_h/desired_h and img_w/desired_w
    r_h, r_w = img_h / desired_h, img_w / desired_w

    # Find which one is the highest, that one will be used
    max_rapp = max(r_h, r_w)
    assert max_rapp != 0, f"Cannot convert data of shape {data.shape} to ({height}, {width})"

    # Compute the new dimensions, based on the highest rapport
    scaled_h, scaled_w = int(img_h / max_rapp), int(img_w / max_rapp)
    assert scaled_h != 0 and scaled_w != 0, f"Cannot convert data of shape {data.shape} to ({height}, {width})"

    resized_data = resize_fn(data, scaled_h, scaled_w, interpolation, **kwargs)
    # Also, find the half, so we can insert the other dimension from the half. Insert the resized image in the original
    # image, halving the larger dimension and keeping half black bars in each side
    new_data = np.zeros(desired_shape, dtype=data.dtype)
    half_h, half_w = int((desired_h - scaled_h) / 2), int((desired_w - scaled_w) / 2)
    new_data[half_h : half_h + scaled_h, half_w : half_w + scaled_w] = resized_data

    if return_coordinates:
        x0, y0, x1, y1 = half_w, half_h, half_w + scaled_w, half_h + scaled_h
        return new_data, (x0, y0, x1, y1)
    return new_data
