from io import BytesIO
from wave import Wave_write, Wave_read

import soundfile as sf
from recode import (
    encode_wav_header_bytes,
    encode_pcm_bytes,
    decode_wav_bytes,
    decode_wav_header_bytes,
    decode_pcm_bytes,
)


# sf.read(file, dtype='int16')


def sf_wf_to_wav(wf, *, sr=44100, subtype='PCM_16', n_channels=1):
    wav = BytesIO()
    with sf.SoundFile(
        wav,
        mode='wb',
        samplerate=sr,
        channels=n_channels,
        format='wav',
        subtype=subtype,
    ) as _file:
        _file.write(wf)

    return wav


def wf_to_wav(wf, *, sr=44100, width_bytes=2, n_channels=1):
    header = encode_wav_header_bytes(
        sr, width_bytes, n_channels=n_channels, nframes=len(wf)
    )
    print(f'{len(header)=}')
    pcm = encode_pcm_bytes(wf, width_bytes * 8, n_channels)
    print(f'{len(pcm)=}')
    return header + pcm


def wav_to_wf(wav):
    print(f'{wav=}')
    wf, sr = decode_wav_bytes(wav)
    return wf


def encode_wav_bytes(
    wf, sr: int = 44100, width_bytes: int = 2, *, n_channels: int = 1
) -> bytes:
    bio = BytesIO()
    with Wave_write(bio) as obj:
        obj.setparams((n_channels, width_bytes, sr, 0, 'NONE', 'not compressed'))
        wf_bytes = encode_pcm_bytes(wf, width=width_bytes * 8, n_channels=n_channels)
        obj.writeframes(wf_bytes)
        bio.seek(0)
    return bio.read()


if __name__ == '__main__':
    wf_data = list(range(10))
    wavfile = encode_wav_bytes(wf_data)
    print(f'{len(wavfile)=}')

    # sf_wavfile = sf_wf_to_wav(wf_data)
    # print(f'{sf_wavfile=}')

    print(decode_wav_header_bytes(wavfile))
    print(decode_wav_bytes(wavfile))

    waveform = wav_to_wf(wavfile)
    print(f'{len(waveform)=}')

    print(Wave_read(BytesIO(wavfile)).getparams())
    print(decode_pcm_bytes(Wave_read(BytesIO(wavfile)).readframes(100)))
