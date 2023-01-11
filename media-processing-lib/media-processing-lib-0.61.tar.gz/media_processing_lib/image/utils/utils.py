"""Utils module"""
from typing import Set
from ...logger import logger

# pylint: disable=import-outside-toplevel, unused-import
def get_available_image_libs() -> Set[str]:
    """Returns a set with all the available image libraries used for reading/writing"""

    res = set()
    try:
        import PIL
        res.add("PIL")
    except ModuleNotFoundError:
        pass

    try:
        import lycon
        res.add("lycon")
    except ModuleNotFoundError:
        pass

    try:
        import cv2
        res.add("opencv")
    except ModuleNotFoundError:
        pass

    try:
        import skimage
        res.add("skimage")
    except ModuleNotFoundError:
        pass

    if len(res) == 0:
        logger.info("Warning! No image libraries available. Use 'pip install -r requirements.txt'")
    return res
