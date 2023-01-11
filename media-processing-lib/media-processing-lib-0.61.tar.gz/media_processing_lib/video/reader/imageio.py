"""ImageIO video reader"""
from typing import Tuple, List, Union
import math
from overrides import overrides
import numpy as np
from imageio import get_reader

from .mpl_video_backend import MPLVideoBackend, MPLFrame
from ...logger import logger

ReadReturnType = Tuple[np.ndarray, int, List[int], int]

class MPLImageIOBackend(MPLVideoBackend):
    """MPLImageIOBackend implementation"""

    def __init__(self, path: str, n_frames: int = None):
        super().__init__(path)
        self.reader = get_reader(path)
        self.metadata = self.reader.get_meta_data()
        self.fps = self.metadata["fps"]
        # Accumulate all frames in this buffer
        self._raw_data = []
        self._raw_n_frames = math.floor(self.metadata["duration"] * self.metadata["fps"]) - 1 # TODO: more checks
        self._iter_reader = iter(self.reader)
        self.n_frames = self._raw_n_frames if n_frames is None else n_frames
        assert self.n_frames <= self._raw_n_frames, \
            f"Requested {self.n_frames}. Raw number of frames from metadata: {self._raw_n_frames}"

        # Read all frames if none are provided. We need a better way to do this perhaps.
        logger.debug(f"ImageIO MPLBackend. Path: {path}. N frames: {self.n_frames}. FPS: {self.fps}")

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
            try:
                new_frame = next(self._iter_reader)[..., 0 : 3]
            except StopIteration:
                logger.info(f"Got StopIteration at frame {len(self._raw_data)}")
                self.n_frames = len(self._raw_data)
                break
            self._raw_data.append(new_frame)
            n_left -= 1
        return self[key]

    @overrides
    def __len__(self) -> int:
        return self.n_frames
