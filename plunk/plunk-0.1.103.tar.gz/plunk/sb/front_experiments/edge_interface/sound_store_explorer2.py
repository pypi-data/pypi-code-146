import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import soundfile as sf
from graze import graze
from dol import FilesOfZip, wrap_kvs, filt_iter
from io import BytesIO
from st_aggrid import GridOptionsBuilder, AgGrid, DataReturnMode, GridUpdateMode
from front.elements import OutputBase, InputBase
from streamlitfront.elements import TextInput, IntInput
from front import APP_KEY, RENDERING_KEY, ELEMENT_KEY, NAME_KEY, OBJ_KEY
from dataclasses import dataclass
from streamlitfront.base import mk_app


# @dataclass
class AggTable(InputBase):
    def __init__(self, df):
        self.df = df

    def render(self):
        st.dataframe(self.df)


class SimpleInput(IntInput):
    def render(self):
        st.write(f'What has been entered={self.output}')


# The App
st.title('Wav Store explorer')


def simple_display(result):
    return result


config_ = {
    APP_KEY: {'title': 'Simple Real Audio ML'},
    # OBJ_KEY: {"trans": crudify},
    RENDERING_KEY: {
        'simple_display': {
            'execution': {
                'inputs': {
                    'result': {
                        ELEMENT_KEY: IntInput,
                        # "options": mall["tag_sound_output"],
                    },
                },
                # "output": {
                #    ELEMENT_KEY: TaggedAudioPlayer,
                # },
            },
        },
    },
}

app = mk_app([simple_display], config=config_)
app()
