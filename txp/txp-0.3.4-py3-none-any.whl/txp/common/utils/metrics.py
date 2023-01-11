import logging

import numpy as np
import pandas as pd
import scipy.signal as signal
from scipy.integrate import cumtrapz
import sys


def peak(data):
    return np.absolute(data).max()


def rms(data):
    return np.sqrt(np.power(data, 2).mean())


def standard_deviation(data):
    return np.std(data)


def rolling_rms(x, n=8) -> np.array:
    """Computes rolling RMS of a signal x.

    We use the windowed rolling mean method from pandas to perform the
        windowing.

    References:
        https://stackoverflow.com/questions/8245687/numpy-root-mean-squared-rms-smoothing-of-a-signal
        https://stackoverflow.com/questions/60428508/calculating-the-rolling-root-mean-squared
    """
    y = (pd.DataFrame(x ** 2).rolling(n).mean() ** 0.5).fillna(0.0).to_numpy()
    return y.reshape(y.shape[0])


def crest_factor(data):
    cf = peak(data) / rms(data)
    if np.isnan(cf):
        cf = sys.float_info.max
        logging.warning("crest factor to high returning maximum possible value")
    return cf


def get_psd(data, sampling_frequency, window="hanning"):
    bin_width = sampling_frequency / len(data)
    return signal.welch(data, fs=sampling_frequency, nperseg=sampling_frequency / bin_width, window=window, axis=0)


def integrate(y, x=None, sampling_frequency=1):
    if x is not None:
        return cumtrapz(y, x=x)
    else:
        return cumtrapz(y, dx=sampling_frequency)



