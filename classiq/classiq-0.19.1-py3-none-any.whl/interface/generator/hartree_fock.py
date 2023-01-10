import pydantic

from classiq.interface.chemistry.ground_state_problem import CHEMISTRY_PROBLEMS
from classiq.interface.generator.chemistry_function_params import (
    ChemistryFunctionParams,
)


class HartreeFock(ChemistryFunctionParams):
    @pydantic.validator("gs_problem")
    def validate_gs_problem(cls, gs_problem):
        if not isinstance(gs_problem, CHEMISTRY_PROBLEMS):
            raise ValueError(
                f"ground state problem must be of type {CHEMISTRY_PROBLEMS}"
            )
        return gs_problem
