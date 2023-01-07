"""sonusai genmixdb

usage: genmixdb [-hvmfs] LOC

options:
   -h, --help
   -v, --verbose    Be verbose.
   -m, --mix        Save mixture data. [default: False].
   -f, --ft         Save feature/truth_f data. [default: False].
   -s, --segsnr     Save segsnr data. [default: False].

Create mixture database data for training and evaluation. Optionally, also create mixture audio and feature/truth data.

genmixdb creates a database of training and evaluation feature and truth data generation information. It allows
the choice of audio neural-network feature types that are supported by the Aaware real-time front-end and truth
data that is synchronized frame-by-frame with the feature data.

Here are some examples:

#### Adding target data
Suppose you have an audio file which is an example, or target, of what you want to
recognize or detect. Of course, for training a NN you also need truth data for that
file (also called labels). If you don't already have it, genmixdb can create truth using
energy-based sound detection on each frame of the feature data. You can also select
different feature types. Here's an example:

genmixdb target_gfr32ts2

where target_gfr32ts2 contains config.yml with the following inside:
---
feature: gfr32ts2

targets:
  - name: data/target.wav

target_augmentations:
  - normalize: -3.5
...

The mixture database is written to a JSON file (mixdb.json) in the same directory that contains the config.yml file.

#### Target data mix with noise and augmentation

genmixdb mix_gfr32ts2.yml

where mix_gfr32ts2.yml contains:
---
feature: gfr32ts2

targets:
  - name: data/target.wav

target_augmentations:
  - normalize: -3.5
    pitch: [-3, 0, 3]
    tempo: [0.8, 1, 1.2]

noises:
  - name: data/noise.wav

noise_augmentations:
  - normalize: -3.5

snrs:
  - 20
...

In this example a time-domain mixture is created and feature data is calculated as
specified by 'feature: gfr32ts2'. Various feature types are available which vary in
spectral and temporal resolution (4 ms or higher), and other feature algorithm
parameters. The total feature size, dimension, and #frames for mixture is reported
in the log file (the log file name is genmixdb.log).

Truth (labels) can be automatically created per feature output frame based on sound
energy detection. By default, these are appended to the feature data in a single HDF5
output file. By default, truth/label generation is turned on with default algorithm
and threshold levels (see truth section) and a single class, i.e., detecting a single
type of sound. The truth format is a single float per class representing the
probability of activity/presence, and multi-class truth/labels are possible by
specifying the number of classes and either a scalar index or a vector of indices in
which to put the truth result. For example, 'num_class: 3' and  'truth_index: 2' adds
a 1x3 vector to the feature data with truth put in index 2 (others would be 0) for
data/target.wav being an audio clip from sound type of class 2.

The mixture is created with potential data augmentation functions in the following way:
1. apply noise augmentation rule
2. apply target augmentation rule
3. adjust noise gain for specific SNR
4. add augmented noise to augmented target

The mixture length is the target length by default, and the noise signal is repeated
if it is shorter, or trimmed if longer.

#### Target and noise using path lists

Target and noise audio is specified as a list containing text files, audio files, and
file globs. Text files are processed with items on each line where each item can be a
text file, an audio file, or a file glob. Each item will be searched for audio files
which can be WAV, MP3, FLAC, AIFF, or OGG format with any sample rate, bit depth, or
channel count. All audio files will be converted to 16 kHz, 16-bit, single channel
format before processing. For example,

genmixdb dog-bark.yml

where dog-bark.yml contains:
---
targets:
  - name: slib/dog-outside/*.wav
  - name: slib/dog-inside/*.wav

will find all .wav files in the specified directories and process them as targets.

"""
from dataclasses import dataclass
from typing import List

from sonusai import logger
from sonusai.mixture import AudiosT
from sonusai.mixture import AugmentedTargets
from sonusai.mixture import ListAudiosT
from sonusai.mixture import Location
from sonusai.mixture import MRecord
from sonusai.mixture import MixtureDatabase


