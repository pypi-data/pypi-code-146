import asyncio
import time


class AsyncLimiter:
    def __init__(self, calls_limit: int = 5, period: int = 1, spread: bool = False):
        if spread:
            self.calls_limit = 1
            self.period = period / calls_limit
        else:
            self.calls_limit = calls_limit
            self.period = period

        self.semaphore = asyncio.Semaphore(calls_limit)
        self.requests_finish_time = []

    async def sleep(self):
        if len(self.requests_finish_time) >= self.calls_limit:
            sleep_before = self.requests_finish_time.pop(0)
            if sleep_before >= time.monotonic():
                await asyncio.sleep(sleep_before - time.monotonic())

    def __call__(self, func):
        async def wrapper(*args, **kwargs):

            async with self.semaphore:
                await self.sleep()
                res = await func(*args, **kwargs)
                self.requests_finish_time.append(time.monotonic() + self.period)

            return res

        return wrapper
