from datetime import datetime
from typing import Optional
import pytz

from advancedLogger.contract import ITimeFormatter


class TimeFormatter(ITimeFormatter):
    def __init__(self, date_fmt: Optional[str] = "%Y-%m-%d", tz: Optional[pytz.BaseTzInfo] = pytz.UTC):
        self.__tz = tz
        self.__dt_fmt = date_fmt

    def get(self):
        return datetime.today().strftime(self.__dt_fmt)

    def convert(self, time: float):
        return datetime.fromtimestamp(time, self.__tz).strftime(self.__dt_fmt)
