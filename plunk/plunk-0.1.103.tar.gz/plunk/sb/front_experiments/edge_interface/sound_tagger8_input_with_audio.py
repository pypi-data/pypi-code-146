from dataclasses import dataclass
from typing import Iterable
from meshed import code_to_dag, DAG
from front import APP_KEY, RENDERING_KEY, ELEMENT_KEY, NAME_KEY, OBJ_KEY
from collections.abc import Callable
from front.crude import prepare_for_crude_dispatch
from streamlitfront.elements import TextInput, SelectBox, FloatSliderInput
from front.elements import OutputBase, FileUploaderBase
from streamlitfront.base import mk_app
from streamlitfront.examples.util import Graph
from streamlitfront.elements import (
    AudioRecorder,
    FileUploader,
    MultiSourceInput,
)
import streamlit as st
import matplotlib.pyplot as plt
import soundfile as sf
from io import BytesIO
from front.crude import Crudifier
from streamlitfront import binder as b


param_to_mall_maps = dict(train_audio='train_audio', tag='tag_store')

# if "mall" not in st.session_state:
#     st.session_state["mall"] = dict(
#         # train_audio={},
#         # tag={},
#         # unused_store={"to": "illustrate"},
#         tag_sound_output={}
#     )

# mall = st.session_state["mall"]

if not b.mall():
    b.mall = dict(tag_sound_output={})

mall = b.mall()

# mall = dict(
#     # train_audio={},
#     # tag={},
#     # unused_store={"to": "illustrate"},
#     tag_sound_output={}
# )


WaveForm = Iterable[int]


@dataclass
class InputAudioPlayer(FileUploaderBase):
    def render(self):
        print('done')


@dataclass
class AudioDisplay(OutputBase):
    def render(self):
        sound, tag = self.output
        if not isinstance(sound, str):
            sound = sound.getvalue()

        arr = sf.read(BytesIO(sound), dtype='int16')[0]
        tab1, tab2 = st.tabs(['Audio Player', 'Waveform'])
        with tab1:
            st.audio(sound)
        with tab2:
            fig, ax = plt.subplots(figsize=(15, 5))
            ax.plot(arr, label=f'Tag={tag}')
            ax.legend()
            st.pyplot(fig)
            # st.write(arr[:10])


@Crudifier(mall=mall, output_store='tag_sound_output')
def tag_sound(train_audio: WaveForm, tag: str):
    # mall["tag_store"] = tag
    return (train_audio, tag)


@Crudifier(mall=mall, param_to_mall_map={'result': 'tag_sound_output'})
def display_tag_sound(result):
    return result


config_ = {
    APP_KEY: {'title': 'Simple Real Audio ML'},
    # OBJ_KEY: {"trans": crudify},
    RENDERING_KEY: {
        'tag_sound': {
            # "description": {"content": "A very simple learn model example."},
            'execution': {
                'inputs': {
                    'train_audio': {ELEMENT_KEY: InputAudioPlayer, 'type': 'wav',},
                    # "tag": {
                    #     ELEMENT_KEY: TextInput,
                    # },
                },
            }
        },
        'display_tag_sound': {
            'execution': {
                'inputs': {
                    'result': {
                        ELEMENT_KEY: SelectBox,
                        'options': mall['tag_sound_output'],
                    },
                },
                'output': {ELEMENT_KEY: AudioDisplay,},
            },
        },
        Callable: {
            'execution': {
                'inputs': {
                    'save_name': {ELEMENT_KEY: TextInput, NAME_KEY: 'Save output as',},
                }
            },
        },
    },
}

app = mk_app([tag_sound, display_tag_sound], config=config_,)
app()
# st.audio(mall["tag_sound_output"]["s3"][0])
#'execution': {'inputs': {'p': {ELEMENT_KEY: FloatSliderInput,}},}
st.write(mall)
