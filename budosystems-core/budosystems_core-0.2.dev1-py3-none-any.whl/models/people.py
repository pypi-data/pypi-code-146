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

"""People related Entity classes and tools."""

from __future__ import annotations

from datetime import date, timedelta

import attr

from . import core, contact, style
from .. import typehints as th

# entity_classes = {'Person', 'Household', 'UserAccount'}
# link_classes = {'FamilyMember', 'StudentRank', 'StudentRequirement'}
# __all__ = list(entity_classes | link_classes | {'entity_classes', 'link_classes'})

__all__ = ["Person", "UserAccount", "Gender", "genders", "Household"]


class UserAccount(core.Entity):
    """
    Represents the login profile and credentials of a system user.
    """

    username: str
    password: str

class Gender(core.ValueObject):
    """Gender representation. Allows for more than male & female."""
    label: str
    subjective_pronoun: str
    objective_pronoun: str
    possessive_pronoun: str
    reflexive_pronoun: str


# Samples of well-known genders to show how flexible Gender class is an how to create new instances.
# Note: This is very Anglo-centric.  How do we make this more i18n friendly?
genders: dict[str, Gender] = dict(
        male=Gender(
                label="male",
                subjective_pronoun="he",
                objective_pronoun="him",
                possessive_pronoun="his",
                reflexive_pronoun="himself"
        ),
        female=Gender(
                label="male",
                subjective_pronoun="she",
                objective_pronoun="her",
                possessive_pronoun="hers",
                reflexive_pronoun="herself"
        ),
        nonbinary_they=Gender(
                label="non-binary",
                subjective_pronoun="they",
                objective_pronoun="they",
                possessive_pronoun="theirs",
                reflexive_pronoun="themselves"
        ),
        nonbinary_ze=Gender(
                label="non-binary",
                subjective_pronoun="ze",
                objective_pronoun="hir",
                possessive_pronoun="hirs",
                reflexive_pronoun="hirself"
        )
)
genders |= dict(
        cismale=attr.evolve(genders['male'], label="cismale"),
        cisfemale=attr.evolve(genders['female'], label="cisfemale"),
        transmale=attr.evolve(genders['male'], label="transmale"),
        transfemale=attr.evolve(genders['female'], label="transfemale"),
        nonbinarytrans_they=attr.evolve(genders['nonbinary_they'], label="non-binary-trans")
)

class Person(contact.Contactable):
    """An individual person.

    This Entity stores information about the person's name, contact information."""

    # Personal info
    title: th.OptStr
    first_name: th.OptStr
    middle_name: th.OptStr
    last_name: th.OptStr
    suffix: th.OptStr
    date_of_birth: th.OptDate
    gender: th.Optional[Gender]

    # Stats
    start_date: th.Optional[date]

    def __attrs_post_init__(self, **_kwargs: th.Any) -> None:
        self._name_fields: th.Optional[th.List[str]] = None

    @property
    def age_delta(self) -> th.Optional[timedelta]:
        """
        Calculates the age as a :class:`datetime.timedelta`

        :return: The age as a
        """
        if self.date_of_birth:
            return date.today() - self.date_of_birth
        return None

    @property
    def age_years(self) -> th.Optional[int]:
        """
        Calculates the age in years and returns the result.
        :return: The age in years of the person, or None if there's no date of birth.
        """
        if self.date_of_birth:
            today = date.today()
            years = today.year - self.date_of_birth.year
            if today.month == self.date_of_birth.month:
                if today.day < self.date_of_birth.day:
                    years -= 1
            elif today.month < self.date_of_birth.month:
                years -= 1
            return years
        return None

    @property
    def name_fields(self) -> th.List[str]:
        """

        :return: List of fields used to compose the name.
        """
        if not hasattr(self, '_name_fields') or not self._name_fields:
            self._name_fields = ['title', 'first_name', 'middle_name', 'last_name', 'suffix']
        return self._name_fields

    @property
    def names_list(self) -> list[str]:
        """

        :return: List of name components.
        """
        return [getattr(self, nf) for nf in self.name_fields]

    @property
    def ranks(self) -> list[style.Rank]:
        """
        :return: The rank history of this student.
        """
        raise NotImplementedError()


class Household(contact.Contactable):
    """
    Represents a household.

    Contact information shared by everyone in the household should be stored here to reduce
    redundant information.
    """
    family_members: th.List[Person]
    primary_contact: Person
