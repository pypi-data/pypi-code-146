"""MPLVideo module"""
from __future__ import annotations
from functools import lru_cache
from typing import Tuple, Callable
from copy import copy, deepcopy
import numpy as np

from .mpl_video_apply import MPLVideoApply
from .reader import MPLVideoBackend
from .utils import build_video_write_fn
from ..image import image_resize
from ..logger import logger

MPLFrame = np.ndarray
FrameApplyFn = Callable[[np.ndarray, "MPLVideo", int], "MPLFrame"] # Applies on video[t] basically

class MPLVideo:
    """
    MPLVideo class
    Parameters
        data np.array, list or tuple of frames
        fps frames per scond
        shape The logical shape of the video. It can differ from the data shape, but for each access, we lazily resize
            the frames accordingly
        n_frames The logical number of frames of the video. It can differ from the length of the data.

    """
    def __init__(self, data: MPLVideoBackend, fps: int, frame_shape: Tuple[int] = None, n_frames: int = None):
        assert len(data) > 0, "No data was provided"
        n_frames = len(data) if n_frames is None else n_frames
        assert n_frames > 0, "No frames left"
        self._fps = fps
        self.n_frames = n_frames

        self.raw_data = data
        self._raw_len = len(data)
        self._raw_first_frame_shape = data[0].shape[0: 2]
        if frame_shape is None:
            frame_shape = self._raw_first_frame_shape
            logger.info(f"Frame shape not provided. Infering from first frame to {frame_shape}")
        assert len(frame_shape) == 2, f"Must be in [H x W] format. Found: {frame_shape}"
        self._frame_shape = tuple(frame_shape)

    @property
    def fps(self):
        """The frames per second of this video"""
        return self._fps

    @fps.setter
    def fps(self, fps: float):
        self._fps = fps

    @property
    def shape(self) -> Tuple[int]:
        """Returns the N x H w W x 3 shapes"""
        return (self.n_frames, *self.frame_shape, 3)

    @property
    def frame_shape(self):
        """The frame shape [H x W] of this video"""
        return self._frame_shape

    def write(self, path: str, video_lib: str = "imageio", **kwargs):
        """
        Saves the current video to the desired path.
        Parameters
            path where to save this current file
            video_lib What video library to use to write the video
        """
        f_write = build_video_write_fn(video_lib)
        f_write(self, path, **kwargs)

    def save(self, *args, **kwargs):
        """Same as self.write()"""
        self.write(*args, **kwargs)

    @lru_cache
    def __getitem__(self, key):
        # Get the raw data at key frame
        item = self.raw_data[key]
        # Resize the image to the desired shape
        item = image_resize(item, height=self.shape[1], width=self.shape[2])
        return item

    def __setitem__(self, key, value):
        assert False, "Cannot set values to a video object. Use video.data or video[i] to get the frame."

    def __len__(self):
        return self.n_frames

    def __eq__(self, other: MPLVideo) -> bool:
        """
        Relatively expensive check to see if two videos are equal. First, we look at shape/fps/n_frames. However,
        these may be equal, but the data may be different. So we look frame by frame in the end to validate.
        """
        check_n_frames = self.n_frames == other.n_frames
        check_shape = self.shape == other.shape
        check_fps = self.fps == other.fps
        if not (check_n_frames and check_shape and check_fps):
            return False

        # Next, we'll go frame by frame
        for i in range(len(self)):
            if not np.allclose(self[i], other[i]):
                return False
        return True

    def __deepcopy__(self, _):
        return MPLVideo(deepcopy(self.raw_data), self.fps, self.frame_shape, self.n_frames)

    def __copy__(self):
        return MPLVideo(copy(self.raw_data), self.fps, self.frame_shape, self.n_frames)

    def apply(self, apply_fn: Callable[[np.ndarray, MPLVideo, int], np.ndarray]) -> MPLVideoApply:
        """
        Applies a function to each frame of the self video and creates a new video with the applied function.
        The callable prototype is (video, timestep) and must return a modified frame of video[timestep]
        Return A new video where each frame is updates according to the provided callback
        """
        return MPLVideoApply(self, apply_fn)

    def __str__(self) -> str:
        f_str= "[MPL Video]" \
              f"\n-  Frame: {self.frame_shape}." \
              f"\n-  Duration: {len(self)}." \
              f"\n-  FPS: {self.fps:.2f}."
        return f_str

    def __hash__(self):
        return hash(f"{id(self.raw_data)}_{self.fps}_{self.n_frames}")

    def __repr__(self) -> str:
        return str(self)
