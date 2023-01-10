from typing import List, Optional

import pydantic
import sympy
from typing_extensions import Literal

from classiq.interface.generator import function_params
from classiq.interface.generator.arith.register_user_input import RegisterUserInput
from classiq.interface.generator.standard_gates.standard_angle_metaclass import (
    MyMetaAngledClassModel,
)

"""
To add new standard gates, refer to the following guide
https://docs.google.com/document/d/1Nt9frxnPkSn8swNpOQ983E95eaEiDWaiuWAKglGtUAA/edit#heading=h.e9g9309bzkxt
"""

_POSSIBLE_PARAMETERS: List[str] = ["theta", "phi", "lam"]
DEFAULT_STANDARD_GATE_ARG_NAME: str = "TARGET"


class _StandardGate(function_params.FunctionParams, metaclass=MyMetaAngledClassModel):  # type: ignore[misc]
    _name: str = ""
    _num_target_qubits: pydantic.PositiveInt = pydantic.PrivateAttr(default=1)
    num_ctrl_qubits: pydantic.NonNegativeInt = pydantic.Field(default=0)

    @pydantic.validator("*", pre=True)
    def validate_parameters(cls, value, field: pydantic.fields.ModelField):
        if field.name in _POSSIBLE_PARAMETERS:
            if isinstance(value, str):
                sympy.parse_expr(value)

            if isinstance(value, sympy.Expr):
                return str(value)

        return value

    def _create_ios(self) -> None:
        argument = RegisterUserInput(
            name=DEFAULT_STANDARD_GATE_ARG_NAME,
            size=self._num_target_qubits,
        )
        self._inputs = {DEFAULT_STANDARD_GATE_ARG_NAME: argument}
        self._outputs = {DEFAULT_STANDARD_GATE_ARG_NAME: argument}

    @property
    def name(self):
        # this is removing the Gate suffix from the classes name
        return self._name or self.__class__.__name__[:-4].lower()

    @property
    def num_target_qubits(self):
        return self._num_target_qubits

    def __init_subclass__(cls, angles: Optional[List[str]] = None, **kwargs):
        super().__init_subclass__()


class UncontrolledStandardGate(_StandardGate):  # type: ignore[misc]
    num_ctrl_qubits: Literal[0] = pydantic.Field(default=0)


class XGate(UncontrolledStandardGate):  # type: ignore[misc]
    """
    creates a X gate
    """

    def get_power_order(self) -> int:
        return 2


class YGate(UncontrolledStandardGate):  # type: ignore[misc]
    """
    creates a Y gate
    """

    def get_power_order(self) -> int:
        return 2


class ZGate(UncontrolledStandardGate):  # type: ignore[misc]
    """
    create a Z gate
    """

    def get_power_order(self) -> int:
        return 2


class HGate(UncontrolledStandardGate):  # type: ignore[misc]
    """
    creates a Hadamard gate
    """

    def get_power_order(self) -> int:
        return 2


class IGate(UncontrolledStandardGate):  # type: ignore[misc]
    """
    creates the identity gate
    """

    _name: str = "id"

    def get_power_order(self) -> int:
        return 1


class SGate(UncontrolledStandardGate):  # type: ignore[misc]
    """
    Z**0.5
    """

    def get_power_order(self) -> int:
        return 4


class SdgGate(UncontrolledStandardGate):  # type: ignore[misc]
    """
    creates the inverse S gate
    """

    def get_power_order(self) -> int:
        return 4


class SXGate(UncontrolledStandardGate):  # type: ignore[misc]
    """
    X**0.5
    """

    def get_power_order(self) -> int:
        return 4


class SXdgGate(UncontrolledStandardGate):  # type: ignore[misc]
    """
    creates the inverse SX gate
    """

    def get_power_order(self) -> int:
        return 4


class TGate(UncontrolledStandardGate):  # type: ignore[misc]
    """
    Z**0.25
    """

    def get_power_order(self) -> int:
        return 8


class TdgGate(UncontrolledStandardGate):  # type: ignore[misc]
    """
    creates the inverse T gate
    """

    def get_power_order(self) -> int:
        return 8


class SwapGate(UncontrolledStandardGate):  # type: ignore[misc]
    """
    Swaps between two qubit states
    """

    _num_target_qubits: pydantic.PositiveInt = pydantic.PrivateAttr(default=2)

    def get_power_order(self) -> int:
        return 2


class iSwapGate(UncontrolledStandardGate):  # type: ignore[misc] # noqa: N801
    """
    Swaps between two qubit states and add phase of i to the amplitudes of |01> and |10>
    """

    _num_target_qubits: pydantic.PositiveInt = pydantic.PrivateAttr(default=2)

    def get_power_order(self) -> int:
        return 4
