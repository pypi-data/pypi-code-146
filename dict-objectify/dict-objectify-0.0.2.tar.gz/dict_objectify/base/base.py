from datetime import datetime
from typing import Any, Dict, List, Tuple

from dict_objectify.base.constants import NONE_EQUIVALENT_VALUES
from dict_objectify.base.field_base import FieldBase
from dict_objectify.base.hash import dict_base_hash


class BaseMeta(type):
    def __new__(mcs, name, bases, class_dict):
        hash_fields = [key
                       for key, value in class_dict.items()
                       if isinstance(value, FieldBase)
                       and value.primary]
        for base in bases:
            if hasattr(base, '_hash_fields'):
                hash_fields.extend(base._hash_fields)
        class_dict['_hash_fields'] = hash_fields

        return super(BaseMeta, mcs).__new__(mcs, name, bases, class_dict)


class Base(FieldBase, metaclass=BaseMeta):
    def __init__(self,
                 *,
                 tag: str = None,
                 data_dict: Dict = None,
                 primary: bool = False,
                 nullable: bool = True,
                 **kwargs) -> None:
        self.data_dict = data_dict if data_dict else dict()
        for key, value in kwargs.items():
            self.__setattr__(key, value)
        super().__init__(tag=tag, primary=primary, nullable=nullable)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__hash__() == other.__hash__()
        return False

    def __hash__(self):
        if self._hash_fields:
            return sum(self.__getattribute__(primary_attr).__hash__()
                       for primary_attr in self._hash_fields
                       if hasattr(self, primary_attr))
        else:
            return dict_base_hash(self.data_dict)

    def __set__(self, instance, value):
        if issubclass(type(value), self.__class__):
            value = value.data_dict
        elif value not in NONE_EQUIVALENT_VALUES:
            raise ValueError(f'Tried to set a value [Value: {value}] '
                             f'of an unsupported type [Type: {type(value)}] '
                             f'on an object with tag [Tag: {self.tag}].')
        super().__set__(instance, value)

    def _map(self, element: Dict) -> Any:
        return type(self)(data_dict=element)

    def _properties(self) -> List[Tuple[str, Any]]:
        return [(p, getattr(self, p)) for p in dir(self.__class__) if
                isinstance(getattr(self.__class__, p), (property, FieldBase))]

    def to_dict(self) -> Dict:
        dct = {}
        for p, attr in self._properties():
            if attr in NONE_EQUIVALENT_VALUES:
                continue
            elif isinstance(attr, (str, int, float, bool)):
                dct[p] = attr
            elif isinstance(attr, datetime):
                dct[p] = attr.strftime('%Y-%m-%d')
            elif isinstance(attr, list):
                if isinstance(attr[0], (str, int, bool)):
                    dct[p] = attr
                elif isinstance(attr[0], datetime):
                    dct[p] = [date.strftime('%Y-%m-%d') for date in attr]
                else:
                    dct[p] = [element.to_dict() for element in attr]
            else:
                dct[p] = attr.to_dict()

        for p, attr in self._properties():
            if p in dct and dct[p] in NONE_EQUIVALENT_VALUES:
                del dct[p]

        return dct

    def is_empty(self) -> bool:
        return True if not self.data_dict else False

    def __str__(self):
        return str(self.to_dict())

    def __bool__(self):
        return bool(self.data_dict)


class MixinBase(object, metaclass=BaseMeta):
    pass
