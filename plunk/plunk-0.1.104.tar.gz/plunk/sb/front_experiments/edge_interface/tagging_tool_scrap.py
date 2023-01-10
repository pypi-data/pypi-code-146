from dataclasses import dataclass
from typing import Iterable
from meshed import code_to_dag, DAG
from front import APP_KEY, RENDERING_KEY, ELEMENT_KEY, NAME_KEY, OBJ_KEY
from collections.abc import Callable
from front.crude import prepare_for_crude_dispatch
from streamlitfront.elements import TextInput, SelectBox, FloatSliderInput
from front.elements import OutputBase
from streamlitfront.base import mk_app
from streamlitfront.examples.util import Graph
import base64
from streamlitfront.elements import (
    AudioRecorder,
    FileUploader,
    MultiSourceInput,
)
import streamlit as st
import matplotlib.pyplot as plt
import soundfile as sf
from io import BytesIO
from front.elements import InputBase
from streamlitfront.elements.js import mk_element_factory
import numpy as np
import os
import streamlit.components.v1 as components


# st_audiorec = mk_element_factory("st_audiorec")

parent_dir = os.path.dirname(os.path.abspath(__file__))
# Custom REACT-based component for recording client audio in browser
build_dir = os.path.join(parent_dir, 'st_audiorec/frontend/build')
# specify directory and initialize st_audiorec object functionality
st_audiorec = components.declare_component('st_audiorec', path=build_dir)
# base64data_audio = st_audiorec()

# # APPROACH: DECODE BASE64 DATA FROM return value
# st.write(base64data_audio)
# if (
#     (base64data_audio != None)
#     and (base64data_audio != "")
#     and ("test" not in base64data_audio)
# ):
#     # decoding process of base64 string to wav file
#     with st.spinner("Decoding audio data..."):
#         base64data_audio = base64data_audio.replace("data:audio/wav;base64,", "")
#         st.write(base64data_audio)  # remove metadata header of base64 string

#         audiofile_name = "temp.wav"
#         wav_file = open(audiofile_name, "wb")
#         decode_string = base64.b64decode(base64data_audio + "==")
#         wav_file.write(decode_string)

#     audiofile_path = os.path.join(os.getcwd(), audiofile_name)
#     st.write(audiofile_path)
#     st.audio(audiofile_path)

val = st_audiorec()
# web component returns arraybuffer from WAV-blob
st.write('Audio data received in the Python backend will appear below this message ...')
st.write(val['arr'])
# if not isinstance(val, dict):  # retrieve audio data

# # wav_bytes contains audio data in format to be further processed
# # display audio data as received on the Python side
# st.audio(wav_bytes, format="audio/wav")
# st.write(val)
