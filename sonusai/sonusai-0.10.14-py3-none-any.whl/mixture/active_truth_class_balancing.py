from dataclasses import dataclass
from typing import List

import numpy as np

from sonusai.mixture.mixdb import MRecord
from sonusai.mixture.mixdb import MRecords
from sonusai.mixture.mixdb import MixtureDatabase
from sonusai.mixture.types import AudiosT
from sonusai.mixture.types import GeneralizedIDs


# NOTE: global object is required for run-time performance; using 'partial' is much slower.
@dataclass
class MPGlobal:
    mixdb: MixtureDatabase = None
    raw_target_audios: AudiosT = None


MP_GLOBAL = MPGlobal()


def balance_active_truth(mixdb: MixtureDatabase,
                         raw_target_audios: AudiosT,
                         logging: bool = True,
                         show_progress: bool = False) -> MRecords:
    """ Add target augmentations until the class count values are balanced
    """
    from sonusai import logger
    from sonusai.mixture.constants import SAMPLE_RATE
    from sonusai.utils.seconds_to_hms import seconds_to_hms

    MP_GLOBAL.mixdb = mixdb
    MP_GLOBAL.raw_target_audios = raw_target_audios

    mixids = _get_augmented_targets_mixids(mixdb)
    class_balancing_samples = _get_class_balancing_samples(mixdb, mixids)
    if logging:
        logger.info('')
        label_digits = max([len(_get_class_label(mixdb, item)) for item in range(len(class_balancing_samples))])
        samples_digits = np.ceil(np.log10(float(max(class_balancing_samples))))
        samples_digits = int(samples_digits + np.ceil(samples_digits / 3))
        for class_index, required_samples in enumerate(class_balancing_samples):
            logger.info(f'Class {_get_class_label(mixdb, class_index):>{label_digits}} '
                        f'needs {required_samples:>{samples_digits},} more active truth samples '
                        f' - {seconds_to_hms(required_samples / SAMPLE_RATE)}')
        logger.info('')

    augmented_targets = [mixdb.mixtures[mixid] for mixid in mixids]
    for class_index, required_samples in enumerate(class_balancing_samples):
        augmented_targets = _balance_class(mixdb=mixdb,
                                           mrecords=augmented_targets,
                                           class_index=class_index,
                                           required_samples=required_samples,
                                           logging=logging,
                                           show_progress=show_progress)

    return augmented_targets


def _balance_class(mixdb: MixtureDatabase,
                   mrecords: MRecords,
                   class_index: int,
                   required_samples: int,
                   logging: bool = True,
                   show_progress: bool = False) -> MRecords:
    """ Add target augmentations for a single class until the required samples are satisfied
    """
    import multiprocessing as mp

    from tqdm import tqdm

    from sonusai import SonusAIError
    from sonusai import logger
    from sonusai.mixture.targets import get_target_indices_for_truth_index
    from sonusai.utils.parallel import p_map

    if required_samples == 0:
        return mrecords

    class_label = _get_class_label(mixdb, class_index)

    # Get list of targets for this class
    target_indices = get_target_indices_for_truth_index(mixdb.targets, class_index)
    if not target_indices:
        raise SonusAIError(f'Could not find single-class targets for class index {class_index}')

    num_cpus = mp.cpu_count()

    remaining_samples = required_samples
    added_samples = 0
    added_targets = 0
    progress = tqdm(total=required_samples, desc=f'Balance class {class_label}', disable=not show_progress)
    while True:
        new_mrecords: MRecords = []
        while len(new_mrecords) < num_cpus:
            for target_index in target_indices:
                augmentation_indices = _get_unused_balancing_augmentations(mixdb=mixdb,
                                                                           mrecords=mrecords,
                                                                           target_file_index=target_index,
                                                                           amount=num_cpus)
                for augmentation_index in augmentation_indices:
                    new_mrecords.append(MRecord(target_file_index=[target_index],
                                                target_augmentation_index=[augmentation_index]))

        new_mrecords = new_mrecords[0:num_cpus]
        new_mrecords = p_map(_process_target, new_mrecords)

        for mrecord in new_mrecords:
            # TODO: remove class_count
            new_samples = np.sum(np.sum(mrecord.class_count))
            remaining_samples -= new_samples

            # If the current mrecord will overshoot the required samples then add it only if
            # overshooting results in a sample count closer to the required than not overshooting.
            if remaining_samples >= 0 or -remaining_samples < remaining_samples + new_samples:
                mrecords.append(mrecord)
                added_samples += new_samples
                added_targets += 1
                progress.update(new_samples)

            if remaining_samples <= 0:
                _remove_unused_augmentations(mixdb=mixdb, mrecords=mrecords)
                progress.update(required_samples - added_samples)
                progress.close()
                if logging:
                    logger.info(f'Added {added_targets:,} new augmented targets for class {class_label}')
                return mrecords


