from typing import Optional

from dict_objectify.base.field_base import FieldBase


class Integer(FieldBase):
    def _parse_string(self, element: str) -> int:
        return int(element)

    def _parse_integer(self, element: int) -> int:
        return element

    def _parse_float(self, element: float) -> int:
        return int(element)

    def __get__(self, instance, owner) -> Optional[int]:
        return super().__get__(instance, owner)
