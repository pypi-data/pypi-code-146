from typing import Optional

from dict_objectify.base.field_base import FieldBase


class Float(FieldBase):
    def _parse_string(self, element: str) -> float:
        return float(element)

    def _parse_integer(self, element: int) -> float:
        return float(element)

    def _parse_float(self, element: float) -> float:
        return element

    def __get__(self, instance, owner) -> Optional[float]:
        return super().__get__(instance, owner)
