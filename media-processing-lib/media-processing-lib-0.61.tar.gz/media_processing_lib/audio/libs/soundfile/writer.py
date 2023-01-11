"""Soundfile writer"""
import soundfile
from ....logger import logger

def audio_write(audio: "MPLAudio", path: str, **kwargs):
    """Uses soundfile to write audio"""
    logger.debug(f"Writing {audio} to '{path}'.")
    soundfile.write(file=path, data=audio.data, samplerate=int(audio.sample_rate), **kwargs)
