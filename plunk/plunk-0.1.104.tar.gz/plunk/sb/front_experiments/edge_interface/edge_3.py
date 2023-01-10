import streamlit as st


from front.spec_maker_base import APP_KEY, RENDERING_KEY, ELEMENT_KEY, NAME_KEY
from streamlitfront.base import mk_app
from meshed import code_to_dag, DAG
from front.elements import FileUploaderBase
from streamlitfront.elements import implement_input_component
from typing import Iterable
from streamlitfront.examples.graph_component import Graph
from utils import wav_complex_display

WaveForm = Iterable[int]

WavUploader = implement_input_component(
    FileUploaderBase,
    component_factory=st.file_uploader,
    input_value_callback=lambda input, self: wav_complex_display(input),
)


@code_to_dag
def display_wf(wf: WaveForm):
    result = display_wf(wf)


config_ = {
    APP_KEY: {'title': 'Simple Load and Display'},
    RENDERING_KEY: {
        DAG: {
            'execution': {
                'inputs': {
                    'wf': {
                        # ELEMENT_KEY: FILE_UPLOADER_COMPONENT,
                        ELEMENT_KEY: WavUploader,
                        'type': 'wav',
                    },
                }
            },
            'graph': {ELEMENT_KEY: Graph, NAME_KEY: 'Flow',},
        }
    },
}

app = mk_app([display_wf], config=config_)
app()
