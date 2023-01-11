"""PIL image resizer"""
import numpy as np
from PIL import Image

def image_resize(data: np.ndarray, height: int, width: int, interpolation: str, **kwargs) -> np.ndarray:
    """PIL image resizer"""
    assert data.dtype == np.uint8
    assert isinstance(height, int) and isinstance(width, int)
    img_data = Image.fromarray(data)

    # As per: https://pillow.readthedocs.io/en/3.1.x/reference/Image.html#PIL.Image.Image.resize
    resample = {
        "nearest" : Image.NEAREST,
        "bilinear" : Image.BILINEAR,
        "bicubic" : Image.BICUBIC,
        "lanczos" : Image.LANCZOS
    }[interpolation]

    img_resized = img_data.resize(size=(width, height), resample=resample, **kwargs)
    np_img_resized = np.array(img_resized, dtype=data.dtype)
    return np_img_resized
