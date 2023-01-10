from dataclasses import dataclass

from eokulapi.Models import day_to_int, from_list
from eokulapi.Models.Lesson import Lesson


@dataclass
class LessonDay:
    """Lesson day model to represent a day in a week"""

    day_number: int
    """Day number of the week"""
    LessonList: list[Lesson]
    """List of lessons in the day"""

    @classmethod
    def from_dict(cls, obj: dict):
        """Converts a dict to LessonDay object

        Args:
            obj (dict): Object to be converted

        Returns:
            LessonDay: LessonDay object that is converted from dict
        """
        liste = from_list(Lesson.from_dict, obj.get("DersProgramiItemList"))
        day = day_to_int(obj.get("Gun"))
        return cls(day, liste)
