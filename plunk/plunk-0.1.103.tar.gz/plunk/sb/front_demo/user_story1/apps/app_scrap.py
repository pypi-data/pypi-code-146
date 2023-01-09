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
    PipelineMaker,
)
from streamlitfront.elements import (
    AudioRecorder,
    FileUploader,
    MultiSourceInput,
)
import streamlit as st

import soundfile as sf
from io import BytesIO
from plunk.sb.front_demo.user_story1.components.components import (
    AudioArrayDisplay,
    GraphOutput,
    ArrayPlotter,
    ArrayWithIntervalsPlotter,
)
from plunk.sb.front_demo.user_story1.utils.tools import (
    DFLT_FEATURIZER,
    DFLT_CHK_SIZE,
    chunker,
    WaveForm,
    Stroll,
    clean_dict,
    scores_to_intervals,
)


def foo(x: int):
    return x


def bar(x: int, msg: str):
    return x * msg


def mk_pipeline_maker_app_with_mall(
    mall: Mapping,
    *,
    step_factories: str = 'step_factories',
    steps: str = 'steps',
    steps_store=None,
    pipelines: str = 'pipelines',
    pipelines_store=None,
    data: str = 'data',
    data_store=None,
    learned_models=None,
    models_scores=None,
):
    if not b.mall():
        b.mall = mall
    mall = b.mall()
    if not b.selected_step_factory():
        b.selected_step_factory = 'chunker'  # TODO make this dynamic

    crudifier = partial(Crudifier, mall=mall)

    steps_store = steps_store or steps
    data_store = data_store or data
    pipelines_store = pipelines_store or pipelines

    @crudifier(
        param_to_mall_map=dict(step_factory=step_factories), output_store=steps_store
    )
    def mk_step(step_factory: Callable, kwargs: dict):
        kwargs = clean_dict(kwargs)  # TODO improve that logic
        step = partial(step_factory, **kwargs)()

        return step

    #
    @crudifier(output_store=pipelines_store,)
    def mk_pipeline(steps: Iterable[Callable]):
        return LineParametrized(*steps)

    @crudifier(
        param_to_mall_map=dict(pipeline=pipelines_store, tagged_data='sound_output'),
        output_store='exec_outputs',
    )
    def exec_pipeline(pipeline: Callable, tagged_data):
        sound, tag = tagged_data

        result = pipeline(sound)
        return result

    def get_step_name(step):
        return [k for k, v in mall[steps].items() if v == step][0]

    def get_selected_pipeline_sig():
        if not b.selected_pipeline():
            return Sig()
        return Sig(mall[pipelines][b.selected_pipeline()])

    config = {
        APP_KEY: {'title': 'Data Preparation'},
        RENDERING_KEY: {
            'mk_step': {
                NAME_KEY: 'Pipeline Step Maker',
                'execution': {
                    'inputs': {
                        'step_factory': {'value': b.selected_step_factory,},
                        'kwargs': {
                            'func_sig': Sig(
                                mall[step_factories][b.selected_step_factory()]
                            ),
                        },
                    },
                    'output': {
                        ELEMENT_KEY: SuccessNotification,
                        'message': 'The step has been created successfully.',
                    },
                },
            },
            'mk_pipeline': {
                NAME_KEY: 'Pipeline Maker',
                'execution': {
                    'inputs': {
                        steps: {
                            ELEMENT_KEY: PipelineMaker,
                            'items': list(mall[steps].values()),
                            'serializer': get_step_name,
                        },
                    },
                    'output': {
                        ELEMENT_KEY: SuccessNotification,
                        'message': 'The pipeline has been created successfully.',
                    },
                },
            },
            'exec_pipeline': {
                NAME_KEY: 'Pipeline Executor',
                'execution': {
                    'inputs': {
                        'pipeline': {'value': b.selected_pipeline,},
                        'data': {
                            ELEMENT_KEY: SelectBox,
                            'options': mall['sound_output'],
                        },
                    }
                },
            },
            'visualize_pipeline': {
                NAME_KEY: 'Pipeline Visualization',
                'execution': {
                    'inputs': {'pipeline': {'value': b.selected_pipeline,},},
                    'output': {
                        ELEMENT_KEY: GraphOutput,
                        NAME_KEY: 'Flow',
                        'use_container_width': True,
                    },
                },
            },
        },
    }

    funcs = [
        mk_step,
        mk_pipeline,
        exec_pipeline,
    ]
    app = mk_app(funcs, config=config)

    return app


if __name__ == '__main__':

    mall = dict(
        # Factory Input Stores
        sound_output=dict(),
        step_factories=dict(),
        # Output Store
        data=dict(),
        steps=dict(),
        pipelines=dict(),
        exec_outputs=dict(),
        learned_models=dict(),
        models_scores=dict(),
    )

    crudifier = partial(prepare_for_crude_dispatch, mall=mall)

    step_factories = dict(
        # ML
        chunker=FuncFactory(foo),
        featurizer=FuncFactory(bar),
    )

    mall['step_factories'] = step_factories

    app = mk_pipeline_maker_app_with_mall(
        mall, step_factories='step_factories', steps='steps', pipelines='pipelines'
    )

    app()
