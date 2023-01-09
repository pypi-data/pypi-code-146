import pandas as pd
import plotly.express as px
import streamlit as st
import numpy as np
from utils import discretize, mk_audio_stream
import time

st.set_page_config(
    page_title='Stream a dataframe', layout='wide',
)

# create live stream from microphone
stream = mk_audio_stream()


# dashboard title
st.title('Stream a dataframe')


# creating a single-element container
placeholder = st.empty()

# live data
while True:
    time.sleep(0.1)

    data = np.frombuffer(stream.read(1024, exception_on_overflow=False), dtype=np.int16)

    dataL = discretize(data[0::2], func=np.std)

    d = {'sound': dataL}
    with placeholder.container():
        # fig = px.line(
        #     data_frame=pd.DataFrame(d),
        #     x=range(200),
        #     y="sound",
        #     range_y=[0, 1000],
        # )
        # st.write(fig)
        st.bar_chart(dataL)
