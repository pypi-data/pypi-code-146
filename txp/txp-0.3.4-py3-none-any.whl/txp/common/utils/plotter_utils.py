from scipy.fft import fft, fftfreq
import numpy as np
from scipy.fft import fft
import matplotlib.pyplot as plt


class FFTPlotter:
    """Fft plotter util.

    Defines a plotter utility class for plotting fft signals.

    Args:
        signal_amplitude_axis: Amplitude axis of the signal, if this argument is None
        then signal_frequency_amplitude_axis has to be given.

        signal_frequency_amplitude_axis: Precalculated fft, if fft has to be calculated within
        the plotter, then this Argument has to be set as None.

        sampling_frequency: frequency of sampling of the signal.
    """

    def __init__(self, signal_amplitude_axis: np.ndarray, signal_frequency_amplitude_axis,
                 sampling_frequency: float):

        if signal_amplitude_axis is None and signal_frequency_amplitude_axis is None:
            raise Exception("signal_amplitude_axis and signal_frequency_amplitude_axis both None")

        self.signal_amplitude_axis = signal_amplitude_axis
        self.signal_frequency_amplitude_axis = signal_frequency_amplitude_axis

        if self.signal_frequency_amplitude_axis is None:
            self.signal_frequency_amplitude_axis = fft(self.signal_amplitude_axis)

        self.sample_count = len(self.signal_frequency_amplitude_axis)

        assert self.sample_count == len(self.signal_frequency_amplitude_axis)
        self.sampling_frequency = sampling_frequency
        self.frequency_axis = fftfreq(self.sample_count, 1 / self.sampling_frequency)
        self.frequency_axis_indices = self.frequency_axis > 0
        self.frequency_axis = self.frequency_axis[self.frequency_axis_indices]
        self.signal_frequency_amplitude_axis = self.signal_frequency_amplitude_axis[self.frequency_axis_indices]

    def plot(self, title, semilogy=False, x_scale=None):
        """Plots fft.
        Args:
            title: tittle for the plot.
            semilogy: If fft needs to be plotted in semi logarithmic scale this argument must be set as True.
            x_scale: x ticks for plotting
        Returns:
            Plotting figure
        """
        fig = plt.figure(figsize=(23, 10))
        fig.suptitle(title, fontsize=20)
        if x_scale is not None:
            plt.xticks(np.arange(0, max(self.frequency_axis) + x_scale, x_scale))
        if semilogy:
            plt.semilogy(self.frequency_axis, 2.0 / self.sample_count * np.abs(self.signal_frequency_amplitude_axis),
                         '-b')
        else:
            plt.plot(self.frequency_axis, 2.0 / self.sample_count * np.abs(self.signal_frequency_amplitude_axis), '-b')
        plt.legend(['FFT'])
        return fig


class PSDPlotter:

    def __init__(self, frequency, psd):
        self.frequency = frequency
        self.psd = psd

    def plot(self, title, semilogy=False, x_scale=None):

        fig = plt.figure(figsize=(23, 10))
        fig.suptitle(title, fontsize=20)
        if x_scale is not None:
            plt.xticks(np.arange(0, max(self.frequency) + x_scale, x_scale))
        if semilogy:
            plt.semilogy(self.frequency, self.psd, '-r')
        else:
            plt.plot(self.frequency, self.psd, '-r')
        plt.legend(['PSD'])
        return fig
