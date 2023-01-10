from __future__ import annotations

from typing import Any, Dict

import pydantic
from pydantic import BaseModel

from classiq.interface.generator.arith.register_user_input import RegisterUserInput

_DEFAULT_CONTROL_NAME: str = "ctrl"
_DEFAULT_NUM_CONTROL_QUBITS = 1
_INVALID_CONTROL_STATE = "invalid_control_state"


class ControlState(BaseModel):
    num_ctrl_qubits: pydantic.PositiveInt = pydantic.Field(
        default=_DEFAULT_NUM_CONTROL_QUBITS, description="Number of control qubits"
    )
    ctrl_state: str = pydantic.Field(
        default=_INVALID_CONTROL_STATE, description="Control state string"
    )
    name: str = pydantic.Field(
        default=_DEFAULT_CONTROL_NAME, description="Control name"
    )

    @pydantic.root_validator()
    def _validate_control(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        num_ctrl_qubits: int = values.get(
            "num_ctrl_qubits", _DEFAULT_NUM_CONTROL_QUBITS
        )
        ctrl_state: str = values.get("ctrl_state", _INVALID_CONTROL_STATE)

        if ctrl_state == _INVALID_CONTROL_STATE:
            ctrl_state = "1" * num_ctrl_qubits
            values["ctrl_state"] = ctrl_state

        cls._validate_control_string(ctrl_state)

        if num_ctrl_qubits == _DEFAULT_NUM_CONTROL_QUBITS:
            num_ctrl_qubits = len(ctrl_state)
            values["num_ctrl_qubits"] = num_ctrl_qubits

        if len(ctrl_state) != num_ctrl_qubits:
            raise ValueError(
                "control state length should be equal to the number of control qubits"
            )

        if values.get("name") == _DEFAULT_CONTROL_NAME:
            values["name"] = f"{_DEFAULT_CONTROL_NAME}_{ctrl_state}"

        return values

    @classmethod
    def _validate_control_string(cls, ctrl_state: str) -> None:
        if not set(ctrl_state) <= {"1", "0"}:
            raise ValueError(
                f"Control state can only be constructed from 0 and 1, received: {ctrl_state}"
            )

    def __str__(self) -> str:
        return self.ctrl_state

    def __len__(self) -> int:
        return self.num_ctrl_qubits

    @property
    def control_register(self) -> RegisterUserInput:
        return RegisterUserInput(name=self.name, size=self.num_ctrl_qubits)

    def rename(self, name: str) -> ControlState:
        return ControlState(ctrl_state=self.ctrl_state, name=name)

    class Config:
        frozen = True
