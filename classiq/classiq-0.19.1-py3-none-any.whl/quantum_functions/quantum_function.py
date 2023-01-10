import sys
from abc import ABC, abstractmethod
from types import FunctionType
from typing import Callable, Dict, List, Optional, Tuple, cast

from classiq.interface.generator.functions import (
    ElementaryFunctionData,
    FunctionImplementation,
    Register,
    RegisterMappingData,
)

# This line is ignored because the entire annotation_parser module is ignored by mypy
from classiq.quantum_functions.annotation_parser import (  # type: ignore[attr-defined]
    AnnotationParser,
    get_annotation_role,
)
from classiq.quantum_functions.function_parser import (
    FunctionParser,
    convert_callable_to_function,
)
from classiq.quantum_register import RegisterRole as Role

# isort: split
from typing import _GenericAlias  # type: ignore[attr-defined]

if sys.version_info >= (3, 9):
    from types import GenericAlias
else:
    GenericAlias = _GenericAlias


class QuantumFunction:
    def __init__(self) -> None:
        self._function_data: Optional[ElementaryFunctionData] = None

    @staticmethod
    def _generate_single_register(
        first_qubit: int, name: str, obj: GenericAlias  # type: ignore[valid-type]
    ) -> Register:
        qreg_size = obj.size  # type: ignore[attr-defined]

        qubits = tuple(range(first_qubit, first_qubit + qreg_size))

        return Register(
            name=name,
            qubits=qubits,
        )

    @classmethod
    def _generate_registers(
        cls, input_names, input_values, output_values
    ) -> Dict[Role, Tuple[Register, ...]]:
        registers: Dict[Role, List[Register]] = {k: list() for k in Role}

        qubit_counter = 0
        for input_name, input_annotation in zip(input_names, input_values):
            role = get_annotation_role(
                annotation=input_annotation, default_role=Role.INPUT
            )

            registers[role].append(
                cls._generate_single_register(
                    first_qubit=qubit_counter,
                    name=input_name,
                    obj=input_annotation,
                )
            )
            qubit_counter += input_annotation.size

        qubit_counter = 0
        for input_name, output_annotation in zip(input_names, output_values):
            role = get_annotation_role(
                annotation=output_annotation, default_role=Role.OUTPUT
            )
            if role == Role.AUXILIARY:
                qubit_counter += output_annotation.size
                continue

            registers[role].append(
                cls._generate_single_register(
                    first_qubit=qubit_counter,
                    name=input_name,
                    obj=output_annotation,
                )
            )
            qubit_counter += output_annotation.size

        return {k: tuple(v) for k, v in registers.items()}

    @classmethod
    def _create_implementation_from_function(
        cls,
        func: FunctionType,
        func_name: str,
        auxiliary_registers: Tuple[Register, ...],
    ) -> FunctionImplementation:
        # Return value
        fp = FunctionParser(func)
        serialized_circuit = fp.extract_function_output()

        implementation = FunctionImplementation(
            name=func_name,
            serialized_circuit=serialized_circuit,
            auxiliary_registers=auxiliary_registers,
        )
        return implementation

    def add_implementation(
        self, func: Callable, name: Optional[str] = None
    ) -> "QuantumFunction":
        func, func_name = convert_callable_to_function(func=func)
        func_name = name or func_name

        # Annotations
        ap = AnnotationParser(func)
        ap.parse()

        registers: Dict[Role, Tuple[Register, ...]] = self._generate_registers(
            input_names=ap.input_names,
            input_values=ap.input_values,
            output_values=ap.output_values,
        )

        implementation = self._create_implementation_from_function(
            func=func,
            func_name=func_name,
            auxiliary_registers=registers[Role.AUXILIARY],
        )

        if self._function_data is None:
            self._function_data = ElementaryFunctionData(
                name=func_name,
                implementations=(implementation,),
                register_mapping=RegisterMappingData.from_registers_dict(
                    regs_dict=registers
                ),
            )
        else:
            self._function_data.register_mapping.validate_equal_mappings(
                RegisterMappingData.from_registers_dict(regs_dict=registers)
            )
            new_implementations = cast(
                Tuple[FunctionImplementation], self._function_data.implementations
            ) + (implementation,)
            implementation.validate_ranges_of_all_registers(
                self._function_data.register_mapping
            )
            self._function_data.implementations = new_implementations

        return self

    @property
    def function_data(self):
        return self._function_data


class QuantumFunctionFactoryBadUsageError(Exception):
    def __init__(self, msg: str):
        self.message = f"{msg} Please call QuantumFunctionFactory.__init__ after initializing all user params."
        super().__init__(self.message)


class QuantumFunctionFactory(ABC):
    """
    Provides the capability of creating parametrized user-defined functions.
    """

    def __init__(self, add_method: Callable, apply_method: Callable):
        self._apply_method = apply_method
        try:
            definition = self.definition
        except AttributeError as e:
            raise QuantumFunctionFactoryBadUsageError(
                f"{self.__class__.__name__} instance definition parsing failed."
            ) from e
        definition.function_data.name = str(self)
        add_method(definition)

    def __str__(self):
        str_list = [self.__class__.__name__.lower()]
        str_list.extend(
            f"{k}_{v}" for k, v in self.__dict__.items() if k != "_apply_method"
        )
        return "_".join(str_list)

    def __call__(self, *args, **kwargs):
        try:
            return self._apply_method(str(self), *args, **kwargs)
        except AttributeError as e:
            raise QuantumFunctionFactoryBadUsageError(
                f"Could not call {self.__class__.__name__}."
            ) from e

    @property
    @abstractmethod
    def definition(self) -> QuantumFunction:
        """
        Abstract method for providing the definition of the user function.
        The QuantumFunction object may be generated either directly, or using existing
        helper tools such as the @qfunc decorator.
        Instance attributes of the QuantumFunctionFactory may be used as parameters for the
        definition.

        Returns:
            The user-defined QuantumFunction object.
        """