def _process_target(mrecord: MRecord) -> MRecord:
    from sonusai.mixture.initialize import initialize_target

    return initialize_target(mrecord=mrecord, mixdb=MP_GLOBAL.mixdb,
                             raw_target_audios=MP_GLOBAL.raw_target_audios)


def _get_class_balancing_samples(mixdb: MixtureDatabase, mixids: GeneralizedIDs) -> List[int]:
    """ Determine the number of additional active truth samples needed for each class in order for
    all classes to be represented evenly over all mixtures.

    If the truth mode is mutually exclusive, ignore the last class (i.e., set to zero).
    """
    from sonusai.mixture.class_count import get_class_count_from_mixids

    class_count = get_class_count_from_mixids(mixdb, mixids)

    if mixdb.truth_mutex:
        class_count = class_count[:-1]

    result = list(np.max(class_count) - class_count)

    if mixdb.truth_mutex:
        result.append(0)

    return result


def _get_augmented_targets_mixids(mixdb: MixtureDatabase) -> GeneralizedIDs:
    """ Get a list of augmented target mixids from a mixture database
    """
    snr = max(mixdb.snrs)
    return [mixid for (mixid, mrecord) in enumerate(mixdb.mixtures) if
            mrecord.snr == snr and mrecord.noise_file_index == 0]


def _get_class_label(mixdb: MixtureDatabase, class_index: int) -> str:
    if mixdb.class_labels is not None:
        return mixdb.class_labels[class_index]

    return str(class_index)


def _get_unused_balancing_augmentations(mixdb: MixtureDatabase,
                                        mrecords: MRecords,
                                        target_file_index: int,
                                        amount: int = 1) -> List[int]:
    """ Get a list of unused balancing augmentations for a given target file index
    """
    from dataclasses import asdict

    from sonusai.mixture.augmentation import get_augmentations
    from sonusai.mixture.balance import get_class_balancing_augmentation

    balancing_augmentations = [item for item in range(len(mixdb.target_augmentations)) if
                               item >= mixdb.first_cba_index]
    used_balancing_augmentations = [mrecord.target_augmentation_index for mrecord in mrecords if
                                    mrecord.target_file_index == target_file_index and
                                    mrecord.target_augmentation_index in balancing_augmentations]

    augmentation_indices = [item for item in balancing_augmentations if item not in used_balancing_augmentations]
    class_balancing_augmentation = get_class_balancing_augmentation(mixdb=mixdb, target_file_index=target_file_index)

    while len(augmentation_indices) < amount:
        new_augmentation = get_augmentations(rules=asdict(class_balancing_augmentation),
                                             num_ir=len(mixdb.ir_files))[0]
        mixdb.target_augmentations.append(new_augmentation)
        augmentation_indices.append(len(mixdb.target_augmentations) - 1)

    return augmentation_indices


def _remove_unused_augmentations(mixdb: MixtureDatabase, mrecords: MRecords) -> None:
    """ Remove any unused target augmentation rules from the end of the database
    """
    max_used_augmentation = max([index for mixture in mrecords for index in mixture.target_augmentation_index]) + 1
    mixdb.target_augmentations = mixdb.target_augmentations[0:max_used_augmentation]
