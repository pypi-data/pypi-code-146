import itertools
import re
from enum import Enum
from typing import Any, Collection, Dict, Iterable, List, Mapping, Optional, Type

import pydantic
from pydantic.fields import ModelPrivateAttr

from classiq.interface.generator.arith.register_user_input import RegisterUserInput
from classiq.interface.helpers.custom_pydantic_types import PydanticNonEmptyString
from classiq.interface.helpers.hashable_mixin import HashableMixin

FunctionParamsDiscriminator = str

IOName = PydanticNonEmptyString
ArithmeticIODict = Dict[IOName, RegisterUserInput]

DEFAULT_ZERO_NAME = "zero"
DEFAULT_OUTPUT_NAME = "OUT"
DEFAULT_INPUT_NAME = "IN"

BAD_FUNCTION_ERROR_MSG = "field must be provided to deduce"
NO_DISCRIMINATOR_ERROR_MSG = "Unknown"

REGISTER_SIZES_MISMATCH_ERROR_MSG = "Register sizes differ between inputs and outputs"

BAD_INPUT_REGISTER_ERROR_MSG = "Bad input register name given"
BAD_OUTPUT_REGISTER_ERROR_MSG = "Bad output register name given"
END_BAD_REGISTER_ERROR_MSG = (
    "Register name must be in snake_case and begin with a letter."
)

ALPHANUM_AND_UNDERSCORE = r"[0-9a-zA-Z_]*"
NAME_REGEX = rf"[a-zA-Z]{ALPHANUM_AND_UNDERSCORE}"


class IO(Enum):
    Input = True
    Output = False

    def __invert__(self) -> "IO":
        return IO(not self.value)


def input_io(is_inverse: bool) -> IO:
    if is_inverse:
        return IO.Output
    return IO.Input


def output_io(is_inverse: bool) -> IO:
    if is_inverse:
        return IO.Input
    return IO.Output


class ParamMetadata(pydantic.BaseModel):
    metadata_type: str


