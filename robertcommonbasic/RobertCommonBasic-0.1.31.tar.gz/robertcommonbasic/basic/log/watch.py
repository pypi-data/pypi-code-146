from datetime import datetime
from functools import reduce
from operator import add as operator_add
from typing import Optional


class Stopwatch:
    def __init__(self, name: Optional[str] = None):
        self._laps = []
        self._lap_start_time = None
        self._lap_name = name

    def start_lap(self, name: str, restart: bool = False):
        now_time = datetime.now()
        if restart:
            self._laps.clear()
        else:
            self._record_last_lap(now_time)

        self._lap_name = name
        self._lap_start_time = now_time

    def stop(self):
        self._record_last_lap(datetime.now())

    def get_total_seconds(self):
        return reduce(operator_add, (lap[1].total_seconds() for lap in self._laps))

    def dump(self, threshold=0) -> str:
        self.stop()
        laps_text = ", ".join(
            (f"{lap_name}={duration.total_seconds():.3f}"
             for lap_name, duration in self._laps if duration.total_seconds() >= threshold))
        return f"total: {self.get_total_seconds():.3f}, laps: {laps_text}"

    def _record_last_lap(self, end_time: datetime):
        if self._lap_name and self._lap_start_time:
            self._laps.append((self._lap_name, end_time - self._lap_start_time))
            self._lap_name = None
            self._lap_start_time = None
