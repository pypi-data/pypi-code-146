#
#  Copyright (c) 2021.  Budo Systems
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#  http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#
#

"""Query builder classes."""
from __future__ import annotations

from abc import abstractmethod, ABC
from typing import Any, Generic, TypeVar, Protocol, Sequence, Union, cast

import asyncio
import operator

from attr import attrs

@attrs
class Query:
    """Root class of a query."""
    criteria: Predicate
    result_type: Union[EntityType, list[Field]]

class EntityType:
    """An entity in the query language."""

class Field:
    """A field in the query language."""


ExpressionResult_co = TypeVar("ExpressionResult_co", covariant=True)
"""Type variable for the final result of an evaluated `Expression` (covariant type)."""

ExpressionResult = TypeVar("ExpressionResult")
"""Type variable for the final result of an evaluated `Expression` (invariant type)."""


class Expression(Generic[ExpressionResult_co], ABC):
    """A combination of primitives and operators that evaluate to a concrete type."""

    @abstractmethod
    async def eval(self) -> ExpressionResult_co:
        """Final evaluation of the expression."""


Predicate = Expression[bool]
"""A combination of primitives and operators that evaluate to a boolean."""


class LiteralExpression(Expression[ExpressionResult_co]):
    """A simple concrete value expression representing a literal."""
    value: ExpressionResult_co

    def __init__(self, value: ExpressionResult_co) -> None:
        self.value = value

    async def eval(self) -> ExpressionResult_co:
        """Evaluation of the literal expression."""
        return self.value


class VariableExpression(Expression[ExpressionResult_co], ABC):
    """A generic variable in the query language."""
    name: str

    def __init__(self, name: str, **_kwargs: Any) -> None:
        self.name = name


OperandType_contra = TypeVar("OperandType_contra", contravariant=True)
"""Type variable for the operands of an `Operator`."""

OperationResult_co = TypeVar("OperationResult_co", covariant=True)
"""Type variable for the result of an `Operator`."""

# OpSignature = TypeVar("OpSignature", bound=Callable[[object, ...], Any])
# """Type variable for the signature of the function that will evaluate the `Operator`."""

class OpSignature(Protocol[OperandType_contra, OperationResult_co]):
    """Callback protocol for the signature of the function tha will evaluate the `Operator`."""
    def __call__(self, *args: OperandType_contra) -> OperationResult_co:
        ...

class Operator(Generic[OperandType_contra, OperationResult_co], ABC):
    """An operator_func that combines components to evaluate to some value during the query."""

    def __init__(self, op: OpSignature[OperandType_contra, OperationResult_co]) -> None:
        self.op = op

    @abstractmethod
    def __call__(self,
                 *args: Expression[OperandType_contra]
                 ) -> OperationExpression[OperandType_contra, OperationResult_co]:
        ...


class OperationExpression(
        Generic[OperandType_contra, OperationResult_co],
        Expression[OperationResult_co],
        ABC
):
    """Evaluable operator_func expression."""

    def __init__(self,
                 operator_func: Operator[OperandType_contra, OperationResult_co],
                 *operands: Expression[OperandType_contra]
                 ) -> None:
        self.operator: Operator[OperandType_contra, OperationResult_co] = operator_func
        self.operands: list[Expression[OperandType_contra]] = list(operands)


class ClosedOperationExpression(OperationExpression[ExpressionResult, ExpressionResult]):
    """Evaluable operator_func expression which give results of the same type as it's operands"""

    async def eval(self) -> ExpressionResult:
        """Evaluates the operands according to the operator_func.

        This default implementation assumes binary operators that evaluate to the same type
        as its operands.
        """

        if len(self.operands) == 0:
            raise AttributeError("No operands to evaluate.")

        values: Sequence[ExpressionResult] = \
            await asyncio.gather(*[op.eval() for op in self.operands])
        result = values[0]
        for i in range(1, len(values)):
            result = self.operator.op(result, values[i])

        return result


class BooleanOperationExpression(ClosedOperationExpression[bool]):
    """Bridge class"""


class BooleanOperator(Operator[bool, bool]):
    """Once evaluated, instances of this operator will return the truth value of all it's boolean
    operands combined by the same operator."""

    def __call__(self, *args: Predicate) -> BooleanOperationExpression:
        return BooleanOperationExpression(self, *args)


class Comparable(Protocol):
    """Any object that supports comparison operators."""

    def __lt__(self, other: Any) -> bool: ...
    def __le__(self, other: Any) -> bool: ...
    def __gt__(self, other: Any) -> bool: ...
    def __ge__(self, other: Any) -> bool: ...
    def __eq__(self, other: Any) -> bool: ...
    def __ne__(self, other: Any) -> bool: ...


class ComparableExpression(Expression[Comparable], ABC):
    """Type of expression that results in a concrete type that supports comparisons."""


class ComparisonOperator(
        Operator[Comparable, bool]):
    """Once evaluated, instances of this operator will return the truth value of all it's operands
    when compared to one another in the order they were given by the same comparator."""

    def __call__(self,
                 *args: Expression[Comparable]
                 ) -> OperationExpression[Comparable, bool]:
        return ComparisonOperationExpression(self, *args)


class ComparisonOperationExpression(OperationExpression[Comparable, bool]):
    """Evaluable comparison operator_func."""
    operator: ComparisonOperator

    async def eval(self) -> bool:
        """Evaluates the operands according to the operator_func."""

        if len(self.operands) < 2:
            raise AttributeError("Not enough operands to compare.")

        values: Sequence[Comparable] = await asyncio.gather(*[op.eval() for op in self.operands])

        result = True
        for i in range(1, len(values)):
            result = result and self.operator.op(values[i - 1], values[i])

        return result


_BOS = OpSignature[bool, bool]

AND = BooleanOperator(cast(_BOS, operator.and_))
"""AND query operator."""

OR = BooleanOperator(cast(_BOS, operator.or_))
"""OR query operator."""

XOR = BooleanOperator(cast(_BOS, operator.xor))
"""XOR (Exclusive Or) query operator."""


_COS = OpSignature[Comparable, bool]

LE = ComparisonOperator(cast(_COS, operator.le))
"""LE (Less Than Or Equal) query operator."""

LT = ComparisonOperator(cast(_COS, operator.lt))
"""LT (Less Than) query operator."""

GE = ComparisonOperator(cast(_COS, operator.ge))
"""GE (Greater Than Or Equal) query operator."""

GT = ComparisonOperator(cast(_COS, operator.gt))
"""GT (Greater Than) query operator."""

EQ = ComparisonOperator(cast(_COS, operator.eq))
"""EQ (Equals) query operator."""

NE = ComparisonOperator(cast(_COS, operator.ne))
"""NE (Not Equals) query operator."""

TRUE = LiteralExpression[bool](True)
"""TRUE query literal."""

FALSE = LiteralExpression[bool](False)
"""FALSE query literal."""

NONE = LiteralExpression[None](None)
"""NONE query literal."""
