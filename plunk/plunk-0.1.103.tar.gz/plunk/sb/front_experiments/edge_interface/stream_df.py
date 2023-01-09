import time
import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(
    page_title='Stream a dataframe', layout='wide',
)

# read csv from local folder
dataset_path = 'data/accel_data.csv'


@st.experimental_memo
def get_data(filepath) -> pd.DataFrame:
    return pd.read_csv(filepath, sep=';')


df = get_data(dataset_path)
min_data = df['ACC_Y'].min()
max_data = df['ACC_Y'].max()

# dashboard title
st.title('Stream a dataframe')


# creating a single-element container
placeholder = st.empty()

# simulate live data
for seconds in range(200):

    vals = df['ACC_Y'].iloc[seconds : seconds + 30].values
    d = {'ACC_Y': vals}
    with placeholder.container():
        fig = px.line(
            data_frame=pd.DataFrame(d),
            x=range(30),
            y='ACC_Y',
            range_y=[min_data, max_data],
        )
        st.write(fig)

        time.sleep(0.1)
