"""sonusai calc_metric_spenh_targetf

usage: calc_metric_spenh_targetf [-hvtpws] [-i MIXID] (-d PLOC) INPUT

options:
    -h, --help
    -v, --verbose               Be verbose.
    -i MIXID, --mixid MIXID     Mixture ID(s) to generate. [default: *].
    -d PLOC, --ploc PLOC        Location of SonusAI predict data.
    -t, --truth-est-mode        Calculate extraction using truth and include metrics.
    -p, --plot                  Enable PDF plots file generation per mixture.
    -w, --wav                   Enable WAV file generation per mixture.
    -s, --summary               Enable summary files generation.

Calculate speech enhancement target_f metrics for prediction data in PLOC and SonusAI mixture database in INPUT.

Inputs:
    PLOC    SonusAI prediction data directory.
    INPUT   SonusAI mixture database directory.

Outputs the following to PLOC:
    <id>_metric_spenh_targetf.txt

    If --plot:
        <id>_metric_spenh_targetf.pdf

    If --wav:
        <id>_target.wav
        <id>_target_est.wav
        <id>_noise.wav
        <id>_noise_est.wav
        <id>_mixture.wav

        If --truth-est-mode:
            <id>_target_truth_est.wav
            <id>_noise_truth_est.wav

    If --summary:
        metric_spenh_targetf_summary.txt
        metric_spenh_targetf_summary.csv
        metric_spenh_targetf_list.csv
        metric_spenh_targetf_estats_list.csv

        If --truth-est-mode:
            metric_spenh_targetf_truth_list.csv
            metric_spenh_targetf_estats_truth_list.csv

"""
from dataclasses import dataclass
from typing import Tuple
from typing import Union

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from sonusai import logger
from sonusai.mixture import AudioF
from sonusai.mixture import AudioT
from sonusai.mixture import Feature
from sonusai.mixture import Location
from sonusai.mixture import MixtureDatabase
from sonusai.mixture import Predict


# NOTE: global object is required for run-time performance; using 'partial' is much slower.
@dataclass
class MPGlobal:
    mixdb: MixtureDatabase = None
    predict_location: Location = None
    truth_est_mode: bool = None
    enable_plot: bool = None
    enable_wav: bool = None


MP_GLOBAL = MPGlobal()


def calc_pcm(s_true: np.ndarray, s_est: np.ndarray, with_log: bool = False) -> np.ndarray:
    """Calculate pcm ((Phase Constrained Magnitude)) err/oss using all source inputs
    which are frames x nsrc x bins. These should include a noise to
    be a complete mixture estimate, i.e. noise_est = mixture - sum-over-n(s_est(:,n,:))
    should be one of the sources in s_true and s_est.
    Calculates mean-over-srcs(mean-over-tf(| (|Sr(t,f)|+|Si(t,f)|) - (|Shr(t,f)|+|Shi(t,f)|) |))
    log is optional if with_log=True (for use as a loss function)
    Returns:
      pcm scalar
    ref:  2022-04-sa-sdr-novel-loss-for-separation
    """

    # multisrc sa-sdr, inputs must be timesteps x nsrc
    err = s_true - s_est  # samples x nsrc

    # -10*log10(sumk(||sk||^2) / sumk(||sk - shk||^2)
    num = np.sum(s_true ** 2)  # sum over samples and sources
    den = np.sum(err ** 2)
    if num == 0 and den == 0:
        ratio = np.inf
    else:
        ratio = num / (den + np.finfo(np.float32).eps)

    sa_sdr = 10 * np.log10(ratio)

    return sa_sdr


def calc_sa_sdr(s_true: np.ndarray,
                s_est: np.ndarray,
                with_scale: bool = False,
                with_negate: bool = False) -> (np.ndarray, np.ndarray):
    """Calculate sa-sdr (source-aggregated SDR (signal distortion ratio)) using all source
    inputs which are samples,nsrc time-domain inputs. These should include a noise to
    be a complete mixture estimate, i.e. noise_est = mixture - sum-over-n(s_est(:,n,:))
    should be one of the sources in s_true and s_est.
    Calculates -10*log10(sumn(||sn||^2) / sumn(||sn - shn||^2)
    Scaling is optional if with_scale=True, scaling is same as in SI-SDR
    Negation is optional if with_negate=True (for use as a loss function)
    Returns:
      sa_sdr scalar
    ref:  2022-04-sa-sdr-novel-loss-for-separation
    """

    if with_scale:
        # calc 1 x nsrc scaling factors
        ref_energy = np.sum(s_true ** 2, axis=0, keepdims=True)  # 1,nsrc
        # if ref_energy is zero, just set scaling to 1.0  # 1,nsrc
        with np.errstate(divide='ignore', invalid='ignore'):
            opt_scale = np.sum(s_true * s_est, axis=0, keepdims=True) / ref_energy
            opt_scale[opt_scale == np.inf] = 1.0
            opt_scale = np.nan_to_num(opt_scale, nan=1.0)
        scaled_ref = opt_scale * s_true  # 1 x nsrc
    else:
        scaled_ref = s_true
        opt_scale = np.ones((1, s_true.shape[1]), dtype=float)

    # multisrc sa-sdr, inputs must be timesteps x nsrc
    err = scaled_ref - s_est  # samples x nsrc

    # -10*log10(sumk(||sk||^2) / sumk(||sk - shk||^2)
    num = np.sum(s_true ** 2)  # sum over samples and sources
    den = np.sum(err ** 2)
    if num == 0 and den == 0:
        ratio = np.inf
    else:
        ratio = num / (den + np.finfo(np.float32).eps)

    sa_sdr = 10 * np.log10(ratio)

    if with_negate:
        sa_sdr = -sa_sdr  # for use as a loss function

    return sa_sdr, opt_scale


