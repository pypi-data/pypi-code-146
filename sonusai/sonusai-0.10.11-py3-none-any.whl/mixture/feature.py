import numpy as np

from sonusai.mixture.mixdb import MixtureDatabase
from sonusai.mixture.types import AudioT
from sonusai.mixture.types import Feature


def get_feature_from_audio(audio: AudioT, feature: str) -> Feature:
    from sonusai.mixture import MRecord
    from sonusai.mixture import MixtureDatabaseConfig
    from sonusai.mixture import get_pad_length

    mixdb = MixtureDatabase(config=MixtureDatabaseConfig(feature=feature,
                                                         num_classes=1,
                                                         truth_mutex=False,
                                                         truth_reduction_function='max'),
                            lazy_load=True)

    audio = np.pad(array=audio, pad_width=(0, get_pad_length(len(audio), mixdb.feature_step_samples)))
    mixdb.mixtures = [MRecord(samples=len(audio))]

    data, _ = mixdb.mixture_ft(mixid=0, mixture=audio, truth_t=np.empty((len(audio), 1)), force=True)
    return data
