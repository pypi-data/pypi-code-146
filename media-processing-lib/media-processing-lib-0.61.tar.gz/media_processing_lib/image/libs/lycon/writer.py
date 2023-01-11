"""Image writer for lycon"""
import numpy as np
import lycon

def image_write(file: np.ndarray, path: str):
    """image writer function for lycon"""
    assert file.min() >= 0 and file.max() <= 255
    lycon.save(path, file.astype(np.uint8))