class FunctionParams(HashableMixin, pydantic.BaseModel):
    _inputs: ArithmeticIODict = pydantic.PrivateAttr(default_factory=dict)
    _outputs: ArithmeticIODict = pydantic.PrivateAttr(default_factory=dict)
    _zero_inputs: ArithmeticIODict = pydantic.PrivateAttr(default_factory=dict)

    def __hash__(self) -> int:  # taken from pydantic.BaseModel otherwise
        return HashableMixin.__hash__(self)

    @property
    def inputs(self) -> ArithmeticIODict:
        return self._inputs

    def inputs_full(self, assign_zero_ios: bool = False) -> ArithmeticIODict:
        if assign_zero_ios:
            return {**self._inputs, **self._zero_inputs}
        return self._inputs

    @property
    def outputs(self) -> ArithmeticIODict:
        return self._outputs

    def num_input_qubits(self, assign_zero_ios: bool = False) -> int:
        return sum(reg.size for reg in self.inputs_full(assign_zero_ios).values())

    @property
    def num_output_qubits(self) -> int:
        return sum(reg.size for reg in self.outputs.values())

    @property
    def _input_names(self) -> List[IOName]:
        return list(self._inputs.keys())

    @property
    def _output_names(self) -> List[IOName]:
        return list(self._outputs.keys())

    def _create_zero_input_registers(self, names_and_sizes: Mapping[str, int]) -> None:
        for name, size in names_and_sizes.items():
            self._zero_inputs[name] = RegisterUserInput(name=name, size=size)

    def _create_zero_inputs_from_outputs(self) -> None:
        for name, reg in self._outputs.items():
            zero_input_name = f"{DEFAULT_ZERO_NAME}_{name}"
            self._zero_inputs[zero_input_name] = reg.revalued(name=zero_input_name)

    def __init__(self, **data: Any) -> None:
        super().__init__(**data)
        self._create_ios()
        if not self._inputs and not self._zero_inputs:
            self._create_zero_inputs_from_outputs()
        self._validate_io_names()
        if self.discriminator() != "Arithmetic":
            self._validate_total_io_sizes()

    def is_powerable(self, assign_zero_ios: bool = False) -> bool:
        input_names = set(self.inputs_full(assign_zero_ios))
        output_names = set(self._output_names)
        return (
            self.num_input_qubits(assign_zero_ios) == self.num_output_qubits
            and len(input_names) == len(output_names)
            and (len(input_names - output_names) <= 1)
            and (len(output_names - input_names) <= 1)
        )

    def get_power_order(self) -> Optional[int]:
        return None

    def _create_ios(self) -> None:
        pass

    @staticmethod
    def _get_size_of_ios(registers: Collection[Optional[RegisterUserInput]]) -> int:
        return sum(reg.size if reg is not None else 0 for reg in registers)

    def _validate_io_names(self) -> None:
        error_msg: List[str] = []
        error_msg += self._get_error_msg(self._inputs, BAD_INPUT_REGISTER_ERROR_MSG)
        error_msg += self._get_error_msg(self._outputs, BAD_OUTPUT_REGISTER_ERROR_MSG)
        if error_msg:
            error_msg += [END_BAD_REGISTER_ERROR_MSG]
            raise ValueError("\n".join(error_msg))

    @staticmethod
    def _sum_registers_sizes(registers: Iterable[RegisterUserInput]) -> int:
        return sum(reg.size for reg in registers)

    def _validate_total_io_sizes(self) -> None:
        total_inputs_size = self._sum_registers_sizes(
            itertools.chain(self._inputs.values(), self._zero_inputs.values())
        )
        total_outputs_size = self._sum_registers_sizes(self._outputs.values())
        if total_inputs_size != total_outputs_size:
            raise ValueError(REGISTER_SIZES_MISMATCH_ERROR_MSG)

    def _get_error_msg(self, names: Iterable[IOName], msg: str) -> List[str]:
        bad_names = [name for name in names if re.fullmatch(NAME_REGEX, name) is None]
        return [f"{msg}: {bad_names}"] if bad_names else []

    @classmethod
    def get_default_input_names(cls) -> Optional[List[IOName]]:
        return cls._get_io_name_default_if_exists(io_attr_name="_inputs")

    @classmethod
    def get_default_output_names(cls) -> Optional[List[IOName]]:
        return cls._get_io_name_default_if_exists(io_attr_name="_outputs")

    @classmethod
    def _is_default_create_io_method(cls) -> bool:
        return cls._create_ios == FunctionParams._create_ios

    @classmethod
    def _get_io_name_default_if_exists(
        cls, io_attr_name: str
    ) -> Optional[List[IOName]]:
        if not cls._is_default_create_io_method():
            return None

        attr: ModelPrivateAttr = cls.__private_attributes__[io_attr_name]
        return list(attr.get_default().keys())

    def get_metadata(self) -> Optional[ParamMetadata]:
        return None

    @classmethod
    def discriminator(cls) -> FunctionParamsDiscriminator:
        return cls.__name__

    class Config:
        frozen = True


def parse_function_params(
    *,
    params: Any,
    discriminator: Any,
    param_classes: Collection[Type[FunctionParams]],
    no_discriminator_error: Exception,
    bad_function_error: Exception,
) -> FunctionParams:  # Any is for use in pydantic validators.
    if not discriminator:
        raise no_discriminator_error

    matching_classes = [
        param_class
        for param_class in param_classes
        if param_class.discriminator() == discriminator
    ]

    if len(matching_classes) != 1:
        raise bad_function_error

    return matching_classes[0].parse_obj(params)


def parse_function_params_values(
    *,
    values: Dict[str, Any],
    params_key: str,
    discriminator_key: str,
    param_classes: Collection[Type[FunctionParams]],
) -> None:
    params = values.get(params_key)
    if isinstance(params, FunctionParams):
        values[discriminator_key] = params.discriminator()
        return
    discriminator = values.get(discriminator_key)
    values[params_key] = parse_function_params(
        params=params,
        discriminator=discriminator,
        param_classes=param_classes,
        no_discriminator_error=ValueError(
            f"The {discriminator_key} {NO_DISCRIMINATOR_ERROR_MSG} {params_key} type."
        ),
        bad_function_error=ValueError(
            f"{BAD_FUNCTION_ERROR_MSG} {discriminator_key}: {discriminator}"
        ),
    )
