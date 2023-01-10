import numpy as np
from typing import Iterable, Callable, List
from functools import partial
from plunk.sb.front_demo.user_story1.utils.tools import (
    WaveForm,
    Stroll,
    clean_dict,
    scores_to_intervals,
    # lined_dag,
    tagged_sounds_to_single_array,
    tagged_sound_to_array,
    assert_dims,
)
from meshed.makers import lined_dag
from omodel.outliers.pystroll import OutlierModel as Stroll
from meshed import DAG


def mk_step(step_factory: Callable, kwargs: dict):
    kwargs = clean_dict(kwargs)  # TODO improve that logic
    step = partial(step_factory, **kwargs)()

    return step


#


def mk_pipeline(steps: Iterable[Callable]):
    return lined_dag(steps)
    # return LineParametrized(*steps)


def exec_pipeline(pipeline: Callable, tagged_data):

    sound, _ = tagged_sound_to_array(*tagged_data)
    wfs = np.array(sound)
    wfs = assert_dims(wfs)

    result = pipeline(wfs)
    return result


def learn_outlier_model(tagged_data, preprocess_pipeline, n_centroids=5):
    sound, tag = tagged_sounds_to_single_array(*tagged_data)
    wfs = np.array(sound)

    wfs = assert_dims(wfs)

    fvs = preprocess_pipeline(wfs)
    model = Stroll(n_centroids=n_centroids)
    model.fit(X=fvs)

    return model


def apply_fitted_model(tagged_data, preprocess_pipeline, fitted_model):
    sound, tag = tagged_sounds_to_single_array(*tagged_data)
    wfs = np.array(sound)
    wfs = assert_dims(wfs)

    fvs = preprocess_pipeline(wfs)
    scores = fitted_model.score_samples(X=fvs)
    return scores


def visualize_pipeline(pipeline: DAG):

    return pipeline


def visualize_scores(scores, threshold=80, num_segs=3):

    intervals = scores_to_intervals(scores, threshold, num_segs)

    return scores, intervals


def upload_sound(train_audio: List[WaveForm], tag: str):
    # sound, tag = train_audio, tag
    # if not isinstance(sound, bytes):
    #     sound = sound.getvalue()

    # arr = sf.read(BytesIO(sound), dtype='int16')[0]
    # return arr, tag
    return train_audio, tag


def display_tag_sound(result):
    return result


def learn_apply_model(tagged_data, pipeline):
    n_centroids = 15
    sound, _ = tagged_sounds_to_single_array(*tagged_data)
    wfs = np.array(sound)
    wfs = assert_dims(wfs)

    fvs = pipeline(wfs)
    model = Stroll(n_centroids=n_centroids)
    fitted_model = model.fit(X=fvs)
    scores = fitted_model.score_samples(X=fvs)
    return scores
