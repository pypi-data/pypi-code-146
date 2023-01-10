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
from meshed import DAG
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
from functools import partial
from front.crude import crudify_based_on_names, prepare_for_crude_dispatch
from collections import defaultdict
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
)
from typing import List


def simple_chunker(wfs, chk_size: int = DFLT_CHK_SIZE):
    return list(chunker(wfs, chk_size=chk_size))


def simple_featurizer(chks):
    fvs = np.array(list(map(DFLT_FEATURIZER, chks)))
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
    data_store=None,
    learned_models=None,
    models_scores=None,
):
    from plunk.sb.front_demo.user_story1.utils.funcs import (
        upload_sound,
        # display_tag_sound,
        mk_step,
        mk_pipeline,
        learn_outlier_model,
        apply_fitted_model,
        # exec_pipeline,
        visualize_pipeline,
        visualize_scores,
    )

    if not b.mall():
        b.mall = mall
    mall = b.mall()
    if not b.selected_step_factory():
        b.selected_step_factory = 'chunker'  # TODO make this dynamic

    steps_store = steps_store or steps
    data_store = data_store or data
    pipelines_store = pipelines_store or pipelines

    general_crudifier = partial(
        crudify_based_on_names,
        param_to_mall_map={
            'step_factory': 'step_factories',
            'tagged_data': 'sound_output',
            'preprocess_pipeline': 'pipelines',
            'tagged_data': 'sound_output',
            'preprocess_pipeline': 'pipelines',
            'fitted_model': 'learned_models',
            'pipeline': 'pipelines_store',
            'scores': 'models_scores',
        },
        output_store={
            mk_step: 'steps_store',
            mk_pipeline: 'pipelines_store',
            learn_outlier_model: 'learned_models',
            apply_fitted_model: 'models_scores',
            upload_sound: 'sound_output',
        },
        crudifier=partial(prepare_for_crude_dispatch, mall=mall),
    )

    [
        upload_sound,
        # display_tag_sound,
        mk_step,
        mk_pipeline,
        learn_outlier_model,
        apply_fitted_model,
        # exec_pipeline,
        visualize_pipeline,
        visualize_scores,
    ] = map(
        general_crudifier,
        [
            upload_sound,
            # display_tag_sound,
            mk_step,
            mk_pipeline,
            learn_outlier_model,
            apply_fitted_model,
            # exec_pipeline,
            visualize_pipeline,
            visualize_scores,
        ],
    )

    def get_step_name(step):
        return [k for k, v in mall[steps].items() if v == step][0]

    def get_selected_step_factory_sig():
        selected_step_factory = mall['step_factories'].get(
            b.selected_step_factory.get()
        )
        if selected_step_factory:
            return Sig(selected_step_factory)

    config = {
        APP_KEY: {'title': 'Data Preparation'},
        RENDERING_KEY: {
            'upload_sound': {
                # NAME_KEY: "Data Loader",
                'execution': {
                    'inputs': {
                        'train_audio': {
                            ELEMENT_KEY: FileUploader,
                            'type': 'wav',
                            'accept_multiple_files': True,
                        },
                    },
                    'output': {
                        ELEMENT_KEY: SuccessNotification,
                        'message': 'Wav files loaded successfully.',
                    },
                },
            },
            'display_tag_sound': {
                'execution': {
                    # 'inputs': {
                    #     'result': {
                    #         ELEMENT_KEY: SelectBox,
                    #         'options': mall['sound_output'],
                    #     },
                    # },
                    'output': {ELEMENT_KEY: AudioArrayDisplay,},
                },
            },
            'mk_step': {
                NAME_KEY: 'Pipeline Step Maker',
                'execution': {
                    'inputs': {
                        'step_factory': {'value': b.selected_step_factory,},
                        'kwargs': {'func_sig': get_selected_step_factory_sig},
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
                        # 'tagged_data': {
                        #     ELEMENT_KEY: SelectBox,
                        #     'options': mall['sound_output'],
                        # },
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
            'visualize_scores': {
                NAME_KEY: 'Scores Visualization',
                'execution': {
                    # 'inputs': {
                    #     'scores': {
                    #         ELEMENT_KEY: SelectBox,
                    #         'options': mall['models_scores'],
                    #     },
                    # },
                    'output': {ELEMENT_KEY: ArrayWithIntervalsPlotter,},
                },
            },
            'simple_model': {
                NAME_KEY: 'Learn model',
                'execution': {
                    # 'inputs': {
                    #     'tagged_data': {
                    #         ELEMENT_KEY: SelectBox,
                    #         'options': mall['sound_output'],
                    #     },
                    #     'preprocess_pipeline': {
                    #         ELEMENT_KEY: SelectBox,
                    #         'options': mall['pipelines'],
                    #     },
                    # },
                    'output': {ELEMENT_KEY: ArrayPlotter,},
                },
            },
            'apply_fitted_model': {
                NAME_KEY: 'Apply model',
                'execution': {
                    # 'inputs': {
                    #     'tagged_data': {
                    #         ELEMENT_KEY: SelectBox,
                    #         'options': mall['sound_output'],
                    #     },
                    #     'preprocess_pipeline': {
                    #         ELEMENT_KEY: SelectBox,
                    #         'options': mall['pipelines'],
                    #     },
                    #     'learned_model': {
                    #         ELEMENT_KEY: SelectBox,
                    #         'options': mall['learned_models'],
                    #     },
                    # },
                    'output': {ELEMENT_KEY: ArrayPlotter,},
                },
            },
        },
    }

    funcs = [
        upload_sound,
        # display_tag_sound,
        mk_step,
        mk_pipeline,
        learn_outlier_model,
        apply_fitted_model,
        # exec_pipeline,
        visualize_pipeline,
        visualize_scores,
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
        steps_store=dict(),
        pipelines_store=dict(),
        pipelines=dict(),
        exec_outputs=dict(),
        learned_models=dict(),
        models_scores=dict(),
    )

    # crudifier = partial(prepare_for_crude_dispatch, mall=mall)

    step_factories = dict(
        # ML
        chunker=FuncFactory(simple_chunker),
        featurizer=FuncFactory(simple_featurizer),
    )

    mall['step_factories'] = step_factories

    app = mk_pipeline_maker_app_with_mall(
        mall, step_factories='step_factories', steps='steps', pipelines='pipelines'
    )

    app()
