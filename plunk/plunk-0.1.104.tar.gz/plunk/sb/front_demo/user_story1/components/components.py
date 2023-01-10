from dataclasses import dataclass
from front.elements import OutputBase
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
from sklearn.preprocessing import normalize
import soundfile as sf
from io import BytesIO


@dataclass
class AudioArrayDisplay(OutputBase):
    def render(self):
        sound, tag = self.output
        # if not isinstance(sound, str):
        if not isinstance(sound, bytes):

            sound = sound.getvalue()

        arr = sf.read(BytesIO(sound), dtype='int16')[0]
        # st.write(type(arr))
        tab1, tab2 = st.tabs(['Audio Player', 'Waveform'])
        with tab1:
            # if not isinstance(sound, bytes):
            #     sound = sound.getvalue()
            # arr = sf.read(BytesIO(sound), dtype="int16")[0]
            st.write(f'type of data={type(sound)}')

            st.audio(sound)
        with tab2:
            fig, ax = plt.subplots(figsize=(15, 5))
            ax.plot(arr, label=f'Tag={tag}')
            ax.legend()
            st.pyplot(fig)
            # st.write(arr[:10])


@dataclass
class GraphOutput(OutputBase):
    use_container_width: bool = False

    def render(self):
        # with st.expander(self.name, True): #cannot nest expanders
        dag = self.output
        st.graphviz_chart(
            figure_or_dot=dag.dot_digraph(),
            use_container_width=self.use_container_width,
        )


@dataclass
class ArrayPlotter(OutputBase):
    def render(self):
        X = self.output
        # st.write(f"Average score of session= {np.mean(X)}")
        fig, ax = plt.subplots(figsize=(15, 5))
        ax.plot(X)
        ax.legend()
        st.pyplot(fig)


@dataclass
class ArrayWithIntervalsPlotter(OutputBase):
    def render(self):
        X, intervals = self.output
        fig = pyplot_with_intervals(X, intervals)
        st.pyplot(fig)


def pyplot_with_intervals(X, intervals=None):
    min_x = np.mean(X)
    xs = list(range(len(X)))
    ys = X
    fig, ax = plt.subplots(figsize=(7, 2))
    ax.plot(xs, ys, linewidth=1)
    if intervals:
        for i, interval in enumerate(intervals):
            start, end = interval
            plt.axvspan(start, end, facecolor='g', alpha=0.5)

            ax.annotate(f'{i}', xy=(start, min_x), ha='left', va='top')
    return fig