def mean_square_error(ytrue: np.ndarray,
                      ypred: np.ndarray,
                      squared: bool = False) -> (np.ndarray, np.ndarray, np.ndarray):
    """Calculate mean square error or root mean square error between ytrue, ypred

    Typical inputs expected to be size frames x classes/bins
    returns:
      err    mean over both dimensions
      err_c  mean-over-dim0 i.e. a value per class/bin
      err_f  mean-over-dim1 i.e. a value per frame
    """
    sqerr = np.square(ytrue - ypred)
    err_c = np.mean(sqerr, axis=0)  # mean over frames for value per class
    err_f = np.mean(sqerr, axis=1)  # mean over classes for value per frame
    err = np.mean(sqerr)  # mean over all
    if not squared:
        err_c = np.sqrt(err_c)
        err_f = np.sqrt(err_f)
        err = np.sqrt(err)

    return err, err_c, err_f


def mean_abs_percentage_error(ytrue: np.ndarray, ypred: np.ndarray) -> (np.ndarray, np.ndarray, np.ndarray):
    """Calculate mean abs percentage error between ytrue, ypred
    If inputs are complex, calculates average:  mape(real)/2 + mape(imag)/2

    Inputs expected to be size frames x classes/bins
    returns:
      err    mean over both dimensions
      err_c  mean-over-dim0 i.e. a value per class/bin
      err_f  mean-over-dim1 i.e. a value per frame
    """
    if np.iscomplexobj(ytrue) is not True and np.iscomplexobj(ypred) is not True:
        abserr = 100 * np.abs((ytrue - ypred) / (ytrue + np.finfo(np.float32).eps))
    else:
        ytrue_r = np.real(ytrue)
        ytrue_i = np.imag(ytrue)
        ypred_r = np.real(ypred)
        ypred_i = np.imag(ypred)
        abserr_r = 100 * np.abs((ytrue_r - ypred_r) / (ytrue_r + np.finfo(np.float32).eps))
        abserr_i = 100 * np.abs((ytrue_i - ypred_i) / (ytrue_i + np.finfo(np.float32).eps))
        abserr = (abserr_r / 2) + (abserr_i / 2)

    err_c = np.mean(abserr, axis=0)  # mean over frames for value per class
    err_f = np.mean(abserr, axis=1)  # mean over classes for value per frame
    err = np.mean(abserr)  # mean over all

    return err, err_c, err_f


def log_error(ytrue: np.ndarray, ypred: np.ndarray) -> (np.ndarray, np.ndarray, np.ndarray):
    """Calculate log error between ytrue, ypred which are complex or real float numpy arrays

    Typical inputs expected to be size frames x classes/bins
    returns:
      logerr    mean over both dimensions, scalar value
      logerr_c  mean-over-dim0 i.e. a value per class/bin
      logerr_f  mean-over-dim1 i.e. a value per frame
    """
    ytsq = np.real(ytrue * np.conjugate(ytrue))
    ypsq = np.real(ypred * np.conjugate(ypred))
    lgerr = abs(10 * np.log10((ytsq + np.finfo(np.float32).eps) / (ypsq + np.finfo(np.float32).eps)))
    # lgerr = abs(10*np.log10(ytsq / (ypsq + np.finfo(np.float32).eps)+np.finfo(np.float32).eps))
    logerr_c = np.mean(lgerr, axis=0)  # mean over frames for value per class
    logerr_f = np.mean(lgerr, axis=1)  # mean over classes for value per frame
    logerr = np.mean(lgerr)

    return logerr, logerr_c, logerr_f


def calculate_pesq(speech_ref: np.ndarray, speech_est: np.ndarray, error_value=0.0):
    """Computes the PESQ score of speech estimate audio vs. the clean speech estimate audio

    Upon error, assigns a value of 0, or user specified value in error_value
    Argument/s:
      speech_ref - speech reference audio, np.ndarray vector of samples.
      speech_est - speech estimated audio, np.ndarray vector of samples.
    Returns:
      score - float value between -0.5 to 4.5.
   """
    import warnings

    from pesq import pesq

    try:
        with warnings.catch_warnings():
            warnings.simplefilter('ignore')
            score = pesq(16000, speech_ref, speech_est, mode='wb')
    except Exception as e:
        logger.debug(f'PESQ error {e}')
        score = error_value

    return score


