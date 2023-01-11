"""Lycon image resizer"""

import numpy as np
from lycon import resize, Interpolation

def image_resize(data: np.ndarray, height: int, width: int, interpolation: str, **kwargs) -> np.ndarray:
    """
    Lycon based image resizing function
    Parameters
    data image we're resizing
    height desired resulting height
    width desired resulting width
    interpolation Interpolation method. Valid options: bilinear, nearest, cubic, lanczos, area
    Returns: Resized image
    """
    assert interpolation in ("bilinear", "nearest", "bicubic", "lancsoz", "area")
    assert isinstance(height, int) and isinstance(width, int)

    # As per: https://github.com/ethereon/lycon/blob/046e9fab906b3d3d29bbbd3676b232bd0bc82787/perf/benchmark.py#L57
    interpolation_types = {
        "bilinear" : Interpolation.LINEAR,
        "nearest" : Interpolation.NEAREST,
        "bicubic" : Interpolation.CUBIC,
        "lanczos" : Interpolation.LANCZOS,
        "area" : Interpolation.AREA
    }

    interpolation_type = interpolation_types[interpolation]
    img_resized = resize(data, height=height, width=width, interpolation=interpolation_type, **kwargs)
    return img_resized.astype(data.dtype)
