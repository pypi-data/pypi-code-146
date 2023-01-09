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

"""Metaclasses for the models."""

from __future__ import annotations

from uuid import NAMESPACE_DNS, uuid5, UUID
from types import MappingProxyType
from typing import TYPE_CHECKING
from abc import ABCMeta

import attr

from .. import typehints as th
from ..events.base import FieldModifiedEvent, Timing
from ..events import MESSAGE_BUS
from ..utils import SingletonMeta

__all__ = ['BudoMeta', 'BudoBase', 'NAMESPACE_BUDO_SYSTEMS', 'ABCBudoMeta', 'SingletonBudoMeta',
           'frozen_field']

NAMESPACE_BUDO_SYSTEMS: th.Final[UUID] = uuid5(NAMESPACE_DNS, 'budo.systems')
"""A new namespace used as a base for class UUIDs."""

frozen_field = {'frozen': True}
AT = th.TypeVar('AT')


def _default_no_eq(cls: 'BudoMeta', fields: th.List[attr.Attribute[AT]]) \
        -> th.List[attr.Attribute[AT]]:
    # pylint: disable=protected-access
    if cls.frozen:
        return fields

    new_field_list: th.List[attr.Attribute[AT]] = []
    for f in fields:
        if f.metadata.get('frozen', False):
            f = f.evolve(
                    eq=True,
                    hash=True,
                    on_setattr=attr.frozen)
        else:
            f = f.evolve(
                    eq=False,
                    hash=False,
                    on_setattr=_signal_update)
        new_field_list.append(f)
    return new_field_list


F_Type = th.TypeVar("F_Type")

def _signal_update(instance: th.Any, field: attr.Attribute[F_Type], new_value: F_Type) -> F_Type:
    old_value = getattr(instance, field.name)
    event = FieldModifiedEvent[F_Type](
            instance=instance,
            field_name=field.name,
            old_value=old_value,
            new_value=new_value,
            timing=Timing.Before
    )

    MESSAGE_BUS.signal(event)

    return new_value


default_attr_config: th.DictStrAny = {
        'kw_only':          True,
        'auto_attribs':     True,
        'auto_detect':      True,
        'collect_by_mro':   True,
        'field_transformer': _default_no_eq,
        'hash':             True,
        'order':            False,
}


class BudoMeta(type):
    """
    Class level common attributes for all model classes.

    :param 'config':
        Class level configuration map (for things not covered by `attrs`)

        Currently recognized keywords:

        `allow_extra`
            Flag to determine whether instances may have extra data attributes
            not specified by the class (and its ancestors). Default: False
    :param 'attrs': A map of keywords to customize the ~`attr.attrs` features of the class
    :param 'kwargs': Any other information to be stored in the class
    :returns: An ~`attr.attrs` wrapped version of the defined class.
    """

    def __new__(mcs, cls_name: str, bases: th.Bases, namespace: th.DictStrAny,
                *,
                attrs: th.Optional[th.IMapStrAny] = None,
                **_kwargs: th.Any) -> BudoMeta:

        # ### Implement all instances of this metaclass as attrs.
        # Merge the `attrs` parameter with the default values.
        attr_config = default_attr_config.copy()
        if attrs:
            attr_config.update(attrs)

        # Check for frozen state before class creation t
        def _frozen_base() -> bool:
            # lazy eval
            return any({getattr(b, 'frozen', False) for b in bases})

        namespace['_frozen'] = attr_config.get('frozen', False) or _frozen_base()

        new_cls: BudoMeta = attr.s(super().__new__(mcs, cls_name, bases, namespace), **attr_config)

        return new_cls

    def __init__(cls, cls_name: str, bases: th.Bases, namespace: th.DictStrAny,
                 *,
                 attrs: th.Optional[th.IMapStrAny] = None,
                 **kwargs: th.Any) -> None:
        super().__init__(cls_name, bases, namespace, **kwargs)

        _used_in_new = [attrs]

        cls._metadata: th.MMapStrAny = kwargs
        cls._uuid: UUID = uuid5(NAMESPACE_BUDO_SYSTEMS, cls_name)

    @property
    def uuid(cls) -> UUID:
        """A class level UUID that can be used to generate reproducible Entity IDs."""
        return cls._uuid

    @property
    def metadata(cls) -> th.IMapStrAny:
        """Class meta-data. Read-only."""
        return MappingProxyType(cls._metadata)

    @property
    def frozen(cls) -> bool:
        """Whether or not the class is frozen."""
        return th.cast(bool, cls._frozen)  # type: ignore[attr-defined]


class ABCBudoMeta(BudoMeta, ABCMeta):
    """Metaclass for Budo classes that also inherit from ABC (e.g. via Generics)"""

class SingletonBudoMeta(BudoMeta, SingletonMeta):
    """Metaclass for Budo classes intended to be singletons."""

class BudoBase(metaclass=BudoMeta):
    """Base class for all classes that are meant to have BudoMeta as a metaclass."""

    if TYPE_CHECKING:
        __attrs_attrs__: th.ClassVar[th.Any]

    # Just here for the linters.
    def __init__(self, **kwargs: th.Any) -> None:
        """
        :param kwargs: If the `allow_extra` flag on the class is True, all items are stored in an
            `extra` field.
        """
    #     if type(self).config['allow_extra']:
    #         self.extra: th.MMapStrAny = kwargs.copy()
