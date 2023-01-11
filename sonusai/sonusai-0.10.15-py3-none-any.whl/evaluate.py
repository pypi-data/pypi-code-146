"""sonusai evaluate

usage: evaluate [-hv] [-i MIXID] (-f FEATURE) (-p PREDICT) [-t PTHR] LOC

options:
    -h, --help
    -v, --verbose                   Be verbose.
    -i MIXID, --mixid MIXID         Mixture ID(s) to generate. [default: *].
    -p PREDICT, --predict PREDICT   A directory containing prediction data.
    -t PTHR, --thr PTHR             Optional prediction decision threshold(s). [default: 0].

Evaluate calculates performance metrics of neural-network models from model prediction data and genft data.

Inputs:
    LOC         A SonusAI mixture database directory.
    MIXID       A glob of mixture ID(s) to generate.
    PREDICT     A directory containing SonusAI predict HDF5 files. Contains:
                    dataset:    predict (either [frames, num_classes] or [frames, timesteps, num_classes])
    PTHR        Scalar or array of thresholds. Default 0 will select values:
                    argmax()    if mixdb indicates single-label mode (truth_mutex = true)
                    0.5         if mixdb indicates multi-label mode  (truth_mutex = false)
                If PTHR = -1, optimal thresholds are calculated using precision_recall_curve() which
                optimizes F1 score.
"""
from typing import Union

import numpy as np

from sonusai import logger
from sonusai.mixture import Feature
from sonusai.mixture import Location
from sonusai.mixture import MixtureDatabase
from sonusai.mixture import Predict
from sonusai.mixture import Segsnr
from sonusai.mixture import Truth


