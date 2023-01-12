import os

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from scipy import signal

from . import calculator as ca

mpl.rcParams['agg.path.chunksize'] = 10**10


class Plots:
    def __init__(self) -> None:
        self.imsize = (16, 9)

    @staticmethod
    def data1d(data, **kwargs):
        """ Plot 1d data

        Args:
            data (array): shape:=(N,)
            show (bool): opt. default True
            save (bool): opt. default False
            savepath (string): opt. default './plot.jpg'
            ylim (list): opt. [low, up]
            title (string): opt.
            xlabel (string): opt.
            ylabel (string): opt.

        Returns:
            None
        """
        _show = kwargs.get('show', True)
        _save = kwargs.get('save', False)
        _savepath = kwargs.get('savepath', './plot.jpg')
        _ylim = kwargs.get('ylim')
        _title = kwargs.get('title')
        _xlabel = kwargs.get('xlabel', 'sample points')
        _ylabel = kwargs.get('ylabel', 'Acceleration [g]')

        # Plot
        fig, ax = plt.subplots()
        ax.plot(data)
        ax.set_ylim(_ylim)
        plt.title(_title)
        plt.xlabel(_xlabel)
        plt.ylabel(_ylabel)
        plt.grid()

        if _show:
            plt.show()
        if _save:
            plt.savefig(_savepath)
        return None

    @staticmethod
    def fft(data, sr, **kwargs):
        """ Calculate and Plot FFT of data

        Args:
            data (array): (N,)
            sr (int): sample rate
            show (bool): opt. default True
            save (bool): opt. default False
            savepath (string): opt. default './plot.jpg'
            xlim (list): opt. [low, up]
            ylim (list): opt. [low, up]
            title (string): opt.
            xlabel (string): opt.
            ylabel (string): opt.

        Returns:
            None
        """
        _show = kwargs.get('show', True)
        _save = kwargs.get('save', False)
        _savepath = kwargs.get('savepath', './plot.jpg')
        _xlim = kwargs.get('xlim', [0, 500])
        _ylim = kwargs.get('ylim')
        _title = kwargs.get('title')
        _xlabel = kwargs.get('xlabel', 'Frequency [Hz]')
        _ylabel = kwargs.get('ylabel', 'FFT Amplitude * 1/n')

        # Plot
        fig, ax = plt.subplots()
        data_fft_x, data_fft_y = ca.calc_fft(data, sr)
        ax.plot(data_fft_x, data_fft_y)
        ax.set_xlim(_xlim)
        ax.set_ylim(_ylim)
        plt.title(_title)
        plt.xlabel(_xlabel)
        plt.ylabel(_ylabel)
        plt.grid()

        if _show:
            plt.show()
        if _save:
            plt.savefig(_savepath)
        return None

    @staticmethod
    def spectrogram(data, sr, **kwargs):
        """ Calculate and Plot Spectrogram of data

        Args:
            data (array): (N,)
            sr (int): sample rate
            show (bool): opt. default True
            save (bool): opt. default False
            savepath (string): opt. default './plot.jpg'
            ylim (list): opt. [low, up]
            title (string): opt.
            xlabel (string): opt.
            ylabel (string): opt.
            colorbar (string): opt.

        Returns:
            None
        """
        _show = kwargs.get('show', True)
        _save = kwargs.get('save', False)
        _savepath = kwargs.get('savepath', './plot.jpg')
        _ylim = kwargs.get('ylim', [0, 500])
        _title = kwargs.get('title')
        _xlabel = kwargs.get('xlabel', 'number of window')
        _ylabel = kwargs.get('ylabel', 'Frequency [Hz]')
        _colorbar = kwargs.get('colorbar', 'Log|STFT|')

        fig, ax = plt.subplots()
        f, t, Sxx = signal.spectrogram(
            data,
            fs=sr,
            nperseg=sr,
            mode='magnitude'
        )
        spectro = ax.pcolormesh(
            t,
            f,
            np.log10(Sxx),
            shading='auto',
            vmax=0,
            vmin=-7
        )
        ax.set_ylim(_ylim)
        fig.colorbar(spectro, label=_colorbar)
        plt.title(_title)
        ax.set_xlabel(_xlabel)
        ax.set_ylabel(_ylabel)

        if _show:
            plt.show()
        if _save:
            plt.savefig(_savepath)
        return None

    @staticmethod
    def clusters(x, y, labels, classes, **kwargs):
        """Scatter plot the 2d data with discrete classes

        Args:
            x (array): (N,)
            y (array): (N,)
            labels (array): (N,)
            classes (str list): [type1, type2..]
            show (bool): opt. default True
            save (bool): opt. default False
            savepath (string): opt. default './plot.jpg'
            title (string): opt.
            xlabel (string): opt.
            ylabel (string): opt.
            size (int): opt. marker size
            alpha (float): opt. marker transparency
            cmap: opt. plt.cm.plasma

        Returns:
            None
        """
        _show = kwargs.get('show', True)
        _save = kwargs.get('save', False)
        _savepath = kwargs.get('savepath', './plot.jpg')
        _title = kwargs.get('title')
        _xlabel = kwargs.get('xlabel', 'X')
        _ylabel = kwargs.get('ylabel', 'Y')
        _size = kwargs.get('size')
        _alpha = kwargs.get('alpha')
        _cmap = kwargs.get('cmap', plt.cm.plasma)  # plasma Pastel1

        _yticklabels = classes

        # Plot
        fig, ax = plt.subplots()
        n_label = len(_yticklabels)
        bounds = np.linspace(0, n_label, n_label+1)
        ticks = np.linspace(0.5, n_label-0.5, n_label)
        norm = mpl.colors.BoundaryNorm(bounds, _cmap.N)
        img = ax.scatter(x,
                         y,
                         c=labels,
                         s=_size,  # marker size
                         alpha=_alpha,  # transparency
                         cmap=_cmap,
                         norm=norm)
        label = [int(i) for i in labels]
        cb = plt.colorbar(mpl.cm.ScalarMappable(norm=norm, cmap=_cmap),
                          ticks=ticks,)
        cb.ax.set_yticklabels(_yticklabels)
        plt.title(_title)
        plt.xlabel(_xlabel)
        plt.ylabel(_ylabel)

        if _show:
            plt.show()
        if _save:
            # fig = plt.gcf()
            # fig.set_size_inches(16, 9)
            # fig.savefig(f'_plot.png', dpi=100)
            plt.savefig(_savepath)
        return None
