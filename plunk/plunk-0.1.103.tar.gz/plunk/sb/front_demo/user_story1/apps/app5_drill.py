"""
An app that loads either a wav file from local folder or records a sound
and visualizes the resulting numpy array 
This app implements the strategy outlined by Thor:
'For example, one rule could go through all functions and remove any params that:
are defaulted
and have defaults that are not handled by py-to-gui_element casting rules (c.f. routing)'
"""
from typing import Mapping
from know.boxes import *
from functools import partial
from typing import Callable, Iterable
from front import APP_KEY, RENDERING_KEY, ELEMENT_KEY, NAME_KEY
from i2 import Sig
from front.crude import Crudifier
from lined import LineParametrized
import numpy as np

from streamlitfront import mk_app, binder as b
from streamlitfront.elements import (
    SelectBox,
    SuccessNotification,
    PipelineMaker,
)
from streamlitfront.elements import FileUploader

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
    scores_to_intervals,
)
from typing import List
from i2 import Sig, FuncFactory, rm_params


def simple_chunker(wfs, chk_size: int = DFLT_CHK_SIZE):
    return list(chunker(wfs, chk_size=chk_size))


def simple_featurizer(chks):
    fvs = np.array(list(map(DFLT_FEATURIZER, chks)))
    return fvs


mk_chunker = rm_params(
    FuncFactory(simple_chunker),
    params_to_remove=['wfs'],
    allow_removal_of_non_defaulted_params=True,
)

mk_featurizer = rm_params(
    FuncFactory(simple_featurizer),
    params_to_remove=['chks'],
    allow_removal_of_non_defaulted_params=True,
)


def tagged_sound_to_array(train_audio: WaveForm, tag: str):
    sound, tag = train_audio, tag
    if not isinstance(sound, bytes):
        sound = sound.getvalue()

    arr = sf.read(BytesIO(sound), dtype='int16')[0]
    return arr, tag


def tagged_sounds_to_single_array(train_audio: List[WaveForm], tag: str):
    sounds, tag = train_audio, tag
    result = []
    for sound in sounds:
        sound = sound.getvalue()
        arr = sf.read(BytesIO(sound), dtype='int16')[0]
        result.append(arr)
    return np.hstack(result).reshape(-1, 1), tag


def assert_dims(wfs):
    if wfs.ndim >= 2:
        wfs = wfs[:, 0]
    return wfs


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
        step = partial(step_factory, **kwargs)()

        return step

    #
    @crudifier(output_store=pipelines_store,)
    def mk_pipeline(steps: Iterable[Callable]):
        result = LineParametrized(*steps)
        print(f'{Sig(result)=}')
        return result

    @crudifier(
        param_to_mall_map=dict(
            tagged_data='sound_output', preprocess_pipeline='pipelines'
        ),
        output_store='learned_models',
    )
    def learn_outlier_model(tagged_data, preprocess_pipeline, n_centroids=5):
        sound, tag = tagged_sounds_to_single_array(*tagged_data)
        wfs = np.array(sound)

        wfs = assert_dims(wfs)

        fvs = preprocess_pipeline(wfs)
        model = Stroll(n_centroids=n_centroids)
        model.fit(X=fvs)

        return model

    @crudifier(
        param_to_mall_map=dict(
            tagged_data='sound_output',
            preprocess_pipeline='pipelines',
            fitted_model='learned_models',
        ),
        output_store='models_scores',
    )
    def apply_fitted_model(tagged_data, preprocess_pipeline, fitted_model):
        sound, tag = tagged_sounds_to_single_array(*tagged_data)
        wfs = np.array(sound)
        wfs = assert_dims(wfs)

        fvs = preprocess_pipeline(wfs)
        scores = fitted_model.score_samples(X=fvs)
        return scores

    @crudifier(param_to_mall_map=dict(pipeline=pipelines_store),)
    def visualize_pipeline(pipeline: LineParametrized):

        return pipeline

    @crudifier(param_to_mall_map=dict(scores='models_scores'),)
    def visualize_scores(scores, threshold=80, num_segs=3):

        intervals = scores_to_intervals(scores, threshold, num_segs)

        return scores, intervals

    @crudifier(output_store='sound_output')
    def upload_sound(train_audio: List[WaveForm], tag: str):

        return train_audio, tag

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
                'execution': {'output': {ELEMENT_KEY: AudioArrayDisplay,},},
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
            'visualize_scores': {
                NAME_KEY: 'Scores Visualization',
                'execution': {'output': {ELEMENT_KEY: ArrayWithIntervalsPlotter,},},
            },
            'simple_model': {
                NAME_KEY: 'Learn model',
                'execution': {'output': {ELEMENT_KEY: ArrayPlotter,},},
            },
            'apply_fitted_model': {
                NAME_KEY: 'Apply model',
                'execution': {'output': {ELEMENT_KEY: ArrayPlotter,},},
            },
        },
    }

    funcs = [
        upload_sound,
        mk_step,
        mk_pipeline,
        learn_outlier_model,
        apply_fitted_model,
        visualize_pipeline,
        visualize_scores,
    ]
    app = mk_app(funcs, config=config)

    return app


mall = dict(
    # Factory Input Stores
    sound_output=dict(),
    step_factories=dict(
        # ML
        chunker=mk_chunker,
        featurizer=mk_featurizer,
    ),
    # Output Store
    data=dict(),
    steps=dict(),
    pipelines=dict(),
    exec_outputs=dict(),
    learned_models=dict(),
    models_scores=dict(),
)


if __name__ == '__main__':

    app = mk_pipeline_maker_app_with_mall(
        mall, step_factories='step_factories', steps='steps', pipelines='pipelines'
    )

    app()