def evaluate(mixdb: MixtureDatabase,
             truth: Truth,
             predict: Predict = None,
             segsnr: Segsnr = None,
             output_dir: Location = None,
             predict_thr: Union[float, np.ndarray] = 0.0,
             feature: Feature = None,
             verbose: bool = False) -> None:
    from os.path import join

    from sonusai import initial_log_messages
    from sonusai import update_console_handler
    from sonusai.metrics import calculate_optimal_thresholds
    from sonusai.metrics import class_summary
    from sonusai.metrics import snr_summary
    from sonusai.mixture import SAMPLE_RATE
    from sonusai.queries import get_mixids_from_snr
    from sonusai.utils import get_num_classes_from_predict
    from sonusai.utils import human_readable_size
    from sonusai.utils import reshape_outputs
    from sonusai.utils import seconds_to_hms

    update_console_handler(verbose)
    initial_log_messages('evaluate')

    if truth.shape[-1] != predict.shape[-1]:
        logger.exception(f'Number of classes in truth and predict are not equal. Exiting.')
        raise SystemExit(1)

    # truth, predict can be either [frames, num_classes] or [frames, timesteps, num_classes]
    # in binary case dim may not exist, detect this and set num_classes == 1
    timesteps = -1
    predict, truth = reshape_outputs(predict=predict, truth=truth, timesteps=timesteps)
    num_classes = get_num_classes_from_predict(predict=predict, timesteps=timesteps)

    fdiff = truth.shape[0] - predict.shape[0]
    if fdiff > 0:
        # truth = truth[0:-fdiff,:]
        predict = np.concatenate((predict, np.zeros((fdiff, num_classes))))
        logger.info(f'Truth has more feature-frames than predict, padding predict with zeros to match.')

    if fdiff < 0:
        predict = predict[0:fdiff, :]
        logger.info(f'Predict has more feature-frames than truth, trimming predict to match.')

    # Check segsnr, input is always in transform frames
    compute_segsnr = False
    if len(segsnr) > 0:
        segsnr_feature_frames = segsnr.shape[0] / (mixdb.feature_step_samples / mixdb.fg.ftransform_R)
        if segsnr_feature_frames == truth.shape[0]:
            compute_segsnr = True
        else:
            logger.warning('segsnr length does not match truth, ignoring.')

    # Check pred_thr array or scalar and return final scalar pred_thr value
    if not mixdb.truth_mutex:
        if num_classes > 1:
            if np.ndim(predict_thr) == 0 and predict_thr == 0:
                # multi-label pred_thr scalar 0 force to 0.5 default
                predict_thr = 0.5

            if np.ndim(predict_thr) == 1:
                if len(predict_thr) == 1:
                    if predict_thr[0] == 0:
                        # multi-label pred_thr array scalar 0 force to 0.5 default
                        predict_thr = 0.5
                    else:
                        # multi-label pred_thr array set to scalar = array[0]
                        predict_thr = predict_thr[0]

    else:
        # single-label mode, force argmax mode
        predict_thr = 0

    if predict_thr == -1:
        thrpr, thrroc, _, _ = calculate_optimal_thresholds(truth, predict, timesteps)
        predict_thr = np.atleast_1d(thrpr)
        predict_thr = np.maximum(predict_thr, 0.001)  # enforce lower limit
        predict_thr = np.minimum(predict_thr, 0.999)  # enforce upper limit
        predict_thr = predict_thr.round(2)

    # Summarize the mixture data
    num_mixtures = len(mixdb.mixtures)
    total_samples = sum([mixture.samples for mixture in mixdb.mixtures])
    duration = total_samples / SAMPLE_RATE

    logger.info('')
    logger.info(f'Mixtures: {num_mixtures}')
    logger.info(f'Duration: {seconds_to_hms(seconds=duration)}')
    logger.info(f'truth:    {human_readable_size(truth.nbytes, 1)}')
    logger.info(f'predict:  {human_readable_size(predict.nbytes, 1)}')
    if compute_segsnr:
        logger.info(f'segsnr:   {human_readable_size(segsnr.nbytes, 1)}')
    if feature:
        logger.info(f'feature:  {human_readable_size(feature.nbytes, 1)}')

    logger.info(f'Classes: {num_classes}')
    if mixdb.truth_mutex:
        logger.info(f'Mode:  Single-label / truth_mutex / softmax')
    else:
        logger.info(f'Mode:  Multi-label / Binary')

    mxid_snro = get_mixids_from_snr(mixdb=mixdb)
    snrlist = list(mxid_snro.keys())
    snrlist.sort(reverse=True)
    logger.info(f'Ordered SNRs: {snrlist}\n')
    if type(predict_thr) is np.ndarray:
        logger.info(f'Prediction Threshold(s): {predict_thr.transpose()}\n')
    else:
        logger.info(f'Prediction Threshold(s): {predict_thr}\n')

    # Top-level report over all mixtures
    macrodf, microdf, wghtdf, mxid_snro = snr_summary(mixdb=mixdb,
                                                      mixid=':',
                                                      truth_f=truth,
                                                      predict=predict,
                                                      segsnr=segsnr if compute_segsnr else None,
                                                      predict_thr=predict_thr)

    if num_classes > 1:
        logger.info(f'Metrics micro-avg per SNR over all {num_mixtures} mixtures:')
    else:
        logger.info(f'Metrics per SNR over all {num_mixtures} mixtures:')
    logger.info(microdf.round(3).to_string())
    logger.info('')
    if output_dir:
        microdf.round(3).to_csv(join(output_dir, 'snr.csv'))

    if mixdb.truth_mutex:
        macrodf, microdf, wghtdf, mxid_snro = snr_summary(mixdb=mixdb,
                                                          mixid=':',
                                                          truth_f=truth[:, 0:-1],
                                                          predict=predict[:, 0:-1],
                                                          segsnr=segsnr if compute_segsnr else None,
                                                          predict_thr=predict_thr)

        logger.info(f'Metrics micro-avg without "Other" class per SNR over all {num_mixtures} mixtures:')
        logger.info(microdf.round(3).to_string())
        logger.info('')
        if output_dir:
            microdf.round(3).to_csv(join(output_dir, 'snrwo.csv'))

    for snri in snrlist:
        mxids = mxid_snro[snri]
        classdf = class_summary(mixdb, mxids, truth, predict, predict_thr)
        logger.info(f'Metrics per class for SNR {snri} over {len(mxids)} mixtures:')
        logger.info(classdf.round(3).to_string())
        logger.info('')
        if output_dir:
            classdf.round(3).to_csv(join(output_dir, f'class_snr{snri}.csv'))


def main():
    from datetime import datetime
    from os import mkdir
    from os.path import join

    import h5py
    from docopt import docopt

    import sonusai
    from sonusai import SonusAIError
    from sonusai import create_file_handler
    from sonusai.utils import read_predict_data
    from sonusai.utils import trim_docstring

    args = docopt(trim_docstring(__doc__), version=sonusai.__version__, options_first=True)

    verbose = args['--verbose']
    feature_name = args['--feature']
    predict_name = args['--predict']
    predict_threshold = float(args['--thr'])
    location = args['LOC']

    mixdb = MixtureDatabase(config=location, show_progress=True)

    # create output directory
    output_dir = f'evaluate-{datetime.now():%Y%m%d}'
    try:
        mkdir(output_dir)
    except OSError as _:
        output_dir = f'evaluate-{datetime.now():%Y%m%d-%H%M%S}'
        try:
            mkdir(output_dir)
        except OSError as error:
            raise SonusAIError(f'Could not create directory, {output_dir}: {error}')

    create_file_handler(join(output_dir, 'evaluate.log'))

    with h5py.File(feature_name, 'r') as f:
        truth_f = np.array(f['truth_f'])
        segsnr = np.array(f['segsnr'])

    predict = read_predict_data(predict_name)

    evaluate(mixdb=mixdb,
             truth=truth_f,
             segsnr=segsnr,
             output_dir=output_dir,
             predict=predict,
             predict_thr=predict_threshold,
             verbose=verbose)

    logger.info(f'Wrote results to {output_dir}')


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        logger.info('Canceled due to keyboard interrupt')
        raise SystemExit(0)
