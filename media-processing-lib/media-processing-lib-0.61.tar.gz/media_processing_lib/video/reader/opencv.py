"""OpenCV video reader"""
from typing import Tuple, List, Union
from overrides import overrides
import cv2
import numpy as np

from .mpl_video_backend import MPLVideoBackend, MPLFrame
from ...logger import logger

ReadReturnType = Tuple[np.ndarray, int, List[int], int]

class MPLOpenCVBackend(MPLVideoBackend):
    """MPLOpenCVBackend backend implmenetation"""

    def __init__(self, path: str, n_frames: int = None):
        super().__init__(path)
        self._video = cv2.VideoCapture(str(path))
        self._raw_n_frames =  int(self._video.get(cv2.CAP_PROP_FRAME_COUNT))
        self.fps = self._video.get(cv2.CAP_PROP_FPS)
        self._raw_data = []

        self.n_frames = self._raw_n_frames if n_frames is None else n_frames
        assert self.n_frames <= self._raw_n_frames, \
            f"Requested {self.n_frames}. Raw number of frames from video: {self._raw_n_frames}"

        # Read all frames if none are provided. We need a better way to do this perhaps.
        logger.debug(f"OpenCV MPLBackend. Path: {path}. N frames: {self.n_frames}. Raw FPS: {self.fps}.")

    @staticmethod
    @overrides
    def supported_formats() -> List[str]:
        return [".mp4", ".avi", ".gif"]

    @overrides
    def __getitem__(self, key: Union[int, slice]) -> Union[MPLFrame, List[MPLFrame]]:
        assert isinstance(key, int), f"Got {type(key)}"
        assert key < self.n_frames, f"Out of bounds: frame {key} >= {self.n_frames}"
        if len(self._raw_data) > key:
            return self._raw_data[key]

        n_left = key - len(self._raw_data) + 1
        while n_left > 0:
            ret, new_frame = self._video.read()
            if not ret:
                logger.info(f"Got None (StopIteration of OpenCV) at frame {len(self._raw_data)}")
                self.n_frames = len(self._raw_data)
                break
            # BGR to RGB
            new_frame = new_frame[..., ::-1]
            new_frame = new_frame[..., 0: 3]
            self._raw_data.append(new_frame)
            n_left -= 1
        return self[key]

    @overrides
    def __len__(self) -> int:
        return self.n_frames
