from dataclasses import dataclass

from eokulapi.Models import from_list
from eokulapi.Models.MarkLesson import MarkLesson


@dataclass
class MarkContainer:
    """Mark container model"""

    avg: float | None
    """Average mark of the student"""
    data: list[MarkLesson]
    """Mark data as list of MarkLesson objects"""

    @classmethod
    def from_dict(cls, obj: dict):
        """Converts a dict to MarkContainer object

        Args:
            obj (dict): Object to be converted

        Returns:
            MarkContainer: MarkContainer object that is converted from dict
        """
        liste = from_list(MarkLesson.from_dict, obj.get("notListesi"))
        ort = sum([lesson.lesson_weekly_period * lesson.score for lesson in liste]) / sum(
            [lesson.lesson_weekly_period for lesson in liste]
        )

        return cls(ort, liste)
