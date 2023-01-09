import asyncio
from websockets import connect
from stream2py.simply import mk_stream_buffer
import pandas as pd
import streamlit as st
import json
from collections import deque

df = pd.DataFrame()
df['value'] = 0.0

URI = 'ws://192.168.1.3:8081/sensor/connect?type=android.sensor.accelerometer'


def init_deque(maxlen=20):
    zeros = [0 for _ in range(maxlen)]
    d = deque(zeros, maxlen=maxlen)
    return d


st.title('Accelerometer')

data_deque = init_deque()
df['value'] = data_deque
# st.session_state["d"] = df
# st.write(st.session_state["d"])


async def accelerometer(uri=URI):
    # st.write(df)
    async with connect(uri) as websocket:
        while True:
            data = await websocket.recv()
            result = json.loads(data)['values'][0]
            data_deque.append(result)
            df['value'] = data_deque
            # st.session_state["d"] = df
            # st.write(data_deque)
            # st.write(df)

            # print(data)
            # with mk_stream_buffer(
            #     read_stream=lambda open_inst: data,
            #     open_stream=lambda: print("open"),
            #     close_stream=lambda open_inst: print("close"),
            #     auto_drop=False,
            #     maxlen=200,
            # ) as count_stream_buffer:
            #     count_reader = count_stream_buffer.mk_reader()
            #     print(f"start reading {count_reader.source_reader_info}")
            #     for i in count_reader:
            #         # do stuff with read data
            #         print(i)
            #         if count_stream_buffer.auto_drop is False:
            #             count_stream_buffer.drop()

            #     print("done reading")


# test = st.empty()
# status = st.empty()
# start = st.checkbox("Connect to WS Server")

# asyncio.run(accelerometer(test))
start = True
if start:
    asyncio.run(accelerometer())

placeholder = st.empty()
with placeholder.container():
    st.write(df)
