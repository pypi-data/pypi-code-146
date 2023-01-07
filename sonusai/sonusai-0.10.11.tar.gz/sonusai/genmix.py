"""sonusai genmix

usage: genmix [-hvgts] [-i MIXID] LOC

options:
    -h, --help
    -v, --verbose                   Be verbose.
    -i MIXID, --mixid MIXID         Mixture ID(s) to generate. [default: *].
    -g, --target                    Save target. [default: False].
    -t, --truth                     Save truth_t. [default: False].
    -s, --segsnr                    Save segsnr_t. [default: False].

Generate SonusAI mixture data from a SonusAI mixture database.

Inputs:
    LOC         A SonusAI mixture database directory.
    MIXID       A glob of mixture ID(s) to generate.

Outputs the following to the mixture database directory:
    <id>.h5:
        dataset:    mixture
        dataset:    targets
        dataset:    noise
        dataset:    target (optional)
        dataset:    truth_t (optional)
        dataset:    segsnr_t (optional)
    <id>.txt
    genmix.log
"""
from dataclasses import dataclass
from typing import List

from sonusai import logger
from sonusai.mixture import GenMixData
from sonusai.mixture import GeneralizedIDs
from sonusai.mixture import MixtureDatabase


# NOTE: global object is required for run-time performance; using 'partial' is much slower.
@dataclass
class MPGlobal:
    mixdb: MixtureDatabase = None
    save_target: bool = None
    compute_truth: bool = None
    compute_segsnr: bool = None
    force: bool = None
    write: bool = None


MP_GLOBAL = MPGlobal()


def genmix(mixdb: MixtureDatabase,
           mixids: GeneralizedIDs = None,
           save_target: bool = False,
           compute_truth: bool = False,
           compute_segsnr: bool = False,
           write: bool = False,
           show_progress: bool = False,
           force: bool = True) -> List[GenMixData]:
    import multiprocessing as mp

    from tqdm import tqdm

    from sonusai.utils import p_tqdm_map

    MP_GLOBAL.mixdb = mixdb
    MP_GLOBAL.save_target = save_target
    MP_GLOBAL.compute_truth = compute_truth
    MP_GLOBAL.compute_segsnr = compute_segsnr
    MP_GLOBAL.force = force
    MP_GLOBAL.write = write

    mixids = mixdb.mixids_to_list(mixids)
    if mp.current_process().daemon:
        results = []
        for mixid in mixids:
            results.append(_genmix_kernel(mixid))
    else:
        progress = tqdm(total=len(mixids), desc='genmix', disable=not show_progress)
        results = p_tqdm_map(_genmix_kernel, mixids, progress=progress)
        progress.close()

    return results


def _genmix_kernel(mixid: int) -> GenMixData:
    targets = MP_GLOBAL.mixdb.mixture_targets(mixid=mixid, force=MP_GLOBAL.force)
    noise = MP_GLOBAL.mixdb.mixture_noise(mixid=mixid, force=MP_GLOBAL.force)
    write_data = [('targets', targets), ('noise', noise)]

    if MP_GLOBAL.compute_truth:
        truth_t = MP_GLOBAL.mixdb.mixture_truth_t(mixid=mixid, targets=targets, noise=noise, force=MP_GLOBAL.force)
        write_data.append(('truth_t', truth_t))
    else:
        truth_t = None

    target = MP_GLOBAL.mixdb.mixture_target(mixid=mixid, targets=targets)
    if MP_GLOBAL.save_target:
        write_data.append(('target', target))

    if MP_GLOBAL.compute_segsnr:
        segsnr_t = MP_GLOBAL.mixdb.mixture_segsnr_t(mixid=mixid,
                                                    targets=targets,
                                                    target=target,
                                                    noise=noise,
                                                    force=MP_GLOBAL.force)
        write_data.append(('segsnr_t', segsnr_t))
    else:
        segsnr_t = None

    mixture = MP_GLOBAL.mixdb.mixture_mixture(mixid=mixid,
                                              targets=targets,
                                              target=target,
                                              noise=noise,
                                              force=MP_GLOBAL.force)
    write_data.append(('mixture', mixture))

    if MP_GLOBAL.write:
        MP_GLOBAL.mixdb.write_mixture_data(mixid, write_data)
        MP_GLOBAL.mixdb.write_mixture_metadata(mixid)

    return GenMixData(targets=targets,
                      noise=noise,
                      mixture=mixture,
                      truth_t=truth_t,
                      segsnr_t=segsnr_t)


def main():
    from docopt import docopt

    import sonusai
    from sonusai.utils import trim_docstring

    args = docopt(trim_docstring(__doc__), version=sonusai.__version__, options_first=True)

    import time
    from os.path import join

    from sonusai import create_file_handler
    from sonusai import initial_log_messages
    from sonusai import logger
    from sonusai import update_console_handler
    from sonusai.mixture import MixtureDatabase
    from sonusai.mixture import MixtureDatabase
    from sonusai.utils import human_readable_size
    from sonusai.utils import seconds_to_hms

    verbose = args['--verbose']
    location = args['LOC']
    mixids = args['--mixid']
    save_target = args['--target']
    compute_truth = args['--truth']
    compute_segsnr = args['--segsnr']

    start_time = time.monotonic()

    create_file_handler(join(location, 'genmix.log'))
    update_console_handler(verbose)
    initial_log_messages('genmix')

    logger.info(f'Load mixture database from {location}')
    mixdb = MixtureDatabase(config=location, show_progress=True)
    mixids = mixdb.mixids_to_list(mixids)

    total_samples = mixdb.total_samples(mixids)
    duration = total_samples / sonusai.mixture.SAMPLE_RATE

    logger.info('')
    logger.info(f'Found {len(mixids):,} mixtures to process')
    logger.info(f'{total_samples:,} samples')

    mixdb.check_audio_files_exist()

    genmix(mixdb=mixdb,
           mixids=mixids,
           save_target=save_target,
           compute_truth=compute_truth,
           compute_segsnr=compute_segsnr,
           write=True,
           show_progress=True)

    logger.info(f'Wrote {len(mixids)} mixtures to {location}')
    logger.info('')
    logger.info(f'Duration: {seconds_to_hms(seconds=duration)}')
    logger.info(f'mixture:  {human_readable_size(total_samples * 2, 1)}')
    if compute_truth:
        logger.info(f'truth_t:  {human_readable_size(total_samples * mixdb.num_classes * 4, 1)}')
    logger.info(f'target:   {human_readable_size(total_samples * 2, 1)}')
    logger.info(f'noise:    {human_readable_size(total_samples * 2, 1)}')
    if compute_segsnr:
        logger.info(f'segsnr:   {human_readable_size(total_samples * 4, 1)}')

    end_time = time.monotonic()
    logger.info(f'Completed in {seconds_to_hms(seconds=end_time - start_time)}')
    logger.info('')


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        logger.info('Canceled due to keyboard interrupt')
        raise SystemExit(0)