# NOTE: global object is required for run-time performance; using 'partial' is much slower.
@dataclass
class MPGlobal:
    mixdb: MixtureDatabase = None
    save_mix: bool = None
    save_ft: bool = None
    save_segsnr: bool = None


MP_GLOBAL = MPGlobal()


def genmixdb(location: Location,
             save_mix: bool = False,
             save_ft: bool = False,
             save_segsnr: bool = False,
             logging: bool = True,
             show_progress: bool = False,
             test_mode: bool = False) -> MixtureDatabase:
    from random import seed

    import numpy as np
    import yaml
    from tqdm import tqdm

    import sonusai
    from sonusai import SonusAIError
    from sonusai import logger
    from sonusai.mixture import Augmentation
    from sonusai.mixture import MRecord
    from sonusai.mixture import MixtureDatabaseConfig
    from sonusai.mixture import SAMPLE_RATE
    from sonusai.mixture import TruthSettings
    from sonusai.mixture import balance_targets
    from sonusai.mixture import evaluate_random_rule
    from sonusai.mixture import generate_mixture_filename
    from sonusai.mixture import get_augmentation_indices_for_mixup
    from sonusai.mixture import get_augmentations
    from sonusai.mixture import get_augmented_target_indices_for_mixup
    from sonusai.mixture import get_augmented_targets
    from sonusai.mixture import get_class_weights_threshold
    from sonusai.mixture import get_ir_files
    from sonusai.mixture import get_mixups
    from sonusai.mixture import get_noise_files
    from sonusai.mixture import get_target_files
    from sonusai.mixture import load_config
    from sonusai.mixture import log_duration_and_sizes
    from sonusai.mixture import update_truth_settings
    from sonusai.utils import dataclass_from_dict
    from sonusai.utils import p_tqdm_map
    from sonusai.utils import seconds_to_hms

    config = load_config(location)

    seed(config['seed'])

    if logging:
        logger.debug(f'Seed: {config["seed"]}')
        logger.debug('Configuration:')
        logger.debug(yaml.dump(config))

    if logging:
        logger.info('Collecting targets')
    target_files = get_target_files(config)
    if len(target_files) == 0:
        raise SonusAIError('Canceled due to no targets')

    if logging:
        logger.debug('List of targets:')
        logger.debug(yaml.dump([target_file.name for target_file in target_files], default_flow_style=False))
        logger.debug('')

    if logging:
        logger.info('Collecting noises')
    noise_files = get_noise_files(config)
    if logging:
        logger.debug('List of noises:')
        logger.debug(yaml.dump([noise_file.name for noise_file in noise_files], default_flow_style=False))
        logger.debug('')

    if logging:
        logger.info('Collecting impulse responses')
    ir_files = get_ir_files(config)
    if logging:
        logger.debug('List of impulse responses:')
        logger.debug(yaml.dump([ir_file for ir_file in ir_files], default_flow_style=False))
        logger.debug('')

    if logging:
        logger.info('Collecting target augmentations')
    target_augmentations = get_augmentations(rules=config['target_augmentations'], num_ir=len(ir_files))
    mixups = get_mixups(target_augmentations)
    if logging:
        for mixup in mixups:
            logger.debug(f'Expanded list of target augmentations for mixup of {mixup}:')
            indices = get_augmentation_indices_for_mixup(target_augmentations, mixup)
            for idx in indices:
                logger.debug(f'- {target_augmentations[idx]}')
            logger.debug('')

    if logging:
        logger.info('Collecting noise augmentations')
    noise_augmentations = get_augmentations(rules=config['noise_augmentations'], num_ir=len(ir_files))
    if logging:
        logger.debug('Expanded list of noise augmentations:')
        for augmentation in noise_augmentations:
            logger.debug(f'- {augmentation}')
        logger.debug('')

    if logging:
        logger.debug(f'SNRs: {config["snrs"]}\n')
        logger.debug(f'Random SNRs: {config["random_snrs"]}\n')
        logger.debug(f'Exhaustive noise: {config["exhaustive_noise"]}\n')

    if config['truth_mode'] not in ['normal', 'mutex']:
        raise SonusAIError(f'invalid truth_mode: {config["truth_mode"]}')
    truth_mutex = config['truth_mode'] == 'mutex'

    if truth_mutex and any(mixup > 1 for mixup in mixups):
        raise SonusAIError(f'Mutex truth mode is not compatible with mixup')

    augmented_targets = get_augmented_targets(target_files, target_augmentations)

    mixdb = MixtureDatabase(
        config=MixtureDatabaseConfig(
            class_balancing=config['class_balancing'],
            class_balancing_augmentation=dataclass_from_dict(Augmentation, config['class_balancing_augmentation']),
            class_labels=config['class_labels'],
            class_weights_threshold=get_class_weights_threshold(config),
            exhaustive_noise=config['exhaustive_noise'],
            feature=config['feature'],
            first_cba_index=len(target_augmentations),
            ir_files=ir_files,
            mixtures=[],
            noise_augmentations=noise_augmentations,
            noises=noise_files,
            num_classes=config['num_classes'],
            random_snrs=config['random_snrs'],
            seed=config['seed'],
            snrs=config['snrs'],
            target_augmentations=target_augmentations,
            targets=target_files,
            truth_mutex=truth_mutex,
            truth_reduction_function=config['truth_reduction_function'],
            truth_settings=dataclass_from_dict(TruthSettings, update_truth_settings(config['truth_settings']))),
        show_progress=show_progress)
    mixdb.location = location

    raw_target_audio_samples = sum([len(x) for x in mixdb.raw_target_audios])
    if logging:
        logger.info('')
        logger.info(f'Raw target audio: {seconds_to_hms(seconds=raw_target_audio_samples / SAMPLE_RATE)}')

    noise_audio_samples = sum([len(xa) for x in mixdb.augmented_noise_audios for xa in x])
    if logging:
        logger.info(f'Augmented noise audio: {seconds_to_hms(seconds=noise_audio_samples / SAMPLE_RATE)}')

    augmented_targets = balance_targets(mixdb, augmented_targets)

    target_sets = 0
    total_duration = 0
    for mixup in mixups:
        augmented_target_indices_for_mixup = get_augmented_target_indices_for_mixup(
            mixdb=mixdb,
            augmented_targets=augmented_targets,
            mixup=mixup)
        target_sets += len(augmented_target_indices_for_mixup)
        for indices in augmented_target_indices_for_mixup:
            for augmented_target in [augmented_targets[idx] for idx in indices]:
                length = int(target_files[augmented_target.target_file_index].duration * sonusai.mixture.SAMPLE_RATE)
                augmentation = target_augmentations[augmented_target.target_augmentation_index]
                if augmentation.tempo is not None:
                    length /= augmentation.tempo
                if length % mixdb.feature_step_samples:
                    length += mixdb.feature_step_samples - int(length % mixdb.feature_step_samples)
                total_duration += float(length) / sonusai.mixture.SAMPLE_RATE

    total_snrs = len(mixdb.snrs) + len(mixdb.random_snrs)
    target_sets *= total_snrs
    total_duration *= total_snrs
    noise_sets = len(noise_files) * len(noise_augmentations) if mixdb.exhaustive_noise else 1
    total_duration *= noise_sets
    total_mixtures = noise_sets * target_sets
    mixid_padding = int(np.ceil(np.log10(total_mixtures)))
    if logging:
        logger.info('')
        logger.info(f'Found {total_mixtures:,} mixtures to process')

    if logging:
        log_duration_and_sizes(total_duration=total_duration,
                               num_classes=mixdb.num_classes,
                               feature_step_samples=mixdb.feature_step_samples,
                               num_bands=mixdb.fg.num_bands,
                               stride=mixdb.fg.stride,
                               desc='Estimated')
        logger.info(
            f'Feature shape:        {mixdb.fg.stride} x {mixdb.fg.num_bands} ({mixdb.fg.stride * mixdb.fg.num_bands} total params)')
        logger.info(f'Feature samples:      {mixdb.feature_samples} samples ({mixdb.feature_ms} ms)')
        logger.info(f'Feature step samples: {mixdb.feature_step_samples} samples ({mixdb.feature_step_ms} ms)')
        logger.info('')

    used_noise_samples = 0
    if mixdb.exhaustive_noise:
        # Get indices and offsets
        for noise_file_index in range(len(noise_files)):
            for noise_augmentation_index, noise_augmentation in enumerate(noise_augmentations):
                noise_offset = 0
                noise_length = len(mixdb.augmented_noise_audios[noise_file_index][noise_augmentation_index])

                for mixup in mixups:
                    augmented_target_indices_for_mixup = get_augmented_target_indices_for_mixup(
                        mixdb=mixdb,
                        augmented_targets=augmented_targets,
                        mixup=mixup)

                    for augmented_target_index_for_mixup in augmented_target_indices_for_mixup:
                        (target_file_index,
                         target_augmentation_index,
                         target_length) = _get_target_info(
                            mixdb=mixdb,
                            augmented_target_indices_for_mixup=augmented_target_index_for_mixup,
                            augmented_targets=augmented_targets,
                            raw_target_audios=mixdb.raw_target_audios)

                        for snr in mixdb.snrs:
                            mixdb.mixtures.append(MRecord(
                                name=generate_mixture_filename(len(mixdb.mixtures), mixid_padding),
                                target_file_index=target_file_index,
                                target_augmentation_index=target_augmentation_index,
                                noise_file_index=noise_file_index,
                                noise_offset=noise_offset,
                                noise_augmentation_index=noise_augmentation_index,
                                snr=snr,
                                random_snr=False))

                            noise_offset = int((noise_offset + target_length) % noise_length)
                            used_noise_samples += target_length

                        for random_snr in mixdb.random_snrs:
                            mixdb.mixtures.append(MRecord(
                                name=generate_mixture_filename(len(mixdb.mixtures), mixid_padding),
                                target_file_index=target_file_index,
                                target_augmentation_index=target_augmentation_index,
                                noise_file_index=noise_file_index,
                                noise_offset=noise_offset,
                                noise_augmentation_index=noise_augmentation_index,
                                snr=evaluate_random_rule(random_snr),
                                random_snr=True))

                            noise_offset = int((noise_offset + target_length) % noise_length)
                            used_noise_samples += target_length

    else:
        # Get indices and offsets
        noise_offset = 0
        noise_file_index = 0
        noise_augmentation_index = 0
        for mixup in mixups:
            augmented_target_indices_for_mixup = get_augmented_target_indices_for_mixup(
                mixdb=mixdb,
                augmented_targets=augmented_targets,
                mixup=mixup)
            for augmented_target_index_for_mixup in augmented_target_indices_for_mixup:
                (target_file_index,
                 target_augmentation_index,
                 target_length) = _get_target_info(
                    mixdb=mixdb,
                    augmented_target_indices_for_mixup=augmented_target_index_for_mixup,
                    augmented_targets=augmented_targets,
                    raw_target_audios=mixdb.raw_target_audios)

                for snr in mixdb.snrs:
                    (noise_file_index,
                     noise_augmentation_index,
                     noise_offset) = _get_next_noise_offset(target_length=target_length,
                                                            augmented_noise_audios=mixdb.augmented_noise_audios,
                                                            noise_file_index=noise_file_index,
                                                            noise_augmentation_index=noise_augmentation_index,
                                                            noise_offset=noise_offset)

                    mixdb.mixtures.append(MRecord(
                        name=generate_mixture_filename(len(mixdb.mixtures), mixid_padding),
                        target_file_index=target_file_index,
                        target_augmentation_index=target_augmentation_index,
                        noise_file_index=noise_file_index,
                        noise_augmentation_index=noise_augmentation_index,
                        noise_offset=noise_offset,
                        snr=snr,
                        random_snr=False))

                    noise_offset += target_length
                    used_noise_samples += target_length

                for random_snr in mixdb.random_snrs:
                    (noise_file_index,
                     noise_augmentation_index,
                     noise_offset) = _get_next_noise_offset(target_length=target_length,
                                                            augmented_noise_audios=mixdb.augmented_noise_audios,
                                                            noise_file_index=noise_file_index,
                                                            noise_augmentation_index=noise_augmentation_index,
                                                            noise_offset=noise_offset)

                    mixdb.mixtures.append(MRecord(
                        name=generate_mixture_filename(len(mixdb.mixtures), mixid_padding),
                        target_file_index=target_file_index,
                        target_augmentation_index=target_augmentation_index,
                        noise_file_index=noise_file_index,
                        noise_augmentation_index=noise_augmentation_index,
                        noise_offset=noise_offset,
                        snr=evaluate_random_rule(random_snr),
                        random_snr=True))

                    noise_offset += target_length
                    used_noise_samples += target_length

    # Fill in the details
    MP_GLOBAL.mixdb = mixdb
    MP_GLOBAL.save_mix = save_mix
    MP_GLOBAL.save_ft = save_ft
    MP_GLOBAL.save_segsnr = save_segsnr

    progress = tqdm(total=total_mixtures, desc='genmixdb', disable=not show_progress)
    mixdb.mixtures = p_tqdm_map(_process_mixture, range(total_mixtures), progress=progress)
    progress.close()

    total_samples = mixdb.total_samples()
    total_duration = total_samples / sonusai.mixture.SAMPLE_RATE
    if logging:
        log_duration_and_sizes(total_duration=total_duration,
                               num_classes=mixdb.num_classes,
                               feature_step_samples=mixdb.feature_step_samples,
                               num_bands=mixdb.fg.num_bands,
                               stride=mixdb.fg.stride,
                               desc='Actual')
        noise_samples_percent = (float(used_noise_samples) / float(noise_audio_samples)) * 100
        logger.info('')
        logger.info(f'Used {noise_samples_percent:,.0f}% of noise audio')
        logger.info('')

    if not test_mode:
        mixdb.save()
        logger.info(f'Wrote mixture database to {mixdb.location}')

    return mixdb


