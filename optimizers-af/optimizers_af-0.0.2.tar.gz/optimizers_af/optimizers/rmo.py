"""
References
----------
2014. R.Rahmani, R.Yusof.
A New Simple, Fast And Efficient Algorithm
For Global Optimization Over Continuous Search-Space Problems.
Radial Movement Optimization.
doi:10.1016/j.amc.2014.09.102

"""

from typing import Tuple

import numpy as np

from optimizers_af.optimizers.base import Base


class RadialMovementOptimization(Base):

    def __init__(
            self,
            generations_number: int,
            particles_number: int,
            bounds: Tuple[float, float],
            scale: int,
            c_parameters: Tuple[float, float],
            weight_limits: Tuple[float, float],
            **kwargs,
    ) -> None:
        super().__init__(**kwargs)
        self.generations_number = generations_number
        self.particles_number = particles_number
        self.bounds = bounds
        self.scale = scale
        self.c_parameters = c_parameters
        self.weight_limits = weight_limits

    def __generate_velocities(self, dimensions_number: int):
        return np.random.uniform(
            low=-1.0,
            size=(self.particles_number, dimensions_number)
        ) * (self.bounds[1] - self.bounds[0]) / self.scale

    def __get_weight(self, generation: int) -> float:
        return (
                self.weight_limits[1]
                - (self.weight_limits[1] - self.weight_limits[0])
                * generation / self.generations_number
        )

    def __get_constrained_locations(
            self,
            centre: np.ndarray,
            weight: float,
            velocities: np.ndarray,
            dimensions_number: int
    ) -> np.ndarray:
        locations = self.bounds[0] + np.random.uniform(
            size=(self.particles_number, dimensions_number)
        ) * (self.bounds[1] - self.bounds[0])
        for i in range(self.particles_number):
            for j in range(dimensions_number):
                locations[i][j] = centre[j] + weight * velocities[i][j]
                if locations[i][j] > self.bounds[1]:
                    locations[i][j] = self.bounds[1]
                if locations[i][j] < self.bounds[0]:
                    locations[i][j] = self.bounds[0]
        return locations

    def fill_history(self) -> None:
        centre, global_minimum = self.history[-1][:2]
        global_best, radial_best = np.array(centre), np.array(centre)
        temp = np.array(centre)
        self.logger.info(f'{global_minimum = :.5f}')
        for generation in range(self.generations_number):
            generation_minimum = self.func(centre)
            velocities = self.__generate_velocities(
                dimensions_number=centre.size,
            )
            weight = self.__get_weight(generation=generation)
            locations = self.__get_constrained_locations(
                centre=centre,
                weight=weight,
                velocities=velocities,
                dimensions_number=centre.size,
            )
            for _, location in enumerate(locations):
                loss = self.func(location)
                if loss < generation_minimum:
                    generation_minimum = loss
                    radial_best = np.array(location)
                    if generation_minimum < global_minimum:
                        global_minimum = generation_minimum
                        temp = radial_best
            centre += self.c_parameters[0] * (global_best - centre)
            centre += self.c_parameters[1] * (radial_best - centre)

            self.history.append(
                (centre, self.func(centre), self._get_time_from_start())
            )
            self.logger.info(
                f'Generation: {generation}.'
                f' Loss: {self.history[-1][1]}.'
                f' Optimization Time: {self.history[-1][2]} msec.'
                f' Centre: {str(self.history[-1][0])}.'
            )
            global_best = temp
