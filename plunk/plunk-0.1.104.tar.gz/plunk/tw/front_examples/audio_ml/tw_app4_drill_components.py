"""Components for tw_app4_drill"""

from functools import partial
from typing import Callable, Iterable, List
from io import BytesIO

from lined import LineParametrized
import numpy as np

import soundfile as sf

# --------------------------------------------------------------------------------------
# UTILS

from plunk.sb.front_demo.user_story1.utils.tools import (
    Stroll,
    scores_to_intervals,
)
from slang import fixed_step_chunker

DFLT_FEATURIZER = lambda chk: np.abs(np.fft.rfft(chk))
DFLT_CHK_SIZE = 2048
DFLT_CHK_STEP = 2048
WaveForm = Iterable[int]


def simple_chunker(it, chk_size: int = DFLT_CHK_SIZE):
    return fixed_step_chunker(it=it, chk_size=chk_size, chk_step=chk_size)


def clean_dict(kwargs):
    result = {k: v for k, v in kwargs.items() if v != ''}
    return result


def tagged_sound_to_array(train_audio: WaveForm, tag: str):
    sound, tag = train_audio, tag
    if not isinstance(sound, bytes):
        sound = sound.getvalue()

    arr = sf.read(BytesIO(sound), dtype='int16')[0]  # TODO: use recode
    return arr, tag


def tagged_sounds_to_single_array(train_audio: List[WaveForm], tag: str):
    sounds, tag = train_audio, tag
    result = []
    for sound in sounds:
        # if not isinstance(sound, bytes):
        sound = sound.getvalue()
        arr = sf.read(BytesIO(sound), dtype='int16')[0]
        result.append(arr)
    # print(np.hstack(result))
    return np.hstack(result).reshape(-1, 1), tag


def assert_dims(wfs):
    if wfs.ndim >= 2:
        wfs = wfs[:, 0]
    return wfs


featurizer = DFLT_FEATURIZER
chunker = simple_chunker
WaveForm = Iterable[int]

# --------------------------------------------------------------------------------------
# COMPONENTS

# @crudifier(
#         param_to_mall_map=dict(step_factory=step_factories), output_store=steps_store
#     )
def mk_step(step_factory: Callable, kwargs: dict):
    kwargs = clean_dict(kwargs)  # TODO improve that logic
    step = partial(step_factory, **kwargs)()

    return step


#
# @crudifier(output_store=pipelines_store,)
def mk_pipeline(steps: Iterable[Callable]):
    return LineParametrized(*steps)


# @crudifier(
#     param_to_mall_map=dict(pipeline=pipelines_store, tagged_data='sound_output'),
#     output_store='exec_outputs',
# )
def exec_pipeline(pipeline: Callable, tagged_data):

    sound, _ = tagged_sound_to_array(*tagged_data)
    wfs = np.array(sound)
    wfs = assert_dims(wfs)

    result = pipeline(wfs)
    return result


# @crudifier(
#     param_to_mall_map=dict(
#         tagged_data='sound_output', preprocess_pipeline='pipelines'
#     ),
#     output_store='learned_models',
# )
def learn_outlier_model(tagged_data, preprocess_pipeline, n_centroids=5):
    sound, tag = tagged_sounds_to_single_array(*tagged_data)
    wfs = np.array(sound)

    wfs = assert_dims(wfs)

    fvs = preprocess_pipeline(wfs)
    model = Stroll(n_centroids=n_centroids)
    model.fit(X=fvs)

    return model


# @crudifier(
#     param_to_mall_map=dict(
#         tagged_data='sound_output',
#         preprocess_pipeline='pipelines',
#         fitted_model='learned_models',
#     ),
#     output_store='models_scores',
# )
def apply_fitted_model(tagged_data, preprocess_pipeline, fitted_model):
    sound, tag = tagged_sounds_to_single_array(*tagged_data)
    wfs = np.array(sound)
    wfs = assert_dims(wfs)

    fvs = preprocess_pipeline(wfs)
    scores = fitted_model.score_samples(X=fvs)
    return scores


# @crudifier(param_to_mall_map=dict(pipeline=pipelines_store),)
def visualize_pipeline(pipeline: LineParametrized):

    return pipeline


# @crudifier(param_to_mall_map=dict(scores='models_scores'),)
def visualize_scores(scores, threshold=80, num_segs=3):

    intervals = scores_to_intervals(scores, threshold, num_segs)

    return scores, intervals


# @crudifier(output_store='sound_output')
def upload_sound(train_audio: List[WaveForm], tag: str):
    # sound, tag = train_audio, tag
    # if not isinstance(sound, bytes):
    #     sound = sound.getvalue()

    # arr = sf.read(BytesIO(sound), dtype='int16')[0]
    # return arr, tag
    return train_audio, tag


# @crudifier(param_to_mall_map={'result': 'sound_output'})
def display_tag_sound(result):
    return result
