from dataclasses import dataclass
from typing import Any
from typing import List
from typing import Tuple
from typing import Union

from pyaaware import FeatureGenerator

from sonusai.mixture.types import AudioF
from sonusai.mixture.types import AudioT
from sonusai.mixture.types import AudiosF
from sonusai.mixture.types import AudiosT
from sonusai.mixture.types import Augmentation
from sonusai.mixture.types import Augmentations
from sonusai.mixture.types import ClassCount
from sonusai.mixture.types import DataClassSonusAIMixin
from sonusai.mixture.types import Feature
from sonusai.mixture.types import GeneralizedIDs
from sonusai.mixture.types import ImpulseResponseData
from sonusai.mixture.types import ImpulseResponseFiles
from sonusai.mixture.types import Location
from sonusai.mixture.types import NoiseFiles
from sonusai.mixture.types import Optional
from sonusai.mixture.types import Segsnr
from sonusai.mixture.types import TargetFiles
from sonusai.mixture.types import Truth
from sonusai.mixture.types import TruthSettings


# NOTE: global object is required for run-time performance; using 'partial' is much slower.
@dataclass
class MPGlobal:
    noise_augmentations: Augmentations = None
    ir_data: List[ImpulseResponseData] = None


MP_GLOBAL = MPGlobal()


@dataclass
class MRecord(DataClassSonusAIMixin):
    name: Location = None
    noise_augmentation_index: int = None
    noise_file_index: int = None
    noise_offset: int = None
    noise_snr_gain: float = None
    random_snr: Optional[bool] = None
    samples: int = None
    snr: float = None
    target_augmentation_index: List[int] = None
    target_file_index: List[int] = None
    target_gain: List[int] = None
    target_snr_gain: float = None


MRecords = List[MRecord]


@dataclass
class MixtureDatabaseConfig(DataClassSonusAIMixin):
    class_balancing: Optional[bool] = False
    class_balancing_augmentation: Optional[Augmentation] = None
    class_labels: List[str] = None
    class_weights_threshold: List[float] = None
    exhaustive_noise: Optional[bool] = True
    feature: str = None
    first_cba_index: Optional[int] = None
    ir_files: ImpulseResponseFiles = None
    mixtures: MRecords = None
    noise_augmentations: Augmentations = None
    noises: NoiseFiles = None
    num_classes: int = None
    random_snrs: Optional[List[str]] = None
    seed: Optional[int] = 0
    snrs: List[float] = None
    target_augmentations: Augmentations = None
    targets: TargetFiles = None
    truth_mutex: bool = None
    truth_reduction_function: str = None
    truth_settings: TruthSettings = None


@dataclass
class TransformConfig:
    N: int
    R: int
    ttype: str


