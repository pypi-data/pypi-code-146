from dataclasses import dataclass
from datetime import time
from typing import Optional

from eokulapi.Models import from_int, from_none, from_str, from_union, str_to_time


@dataclass
class Lesson:
    """Lesson model to represent a lesson in a day"""

    start: time
    """Start time of the lesson"""
    end: time
    """End time of the lesson"""
    name: str
    """Name of the lesson"""
    nth: int
    """Nth lesson of the day"""
    teacher: Optional[str] = None
    """Teacher of the lesson, if known"""

    @classmethod
    def from_dict(cls, obj: dict):
        """Converts a dict to Lesson object

        Args:
            obj (dict): Object to be converted

        Returns:
            Lesson: Lesson object that is converted from dict
        """
        start = str_to_time(obj.get("Baslangic_Saati"))
        end = str_to_time(obj.get("Bitis_Saati"))
        name = from_str(obj.get("Ders"))
        nth = from_int(obj.get("KacinciDers"))
        teacher = from_union([from_str, from_none], obj.get("Ogretmen"))
        if not teacher:
            return cls(start, end, name, nth)
        if teacher[0] == " ":
            teacher = teacher[1:]
        return cls(start, end, name, nth, teacher)
