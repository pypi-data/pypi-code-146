from datetime import timedelta
from time import time


class MeasureTime:
    def __init__(self):
        self.start = self.end = 0

    def __enter__(self):
        self.start = time()
        return self

    def __exit__(self, *args, **kwargs):
        self.end = time()

    @property
    def delta(self) -> float:
        return round(self.duration.total_seconds(), 3)

    @property
    def duration(self) -> timedelta:
        return timedelta(seconds=self.end - self.start)
