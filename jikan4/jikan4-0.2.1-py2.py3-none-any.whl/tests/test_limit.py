import pytest
import time

from jikan4.utils.limiter import Limiter


def test_limiter():
    limiter = Limiter(
        calls_limit=3, period=2, spread=False
    )  # Make 3 calls wait 2 seconds and then make the last 2 calls

    @limiter
    def test_limiter():
        pass

    start = time.time()
    for _ in range(5):
        test_limiter()
    end = time.time()

    elapsed = end - start
    expected = 2

    assert expected < elapsed < expected + 1, "Rate limit not working"


def test_limiter_spread():
    limiter = Limiter(
        calls_limit=3, period=2, spread=True
    )  # Make 1 call each 2/3 seconds (3 calls for 2 seconds) until complete 5 calls

    @limiter
    def test_limiter():
        pass

    start = time.time()
    for _ in range(5):
        test_limiter()
    end = time.time()

    elapsed = end - start
    expected = (2 / 3) * 4  # First call is instant

    assert expected < elapsed < expected + 1, "Rate limit not working"
