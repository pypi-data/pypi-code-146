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


param_to_mall_maps = dict(train_audio='train_audio', tag='tag_store')

if 'mall' not in st.session_state:
    st.session_state['mall'] = dict(
        # train_audio={},
        # tag={},
        # unused_store={"to": "illustrate"},
        tag_sound_output={}
    )

mall = st.session_state['mall']
# mall = dict(
#     # train_audio={},
#     # tag={},
#     # unused_store={"to": "illustrate"},
#     tag_sound_output={}
# )


WaveForm = Iterable[int]


@dataclass
class TaggedAudioPlayer(OutputBase):
    def render(self):
        sound, tag = self.output
        if not isinstance(sound, str):
            sound = sound.getvalue()

        st.audio(sound)


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


@dataclass
class DfVisualizer(OutputBase):
    def render(self):
        # m = self.output

        st.dataframe(mall['tag_sound_output'])


# crudify = Crudifier(mall=mall, output_store="tag_sound_output")
# f = crudify(display_df)


# May be partialize the mall argument?
# make a separate crudifier, with some defaults specified
# check "verbose"


@Crudifier(mall=mall, output_store='tag_sound_output')
def tag_sound(train_audio: WaveForm, tag: str):
    # mall["tag_store"] = tag
    return (train_audio, tag)


@Crudifier(mall=mall, param_to_mall_map={'result': 'tag_sound_output'})
def display_tag_sound(result):
    return result


@Crudifier(mall=mall, param_to_mall_map={'result': 'tag_sound_output'})
def visualize_tag_sound(result):
    return result


def mall_to_df(mall):
    names = list(mall['tag_sound_output'].keys())
    # pd.DataFrame


def explore_dataset(result):
    return mall['tag_sound_output']


def set_train_test_proportion(train_proportion):
    mall['train_test_proportion'] = train_proportion
    return train_proportion


config_ = {
    APP_KEY: {'title': 'Simple Real Audio ML'},
    # OBJ_KEY: {"trans": crudify},
    RENDERING_KEY: {
        'tag_sound': {
            # "description": {"content": "A very simple learn model example."},
            'execution': {
                'inputs': {
                    'train_audio': {
                        ELEMENT_KEY: MultiSourceInput,
                        'From a file': {ELEMENT_KEY: FileUploader, 'type': 'wav',},
                        'From the microphone': {ELEMENT_KEY: AudioRecorder},
                    },
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
