"""Function library module, implementing facilities for adding user defined functions to the Classiq platform."""
from typing import Any, Dict, Tuple, Type, Union

from classiq.interface.generator.functions import (
    DEFAULT_FUNCTION_LIBRARY_NAME,
    CompositeFunctionData,
    ElementaryFunctionData,
    FunctionData,
    FunctionLibraryData,
)
from classiq.interface.generator.user_defined_function_params import CustomFunction

from classiq.exceptions import ClassiqValueError
from classiq.quantum_functions.quantum_function import (
    QuantumFunction,
    QuantumFunctionFactory,
)

QASM_INTRO = 'OPENQASM 2.0;\ninclude "qelib1.inc";\n'
QASM3_INTRO = 'OPENQASM 3.0;\ninclude "stdgates.inc";\n'


class FunctionLibrary:
    """Facility to manage functions."""

    def __init__(self, *functions, name: str = DEFAULT_FUNCTION_LIBRARY_NAME):
        """
        Args:
            name (:obj:`str`, optional): The name of the function library.
            *functions (:obj:`FunctionData`, optional): A list of functions to initialize the object.
        """
        self._data = FunctionLibraryData(name=name)
        self._params: Dict[str, CustomFunction] = dict()
        self._func_factories: Dict[str, Type[QuantumFunctionFactory]] = dict()

        for f in functions:
            self.add_function(f)

    def get_function(self, function_name: str) -> CustomFunction:
        return self._params[function_name]

    def get_function_factory(
        self, function_factory_name: str
    ) -> Type[QuantumFunctionFactory]:
        return self._func_factories[function_factory_name]

    def __getitem__(self, key: Any) -> CustomFunction:
        if isinstance(key, str):
            return self.get_function(key)
        else:
            raise ClassiqValueError("Invalid key")

    def add_function(
        self,
        function_data: Union[
            FunctionData, QuantumFunction, Type[QuantumFunctionFactory]
        ],
        override_existing_functions: bool = False,
    ) -> None:
        """Adds a function to the function library.

        Args:
            function_data (FunctionData): The function data object.
            override_existing_functions (:obj:`bool`, optional): Defaults to False.

        Returns:
            None
        """
        if isinstance(function_data, type) and issubclass(
            function_data, QuantumFunctionFactory
        ):
            self._func_factories[function_data.__name__] = function_data
            return
        if isinstance(function_data, QuantumFunction):
            function_data = function_data.function_data

        if not isinstance(
            function_data, (ElementaryFunctionData, CompositeFunctionData)
        ):
            raise ClassiqValueError(
                f"FunctionData object expected, got {function_data.__class__.__name__}"
            )

        function_name = function_data.name
        if (
            not override_existing_functions
            and function_name in self._data.function_dict
        ):
            raise ClassiqValueError("Cannot override existing functions.")

        if isinstance(function_data, CompositeFunctionData):
            for call in filter(
                lambda i: isinstance(i.function_params, CustomFunction),
                function_data.logic_flow,
            ):
                if self._data and call.function_params not in self.data:
                    raise ClassiqValueError(
                        "The function is not found in included library."
                    )

        self._data.function_dict[function_name] = function_data
        self._params[function_name] = self._to_params(function_data)

    def remove_function(self, function_name: str) -> FunctionData:
        """Removes a function from the function library.

        Args:
            function_name (str): The name of the function.

        Returns:
            The removed function data.
        """
        self._params.pop(function_name)
        return self._data.function_dict.pop(function_name)

    @property
    def name(self) -> str:
        """The library name."""
        return self._data.name

    @property
    def function_names(self) -> Tuple[str, ...]:
        """Get a tuple of the names of the functions in the library.

        Returns:
            The names of the functions in the library.
        """
        return tuple(self._data.function_dict.keys())

    @property
    def function_factory_names(self) -> Tuple[str, ...]:
        return tuple(self._func_factories.keys())

    @property
    def data(self) -> FunctionLibraryData:
        return self._data

    @staticmethod
    def _to_params(data: FunctionData) -> CustomFunction:
        params = CustomFunction(name=data.name)
        params.generate_ios(
            inputs=data.inputs,
            outputs=data.outputs,
        )
        return params