def _get_next_noise_offset(target_length: int,
                           augmented_noise_audios: ListAudiosT,
                           noise_file_index: int,
                           noise_augmentation_index: int,
                           noise_offset: int) -> (int, int, int):
    from sonusai import SonusAIError

    if noise_offset + target_length >= len(augmented_noise_audios[noise_file_index][noise_augmentation_index]):
        if noise_offset == 0:
            raise SonusAIError('Length of target audio exceeds length of noise audio')

        noise_offset = 0
        noise_augmentation_index += 1
        if noise_augmentation_index == len(augmented_noise_audios[noise_file_index]):
            noise_augmentation_index = 0
            noise_file_index += 1
            if noise_file_index == len(augmented_noise_audios):
                noise_file_index = 0

    return noise_file_index, noise_augmentation_index, noise_offset


def _get_target_info(mixdb: MixtureDatabase,
                     augmented_target_indices_for_mixup: List[int],
                     augmented_targets: AugmentedTargets,
                     raw_target_audios: AudiosT) -> (List[int], List[int], int):
    from sonusai.mixture import estimate_audio_length

    target_file_index = []
    target_augmentation_index = []
    target_length = 0
    for idx in augmented_target_indices_for_mixup:
        tfi = augmented_targets[idx].target_file_index
        tai = augmented_targets[idx].target_augmentation_index

        target_file_index.append(tfi)
        target_augmentation_index.append(tai)

        raw_target_audio = raw_target_audios[tfi]
        target_augmentation = mixdb.target_augmentations[tai]
        target_length = max(estimate_audio_length(audio=raw_target_audio,
                                                  augmentation=target_augmentation,
                                                  length_common_denominator=mixdb.feature_step_samples),
                            target_length)
    return target_file_index, target_augmentation_index, target_length


