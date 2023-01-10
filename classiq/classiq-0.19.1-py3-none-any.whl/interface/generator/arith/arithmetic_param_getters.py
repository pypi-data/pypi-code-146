from typing import Callable, Dict, List, Optional, Union

from classiq.interface.generator.arith.arithmetic_operations import (
    ArithmeticOperationParams,
)
from classiq.interface.generator.arith.ast_node_rewrite import SEPARATOR
from classiq.interface.generator.arith.binary_ops import (
    Adder,
    BitwiseAnd,
    BitwiseOr,
    BitwiseXor,
    CyclicShift,
    Equal,
    GreaterEqual,
    GreaterThan,
    LessEqual,
    LessThan,
    LShift,
    Max,
    Min,
    Multiplier,
    NotEqual,
    RShift,
    Subtractor,
)
from classiq.interface.generator.arith.fix_point_number import FixPointNumber
from classiq.interface.generator.arith.logical_ops import LogicalAnd, LogicalOr
from classiq.interface.generator.arith.register_user_input import RegisterUserInput
from classiq.interface.generator.arith.unary_ops import BitwiseInvert, Negation

from classiq.exceptions import ClassiqArithmeticError

IntOrRegister = Union[int, RegisterUserInput]
FixPointOrRegister = Union[FixPointNumber, RegisterUserInput]
ParamsGetter = Callable[..., ArithmeticOperationParams]  # Argument vary

_TARGET_ERROR_MESSAGE: str = "Target unavailable for the requested operation"


def id2op(node_id: str) -> str:
    return node_id.rsplit(SEPARATOR)[0]


def get_params_type(node_id: str) -> ParamsGetter:
    return params_getter_map[id2op(node_id)]


def or_params_getter(
    left_arg: IntOrRegister,
    right_arg: IntOrRegister,
    output_name: str,
    output_size: Optional[int] = None,
    inplace_arg: Optional[str] = None,
    target: Optional[RegisterUserInput] = None,
) -> ArithmeticOperationParams:
    if target is not None:
        raise ClassiqArithmeticError(_TARGET_ERROR_MESSAGE)
    return BitwiseOr(
        left_arg=left_arg,
        right_arg=right_arg,
        output_name=output_name,
        output_size=output_size,
    )


def and_params_getter(
    left_arg: IntOrRegister,
    right_arg: IntOrRegister,
    output_name: str,
    output_size: Optional[int] = None,
    inplace_arg: Optional[str] = None,
    target: Optional[RegisterUserInput] = None,
) -> ArithmeticOperationParams:
    if target is not None:
        raise ClassiqArithmeticError(_TARGET_ERROR_MESSAGE)
    return BitwiseAnd(
        left_arg=left_arg,
        right_arg=right_arg,
        output_name=output_name,
        output_size=output_size,
    )


def xor_params_getter(
    left_arg: IntOrRegister,
    right_arg: IntOrRegister,
    output_name: str,
    output_size: Optional[int] = None,
    inplace_arg: Optional[str] = None,
    target: Optional[RegisterUserInput] = None,
) -> ArithmeticOperationParams:
    if target is not None:
        raise ClassiqArithmeticError(_TARGET_ERROR_MESSAGE)
    return BitwiseXor(
        left_arg=left_arg,
        right_arg=right_arg,
        output_name=output_name,
        output_size=output_size,
    )


def invert_params_getter(
    arg: IntOrRegister,
    output_name: str,
    output_size: Optional[int] = None,
    inplace_arg: Optional[str] = None,
    target: Optional[RegisterUserInput] = None,
) -> ArithmeticOperationParams:
    if target is not None:
        raise ClassiqArithmeticError(_TARGET_ERROR_MESSAGE)
    return BitwiseInvert(
        arg=arg,
        output_name=output_name,
        output_size=output_size,
        inplace=inplace_arg is not None,
    )


def usub_params_getter(
    arg: IntOrRegister,
    output_name: str,
    output_size: Optional[int] = None,
    inplace_arg: Optional[str] = None,
    target: Optional[RegisterUserInput] = None,
) -> ArithmeticOperationParams:
    if target is not None:
        raise ClassiqArithmeticError(_TARGET_ERROR_MESSAGE)
    return Negation(
        arg=arg,
        output_name=output_name,
        output_size=output_size,
        inplace=inplace_arg is not None,
    )


