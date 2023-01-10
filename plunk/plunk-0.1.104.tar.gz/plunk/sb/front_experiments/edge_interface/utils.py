import io
import numpy as np
import soundfile as sf
import streamlit as st
import pyaudio


def discretize(arr, num_windows=200, func=np.mean):
    step = len(arr) // num_windows
    dis = [func(arr[i * step : i * (step + 1)]) for i in range(num_windows)]
    return np.array(dis)


def wav_complex_display(uploaded_file):
    bytes = bytes_from_uploaded(uploaded_file)
    st.audio(bytes)
    arr = arr_from_bytes(bytes)
    arr_d = discretize(arr)
    st.write(f'length = {len(arr)}')
    st.bar_chart(arr_d)


def arr_from_bytes(bytes, dtype='int16'):
    arr = sf.read(bytes, dtype=dtype)[0]

    return arr


def bytes_from_uploaded(uploaded_file):
    uploaded_file.seek(0)
    result = io.BytesIO(uploaded_file.read())

    return result


def mk_audio_stream():
    p = pyaudio.PyAudio()
    stream = p.open(
        format=pyaudio.paInt16,
        channels=1,
        rate=44100,
        input=True,
        output=True,
        frames_per_buffer=1024,
        output_device_index=3,
    )
    return stream
