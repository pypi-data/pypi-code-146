from typing import Optional, Union

import pydantic
from pydantic import BaseModel

from classiq.interface.backend.backend_preferences import (
    BackendPreferencesTypes,
    backend_preferences_field,
)
from classiq.interface.chemistry.ground_state_problem import (
    CHEMISTRY_PROBLEMS,
    CHEMISTRY_PROBLEMS_TYPE,
)
from classiq.interface.chemistry.operator import PauliOperator
from classiq.interface.executor.optimizer_preferences import GroundStateOptimizer
from classiq.interface.generator.result import GeneratedCircuit

AnsatzType = Union[str, GeneratedCircuit, None]


# Note: the `solve` methods of this class are defined in `classiq/applications/chemistry/ground_state_solver.py
class GroundStateSolver(BaseModel):
    ground_state_problem: CHEMISTRY_PROBLEMS_TYPE = pydantic.Field(
        description=f"{CHEMISTRY_PROBLEMS} object"
    )
    ansatz: AnsatzType = pydantic.Field(
        description="GeneratedCircuit object or a str of the ansatz circuit"
    )
    optimizer_preferences: Optional[GroundStateOptimizer] = pydantic.Field(
        description="GroundStateOptimizer object"
    )
    backend_preferences: Optional[BackendPreferencesTypes] = backend_preferences_field()
    hamiltonian: Optional[PauliOperator] = pydantic.Field(
        description="A direct input of the Hamiltonian as a PauliOperator object"
    )
