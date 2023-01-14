from typing import Generic, Iterable, List, Type, TypeVar

from str2bool import str2bool

from dict_objectify.base.base import Base
from dict_objectify.base.constants import NONE_EQUIVALENT_VALUES
from dict_objectify.base.field_base import FieldBase
from dict_objectify.fields.date import datetime

T = TypeVar('T', str, bool, int, float, datetime, FieldBase)


class Array(FieldBase, Generic[T]):
    def __init__(self,
                 model: Type[T],
                 tag: str = None,
                 *,
                 primary: bool = False,
                 nullable: bool = True) -> None:
        super().__init__(tag, primary=primary, nullable=nullable)
        if issubclass(model, FieldBase) and not issubclass(model, Base):
            raise ValueError(f'The Array tag may use either primitives like '
                             f'str, int, and float, or Base objects. '
                             f'It may not currently use field types.'
                             f'The type that was specified is {model}.')
        self.model = model

    def __set__(self, instance, value: List[T]) -> None:
        if value in NONE_EQUIVALENT_VALUES:
            processed_value = value
        else:
            if isinstance(value, (dict, str)) or not isinstance(
                    value, Iterable):
                # Most iterables should work,
                # but not a dictionary or string.
                raise ValueError(
                    f'Tried to set Array tag [Tag: {self.tag}] with '
                    f'a value [Value: {value}] of unsupported '
                    f'[type: {type(value)}].')

            processed_value = [v for v in value
                               if v not in NONE_EQUIVALENT_VALUES]

            if issubclass(self.model, Base):
                processed_value = [element.data_dict
                                   for element in processed_value]

        super().__set__(instance, processed_value)

    def _map(self, element: List) -> List[T]:
        if isinstance(element, (list, set)):
            elements = [e for e in element if e not in NONE_EQUIVALENT_VALUES]
        else:
            elements = element

        if not elements:
            return []

        if self.model is str:
            if not isinstance(elements[0], (str, int, float)):
                raise ValueError(f'Expected list of types convertible to '
                                 f'string, received value [Value: {element}] '
                                 f'of type [Type: {type(elements[0])}] '
                                 f'instead.')
            mapped_element = [str(obj) for obj in elements]
        elif self.model is bool:
            if isinstance(elements[0], bool):
                return elements
            mapped_element = [str2bool(obj) for obj in elements]
        elif self.model is int:
            mapped_element = [int(obj) for obj in elements]
        elif self.model is float:
            mapped_element = [float(obj) for obj in elements]
        elif isinstance(elements, (dict, str)):
            mapped_element = [self.model(data_dict=elements)]
        else:
            mapped_element = [self.model(data_dict=data_dict)
                              for data_dict in elements
                              if data_dict not in NONE_EQUIVALENT_VALUES]

        return [e for e in mapped_element if e not in NONE_EQUIVALENT_VALUES]
