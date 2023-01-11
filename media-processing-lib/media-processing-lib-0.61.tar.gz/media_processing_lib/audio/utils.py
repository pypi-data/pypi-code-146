"""Utils for audio"""
from typing import Tuple, Set
import tempfile
import subprocess

from .libs.soundfile import audio_write as audio_write_soundfile
from .libs.librosa import audio_read as audio_read_librosa
from ..logger import logger

def build_reader(audio_lib: str):
    """Build the reader function"""
    assert audio_lib in get_available_audio_libs().intersection(["librosa"])
    if audio_lib == "librosa":
        return audio_read_librosa
    return None

# pylint: disable=import-outside-toplevel, unused-import
def get_available_audio_libs() -> Set[str]:
    """Returns a set with all the available audio libraries used for reading/writing"""
    res = set()
    try:
        import librosa
        res.add("librosa")
    except ModuleNotFoundError:
        pass

    try:
        import soundfile
        res.add("soundfile")
    except ModuleNotFoundError:
        pass

    if len(res) == 0:
        logger.info("Warning! No image libraries available. Use 'pip install -r requirements.txt'")
    return res

def get_wav_from_video(path: str) -> Tuple[int, str]:
    """Given a video path, use ffmpeg under the hood to extract the audio, and return the audio fd and path."""
    fd, tmp_path = tempfile.mkstemp(suffix=".wav")
    logger.debug2(f"Extracting audio from '{path}'. Will be stored at '{tmp_path}'.")
    command = f"ffmpeg -loglevel panic -y -i {path} -strict -2 {tmp_path}"
    subprocess.call(command, shell=True)
    return fd, tmp_path

def build_writer(audio_lib: str):
    """Builds the writer function"""
    assert audio_lib in get_available_audio_libs().intersection(["soundfile"])
    if audio_lib == "soundfile":
        return audio_write_soundfile
    return None