def adder_params_getter(
    left_arg: FixPointOrRegister,
    right_arg: FixPointOrRegister,
    output_name: str,
    output_size: Optional[int] = None,
    inplace_arg: Optional[str] = None,
    target: Optional[RegisterUserInput] = None,
) -> ArithmeticOperationParams:
    if target is not None:
        raise ClassiqArithmeticError(_TARGET_ERROR_MESSAGE)
    return Adder(
        left_arg=left_arg,
        right_arg=right_arg,
        inplace_arg=inplace_arg,
        output_name=output_name,
        output_size=output_size,
    )


def multiplier_params_getter(
    left_arg: FixPointOrRegister,
    right_arg: FixPointOrRegister,
    output_name: str,
    output_size: Optional[int] = None,
    inplace_arg: Optional[str] = None,
    target: Optional[RegisterUserInput] = None,
) -> ArithmeticOperationParams:
    if target is not None:
        raise ClassiqArithmeticError(_TARGET_ERROR_MESSAGE)
    return Multiplier(
        left_arg=left_arg,
        right_arg=right_arg,
        output_name=output_name,
        output_size=output_size,
    )


def min_params_getter(
    left_arg: FixPointOrRegister,
    right_arg: FixPointOrRegister,
    output_name: str,
    output_size: Optional[int] = None,
    inplace_arg: Optional[str] = None,
    target: Optional[RegisterUserInput] = None,
) -> ArithmeticOperationParams:
    if target is not None:
        raise ClassiqArithmeticError(_TARGET_ERROR_MESSAGE)
    return Min(
        left_arg=left_arg,
        right_arg=right_arg,
        output_name=output_name,
        output_size=output_size,
    )


def max_params_getter(
    left_arg: FixPointOrRegister,
    right_arg: FixPointOrRegister,
    output_name: str,
    output_size: Optional[int] = None,
    inplace_arg: Optional[str] = None,
    target: Optional[RegisterUserInput] = None,
) -> ArithmeticOperationParams:
    if target is not None:
        raise ClassiqArithmeticError(_TARGET_ERROR_MESSAGE)
    return Max(
        left_arg=left_arg,
        right_arg=right_arg,
        output_name=output_name,
        output_size=output_size,
    )


def sub_params_getter(
    left_arg: FixPointOrRegister,
    right_arg: FixPointOrRegister,
    output_name: str,
    output_size: Optional[int] = None,
    inplace_arg: Optional[str] = None,
    target: Optional[RegisterUserInput] = None,
) -> ArithmeticOperationParams:
    if target is not None:
        raise ClassiqArithmeticError(_TARGET_ERROR_MESSAGE)
    return Subtractor(
        left_arg=left_arg,
        right_arg=right_arg,
        inplace_arg=inplace_arg,
        output_name=output_name,
        output_size=output_size,
    )


def equal_params_getter(
    left_arg: FixPointOrRegister,
    right_arg: FixPointOrRegister,
    output_name: str,
    output_size: Optional[int] = None,
    inplace_arg: Optional[str] = None,
    target: Optional[RegisterUserInput] = None,
) -> ArithmeticOperationParams:
    return Equal(
        left_arg=left_arg, right_arg=right_arg, output_name=output_name, target=target
    )


def not_equal_params_getter(
    left_arg: FixPointOrRegister,
    right_arg: FixPointOrRegister,
    output_name: str,
    output_size: Optional[int] = None,
    inplace_arg: Optional[str] = None,
    target: Optional[RegisterUserInput] = None,
) -> ArithmeticOperationParams:
    return NotEqual(
        left_arg=left_arg, right_arg=right_arg, output_name=output_name, target=target
    )


def greater_than_params_getter(
    left_arg: FixPointOrRegister,
    right_arg: FixPointOrRegister,
    output_name: str,
    output_size: Optional[int] = None,
    inplace_arg: Optional[str] = None,
    target: Optional[RegisterUserInput] = None,
) -> ArithmeticOperationParams:
    return GreaterThan(
        left_arg=left_arg, right_arg=right_arg, output_name=output_name, target=target
    )


def greater_equal_params_getter(
    left_arg: FixPointOrRegister,
    right_arg: FixPointOrRegister,
    output_name: str,
    output_size: Optional[int] = None,
    inplace_arg: Optional[str] = None,
    target: Optional[RegisterUserInput] = None,
) -> ArithmeticOperationParams:
    return GreaterEqual(
        left_arg=left_arg, right_arg=right_arg, output_name=output_name, target=target
    )


