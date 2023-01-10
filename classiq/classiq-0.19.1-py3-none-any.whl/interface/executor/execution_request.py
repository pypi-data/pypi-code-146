from typing import Any, Dict, Union

import pydantic
from pydantic import BaseModel
from typing_extensions import Literal

from classiq.interface.backend.backend_preferences import IonqBackendPreferences
from classiq.interface.executor.execution_preferences import ExecutionPreferences
from classiq.interface.executor.hamiltonian_minimization_problem import (
    HamiltonianMinimizationProblem,
)
from classiq.interface.executor.quantum_program import (
    QuantumBaseProgram,
    QuantumInstructionSet,
    QuantumProgram,
)
from classiq.interface.generator.result import GeneratedCircuit


class GeneratedCircuitExecution(GeneratedCircuit):
    execution_type: Literal["generated_circuit"] = "generated_circuit"


class QuantumProgramExecution(QuantumProgram):
    execution_type: Literal["quantum_program"] = "quantum_program"


class AmplitudeEstimationExecution(QuantumBaseProgram):
    execution_type: Literal["amplitude_estimation"] = "amplitude_estimation"


class HamiltonianMinimizationProblemExecution(HamiltonianMinimizationProblem):
    execution_type: Literal[
        "hamiltonian_minimization_problem"
    ] = "hamiltonian_minimization_problem"


ExecutionPayloads = Union[
    GeneratedCircuitExecution,
    QuantumProgramExecution,
    AmplitudeEstimationExecution,
    HamiltonianMinimizationProblemExecution,
]


class ExecutionRequest(BaseModel):
    execution_payload: ExecutionPayloads
    preferences: ExecutionPreferences = pydantic.Field(
        default_factory=ExecutionPreferences,
        description="preferences for the execution",
    )

    @pydantic.validator("preferences")
    def validate_ionq_backend(
        cls, preferences: ExecutionPreferences, values: Dict[str, Any]
    ):
        """
        This function implement the following check:
        BE \\ payload | IonQ program | Qasm program | Other
        --------------|--------------|--------------|------
        IonQ backend  |       V      |      V       |   X
        Other backend |       X      |      V       |   V
        Since:
        - We can't execute non-programs on the IonQ backends
        - We can't execute IonQ programs on non-IonQ backends
        """
        quantum_program = values.get("execution_payload")
        is_ionq_backend = isinstance(
            preferences.backend_preferences, IonqBackendPreferences
        )
        if isinstance(quantum_program, QuantumProgram):
            if (
                quantum_program.syntax == QuantumInstructionSet.IONQ
                and not is_ionq_backend
            ):
                raise ValueError("Can only execute IonQ code on IonQ backend.")
        else:
            # If we handle anything other than a program.
            if is_ionq_backend:
                raise ValueError(
                    "IonQ backend supports only execution of QuantumPrograms"
                )
        return preferences
