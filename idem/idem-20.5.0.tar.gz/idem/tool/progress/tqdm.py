from typing import Iterable

try:
    from tqdm.auto import tqdm

    HAS_LIBS = (True,)
except ImportError as e:
    HAS_LIBS = False, str(e)


def __virtual__(hub):
    return HAS_LIBS


def create(hub, iterable: Iterable, **kwargs) -> Iterable:
    """
    Create a tqdm progress bar that updates as the iterable is iterated
    """
    progress_bar = tqdm(
        iterable,
        **kwargs,
    )

    return progress_bar


def update(hub, progress_bar: Iterable, **kwargs):
    if not isinstance(progress_bar, tqdm):
        return
    progress_bar.update(**kwargs)
