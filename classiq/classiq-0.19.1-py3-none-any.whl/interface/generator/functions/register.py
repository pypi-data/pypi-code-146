from __future__ import annotations

from operator import attrgetter
from typing import Iterable, Tuple

import pydantic
from pydantic import BaseModel

from classiq.interface.helpers.custom_pydantic_types import PydanticNonEmptyString

QubitsType = Tuple[pydantic.NonNegativeInt, ...]


class Register(BaseModel):
    """
    A user-defined custom register.
    """

    name: PydanticNonEmptyString = pydantic.Field(
        description="The name of the custom register",
    )

    qubits: QubitsType = pydantic.Field(
        description="A tuple of qubits as integers as indexed within a custom function code",
    )

    @property
    def width(self) -> pydantic.PositiveInt:
        """The number of qubits of the custom register"""
        return len(self.qubits)

    @pydantic.validator("qubits")
    def validate_qubits(cls, qubits: QubitsType):
        if len(qubits) == 0:
            raise ValueError("qubits field must be non-empty.")
        if len(set(qubits)) != len(qubits):
            raise ValueError("All qubits of a register must be distinct.")
        return qubits


def get_register_names(reg_list: Iterable[Register]) -> Iterable[str]:
    return map(attrgetter("name"), reg_list)
