import requests
from datetime import datetime, timezone
import math
from typing import NamedTuple


class PumpData(NamedTuple):
    speed: int
    power: int
    on: bool


class Pump:
    _default_timeout = 2

    def __init__(self, base_url):
        self.base_url = base_url

    def get_data(self):
        utc_now = math.floor(datetime.now(timezone.utc).timestamp() * 1000)
        api_url = f'{self.base_url}/cgi-bin/EpvCgi?name=AllRd&val=0&type=get&time={utc_now}'
        response = requests.get(api_url, timeout=self._default_timeout)
        response.raise_for_status()
        json = response.json()
        data = PumpData(int(json["CurrentSpeed"]),
                        int(json["CurrentWatts"]), json["RunningStatus"] == '1')
        return data

    def set_speed(self, speed):
        utc_now = math.floor(datetime.now(timezone.utc).timestamp() * 1000)
        api_url = f'{self.base_url}/cgi-bin/EpvCgi?name=SetCurrentSpeed&val={speed}&type=set&time={utc_now}'
        response = requests.get(api_url, timeout=self._default_timeout)
        response.raise_for_status()
        return response.json()

    def turn_on(self):
        utc_now = math.floor(datetime.now(timezone.utc).timestamp() * 1000)
        api_url = f'{self.base_url}/cgi-bin/EpvCgi?name=RunStop&val=1&type=set&time={utc_now}'
        response = requests.get(api_url, timeout=self._default_timeout)
        response.raise_for_status()
        return response.json()

    def turn_off(self):
        utc_now = math.floor(datetime.now(timezone.utc).timestamp() * 1000)
        api_url = f'{self.base_url}/cgi-bin/EpvCgi?name=RunStop&val=2&type=set&time={utc_now}'
        response = requests.get(api_url, timeout=self._default_timeout)
        response.raise_for_status()
        return response.json()
