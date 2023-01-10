import os
import time
from numbers import Number
import pytest
from . import utils
from ...concurrent.interrupt import StopPypushflowTask


def create_file(sleep_time: Number, filename: str) -> str:
    time.sleep(sleep_time)
    with open(filename, "w"):
        pass
    return filename


@pytest.mark.parametrize("scaling", [True, False])
@pytest.mark.parametrize("max_workers", [None, 1])
@pytest.mark.parametrize("pool_type", utils.POOLS)
def test_interrupt(scaling, max_workers, pool_type, tmpdir):
    if pool_type == "thread":
        pytest.skip("threads cannot be interrupted")
    if os.name == "nt" and pool_type in (
        "process",
        "ndprocess",
        "multiprocessing",
        "ndmultiprocessing",
        "billiard",
    ):
        pytest.skip("not supported on windows")

    callback_event = utils.Event()
    exception = None
    result = None

    def reset():
        nonlocal result
        nonlocal exception
        result = None
        exception = None
        callback_event.reset()

    def callback(r):
        nonlocal result
        result = r
        callback_event.set()

    def error_callback(e):
        nonlocal exception
        exception = e
        callback_event.set()

    def run_normal(filename):
        nonlocal result
        reset()
        pool.apply_async(
            create_file,
            args=(0, str(filename)),
            callback=callback,
            error_callback=error_callback,
        )
        callback_event.wait(10)
        assert result == str(filename)
        assert filename.exists()

    def run_interrupt(filename):
        nonlocal exception
        reset()
        pool.apply_async(
            create_file,
            args=(5, str(filename)),
            callback=callback,
            error_callback=error_callback,
        )
        time.sleep(2)
        pool.interrupt()
        callback_event.wait(10)
        assert isinstance(exception, StopPypushflowTask), str(type(exception))
        assert not filename.exists()

    with utils.pool_context(scaling, pool_type, max_workers=max_workers) as pool:
        run_normal(tmpdir / "test1.txt")
        run_interrupt(tmpdir / "test2.txt")
        run_interrupt(tmpdir / "test3.txt")
        run_normal(tmpdir / "test4.txt")
