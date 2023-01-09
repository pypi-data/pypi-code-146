"""Webservice for Volume and Zero Crossing"""
import time
from typing import Generator, Dict, Union
from dataclasses import dataclass
from itertools import count

import numpy as np
from audiostream2py import PyAudioSourceReader
from taped import LiveWf

_stream: Dict[str, Union[Generator, None]] = dict(source=None)


def volume(chk):
    return np.std(chk)


def zero_crossing_ratio(chk):
    return sum(np.diff(np.array(chk) > 0).astype(int)) / (len(chk) - 1)


@dataclass
class AudioGraphData:
    graph_type: str = 'volume'
    refresh_rate_s: float = 0.5
    window_time_s: float = 5
    output: LiveWf = None

    GRAPH_TYPES = {
        'volume': {'function': volume, 'chk_size': 2048, 'chk_step': 512},
        'zero_crossing_ration': {
            'function': zero_crossing_ratio,
            'chk_size': 1000,
            'chk_step': None,
        },
    }

    @classmethod
    def chunk_indices(cls, chk_size=2048, chk_step=None, *, start=0, stop=None):
        """
        >>> list(chunk_indices(10, 5, stop=30))
        [(0, 10), (5, 15), (10, 20), (15, 25), (20, 30), (25, 35)]
        """
        chk_step = chk_step or chk_size
        i_gen = (
            range(start, stop, chk_step) if stop is not None else count(start, chk_step)
        )
        for i in i_gen:
            yield i, i + chk_size

    @classmethod
    def data_window(cls, window_data, *, function, chk_size, chk_step):
        return [
            function(window_data[slice(*chk_idx)])
            for chk_idx in cls.chunk_indices(chk_size, chk_step, stop=len(window_data))
        ]

    def window_data_gen(self):
        """Generate last window_time_s worth of waveform
        """
        while self.output.is_running:
            n_window_samples = self.output.sr * self.window_time_s
            d_idx = int(min(n_window_samples, self.output.available_samples_in_buffer))
            if not d_idx:
                print('sleep')
                time.sleep(self.refresh_rate_s)
                continue
            yield self.window_timestamp(d_idx), self.output[-d_idx:-1]

    def window_timestamp(self, n_window_samples: int):
        reader = self.output.mk_reader()
        ts, _ = reader.tail()
        n_samples_before_ts = n_window_samples - self.output.chk_size
        window_ts = int(ts - n_samples_before_ts / self.output.sr * 1e6)
        return window_ts


def go(input_device=None, window_time_s=5, refresh_rate_s=0.5):
    with LiveWf(input_device_index=input_device) as live_wf:
        graph_data = AudioGraphData(
            refresh_rate_s=refresh_rate_s, window_time_s=window_time_s, output=live_wf
        )
        for window_timestamp, window_data in graph_data.window_data_gen():
            window = {
                graph_type: graph_data.data_window(window_data, **kwargs)
                for graph_type, kwargs in graph_data.GRAPH_TYPES.items()
            }
            window['timestamp'] = window_timestamp
            yield window


def start_stream(input_device=None, window_time_s=5, refresh_rate_s=0.5):
    _stream['source'] = go(
        input_device=input_device,
        window_time_s=window_time_s,
        refresh_rate_s=refresh_rate_s,
    )
    return 'starting'


def stop_stream():
    if _stream['source'] is not None:
        try:
            _stream['source'].close()
        finally:
            _stream['source'] = None
    return 'stopped'


def output():
    """Returns the output"""
    # if not _stream['source']:
    #     # auto start if not started
    #     start_stream()
    return next(_stream['source'])


# Make a list of functions or instance methods
func_list = [
    start_stream,
    output,
    stop_stream,
    PyAudioSourceReader.list_recording_devices,
]

if __name__ == '__main__':
    # Create an HTTP server
    from py2http.service import run_app

    # TODO: Improvement of webservice with state manager
    start_stream(input_device='NexiGo N930AF FHD Webcam Audio')

    run_app(func_list, http_method='get')
