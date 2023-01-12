import time
import datetime as dt


def wait(target_time):
    """Wait until a specified time.

    Args:
        target_time (str): Time in ISO format to wait until,
            i.e. "2015-10-21T07:28:00"

    """
    t0 = dt.datetime.now()
    t1 = dt.datetime.fromisoformat(target_time)

    assert t1 > t0, f"time {t1} is in the past"

    diff = t1 - t0
    print(f"Waiting for {diff.total_seconds()} seconds")
    time.sleep(diff.total_seconds())
