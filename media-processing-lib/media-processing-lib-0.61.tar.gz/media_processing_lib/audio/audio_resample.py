""""Audio resample"""
import numpy as np

# pylint: disable=import-outside-toplevel, cyclic-import
def audio_resample(audio: "MPLAudio", sample_rate) -> "MPLAudio":
    """Audio resample"""
    from .mpl_audio import MPLAudio

    new_len = int(len(audio.data) / audio.sample_rate * sample_rate)
    x = np.arange(0, new_len)
    xp = np.arange(0, len(audio.data))
    new_data = np.interp(x, xp, audio.data)
    new_audio = MPLAudio(new_data, sample_rate)
    return new_audio
