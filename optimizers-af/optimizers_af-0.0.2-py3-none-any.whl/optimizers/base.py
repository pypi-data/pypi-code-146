from datetime import datetime

import numpy as np

from optimizers_af.logs.logged_object import LoggedObject


class Base(LoggedObject):
    """

    Parameters
    ----------
    func : callable
       An objective function with 1D-array as an argument.

    """

    def __init__(self, func: callable) -> None:
        self.history = []
        self.start = datetime.now()
        self.func = func

    def _get_time_from_start(self) -> int:
        return (datetime.now() - self.start).microseconds

    def fill_history(self) -> None:
        pass

    def run(self, point: np.ndarray):
        """

        Parameters
        ----------
        point : array-like
            An argument of the objective function
            that is 1D-array to be optimized.

        Returns
        -------
        parameters : array-like
            The optimized argument of the objective function.

        """
        self.start = datetime.now()
        self.history = [
            (point, self.func(point), self._get_time_from_start())
        ]
        try:
            self.fill_history()
        except (KeyboardInterrupt, SystemError):
            pass
        point, loss, optimization_time = self.history[-1]
        return point, loss, optimization_time
