#
#  Copyright (c) 2021.  Budo Systems
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#  http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#
#

"""Core set of classes from which most other model classes will inherit."""

from __future__ import annotations

# from enum import Enum
from uuid import uuid4, uuid5, UUID
from warnings import warn
from inspect import getmembers, ismethod, signature

from attr import field, resolve_types, fields_dict, fields, Factory
from attr.setters import frozen
from attrs_strict import type_validator, AttributeTypeError

from ..utils import SingletonMeta
from .. import typehints as th
from .validation import ValidationWarning, DeserializationWarning
from .meta import BudoBase, frozen_field, SingletonBudoMeta

__all__ = ['Entity', 'BasicInfo', 'ValueObject', 'from_dict', 'validate',
           'MissingUUID', 'MissingBudoObject']

#:  Type variable
BudoType = th.TypeVar('BudoType', bound=BudoBase)


def from_dict(cls: th.Type[BudoType], data: th.IMapStrAny) -> BudoType:
    """Creates a new instance of the `BudoType` `cls` from the provided `data`."""
    resolve_types(cls)
    params: dict[str, th.Any] = {}
    cls_fields = fields_dict(cls)

    for k, v in data.items():
        warning_err: th.Optional[Exception] = None
        param_type = cls_fields[k].type
        if isinstance(param_type, type):
            if isinstance(v, param_type):
                params[k] = v
                continue

            try:
                type_sig = signature(param_type)
                if len(type_sig.parameters) > 0:
                    params[k] = param_type(v)
                    continue
            except ValueError as v_err:
                warning_err = v_err
            except TypeError as t_err:
                warning_err = t_err
        warn_txt = f"Cannot coerce value {v} to type {param_type} for key {k}"
        warn(DeserializationWarning(msg_txt=warn_txt, exception=warning_err))
        params[k] = v

    return cls(**params)


def validate(obj: th.Any) -> bool:
    """Object validator.

    Calls each validator defined (methods with a name starting with ``_validate_``).

    :returns: True if all validators are satisfied, False if any validator fails.
    """
    valid = True
    validators = getmembers(obj, lambda a: ismethod(a) and a.__name__.startswith('_validate_'))
    for _v_name, v_method in validators:
        # Call all the validators regardless of previous results
        # to issue any validation warnings they might find
        valid = v_method() and valid
    return valid


class MissingUUID(UUID, metaclass=SingletonMeta, hex='0'*32):
    """Sentinel `UUID` for determining if one is missing from the arguments when instantiating
    an `Entity`"""


class MissingBudoObject(BudoBase, metaclass=SingletonBudoMeta):
    """Sentinel `BudoBase` object."""


class Entity(BudoBase):
    """
    Instance level commonalities for all model classes.
    """

    id_name: str = field(eq=False, order=False, hash=False, factory=lambda: str(uuid4()))
    """(Optional) The field that will be used to generate the `entity_id`"""

    entity_id: UUID = field(default=MissingUUID(), eq=True, hash=True, on_setattr=frozen)
    """
    (Optional) The unique identifier for an instance of `Entity` (and all its subclasses)
    """

    def __attrs_post_init__(self) -> None:
        if self.entity_id is MissingUUID():
            object.__setattr__(self, 'entity_id',
                               uuid5(self.__class__.uuid, str(self.id_name)))

    # @th.Property[UUID]
    # def entity_id(obj) -> UUID:
    #     """Main identifier for the object."""
    #     return obj._entity_id

    def _validate_field_value_types(self) -> bool:
        assert isinstance(self, th.AttrsClass)
        resolve_types(type(self))
        strict_type_validator = type_validator(empty_ok=False)
        # optional_type = type_validator(empty_ok=True)

        valid = True
        for fld in fields(type(self)):  # pylint: disable=not-an-iterable
            if fld.type:
                value = self.__dict__[fld.name]
                try:
                    strict_type_validator(self, fld, value)
                except AttributeTypeError as err:
                    valid = False
                    v_warn = ValidationWarning(
                            msg_txt='Attribute value does not match specified type',
                            details={
                                    'name':          fld.name,
                                    'value':         value,
                                    'expected type': fld.type,
                                    'actual type':   type(value),
                                    'err':           err
                            })
                    warn(v_warn)
                except TypeError as err:
                    valid = False
                    v_warn = ValidationWarning(msg_txt='Encountered an Error during validation',
                                               details=err)
                    warn(v_warn)

        return valid


def _slug(self: BasicInfo) -> str:
    return self.slug


class BasicInfo(Entity):
    """
    Basic Entity fields for objects that are meant to be user-facing.
    """

    name: str
    """Human readable display name of the object in question."""

    slug: str = field(metadata=frozen_field)
    """A machine-accessible name that can be used for interfaces (e.g., URL token,
    CLI argument).  Human-friendlier version of entity_id.  Restricted to ASCII-token
    characters."""

    description: str = ""
    """Human readable description of the object."""

    id_name: str = field(metadata=frozen_field,
                         default=Factory(factory=_slug, takes_self=True))
    """This redefinition of the :attr:`Entity.id_name` field changes the default factory to
    point to the :attr:`slug` field."""


class ValueObject(BudoBase, attrs={'frozen': True}):
    """Common data and operations for Value Objects."""
