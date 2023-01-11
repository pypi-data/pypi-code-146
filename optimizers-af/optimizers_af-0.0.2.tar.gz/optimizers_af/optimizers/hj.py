"""
References
----------
1961.
R.Hooke, T.A.Jeeves.
``Direct Search'' Solution of Numerical and Statistical Problems.
doi:10.1145/321062.321069

"""

import numpy as np

from optimizers_af.optimizers.base import Base


class HookeJeeves(Base):

    def __init__(
            self,
            accuracy: float,
            initial_step_size: float,
            step_reduction_factor: float,
            **kwargs,
    ) -> None:
        super().__init__(**kwargs)
        self.accuracy = accuracy
        self.initial_step_size = initial_step_size
        if not 0 < step_reduction_factor < 1:
            raise ValueError('Wrong `step_reduction_factor` value.')
        self.step_reduction_factor = step_reduction_factor

    def __make_exploratory_move(
            self,
            point: np.ndarray,
            step_size: float,
    ) -> np.ndarray:
        old_loss = self.func(point)
        for i in range(point.size):
            if (i + 1) % 100 == 0:
                self.logger.info(
                    f'{i + 1}/{point.shape[0]} coordinates '
                    f'are processed at step {len(self.history)}...'
                )
            _steps = np.zeros(point.size)
            _steps[i] += step_size
            new_point = point + _steps
            new_loss = self.func(new_point)
            if self.func(new_point) < old_loss:
                point = new_point
                old_loss = new_loss
                continue
            new_point = point - _steps
            new_loss = self.func(new_point)
            if new_loss < old_loss:
                point = new_point
                old_loss = new_loss
        return point

    def fill_history(self) -> None:
        step_size = self.initial_step_size
        point_1, loss_1 = self.history[-1][:2]
        while step_size > self.accuracy:
            point_2 = self.__make_exploratory_move(
                point=point_1,
                step_size=step_size,
            )
            loss_2 = self.func(point_2)
            if loss_2 >= loss_1:
                step_size *= self.step_reduction_factor
                continue

            while True:
                point_3 = self.__make_exploratory_move(
                    point=2 * point_2 - point_1,
                    step_size=step_size,
                )
                loss_3 = self.func(point_3)
                if loss_3 >= loss_2:
                    point_1 = point_2
                    loss_1 = loss_2
                    break
                point_1, point_2 = point_2, point_3
                loss_1, loss_2 = loss_2, loss_3
            self.history.append(
                (point_2, loss_2, self._get_time_from_start())
            )
            self.logger.info(
                f'Step: {len(self.history) - 1}.'
                f' Loss: {self.history[-1][1]}.'
                f' Optimization Time: {self.history[-1][2]} msec.'
                f' Point: {str(self.history[-1][0])}.'
            )
