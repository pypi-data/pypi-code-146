from __future__ import annotations

import numpy as np
import pandas as pd
from assimulo.problem import Explicit_Problem  # type: ignore
from assimulo.solvers import CVode  # type: ignore
from assimulo.solvers.sundials import CVodeError  # type: ignore
from dataclasses import dataclass
from typing import Callable, Optional, cast
from ..types import Array


@dataclass
class AssmimuloSettings:
    atol: float = 1e-8
    rtol: float = 1e-8
    maxnef: int = 4
    maxncf: int = 1
    verbosity: int = 50


@dataclass
class IntegrationResult:
    time: Array
    values: Array


@dataclass(init=False)
class Assimulo:
    problem: Explicit_Problem
    integrator: CVode
    settings: AssmimuloSettings

    def __init__(
        self,
        rhs: Callable,
        y0: list[float],
        settings: Optional[AssmimuloSettings] = None,
    ) -> None:
        self.problem = Explicit_Problem(rhs, y0)
        self.integrator = CVode(self.problem)
        self.settings = AssmimuloSettings() if settings is None else settings

    def _set_settings(self) -> None:
        for k, v in self.settings.__dict__.items():
            setattr(self.integrator, k, v)

    def update_settings(self, settings: AssmimuloSettings) -> None:
        self.settings = settings

    def integrate(
        self,
        t_end: float,
        steps: Optional[int],
        time_points: Optional[list[float]],
    ) -> Optional[IntegrationResult]:
        self._set_settings()
        if steps is None:
            steps = 0
        try:
            t, y = self.integrator.simulate(t_end, steps, time_points)
            return IntegrationResult(np.array(t, dtype=float), np.array(y, dtype=float))
        except CVodeError:
            return None

    def integrate_to_steady_state(self, tolerance: float) -> Optional[Array]:
        self.reset()
        self._set_settings()
        t_end = 1000
        for _ in range(1, 4):
            res = self.integrate(t_end, None, None)
            if res is None:
                return None
            y = res.values
            if np.linalg.norm(y[-1] - y[-2], ord=2) < tolerance:
                return cast(Array, y[-1])
            t_end *= 1000
        return None

    def reset(self) -> None:
        self.integrator.reset()
