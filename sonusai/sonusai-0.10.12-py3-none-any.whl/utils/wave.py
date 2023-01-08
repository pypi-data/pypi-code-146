from sonusai.mixture import SAMPLE_RATE
from sonusai.mixture.types import AudioT


def write_wav(name: str, audio: AudioT, sample_rate: int = SAMPLE_RATE) -> None:
    """ Write a simple, uncompressed WAV file.

    To write multiple channels, use a 2D array of shape [samples, channels].
    The bits per sample and PCM/float are determined by the data type.

    """
    from scipy.io.wavfile import write

    write(name, sample_rate, audio)