class MixtureDatabase:
    from sonusai.mixture.types import AudiosT
    from sonusai.mixture.types import ListAudiosT

    def __init__(self,
                 config: Union[Location, MixtureDatabaseConfig],
                 lazy_load: bool = False,
                 show_progress: bool = False):
        if isinstance(config, MixtureDatabaseConfig):
            self.config = config
            self.location = None
        else:
            self._load_from_location(config)
            self.location = config

        self.fg = FeatureGenerator(feature_mode=self.feature,
                                   num_classes=self.num_classes,
                                   truth_mutex=self.truth_mutex)

        self.ft_config = TransformConfig(N=self.fg.ftransform_N,
                                         R=self.fg.ftransform_R,
                                         ttype=self.fg.ftransform_ttype)

        self.eft_config = TransformConfig(N=self.fg.eftransform_N,
                                          R=self.fg.eftransform_R,
                                          ttype=self.fg.eftransform_ttype)

        self.it_config = TransformConfig(N=self.fg.itransform_N,
                                         R=self.fg.itransform_R,
                                         ttype=self.fg.itransform_ttype)

        self.show_progress = show_progress
        self._ir_data = None
        self._raw_target_audios = None
        self._augmented_noise_audios = None

        if not lazy_load:
            self.load_ir_data(show_progress=show_progress)
            self.load_raw_target_audios(show_progress=show_progress)
            self.load_augmented_noise_audios(show_progress=show_progress)

    def _load_from_location(self, location: Location) -> None:
        import json
        from os.path import exists
        from os.path import isdir
        from os.path import join

        from sonusai import SonusAIError

        if not isdir(location):
            raise SonusAIError(f'{location} is not a directory')

        filename = join(location, 'mixdb.json')
        if not exists(filename):
            raise SonusAIError(f'could not find mixture database in {location}')

        with open(file=filename, mode='r', encoding='utf-8') as f:
            self.config = MixtureDatabaseConfig.from_dict(json.loads(f.read()))

    @property
    def json(self) -> str:
        """Convert MixtureDatabase to JSON

        :return: JSON representation of database
        """
        return self.config.to_json(indent=2)

    def save(self) -> None:
        """Save the MixtureDatabase as a JSON file

        """
        from os.path import join

        json_name = join(self.location, 'mixdb.json')
        with open(file=json_name, mode='w') as file:
            file.write(self.json)

    def forward_transform(self, audio: AudioT) -> AudioF:
        """Tranform time domain data into frequency domain using the forward transform config from the feature

        A new transform is used for each call; i.e., state is not maintained between calls to forward_transform().

        :param audio: Time domain data [samples]
        :return: Frequency domain data [frames, bins]
        """
        from pyaaware import ForwardTransform

        from sonusai.mixture import calculate_transform_from_audio

        return calculate_transform_from_audio(audio=audio,
                                              transform=ForwardTransform(N=self.ft_config.N,
                                                                         R=self.ft_config.R,
                                                                         ttype=self.ft_config.ttype))

    def inverse_transform(self, transform: AudioF, trim: bool = True) -> AudioT:
        """Tranform frequency domain data into time domain using the inverse transform config from the feature

        A new transform is used for each call; i.e., state is not maintained between calls to inverse_transform().

        :param transform: Frequency domain data [frames, bins]
        :param trim: Removes starting samples so output waveform will be time-aligned with input waveform to the transform
        :return: Time domain data [samples]
        """
        from pyaaware import InverseTransform

        from sonusai.mixture import calculate_audio_from_transform

        return calculate_audio_from_transform(data=transform,
                                              transform=InverseTransform(N=self.it_config.N,
                                                                         R=self.it_config.R,
                                                                         ttype=self.it_config.ttype),
                                              trim=trim)

    @property
    def class_balancing(self):
        return self.config.class_balancing

    @class_balancing.setter
    def class_balancing(self, value):
        self.config.class_balancing = value

    @property
    def class_balancing_augmentation(self):
        return self.config.class_balancing_augmentation

    @class_balancing_augmentation.setter
    def class_balancing_augmentation(self, value):
        self.config.class_balancing_augmentation = value

    @property
    def class_labels(self):
        return self.config.class_labels

    @class_labels.setter
    def class_labels(self, value):
        from sonusai import SonusAIError

        if value is not None and (not isinstance(value, list) or len(value) != self.num_classes):
            raise SonusAIError(f'invalid class_labels length')
        self.config.class_labels = value

    @property
    def class_weights_threshold(self):
        return self.config.class_weights_threshold

    @class_weights_threshold.setter
    def class_weights_threshold(self, value):
        from sonusai import SonusAIError

        if len(value) not in [1, self.num_classes]:
            raise SonusAIError(f'invalid class_weights_threshold length: {len(class_weights_threshold)}')
        self.config.class_weights_threshold = value

    @property
    def exhaustive_noise(self):
        return self.config.exhaustive_noise

    @exhaustive_noise.setter
    def exhaustive_noise(self, value):
        self.config.exhaustive_noise = value

    @property
    def feature(self):
        return self.config.feature

    @feature.setter
    def feature(self, value):
        self.config.feature = value

    @property
    def transform_frame_ms(self):
        from sonusai.mixture import SAMPLE_RATE

        return float(self.ft_config.R) / float(SAMPLE_RATE / 1000)

    @property
    def feature_ms(self):
        return self.transform_frame_ms * self.fg.decimation * self.fg.stride

    @property
    def feature_samples(self):
        return self.ft_config.R * self.fg.decimation * self.fg.stride

    @property
    def feature_step_ms(self):
        return self.transform_frame_ms * self.fg.decimation * self.fg.step

    @property
    def feature_step_samples(self):
        return self.ft_config.R * self.fg.decimation * self.fg.step

    @property
    def first_cba_index(self):
        return self.config.first_cba_index

    @first_cba_index.setter
    def first_cba_index(self, value):
        self.config.first_cba_index = value

    @property
    def ir_files(self):
        return self.config.ir_files

    @property
    def mixtures(self):
        return self.config.mixtures

    @mixtures.setter
    def mixtures(self, value):
        self.config.mixtures = value

    @property
    def noise_augmentations(self):
        return self.config.noise_augmentations

    @noise_augmentations.setter
    def noise_augmentations(self, value):
        self.config.noise_augmentations = value

    @property
    def noises(self):
        return self.config.noises

    @noises.setter
    def noises(self, value):
        self.config.noises = value

    @property
    def num_classes(self):
        return self.config.num_classes

    @num_classes.setter
    def num_classes(self, value):
        self.config.num_classes = value

    @property
    def random_snrs(self):
        return self.config.random_snrs

    @random_snrs.setter
    def random_snrs(self, value):
        self.config.random_snrs = value

    @property
    def seed(self):
        return self.config.seed

    @seed.setter
    def seed(self, value):
        self.config.seed = value

    @property
    def snrs(self):
        return self.config.snrs

    @snrs.setter
    def snrs(self, value):
        self.config.snrs = value

    @property
    def target_augmentations(self):
        return self.config.target_augmentations

    @target_augmentations.setter
    def target_augmentations(self, value):
        self.config.target_augmentations = value

    @property
    def targets(self):
        return self.config.targets

    @targets.setter
    def targets(self, value):
        self.config.targets = value

    @property
    def truth_mutex(self):
        return self.config.truth_mutex

    @truth_mutex.setter
    def truth_mutex(self, value):
        self.config.truth_mutex = value

    @property
    def truth_reduction_function(self):
        return self.config.truth_reduction_function

    @truth_reduction_function.setter
    def truth_reduction_function(self, value):
        self.config.truth_reduction_function = value

    @property
    def truth_settings(self):
        return self.config.truth_settings

    @truth_settings.setter
    def truth_settings(self, value):
        self.config.truth_settings = value

    @property
    def raw_target_audios(self) -> AudiosT:
        """Get the list of raw (unaugmented) target audio, loading from disk if necessary

        :return: List of raw target audio
        """
        if self._raw_target_audios is None:
            self.load_raw_target_audios(show_progress=self.show_progress)

        return self._raw_target_audios

    def load_raw_target_audios(self, show_progress: bool = False) -> None:
        """Load all raw (unaugmented) target audio into memory

        :param show_progress: Enable progress bar display
        """
        from tqdm import tqdm

        from sonusai.mixture import read_audio
        from sonusai.utils import p_tqdm_map

        names = [target.name for target in self.targets]
        progress = tqdm(total=len(names), desc='Read target audio', disable=not show_progress)
        self._raw_target_audios = p_tqdm_map(read_audio, names, progress=progress)
        progress.close()

    @property
    def augmented_noise_audios(self) -> ListAudiosT:
        """Get the list of augmented noise audio, loading from disk if necessary

        :return: List of augmented noise audio
        """
        if self._augmented_noise_audios is None:
            self.load_augmented_noise_audios(show_progress=self.show_progress)

        return self._augmented_noise_audios

    def load_augmented_noise_audios(self, show_progress: bool = False) -> None:
        """Load all augmented noise audio into memory

        :param show_progress: Enable progress bar display
        """
        from tqdm import tqdm

        from sonusai.mixture import read_audio
        from sonusai.utils import p_tqdm_map

        names = [noise.name for noise in self.noises]

        progress = tqdm(total=len(names), desc='Read noise audio', disable=not show_progress)
        raw_noise_audios = p_tqdm_map(read_audio, names, progress=progress)
        progress.close()

        MP_GLOBAL.noise_augmentations = self.noise_augmentations
        MP_GLOBAL.ir_data = self.ir_data

        progress = tqdm(total=len(names), desc='Augment noise audio', disable=not show_progress)
        self._augmented_noise_audios = p_tqdm_map(_augment_noise_audio, raw_noise_audios, progress=progress)
        progress.close()

    @property
    def ir_data(self) -> List[ImpulseResponseData]:
        """Get the list of impulse response data, loading from disk if necessary

        :return: List of impulse response data
        """
        if self._ir_data is None:
            self.load_ir_data(show_progress=self.show_progress)

        return self._ir_data

    def load_ir_data(self, show_progress: bool = False) -> None:
        """Load all impulse response data into memory

        :param show_progress: Enable progress bar display
        :return: List of impulse response data
        """
        if len(self.ir_files) == 0:
            self._ir_data = []
            return

        from tqdm import tqdm

        from sonusai.mixture import read_ir
        from sonusai.utils import p_tqdm_map

        progress = tqdm(total=len(self.ir_files), desc='Read impulse response data', disable=not show_progress)
        self._ir_data = p_tqdm_map(read_ir, self.ir_files, progress=progress)
        progress.close()

    def total_samples(self, mixids: GeneralizedIDs = '*') -> int:
        return sum([self.mixture_samples(mixid) for mixid in self.mixids_to_list(mixids)])

    def total_transform_frames(self, mixids: GeneralizedIDs = '*') -> int:
        return self.total_samples(mixids) // self.ft_config.R

    def total_feature_frames(self, mixids: GeneralizedIDs = '*') -> int:
        return self.total_samples(mixids) // self.feature_step_samples

    def mixture_samples(self, mixid: int) -> int:
        return self.mixtures[mixid].samples

    def mixture_transform_frames(self, mixid: int) -> int:
        return self.mixture_samples(mixid) // self.ft_config.R

    def mixture_feature_frames(self, mixid: int) -> int:
        return self.mixture_samples(mixid) // self.feature_step_samples

    def mixids_to_list(self, ids: GeneralizedIDs = None) -> List[int]:
        """Resolve generalized mixture IDs to a list of integers

        :param ids: Generalized mixture IDs
        :return: List of mixture ID integers
        """
        return generic_ids_to_list(len(self.mixtures), ids)

    def mixture_metadata(self, mixid: int) -> str:
        """Create a string of metadata for a mixture ID

        :param mixid: Mixture ID
        :return: String of metadata
        """
        mrecord = self.mixtures[mixid]
        metadata = ''
        for ti in range(len(mrecord.target_file_index)):
            tfi = mrecord.target_file_index[ti]
            tai = mrecord.target_augmentation_index[ti]
            metadata += f'target {ti} name: {self.targets[tfi].name}\n'
            metadata += f'target {ti} augmentation: {self.target_augmentations[tai].to_dict()}\n'
            if self.target_augmentations[tai].ir is None:
                ir_name = None
            else:
                ir_name = self.ir_files[self.target_augmentations[tai].ir]
            metadata += f'target {ti} ir: {ir_name}\n'
            metadata += f'target {ti} target_gain: {mrecord.target_gain[ti]}\n'
            truth_settings = self.targets[tfi].truth_settings
            for tsi in range(len(truth_settings)):
                metadata += f'target {ti} truth index {tsi}: {truth_settings[tsi].index}\n'
                metadata += f'target {ti} truth function {tsi}: {truth_settings[tsi].function}\n'
                metadata += f'target {ti} truth config {tsi}: {truth_settings[tsi].config}\n'
        nfi = mrecord.noise_file_index
        nai = mrecord.noise_augmentation_index
        metadata += f'noise name: {self.noises[nfi].name}\n'
        metadata += f'noise augmentation: {self.noise_augmentations[nai].to_dict()}\n'
        if self.noise_augmentations[nai].ir is None:
            ir_name = None
        else:
            ir_name = self.ir_files[self.noise_augmentations[nai].ir]
        metadata += f'noise ir: {ir_name}\n'
        metadata += f'snr: {mrecord.snr}\n'
        metadata += f'random_snr: {mrecord.random_snr}\n'
        metadata += f'samples: {mrecord.samples}\n'
        metadata += f'target_snr_gain: {mrecord.target_snr_gain}\n'
        metadata += f'noise_snr_gain: {mrecord.noise_snr_gain}\n'

        return metadata

    def write_mixture_metadata(self, mixid: int) -> None:
        """Write mixture metadata to a text file

        :param mixid: Mixture ID
        """
        from os.path import splitext

        with open(file=splitext(self.mixture_filename(mixid))[0] + '.txt', mode='w') as f:
            f.write(self.mixture_metadata(mixid))

    def mixture_filename(self, mixid: int) -> Location:
        """Get the HDF5 file name for the given mixture ID

        :param mixid: Mixture ID
        :return: File name
        """
        from os.path import join

        return join(self.location, self.mixtures[mixid].name) if self.location is not None else None

    def check_audio_files_exist(self) -> None:
        """Walk through all the noise and target audio files in a mixture database ensuring that they exist
        """
        from os.path import exists

        from sonusai import SonusAIError
        from sonusai.mixture import tokenized_expandvars

        for file_index in range(len(self.noises)):
            file_name, _ = tokenized_expandvars(self.noises[file_index].name)
            if not exists(file_name):
                raise SonusAIError(f'Could not find {file_name}')

        for file_index in range(len(self.targets)):
            file_name, _ = tokenized_expandvars(self.targets[file_index].name)
            if not exists(file_name):
                raise SonusAIError(f'Could not find {file_name}')

    def read_mixture_data(self, mixid: int, items: Union[List[str], str]) -> Any:
        """Read mixture data from a mixture HDF5 file

        :param mixid: Mixture ID
        :param items: String(s) of dataset(s) to retrieve
        :return: Data (or tuple of data)
        """
        from os.path import exists

        import h5py
        import numpy as np

        from sonusai import SonusAIError

        def _get_dataset(file: h5py.File, name: str) -> Any:
            if name in file:
                return np.array(file[name])
            return None

        if not isinstance(items, list):
            items = [items]

        name = self.mixture_filename(mixid)
        if exists(name):
            try:
                with h5py.File(name, 'r') as f:
                    result = ([_get_dataset(f, item) for item in items])
            except Exception as e:
                raise SonusAIError(f'Error reading {name}: {e}')
        else:
            result = ([None for item in items])

        if len(items) == 1:
            result = result[0]

        return result

    def write_mixture_data(self, mixid: int, items: Union[List[Tuple[str, Any]], Tuple[str, Any]]) -> None:
        """Write mixture data to a mixture HDF5 file

        :param mixid: Mixture ID
        :param items: Tuple(s) of (name, data)
        """
        import h5py

        if not isinstance(items, list):
            items = [items]

        with h5py.File(self.mixture_filename(mixid), 'a') as f:
            for item in items:
                if item[0] in f:
                    del f[item[0]]
                f.create_dataset(name=item[0], data=item[1])

    def mixture_targets(self,
                        mixid: int,
                        force: bool = False) -> AudiosT:
        """Get the list of augmented target audio data (one per target in the mixup) for the given mixid

        :param mixid: Mixture ID
        :param force: Force computing data from original sources regardless of whether or not cached data exists
        :return: List of augmented target audio data (one per target in the mixup)
        """
        from sonusai.mixture import apply_augmentation
        from sonusai.mixture import apply_gain
        from sonusai.mixture import pad_audio_to_length
        from sonusai.mixture import read_audio

        if not force:
            targets = self.read_mixture_data(mixid, 'targets')
            if targets is not None:
                return list(targets)

        mrecord = self.mixtures[mixid]
        targets = []
        for idx in range(len(mrecord.target_file_index)):
            if self.raw_target_audios is not None:
                target = self.raw_target_audios[mrecord.target_file_index[idx]]
            else:
                target = read_audio(self.targets[mrecord.target_file_index[idx]].name)

            target = apply_augmentation(audio=target,
                                        augmentation=self.target_augmentations[mrecord.target_augmentation_index[idx]],
                                        length_common_denominator=self.feature_step_samples)

            target = apply_gain(audio=target, gain=mrecord.target_snr_gain)
            target = pad_audio_to_length(audio=target, length=mrecord.samples)
            targets.append(target)

        return targets

    def mixture_targets_f(self,
                          mixid: int,
                          targets: AudiosT = None,
                          force: bool = False) -> AudiosF:
        """Get the list of augmented target transform data (one per target in the mixup) for the given mixid

        :param mixid: Mixture ID
        :param targets: List of augmented target audio data (one per target in the mixup) for the given mixid
        :param force: Force computing data from original sources regardless of whether or not cached data exists
        :return: List of augmented target transform data (one per target in the mixup)
        """
        if targets is None:
            targets = self.mixture_targets(mixid=mixid, force=force)

        return [self.forward_transform(target) for target in targets]

    def mixture_target(self,
                       mixid: int,
                       targets: AudiosT = None,
                       force: bool = False) -> AudioT:
        """Get the augmented target audio data for the given mixid

        :param mixid: Mixture ID
        :param targets: List of augmented target audio data (one per target in the mixup) for the given mixid
        :param force: Force computing data from original sources regardless of whether or not cached data exists
        :return: Augmented target audio data
        """
        from sonusai.mixture import apply_ir

        if not force:
            target = self.read_mixture_data(mixid, 'target')
            if target is not None:
                return target

        if targets is None:
            targets = self.mixture_targets(mixid=mixid, force=force)

        # Apply impulse responses to targets
        targets_ir = []
        for idx, target in enumerate(targets):
            ir_idx = self.target_augmentations[self.mixtures[mixid].target_augmentation_index[idx]].ir
            if ir_idx is not None:
                targets_ir.append(apply_ir(audio=target, ir=self.ir_data[ir_idx]))
            else:
                targets_ir.append(target)
        targets = targets_ir

        return sum(targets)

    def mixture_target_f(self,
                         mixid: int,
                         targets: AudiosT = None,
                         target: AudioT = None,
                         force: bool = False) -> AudioF:
        """Get the augmented target transform data for the given mixid

        :param mixid: Mixture ID
        :param targets: List of augmented target audio data (one per target in the mixup) for the given mixid
        :param target: Augmented target audio for the given mixid
        :param force: Force computing data from original sources regardless of whether or not cached data exists
        :return: Augmented target transform data
        """
        if target is None:
            target = self.mixture_target(mixid=mixid, targets=targets, force=force)

        return self.forward_transform(target)

    def mixture_noise(self,
                      mixid: int,
                      force: bool = False) -> AudioT:
        """Get the augmented noise audio data for the given mixid

        :param mixid: Mixture ID
        :param force: Force computing data from original sources regardless of whether or not cached data exists
        :return: Augmented noise audio data
        """
        from sonusai.mixture import apply_augmentation
        from sonusai.mixture import apply_gain
        from sonusai.mixture import get_next_noise
        from sonusai.mixture import read_audio

        if not force:
            noise = self.read_mixture_data(mixid, 'noise')
            if noise is not None:
                return noise

        mrecord = self.mixtures[mixid]
        if self.augmented_noise_audios is not None:
            noise = self.augmented_noise_audios[mrecord.noise_file_index][mrecord.noise_augmentation_index]
        else:
            noise = apply_augmentation(audio=read_audio(self.noises[mrecord.noise_file_index].name),
                                       augmentation=self.noise_augmentations[mrecord.noise_augmentation_index])

        noise = get_next_noise(audio=noise, offset=mrecord.noise_offset, length=mrecord.samples)
        noise = apply_gain(audio=noise, gain=mrecord.noise_snr_gain)

        return noise

    def mixture_noise_f(self,
                        mixid: int,
                        noise: AudioT = None,
                        force: bool = False) -> AudioF:
        """Get the augmented noise transform for the given mixid

        :param mixid: Mixture ID
        :param noise: Augmented noise audio data for the given mixid
        :param force: Force computing data from original sources regardless of whether or not cached data exists
        :return: Augmented noise transform data
        """
        if noise is None:
            noise = self.mixture_noise(mixid=mixid, force=force)

        return self.forward_transform(noise)

    def mixture_mixture(self,
                        mixid: int,
                        targets: AudiosT = None,
                        target: AudioT = None,
                        noise: AudioT = None,
                        force: bool = False) -> AudioT:
        """Get the mixture audio data for the given mixid

        :param mixid: Mixture ID
        :param targets: List of augmented target audio data (one per target in the mixup) for the given mixid
        :param target: Augmented target audio data for the given mixid
        :param noise: Augmented noise audio data for the given mixid
        :param force: Force computing data from original sources regardless of whether or not cached data exists
        :return: Mixture audio data
        """
        if not force:
            mixture = self.read_mixture_data(mixid, 'mixture')
            if mixture is not None:
                return mixture

        if target is None:
            target = self.mixture_target(mixid=mixid, targets=targets)

        if noise is None:
            noise = self.mixture_noise(mixid=mixid)

        mixture = target + noise

        return mixture

    def mixture_mixture_f(self, mixid: int,
                          targets: AudiosT = None,
                          target: AudioT = None,
                          noise: AudioT = None,
                          mixture: AudioT = None,
                          force: bool = False) -> AudioF:
        """Get the mixture transform for the given mixid

        :param mixid: Mixture ID
        :param targets: List of augmented target audio data (one per target in the mixup) for the given mixid
        :param target: Augmented target audio data for the given mixid
        :param noise: Augmented noise audio data for the given mixid
        :param mixture: Mixture audio data for the given mixid
        :return: Mixture transform data
        """
        if mixture is None:
            mixture = self.mixture_mixture(mixid=mixid, targets=targets, target=target, noise=noise, force=force)

        return self.forward_transform(mixture)

    def mixture_truth_t(self,
                        mixid: int,
                        targets: AudiosT = None,
                        noise: AudioT = None,
                        force: bool = False) -> Truth:
        """Get the truth_t data for the given mixid

        :param mixid: Mixture ID
        :param targets: List of augmented target audio data (one per target in the mixup) for the given mixid
        :param noise: Augmented noise audio data for the given mixid
        :param force: Force computing data from original sources regardless of whether or not cached data exists
        :return: truth_t data
        """
        import numpy as np

        from sonusai import SonusAIError
        from sonusai.mixture import TruthFunctionConfig
        from sonusai.mixture import truth_function

        if not force:
            truth_t = self.read_mixture_data(mixid, 'truth_t')
            if truth_t is not None:
                return truth_t

        if targets is None:
            targets = self.mixture_targets(mixid=mixid)

        if noise is None:
            noise = self.mixture_noise(mixid=mixid)

        mrecord = self.mixtures[mixid]
        if len(targets) != len(mrecord.target_file_index):
            raise SonusAIError('Number of target audio entries does not match number of targets')

        if not all(len(target_audio) == len(noise) for target_audio in targets):
            raise SonusAIError('Lengths of target audio do not match length of noise audio')

        truth_t = np.zeros((self.mixture_samples(mixid), self.num_classes), dtype=np.float32)
        for idx in range(len(targets)):
            for truth_setting in self.targets[mrecord.target_file_index[idx]].truth_settings:
                config = TruthFunctionConfig(
                    feature=self.feature,
                    index=truth_setting.index,
                    function=truth_setting.function,
                    config=truth_setting.config,
                    num_classes=self.num_classes,
                    mutex=self.truth_mutex,
                    target_gain=mrecord.target_gain[idx] * mrecord.target_snr_gain
                )
                truth_t += truth_function(target_audio=targets[idx], noise_audio=noise, config=config)

        return truth_t

    def mixture_segsnr_t(self,
                         mixid: int,
                         targets: AudiosT = None,
                         target: AudioT = None,
                         noise: AudioT = None,
                         force: bool = False) -> Segsnr:
        """Get the segsnr_t data for the given mixid

        :param mixid: Mixture ID
        :param targets: List of augmented target audio data (one per target in the mixup) for the given mixid
        :param target: Augmented target audio data for the given mixid
        :param noise: Augmented noise audio data for the given mixid
        :param force: Force computing data from original sources regardless of whether or not cached data exists
        :return: segsnr_t data
        """
        import numpy as np

        from pyaaware import ForwardTransform

        if not force:
            segsnr_t = self.read_mixture_data(mixid, 'segsnr_t')
            if segsnr_t is not None:
                return segsnr_t

        if target is None:
            target = self.mixture_target(mixid=mixid, targets=targets)

        if noise is None:
            noise = self.mixture_noise(mixid=mixid)

        fft = ForwardTransform(N=self.ft_config.N, R=self.ft_config.R, ttype=self.ft_config.ttype)

        segsnr_t = np.empty(self.mixture_samples(mixid), dtype=np.float32)

        frame = 0
        for offset in range(0, self.mixture_samples(mixid), self.ft_config.R):
            indices = slice(offset, offset + self.ft_config.R)

            target_energy = fft.energy_t(target[indices])
            noise_energy = fft.energy_t(noise[indices])

            if noise_energy == 0:
                snr = np.float32(np.inf)
            else:
                snr = np.float32(target_energy / noise_energy)

            segsnr_t[indices] = snr

        return segsnr_t

    def mixture_segsnr(self,
                       mixid: int,
                       segsnr_t: Segsnr = None,
                       targets: AudiosT = None,
                       target: AudioT = None,
                       noise: AudioT = None,
                       force: bool = False) -> Segsnr:
        """Get the segsnr data for the given mixid

        :param mixid: Mixture ID
        :param segsnr_t: segsnr_t data for the given mixid
        :param targets: List of augmented target audio data (one per target in the mixup) for the given mixid
        :param target: Augmented target audio data for the given mixid
        :param noise: Augmented noise audio data for the given mixid
        :param force: Force computing data from original sources regardless of whether or not cached data exists
        :return: segsnr data
        """
        if not force:
            segsnr = self.read_mixture_data(mixid, 'segsnr')
            if segsnr is not None:
                return segsnr

            segsnr_t = self.read_mixture_data(mixid, 'segsnr_t')
            if segsnr_t is not None:
                return segsnr_t[0::self.ft_config.R]

        if segsnr_t is None:
            segsnr_t = self.mixture_segsnr_t(mixid=mixid, targets=targets, target=target, noise=noise)

        segsnr = segsnr_t[0::self.ft_config.R]

        return segsnr

    def mixture_ft(self,
                   mixid: int,
                   targets: AudiosT = None,
                   target: AudioT = None,
                   noise: AudioT = None,
                   mixture_f: AudioF = None,
                   mixture: AudioT = None,
                   truth_t: Truth = None,
                   force: bool = False) -> (Feature, Truth):
        """Get the feature and truth_f data for the given mixid

        :param mixid: Mixture ID
        :param targets: List of augmented target audio data (one per target in the mixup) for the given mixid
        :param target: Augmented target audio data for the given mixid
        :param noise: Augmented noise audio data for the given mixid
        :param mixture_f: Mixture transform data for the given mixid
        :param mixture: Mixture audio data for the given mixid
        :param truth_t: truth_t for the given mixid
        :param force: Force computing data from original sources regardless of whether or not cached data exists
        :return: Tuple of (feature, truth_f) data
        """
        import numpy as np

        from sonusai.mixture import truth_reduction

        if not force:
            feature, truth_f = self.read_mixture_data(mixid, ['feature', 'truth_f'])
            if feature is not None and truth_f is not None:
                return feature, truth_f

        if mixture_f is None:
            mixture_f = self.mixture_mixture_f(mixid=mixid,
                                               targets=targets,
                                               target=target,
                                               noise=noise,
                                               mixture=mixture)

            if truth_t is None:
                truth_t = self.mixture_truth_t(mixid=mixid, targets=targets, noise=noise)

            mrecord = self.mixtures[mixid]

            transform_frames = self.mixture_transform_frames(mixid)
            feature_frames = self.mixture_feature_frames(mixid)

            if truth_t is None:
                truth_t = np.zeros((self.mixture_samples(mixid), self.num_classes), dtype=np.float32)

            feature = np.empty((feature_frames, self.fg.stride, self.fg.num_bands), dtype=np.float32)
            truth_f = np.empty((feature_frames, self.num_classes), dtype=np.complex64)

            feature_frame = 0
            for transform_frame in range(transform_frames):
                indices = slice(transform_frame * self.ft_config.R,
                                (transform_frame + 1) * self.ft_config.R)
                self.fg.execute(mixture_f[transform_frame],
                                truth_reduction(truth_t[indices], self.truth_reduction_function))

                if self.fg.eof():
                    feature[feature_frame] = self.fg.feature()
                    truth_f[feature_frame] = self.fg.truth()
                    feature_frame += 1

            if np.isreal(truth_f).all():
                truth_f = np.float32(np.real(truth_f))

            return feature, truth_f

        def mixture_feature(self,
                            mixid: int,
                            targets: AudiosT = None,
                            noise: AudioT = None,
                            mixture: AudioT = None,
                            truth_t: Truth = None,
                            force: bool = False) -> Feature:
            """Get the feature data for the given mixid

            :param mixid: Mixture ID
            :param targets: List of augmented target audio data (one per target in the mixup) for the given mixid
            :param noise: Augmented noise audio data for the given mixid
            :param mixture: Mixture audio data for the given mixid
            :param truth_t: truth_t for the given mixid
            :param force: Force computing data from original sources regardless of whether or not cached data exists
            :return: Feature data
            """
            feature, _ = self.mixture_ft(mixid=mixid,
                                         targets=targets,
                                         noise=noise,
                                         mixture=mixture,
                                         truth_t=truth_t,
                                         force=force)
            return feature

        def mixture_truth_f(self,
                            mixid: int,
                            targets: AudiosT = None,
                            noise: AudioT = None,
                            mixture: AudioT = None,
                            truth_t: Truth = None,
                            force: bool = False) -> Truth:
            """Get the truth_f data for the given mixid

            :param mixid: Mixture ID
            :param targets: List of augmented target audio data (one per target in the mixup) for the given mixid
            :param noise: Augmented noise audio data for the given mixid
            :param mixture: Mixture audio data for the given mixid
            :param truth_t: truth_t for the given mixid
            :param force: Force computing data from original sources regardless of whether or not cached data exists
            :return: truth_f data
            """
            _, truth_f = self.mixture_ft(mixid=mixid,
                                         targets=targets,
                                         noise=noise,
                                         mixture=mixture,
                                         truth_t=truth_t,
                                         force=force)
            return truth_f

    def mixture_class_count(self,
                            mixid: int,
                            targets: AudiosT = None,
                            noise: AudioT = None,
                            truth_t: Truth = None) -> ClassCount:
        """Compute the number of samples for which each truth index is active for the given mixid

        :param mixid: Mixture ID
        :param targets: List of augmented target audio (one per target in the mixup) for the given mixid
        :param noise: Augmented noise audio for the given mixid
        :param truth_t: truth_t for the given mixid
        :return: List of class counts
        """
        if truth_t is None:
            truth_t = self.mixture_truth_t(mixid=mixid, targets=targets, noise=noise)

        class_count = [0] * self.num_classes
        num_classes = self.num_classes
        if self.truth_mutex:
            num_classes -= 1
        for cl in range(num_classes):
            class_count[cl] = int(np.sum(truth_t[:, cl] >= self.class_weights_threshold[cl]))

        return class_count


