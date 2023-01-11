"""Generic utils for this module"""
from typing import Callable, List
import numpy as np

# fdef try_fn(fn: Callable, n_tries: int, *args, **kwargs):
#     """Try to call some specific function n times before bailing."""
#     if n_tries is None:
#         n_tries = 5

#     for i in range(n_tries):
#         try:
#             return fn(*args, **kwargs)
#         except Exception as e: #pylint: disable=broad-except
#             logger.debug(f"Failed {i + 1}/{n_tries}. Function: {fn}. Error: {e}")
#             continue
#     assert False

def map_apply_fn(apply_fns: List[Callable], frame: np.ndarray, video: "MPLVideo", key: int) -> np.ndarray:
    """Applies a list of fns to the video"""
    y = frame
    for fn in apply_fns:
        y = fn(y, video, key)
    return y
