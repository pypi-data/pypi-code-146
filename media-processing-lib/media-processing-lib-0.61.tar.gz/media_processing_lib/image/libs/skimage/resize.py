"""Skimage image resizer"""
import numpy as np
from skimage.transform import resize

def image_resize(data: np.ndarray, height: int, width: int, interpolation: str, **kwargs) -> np.ndarray:
    """Skimage image resizer"""
    assert interpolation in ("nearest", "bilinear", "bicubic", "biquadratic", "biquartic", "biquintic")
    assert isinstance(height, int) and isinstance(width, int)

    # As per: https://scikit-image.org/docs/stable/api/skimage.transform.html#skimage.transform.warp
    order = {
        "nearest" : 0,
        "bilinear" : 1,
        "biquadratic" : 2,
        "bicubic" : 3,
        "biquartic" : 4,
        "biquintic" : 5
    }[interpolation]
    img_resized = resize(data, output_shape=(height, width), order=order, preserve_range=True, **kwargs)
    img_resized = img_resized.astype(data.dtype)
    return img_resized
