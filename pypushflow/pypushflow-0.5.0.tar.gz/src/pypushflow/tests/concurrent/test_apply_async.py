import pytest
from . import utils


def add(a, b):
    return a + b


def error(a, b):
    raise RuntimeError("intentional error")


FUNCTIONS = {"add": add, "error": error}


@pytest.mark.parametrize("scaling", [True, False])
@pytest.mark.parametrize("max_workers", [None, 1])
@pytest.mark.parametrize("pool_type", utils.POOLS)
@pytest.mark.parametrize("func", ["add", "error"])
def test_apply_async(scaling, max_workers, pool_type, func):
    callback_event = utils.Event()
    failed_msg = ""

    def result_callback(return_value):
        nonlocal failed_msg
        try:
            if return_value != 2:
                failed_msg = f"{return_value} != 2"
        finally:
            callback_event.set()

    def error_callback(exception):
        nonlocal failed_msg
        try:
            if not isinstance(exception, RuntimeError):
                failed_msg = f"{exception} is not a RuntimeError"
            elif str(exception) != "intentional error":
                failed_msg = f"'{exception}' != 'intentional error'"
        finally:
            callback_event.set()

    with utils.pool_context(scaling, pool_type, max_workers=max_workers) as pool:
        pool.apply_async(
            FUNCTIONS[func],
            args=(1, 1),
            callback=result_callback,
            error_callback=error_callback,
        )
        callback_event.wait(10)
        assert not failed_msg, failed_msg