def plot_mixpred(mixture: AudioT,
                 mixture_f: AudioF,
                 target: AudioT = None,
                 feature: Feature = None,
                 predict: Predict = None,
                 tp_title: str = '') -> plt.figure:
    from sonusai.mixture import SAMPLE_RATE

    num_plots = 2
    if feature is not None:
        num_plots += 1
    if predict is not None:
        num_plots += 1

    fig, ax = plt.subplots(num_plots, 1, constrained_layout=True, figsize=(11, 8.5))

    # Plot the waveform
    p = 0
    x_axis = np.arange(len(mixture), dtype=np.float32) / SAMPLE_RATE
    ax[p].plot(x_axis, mixture, label='Mixture', color='mistyrose')
    ax[0].set_ylabel('magnitude', color='tab:blue')
    ax[p].set_xlim(x_axis[0], x_axis[-1])
    # ax[p].set_ylim([-1.025, 1.025])
    if target is not None:  # Plot target time-domain waveform on top of mixture
        ax[0].plot(x_axis, target, label='Target', color='tab:blue')
        # ax[0].tick_params(axis='y', labelcolor=color)
    ax[p].set_title('Waveform')

    # Plot the mixture spectrogram
    p += 1
    ax[p].imshow(np.transpose(mixture_f), aspect='auto', interpolation='nearest', origin='lower')
    ax[p].set_title('Mixture')

    if feature is not None:
        p += 1
        ax[p].imshow(np.transpose(feature), aspect='auto', interpolation='nearest', origin='lower')
        ax[p].set_title('Feature')

    if predict is not None:
        p += 1
        ax[p].imshow(np.transpose(predict), aspect='auto', interpolation='nearest', origin='lower')
        ax[p].set_title('Predict ' + tp_title)

    return fig


def plot_pdb_predtruth(predict: np.ndarray,
                       truth_f: Union[np.ndarray, None] = None,
                       metric: Union[np.ndarray, None] = None,
                       tp_title: str = '') -> plt.figure:
    """Plot predict and optionally truth and a metric in power db, e.g. applies 10*log10(predict)"""

    num_plots = 2
    if truth_f is not None:
        num_plots += 1

    fig, ax = plt.subplots(num_plots, 1, constrained_layout=True, figsize=(11, 8.5))

    # Plot the predict spectrogram
    p = 0
    tmp = 10 * np.log10(predict.transpose() + np.finfo(np.float32).eps)
    ax[p].imshow(tmp, aspect='auto', interpolation='nearest', origin='lower')
    ax[p].set_title('Predict')

    if truth_f is not None:
        p += 1
        tmp = 10 * np.log10(truth_f.transpose() + np.finfo(np.float32).eps)
        ax[p].imshow(tmp, aspect='auto', interpolation='nearest', origin='lower')
        ax[p].set_title('Truth')

    # Plot the predict avg, and optionally truth avg and metric lines
    pred_avg = 10 * np.log10(np.mean(predict, axis=-1) + np.finfo(np.float32).eps)
    p += 1
    x_axis = np.arange(len(pred_avg), dtype=np.float32)  # / SAMPLE_RATE
    ax[p].plot(x_axis, pred_avg, color='black', linestyle='dashed', label='Predict mean over freq.')
    ax[p].set_ylabel('mean db', color='black')
    ax[p].set_xlim(x_axis[0], x_axis[-1])
    if truth_f is not None:
        truth_avg = 10 * np.log10(np.mean(truth_f, axis=-1) + np.finfo(np.float32).eps)
        ax[p].plot(x_axis, truth_avg, color='green', linestyle='dashed', label='Truth mean over freq.')

    if metric is not None:  # instantiate 2nd y-axis that shares the same x-axis
        ax2 = ax[p].twinx()
        color2 = 'red'
        ax2.plot(x_axis, metric, color=color2, label='sig distortion (mse db)')
        ax2.set_xlim(x_axis[0], x_axis[-1])
        ax2.set_ylim([0, np.max(metric)])
        ax2.set_ylabel('spectral distortion (mse db)', color=color2)
        ax2.tick_params(axis='y', labelcolor=color2)
        ax[p].set_title('SNR and SNR mse (mean over freq. db)')
    else:
        ax[p].set_title('SNR (mean over freq. db)')
        # ax[0].tick_params(axis='y', labelcolor=color)
    return fig


def plot_epredtruth(predict: np.ndarray,
                    predict_wav: np.ndarray,
                    truth_f: Union[np.ndarray, None] = None,
                    truth_wav: Union[np.ndarray, None] = None,
                    metric: Union[np.ndarray, None] = None,
                    tp_title: str = '') -> plt.figure:
    """Plot predict spectrogram and waveform and optionally truth and a metric)"""

    num_plots = 2
    if truth_f is not None:
        num_plots += 1
    if metric is not None:
        num_plots += 1

    fig, ax = plt.subplots(num_plots, 1, constrained_layout=True, figsize=(11, 8.5))

    # Plot the predict spectrogram
    p = 0
    ax[p].imshow(predict.transpose(), aspect='auto', interpolation='nearest', origin='lower')
    ax[p].set_title('Predict')

    if truth_f is not None:
        p += 1
        ax[p].imshow(truth_f.transpose(), aspect='auto', interpolation='nearest', origin='lower')
        ax[p].set_title('Truth')

    # Plot the predict wav, and optionally truth avg and metric lines
    p += 1
    x_axis = np.arange(len(predict_wav), dtype=np.float32)  # / SAMPLE_RATE
    ax[p].plot(x_axis, predict_wav, color='black', linestyle='dashed', label='Speech Estimate')
    ax[p].set_ylabel('Amplitude', color='black')
    ax[p].set_xlim(x_axis[0], x_axis[-1])
    if truth_wav is not None:
        ntrim = len(truth_wav) - len(predict_wav)
        if ntrim > 0:
            truth_wav = truth_wav[0:-ntrim]
        ax[p].plot(x_axis, truth_wav, color='green', linestyle='dashed', label='True Target')

    # Plot the metric lines
    if metric is not None:
        p += 1
        x_axis = np.arange(len(metric), dtype=np.float32)  # / SAMPLE_RATE
        ax[p].plot(x_axis, metric, color='red', label='Target LogErr')
        ax[p].set_ylabel('log error db', color='red')
        ax[p].set_xlim(x_axis[0], x_axis[-1])
        ax[p].set_ylim([-0.01, np.max(metric) + .01])

    return fig


