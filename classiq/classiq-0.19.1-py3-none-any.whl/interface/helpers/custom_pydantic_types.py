from typing import TYPE_CHECKING, Any, List, Tuple

import pydantic

# General int types

if TYPE_CHECKING:
    PydanticLargerThanOneInteger = int
else:

    class PydanticLargerThanOneInteger(pydantic.ConstrainedInt):
        gt = 1


# Probability float types
if TYPE_CHECKING:
    PydanticProbabilityFloat = float
    PydanticNonOneProbabilityFloat = float
    PydanticNonZeroProbabilityFloat = float
else:

    class PydanticProbabilityFloat(pydantic.ConstrainedFloat):
        ge = 0.0
        le = 1.0

    class PydanticNonOneProbabilityFloat(pydantic.ConstrainedFloat):
        ge = 0.0
        lt = 1.0

    class PydanticNonZeroProbabilityFloat(pydantic.ConstrainedFloat):
        gt = 0.0
        le = 1.0


# CVAR parameter types
if TYPE_CHECKING:
    PydanticAlphaParamCVAR = float
else:

    class PydanticAlphaParamCVAR(pydantic.ConstrainedFloat):
        gt = 0.0
        le = 1.0


# General string types
if TYPE_CHECKING:
    PydanticNonEmptyString = str
else:
    PydanticNonEmptyString = pydantic.constr(min_length=1)

# Name string types
if TYPE_CHECKING:
    PydanticFunctionNameStr = str
else:
    PydanticFunctionNameStr = pydantic.constr(
        strict=True, regex="^([a-z][a-z0-9]*)(_[a-z0-9]+)*$"
    )

if TYPE_CHECKING:
    PydanticPauliMonomial = tuple
else:
    PydanticPauliMonomial = pydantic.conlist(item_type=Any, min_items=2, max_items=2)

if TYPE_CHECKING:
    PydanticPauliMonomialStr = str
else:
    PydanticPauliMonomialStr = pydantic.constr(
        strict=True, strip_whitespace=True, min_length=1, regex="^[IXYZ]+$"
    )

if TYPE_CHECKING:
    PydanticPauliList = List[Tuple[PydanticPauliMonomialStr, complex]]
else:
    PydanticPauliList = pydantic.conlist(item_type=tuple, min_items=1)

if TYPE_CHECKING:
    PydanticFloatTuple = Tuple[float, float]
else:
    PydanticFloatTuple = pydantic.conlist(item_type=float, min_items=2, max_items=2)

if TYPE_CHECKING:
    PydanticNonNegIntTuple = Tuple[pydantic.NonNegativeInt, pydantic.NonNegativeInt]
else:
    PydanticNonNegIntTuple = pydantic.conlist(
        item_type=pydantic.NonNegativeInt, min_items=2, max_items=2
    )

if TYPE_CHECKING:
    PydanticExpressionStr = str
else:
    PydanticExpressionStr = pydantic.constr(
        strip_whitespace=True, min_length=1, max_length=1024
    )
if TYPE_CHECKING:
    AtomType = list
else:
    AtomType = pydantic.conlist(item_type=Any, min_items=2, max_items=2)
