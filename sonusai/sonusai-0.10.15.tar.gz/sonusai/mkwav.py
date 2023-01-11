"""sonusai mkwav

usage: mkwav [-hvtn] [-i MIXID] LOC

options:
    -h, --help
    -v, --verbose                   Be verbose.
    -i MIXID, --mixid MIXID         Mixture ID(s) to generate. [default: *].
    -t, --target                    Write target file.
    -n, --noise                     Write noise file.

The mkwav command creates WAV files from a SonusAI database.

Inputs:
    LOC         A SonusAI mixture database directory.
    MIXID       A glob of mixture ID(s) to generate.

Outputs the following to the mixture database directory:
    <id>_mixture.wav:   mixture
    <id>_target.wav:    target (optional)
    <id>_noise.wav:     noise (optional)
    <id>.txt
    mkwav.log

"""
from dataclasses import dataclass

from sonusai import logger
from sonusai.mixture import AudioT
from sonusai.mixture import MixtureDatabase


# NOTE: global object is required for run-time performance; using 'partial' is much slower.
@dataclass
class MPGlobal:
    mixdb: MixtureDatabase = None
    write_target: bool = None
    write_noise: bool = None


MP_GLOBAL = MPGlobal()


def mkwav(mixdb: MixtureDatabase, mixid: int) -> (AudioT, AudioT, AudioT):
    from sonusai.genmix import genmix

    data = genmix(mixdb=mixdb, mixids=mixid, force=False)

    return data[0].mixture, sum(data[0].targets), data[0].noise


def _process_mixture(mixid: int) -> None:
    from os.path import exists
    from os.path import join
    from os.path import splitext

    import h5py
    import numpy as np

    from sonusai.utils import float_to_int16
    from sonusai.utils import write_wav

    mixture_filename = join(MP_GLOBAL.mixdb.location, MP_GLOBAL.mixdb.mixtures[mixid].name)
    mixture_basename = splitext(mixture_filename)[0]

    target = None
    noise = None

    need_data = True
    if exists(mixture_filename + '.h5'):
        with h5py.File(mixture_filename, 'r') as f:
            if 'mixture' in f:
                need_data = False
            if MP_GLOBAL.write_target and 'targets' not in f:
                need_data = True
            if MP_GLOBAL.write_noise and 'noise' not in f:
                need_data = True

    if need_data:
        mixture, target, noise = mkwav(mixdb=MP_GLOBAL.mixdb, mixid=mixid)
    else:
        with h5py.File(mixture_filename, 'r') as f:
            mixture = np.array(f['mixture'])
            if MP_GLOBAL.write_target:
                target = sum(np.array(f['targets']))
            if MP_GLOBAL.write_noise:
                noise = np.array(f['noise'])

    write_wav(name=mixture_basename + '_mixture.wav', audio=float_to_int16(mixture))
    if MP_GLOBAL.write_target:
        write_wav(name=mixture_basename + '_target.wav', audio=float_to_int16(target))
    if MP_GLOBAL.write_noise:
        write_wav(name=mixture_basename + '_noise.wav', audio=float_to_int16(noise))

    with open(file=mixture_basename + '.txt', mode='w') as f:
        f.write(MP_GLOBAL.mixdb.mixture_metadata(mixid))


def main():
    import time
    from os.path import join

    from docopt import docopt
    from tqdm import tqdm

    import sonusai
    from sonusai import create_file_handler
    from sonusai import initial_log_messages
    from sonusai import update_console_handler
    from sonusai.mixture import MixtureDatabase
    from sonusai.utils import p_tqdm_map
    from sonusai.utils import human_readable_size
    from sonusai.utils import seconds_to_hms
    from sonusai.utils import trim_docstring

    args = docopt(trim_docstring(__doc__), version=sonusai.__version__, options_first=True)

    verbose = args['--verbose']
    mixid = args['--mixid']
    write_target = args['--target']
    write_noise = args['--noise']
    location = args['LOC']

    start_time = time.monotonic()

    create_file_handler(join(location, 'mkwav.log'))
    update_console_handler(verbose)
    initial_log_messages('mkwav')

    logger.info(f'Load mixture database from {location}')
    mixdb = MixtureDatabase(config=location, show_progress=True)
    mixid = mixdb.mixids_to_list(mixid)

    total_samples = mixdb.total_samples(mixid)
    duration = total_samples / sonusai.mixture.SAMPLE_RATE

    logger.info('')
    logger.info(f'Found {len(mixid):,} mixtures to process')
    logger.info(f'{total_samples:,} samples')

    mixdb.check_audio_files_exist()

    MP_GLOBAL.mixdb = mixdb
    MP_GLOBAL.write_target = write_target
    MP_GLOBAL.write_noise = write_noise

    progress = tqdm(total=len(mixid), desc='mkwav')
    p_tqdm_map(_process_mixture, mixid, progress=progress)
    progress.close()

    logger.info(f'Wrote {len(mixid)} mixtures to {location}')
    logger.info('')
    logger.info(f'Duration: {seconds_to_hms(seconds=duration)}')
    logger.info(f'mixture:  {human_readable_size(total_samples * 2, 1)}')
    if write_target:
        logger.info(f'target:   {human_readable_size(total_samples * 2, 1)}')
    if write_noise:
        logger.info(f'noise:    {human_readable_size(total_samples * 2, 1)}')

    end_time = time.monotonic()
    logger.info(f'Completed in {seconds_to_hms(seconds=end_time - start_time)}')
    logger.info('')


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        logger.info('Canceled due to keyboard interrupt')
        raise SystemExit(0)
