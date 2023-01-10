from typing import Any, Dict, List, Optional, cast

import pydantic
import sympy

from classiq.interface.generator.arith.register_user_input import RegisterUserInput
from classiq.interface.generator.function_params import FunctionParams
from classiq.interface.generator.parameters import ParameterFloatType

CTRL = "CTRL"
TARGET = "TARGET"


class Mcu(FunctionParams):
    """
    Multi-controlled u-gate.
    Based on U(theta, phi, lam, gam) = e^(i*(gam + (phi + lam)/2)) * RZ(phi) * RY(theta) * RZ(lam)
    For a general gate U, four angles are required - theta, phi, lambda and gam.

    U(gam, phi,theta, lam) =
    e^(i*gam) *
    cos(theta/2) & -e^(i*lam)*sin(theta/2) \\
    e^(i*phi)*sin(theta/2) & e^(i*(phi+lam))*cos(theta/2) \\

    U(gam, phi,theta, lam) =
    e^(i*gam) *
    cos(theta/2)            &    -e^(i*lam)*sin(theta/2) \\
    e^(i*phi)*sin(theta/2)  &    e^(i*(phi+lam))*cos(theta/2) \\
    """

    theta: ParameterFloatType = pydantic.Field(
        default=0, description="Theta radian angle."
    )
    phi: ParameterFloatType = pydantic.Field(default=0, description="Phi radian angle.")
    lam: ParameterFloatType = pydantic.Field(
        default=0, description="Lambda radian angle."
    )
    gam: ParameterFloatType = pydantic.Field(default=0, description="gam radian angle.")

    num_ctrl_qubits: Optional[pydantic.PositiveInt] = pydantic.Field(
        default=None, description="The number of control qubits."
    )
    ctrl_state: Optional[str] = pydantic.Field(
        default=None, description="string of the control state"
    )

    _registers: List[RegisterUserInput] = pydantic.PrivateAttr()

    @pydantic.root_validator()
    def validate_control(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        num_ctrl_qubits = values.get("num_ctrl_qubits")
        ctrl_state = values.get("ctrl_state")

        if ctrl_state is not None:
            ctrl_state = cast(str, ctrl_state)

        if ctrl_state is None and num_ctrl_qubits is None:
            raise ValueError("num_ctrl_qubits or ctrl_state must exist.")

        if ctrl_state is None and num_ctrl_qubits is not None:
            values["ctrl_state"] = "1" * num_ctrl_qubits
            ctrl_state = values["ctrl_state"]

        if num_ctrl_qubits is None and ctrl_state is not None:
            num_ctrl_qubits = len(ctrl_state)
            values["num_ctrl_qubits"] = num_ctrl_qubits

        if len(ctrl_state) != num_ctrl_qubits:
            raise ValueError(
                "control state length should be equal to the number of control qubits"
            )

        return values

    @pydantic.validator("theta", "phi", "lam", "gam", pre=True)
    def validate_parameters(cls, parameter):
        if isinstance(parameter, str):
            sympy.parse_expr(parameter)

        if isinstance(parameter, sympy.Expr):
            return str(parameter)
        return parameter

    def _set_registers(self) -> None:
        if self.num_ctrl_qubits is None:
            raise ValueError("num_ctrl_qubits must have a valid value.")
        ctrl_register = RegisterUserInput(size=self.num_ctrl_qubits, name=CTRL)
        target_register = RegisterUserInput(size=1, name=TARGET)
        self._registers = [ctrl_register, target_register]

    def _create_ios(self) -> None:
        self._set_registers()
        self._inputs = {reg.name: reg for reg in self._registers}
        self._outputs = {reg.name: reg for reg in self._registers}

    @property
    def registers(self) -> List[RegisterUserInput]:
        return self._registers
