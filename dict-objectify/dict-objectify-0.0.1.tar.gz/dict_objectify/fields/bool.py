from typing import Optional

from str2bool import str2bool

from dict_objectify.base.field_base import FieldBase


class Bool(FieldBase):
    def _parse_string(self, element: str) -> bool:
        return str2bool(element)

    def _parse_bool(self, element: bool) -> bool:
        return element

    def __get__(self, instance, owner) -> Optional[bool]:
        return super().__get__(instance, owner)
