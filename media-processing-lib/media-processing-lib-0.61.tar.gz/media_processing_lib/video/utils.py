"""Generic utility file for videos"""
from typing import Set, Callable
from ..logger import logger
from .reader import MPLImageIOBackend, MPLImagesPathBackend, MPLDecordBackend, MPLPimsBackend, \
    MPLOpenCVBackend, MPLNumpyPathBackend
from .libs.imageio import video_write as video_write_imageio
from .libs.opencv import video_write as video_write_opencv

# pylint: disable=import-outside-toplevel, unused-import
def get_available_video_read_libs() -> Set[str]:
    """Returns a set with all the available video libraries used for reading"""
    # TODO: perhaps use importlib and make this better
    res = set()
    try:
        import decord
        res.add("decord")
    except ModuleNotFoundError:
        pass

    try:
        import pims
        res.add("pims")
    except ModuleNotFoundError:
        pass

    try:
        import cv2
        res.add("opencv")
    except ModuleNotFoundError:
        pass

    try:
        import imageio
        res.add("imageio")
    except ModuleNotFoundError:
        pass

    res.add("images_path")
    res.add("numpy_path")

    if len(res) == 0:
        logger.info("Warning! No video libraries available. Use 'pip install -r requirements.txt'")
    return res

# pylint: disable=import-outside-toplevel, unused-import
def get_available_video_write_libs() -> Set[str]:
    """Returns a set with all the available video libraries used for writing"""
    # TODO: perhaps use importlib and make this better
    res = set()
    try:
        import cv2
        res.add("opencv")
    except ModuleNotFoundError:
        pass

    try:
        import imageio
        res.add("imageio")
    except ModuleNotFoundError:
        pass

    if len(res) == 0:
        logger.info("Warning! No video libraries available. Use 'pip install -r requirements.txt'")
    return res

def build_video_read_fn(video_lib: str) -> Callable:
    """Builds the video read function"""
    assert video_lib in get_available_video_read_libs()
    if video_lib == "pims":
        return MPLPimsBackend
    if video_lib == "imageio":
        return MPLImageIOBackend
    if video_lib == "images_path":
        return MPLImagesPathBackend
    if video_lib == "numpy_path":
        return MPLNumpyPathBackend
    if video_lib == "opencv":
        return MPLOpenCVBackend
    if video_lib == "decord":
        return MPLDecordBackend
    assert False, "Unknown video lib: '{video_lib}'"

def build_video_write_fn(video_lib: str) -> Callable:
    """Builds the video write fn"""
    assert video_lib in get_available_video_write_libs(), \
        f"Video library '{video_lib}' not in '{get_available_video_write_libs()}'"
    if video_lib == "imageio":
        return video_write_imageio
    if video_lib == "opencv":
        return video_write_opencv
    assert False, f"Unknown video lib: '{video_lib}'"

def default_frame_apply_fn(frame, _, __) -> "MPLFrame":
    """Identity function for MPLVideoApply"""
    return frame
