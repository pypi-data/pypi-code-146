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

"""Martial arts business, studio, style, and rank related Entity classes and tools."""

from __future__ import annotations

import operator
from datetime import timedelta
from collections.abc import Set

from attr import field

from . import core, contact, meta
from .. import typehints as th

__all__ = ['Business', 'Studio', 'Style', 'Curriculum', 'Rank',
           'Requirement', 'NoRequirement', 'RequirementGroup', 'Skill',
           'N_OfRequirementGroup', 'TimeInClassRequirement', 'TimeInRankRequirement',
           'AttendanceRequirement', 'GenericRequirement']

class Business(contact.Contactable, core.BasicInfo):
    """Represents the business(es) at the root of the database."""

    def __attrs_post_init__(self) -> None:
        super().__attrs_post_init__()
        self._studios: set[Studio] = set()

    @th.Property[Set['Studio']]
    def studios(self) -> Set[Studio]:
        """Locations owned/managed by this business.  (Read-only)"""
        return frozenset(self._studios)

    def add_studio(self, studio: Studio, reciprocate: bool = True) -> None:
        """
        Add a business location to this business.

        :param studio: The studio to add.
        :param reciprocate: Whether to reciprocate the operation on `studio`.
        """
        self._studios.add(studio)
        if reciprocate:
            studio.add_business(self, False)

    def remove_studio(self, studio: Studio, reciprocate: bool = True) -> None:
        """
        Removes a business location from this business.

        :param studio: The studio to remove.
        :param reciprocate: Whether to reciprocate the operation on `studio`.
        """
        self._studios.remove(studio)
        if reciprocate:
            studio.remove_business(self, False)

class Studio(contact.Contactable, core.BasicInfo):
    """Represents the business location(s) where the classes are."""

    def __attrs_post_init__(self) -> None:
        self._styles: set[Style] = set()
        self._businesses: set[Business] = set()

    @th.Property[Set['Style']]
    def styles(self) -> Set[Style]:
        """Styles taught at the studio.  (Read-only)"""
        return frozenset(self._styles)

    def add_style(self, style: Style, reciprocate: bool = True) -> None:
        """
        Add a style to this studio.

        :param style: The style to add.
        :param reciprocate: Whether to reciprocate the operation on `style`.
        """
        self._styles.add(style)
        if reciprocate:
            style.add_studio(self, False)

    def remove_style(self, style: Style, reciprocate: bool = True) -> None:
        """
        Remove a style to this studio.

        :param style: The style to remove.
        :param reciprocate: Whether to reciprocate the operation on `style`.
        """
        self._styles.remove(style)
        if reciprocate:
            style.remove_studio(self, False)

    @th.Property[Set[Business]]
    def businesses(self) -> Set[Business]:
        """Businesses co-located at this studio.  (Read-only)"""
        return frozenset(self._businesses)

    def add_business(self, business: Business, reciprocate: bool = True) -> None:
        """
        Add a style to this studio.

        :param business: The business to add.
        :param reciprocate: Whether to reciprocate the operation on `business`.
        """
        self._businesses.add(business)
        if reciprocate:
            business.add_studio(self, False)

    def remove_business(self, business: Business, reciprocate: bool = True) -> None:
        """
        Remove a style to this business.

        :param business: The business to remove.
        :param reciprocate: Whether to reciprocate the operation on `business`.
        """
        self._businesses.remove(business)
        if reciprocate:
            business.remove_studio(self, False)

class Style(core.BasicInfo):
    """
    Represents the business of practice (e.g., martial arts business) being taught at the business.
    """
    curriculum: th.Optional[Curriculum] = None
    """The set of requirements for progression within the style."""

    def __attrs_post_init__(self) -> None:
        super().__attrs_post_init__()
        self._studios: set[Studio] = set()

    @th.Property[Set[Studio]]
    def studios(self) -> Set[Studio]:
        """Locations owned/managed by this style.  (Read-only)"""
        return frozenset(self._studios)

    def add_studio(self, studio: Studio, reciprocate: bool = True) -> None:
        """
        Add a studio to this style.

        :param studio: The studio to add.
        :param reciprocate: Whether to reciprocate the operation on `studio`.
        """
        self._studios.add(studio)
        if reciprocate:
            studio.add_style(self, False)

    def remove_studio(self, studio: Studio, reciprocate: bool = True) -> None:
        """
        Remove a studio to this style.

        :param studio: The studio to remove.
        :param reciprocate: Whether to reciprocate the operation on `studio`.
        """
        self._studios.remove(studio)
        if reciprocate:
            studio.remove_style(self, False)

class Curriculum(core.BasicInfo):
    """
    Represents the training curriculum.

    For studios that have their students progress in rank based on specific requirements.
    """
    style: Style
    """The style for which this curriculum applies."""

    requirement_schema: dict[str, str] = field(factory=dict)
    """An ordered dictionary of (tag: label), used for organizing requirements within the rank.

    The key (tag) is intended to be for internal purposes only.
    The value (label) is intended to be public facing.
    """

    @property
    def lowest_rank(self) -> Rank:
        """
        Returns the lowest rank in the curriculum.

        :returns: The lowest rank of this curriculum.
        """
        raise NotImplementedError

    def add_rank(self, rank: Rank) -> None:
        """
        Adds a rank to this curriculum.

        :param rank: The rank to be added.
        """
        raise NotImplementedError

    def remove_rank(self, rank: Rank) -> None:
        """
        Removes a rank from this curriculum.

        :param rank: The rank to be removed.
        """
        raise NotImplementedError

    def clone(self, equivalent_ranks: bool = False) -> Curriculum:
        """Creates a deep copy of this curriculum including it ranks. If
        `equivalent_ranks` is True, then create an equivalence mapping.

        :param equivalent_ranks: Whether to create an equivalence relationship between the ranks
            of this curriculum and those of the clone.
        :returns: A clone of this curriculum.
        """
        raise NotImplementedError

