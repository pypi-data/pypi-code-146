from typing import Any, List, Optional

from dict_objectify.base.constants import NONE_EQUIVALENT_VALUES
from dict_objectify.base.field_base import FieldBase


class EnumField(FieldBase):
    def __init__(self,
                 enumeration: List[Any],
                 tag: str = None,
                 *,
                 primary: bool = False,
                 nullable: bool = True) -> None:
        super().__init__(tag, primary=primary, nullable=nullable)

        if any([e in NONE_EQUIVALENT_VALUES for e in enumeration]):
            raise ValueError(
                f'Got a None-equivalent as an allowed enumeration value in '
                f'enum with tag [Tag: {self.tag}] '
                f'Please use the parameter `nullable` to allow this field to '
                f'be `None`. [Enumeration: {enumeration}]'
            )
        if len({type(e) for e in enumeration}) > 1:
            raise TypeError('All the elements in enumeration '
                            'must have the same type')

        self.enumeration = enumeration

    def __set__(self, instance, value):
        if value in self.enumeration:
            super().__set__(instance, value)
        elif value in NONE_EQUIVALENT_VALUES and self.nullable:
            super().__set__(instance, value)
        else:
            raise ValueError(
                f'Attempted to set value [Value: {value}] '
                f'of type [Type: {type(value)}] '
                f'in a class of type [Type: {type(instance)}] '
                f'in enumeration with tag [Tag: {self.tag}]. '
                f'Allowed values are [Enumeration: {self.enumeration}], '
                f'and the tag {"is" if self.nullable else "is not"} nullable.')

    def _process(self, element: Any) -> Optional[Any]:
        return element
