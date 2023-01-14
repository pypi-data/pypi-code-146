from datetime import datetime
from typing import Any, Dict, List, Optional, Set

from dict_objectify.base.constants import NONE_EQUIVALENT_VALUES


class FieldBase(object):
    def __init__(self,
                 tag: str = None,
                 *,
                 primary: bool = False,
                 nullable: bool = True) -> None:
        self.tag = tag
        self.primary = primary
        self.nullable = nullable

    def __set_name__(self, owner, name):
        self._name = name
        if not self.tag:
            self.tag = name

    def __get__(self, instance, owner) -> Optional[Any]:
        if instance is not None:
            try:
                element = instance.data_dict[self.tag]
            except KeyError:
                raise AttributeError(f'Missing dict key for [{self.tag}]')
            if element not in NONE_EQUIVALENT_VALUES:
                element = self._map(element)
            return element
        else:
            return self

    def __set__(self, instance, value):
        data_dict = instance.data_dict
        if value in NONE_EQUIVALENT_VALUES and not self.nullable:
            raise ValueError(f'[Field: {self.tag}] '
                             f'in a class of type [Type: {type(instance)}] '
                             f'is not nullable. '
                             f'Attempted to set a None-equivalent value. '
                             f'[Value: {value}]')
        else:
            data_dict[self.tag] = value

    def _map(self, element: Any) -> Any:
        return self._process(element)

    def _process(self, element: Any) -> Optional[Any]:

        if isinstance(element, bool):
            return self._parse_bool(element)
        elif isinstance(element, int):
            return self._parse_integer(element)
        elif isinstance(element, str):
            return self._parse_string(element)
        elif isinstance(element, float):
            return self._parse_float(element)
        elif isinstance(element, bytes):
            return self._parse_bytes(element)
        elif isinstance(element, Dict):
            return self._parse_dict(element)
        elif isinstance(element, List):
            return self._parse_list(element)
        elif isinstance(element, Set):
            return self._parse_set(element)
        elif isinstance(element, datetime):
            return self._parse_datetime(element)

        else:
            return self._parse_unsupported_type(element)

    def _parse_integer(self, element: int) -> Optional[Any]:
        return self._parse_unsupported_type(element)

    def _parse_string(self, element: str) -> Optional[Any]:
        return self._parse_unsupported_type(element)

    def _parse_bool(self, element: bool) -> Optional[Any]:
        return self._parse_unsupported_type(element)

    def _parse_float(self, element: float) -> Optional[Any]:
        return self._parse_unsupported_type(element)

    def _parse_bytes(self, element: bytes) -> Optional[Any]:
        return self._parse_unsupported_type(element)

    def _parse_dict(self, element: Dict) -> Optional[Any]:
        return self._parse_unsupported_type(element)

    def _parse_list(self, element: List) -> Optional[Any]:
        return self._parse_unsupported_type(element)

    def _parse_set(self, element: Set) -> Optional[Any]:
        return self._parse_unsupported_type(element)

    def _parse_datetime(self, element: datetime) -> Optional[Any]:
        return self._parse_unsupported_type(element)

    def _parse_unsupported_type(self, element) -> Optional[Any]:
        raise ValueError(f'[Value: {element}] of [tag: {self.tag}] '
                         f'is of an unsupported [type: {type(element)}].')
