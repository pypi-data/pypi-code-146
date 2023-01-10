from typing import Any, Dict, List, Optional, Union

from pyomo.core import ConcreteModel

from classiq.interface.backend.backend_preferences import BackendPreferences
from classiq.interface.chemistry import operator
from classiq.interface.combinatorial_optimization import optimization_problem, sense
from classiq.interface.combinatorial_optimization.encoding_types import EncodingType
from classiq.interface.combinatorial_optimization.preferences import (
    GASPreferences,
    QAOAPreferences,
    QSolverPreferences,
)
from classiq.interface.combinatorial_optimization.solver_types import QSolver
from classiq.interface.executor.optimizer_preferences import CombinatorialOptimizer
from classiq.interface.executor.result import GroverAdaptiveSearchResult
from classiq.interface.executor.vqe_result import OptimizationResult, SolverResult
from classiq.interface.generator.model import Model
from classiq.interface.generator.result import GeneratedCircuit

from classiq._internals.api_wrapper import ApiWrapper
from classiq._internals.async_utils import Asyncify
from classiq.exceptions import ClassiqCombinatorialOptimizationError, ClassiqError
from classiq.model_designer import ModelDesigner

GAS_MODEL_ERROR_MESSAGE = "GAS model is not implemented yet."


class CombinatorialOptimization(metaclass=Asyncify):
    def __init__(
        self,
        model: ConcreteModel,
        qsolver_preferences: QSolverPreferences,
        ansatz: Optional[GeneratedCircuit] = None,
        optimizer_preferences: Optional[CombinatorialOptimizer] = None,
        backend_preferences: Optional[BackendPreferences] = None,
        encoding_type: Optional[EncodingType] = None,
    ):
        self.is_maximization = sense.is_maximization(model)
        self._qsolver = qsolver_preferences.qsolver

        arguments: Dict[str, Any] = {
            "serialized_model": model,
            "encoding_type": encoding_type,
            "qsolver_preferences": qsolver_preferences,
        }
        if optimizer_preferences is not None:
            arguments["optimizer_preferences"] = optimizer_preferences
        if backend_preferences is not None:
            arguments["backend_preferences"] = backend_preferences

        self._problem = optimization_problem.OptimizationProblem(**arguments)
        self._model_designer: Optional[ModelDesigner] = None

        # The ansatz is added using its special setter method
        if ansatz is not None:
            self.ansatz = ansatz

    @property
    def qsolver_preferences(self) -> QSolverPreferences:
        return self._problem.qsolver_preferences

    @property
    def optimizer_preferences(self) -> CombinatorialOptimizer:
        return self._problem.optimizer_preferences

    @property
    def backend_preferences(self) -> BackendPreferences:
        return self._problem.backend_preferences

    @property
    async def ansatz_async(self) -> GeneratedCircuit:
        return self._problem.ansatz or await self.synthesize_async()

    @ansatz_async.setter
    def ansatz_async(self, value: GeneratedCircuit) -> None:
        self._problem.qsolver_preferences.qsolver = QSolver.Custom
        self._problem.ansatz = value

    @property
    async def model_designer_async(self) -> ModelDesigner:
        return self._model_designer or await self.get_model_designer_async()

    @model_designer_async.setter
    def model_designer_async(self, value: ModelDesigner) -> None:
        self._problem.qsolver_preferences.qsolver = QSolver.Custom
        self._model_designer = value

    @property
    def should_check_valid_solutions(self):
        return self.optimizer_preferences.should_check_valid_solutions

    @should_check_valid_solutions.setter
    def should_check_valid_solutions(self, value: bool):
        self.optimizer_preferences.should_check_valid_solutions = value

    async def get_model_designer_async(self) -> ModelDesigner:
        # Don't use model_designer_async.setter to retain the previous qsolver
        self._model_designer = ModelDesigner.from_model(
            await self.get_ansatz_model_async()
        )
        return await self.model_designer_async

    async def synthesize_async(self) -> GeneratedCircuit:
        if self._qsolver == "GAS":
            return await self.synthesize_gas()
        else:
            return await self.synthesize_qaoa()

    async def synthesize_gas(self) -> GeneratedCircuit:
        return await ApiWrapper.call_gas_circuit_generate_task(problem=self._problem)

    async def synthesize_qaoa(self) -> GeneratedCircuit:
        model_designer = await self.model_designer_async

        # We don't use the ansatz_async.setter because we don't want to set qsolver to QSolver.Custom
        self._problem.ansatz = await model_designer.synthesize_async()
        return await self.ansatz_async

    async def solve_async(
        self,
    ) -> Union[OptimizationResult, GroverAdaptiveSearchResult]:
        if not self._qsolver == "GAS":
            await self.ansatz_async  # This ensures that the ansatz is created when not provided

        if isinstance(self._problem.qsolver_preferences, QAOAPreferences):
            return await ApiWrapper.call_combinatorial_optimization_solve_task_vqe(
                self._problem
            )
        elif isinstance(self._problem.qsolver_preferences, GASPreferences):
            return await ApiWrapper.call_combinatorial_optimization_solve_task_gas(
                self._problem
            )

        raise ValueError("Input problem must have qaoa or gas preferences.")

    async def solve_classically_async(self) -> SolverResult:
        return await ApiWrapper.call_combinatorial_optimization_solve_classically_task(
            problem=self._problem
        )

    async def get_ansatz_model_async(self) -> Model:
        if self._qsolver == QSolver.Custom:
            raise ClassiqCombinatorialOptimizationError(
                "Can't generate model for custom qsolver."
            )

        if self._qsolver == QSolver.GAS:
            raise ClassiqCombinatorialOptimizationError(GAS_MODEL_ERROR_MESSAGE)

        try:
            result = await ApiWrapper.call_combinatorial_optimization_model_task(
                problem=self._problem
            )
        except ClassiqError as exc:
            raise ClassiqCombinatorialOptimizationError(
                f"Get model failed: {exc}"
            ) from exc
        return result

    async def get_operator_async(self) -> operator.PauliOperator:
        return await ApiWrapper.call_combinatorial_optimization_operator_task(
            problem=self._problem
        )

    async def get_objective_async(self) -> str:
        result = await ApiWrapper.call_combinatorial_optimization_objective_task(
            problem=self._problem
        )
        return result.details

    async def get_initial_point_async(self) -> List[float]:
        if not self._qsolver == "GAS":
            await self.ansatz_async  # This ensures that the ansatz is created when not provided

        result = await ApiWrapper.call_combinatorial_optimization_initial_point_task(
            problem=self._problem
        )

        return result.initial_point