def _process_mixture(mixid: int) -> MRecord:
    from sonusai import SonusAIError
    from sonusai.mixture import initialize_mixture

    mrecord = MP_GLOBAL.mixdb.mixtures[mixid]
    if len(mrecord.target_file_index) != len(mrecord.target_augmentation_index):
        raise SonusAIError('target_file_index and target_augmentation_index are not the same length')

    raw_target_audios = [MP_GLOBAL.mixdb.raw_target_audios[mrecord.target_file_index[ti]] for ti in
                         range(len(mrecord.target_file_index))]
    noise_audio = MP_GLOBAL.mixdb.augmented_noise_audios[mrecord.noise_file_index][mrecord.noise_augmentation_index]

    mrecord, genmix_data = initialize_mixture(mixdb=MP_GLOBAL.mixdb,
                                              mrecord=mrecord,
                                              raw_target_audios=raw_target_audios,
                                              noise_audio=noise_audio)

    if MP_GLOBAL.save_mix or MP_GLOBAL.save_ft:
        write_data = []

        if MP_GLOBAL.save_mix:
            write_data.append(('targets', genmix_data.targets))
            write_data.append(('noise', genmix_data.noise))
            write_data.append(('mixture', genmix_data.mixture))

        if MP_GLOBAL.save_ft:
            truth_t = MP_GLOBAL.mixdb.mixture_truth_t(mixid=mixid,
                                                      targets=genmix_data.targets,
                                                      noise=genmix_data.noise)
            feature, truth_f = MP_GLOBAL.mixdb.mixture_ft(mixid=mixid,
                                                          mixture=genmix_data.mixture,
                                                          truth_t=truth_t)
            write_data.append(('feature', feature))
            write_data.append(('truth_f', truth_f))

            if MP_GLOBAL.save_segsnr:
                segsnr = MP_GLOBAL.mixdb.mixture_segsnr(mixid=mixid,
                                                        targets=genmix_data.targets,
                                                        noise=genmix_data.noise)
                write_data.append(('segsnr', segsnr))

        MP_GLOBAL.mixdb.write_mixture_data(mixid, write_data)
        MP_GLOBAL.mixdb.write_mixture_metadata(mixid)

    return mrecord


