import importlib
from pathlib import Path
from types import ModuleType

import numpy as np


def load_module(path: Path, name: str, execute: bool = True) -> ModuleType:
    """Load the moduled named name from the given path. Also execute it if execute flag is true."""

    loader = importlib.machinery.SourceFileLoader(
        name, str(path / (name + ".py"))
    )
    spec = importlib.util.spec_from_loader(name, loader)
    mod = importlib.util.module_from_spec(spec)

    if execute:
        loader.exec_module(mod)

    return mod


# taken from https://stackoverflow.com/questions/20027936/how-to-efficiently-concatenate-many-arange-calls-in-numpy
def multirange(counts: np.ndarray) -> np.ndarray:
    # [2, 4, 1] -> [0, 1, 0, 1, 2, 3, 0]
    counts1 = counts[:-1]
    reset_index = np.cumsum(counts1)

    incr = np.ones(counts.sum(), dtype=int)
    incr[0] = 0
    incr[reset_index] = 1 - counts1

    # Reuse the incr array for the final result.
    incr.cumsum(out=incr)
    return incr