class Rank(core.BasicInfo):
    """
    Represents a martial art rank.
    """
    curriculum: Curriculum
    """The curriculum used to evaluate this rank."""

    rank_order: int
    """The relative position of this rank compared to others in the curriculum."""

    def __attrs_post_init__(self) -> None:
        self.curriculum.add_rank(self)  # Autolink rank and curriculum

    def _common_cmp(self, op: th.BoolBinOp, other: th.Union[Rank, object]) -> bool:
        if not isinstance(other, Rank):
            return NotImplemented
        if self.curriculum != other.curriculum:
            return False
        return op(self.rank_order, other.rank_order)

    def __eq__(self, other: th.Union[Rank, object]) -> bool:
        return self._common_cmp(operator.eq, other)

    def __ne__(self, other: th.Union[Rank, object]) -> bool:
        # Doing not `operator.eq` instead of `operator.ne` because of how curriculum factors in
        return not self._common_cmp(operator.eq, other)

    def __lt__(self, other: th.Union[Rank, object]) -> bool:
        return self._common_cmp(operator.lt, other)

    def __le__(self, other: th.Union[Rank, object]) -> bool:
        return self._common_cmp(operator.le, other)

    def __gt__(self, other: th.Union[Rank, object]) -> bool:
        return self._common_cmp(operator.gt, other)

    def __ge__(self, other: th.Union[Rank, object]) -> bool:
        return self._common_cmp(operator.ge, other)

    @th.Property[Style]
    def style(self) -> Style:
        """Convenience property to access the business."""
        return self.curriculum.style

class Requirement(core.BasicInfo):
    """Base class for a requirement for a student to meet to earn a rank."""

class NoRequirement(Requirement, metaclass=meta.SingletonBudoMeta,
                    name="∅", slug="none", description="No Requirement"):
    """Singleton `Requirement` indicating that there are no specific requirements.
    Serves as a placeholder where needed."""

class Skill(Requirement):
    """
    Specialized `Requirement` representing a teachable skill the student can learn.
    """
    instructions: str
    """The instructions a student can read to correctly perform the skill."""

    teaching_notes: str
    """Additional notes meant for instructors to assist them on how to teach this skill."""

class RequirementGroup(Requirement):
    """
    Specialized `Requirement` for grouping multiple other Requirement objects under a single
    entry.

    Can be used as an 'AND' combinator.
    """
    group: list[Requirement]
    """A list of requirements."""

class N_OfRequirementGroup(RequirementGroup):
    """
    `RequirementGroup` where only a subset of the requirements needs to be met.

    Can be used as an 'OR' combinator (with `min_in_group` = 1).
    """
    min_in_group: int
    """The minimum number of requirements within the group that must be met."""

class TimeInClassRequirement(Requirement):
    """
    Specialized `Requirement` for time in class expectations.
    """
    min_class_time: timedelta = timedelta(0)
    """The minimum duration of time a student must attend in class since
        last rank before being eligible for this rank."""

    def min_class_dhm(self, *, days: int = 0, hours: int = 0, minutes: int = 0) -> None:
        """
        An alternative setter for `min_class_time`.

        :param days: Number of days portion of minimum class time.
            (Note: 1 day = 24 hours, not 1 session; for the latter see `AttendanceRequirement`)
        :param hours: Number of hours portion of minimum class time.
        :param minutes: Number of minutes portion of minimum class time.
        """
        self.min_class_time = timedelta(days=days, hours=hours, minutes=minutes)

class TimeInRankRequirement(Requirement):
    """
    Specialized `Requirement` for time in rank expectations.
    """
    min_rank_time: timedelta = timedelta(0)
    """Minimum duration since earning last rank before being eligible for this rank."""

    def min_rank_days(self, *,
                      years: int = 0, months: int = 0, weeks: int = 0, days: int = 0) -> None:
        """
        An alternative setter for `min_rank_time`.

        :param years: Minimum number of years in rank.
            Multiples of 365 days (no regard for leap years)
        :param months: Minimum number of months in rank.
            Multiples of 30 days (no regard for month length variations)
        :param weeks: Minimum number of weeks in rank.
            Multiples of 7 days.
        :param days: Minimum number of days in rank.
            (Note: 1 day = 24 hours, not 1 session; for the latter see `AttendanceRequirement`.)
        """
        self.min_rank_time = timedelta(days=365*years + 30*months + 7*weeks + days)

class AttendanceRequirement(Requirement):
    """
    Specialized `Requirement` for minimum attendance expectations.
    """
    min_attended_classes: int
    """Minimum number of classes to attend since last rank before being
        eligible for this rank."""

class GenericRequirement(Requirement):
    """
    `Requirement` type for cases not represented by another specialization.
    """
    wording: str
    """Criteria expressed in natural language."""
