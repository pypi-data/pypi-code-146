import warnings

from mltraq import options
from mltraq.extras.environment import is_pyodide, is_tty

with warnings.catch_warnings():
    warnings.simplefilter("ignore")

    from tqdm.auto import tqdm

    if is_pyodide():
        tqdm.monitor_interval = 0


disable = not is_tty() or options.get("tqdm.disable")


def progress(*args, **kwargs):
    return tqdm(*args, **kwargs, leave=False, delay=options.get("tqdm.delay"), disable=disable)
