"""
An app that loads either a wav file from local folder or records a sound
and visualizes the resulting numpy array 
"""
from typing import Mapping
from know.boxes import *
from functools import partial
from typing import Callable, Iterable
from front import APP_KEY, RENDERING_KEY, ELEMENT_KEY, NAME_KEY
from i2 import Pipe, Sig
from front.crude import Crudifier, prepare_for_crude_dispatch
from lined import LineParametrized
import numpy as np

from streamlitfront import mk_app, binder as b
from streamlitfront.elements import (
    SelectBox,
    SuccessNotification,
    KwargsInput,
    PipelineMaker,
)
from streamlitfront.elements import (
    AudioRecorder,
    FileUploader,
    MultiSourceInput,
)
import streamlit as st
from plunk.sb.front_experiments.streamlitfront_dataprep.data_prep2 import (
    # DFLT_WF_PATH,
    # DFLT_ANNOT_PATH,
    data_from_wav_folder,
)
import soundfile as sf
from io import BytesIO
import matplotlib.pyplot as plt
from plunk.sb.front_demo.user_story1.components.components import (
    AudioArrayDisplay,
    GraphOutput,
    ArrayPlotter,
)
from plunk.sb.front_demo.user_story1.utils.tools import (
    DFLT_CHUNKER,
    DFLT_FEATURIZER,
    DFLT_CHK_SIZE,
    chunker,
    featurizer,
    WaveForm,
    Stroll,
)

# DFLT_FEATURIZER = lambda chk: np.abs(np.fft.rfft(chk))


@Sig(chunker)
def simple_chunker(wfs):
    return list(chunker(wfs))


def simple_featurizer(chks):
    fvs = np.array(list(map(np.std, chks)))
    return fvs


def simple_waveform_func(wfs):
    chks = list(chunker(wfs, chk_size=DFLT_CHK_SIZE))
    fvs = simple_featurizer(chks)

    return fvs


def mk_pipeline_maker_app_with_mall(
    mall: Mapping,
    *,
    step_factories: str = 'step_factories',
    steps: str = 'steps',
    steps_store=None,
    pipelines: str = 'pipelines',
    pipelines_store=None,
    data: str = 'data',
    data_output=None,
    data_store=None,
):
    # TODO: Like to not have this binder logic involving streamlit state here! Contain it!
    if not b.mall():
        # TODO: Maybe it's here that we need to use know.malls.mk_mall?
        b.mall = mall
    mall = b.mall()
    if not b.selected_step_factory():
        b.selected_step_factory = 'chunker'  # TODO make this dynamic

    crudifier = partial(Crudifier, mall=mall)

    steps_store = steps_store or steps
    data_store = data_store or data
    pipelines_store = pipelines_store or pipelines

    @crudifier(
        # TODO: Does this work if pipelines_store is a mapping instead of a string?
        param_to_mall_map=dict(
            tagged_data='sound_output', waveform_func='waveform_funcs'
        ),
        # output_store='exec_outputs'
    )
    def simple_model(tagged_data, waveform_func):
        sound, tag = tagged_data

        wfs = sound
        chks = list(chunker(wfs, chk_size=DFLT_CHK_SIZE))
        fvs = simple_featurizer(chks)

        return fvs

    @crudifier(output_store='sound_output')
    def upload_sound(train_audio: WaveForm, tag: str):
        # mall["tag_store"] = tag
        sound, tag = train_audio, tag
        if not isinstance(sound, bytes):
            sound = sound.getvalue()

        arr = sf.read(BytesIO(sound), dtype='int16')[0]
        return arr, tag

    @crudifier(param_to_mall_map={'result': 'sound_output'})
    def display_tag_sound(result):
        return result

    config = {
        APP_KEY: {'title': 'Base Audio'},
        RENDERING_KEY: {
            'upload_sound': {
                # NAME_KEY: "Data Loader",
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
                    'output': {
                        ELEMENT_KEY: SuccessNotification,
                        'message': 'Wav loaded successfully.',
                    },
                },
            },
            'display_tag_sound': {
                'execution': {
                    'inputs': {
                        'result': {
                            ELEMENT_KEY: SelectBox,
                            'options': mall['sound_output'],
                        },
                    },
                    'output': {ELEMENT_KEY: AudioArrayDisplay,},
                },
            },
            'simple_model': {
                NAME_KEY: 'Visualize outputs',
                'execution': {
                    'inputs': {
                        'tagged_data': {
                            ELEMENT_KEY: SelectBox,
                            'options': mall['sound_output'],
                        },
                    },
                    'output': {ELEMENT_KEY: ArrayPlotter,},
                },
            },
        },
    }

    funcs = [
        upload_sound,
        display_tag_sound,
        simple_model,
    ]
    app = mk_app(funcs, config=config)

    return app


if __name__ == '__main__':

    mall = dict(
        # Factory Input Stores
        sound_output=dict(),
        step_factories=dict(),
        # Funcs store
        waveform_funcs=dict(),
        # Output Store
        data=dict(),
        steps=dict(),
        pipelines=dict(),
        exec_outputs=dict(),
        learned_models=dict(),
    )

    crudifier = partial(prepare_for_crude_dispatch, mall=mall)

    step_factories = dict(
        # Source Readers
        # data_loader_factory=FuncFactory(data_from_wav_folder),
        # data_loader=data_from_wav_folder,
        # Chunkers
        chunker=FuncFactory(simple_chunker),
        featurizer=FuncFactory(simple_featurizer),
    )
    mall['waveform_funcs'] = dict(waveform_func=simple_waveform_func)

    mall['step_factories'] = step_factories

    app = mk_pipeline_maker_app_with_mall(
        mall, step_factories='step_factories', steps='steps', pipelines='pipelines'
    )

    app()
