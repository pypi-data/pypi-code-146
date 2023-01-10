"""sonusai lsdb

usage: lsdb [-hta] [-i MIXID] [-c TID] LOC

Options:
    -h, --help
    -i MIXID, --mixid MIXID         Mixture ID(s) to analyze. [default: *].
    -c TID, --truth_index TID       Analyze mixtures that contain this truth index.
    -t, --targets                   List all target files.
    -a, --all_class_counts          List all class counts.

List mixture data information from a SonusAI mixture database.

Inputs:
    LOC     A SonusAI mixture database directory.

"""
import numpy as np

from sonusai import logger
from sonusai.mixture import GeneralizedIDs
from sonusai.mixture import MixtureDatabase


def lsdb(mixdb: MixtureDatabase,
         mixids: GeneralizedIDs = None,
         truth_index: int = None,
         list_targets: bool = False,
         all_class_counts: bool = False) -> None:
    import h5py

    from sonusai import SonusAIError
    from sonusai.mixture import calculate_snr_f_statistics
    from sonusai.mixture import SAMPLE_RATE
    from sonusai.mixture import get_truth_indices_for_target
    from sonusai.queries import get_mixids_from_truth_index
    from sonusai.utils import consolidate_range
    from sonusai.utils import print_mixture_details
    from sonusai.utils import seconds_to_hms

    desc_len = 24

    total_samples = mixdb.total_samples()
    total_duration = total_samples / SAMPLE_RATE

    logger.info(f'{"Mixtures":{desc_len}} {len(mixdb.mixtures)}')
    logger.info(f'{"Duration":{desc_len}} {seconds_to_hms(seconds=total_duration)}')
    logger.info(f'{"Targets":{desc_len}} {len(mixdb.targets)}')
    logger.info(f'{"Target augmentations":{desc_len}} {len(mixdb.target_augmentations)}')
    logger.info(f'{"Noise augmentations":{desc_len}} {len(mixdb.noise_augmentations)}')
    logger.info(f'{"Noises":{desc_len}} {len(mixdb.noises)}')
    logger.info(f'{"Feature":{desc_len}} {mixdb.feature}')
    logger.info(
        f'{"Feature shape":{desc_len}} {mixdb.fg.stride} x {mixdb.fg.num_bands} ({mixdb.fg.stride * mixdb.fg.num_bands} total params)')
    logger.info(f'{"Feature samples":{desc_len}} {mixdb.feature_samples} samples ({mixdb.feature_ms} ms)')
    logger.info(
        f'{"Feature step samples":{desc_len}} {mixdb.feature_step_samples} samples ({mixdb.feature_step_ms} ms)')
    logger.info(f'{"Feature overlap":{desc_len}} {mixdb.fg.step / mixdb.fg.stride} ({mixdb.feature_step_ms} ms)')
    logger.info(f'{"SNRs":{desc_len}} {mixdb.snrs}')
    logger.info(f'{"Random SNRs":{desc_len}} {mixdb.random_snrs}')
    logger.info(f'{"Classes":{desc_len}} {mixdb.num_classes}')
    logger.info(f'{"Truth mutex":{desc_len}} {mixdb.truth_mutex}')
    # TODO: fix class count
    logger.info(f'{"Class count":{desc_len}} not supported')
    # print_class_count(class_count=class_count, length=desc_len, print_fn=logger.info)
    # TODO: add class weight calculations here
    logger.info('')

    if list_targets:
        logger.info('Target details:')
        idx_len = int(np.ceil(np.log10(len(mixdb.targets))))
        for idx, target in enumerate(mixdb.targets):
            desc = f'  {idx:{idx_len}} Name'
            logger.info(f'{desc:{desc_len}} {target.name}')
            desc = f'  {idx:{idx_len}} Truth index'
            logger.info(f'{desc:{desc_len}} {get_truth_indices_for_target(target)}')
        logger.info('')

    if truth_index is not None:
        if 0 <= truth_index > mixdb.num_classes:
            raise SonusAIError(f'Given truth_index is outside valid range of 1-{mixdb.num_classes}')
        ids = get_mixids_from_truth_index(mixdb=mixdb, predicate=lambda x: x in [truth_index])[truth_index]
        logger.info(f'Mixtures with truth index {truth_index}: {ids}')
        logger.info('')

    mixids = mixdb.mixids_to_list(mixids)

    if len(mixids) == 1:
        print_mixture_details(mixdb=mixdb, mixid=mixids[0], desc_len=desc_len, print_fn=logger.info)
        if all_class_counts:
            # TODO: fix class count
            logger.info('All class count not supported')
            # print_class_count(class_count=class_count, length=desc_len, print_fn=logger.info, all_class_counts=True)
    else:
        logger.info(f'Calculating statistics from truth_f files for {len(mixids):,} mixtures'
                    f' ({consolidate_range(mixids)})')
        for mixid in mixids:
            with h5py.File(mixdb.mixture_filename(mixid), 'r') as f:
                if mixid == mixids[0]:
                    truth_f = np.array(f['truth_f'])
                else:
                    truth_f = np.concatenate((truth_f, np.array(f['truth_f'])))

        snr_mean, snr_std, snr_db_mean, snr_db_std = calculate_snr_f_statistics(truth_f)

        logger.info('Truth')
        logger.info(f'  {"mean":^8s}  {"std":^8s}  {"db_mean":^8s}  {"db_std":^8s}')
        for c in range(len(snr_mean)):
            logger.info(f'  {snr_mean[c]:8.2f}  {snr_std[c]:8.2f}  {snr_db_mean[c]:8.2f}  {snr_db_std[c]:8.2f}')


def main():
    from docopt import docopt

    import sonusai
    from sonusai import create_file_handler
    from sonusai import initial_log_messages
    from sonusai import update_console_handler
    from sonusai.utils import trim_docstring

    args = docopt(trim_docstring(__doc__), version=sonusai.__version__, options_first=True)

    mixid = args['--mixid']
    truth_index = args['--truth_index']
    list_targets = args['--targets']
    all_class_counts = args['--all_class_counts']
    location = args['LOC']

    if truth_index is not None:
        truth_index = int(truth_index)

    create_file_handler('lsdb.log')
    update_console_handler(False)
    initial_log_messages('lsdb')

    logger.info(f'Analyzing {location}')

    mixdb = MixtureDatabase(config=location, show_progress=True)
    lsdb(mixdb=mixdb,
         mixids=mixid,
         truth_index=truth_index,
         list_targets=list_targets,
         all_class_counts=all_class_counts)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        logger.info('Canceled due to keyboard interrupt')
        raise SystemExit(0)
