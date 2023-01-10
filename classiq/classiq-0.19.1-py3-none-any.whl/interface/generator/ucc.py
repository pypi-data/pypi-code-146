from typing import Iterable, Optional

import pydantic

from classiq.interface.generator.chemistry_function_params import (
    ChemistryFunctionParams,
)
from classiq.interface.generator.excitations import EXCITATIONS_TYPE

_EXCITATIONS_DICT = {"s": 1, "d": 2, "t": 3, "q": 4}


class UCC(ChemistryFunctionParams):
    """
    Ucc ansatz
    """

    use_naive_evolution: bool = pydantic.Field(
        default=False, description="Whether to evolve the operator naively"
    )
    excitations: EXCITATIONS_TYPE = pydantic.Field(
        default_factory=lambda: [1, 2],
        description="type of excitation operators in the UCC ansatz",
    )
    max_depth: Optional[pydantic.PositiveInt] = pydantic.Field(
        default=None,
        description="Maximum depth of the generated quantum circuit ansatz",
    )
    parameter_prefix: str = pydantic.Field(
        default="param_",
        description="Prefix for the generated parameters",
    )

    @pydantic.validator("excitations")
    def _validate_excitations(cls, excitations: EXCITATIONS_TYPE) -> EXCITATIONS_TYPE:
        if isinstance(excitations, int):
            if excitations not in _EXCITATIONS_DICT.values():
                raise ValueError(
                    f"possible values of excitations are {list(_EXCITATIONS_DICT.values())}"
                )
            excitations = [excitations]

        elif isinstance(excitations, Iterable):
            excitations = list(excitations)  # type: ignore[assignment]
            if all(isinstance(idx, int) for idx in excitations):
                if any(idx not in _EXCITATIONS_DICT.values() for idx in excitations):
                    raise ValueError(
                        f"possible values of excitations are {list(_EXCITATIONS_DICT.values())}"
                    )

            elif all(isinstance(idx, str) for idx in excitations):
                if any(idx not in _EXCITATIONS_DICT.keys() for idx in excitations):
                    raise ValueError(
                        f"possible values of excitations are {list(_EXCITATIONS_DICT.keys())}"
                    )
                excitations = sorted(_EXCITATIONS_DICT[idx] for idx in excitations)  # type: ignore[index]

            else:
                raise ValueError(
                    "excitations must be of the same type (all str or all int)"
                )
        return excitations
