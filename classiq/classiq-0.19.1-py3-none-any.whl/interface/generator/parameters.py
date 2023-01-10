from typing import TYPE_CHECKING, Any, Union

if TYPE_CHECKING:
    from typing_extensions import TypeAlias
else:
    TypeAlias = Any

ParameterType: TypeAlias = str
ParameterFloatType: TypeAlias = Union[float, ParameterType]
