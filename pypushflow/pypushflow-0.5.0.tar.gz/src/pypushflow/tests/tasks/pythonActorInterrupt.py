from time import sleep


def run(**kwargs):
    kwargs.setdefault("counter", 0)
    sleep(kwargs.get("sleep_time", 0))
    kwargs["counter"] += 1
    return kwargs
