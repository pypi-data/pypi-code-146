"""Decord video reader"""
from typing import Tuple, List, Union
from overrides import overrides
import numpy as np
from decord import VideoReader, cpu, gpu

from .mpl_video_backend import MPLVideoBackend, MPLFrame
from ...logger import logger

ReadReturnType = Tuple[np.ndarray, int, List[int], int]

class MPLDecordBackend(MPLVideoBackend):
    """MPLDecordBackend implementation"""
    def __init__(self, path: str, n_frames: int = None, device: str = "cpu"):
        super().__init__(path)
        assert device in ("cpu", "gpu"), f"Got {device}"
        self.device = device
        self._video = VideoReader(str(self.path), ctx={"cpu": cpu(), "gpu": gpu()}[device])
        self._raw_n_frames = len(self._video)
        self.fps = self._video.get_avg_fps()

        self.n_frames = self._raw_n_frames if n_frames is None else n_frames
        assert self.n_frames <= self._raw_n_frames, \
            f"Requested {self.n_frames}. Raw number of frames from video: {self._raw_n_frames}"

        # Read all frames if none are provided. We need a better way to do this perhaps.
        logger.debug(f"Decord MPLBackend. Path: {path}. N frames: {self.n_frames}. Raw FPS: {self.fps}. "
                     f"Device: {self.device}")

    @staticmethod
    @overrides
    def supported_formats() -> List[str]:
        return [".mp4", ".avi", ".gif"]

    @overrides
    def __getitem__(self, key: Union[int, slice]) -> Union[MPLFrame, List[MPLFrame]]:
        assert isinstance(key, int), f"Got {type(key)}"
        res = self._video[key].asnumpy()
        return res

    @overrides
    def __len__(self) -> int:
        return self.n_frames
