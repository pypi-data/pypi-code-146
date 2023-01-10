import ast
import enum
import keyword
import re
from typing import Any, Dict, Optional, Set

import pydantic

from classiq.interface.generator.arith import arithmetic_expression_parser
from classiq.interface.generator.arith.arithmetic_result_builder import (
    ArithmeticDefinitions,
    ArithmeticResultBuilder,
)
from classiq.interface.generator.arith.fix_point_number import (
    MAX_FRACTION_PLACES,
    FixPointNumber,
)
from classiq.interface.generator.arith.register_user_input import RegisterUserInput
from classiq.interface.generator.function_params import FunctionParams
from classiq.interface.helpers.custom_pydantic_types import PydanticExpressionStr

DEFAULT_TARGET_NAME = "arithmetic_target"

SUPPORTED_VAR_NAMES_REG = "[A-Za-z][A-Za-z0-9]*"

SUPPORTED_FUNC_NAMES: Set[str] = {"or", "and"}.union(
    arithmetic_expression_parser.SUPPORTED_FUNC_NAMES
)
FORBIDDEN_LITERALS: Set[str] = set(keyword.kwlist) - SUPPORTED_FUNC_NAMES


class UncomputationMethods(str, enum.Enum):
    naive = "naive"
    optimized = "optimized"


class MappingMethods(str, enum.Enum):
    naive = UncomputationMethods.naive.value
    optimized = UncomputationMethods.optimized.value
    dirty_optimized = "dirty_optimized"
    no_uncomputation = "no_uncomputation"


class ArithmeticTemplate(FunctionParams):
    max_fraction_places: pydantic.NonNegativeInt = MAX_FRACTION_PLACES
    expression: PydanticExpressionStr
    definitions: ArithmeticDefinitions
    qubit_count: Optional[pydantic.NonNegativeInt] = None
    simplify: bool = False

    @pydantic.validator("expression")
    def _check_expression_is_legal(cls, expression: str) -> str:
        try:
            ast.parse(expression, "", "eval")
        except SyntaxError:
            raise ValueError(f"Failed to parse expression '{expression}'")
        return expression

    @pydantic.validator("simplify")
    def _validate_expression_graph_for_simplify(
        cls, simplify: bool, values: Dict[str, Any]
    ) -> bool:
        if simplify:
            arithmetic_expression_parser.validate_expression(
                expression=values.get("expression", ""), validate_degrees=True
            )
        return simplify

    @pydantic.root_validator()
    def _check_all_variable_are_defined(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        expression: str = values.get("expression", "")
        definitions: ArithmeticDefinitions = values.get("definitions", dict())
        literals = set(re.findall(SUPPORTED_VAR_NAMES_REG, expression))

        not_allowed = literals.intersection(FORBIDDEN_LITERALS)
        if not_allowed:
            raise ValueError(f"The following names: {not_allowed} are not allowed")

        undefined_literals = literals.difference(definitions, SUPPORTED_FUNC_NAMES)
        if undefined_literals:
            raise ValueError(f"{undefined_literals} need to be defined in definitions")
        return values

    @pydantic.root_validator()
    def _substitute_expression(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        expression = values.get("expression")
        definitions = values.get("definitions")
        if expression is None or definitions is None:
            raise ValueError("Valid expression and definition are required")
        new_definition = dict()
        for var_name, value in definitions.items():
            if isinstance(value, RegisterUserInput):
                new_definition[var_name] = value
                continue
            elif isinstance(value, int):
                pass
            elif isinstance(value, float):
                value = FixPointNumber(float_value=value).actual_float_value
            elif isinstance(value, FixPointNumber):
                value = value.actual_float_value
            else:
                raise ValueError(f"{type(value)} type is illegal")

            expression = re.sub(r"\b" + var_name + r"\b", str(value), expression)
        values["expression"] = expression
        values["definitions"] = new_definition
        return values

    @pydantic.validator("definitions")
    def _set_register_names(
        cls, definitions: ArithmeticDefinitions
    ) -> ArithmeticDefinitions:
        for name, reg in definitions.items():
            if isinstance(reg, RegisterUserInput):
                definitions[name] = reg.revalued(name=name)
        return definitions

    def _create_inputs(self) -> None:
        literal_set = (
            set(re.findall("[A-Za-z][A-Za-z0-9]*", self.expression))
            - SUPPORTED_FUNC_NAMES
        )
        self._inputs = {
            name: register
            for name, register in self.definitions.items()
            if name in literal_set and isinstance(register, RegisterUserInput)
        }


class Arithmetic(ArithmeticTemplate):
    output_name: str = "expression_result"
    target: Optional[RegisterUserInput] = None
    uncomputation_method: MappingMethods = MappingMethods.optimized
    inputs_to_save: Set[str] = pydantic.Field(default_factory=set)

    @pydantic.validator("target", always=True)
    def _validate_target_name(
        cls, target: Optional[RegisterUserInput]
    ) -> Optional[RegisterUserInput]:
        if target is None:
            return None
        return target if target.name else target.revalued(name=DEFAULT_TARGET_NAME)

    @pydantic.validator("inputs_to_save", always=True)
    def _validate_inputs_to_save(
        cls, inputs_to_save: Set[str], values: Dict[str, Any]
    ) -> Set[str]:
        assert all(reg in values.get("definitions", {}) for reg in inputs_to_save)
        return inputs_to_save

    def _create_ios(self) -> None:
        self._create_inputs()
        self._outputs = {
            name: self._inputs[name]
            for name in self.inputs_to_save
            if name in self._inputs
        }
        self._outputs[self.output_name] = ArithmeticResultBuilder(
            graph=arithmetic_expression_parser.parse_expression(
                self.expression, validate_degrees=True
            ),
            definitions=self.definitions,
            max_fraction_places=self.max_fraction_places,
            output_name=self.output_name,
        ).result
        if self.target:
            self._inputs[self.target.name] = self.target


class ArithmeticOracle(ArithmeticTemplate):
    uncomputation_method: UncomputationMethods = UncomputationMethods.optimized

    @pydantic.validator("expression")
    def _validate_compare_expression(cls, expression: str) -> str:
        ast_obj = ast.parse(expression, "", "eval")
        if not isinstance(ast_obj, ast.Expression):
            raise ValueError("Must be an expression")
        if not isinstance(ast_obj.body, (ast.Compare, ast.BoolOp)):
            raise ValueError("Must be a comparison expression")
        return expression

    def get_power_order(self) -> Optional[int]:
        return 2

    @staticmethod
    def _arithmetic_expression_output_name() -> str:
        return "expression_result"

    def _create_ios(self) -> None:
        self._create_inputs()
        self._outputs = {**self._inputs}

    def get_arithmetic_expression_params(self) -> Arithmetic:
        return Arithmetic(
            max_fraction_places=self.max_fraction_places,
            expression=self.expression,
            definitions=self.definitions,
            uncomputation_method=self.uncomputation_method,
            qubit_count=self.qubit_count,
            simplify=self.simplify,
            output_name=self._arithmetic_expression_output_name(),
            target=RegisterUserInput(size=1),
            inputs_to_save=set(self.definitions.keys()),
        )
