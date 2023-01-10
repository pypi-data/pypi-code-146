from __future__ import annotations

import abc
from typing import Any, Dict, Iterable, Optional

import pydantic

from classiq.interface.generator.arith.register_user_input import RegisterUserInput
from classiq.interface.generator.function_params import FunctionParams

_DEFAULT_GARBAGE_OUT_NAME = "extra_qubits"
_IDENTICAL_GARBAGE_OUTPUT_NAME_ERROR_MSG = "Output and garbage names cannot be the same"


class ArithmeticOperationParams(FunctionParams):
    output_size: Optional[pydantic.PositiveInt]
    output_name: str
    garbage_output_name: str = _DEFAULT_GARBAGE_OUT_NAME
    _result_register: Optional[RegisterUserInput] = pydantic.PrivateAttr(default=None)

    @pydantic.validator("garbage_output_name")
    def _validate_garbage_output_name(
        cls, garbage_output_name: str, values: Dict[str, Any]
    ) -> str:
        output_name: Optional[str] = values.get("output_name")
        if garbage_output_name == output_name:
            raise ValueError(_IDENTICAL_GARBAGE_OUTPUT_NAME_ERROR_MSG)
        return garbage_output_name

    @staticmethod
    def _assert_boolean_register(reg: RegisterUserInput) -> None:
        if reg.is_boolean_register():
            return
        raise ValueError("Register doesn't match a boolean variable")

    @abc.abstractmethod
    def _get_result_register(self) -> RegisterUserInput:
        pass

    @property
    def result_register(self) -> RegisterUserInput:
        if self._result_register is None:
            self._result_register = self._get_result_register()
        return self._result_register

    @abc.abstractmethod
    def is_inplaced(self) -> bool:
        pass

    @property
    def _include_sign(self) -> bool:
        return self.output_size is None

    @abc.abstractmethod
    def get_params_inplace_options(self) -> Iterable[ArithmeticOperationParams]:
        pass
