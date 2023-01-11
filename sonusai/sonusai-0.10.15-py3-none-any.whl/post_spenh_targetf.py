"""sonusai post_spenh_targetf

usage: post_spenh_targetf [-hv] (-m MODEL) (-w KMODEL) INPUT ...

options:
    -h, --help
    -v, --verbose                   Be verbose.
    -m MODEL, --model MODEL         Python model file.
    -w KMODEL, --weights KMODEL     Keras model weights file.

Run post-processing on speech enhancement targetf prediction data.

Inputs:
    MODEL       A SonusAI Python model file with build and/or hypermodel functions.
    KMODEL      A Keras model weights file (or model file with weights).
    INPUT       A single H5 file or a glob of H5 files

Outputs the following to post_spenh_targetf-<TIMESTAMP> directory:
    <name>.wav
    post_spenh_targetf.log

"""
from dataclasses import dataclass

from sonusai import logger


# NOTE: global object is required for run-time performance; using 'partial' is much slower.
@dataclass
class MPGlobal:
    N: int = None
    R: int = None
    ttype: str = None
    output_dir: str = None


MP_GLOBAL = MPGlobal()


def main():
    from docopt import docopt

    import sonusai
    from sonusai.utils import trim_docstring

    args = docopt(trim_docstring(__doc__), version=sonusai.__version__, options_first=True)

    verbose = args['--verbose']
    model_name = args['--model']
    weights_name = args['--weights']
    input_name = args['INPUT']

    import time
    from os import makedirs
    from os.path import basename
    from os.path import isfile
    from os.path import join
    from os.path import splitext

    import h5py
    from pyaaware import FeatureGenerator
    from tqdm import tqdm

    from sonusai import create_file_handler
    from sonusai import initial_log_messages
    from sonusai import logger
    from sonusai import update_console_handler
    from sonusai.utils import check_keras_overrides
    from sonusai.utils import create_ts_name
    from sonusai.utils import import_keras_model
    from sonusai.utils import p_tqdm_map
    from sonusai.utils import seconds_to_hms

    start_time = time.monotonic()

    model_base = basename(model_name)

    output_dir = create_ts_name('post_spenh_targetf')
    makedirs(output_dir, exist_ok=True)

    # Setup logging file
    create_file_handler(join(output_dir, 'post_spenh_targetf.log'))
    update_console_handler(verbose)
    initial_log_messages('post_spenh_targetf')

    # Import model definition file
    logger.info(f'Importing {model_base}')
    model = import_keras_model(model_name)
    feature_mode = None
    with h5py.File(weights_name, 'r') as f:
        if 'sonusai_feature' in f.attrs:
            feature_mode = f.attrs['sonusai_feature']
        else:
            logger.warn(f'Could not find SonusAI feature in weights file; using hypermodel default.')
        if 'sonusai_num_classes' in f.attrs:
            num_classes = int(f.attrs['sonusai_num_classes'])
        else:
            logger.warn(f'Could not find SonusAI num_classes in weights file; using hypermodel default.')

    # Check overrides
    check_keras_overrides(model, feature_mode, num_classes, None, None)

    logger.info('Building model')
    try:
        hypermodel = model.MyHyperModel(feature=feature_mode,
                                        num_classes=num_classes)
    except Exception as e:
        logger.exception(f'build_model() in {model_base} failed: {e}.')
        raise SystemExit(1)

    fg = FeatureGenerator(feature_mode=hypermodel.feature,
                          num_classes=hypermodel.num_classes,
                          truth_mutex=hypermodel.truth_mutex)

    MP_GLOBAL.N = fg.itransform_N
    MP_GLOBAL.R = fg.itransform_R
    MP_GLOBAL.ttype = fg.itransform_ttype
    MP_GLOBAL.output_dir = output_dir

    if not all(isfile(file) and splitext(file)[1] == '.h5' for file in input_name):
        logger.exception(f'Do not know how to process input from {input_name}')
        raise SystemExit(1)

    logger.info('')
    logger.info(f'Found {len(input_name):,} files to process')

    progress = tqdm(total=len(input_name), desc='post_spenh_targetf')
    p_tqdm_map(_process, input_name, progress=progress)
    progress.close()

    logger.info(f'Wrote {len(input_name)} mixtures to {output_dir}')
    logger.info('')

    end_time = time.monotonic()
    logger.info(f'Completed in {seconds_to_hms(seconds=end_time - start_time)}')
    logger.info('')


def _process(file: str) -> None:
    """Run extraction on predict data to generate estimation audio
    """
    from os.path import basename
    from os.path import join
    from os.path import splitext

    import h5py
    import numpy as np
    from pyaaware import InverseTransform

    from sonusai import SonusAIError
    from sonusai.mixture import calculate_audio_from_transform
    from sonusai.utils import float_to_int16
    from sonusai.utils import unstack_complex
    from sonusai.utils import write_wav

    try:
        with h5py.File(file, 'r') as f:
            predict = unstack_complex(np.array(f['predict']))
    except Exception as e:
        raise SonusAIError(f'Error reading {file}: {e}')

    output_name = join(MP_GLOBAL.output_dir, splitext(basename(file))[0] + '.wav')
    audio = calculate_audio_from_transform(data=predict,
                                           transform=InverseTransform(N=MP_GLOBAL.N,
                                                                      R=MP_GLOBAL.R,
                                                                      ttype=MP_GLOBAL.ttype))
    write_wav(name=output_name, audio=float_to_int16(audio))


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        logger.info('Canceled due to keyboard interrupt')
        exit()
