from pyaaware import ForwardTransform
from pyaaware import InverseTransform

from sonusai.mixture.types import AudioF
from sonusai.mixture.types import AudioT
from sonusai.mixture.types import ImpulseResponseData
from sonusai.mixture.types import Location


def get_next_noise(audio: AudioT, offset: int, length: int) -> AudioT:
    """Get next sequence of noise data from noise audio file

    :param audio: Overall noise audio (entire file's worth of data)
    :param offset: Starting sample
    :param length: Number of samples to get
    :return: Sequence of noise audio data
    """
    import numpy as np

    return np.take(audio, range(offset, offset + length), mode='wrap')


def read_ir(name: Location) -> ImpulseResponseData:
    """Read impulse response data from a file

    :param name: File name
    :return: ImpulseResponseData object
    """
    import numpy as np
    from scipy.io import wavfile

    from sonusai import SonusAIError
    from sonusai.mixture import ImpulseResponseData
    from sonusai.mixture import apply_ir
    from sonusai.mixture import tokenized_expandvars

    expanded_name, _ = tokenized_expandvars(name)

    try:
        # Read in and normalize to -20 dBFS to avoid clipping when applying IR
        sample_rate, data = wavfile.read(expanded_name)
        max_data = max(abs(data)) * 10
        data = list(np.array(data / max_data, dtype=np.float32))

        # Find offset to align convolved audio with original
        ir = ImpulseResponseData(sample_rate=sample_rate, offset=0, filter=data)
        x = np.zeros((len(ir.filter),), dtype=np.float32)
        x[0] = 1
        y = list(apply_ir(x, ir))

        return ImpulseResponseData(sample_rate=sample_rate, offset=y.index(max(y)), filter=data)
    except Exception as e:
        if name != expanded_name:
            raise SonusAIError(f'Error reading {name} (expanded: {expanded_name}): {e}')
        else:
            raise SonusAIError(f'Error reading {name}: {e}')


def read_audio(name: Location) -> AudioT:
    """Read audio data from a file

    :param name: File name
    :return: Array of time domain audio data
    """
    import numpy as np
    import sox

    from sonusai import SonusAIError
    from sonusai.mixture import BIT_DEPTH
    from sonusai.mixture import CHANNEL_COUNT
    from sonusai.mixture import ENCODING
    from sonusai.mixture import SAMPLE_RATE
    from sonusai.mixture import tokenized_expandvars

    expanded_name, _ = tokenized_expandvars(name)

    if BIT_DEPTH == 8:
        encoding_out = np.int8
    elif BIT_DEPTH == 16:
        encoding_out = np.int16
    elif BIT_DEPTH == 24:
        encoding_out = np.int32
    elif BIT_DEPTH == 32:
        if ENCODING == 'floating-point':
            encoding_out = np.float32
        else:
            encoding_out = np.int32
    elif BIT_DEPTH == 64:
        encoding_out = np.float64
    else:
        raise SonusAIError(f'Invalid BIT_DEPTH {BIT_DEPTH}')

    try:
        # Read in and convert to desired format
        # NOTE: pysox format transformations do not handle encoding properly; need to use direct call to sox instead
        args = ['-D',
                '-V2',
                '-c', '1',
                expanded_name,
                '-t', 'raw',
                '-r', str(SAMPLE_RATE),
                '-b', str(BIT_DEPTH),
                '-c', str(CHANNEL_COUNT),
                '-e', ENCODING,
                '-']
        status, out, err = sox.core.sox(args, None, False)
        if status != 0:
            raise SonusAIError(f'sox stdout: {out}\nsox stderr: {err}')

        return np.frombuffer(out, dtype=encoding_out)

    except Exception as e:
        if name != expanded_name:
            raise SonusAIError(f'Error reading {name} (expanded: {expanded_name}):\n{e}')
        else:
            raise SonusAIError(f'Error reading {name}:\n{e}')


def calculate_transform_from_audio(audio: AudioT, transform: ForwardTransform) -> AudioF:
    """Apply forward transform to input audio data to generate transform data

    :param audio: Time domain data [samples]
    :param transform: ForwardTransform object
    :return: Frequency domain data [frames, bins]
    """
    return transform.execute_all(audio).transpose()


def calculate_audio_from_transform(data: AudioF, transform: InverseTransform, trim: bool = True) -> AudioT:
    """Apply inverse transform to input transform data to generate audio data

    :param data: Frequency domain data [frames, bins]
    :param transform: InverseTransform object
    :param trim: Removes starting samples so output waveform will be time-aligned with input waveform to the transform
    :return: Time domain data [samples]
    """
    audio = transform.execute_all(data.transpose())
    if trim:
        audio = audio[transform.N - transform.R:]

    return audio
