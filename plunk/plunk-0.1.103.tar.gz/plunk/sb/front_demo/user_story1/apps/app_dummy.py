import streamlit as st
from typing import List, Iterable
import soundfile as sf
from io import BytesIO
import numpy as np

Waveform = Iterable[int]


def tagged_sounds_to_single_array(train_audio: List[Waveform], tag: str):
    sounds, tag = train_audio, tag
    result = []
    for sound in sounds:
        # if not isinstance(sound, bytes):
        sound = sound.getvalue()
        arr = sf.read(BytesIO(sound), dtype='int16')[0]
        result.append(arr)
    print(np.hstack(result))
    return np.hstack(result), tag


st.title('Dummy app')
files = st.file_uploader(label='one', accept_multiple_files=True)
arr, tag = tagged_sounds_to_single_array(files, tag='Normal')
st.write(type(arr), arr.shape, arr[0])
