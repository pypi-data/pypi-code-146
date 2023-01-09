from __future__ import annotations

import logging
import numpy as np
import pandas as pd
from .integrator import Assimulo
from .model import Model
from dataclasses import dataclass, field
from typing import Any, Optional, Type
from ..types import Array

logger = logging.getLogger()


@dataclass(repr=False)
class SimulationResult:
    time: Array
    values: dict[str, Array]
    constants: dict[str, float]

    def __repr__(self) -> str:
        return f"Simulation until t={self.time[-1]}"

    def to_frame(self) -> pd.DataFrame:
        return pd.DataFrame(
            data=self.values,
            index=self.time,  # type: ignore
        )


def concatenate_results(results: list[SimulationResult]) -> pd.DataFrame:
    df = results[0].to_frame()
    if len(results) > 1:
        for result in results[1:]:
            df = pd.concat((df, result.to_frame().iloc[1:]))
    return df


@dataclass(init=False)
class Simulator:
    model: Model
    integrator: Assimulo
    y0: list[float] = field(default_factory=list)
    # Could also be ResultContainer once you add other model types again
    results: list[SimulationResult] = field(default_factory=list)

    def __init__(
        self,
        model: Model,
        integrator: Type[Assimulo],
        y0: dict[str, float],
        results: Optional[SimulationResult] = None,
    ):
        self.model = model
        self.update_y0(y0)
        self.integrator = integrator(rhs=self.model._get_problem, y0=self.y0)
        if results is None:
            self.results = list()

    def __reduce__(self) -> Any:
        return (
            self.__class__,
            (
                self.model,
                self.integrator,
                self.y0,
            ),
            (("results", self.results),),
        )

    def update_y0(self, y0: dict[str, float]) -> None:
        self.y0 = [y0[i] for i in self.model.stoichiometries]

    def clear_results(self) -> None:
        self.results = list()
        self.integrator.reset()

    def simulate(
        self,
        t_end: float,
    ) -> Optional[SimulationResult]:
        if (integration := self.integrator.integrate(t_end, None, None)) is None:
            logger.warning("Simulation failed")
            return None
        res = SimulationResult(
            integration.time,
            dict(zip(self.model.stoichiometries, integration.values.T)),
            self.model.constant_values,
        )
        self.results.append(res)
        return res

    def simulate_to_steady_state(self, tolerance: float = 1e-6) -> Optional[dict[str, float]]:
        if (integration := self.integrator.integrate_to_steady_state(tolerance)) is not None:
            return dict(zip(self.model.stoichiometries, integration))
        else:
            logger.warning("Simulation failed")
            return None

    def get_results(self) -> pd.DataFrame:
        return concatenate_results(self.results)

    def _get_result_constants(self, result: SimulationResult) -> dict[str, Array]:
        return {k: np.full(len(result.time), v) for k, v in result.constants.items()}

    def _get_result_derived_variables(
        self,
        args: dict[str, Array],
    ) -> dict[str, Array]:
        return self.model._algebraic_modules.get_values_array(args)

    def _get_result_all_variables(self, result: SimulationResult, constants: dict[str, Array]) -> dict[str, Array]:
        args = result.values | constants | {"time": result.time}
        return result.values | self._get_result_derived_variables(args)

    def _get_result_fluxes(self, result: SimulationResult) -> dict[str, Array]:
        constants = self._get_result_constants(result)
        all_variables = self._get_result_all_variables(result, constants)
        args = all_variables | constants | {"time": result.time}
        return self.model._reactions.get_fluxes_array(args)

    def get_full_results(self) -> pd.DataFrame:
        full_results: list[SimulationResult] = []
        for result in self.results:
            full_results.append(
                SimulationResult(
                    values=self._get_result_all_variables(result, self._get_result_constants(result)),
                    time=result.time,
                    constants=result.constants,
                )
            )
        return concatenate_results(full_results)

    def get_fluxes(self) -> pd.DataFrame:
        fluxes: list[SimulationResult] = []
        for result in self.results:
            result_fluxes = self._get_result_fluxes(result)
            fluxes.append(
                SimulationResult(
                    values=result_fluxes,
                    time=result.time,
                    constants=result.constants,
                )
            )
        return concatenate_results(fluxes)