def less_than_params_getter(
    left_arg: FixPointOrRegister,
    right_arg: FixPointOrRegister,
    output_name: str,
    output_size: Optional[int] = None,
    inplace_arg: Optional[str] = None,
    target: Optional[RegisterUserInput] = None,
) -> ArithmeticOperationParams:
    return LessThan(
        left_arg=left_arg, right_arg=right_arg, output_name=output_name, target=target
    )


def less_equal_params_getter(
    left_arg: FixPointOrRegister,
    right_arg: FixPointOrRegister,
    output_name: str,
    output_size: Optional[int] = None,
    inplace_arg: Optional[str] = None,
    target: Optional[RegisterUserInput] = None,
) -> ArithmeticOperationParams:
    return LessEqual(
        left_arg=left_arg, right_arg=right_arg, output_name=output_name, target=target
    )


def logical_and_params_getter(
    *arg: List[FixPointOrRegister],
    output_name: str,
    output_size: Optional[int] = None,
    inplace_arg: Optional[str] = None,
    target: Optional[RegisterUserInput] = None
) -> ArithmeticOperationParams:
    return LogicalAnd(args=arg, output_name=output_name, target=target)


def logical_or_params_getter(
    *arg: List[FixPointOrRegister],
    output_name: str,
    output_size: Optional[int] = None,
    inplace_arg: Optional[str] = None,
    target: Optional[RegisterUserInput] = None
) -> ArithmeticOperationParams:
    return LogicalOr(args=arg, output_name=output_name, target=target)


def lshift_params_getter(
    left_arg: RegisterUserInput,
    right_arg: int,
    output_name: str,
    output_size: Optional[int] = None,
    inplace_arg: Optional[str] = None,
    target: Optional[RegisterUserInput] = None,
) -> ArithmeticOperationParams:
    if target is not None:
        raise ClassiqArithmeticError(_TARGET_ERROR_MESSAGE)
    return LShift(
        left_arg=left_arg,
        right_arg=right_arg,
        output_name=output_name,
        inplace_arg=inplace_arg,
    )


def rshift_params_getter(
    left_arg: RegisterUserInput,
    right_arg: int,
    output_name: str,
    output_size: Optional[int] = None,
    inplace_arg: Optional[str] = None,
    target: Optional[RegisterUserInput] = None,
) -> ArithmeticOperationParams:
    if target is not None:
        raise ClassiqArithmeticError(_TARGET_ERROR_MESSAGE)
    return RShift(
        left_arg=left_arg,
        right_arg=right_arg,
        output_name=output_name,
        inplace_arg=inplace_arg,
    )


def clshift_params_getter(
    left_arg: RegisterUserInput,
    right_arg: int,
    output_name: str,
    output_size: Optional[int] = None,
    inplace_arg: Optional[str] = None,
    target: Optional[RegisterUserInput] = None,
) -> ArithmeticOperationParams:
    if target is not None:
        raise ClassiqArithmeticError(_TARGET_ERROR_MESSAGE)
    return CyclicShift(
        left_arg=left_arg,
        right_arg=-right_arg,
        output_name=output_name,
        inplace_arg=inplace_arg,
    )


def crshift_params_getter(
    left_arg: RegisterUserInput,
    right_arg: int,
    output_name: str,
    output_size: Optional[int] = None,
    inplace_arg: Optional[str] = None,
    target: Optional[RegisterUserInput] = None,
) -> ArithmeticOperationParams:
    if target is not None:
        raise ClassiqArithmeticError(_TARGET_ERROR_MESSAGE)
    return CyclicShift(
        left_arg=left_arg,
        right_arg=right_arg,
        output_name=output_name,
        inplace_arg=inplace_arg,
    )


params_getter_map: Dict[str, ParamsGetter] = dict(
    BitOr=or_params_getter,
    BitAnd=and_params_getter,
    BitXor=xor_params_getter,
    Add=adder_params_getter,
    Invert=invert_params_getter,
    Eq=equal_params_getter,
    And=logical_and_params_getter,
    Or=logical_or_params_getter,
    USub=usub_params_getter,
    Sub=sub_params_getter,
    Mult=multiplier_params_getter,
    Gt=greater_than_params_getter,
    GtE=greater_equal_params_getter,
    Lt=less_than_params_getter,
    LtE=less_equal_params_getter,
    NotEq=not_equal_params_getter,
    RShift=rshift_params_getter,
    LShift=lshift_params_getter,
    CRShift=crshift_params_getter,
    CLShift=clshift_params_getter,
    min=min_params_getter,
    max=max_params_getter,
)
