"""Render a stream"""
import datetime
import time
from collections import defaultdict, deque
from dataclasses import dataclass
from functools import partial
from typing import List, DefaultDict, Iterable, Union

from audiostream2py import PyAudioSourceReader

import streamlit as st
from front import APP_KEY, RENDERING_KEY, ELEMENT_KEY, Crudifier, NAME_KEY
from front.elements import OutputBase
import matplotlib.pyplot as plt
from plunk.ap.snippets import prefill_deque_with_value
from stream2py import StreamBuffer, BufferReader

from streamlitfront import mk_app, binder as b
from streamlitfront.elements import SelectBox

from plunk.ap.live_graph.live_graph_data_buffer import (
    mk_live_graph_data_buffer,
    GRAPH_TYPES,
)

if not b.mall():
    b.mall = dict(source=None,)

mall = b.mall()
if not b.input_devices():
    b.input_devices = PyAudioSourceReader.list_recording_devices()
crudifier = partial(Crudifier, mall=mall)


def time_string(timestamp):
    st.markdown(f'## time: {str(datetime.datetime.fromtimestamp(timestamp / 1e6))}')


def line_plot(graph_data: Iterable[Union[int, float]], title: str, figsize=(15, 5)):
    fig, ax = plt.subplots(figsize=figsize)
    st.markdown(f'## {title}')
    ax.plot(graph_data)
    st.pyplot(fig)
    plt.close(fig)


PLOT_TYPES = {'line': line_plot}


def plot(graph_type: str, graph_data: Iterable[Union[int, float]]):
    """Checks for plot type and draws plot

    :param graph_type:
    :param graph_data:
    :return:
    """
    plot_type = GRAPH_TYPES[graph_type]['plot']
    PLOT_TYPES[plot_type](graph_data, title=graph_type)


@dataclass
class DataGraph(OutputBase):
    output: StreamBuffer = None
    plots_data: DefaultDict[str, deque] = None

    def prefill_plots_data(self, data_reader: BufferReader, fill_value=0):
        """Prefill data upto the expected plot data window size

        :param data_reader:
        :param fill_value:
        :return:
        """
        pd = prefill_deque_with_value(
            value=0, maxlen=data_reader._buffer._sorted_deque.maxlen
        )
        self.plots_data = defaultdict(pd.copy)
        data_list = data_reader.range(
            fill_value, time.time() * 1e6, peek=True, ignore_no_item_found=True
        )
        if data_list is not None:
            for d in data_list:
                self.append_plots_data(d)

    def append_plots_data(self, data: dict):
        """Parse by graph type and add data point to plots_data

        :param data: dict(timestamp=1, volume=2, zero_crossing_ratio=3)
        :return:
        """
        for k, v in data.items():
            if k in GRAPH_TYPES and v is not None:
                self.plots_data[k].append(v)

    def timestamp(self, data_reader: BufferReader, data: dict):
        """Get timestamp using SourceReader key function

        :param data_reader:
        :param data: dict(timestamp=1, volume=2, zero_crossing_ratio=3)
        :return:
        """
        key = data_reader._buffer.key
        return key(data)

    def render(self):
        if self.output:
            box = st.empty()
            i = 0
            data_reader = self.output.mk_reader(
                read_size=self.output._maxlen, ignore_no_item_found=True
            )
            self.prefill_plots_data(data_reader)
            while self.output.is_running:
                if (data_list := data_reader.read()) is not None:
                    # print(f'{len(data_list)=}')
                    for data in data_list:
                        self.append_plots_data(data)
                        i += 1
                    timestamp = self.timestamp(data_reader, data)
                    print(f'rendering...({i})')
                    with box.container():
                        for graph_type, graph_data in self.plots_data.items():
                            plot(graph_type, graph_data)
                        time_string(timestamp)
                else:
                    time.sleep(0.1)
                    # print('sleeping...')
            print('exit render')


def stop_stream():
    if mall['source']:
        try:
            mall['source'].stop()
            mall['source'] = None
        except Exception as e:
            print(e)


@crudifier(output_store='source')
def data_stream(
    input_device=None,
    rate=44100,
    width=2,
    channels=1,
    frames_per_buffer=44100,
    seconds_to_keep_in_stream_buffer=60,
    graph_types='volume',
):
    stop_stream()
    source = mk_live_graph_data_buffer(
        input_device,
        rate,
        width,
        channels,
        frames_per_buffer,
        seconds_to_keep_in_stream_buffer,
        graph_types,
    )
    source.start()
    return source


if __name__ == '__main__':
    app = mk_app(
        [data_stream, stop_stream],
        config={
            APP_KEY: {'title': 'My Stream App'},
            RENDERING_KEY: {
                'data_stream': {
                    NAME_KEY: 'Get Data Stream',
                    'description': {'content': 'Configure soundcard for data stream'},
                    'execution': {
                        'inputs': {
                            'input_device': {
                                ELEMENT_KEY: SelectBox,
                                'options': b.input_devices(),
                            },
                            'graph_types': {  # TODO option to select more than one graph type
                                ELEMENT_KEY: SelectBox,
                                'options': list(GRAPH_TYPES),
                            },
                        },
                        'output': {ELEMENT_KEY: DataGraph},
                    },
                },
            },
        },
    )
    app()
