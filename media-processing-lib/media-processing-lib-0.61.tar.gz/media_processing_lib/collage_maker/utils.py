"""Utils for collage maker"""
from typing import Callable, Tuple, List
from pathlib import Path
import numpy as np

from ..image import image_read, image_add_title

def auto_load_fn(file_path: Path) -> Callable[[Path], np.ndarray]:
    """Tries to autoload a file"""
    suffix = file_path.suffix[1:]
    if suffix in ("png", "jpg"):
        return image_read
    if suffix == "npy":
        return np.load
    if suffix == "npz":
        def f(x):
            X = np.load(x, allow_pickle=True)["arr_0"]
            try:
                _ = X.shape
            except Exception as _:
                X = X.item()
            return X
        return f
    assert False, f"Suffix unknown: '{suffix}'. Path: '{file_path}'"

def get_closest_square(N: int) -> Tuple[int, int]:
    """
    Objective:

    Given a stack of N images
    Find the closest square X>=N*N and then remove rows 1 by 1 until it still fits X

    Example: 9: 3*3; 12 -> 3*3 -> 3*4 (3 rows). 65 -> 8*8 -> 8*9. 73 -> 8*8 -> 8*9 -> 9*9
    """

    x = int(np.sqrt(N))
    r, c = x, x
    # There are only 2 rows possible between x^2 and (x+1)^2 because (x+1)^2 = x^2 + 2*x + 1, thus we can add 2 columns
    #  at most. If a 3rd column is needed, then closest lower bound is (x+1)^2 and we must use that.
    if c * r < N:
        c += 1
    if c * r < N:
        r += 1
    assert (c + 1) * r > N and c * (r + 1) > N
    return r, c

def collage_fn(images: List[np.ndarray], rows_cols: Tuple[int, int] = None,
               titles: List[str] = None, **kwargs) -> np.ndarray:
    """
    Make a concatenated collage based on the desired r,c format
    Parameters
    images A stack of images
    rows_cols Tuple for number of rows and columns
    titles Titles for each image. Optional.
    kwargs are used for image_add_title method

    Return: A numpy array of stacked images according to (rows, cols) inputs.
    """
    shapes = [x.shape for x in images]
    rows_cols = get_closest_square(len(images)) if rows_cols is None else rows_cols
    assert rows_cols[0] * rows_cols[1] >= len(images), \
        f"Rows ({rows_cols[0]}) * Cols ({rows_cols[1]}) < Images ({len(images)})"

    if titles is not None:
        images = [image_add_title(image, title, **kwargs) for (image, title) in zip(images, titles)]
        shapes = [x.shape for x in images]
    assert np.std(shapes, axis=0).sum() == 0, f"Shapes not equal: {shapes}"

    # Put all the results in a new array
    result = np.zeros((rows_cols[0] * rows_cols[1], *shapes[0]), dtype=np.uint8)
    result[0 : len(images)] = np.array(images)
    result = result.reshape((rows_cols[0], rows_cols[1], *shapes[0]))
    result = np.concatenate(np.concatenate(result, axis=1), axis=1)
    return result
