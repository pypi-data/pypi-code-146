import websocket
import json
from streamz import Stream
from streamz.dataframe import DataFrame
import pandas as pd
import hvplot.streamz
from streamz.dataframe import Random
import datetime
import plotly.graph_objects as go

source = Stream()

df = pd.DataFrame({'x': []})
sdf = DataFrame(source, example=df)


def on_message(ws, message):
    values = json.loads(message)['values']
    x = values[0]
    y = values[1]
    z = values[2]
    source.emit(pd.DataFrame({'x': [float(x)]}, index=[pd.Timestamp.now()]))
    # source.emit(pd.DataFrame({"x": [x]},index=[datetime.datetime.now()]))


#     pd.DataFrame(dict(used=100*vmem.used/vmem.total,
#                              free=100*vmem.free/vmem.total),
#                         index=[pd.Timestamp.now()])
#     t = datetime.datetime.now()
#     times.append(t)
#     vals.append(float(x))
#     fig.data[0].x = times
#     fig.data[0].y = vals
# df = df.append(pd.DataFrame({"x": float(x)}, index=[t]))
# print(sdf.x.sum())


def on_error(ws, error):
    print('error occurred')
    print(error)


def on_close(ws, close_code, reason):
    print('connection close')
    print('close code : ', close_code)
    print('reason : ', reason)


def on_open(ws):
    print('connection open')


if __name__ == '__main__':
    ws = websocket.WebSocketApp(
        'ws://192.168.1.3:8080/sensor/connect?type=android.sensor.accelerometer',
        on_open=on_open,
        on_message=on_message,
        on_error=on_error,
        on_close=on_close,
    )
    sdf.hvplot(backlog=100)
    # sdf.hvplot()

    # fig.show()

    ws.run_forever()

# To analyse multiple sensor data simultaneously, you can add as many websocket connections for different sensors as you want.
