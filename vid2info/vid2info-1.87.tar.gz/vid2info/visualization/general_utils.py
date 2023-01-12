"""
General utils that are help to visualize the results of the inference. Mostly by formatting data.

Author: Eric Canas.
Github: https://github.com/Eric-Canas
Email: eric@ericcanas.com
Date: 17-07-2022
"""
import numpy as np


def apply_pad_on_shortest_axis(original_hw: tuple[int | float, int | float] | list[ int | float, int | float] | np.ndarray,
                               corner_xy: tuple[float, float] | list[float | float] | np.ndarray,
                               pad: float) -> tuple[float, float]:
    """
    Clips the corner (in the range (0., 1.)) in order to be in the range (pad, 1.-pad) in the shortest original axis
    and to have the same total length once rescaled to the original_hw on the largest axis.

    Args:
        original_hw: tuple of two ints or floats. The original size of the image.
        corner_xy: tuple of two floats. The corner to clip. In the range (0., 1.).
        pad: float. The padding to apply. In the range (0., 0.5).

    Returns:
        tuple of two floats. The clipped corner in the format (x, y).
    """
    h, w = original_hw
    w_corner, h_corner = corner_xy
    # If shortest axis is h, then we need to clip adapt w
    if w > h:
        h_corner = np.clip(h_corner, pad, 1. - pad)
        w_pad = pad * h / w
        w_corner = np.clip(w_corner, w_pad, 1. - w_pad)
    # If shortest axis is w, then we need to clip adapt h
    else:
        w_corner = np.clip(w_corner, pad, 1. - pad)
        h_pad = pad * w / h
        h_corner = np.clip(h_corner, h_pad, 1. - h_pad)
    return (float(w_corner), float(h_corner))