def main():
    from docopt import docopt

    import sonusai
    from sonusai.utils import trim_docstring

    args = docopt(trim_docstring(__doc__), version=sonusai.__version__, options_first=True)

    import time
    from os import makedirs
    from os import remove
    from os.path import exists
    from os.path import isdir
    from os.path import join

    from sonusai import create_file_handler
    from sonusai import initial_log_messages
    from sonusai import logger
    from sonusai import update_console_handler
    from sonusai.utils import seconds_to_hms

    verbose = args['--verbose']
    save_mix = args['--mix']
    save_ft = args['--ft']
    save_segsnr = args['--segsnr']
    location = args['LOC']

    start_time = time.monotonic()

    if exists(location) and not isdir(location):
        remove(location)

    makedirs(location, exist_ok=True)

    create_file_handler(join(location, 'genmixdb.log'))
    update_console_handler(verbose)
    initial_log_messages('genmixdb')

    logger.info(f'Creating mixture database for {location}')
    logger.info('')

    genmixdb(location=location,
             save_mix=save_mix,
             save_ft=save_ft,
             save_segsnr=save_segsnr,
             show_progress=True)

    end_time = time.monotonic()
    logger.info(f'Completed in {seconds_to_hms(seconds=end_time - start_time)}')
    logger.info('')


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        logger.info('Canceled due to keyboard interrupt')
        raise SystemExit(0)
