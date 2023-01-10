from dataclasses import dataclass
from typing import Any

from eokulapi.Models import from_int, from_str, str_to_float
from eokulapi.Models.AvgMarkLesson import AvgMarkLesson


@dataclass
class MarkLesson:
    """Mark lesson model

    Note that each MarkLesson object only contains one term data.
    Using lesson_id as a primary key among MarkLesson objects is not recommended.
    Use a combination of lesson_id and term instead."""

    lesson: str
    """Name of the lesson"""
    lesson_id: str
    """ID of the lesson"""
    lesson_weekly_period: int
    """Weekly period count of the lesson"""
    term: int
    """Term of the lesson
    
    it is even for the first term and odd for the second term"""
    isExempt: bool
    """Whether the student is exempt from the lesson"""
    odv: Any
    """Not implemented. possibly a float"""
    tpu: Any
    """Not implemented. possibly a float"""
    score: float
    """Score of the student in the lesson"""
    sozlu: dict[int, float]
    """Dict of `sözlü` exam scores (Exam Number: Score)
    
    Dict keys are from 1 to 6, but not all of them are present as `sozlu`:
    1: `performans1`
    2: `performans2`
    3: `performans3`
    4: `uygulama1`
    5: `uygulama2`
    6: `uygulama3`
    mark_to_str() method can be used to convert the keys to string representations of the marks.
    
    Note that all of the keys are *not* present in all of the lessons."""
    yazili: dict[int, float]
    """Dict of `yazılı` exam scores (Exam Number: Score)
    
    Dict keys are from 1 to 6, but not all of them are present as `yazili`:
    1: `sınav1`
    2: `sınav2`
    3: `sınav3`
    4: `sınav4`
    5: `sınav5`
    6: `ortak_sınav`
    mark_to_str() method can be used to convert the keys to string representations of the marks.
    
    Note that all of the keys are *not* present in all of the lessons."""

    def mark_to_str(self, mark_type: bool, mark_no: int) -> str:
        """Converts a mark number to a string representation of the mark

        Args:
            mark_type (bool): Whether the mark is `yazili` or `sozlu`.
            mark_no (int): Number of the mark, from 1 to 6

        Raises:
            AssertionError: If arguments are invalid

        Returns:
            str: String representation of the mark (e.g. `matematik 1. dönem 2. yazılı`)
        """

        assert mark_type in [True, False]
        assert mark_no in range(1, 7)

        string = ""

        string += self.lesson.replace("I", "ı").lower()  # to deal with Turkish characters

        string += " "

        if self.term % 2 == 0:
            string += "1. dönem"
        else:
            string += "2. dönem"

        string += " "

        if mark_type:  # yazili
            if 1 <= mark_no <= 5:
                string += f"{mark_no}. yazılı"
            elif mark_no == 6:
                string += "Ortak yazılı"
        else:  # sozlu
            if 1 <= mark_no <= 3:
                string += f"{mark_no}. performans"
            elif 4 <= mark_no <= 6:
                string += f"{mark_no-3}. uygulama"

        return string

    def isMarkOfSelf(self, object: object) -> bool:
        """Checks whether the object is a mark object for self

        Args:
            o (object): Object to check

        Returns:
            bool: Whether the object is a mark object for self
        """
        if isinstance(object, MarkLesson):
            return object.lesson == self.lesson and object.term == self.term
        return False

    def isAvgmarkOfSelf(self, object: object) -> bool:
        """Checks whether the object is an average mark object for self

        Args:
            o (object): Object to check

        Returns:
            bool: Whether the object is an average mark object for self
        """
        if isinstance(object, AvgMarkLesson):
            return object.lesson_name == self.lesson and object.term == self.term
        return False

    @classmethod
    def from_dict(cls, obj: dict):
        """Converts a dict to MarkLesson object

        Args:
            obj (dict): Object to be converted

        Returns:
            MarkLesson: MarkLesson object that is converted from dict
        """
        ders = from_str(obj.get("Ders"))
        ders_kodu = from_str(obj.get("DersKodu"))
        ders_saati = from_int(int(from_str(obj.get("DersSaati"))))
        donem = from_int(int(from_str(obj.get("Donem"))))
        muaf = False if from_str(obj.get("Muaf")) == "-" else True
        odv = obj.get("ODV")
        tpu = obj.get("TPU")
        puan = str_to_float(obj.get("PUANI"))

        sozlu: dict[int, float] = {}
        yazili: dict[int, float] = {}

        for i in range(1, 7):
            dat = from_str(obj.get(f"SZL{i}"))
            if dat:
                sozlu[i] = str_to_float(dat)
        for i in range(1, 7):
            dat = from_str(obj.get(f"Y{i}"))
            if dat:
                yazili[i] = str_to_float(dat)

        return cls(ders, ders_kodu, ders_saati, donem, muaf, odv, tpu, puan, sozlu, yazili)
