"""MPLAudio module"""
from __future__ import annotations
from abc import ABC
from typing import Any
from copy import copy
import numpy as np

from .audio_resample import audio_resample
from .utils import build_writer

class MPLAudio(ABC):
    """MPLAudio implementation"""
    def __init__(self, data:Any, sample_rate: int):
        self.data = data
        self.sample_rate = sample_rate
        self.shape = self.data.shape

    def resample(self, sample_rate: int) -> MPLAudio:
        """
        Resamples this audio object to a new sample rate
        Returns copy of this audio with the new sample rate
        """
        # Lazily use NumPy for this task
        return audio_resample(self, sample_rate)

    def save(self, *args, **kwargs):
        """
        Saves the current audio to the desired path. Calls audio_write with it's desired params, such as audio_lib
        Parameters: path A path where to save this current file
        """
        self.write(*args, **kwargs)

    def write(self, path: str, audio_lib: str = "soundfile", **kwargs):
        """
        Saves the current audio to the desired path. Calls audio_write with it's desired params, such as audio_lib
        Parameters: path A path where to save this current file
        """

        path = str(path) if not isinstance(path, str) else path
        f_write = build_writer(audio_lib)
        f_write(self, path, **kwargs)

    def __len__(self):
        return len(self.data)

    def __setitem__(self, key, value):
        assert False, "Cannot set values to an audio object. Use audio.data or audio[i] to get the value."

    def __getitem__(self, key: slice | int):
        if isinstance(key, slice):
            assert key.step is None
            data = self.data[key]
            return MPLAudio(data, self.sample_rate)
        return self.data[key]

    def __copy__(self) -> MPLAudio:
        return MPLAudio(copy(self.data), self.sample_rate)

    def __str__(self):
        f_str = "[MPLAudio]"
        f_str += f"\n - Shape: {self.shape}"
        f_str += f"\n-  Sample rate: {self.sample_rate}"
        return f_str

    def __eq__(self, other: MPLAudio):
        # Close enough equality
        return (self.sample_rate == other.sample_rate) and (self.shape == other.shape) \
            and np.median(np.abs(self.data - other.data)) < 1e-4

    # # @brief Applies a function to each frame of the self video and creates a new video with the applied function.
    # #  The callable prototype is (video, timestep) and must return a modified frame of video[timestep]
    # # @return A new video where each frame is updates according to the provided callback
    # def apply(self, applyFn:Callable[[MPLVideo, int], np.ndarray]) -> MPLVideo:
    # 	N = len(self)
    # 	firstFrame = applyFn(self, 0)
    # 	newData = np.zeros((self.nFrames, *firstFrame.shape), dtype=np.uint8)
    # 	newData[0] = firstFrame
    # 	for i in Debug.range(1, N, desc="[MPLVideo::aply]"):
    # 		newFrame = applyFn(self, i)
    # 		newData[i] = newFrame
    # 	return MPLVideo(newData, self.fps, self.shape, self.nFrames)
    # def saveApply(self, path:str, applyFn:Callable[[MPLVideo, int], np.ndarray], **kwargs):
    # 	from .video_writer import tryWriteVideoApply
    # 	tryWriteVideoApply(self, path, applyFn, **kwargs)

# def save_wav(wav, path, sr):
# 	wav *= 32767 / max(0.01, np.max(np.abs(wav)))
# 	#proposed by @dsmiller
# 	wavfile.write(path, sr, wav.astype(np.int16))
