import numpy as np
from PIL import Image


class ModelNotImplementedError(Exception):
    pass


def open_img(image: object) -> Image:
    """open_img. Open a path, bytes or numpy image

    :param image:
    :type image: object
    :rtype: Image
    """
    if isinstance(image, str) or isinstance(image, bytes):
        to_predict = Image.open(image)
    elif isinstance(image, np.ndarray):
        to_predict = Image.fromarray(np.uint8(image))
    else:
        raise ValueError(str(type(image)) + " not implemented")
    to_predict = to_predict.convert("RGB")

    return to_predict
