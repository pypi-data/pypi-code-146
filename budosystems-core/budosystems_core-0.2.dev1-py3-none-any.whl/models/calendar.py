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

"""Calendar related Entity classes and tools."""

from __future__ import annotations
from datetime import date, time, timedelta

from icalendar import cal  # type: ignore # No type hints
from dateutil import rrule

from . import core, people, style
from .. import typehints as th

class Calendar(core.Entity):
    """Represents a calendar."""
    _cal = cal.Calendar

    @classmethod
    def from_ical(cls, icaldata: str, multiple: bool = False) \
            -> th.Union[Calendar, th.List[Calendar]]:
        """
        Create a new Calendar instance from an iCal formatted string.

        :param icaldata: An iCal formatted string
        :param multiple: Whether to process `icaldata` as multiple calendars
        :returns: A Calendar or a list of them (depending on the value of `multiple`)
        """
        # Convert iCal string to a python data structure
        ical = cal.Calendar.from_ical(icaldata, multiple)

        # Process the data structure into our model to store in the database
        return cls(cal=ical)

    def to_ical(self, sort: bool = True) -> str:
        """
        Export the current Calendar object to an iCal string.

        :param sort: Whether to have the output sorted.
        :returns: An iCal formatted string
        """
        # Convert our model into the icalendar library data structure.
        self._cal = cal.Calendar()

        # TODO: The rest of this algorithm

        # Convert the result into a string
        return str(self._cal.to_ical(sort))


class TrainingClass(core.BasicInfo):
    """Represents an individual time slot for a class."""
    __collection__ = 'training_classes'

    training_date: date
    start_time: time
    duration: timedelta


class ClassSchedule(core.BasicInfo):
    """Represents a class schedule."""

    _rruleset_obj: rrule.rruleset

    template: TrainingClass
    recurrence: str  # rrule / rruleset

    @property
    def rrule(self) -> str:
        """"The class schedule as an iCal RRULE (Recurrence Rule) string."""
        return str(self._rruleset_obj)

    @rrule.setter
    def rrule(self, rrstr: str) -> None:
        self._rruleset_obj = th.cast(rrule.rruleset, rrule.rrulestr(rrstr, forceset=True))


class Attendance(core.Entity):
    """An individual attendance record entry for a student."""
    student: people.Person
    session: TrainingClass
    late: timedelta
    left_early: timedelta


class ClassCurriculum(core.Entity):
    """Links a TrainingClass to a Curriculum taught in that class."""
    session: TrainingClass
    curriculum: style.Curriculum
