import time

def wait(wait_time):
    """Suspends the current thread for a specified amount of time.

    Parameters
    ----------
    wait_time: float
        Wait time in seconds to suspend the current thread.
    """
    time_end = time.time() + wait_time  
    while time.time() < time_end:
        pass