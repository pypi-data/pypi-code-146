from typing import Any, Dict, Optional

import pydantic
import pyomo.core as pyo
from pydantic import BaseModel

from classiq.interface.backend.backend_preferences import (
    BackendPreferencesTypes,
    backend_preferences_field,
    is_exact_simulator,
)
from classiq.interface.combinatorial_optimization import model_serializer
from classiq.interface.combinatorial_optimization.encoding_types import EncodingType
from classiq.interface.combinatorial_optimization.preferences import QSolverPreferences
from classiq.interface.combinatorial_optimization.solver_types import QSolver
from classiq.interface.executor.optimizer_preferences import CombinatorialOptimizer
from classiq.interface.generator.result import GeneratedCircuit


class OptimizationProblem(BaseModel):
    qsolver_preferences: QSolverPreferences = pydantic.Field(
        default=...,
        description="preferences for the QSolver: QAOAMixer, QAOAPenalty or GAS",
    )
    optimizer_preferences: CombinatorialOptimizer = pydantic.Field(
        default_factory=CombinatorialOptimizer,
        description="preferences for the VQE execution",
    )
    serialized_model: Optional[Dict[str, Any]] = None
    backend_preferences: BackendPreferencesTypes = backend_preferences_field()
    encoding_type: Optional[EncodingType] = pydantic.Field(
        default=EncodingType.BINARY,
        description="encoding scheme for integer variables",
    )
    ansatz: Optional[GeneratedCircuit] = pydantic.Field(
        default=None, description="GeneratedCircuit object of the ansatz circuit"
    )

    class Config:
        smart_union = True
        extra = "forbid"
        validate_assignment = True

    @pydantic.validator("serialized_model", pre=True)
    def serialize_model(cls, model: Any):
        if isinstance(model, pyo.ConcreteModel):
            return model_serializer.to_json(model, return_dict=True)

        return model

    @pydantic.root_validator()
    def set_should_check_valid_solutions(cls, values):
        qsolver_preferences = values.get("qsolver_preferences")
        backend_preferences = values.get("backend_preferences")
        optimizer_preferences = values.get("optimizer_preferences")

        if qsolver_preferences.qsolver == QSolver.Custom:
            pass

        elif qsolver_preferences.qsolver == QSolver.QAOAMixer and is_exact_simulator(
            backend_preferences
        ):
            optimizer_preferences.should_check_valid_solutions = True

        else:
            optimizer_preferences.should_check_valid_solutions = False

        return values
