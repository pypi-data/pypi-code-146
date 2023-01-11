"""Librosa reader"""
from typing import Union, Tuple
from pathlib import Path
import librosa
import numpy as np

def audio_read(path: Union[str, Path], **kwargs) -> Tuple[np.ndarray, int]:
    """Uses librosa to read audio"""
    if "sampleRate" in kwargs:
        kwargs["sr"] = kwargs["sampleRate"]
        del kwargs["sampleRate"]

    return librosa.load(path, **kwargs)
