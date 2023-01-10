from typing import Iterable
from meshed import DAG
from front import APP_KEY, RENDERING_KEY, ELEMENT_KEY, NAME_KEY
from collections.abc import Callable
from front.crude import prepare_for_crude_dispatch
from streamlitfront.elements import TextInput, SelectBox

from streamlitfront.base import mk_app
from streamlitfront.examples.util import Graph
from streamlitfront.elements import (
    AudioRecorder,
    FileUploader,
    MultiSourceInput,
)
import streamlit as st

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


def crudify(funcs):
    for func in funcs:
        yield prepare_for_crude_dispatch(
            func, param_to_mall_map=param_to_mall_map, mall=mall
        )


WaveForm = Iterable[int]


# @code_to_dag
@prepare_for_crude_dispatch(mall=mall, output_store='tag_sound_output')
def tag_sound(train_audio: WaveForm, tag: str):
    # mall["tag_store"] = tag
    return (train_audio, tag)


@prepare_for_crude_dispatch(mall=mall, param_to_mall_map={'result': 'tag_sound_output'})
def display_tag_sound(result):
    return result


# crudified_tag_sound = prepare_for_crude_dispatch(
#     tag_sound, mall=mall, output_store="tag_sound_output"
# )
# crudified_display_tag_sound = prepare_for_crude_dispatch(
#     display_tag_sound, mall=mall, param_to_mall_map={"result": "tag_sound_output"}
# )

print(type(tag_sound))
from i2 import Sig

print(Sig(display_tag_sound))

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
                }
            },
        },
        DAG: {'graph': {ELEMENT_KEY: Graph, NAME_KEY: 'Flow',},},
        Callable: {
            'execution': {
                'inputs': {
                    'save_name': {ELEMENT_KEY: TextInput, NAME_KEY: 'Save output as',},
                }
            },
        },
    },
}

app = mk_app([tag_sound, display_tag_sound], config=config_)
app()
st.write(mall)
