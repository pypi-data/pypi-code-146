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

"""Everything related to contact information."""

from __future__ import annotations

from collections.abc import MutableMapping, ItemsView, KeysView, ValuesView, Mapping, Iterable

import warnings

# from attr import field  # type: ignore # conditionally exported
import attr

from email_validator import validate_email, EmailNotValidError  # type: ignore

from .. import typehints as th
from . import core, meta

from .validation import ValidationWarning

__all__ = ['Contact', 'PhoneNumber', 'EmailAddress', 'PhysicalAddress', 'ContactList',
           'Contactable', 'MissingContact']

# pylint: disable=too-few-public-methods

class Contact(core.ValueObject):
    """
    General structure for objects that represent some sort of contact information.
    """
    #:  Human readable identifier of what this contact represents.  This typically will
    #:      be a short word or phrase (e.g., "home", "office", "alt website")
    label: str

    #:  The contact address as a string.
    value: str

class MissingContact(Contact, metaclass=meta.SingletonBudoMeta,
                     label="None", value="Missing"):
    """Singleton contact to indicate that the contact is missing."""


CT = th.TypeVar('CT', bound=Contact)
CT_Missing = th.Union[CT, MissingContact]

if not th.TYPE_CHECKING:
    ellipsis = type(Ellipsis)
OptStrEllipsis = th.Union[str, ellipsis, None]


class ContactList(core.Entity, MutableMapping[OptStrEllipsis, CT_Missing[CT]],
                  metaclass=meta.ABCBudoMeta):
    """Aggregate class for Contacts. Each list has a 'preferred' contact from the list, which
    can be accessed by passing `...` (`Ellipsis`) or None as the key to the map operations."""

    # pylint: disable=unnecessary-ellipsis

    data: dict[str, CT_Missing[CT]] = attr.ib(factory=dict)
    preferred: th.OptStr = None

    def _true_key(self, key: OptStrEllipsis) -> str:
        if (key is None or key is ...) and self.preferred:
            return self.preferred
        if isinstance(key, str):
            return key
        raise KeyError

    def __setitem__(self, key: OptStrEllipsis, value: CT_Missing[CT]) -> None:
        """

        :param key:
        :param value:
        """
        if (key is None or key is ...) and isinstance(value, Contact):
            key = value.label
        assert isinstance(key, str)
        self.data[key] = value  # pylint: disable=unsupported-assignment-operation
        if len(self.data) == 1:
            self.preferred = key

    def __getitem__(self, key: OptStrEllipsis) -> CT_Missing[CT]:
        """

        :param key:
        :return:
        """
        _key = self._true_key(key)
        return self.data[_key]

    def __delitem__(self, key: OptStrEllipsis) -> None:
        """

        :param key:
        """
        _key = self._true_key(key)
        del self.data[_key]  # pylint: disable=unsupported-delete-operation

        if len(self.data) == 0:
            self.preferred = None
        elif len(self.data) > 0 and key == self.preferred:
            self.preferred = list(self.data.keys())[0]

    def __iter__(self) -> th.Iterator[str]:
        return iter(self.data)

    def __len__(self) -> int:
        return len(self.data)

    def __contains__(self, item: object) -> bool:
        return item in self.data    # pylint: disable=unsupported-membership-test

    def keys(self) -> KeysView[str]:
        """See `dict.keys`"""
        return self.data.keys()

    def items(self) -> ItemsView[str, CT_Missing[CT]]:
        """See `dict.items`"""
        return self.data.items()

    def values(self) -> ValuesView[CT_Missing[CT]]:
        """See `dict.values`"""
        return self.data.values()

    def get(self, key: OptStrEllipsis,  # type: ignore[override]
            default: CT_Missing[CT] = MissingContact()) -> CT_Missing[CT]:
        """See `dict.get`"""
        _key = self._true_key(key)
        return self.data.get(_key, default)

    def __eq__(self, other: th.Any) -> bool:
        return super().__eq__(other) or self.data == other

    def __ne__(self, other: th.Any) -> bool:
        return self.data != other and super().__ne__(other)

    def pop(self, key: OptStrEllipsis,  # type: ignore[override]
            default: CT_Missing[CT] = MissingContact()) -> CT_Missing[CT]:
        """See `dict.pop`"""
        _key = self._true_key(key)
        return self.data.pop(_key, default)

    def popitem(self) -> tuple[str, CT_Missing[CT]]:
        """See `dict.popitem`"""
        return self.data.popitem()

    def clear(self) -> None:
        """See `dict.clear`"""
        self.data.clear()

    # pylint: disable=arguments-differ, signature-differs
    @th.overload    # type: ignore[override]
    def update(self, values: Mapping[str, CT], **kwargs: CT) -> None:
        ...

    @th.overload
    def update(self, values: Iterable[tuple[str, CT]], **kwargs: CT) -> None:
        ...

    @th.overload
    def update(self, values: None = None, **kwargs: CT) -> None:
        ...

    def update(self,
               values: th.Union[Mapping[str, CT], Iterable[tuple[str, CT]], None] = None,
               **kwargs: CT
               ) -> None:
        """See `dict.update`"""
        if values is None:
            self.data.update(**kwargs)
        else:
            self.data.update(values, **kwargs)

    def setdefault(self, key: OptStrEllipsis,       # type: ignore[override]
                   default: CT_Missing[CT] = MissingContact()) -> CT_Missing[CT]:
        """See `dict.setdefault`"""
        _key = self._true_key(key)

        # if isinstance(default, MissingContact):
        #     return self.data.setdefault(_key, default)
        return self.data.setdefault(_key, default)


class Contactable(core.Entity):
    """Convenience class for Entities that can have
    addresses, phone numbers, and email addresses.
    """
    phone_numbers: ContactList[PhoneNumber] = attr.ib(factory=ContactList)
    email_addresses: ContactList[EmailAddress] = attr.ib(factory=ContactList)
    physical_addresses: ContactList[PhysicalAddress] = attr.ib(factory=ContactList)


class PhoneNumber(Contact):
    """
    Identifies this object as a phone number.

    :keyword is_fax: Whether this phone number is for a fax-machine.
    :keyword can_text: Whether this phone number can receive text messages.
    """
    is_fax: bool
    can_text: bool


class EmailAddress(Contact):
    """Identifies this object as an e-mail address."""
    def _validate_email_format(self) -> th.OptBool:
        if self.value:  # pylint: disable=no-member
            try:
                valid = validate_email(self.value)  # pylint: disable=no-member
                return bool(valid)
            except EmailNotValidError as err:
                warnings.warn(ValidationWarning('Email address is not valid.', err))
                return False
        warnings.warn(ValidationWarning('Email not set'))
        return None


class PhysicalAddress(Contact):
    """
    Identifies this object as a physical address.

    :keyword locale: The ISO code used to assist in representing the address meaningfully.
    :keyword address: The address split in its component parts.
    """
    locale: str
    address: th.DictStrAny = attr.ib(factory=dict)
