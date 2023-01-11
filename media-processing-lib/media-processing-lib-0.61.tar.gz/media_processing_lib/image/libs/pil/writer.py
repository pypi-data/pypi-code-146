"""PIL image writer"""
import numpy as np
from PIL import Image

def image_write(file: np.ndarray, path: str):
    """PIL image writer"""
    assert file.min() >= 0 and file.max() <= 255
    img = Image.fromarray(file.astype(np.uint8), "RGB")
    img.save(path)