def get_mrecords_from_mixids(mixdb: MixtureDatabase, mixids: GeneralizedIDs = None) -> MRecords:
    """Get a list of MRecords for the given mixture IDs

    :param mixdb: Mixture database
    :param mixids: Mixture IDs
    :return: MRecords
    """
    from copy import deepcopy

    return [deepcopy(mixdb.mixtures[i]) for i in mixdb.mixids_to_list(mixids)]


def _augment_noise_audio(audio: AudioT) -> AudiosT:
    from sonusai.mixture import apply_augmentation
    from sonusai.mixture import apply_ir

    results = []
    for augmentation in MP_GLOBAL.noise_augmentations:
        result = apply_augmentation(audio, augmentation)
        if augmentation.ir is not None:
            result = apply_ir(result, MP_GLOBAL.ir_data[augmentation.ir])
        results.append(result)

    return results


def generic_ids_to_list(num_ids: int, ids: GeneralizedIDs = None) -> List[int]:
    """Resolve generalized IDs to a list of integers

    :param num_ids: Total number of indices
    :param ids: Generalized  IDs
    :return: List of ID integers
    """
    from sonusai import SonusAIError

    all_ids = list(range(num_ids))

    if ids is None:
        return all_ids

    if isinstance(ids, str):
        if ids == '*':
            return all_ids

        try:
            result = eval(f'{all_ids}[{ids}]')
            if not isinstance(result, list):
                result = [result]
            return result
        except NameError:
            raise SonusAIError(f'Empty ids {ids}')

    if isinstance(ids, range):
        result = list(ids)
    elif isinstance(ids, int):
        result = [ids]
    else:
        result = ids

    if not all(isinstance(x, int) and 0 <= x < num_ids for x in result):
        raise SonusAIError(f'Invalid entries in ids of {ids}')

    if not result:
        raise SonusAIError(f'Empty ids {ids}')

    return result
