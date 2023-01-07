from typing import List

import numpy as np

from sonusai.mixture.mixdb import MixtureDatabase
from sonusai.mixture.types import AudioT
from sonusai.mixture.types import Truth
from sonusai.mixture.types import TruthFunctionConfig


def _strictly_decreasing(list_to_check: list) -> bool:
    return all(x > y for x, y in zip(list_to_check, list_to_check[1:]))


def truth_function(target_audio: AudioT, noise_audio: AudioT, config: TruthFunctionConfig) -> Truth:
    import h5py
    from pyaaware import FeatureGenerator
    from pyaaware import ForwardTransform
    from pyaaware import SED

    from sonusai import SonusAIError
    from sonusai.mixture import calculate_mapped_snr_f

    fg = FeatureGenerator(feature_mode=config.feature, num_classes=config.num_classes, truth_mutex=config.mutex)
    frame_size = fg.ftransform_R
    truth = np.zeros((len(target_audio), config.num_classes), dtype=np.float32)
    offsets = range(0, len(target_audio), frame_size)
    zero_based_indices = [x - 1 for x in config.index]
    target_fft = ForwardTransform(N=fg.ftransform_N, R=fg.ftransform_R, ttype=fg.ftransform_ttype)
    noise_fft = ForwardTransform(N=fg.ftransform_N, R=fg.ftransform_R, ttype=fg.ftransform_ttype)

    if config.function == 'sed':
        if len(target_audio) % frame_size != 0:
            raise SonusAIError(f'Number of samples in audio is not a multiple of {frame_size}')

        if config.config is None:
            raise SonusAIError('Truth function SED missing config')

        parameters = ['thresholds']
        for parameter in parameters:
            if parameter not in config.config:
                raise SonusAIError(f'Truth function SED config missing required parameter: {parameter}')

        thresholds = config.config['thresholds']
        if not _strictly_decreasing(thresholds):
            raise SonusAIError(f'Truth function SED thresholds are not strictly decreasing: {thresholds}')

        if config.target_gain == 0:
            return truth

        # SED wants 1-based indices
        sed = SED(thresholds=thresholds,
                  index=config.index,
                  frame_size=frame_size,
                  num_classes=config.num_classes,
                  mutex=config.mutex)

        target_audio = target_audio / config.target_gain
        for offset in offsets:
            indices = slice(offset, offset + frame_size)
            new_truth = sed.execute(target_fft.energy_t(target_audio[indices]))
            truth[indices] = np.reshape(new_truth, (1, len(new_truth)))

        return truth

    if config.function == 'file':
        if config.config is None:
            raise SonusAIError('Truth function file missing config')

        parameters = ['file']
        for parameter in parameters:
            if parameter not in config.config:
                raise SonusAIError(f'Truth function file config missing required parameter: {parameter}')

        with h5py.File(config.config['file'], 'r') as f:
            truth_in = np.array(f['truth_t'])

        if truth_in.ndim != 2:
            raise SonusAIError('Truth file data is not 2 dimensions')

        if truth_in.shape[0] != len(target_audio):
            raise SonusAIError('Truth file does not contain the right amount of samples')

        if config.target_gain == 0:
            return truth

        if len(zero_based_indices) > 1:
            if len(zero_based_indices) != truth_in.shape[1]:
                raise SonusAIError('Truth file does not contain the right amount of classes')

            truth[:, zero_based_indices] = truth_in
        else:
            index = zero_based_indices[0]
            if index + truth_in.shape[1] > config.num_classes:
                raise SonusAIError('Truth file contains too many classes')

            truth[:, index:index + truth_in.shape[1]] = truth_in

        return truth

    if config.function == 'energy_t':
        if config.target_gain == 0:
            return truth

        for offset in offsets:
            target_energy = target_fft.energy_t(target_audio[offset:offset + frame_size])
            truth[offset:offset + frame_size, zero_based_indices] = np.float32(target_energy)

        return truth

    if config.function == 'target_f':
        if config.num_classes != 2 * target_fft.bins:
            raise SonusAIError(f'Invalid num_classes for target_f truth: {config.num_classes}')

        truth = np.zeros((len(target_audio), config.num_classes), dtype=np.float32)
        if config.target_gain == 0:
            return truth

        for offset in offsets:
            target_f = np.complex64(target_fft.execute(target_audio[offset:offset + frame_size]))

            indices = slice(offset, offset + frame_size)
            for index in zero_based_indices:
                start = index
                stop = start + target_fft.bins
                truth[indices, start:stop] = np.real(target_f)

                start = stop
                stop = start + target_fft.bins
                truth[indices, start:stop] = np.imag(target_f)

        return truth

    if config.function == 'target_mixture_f':
        if config.num_classes != 2 * target_fft.bins + 2 * noise_fft.bins:
            raise SonusAIError(f'Invalid num_classes for target_mixture_f truth: {config.num_classes}')

        truth = np.zeros((len(target_audio), config.num_classes), dtype=np.float32)
        if config.target_gain == 0:
            return truth

        for offset in offsets:
            target_f = np.complex64(target_fft.execute(target_audio[offset:offset + frame_size]))
            noise_f = np.complex64(noise_fft.execute(noise_audio[offset:offset + frame_size]))
            mixture_f = target_f + noise_f

            indices = slice(offset, offset + frame_size)
            for index in zero_based_indices:
                start = index
                stop = start + target_fft.bins
                truth[indices, start:stop] = np.real(target_f)

                start = stop
                stop = start + target_fft.bins
                truth[indices, start:stop] = np.imag(target_f)

                start = stop
                stop = start + noise_fft.bins
                truth[indices, start:stop] = np.real(mixture_f)

                start = stop
                stop = start + noise_fft.bins
                truth[indices, start:stop] = np.imag(mixture_f)

        return truth

    if config.function == 'crm':
        if config.num_classes != target_fft.bins:
            raise SonusAIError(f'Invalid num_classes for crm truth: {config.num_classes}')

        if target_fft.bins != noise_fft.bins:
            raise SonusAIError('Transform size mismatch for crm truth')

        truth = np.zeros((len(target_audio), config.num_classes), dtype=np.float32)

        if config.target_gain == 0:
            return truth

        for offset in offsets:
            target_f = np.complex64(target_fft.execute(target_audio[offset:offset + frame_size]))
            noise_f = np.complex64(noise_fft.execute(noise_audio[offset:offset + frame_size]))
            mixture_f = target_f + noise_f

            crm = np.empty(target_f.shape, dtype=np.complex64)
            with np.nditer(target_f, flags=['multi_index'], op_flags=['readwrite']) as it:
                for _ in it:
                    num = target_f[it.multi_index]
                    den = mixture_f[it.multi_index]
                    if num == 0:
                        crm[it.multi_index] = 0
                    elif den == 0:
                        crm[it.multi_index] = complex(np.inf, np.inf)
                    else:
                        crm[it.multi_index] = num / den

            indices = slice(offset, offset + frame_size)
            for index in zero_based_indices:
                truth[indices, index:index + target_fft.bins] = np.real(crm)
                truth[indices, (index + target_fft.bins):(index + 2 * target_fft.bins)] = np.imag(crm)

        return truth

    if config.function in ['energy_f', 'snr_f', 'mapped_snr_f']:
        if config.target_gain == 0:
            return truth

        snr_db_mean = None
        snr_db_std = None
        if config.function == 'mapped_snr_f':
            if config.config is None:
                raise SonusAIError('Truth function mapped SNR missing config')

            parameters = ['snr_db_mean', 'snr_db_std']
            for parameter in parameters:
                if parameter not in config.config:
                    raise SonusAIError(f'Truth function mapped SNR config missing required parameter: {parameter}')

            snr_db_mean = config.config['snr_db_mean']
            if len(snr_db_mean) != target_fft.bins:
                raise SonusAIError(f'Truth function mapped SNR snr_db_mean does not have {target_fft.bins} elements')

            snr_db_std = config.config['snr_db_std']
            if len(snr_db_std) != target_fft.bins:
                raise SonusAIError(f'Truth function mapped SNR snr_db_std does not have {target_fft.bins} elements')

        for index in zero_based_indices:
            if index + target_fft.bins > config.num_classes:
                raise SonusAIError('Truth index exceeds the number of classes')

        for offset in offsets:
            target_energy = np.float32(
                target_fft.energy_f(target_audio[offset:offset + frame_size]))
            if config.function in ['snr_f', 'mapped_snr_f']:
                noise_energy = np.float32(noise_fft.energy_f(noise_audio[offset:offset + frame_size]))
            else:
                noise_energy = np.float32(1)

            indices = slice(offset, offset + frame_size)
            for index in zero_based_indices:
                old_err = np.seterr(divide='ignore', invalid='ignore')
                tmp = target_energy / noise_energy
                np.seterr(**old_err)

                tmp = np.nan_to_num(tmp, nan=-np.inf, posinf=np.inf, neginf=-np.inf)

                if config.function == 'mapped_snr_f':
                    tmp = calculate_mapped_snr_f(tmp, snr_db_mean, snr_db_std)

                truth[indices, index:index + target_fft.bins] = tmp

        return truth

    if config.function == 'phoneme':
        # Read in .txt transcript and run a Python function to generate text grid data
        # (indicating which phonemes are active)
        # Then generate truth based on this data and put in the correct classes based on config.index
        raise SonusAIError('Truth function phoneme is not supported yet')

    raise SonusAIError(f'Unsupported truth function: {config.function}')


def get_truth_indices_for_mixid(mixdb: MixtureDatabase, mixid: int) -> List[int]:
    """Get a list of truth indices for a given mixid."""

    from sonusai.mixture.targets import get_truth_indices_for_target

    indices = []
    for target_file_index in mixdb.mixtures[mixid].target_file_index:
        indices.append(*get_truth_indices_for_target(mixdb.targets[target_file_index]))

    return sorted(list(set(indices)))


def truth_reduction(x: Truth, func: str) -> Truth:
    from sonusai import SonusAIError

    if func == 'max':
        return np.max(x, axis=0)

    if func == 'mean':
        return np.mean(x, axis=0)

    raise SonusAIError(f'Invalid truth reduction function: {func}')
