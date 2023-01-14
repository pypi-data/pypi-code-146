from typing import Dict, Optional

from dict_objectify.base.field_base import FieldBase


class Text(FieldBase):
    def _parse_string(self, element: str) -> str:
        return element

    def _parse_float(self, element: float) -> str:
        return str(element)

    def _parse_bytes(self, element: bytes) -> str:
        return element.decode("utf-8")

    def _parse_dict(self, element: Dict) -> str:
        text = element.get('#text')
        if text:
            return text
        else:
            return list(element.values())[0]

    def __get__(self, instance, owner) -> Optional[str]:
        return super().__get__(instance, owner)
