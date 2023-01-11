"""to image module"""
import numpy as np

def to_image(x: np.ndarray) -> np.ndarray:
    """
    To image
    Generic NumPy to plottable image uint8 [0 : 255] image. Basically, turns the image in [0:1] and float32,
    applies minMax, does some stuff about potential shapes being wrong, converts image to [0:255] and to uint8.
    Parameters:
        x A NumPy array that is to be converted to [0 : 255] image
    Returns: A numpy array that is the image version of the original array

    """
    x = np.array(x)
    x = x.astype(np.float32)
    img_min, img_max = x.min(), x.max()
    x = (x - img_min) / (img_max - img_min + np.spacing(1))
    x = x.squeeze()
    if len(x.shape) == 2:
        x = np.expand_dims(x, axis=-1)
    assert len(x.shape) == 3, f"Got: {x.shape}."
    if x.shape[0] in (1, 3):
        x = x.transpose(1, 2, 0)
    if x.shape[-1] == 1:
        x = np.concatenate([x, x, x], axis=-1)
    if x.shape[-1] == 4:
        x = x[..., 0 : 3]
    x = np.clip(x, 0, 1) * 255
    x = x.astype(np.uint8)
    return x
