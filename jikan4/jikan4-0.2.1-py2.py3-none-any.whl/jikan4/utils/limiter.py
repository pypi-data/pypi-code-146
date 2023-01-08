import time


class Limiter:
    def __init__(self, calls_limit: int = 5, period: int = 1, spread: bool = False):
        if spread:
            self.calls_limit = 1
            self.period = period / calls_limit

        else:
            self.calls_limit = calls_limit
            self.period = period

        self.calls = -1  # To make the first call not wait

    def __call__(self, func):
        def wrapper(*args, **kwargs):
            self.calls += 1
            if self.calls >= self.calls_limit:
                time.sleep(self.period)
                self.calls = 0

            res = func(*args, **kwargs)
            return res

        return wrapper
