"""Common components for contracts."""

import base64
import copy
from abc import ABC, abstractmethod
from dataclasses import (_FIELD_BASE, _FIELDS, Field, _is_dataclass_instance,
                         asdict, dataclass, field, fields)
from typing import Optional

from requests import Response

__all__ = [
    'ContractException',
    'Contractor',
    'ContractEvent',
    'ContractEventFactory'
]


class ContractException(Exception):
    ...


class Contractor(ABC):

    _URL = None

    _HEADERS = {
        'accept': 'application/json',
        'content-type': 'application/json'
    }

    MOCK_TASK_ID = '5df72f4a97ef4e358e7c610bc2bdfa14'

    EVERYONE = ['*']

    @abstractmethod
    def _validate_response(self, resp: Response) -> None:
        """Validate response. Should only focus on problems unrelated to business logic."""
        ...


def _asdict_pickled(obj, *, dict_factory=dict):
    """Make `asdict` compitable with cloudpickled dataclass object.

    The original `asdict` implementation is not compitable with cloudpickled dataclass
    object. It returns empty dict if the dataclass' module is `__main__`.
    """
    obj_dict = asdict(obj)
    if obj_dict:
        return obj_dict
    else:
        return _asdict_inner_pickled(obj, dict_factory)


def _asdict_inner_pickled(obj, dict_factory):
    if _is_dataclass_instance(obj):
        result = []
        for f in fields_pickled(obj):
            value = _asdict_inner_pickled(getattr(obj, f.name), dict_factory)
            result.append((f.name, value))
        return dict_factory(result)
    elif isinstance(obj, tuple) and hasattr(obj, '_fields'):
        return type(obj)(*[_asdict_inner_pickled(v, dict_factory) for v in obj])
    elif isinstance(obj, (list, tuple)):
        return type(obj)(_asdict_inner_pickled(v, dict_factory) for v in obj)
    elif isinstance(obj, dict):
        return type(obj)((_asdict_inner_pickled(k, dict_factory),
                          _asdict_inner_pickled(v, dict_factory))
                         for k, v in obj.items())
    else:
        return copy.deepcopy(obj)


def fields_pickled(class_or_instance):
    try:
        fields = getattr(class_or_instance, _FIELDS)
    except AttributeError:
        raise TypeError('must be called with a dataclass type or instance')

    return tuple(f for f in fields.values()
                 if (isinstance(f, Field)
                     and isinstance(f._field_type, _FIELD_BASE)
                     and f._field_type.name == '_FIELD'))


@dataclass
class ContractEvent(ABC):
    """合约事件."""

    TYPE = None

    type: str = field(init=False)

    def __post_init__(self):
        self.type = self.TYPE

    @classmethod
    def contract_to_event(cls, contract: dict) -> 'ContractEvent':
        raise NotImplementedError()

    def event_to_contract(self) -> dict:
        dict_obj = _asdict_pickled(self)
        for _key, _value in dict_obj.items():
            if isinstance(_value, bytes):
                dict_obj[_key] = base64.b64encode(_value).decode()
        return dict_obj

    def _get_origin_type(self, _type):
        """Return the original type(types).

        To facilitate `isinstance` check for values.

        `Note: Only unwrap the most outer layer. For example: Union[str, List[str]] will be
        unwrapped as (str, list).`
        """
        if isinstance(_type, type):
            return _type
        elif _type.__module__ == 'typing':
            if isinstance(_type.__origin__, type):
                return _type.__origin__
            else:
                return tuple(self._get_origin_type(_arg_type) for _arg_type in _type.__args__)
        else:
            raise ValueError('wrong')

    def validate(self) -> None:
        """To validate event data and raise errors if failed."""
        for _field in fields(self):
            _name = _field.name
            _type = _field.type
            _default = _field.default
            _value = self.__getattribute__(_name)
            _original_type = self._get_origin_type(_type)
            if _default is None:
                assert (
                    _value is None or isinstance(_value, _original_type)
                ), f'invalid {_name} value: {_value}'
            else:
                assert (
                    _value is not None and isinstance(_value, _original_type)
                ), f'invalid {_name} value: {_value}'


class ContractEventFactory(ABC):
    """A factory to convert contract text to a ContractEvent object."""

    @classmethod
    @abstractmethod
    def contract_to_event(cls, contract: dict) -> Optional[ContractEvent]:
        """Decode contract data into event objects and handle errors."""
        ...
