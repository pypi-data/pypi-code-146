"""Audio reader"""
import os
import mimetypes
import warnings

from .utils import get_wav_from_video, build_reader
from .mpl_audio import MPLAudio
from ..logger import logger, logging

# pylint: disable=broad-except
def audio_read(path: str, audio_lib: str = "librosa", force_wav: bool=True, **kwargs):
    """
    audio_read implementation from a path
    FUN FACT: Reading mp4 (videos in general?) will yield different results every time, so we can convert data to wav
        first if mp4
    """
    if logger.getEffectiveLevel() < logging.DEBUG:
        warnings.filterwarnings("ignore")
    f_read = build_reader(audio_lib)

    is_video = mimetypes.guess_type(path)[0].startswith("video")
    if force_wav and is_video:
        fd, tmp_path = get_wav_from_video(path)
        logger.debug(f"Converting {path} video to wav. Got path: {tmp_path}")
        path = tmp_path

    audio_data, sample_rate = f_read(path, **kwargs)
    audio = MPLAudio(audio_data, sample_rate)
    logger.debug(f"Read audio {path}. Shape: {audio.shape}. Sample rate: {audio.sample_rate:.2f}")
    if force_wav and is_video:
        os.remove(path)
        os.close(fd)
    return audio
