from dataclasses import dataclass

from eokulapi.Models import from_int, from_str
from eokulapi.Models.AvgMark import AvgMark


@dataclass
class AvgMarkLesson:
    """Average mark lesson model"""

    lesson_name: str
    """Name of the lesson"""
    term: int
    """Term of the lesson
    
    it is even for the first term and odd for the second term"""
    marks: dict[int, AvgMark]
    """Marks of the lesson as dict of AvgMark objects (Exam Number: AvgMark)"""

    @classmethod
    def from_dict(cls, obj: dict):
        """Converts a dict to AvgMarkLesson object

        Args:
            obj (dict): Object to be converted

        Returns:
            AvgMarkLesson: AvgMarkLesson object that is converted from dict
        """
        ders = from_str(obj.get("DERS"))
        donem = from_int(int(from_str(obj.get("DONEM"))))
        marks = {}
        for i in range(1, 7):
            mark = AvgMark.from_dict(
                {
                    "value": obj.get(f"Y{i}"),
                    "description": obj.get(f"Y{i}ACIKLAMA"),
                    "description_value": obj.get(f"Y{i}ACIKLAMADEGER"),
                    "avg_mark": obj.get(f"Y{i}SUBEORT"),
                }
            )
            marks[i] = mark
        return cls(ders, donem, marks)
