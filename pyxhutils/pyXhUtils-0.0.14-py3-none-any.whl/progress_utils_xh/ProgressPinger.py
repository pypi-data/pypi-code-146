import datetime as dt
from typing import Callable


class ProgressPinger:
    def __init__(self, print_every_n_count: int = 100, print_every_n_second: int = 15):
        self.count = 0
        self.lastUpdate = dt.datetime.now()
        self.print_every_n_count = print_every_n_count
        self.print_every_n_second = print_every_n_second

    def ping(self):
        self.count += 1

        printed = False
        if self.count % self.print_every_n_count == 0:
            ProgressPinger.print_log(f"Processed count: {self.print_every_n_count}")
            printed = True

        if not printed and self.lastUpdate + dt.timedelta(seconds=self.print_every_n_second) < dt.datetime.now():
            ProgressPinger.print_log(f"Processed count: {self.print_every_n_count}")

        self.lastUpdate = dt.datetime.now()

    @staticmethod
    def log_formatting(msg: str) -> str:
        return f"[{dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {msg}"

    @staticmethod
    def print_log(msg: str, formatting: Callable[[str], str] = log_formatting):
        print(formatting(msg))
