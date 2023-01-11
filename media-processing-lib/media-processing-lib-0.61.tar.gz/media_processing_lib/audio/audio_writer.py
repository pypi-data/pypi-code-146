"""Audio writer"""
from typing import List, Union
from pathlib import Path
import numpy as np

# from .utils import build_writer
from .mpl_audio import MPLAudio

# pylint: disable=import-outside-toplevel, broad-except, cyclic-import
def audio_write(audio: Union["MPLAudio", np.ndarray, List], path: Union[str, Path],
                audio_lib: str = "soundfile", **kwargs):
    """Audio writer implementation from a MPLAudio/numpy array or data"""
    if isinstance(audio, (np.ndarray, List)):
        assert "sample_rate" in kwargs
        sample_rate = kwargs.pop("sample_rate")
        audio = MPLAudio(audio, sample_rate)
    audio.write(path, audio_lib, **kwargs)
