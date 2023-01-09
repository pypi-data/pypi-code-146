from __future__ import annotations

__all__ = [
    "Axes",
    "Array",
    "DataFrame",
    "Figure",
    "Series",
]

import numpy as np
import numpy.typing as npt
import pandas as pd
from matplotlib.axes import Axes
from matplotlib.figure import Figure
from typing_extensions import TypeAlias

Array: TypeAlias = npt.NDArray[np.float64]
Series: TypeAlias = pd.Series
DataFrame: TypeAlias = pd.DataFrame
