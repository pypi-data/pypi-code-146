import numpy as np


def int16_to_float(x: np.ndarray) -> np.ndarray:
    """ Convert int16 array to floating point with range +/- 1
    """
    return np.float32(x) / 32768


def float_to_int16(x: np.ndarray) -> np.ndarray:
    """ Convert float point array with range +/- 1 to int16
    """
    return np.int16(x * 32768)
