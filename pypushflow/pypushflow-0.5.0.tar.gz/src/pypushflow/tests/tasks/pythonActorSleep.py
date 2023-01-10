from time import sleep


def run(**kwargs):
    sleep(kwargs.get("sleep_time", 0))
    return kwargs
