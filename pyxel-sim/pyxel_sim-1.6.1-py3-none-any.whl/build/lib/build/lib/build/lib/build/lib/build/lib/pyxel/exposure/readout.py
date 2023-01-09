#  Copyright (c) European Space Agency, 2017, 2018, 2019, 2020, 2021, 2022.
#
#  This file is subject to the terms and conditions defined in file 'LICENCE.txt', which
#  is part of this Pyxel package. No part of the package, including
#  this file, may be copied, modified, propagated, or distributed except according to
#  the terms contained in the file ‘LICENCE.txt’.
#
#
"""TBW."""

from typing import Any, Iterator, Optional, Sequence, Tuple, Union

import numpy as np

from pyxel import load_table
from pyxel.evaluator import eval_range


class Readout:
    """TBW.

    Parameters
    ----------
    times
    times_from_file
    start_time
    non_destructive
    """

    def __init__(
        self,
        times: Optional[Union[Sequence, str]] = None,
        times_from_file: Optional[str] = None,
        start_time: float = 0.0,
        non_destructive: bool = False,
    ):
        self._time_domain_simulation = True

        if times is not None and times_from_file is not None:
            raise ValueError("Both times and times_from_file specified. Choose one.")
        elif times is times_from_file is None:
            self._times = np.array(
                [1]
            )  # by convention default readout/exposure time is 1 second
            self._time_domain_simulation = False
        elif times_from_file:
            self._times = load_table(times_from_file).to_numpy(dtype=float).flatten()
        elif times:
            self._times = np.array(eval_range(times), dtype=float)
        else:
            raise ValueError("Sampling times not specified.")

        if self._times[0] == 0:
            raise ValueError("Readout times should be non-zero values.")
        elif start_time >= self._times[0]:
            raise ValueError("Readout times should be greater than start time.")

        self._non_destructive = non_destructive

        self._times_linear: bool = True
        self._start_time: float = start_time
        self._steps: np.ndarray = np.array([])
        self._num_steps: int = 0
        self._set_steps()

    def __repr__(self) -> str:
        cls_name: str = self.__class__.__name__
        return f"{cls_name}<num_steps={self._num_steps}>"

    def _set_steps(self) -> None:
        """TBW."""
        self._times, self._steps = calculate_steps(self._times, self._start_time)
        self._times_linear = bool(np.all(self._steps == self._steps[0]))
        self._num_steps = len(self._times)

    def time_step_it(self) -> Iterator[Tuple[float, float]]:
        """TBW."""
        return zip(self._times, self._steps)

    @property
    def start_time(self) -> float:
        """Return start time."""
        return self._start_time

    @start_time.setter
    def start_time(self, value: float) -> None:
        """Set start time."""
        if value >= self._times[0]:
            raise ValueError("Readout times should be greater than start time.")
        self._start_time = value
        self._set_steps()

    @property
    def times(self) -> Any:
        """Get readout times."""
        return self._times

    @times.setter
    def times(self, value: Union[Sequence, np.ndarray]) -> None:
        """Set readout times.

        Parameters
        ----------
        value
        """
        if value[0] == 0:
            raise ValueError("Readout times should be non-zero values.")
        elif self._start_time >= value[0]:
            raise ValueError("Readout times should be greater than start time.")
        self._times = np.array(value)
        self._set_steps()

    @property
    def time_domain_simulation(self) -> bool:
        """TBW."""
        return self._time_domain_simulation

    @property
    def steps(self) -> np.ndarray:
        """TBW."""
        return self._steps

    @property
    def non_destructive(self) -> bool:
        """Get non-destructive readout mode."""
        return self._non_destructive

    @non_destructive.setter
    def non_destructive(self, value: bool) -> None:
        """Set non-destructive mode."""
        self._non_destructive = value


def calculate_steps(
    times: np.ndarray, start_time: float
) -> Tuple[np.ndarray, np.ndarray]:
    """Calculate time differences for a given array and start time.

    Parameters
    ----------
    times: ndarray
    start_time: float

    Returns
    -------
    times: ndarray
        Modified times according to start time.
    steps: ndarray
        Steps corresponding to times.
    """
    steps = np.diff(
        np.concatenate((np.array([start_time]), times), axis=0),
        axis=0,
    )

    return times, steps
