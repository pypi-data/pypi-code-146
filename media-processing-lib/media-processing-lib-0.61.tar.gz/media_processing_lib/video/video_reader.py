"""Video reader module"""
from pathlib import Path

from .utils import build_video_read_fn
from .mpl_video import MPLVideo
from ..logger import logger

def video_read(path: str, fps: int = None, video_lib: str = "imageio", frame_shape = None,
               n_frames = None, **kwargs) -> MPLVideo:
    """Reads a video from a path using a video library"""
    path = Path(path).resolve()
    f_read = build_video_read_fn(video_lib)

    data = f_read(path, **kwargs)
    if fps is None:
        assert hasattr(data, "fps"), f"FPS not provided and video library {video_lib} has no fps attribute"
        fps = data.fps
    video = MPLVideo(data, fps=fps, frame_shape=frame_shape, n_frames=n_frames)
    logger.debug(f"Read video: {video}. \n Path: '{path}'. Video library: '{video_lib}'")
    return video
