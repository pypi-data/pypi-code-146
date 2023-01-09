"""
Simple example of streaming live accelerometer data from android phone
Android app: see https://github.com/umer0586/SensorServer
"""


import websocket
import json

# use SourceReader, check the audio one (audiostream2py)
def on_message(
    ws, message
):  # add incoming data to a standard deque: standard attribute to the SourceReader, so the read would read from the deque and pop data
    result = json.loads(message)
    values = result['values']
    bt = result['timestamp']
    x = values[0]
    d = {'bt': bt, 'acc_x': x}

    # source.emit(x)
    print(d)


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
    ws = websocket.WebSocketApp(  # put it in open
        'ws://192.168.1.3:8080/sensor/connect?type=android.sensor.accelerometer',
        # "ws://192.168.1.1:56478/sensor/connect?type=android.sensor.accelerometer",
        on_open=on_open,
        on_message=on_message,
        on_error=on_error,
        on_close=on_close,
    )

    ws.run_forever()  # may be stop the signal at some point, the close()
