from datetime import datetime
from typing import Optional

import pytz


class TimeFormatter:
    def __init__(self, date_fmt: Optional[str] = "%Y-%m-%d", tz: Optional[pytz.BaseTzInfo] = pytz.UTC):
        self.__tz = tz
        self.__dt_fmt = date_fmt

    def get(self):
        return datetime.today().strftime(self.__dt_fmt)

    def convert(self, time: int):
        return datetime.fromtimestamp(time, self.__tz).strftime(self.__dt_fmt)