def _process_mixture(mixid: int) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    from os.path import basename
    from os.path import join
    from os.path import splitext

    import h5py

    from sonusai import SonusAIError
    from sonusai.utils import float_to_int16
    from sonusai.utils import unstack_complex
    from sonusai.utils import write_wav

    mixdb = MP_GLOBAL.mixdb
    predict_location = MP_GLOBAL.predict_location
    truth_est_mode = MP_GLOBAL.truth_est_mode
    enable_plot = MP_GLOBAL.enable_plot
    enable_wav = MP_GLOBAL.enable_wav

    # 1) Collect true target, noise, mixture data
    target = mixdb.mixture_target(mixid)
    target_f = mixdb.mixture_target_f(mixid, target=target)

    noise = mixdb.mixture_noise(mixid)
    noise_f = mixdb.mixture_noise_f(mixid, noise=noise)

    mixture = mixdb.mixture_mixture(mixid, target=target, noise=noise)
    mixture_f = mixdb.mixture_mixture_f(mixid, mixture=mixture)

    feature, truth_f = mixdb.mixture_ft(mixid, mixture=mixture)

    targetfi = mixdb.inverse_transform(target_f)  # need to use inv-tf to match size & tf properties
    noisefi = mixdb.inverse_transform(noise_f)  # need to use inv-tf to match size & tf properties

    # 2)  Read predict data
    output_name = join(predict_location, mixdb.mixtures[mixid].name)
    base_name = splitext(output_name)[0]
    try:
        with h5py.File(output_name, 'r') as f:
            predict = np.array(f['predict'])
    except Exception as e:
        raise SonusAIError(f'Error reading {output_name}: {e}')

    # 3) Extraction - for target_f truth, simply unstack as predict is estimating the target
    predict_complex = unstack_complex(predict)
    truth_f_complex = unstack_complex(truth_f)
    noise_est_complex = mixture_f - predict_complex
    target_est_wav = mixdb.inverse_transform(predict_complex)
    noise_est_wav = mixdb.inverse_transform(noise_est_complex)

    target_truth_est_complex = None
    target_truth_est_audio = None

    noise_truth_est_complex = None
    noise_truth_est_audio = None

    if truth_est_mode:
        # estimates using truth instead of prediction
        target_truth_est_complex = truth_f_complex
        target_truth_est_audio = mixdb.inverse_transform(target_truth_est_complex)

        noise_truth_est_complex = mixture_f - target_truth_est_complex
        noise_truth_est_audio = mixdb.inverse_transform(noise_truth_est_complex)

    # 4) Metrics
    # Mean absolute error (real and imag)
    cmape_tg, cmape_tg_bin, cmape_tg_frame = mean_abs_percentage_error(truth_f_complex, predict_complex)
    # Target/Speech logerr - PSD estimation accuracy symmetric mean log-spectral distortion
    lerr_tg, lerr_tg_bin, lerr_tg_frame = log_error(truth_f_complex, predict_complex)
    # Noise logerr - PSD estimation accuracy
    lerr_n, lerr_n_bin, lerr_n_frame = log_error(noise_f, noise_est_complex)
    # Noise td logerr
    # lerr_nt, lerr_nt_bin, lerr_nt_frame = log_error(noisefi, noise_truth_est_audio)

    # SA-SDR (time-domain source-aggragated SDR)
    ytrue = np.concatenate((targetfi[:, np.newaxis], noisefi[:, np.newaxis]), axis=1)
    ypred = np.concatenate((target_est_wav[:, np.newaxis], noise_est_wav[:, np.newaxis]), axis=1)
    sa_sdr, _ = calc_sa_sdr(ytrue, ypred)  # note: w/o scale is more pessimistic number

    # Speech intelligibility measure - PESQ
    pesq_speech = calculate_pesq(target, target_est_wav)
    pesq_mixture = calculate_pesq(target, mixture)
    pesq_impr = pesq_speech - pesq_mixture  # pesq improvement
    pesq_impr_pc = pesq_impr / (pesq_mixture + np.finfo(np.float32).eps) * 100  # pesq improvement %

    # 5) Save per mixture metric results
    # Single row in table of scalar metrics per mixture
    mtable1_col = ['MXSNR', 'MXPESQ', 'PESQ', 'PESQi%', 'SASDR', 'SPCMAPE%', 'SPLERR', 'NLERR', 'SPFILE', 'NFILE']
    ti = mixdb.mixtures[mixid].target_file_index[0]
    ni = mixdb.mixtures[mixid].noise_file_index
    metr1 = [mixdb.mixtures[mixid].snr, pesq_mixture, pesq_speech, pesq_impr_pc, sa_sdr, cmape_tg, lerr_tg,
             lerr_n, basename(mixdb.targets[ti].name), basename(mixdb.noises[ni].name)]
    mtab1 = pd.DataFrame([metr1], columns=mtable1_col, index=[mixid])

    # Stats of per frame estimation metrics
    efs_table2_col = ['Max', 'Min', 'Avg', 'Median']
    efs_table2_row = ['SPCMAPE%', 'SPLERR', 'NLERR']
    metr2 = [[np.max(cmape_tg_frame), np.min(cmape_tg_frame), np.mean(cmape_tg_frame), np.median(cmape_tg_frame)],
             [np.max(lerr_tg_frame), np.min(lerr_tg_frame), np.mean(lerr_tg_frame), np.median(lerr_tg_frame)],
             [np.max(lerr_n_frame), np.min(lerr_n_frame), np.mean(lerr_n_frame), np.median(lerr_n_frame)]]
    mtab2 = pd.DataFrame(metr2, columns=efs_table2_col, index=efs_table2_row)
    mtab2flat_col = ['MXSNR', 'SPCMAPE Max', 'SPCMAPE Min', 'SPCMAPE Avg', 'SPCMAPE Median',
                     'SPLERR Max', 'SPLERR Min', 'SPLERR Avg', 'SPLERR Median',
                     'NLERR Max', 'NLERR Min', 'NLERR Avg', 'NLERR Median']
    tmp = np.insert(np.array(metr2), 0, mixdb.mixtures[mixid].snr).reshape(1, 13)
    mtab2_flat = pd.DataFrame(tmp, columns=mtab2flat_col, index=[mixid])

    all_metrics_table_1 = mtab1
    all_metrics_table_2 = mtab2_flat

    metric_name = base_name + '_metric_spenh_targetf.txt'
    with open(metric_name, 'w') as f:
        print('Speech enhancement metrics:', file=f)
        print(mtab1.round(2).to_string(), file=f)
        print('', file=f)
        print(f'Extraction statistics over {mixture_f.shape[0]} frames:', file=f)
        print(mtab2.round(2).to_string(), file=f)
        print('', file=f)
        print(f'Target path: {mixdb.targets[ti].name}', file=f)
        print(f'Noise path: {mixdb.noises[ni].name}', file=f)
        # print(f'PESQ improvement: {pesq_impr:0.2f}, {pesq_impr_pc:0.1f}%', file=f)

    lerr_tgtr_frame = None
    lerr_ntr_frame = None
    all_metrics_table_3 = None
    all_metrics_table_4 = None

    if truth_est_mode:
        cmape_tgtr, cmape_tgtr_bin, cmape_tgtr_frame = mean_abs_percentage_error(truth_f_complex,
                                                                                 target_truth_est_complex)
        # metrics of estimates using truth instead of prediction
        lerr_tgtr, lerr_tgtr_bin, lerr_tgtr_frame = log_error(truth_f_complex, target_truth_est_complex)
        lerr_ntr, lerr_ntr_bin, lerr_ntr_frame = log_error(noise_f, noise_truth_est_complex)

        # ytrue = np.concatenate((targetfi[:, np.newaxis], noisefi[:, np.newaxis]), axis=1)
        ypred = np.concatenate((target_truth_est_audio[:, np.newaxis], noise_truth_est_audio[:, np.newaxis]), axis=1)
        sa_sdr_tr, opt_scale_tr = calc_sa_sdr(ytrue, ypred, with_scale=True)  # scale should be ones

        pesq_speechtr = calculate_pesq(target, target_truth_est_audio)
        pesq_impr_sptr = pesq_speechtr - pesq_mixture  # pesq improvement
        pesq_impr_pctr = pesq_impr_sptr / (pesq_mixture + np.finfo(np.float32).eps) * 100  # pesq improvement %

        mtable3_col = ['MXSNR', 'MXPESQ', 'PESQ', 'PESQi%', 'SASDR', 'SPCMAPE%', 'SPLERR', 'NLERR']
        metr3 = [mixdb.mixtures[mixid].snr, pesq_mixture, pesq_speechtr, pesq_impr_pctr, sa_sdr_tr,
                 cmape_tgtr, lerr_tgtr, lerr_ntr]
        mtab3 = pd.DataFrame([metr3], columns=mtable3_col, index=[mixid])

        # Stats of per frame estimation metrics
        efs_table4_col = ['Max', 'Min', 'Avg', 'Median']
        efs_table4_row = ['SPCMAPE%', 'SPLERR', 'NLERR']
        metr4 = [[np.max(cmape_tgtr_frame), np.min(cmape_tgtr_frame), np.mean(cmape_tgtr_frame),
                  np.median(cmape_tgtr_frame)],
                 [np.max(lerr_tgtr_frame), np.min(lerr_tgtr_frame), np.mean(lerr_tgtr_frame),
                  np.median(lerr_tgtr_frame)],
                 [np.max(lerr_ntr_frame), np.min(lerr_ntr_frame), np.mean(lerr_ntr_frame),
                  np.median(lerr_ntr_frame)]]
        mtab4 = pd.DataFrame(metr4, columns=efs_table4_col, index=efs_table4_row)

        # Append extraction metrics to metrics file:
        with open(metric_name, 'a') as f:
            print('', file=f)
            print('Speech enhancement metrics of extraction method using truth:', file=f)
            print(mtab3.round(2).to_string(), file=f)
            print('', file=f)
            print('Extraction (using Truth) statistics over frames:', file=f)
            print(mtab4.round(2).to_string(), file=f)

        # Append to all mixture table
        # mtab4flat_col = ['MXSNR', 'SPLERR Max', 'SPLERR Min', 'SPLERR Avg', 'SPLERR Median',
        #                  'NLERR Max', 'NLERR Min', 'NLERR Avg', 'NLERR Median']
        mtab4flat_col = ['MXSNR', 'SPCMAPE Max', 'SPCMAPE Min', 'SPCMAPE Avg', 'SPCMAPE Median',
                         'SPLERR Max', 'SPLERR Min', 'SPLERR Avg', 'SPLERR Median',
                         'NLERR Max', 'NLERR Min', 'NLERR Avg', 'NLERR Median']
        tmp = np.insert(np.array(metr4), 0, mixdb.mixtures[mixid].snr).reshape(1, 13)  # Insert MXSNR
        mtab4_flat = pd.DataFrame(tmp, columns=mtab4flat_col, index=[mixid])

        all_metrics_table_3 = mtab3
        all_metrics_table_4 = mtab4_flat

    # 7) write wav files
    if enable_wav:
        write_wav(name=base_name + '_mixture.wav', audio=float_to_int16(mixture))
        write_wav(name=base_name + '_target_est.wav', audio=float_to_int16(target_est_wav))
        write_wav(name=base_name + '_noise_est.wav', audio=float_to_int16(noise_est_wav))
        write_wav(name=base_name + '_target.wav', audio=float_to_int16(target))
        write_wav(name=base_name + '_noise.wav', audio=float_to_int16(noise))
        # debug code to test for perfect reconstruction of the extraction method
        # note both 75% olsa-hanns and 50% olsa-hann modes checked to have perfect reconstruction
        # target_r = mixdb.inverse_transform(target_f)
        # noise_r = mixdb.inverse_transform(noise_f)
        # _write_wav(name=base_name + '_target_r.wav', audio=float_to_int16(target_r))
        # _write_wav(name=base_name + '_noise_r.wav', audio=float_to_int16(noise_r)) # chk perfect rec
        if truth_est_mode:
            write_wav(name=base_name + '_target_truth_est.wav', audio=float_to_int16(target_truth_est_audio))
            write_wav(name=base_name + '_noise_truth_est.wav', audio=float_to_int16(noise_truth_est_audio))

    # 8) Write out plot file
    if enable_plot:
        from matplotlib.backends.backend_pdf import PdfPages
        plot_fname = base_name + '_metric_spenh_targetf.pdf'

        # Reshape feature to eliminate overlap redundancy for easier to understand spectrogram view
        # Original size (frames, stride, num_bands), decimates in stride dimension only if step is > 1
        # Reshape to get frames*decimated_stride, num_bands
        step = int(mixdb.feature_samples / mixdb.feature_step_samples)
        if feature.ndim != 3:
            raise SonusAIError(f'feature does not have 3 dimensions: frames, stride, num_bands')

        # for feature cn*00n**
        feat_sgram = unstack_complex(feature)
        feat_sgram = 20 * np.log10(abs(feat_sgram) + np.finfo(np.float32).eps)
        feat_sgram = feat_sgram[:, -step:, :]  # decimate,  Fx1xB
        feat_sgram = np.reshape(feat_sgram, (feat_sgram.shape[0] * feat_sgram.shape[1], feat_sgram.shape[2]))

        with PdfPages(plot_fname) as pdf:
            # page1 we always have a mixture and prediction, target optional if truth provided
            tfunc_name = mixdb.targets[0].truth_settings[0].function  # first target, assumes all have same
            if tfunc_name == 'mapped_snr_f':  # leave as unmapped snr
                predplot = predict
                tfunc_name = mixdb.targets[0].truth_settings[0].function
            elif tfunc_name == 'target_f':
                predplot = 20 * np.log10(abs(predict_complex) + np.finfo(np.float32).eps)
            else:
                predplot = 10 * np.log10(predict + np.finfo(np.float32).eps)  # use db scale
                tfunc_name = tfunc_name + ' (db)'

            mixspec = 20 * np.log10(abs(mixture_f) + np.finfo(np.float32).eps)
            pdf.savefig(plot_mixpred(mixture=mixture,
                                     mixture_f=mixspec,
                                     target=target,
                                     feature=feat_sgram,
                                     predict=predplot,
                                     tp_title=tfunc_name))

            # ----- page 2, plot unmapped predict, opt truth reconstructed and line plots of mean-over-f
            # pdf.savefig(plot_pdb_predtruth(predict=pred_snr_f, tp_title='predict snr_f (db)'))

            # page 3 speech extraction
            tg_spec = 20 * np.log10(abs(target_f) + np.finfo(np.float32).eps)
            tg_est_spec = 20 * np.log10(abs(predict_complex) + np.finfo(np.float32).eps)
            # n_spec = np.reshape(n_spec,(n_spec.shape[0] * n_spec.shape[1], n_spec.shape[2]))
            pdf.savefig(plot_epredtruth(predict=tg_est_spec,
                                        predict_wav=target_est_wav,
                                        truth_f=tg_spec,
                                        truth_wav=target,
                                        metric=lerr_tg_frame,
                                        tp_title='speech estimate'))

            # page 4 noise extraction
            n_spec = 20 * np.log10(abs(noise_f) + np.finfo(np.float32).eps)
            n_est_spec = 20 * np.log10(abs(noise_est_complex) + np.finfo(np.float32).eps)
            pdf.savefig(plot_epredtruth(predict=n_est_spec,
                                        predict_wav=noise_est_wav,
                                        truth_f=n_spec,
                                        truth_wav=noisefi,
                                        metric=lerr_n_frame,
                                        tp_title='noise estimate'))

            if truth_est_mode:
                # page 5 truth-based speech extraction
                tg_trest_spec = 20 * np.log10(abs(target_truth_est_complex) + np.finfo(np.float32).eps)
                pdf.savefig(plot_epredtruth(predict=tg_trest_spec,
                                            predict_wav=target_truth_est_audio,
                                            truth_f=tg_spec,
                                            truth_wav=target,
                                            metric=lerr_tgtr_frame,
                                            tp_title='truth-based speech estimate'))

                # page 6 truth-based noise extraction
                n_trest_spec = 20 * np.log10(abs(noise_truth_est_complex) + np.finfo(np.float32).eps)
                pdf.savefig(plot_epredtruth(predict=n_trest_spec,
                                            predict_wav=noise_truth_est_audio,
                                            truth_f=n_spec,
                                            truth_wav=noisefi,
                                            metric=lerr_ntr_frame,
                                            tp_title='truth-based noise estimate'))

        plt.close('all')

    return all_metrics_table_1, all_metrics_table_2, all_metrics_table_3, all_metrics_table_4


