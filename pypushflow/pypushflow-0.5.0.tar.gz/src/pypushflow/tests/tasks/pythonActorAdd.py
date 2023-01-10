import time


def run(value=None, **kwargs):

    time.sleep(1)
    if value is None:
        raise RuntimeError("Missing argument 'value'!")
    value = value + 1
    return {"value": value}
