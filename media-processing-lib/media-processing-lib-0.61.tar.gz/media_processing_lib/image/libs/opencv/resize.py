"""OpenCV image resizer"""

import numpy as np
import cv2

def image_resize(data: np.ndarray, height: int, width: int, interpolation: str, **kwargs) -> np.ndarray:
    """
    OpenCV based image resizing function
    Parameters
    data image we're resizing
    height desired resulting height
    width desired resulting width
    interpolation Interpolation method. Valid options: nearest, bilinear, area, bicubic, lanczos
    Returns: Resized image
    """
    assert isinstance(height, int) and isinstance(width, int)

    # As per: https://docs.opencv.org/2.4/modules/imgproc/doc/geometric_transformations.html#resize
    interpolation = {
        "nearest" : cv2.INTER_NEAREST,
        "bilinear" : cv2.INTER_LINEAR,
        "area" : cv2.INTER_AREA,
        "bicubic" : cv2.INTER_CUBIC,
        "lanczos" : cv2.INTER_LANCZOS4
    }[interpolation]
    img_resized = cv2.resize(data, dsize=(width, height), interpolation=interpolation, **kwargs).astype(data.dtype)
    return img_resized
