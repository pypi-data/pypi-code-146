"""Video writer module"""
from typing import Union, List
import numpy as np
from .mpl_video import MPLVideo
from .reader import MPLRawDataBackend
from ..logger import logger

def video_write(video: Union[MPLVideo, np.ndarray, List], path: str, video_lib: str = "imageio", **kwargs):
    """Write a video to the disk given a video writing library"""
    path = str(path) if not isinstance(path, str) else path
    if isinstance(video, (np.ndarray, list)):
        logger.debug("Raw data provided, converting it first to MPLVideo")
        assert "fps" in kwargs
        fps = kwargs.pop("fps")
        video = MPLVideo(MPLRawDataBackend(video), fps=fps)
    video.write(path, video_lib, **kwargs)