def main():
    from docopt import docopt

    import sonusai
    from sonusai.utils import trim_docstring

    args = docopt(trim_docstring(__doc__), version=sonusai.__version__, options_first=True)

    verbose = args['--verbose']
    mixids = args['--mixid']
    predict_location = args['--ploc']
    truth_est_mode = args['--truth-est-mode']
    enable_plot = args['--plot']
    enable_wav = args['--wav']
    enable_summary = args['--summary']
    input_name = args['INPUT']

    from os.path import join

    from tqdm import tqdm

    from sonusai import create_file_handler
    from sonusai import initial_log_messages
    from sonusai import update_console_handler
    from sonusai.mixture import MixtureDatabase
    from sonusai.utils import p_tqdm_map

    # Setup logging file
    create_file_handler(join(predict_location, 'calc_metric_spenh_targetf.log'))
    update_console_handler(verbose)
    initial_log_messages('calc_metric_spenh_targetf')

    mixdb = MixtureDatabase(config=input_name, show_progress=True)
    mixids = mixdb.mixids_to_list(mixids)
    logger.info(f'Found {len(mixids)} mixtures with {mixdb.num_classes} classes from {input_name}')

    mtab_snr_summary_tr = None
    mtab_snr_summary_emtr = None

    MP_GLOBAL.mixdb = mixdb
    MP_GLOBAL.predict_location = predict_location
    MP_GLOBAL.truth_est_mode = truth_est_mode
    MP_GLOBAL.enable_plot = enable_plot
    MP_GLOBAL.enable_wav = enable_wav

    progress = tqdm(total=len(mixids), desc='calc_metric_spenh_targetf')
    all_metrics_tables = p_tqdm_map(_process_mixture, mixids, progress=progress)
    progress.close()

    all_metrics_table_1 = pd.concat([item[0] for item in all_metrics_tables])
    all_metrics_table_2 = pd.concat([item[1] for item in all_metrics_tables])
    all_metrics_table_3 = pd.concat([item[2] for item in all_metrics_tables])
    all_metrics_table_4 = pd.concat([item[3] for item in all_metrics_tables])

    if not enable_summary:
        return

    # 9) Done with mixtures, write out summary metrics
    # Calculate SNR summary for
    all_mtab1_sorted = all_metrics_table_1.sort_values(by=['MXSNR', 'SPFILE'])
    all_mtab2_sorted = all_metrics_table_2.sort_values(by=['MXSNR'])
    mtab_snr_summary = all_mtab1_sorted.query('MXSNR==' + str(mixdb.snrs[0])).mean(numeric_only=True).to_frame().T
    mtab_snr_summary_em = all_mtab2_sorted.query('MXSNR==' + str(mixdb.snrs[0])).mean(numeric_only=True).to_frame().T
    for snri in range(1, len(mixdb.snrs)):
        mtab_snr_summary = pd.concat([mtab_snr_summary,
                                      all_mtab1_sorted.query('MXSNR==' + str(mixdb.snrs[snri])).mean(
                                          numeric_only=True).to_frame().T])
        mtab_snr_summary_em = pd.concat([mtab_snr_summary_em,
                                         all_mtab2_sorted.query('MXSNR==' + str(mixdb.snrs[snri])).mean(
                                             numeric_only=True).to_frame().T])

    if truth_est_mode:
        all_mtab3_sorted = all_metrics_table_3.sort_values(by=['MXSNR'])
        all_mtab4_sorted = all_metrics_table_4.sort_values(by=['MXSNR'])
        mtab_snr_summary_tr = all_mtab3_sorted.query('MXSNR==' + str(mixdb.snrs[0])).mean(
            numeric_only=True).to_frame().T
        mtab_snr_summary_emtr = all_mtab4_sorted.query('MXSNR==' + str(mixdb.snrs[0])).mean(
            numeric_only=True).to_frame().T
        for snri in range(1, len(mixdb.snrs)):
            mtab_snr_summary_tr = pd.concat([mtab_snr_summary_tr,
                                             all_mtab3_sorted.query('MXSNR==' + str(mixdb.snrs[snri])).mean(
                                                 numeric_only=True).to_frame().T])
            mtab_snr_summary_emtr = pd.concat([mtab_snr_summary_emtr,
                                               all_mtab4_sorted.query('MXSNR==' + str(mixdb.snrs[snri])).mean(
                                                   numeric_only=True).to_frame().T])

    num_mix = len(mixids)
    if num_mix > 1:
        with open(join(predict_location, 'metric_spenh_targetf_summary.txt'), 'w') as f:
            print(f'Speech enhancement metrics avg over each SNR:', file=f)
            print(mtab_snr_summary.round(2).to_string(), file=f)
            print('', file=f)
            print(f'Extraction statistics stats avg over each SNR:', file=f)
            print(mtab_snr_summary_em.round(2).to_string(), file=f)
            print('', file=f)

            print(f'Speech enhancement metrics stats over all {num_mix} mixtures:', file=f)
            print(all_metrics_table_1.describe().round(2).to_string(), file=f)
            print('', file=f)
            print(f'Extraction statistics stats over all {num_mix} mixtures:', file=f)
            print(all_metrics_table_2.describe().round(2).to_string(), file=f)
            print('', file=f)

            if truth_est_mode:
                print(f'Truth-based speech enhancement metrics avg over each SNR:', file=f)
                print(mtab_snr_summary_tr.round(2).to_string(), file=f)
                print('', file=f)
                print(f'Truth-based extraction statistics stats avg over each SNR:', file=f)
                print(mtab_snr_summary_emtr.round(2).to_string(), file=f)
                print('', file=f)

                print(f'Truth-based speech enhancement metrics stats over all {num_mix} mixtures:', file=f)
                print(all_metrics_table_3.describe().round(2).to_string(), file=f)
                print('', file=f)
                print(f'Truth-based extraction statistic stats over all {num_mix} mixtures:', file=f)
                print(all_metrics_table_4.describe().round(2).to_string(), file=f)
                print('', file=f)

            print('Speech enhancement metrics all-mixtures list:', file=f)
            print(all_metrics_table_1.round(2).to_string(), file=f)
            print('', file=f)
            print('Extraction statistics all-mixtures list:', file=f)
            print(all_metrics_table_2.round(2).to_string(), file=f)

            # Write summary to .csv file
            csv_name = join(predict_location, 'metric_spenh_targetf_summary.csv')
            header_args = {
                'mode': 'a',
                'encoding': 'utf-8',
                'index': False,
                'header': False,
            }
            table_args = {
                'mode': 'a',
                'encoding': 'utf-8',
            }
            label = f'Speech enhancement metrics stats over {num_mix} mixtures:'
            pd.DataFrame([label]).to_csv(csv_name, **header_args)
            all_metrics_table_1.describe().round(2).to_csv(csv_name, encoding='utf-8')
            pd.DataFrame(['']).to_csv(csv_name, **header_args)

            label = f'Extraction statistics stats over {num_mix} mixtures:'
            pd.DataFrame([label]).to_csv(csv_name, **header_args)
            all_metrics_table_2.describe().round(2).to_csv(csv_name, **table_args)
            pd.DataFrame(['']).to_csv(csv_name, **header_args)

            if truth_est_mode:
                label = 'Speech enhancement metrics of extraction method using truth, stats:'
                pd.DataFrame([label]).to_csv(csv_name, **header_args)
                all_metrics_table_3.describe().round(2).to_csv(csv_name, **table_args)
                pd.DataFrame(['']).to_csv(csv_name, **header_args)

                label = 'Truth extraction statistics stats:'
                pd.DataFrame([label]).to_csv(csv_name, **header_args)
                all_metrics_table_4.describe().round(2).to_csv(csv_name, **table_args)
                pd.DataFrame(['']).to_csv(csv_name, **header_args)

            csv_name = join(predict_location, 'metric_spenh_targetf_list.csv')
            pd.DataFrame(['Speech enhancement metrics list:']).to_csv(csv_name, **header_args)
            all_metrics_table_1.round(2).to_csv(csv_name, **table_args)

            csv_name = join(predict_location, 'metric_spenh_targetf_estats_list.csv')
            pd.DataFrame(['Extraction statistics list:']).to_csv(csv_name, **header_args)
            all_metrics_table_2.round(2).to_csv(csv_name, **table_args)

            if truth_est_mode:
                csv_name = join(predict_location, 'metric_spenh_targetf_truth_list.csv')
                pd.DataFrame(['Speech enhancement metrics list:']).to_csv(csv_name, **header_args)
                all_metrics_table_3.round(2).to_csv(csv_name, **table_args)

                csv_name = join(predict_location, 'metric_spenh_targetf_truth_list.csv')
                pd.DataFrame(['Extraction statistics list:']).to_csv(csv_name, **header_args)
                all_metrics_table_4.round(2).to_csv(csv_name, **table_args)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        logger.info('Canceled due to keyboard interrupt')
        exit()
