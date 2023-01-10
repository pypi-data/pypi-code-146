import websocket
import json
from typing import Any
from collections import deque

# use SourceReader, check the audio one (audiostream2py)


def on_message(self):
    def wrapped(
        ws, message
    ):  # add incoming data to a standard deque: standard attribute to the SourceReader, so the read would read from the deque and pop data
        result = json.loads(message)
        values = result['values']
        bt = result['timestamp']
        x = values[0]
        d = {'bt': bt, 'acc_x': x}
        self.data.append(d)
        # source.emit(x)
        # print(d)

    return wrapped


def on_error(ws, error):
    print('error occurred')
    print(error)


def on_close(ws, close_code, reason):
    print('connection close')
    print('close code : ', close_code)
    print('reason : ', reason)


def on_open(ws):
    print('connection open')


DFLT_URL = 'ws://192.168.1.3:8080/sensor/connect?type=android.sensor.accelerometer'
DFLT_DEQUE_SIZE = 5


class AccelSource:
    """The interface for the StreamSource class."""

    def __init__(self, url, deque_size=DFLT_DEQUE_SIZE):
        self.url = url
        self.data = deque(maxlen=deque_size)

    def key(self, data) -> Any:
        ...

    @property
    def info(self) -> dict:
        return {}

    @property
    def sleep_time_on_read_none_s(self) -> int:
        return 0

    def read(self) -> Any:
        data = self.data.popleft()
        print(f'data retrieved = {data}')
        return data

    def open(self) -> None:
        self.ws = websocket.WebSocketApp(  # put it in open
            self.url,  # "ws://192.168.1.1:56478/sensor/connect?type=android.sensor.accelerometer",
            on_open=on_open,
            on_message=on_message(self),
            on_error=on_error,
            on_close=on_close,
        )
        self.ws.run_forever()

    def close(self) -> None:
        self.ws.close()


if __name__ == '__main__':
    stream = AccelSource(url=DFLT_URL)
    stream.open()
    stream.read()
    stream.close()
