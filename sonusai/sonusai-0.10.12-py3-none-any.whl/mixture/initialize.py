import numpy as np

from sonusai.mixture.mixdb import MRecord
from sonusai.mixture.mixdb import MixtureDatabase
from sonusai.mixture.types import AudioT
from sonusai.mixture.types import AudiosT
from sonusai.mixture.types import GenMixData


def _initialize_target_audio(mixdb: MixtureDatabase,
                             mrecord: MRecord,
                             raw_target_audios: AudiosT) -> AudiosT:
    """ Apply augmentation and update target metadata
    """
    from sonusai.mixture import pad_audio_to_length
    from sonusai.mixture.augmentation import apply_augmentation

    targets = []
    mrecord.target_gain = []
    for idx in range(len(raw_target_audios)):
        target_augmentation = mixdb.target_augmentations[mrecord.target_augmentation_index[idx]]

        targets.append(apply_augmentation(audio=raw_target_audios[idx],
                                          augmentation=target_augmentation,
                                          length_common_denominator=mixdb.feature_step_samples))

        # target_gain is used to back out the gain augmentation in order to return the target audio
        # to its normalized level when calculating truth (if needed).
        if target_augmentation.gain is not None:
            target_gain = 10 ** (target_augmentation.gain / 20)
        else:
            target_gain = 1
        mrecord.target_gain.append(target_gain)

    mrecord.samples = max([len(item) for item in targets])

    for idx in range(len(targets)):
        targets[idx] = pad_audio_to_length(audio=targets[idx], length=mrecord.samples)

    return targets


def initialize_target(mixdb: MixtureDatabase,
                      mrecord: MRecord,
                      raw_target_audios: AudiosT) -> MRecord:
    """ Apply augmentation and update target metadata
    """
    _initialize_target_audio(mixdb, mrecord, raw_target_audios)
    return mrecord


def _initialize_mixture_gains(mrecord: MRecord,
                              target_audios: AudiosT,
                              noise_audio: AudioT) -> MRecord:
    from sonusai.utils import dbfs_to_sample

    target_audio = np.float32(sum(target_audios))

    if mrecord.snr < -96:
        # Special case for zeroing out target data
        mrecord.target_snr_gain = 0
        mrecord.noise_snr_gain = 1
        # Setting target_gain to zero will cause the truth to be all zeros.
        mrecord.target_gain = [0] * len(mrecord.target_gain)
    elif mrecord.snr > 96:
        # Special case for zeroing out noise data
        mrecord.target_snr_gain = 1
        mrecord.noise_snr_gain = 0
    else:
        target_energy = np.mean(np.square(target_audio))
        noise_energy = np.mean(np.square(np.float32(noise_audio)))
        if noise_energy == 0:
            noise_gain = 1
        else:
            noise_gain = np.sqrt(target_energy / noise_energy) / 10 ** (mrecord.snr / 20)

        # Check for noise_gain > 1 to avoid clipping
        if noise_gain > 1:
            mrecord.target_snr_gain = 1 / noise_gain
            mrecord.noise_snr_gain = 1
        else:
            mrecord.target_snr_gain = 1
            mrecord.noise_snr_gain = noise_gain

    # Check for clipping in mixture
    gain_adjusted_target_audio = target_audio * mrecord.target_snr_gain
    gain_adjusted_noise_audio = np.float32(noise_audio) * mrecord.noise_snr_gain
    mixture_audio = gain_adjusted_target_audio + gain_adjusted_noise_audio
    if any(abs(mixture_audio) >= 32768):
        # Clipping occurred; lower gains to bring audio within int16 bounds
        gain_adjustment = dbfs_to_sample(-0.25) / max(abs(mixture_audio))
        mrecord.target_snr_gain *= gain_adjustment
        mrecord.noise_snr_gain *= gain_adjustment

    return mrecord


def initialize_mixture(mixdb: MixtureDatabase,
                       mrecord: MRecord,
                       raw_target_audios: AudiosT,
                       noise_audio: AudioT) -> (MRecord, GenMixData):
    from sonusai.mixture import apply_gain
    from sonusai.mixture import apply_ir
    from sonusai.mixture import get_next_noise

    targets = _initialize_target_audio(mixdb=mixdb, mrecord=mrecord, raw_target_audios=raw_target_audios)
    noise = get_next_noise(audio=noise_audio, offset=mrecord.noise_offset, length=mrecord.samples)
    mrecord = _initialize_mixture_gains(mrecord=mrecord, target_audios=targets, noise_audio=noise)
    targets = [apply_gain(audio=target, gain=mrecord.target_snr_gain) for target in targets]
    noise = apply_gain(audio=noise, gain=mrecord.noise_snr_gain)

    # Apply impulse response to targets
    targets_ir = []
    for idx, target in enumerate(targets):
        ir_idx = mixdb.target_augmentations[mrecord.target_augmentation_index[idx]].ir
        if ir_idx is not None:
            targets_ir.append(apply_ir(audio=target, ir=mixdb.ir_data[ir_idx]))
        else:
            targets_ir.append(target)

    mixture = sum(targets_ir) + noise

    return mrecord, GenMixData(mixture=mixture, targets=targets, noise=noise)
