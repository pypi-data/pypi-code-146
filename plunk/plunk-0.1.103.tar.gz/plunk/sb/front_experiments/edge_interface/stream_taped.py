import pandas as pd
import plotly.express as px
import streamlit as st
import numpy as np
from utils import discretize, mk_audio_stream
import time
from taped import LiveWf, simple_chunker
from taped.base import WfChunks
from lined import Pipeline, iterize
from functools import partial

DFLT_CHK_SIZE = 2048 * 4

# simple ML functions
def chk_to_fv(chk):
    return np.std(chk)


def process_chk(chk):
    return chk_to_fv(chk)


featurizer = np.std
chunker = partial(simple_chunker, chk_size=2048)
p = Pipeline(chunker, iterize(featurizer))


# page config
st.set_page_config(
    page_title='Stream a dataframe', layout='wide',
)

# dashboard title
st.title('Stream a dataframe')

# creating a single-element container
placeholder = st.empty()

# live data

i = 0
with LiveWf() as live_wf:
    while True:
        with placeholder.container():
            i += 5
            chks = live_wf[i : i + 100]

            # chks = p(live_wf[i : i + 100])

            dataL = chks
            d = {'sound': dataL}
            # fig = px.line(
            #     data_frame=pd.DataFrame(d),
            #     x=range(200),
            #     y="sound",
            #     range_y=[0, 1000],
            # )
            # st.write(fig)
            st.bar_chart(dataL)
