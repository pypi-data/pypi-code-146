from dataclasses import dataclass
from datetime import date
from typing import Union

from eokulapi.Models import from_int, from_str, month_to_int, str_to_date


@dataclass
class ExamSchedule:
    """Exam schedule model"""

    isPast: bool
    """Whether the exam is past or not"""
    date: date
    """Date of the exam"""
    lesson: str
    """Exam's lesson"""

    @classmethod
    def from_dict(cls, obj: dict) -> Union["ExamSchedule", list["ExamSchedule"], None]:
        """Converts a dict to ExamSchedule object

        Args:
            obj (dict): Object to be converted

        Returns:
            ExamSchedule: If obj contains only one exam schedule, returns ExamSchedule object that is converted from dict
            list[ExamSchedule]: If obj contains multiple exam schedules, returns list of ExamSchedule objects that are converted from dict
            None: If obj doesn't contain any exam schedule
        """
        dtype = from_int(obj.get("Liste"))
        if dtype == 2:
            isPast = False
            gun = from_str(obj.get("Ders")).split()
            ders = from_str(obj.get("Gun"))
        elif dtype == 3:
            isPast = True
            gun = from_str(obj.get("Gun")).split()
            ders = from_str(obj.get("Ders"))
        else:
            return None
        date_str = f"{gun[0]:02};{month_to_int(gun[1]):02};{gun[2]:04}"
        dt = str_to_date(date_str)

        if dtype == 3:
            return [cls(isPast, dt, d) for d in ders.split("|")]

        return cls(isPast, dt, ders)
