import warnings
from typing import List

import numpy as np

from sonusai.mixture import GeneralizedIDs
from sonusai.mixture import MixtureDatabase

with warnings.catch_warnings():
    warnings.simplefilter('ignore')
    from keras.utils import Sequence


class KerasFromMixtureDatabase(Sequence):
    """Generates data for Keras from a SonusAI mixture database
    """
    from dataclasses import dataclass

    @dataclass(frozen=True)
    class BatchParams:
        mixids: List[int]
        offset: int
        extra: int
        padding: int

    def __init__(self,
                 mixdb: MixtureDatabase,
                 mixids: GeneralizedIDs,
                 batch_size: int,
                 timesteps: int,
                 flatten: bool,
                 add1ch: bool,
                 shuffle: bool = False):
        """Initialization
        """
        self.mixdb = mixdb
        self.mixids = self.mixdb.mixids_to_list(mixids)
        self.batch_size = batch_size
        self.timesteps = timesteps
        self.flatten = flatten
        self.add1ch = add1ch
        self.shuffle = shuffle
        self.stride = self.mixdb.fg.stride
        self.num_bands = self.mixdb.fg.num_bands
        self.num_classes = self.mixdb.num_classes
        self.mixture_frame_segments = None
        self.batch_frame_segments = None
        self.total_batches = None

        self._initialize_mixtures()

    def __len__(self) -> int:
        """Denotes the number of batches per epoch
        """
        return self.total_batches

    def __getitem__(self, batch_index: int) -> (np.ndarray, np.ndarray):
        """Get one batch of data
        """
        from sonusai.utils import reshape_inputs

        batch_params = self.batch_params[batch_index]

        result = [self.mixdb.mixture_ft(mixid) for mixid in batch_params.mixids]
        feature = np.vstack([result[i][0] for i in range(len(result))])
        truth = np.vstack([result[i][1] for i in range(len(result))])

        pad_shape = list(feature.shape)
        pad_shape[0] = batch_params.padding
        feature = np.vstack([feature, np.zeros(pad_shape)])

        pad_shape = list(truth.shape)
        pad_shape[0] = batch_params.padding
        truth = np.vstack([truth, np.zeros(pad_shape)])

        if batch_params.extra > 0:
            feature = feature[batch_params.offset:-batch_params.extra]
            truth = truth[batch_params.offset:-batch_params.extra]
        else:
            feature = feature[batch_params.offset:]
            truth = truth[batch_params.offset:]

        feature, truth = reshape_inputs(feature=feature,
                                        truth=truth,
                                        batch_size=self.batch_size,
                                        timesteps=self.timesteps,
                                        flatten=self.flatten,
                                        add1ch=self.add1ch)

        return feature, truth

    def on_epoch_end(self) -> None:
        """Modification of dataset between epochs
        """
        import random

        if self.shuffle:
            random.shuffle(self.mixids)
            self._initialize_mixtures()

    def _initialize_mixtures(self) -> None:
        from sonusai.utils import get_frames_per_batch

        frames_per_batch = get_frames_per_batch(self.batch_size, self.timesteps)
        # Always extend the number of batches to use all available data
        # The last batch may need padding
        self.total_batches = int(np.ceil(self.mixdb.total_feature_frames(self.mixids) / frames_per_batch))

        # Compute mixid, offset, and extra for dataset
        # offsets and extras are needed because mixtures are not guaranteed to fall on batch boundaries.
        # When fetching a new index that starts in the middle of a sequence of mixtures, the
        # previous feature frame offset must be maintained in order to preserve the correct
        # data sequence. And the extra must be maintained in order to preserve the correct data length.
        cumulative_frames = 0
        start_mixture_index = 0
        offset = 0
        self.batch_params = []
        self.file_indices = []
        total_frames = 0
        for idx, mixid in enumerate(self.mixids):
            current_frames = self.mixdb.mixture_samples(mixid) // self.mixdb.feature_step_samples
            self.file_indices.append(slice(total_frames, total_frames + current_frames))
            total_frames += current_frames
            cumulative_frames += current_frames
            while cumulative_frames >= frames_per_batch:
                extra = cumulative_frames - frames_per_batch
                mixids = self.mixids[start_mixture_index:idx + 1]
                self.batch_params.append(self.BatchParams(mixids=mixids, offset=offset, extra=extra, padding=0))
                if extra == 0:
                    start_mixture_index = idx + 1
                    offset = 0
                else:
                    start_mixture_index = idx
                    offset = current_frames - extra
                cumulative_frames = extra

        # If needed, add final batch with padding
        needed_frames = self.total_batches * frames_per_batch
        padding = needed_frames - total_frames
        if padding != 0:
            mixids = self.mixids[start_mixture_index:]
            self.batch_params.append(self.BatchParams(mixids=mixids, offset=offset, extra=0, padding=padding))


KerasFromH5 = KerasFromMixtureDatabase
