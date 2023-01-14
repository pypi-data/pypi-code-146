"""Statistical Funtions for aggregation."""
from abc import ABC
from abc import abstractmethod
from dataclasses import dataclass
from typing import Any

import numpy as np
import numpy.typing as npt


@dataclass
class StatsMethod(ABC):
    """Abstract method for gdptools weighted stats."""

    @abstractmethod
    def get_stat(
        self,
    ) -> Any:
        """Abstract weighted method."""


@dataclass
class MAWeightedAverage(StatsMethod):
    """Weighted Average."""

    array: npt.NDArray
    weights: npt.NDArray[np.double]
    def_val: Any

    def get_stat(self) -> Any:
        """Get weighted masked average."""
        try:
            tmp = np.ma.average(self.array, weights=self.weights, axis=1)
        except KeyError:
            numpts = self.weights.shape[0]
            tmp = np.full((numpts), self.def_val)
        return tmp


@dataclass
class WeightedAverage(StatsMethod):
    """Weighted Average."""

    array: npt.NDArray
    weights: npt.NDArray[np.double]
    def_val: Any

    def get_stat(self) -> Any:
        """Get weighted masked average."""
        try:
            tmp = np.average(self.array, weights=self.weights, axis=1)
        except KeyError:
            numpts = self.weights.shape[0]
            tmp = np.full((numpts), self.def_val)
        return tmp
