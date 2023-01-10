from dataclasses import dataclass
from typing import Optional

from eokulapi.Models.AbsenteeismContainer import AbsenteeismContainer
from eokulapi.Models.AdditionalExam import AdditionalExam
from eokulapi.Models.AvgMarkContainer import AvgMarkContainer
from eokulapi.Models.DocumentContainer import DocumentContainer
from eokulapi.Models.EndtermMarkContainer import EndtermMarkContainer
from eokulapi.Models.ExamScheduleContainer import ExamScheduleContainer
from eokulapi.Models.LessonSchedule import LessonSchedule
from eokulapi.Models.MarkContainer import MarkContainer
from eokulapi.Models.Responsibility import Responsibility
from eokulapi.Models.Transfer import Transfer


@dataclass
class EokulStudent:
    """Eokul student model"""

    tckn: int
    """Student's Turkish Citizen Identification Number"""
    name: str
    """Student's name"""
    class_: str
    """Student's class"""
    grade: int
    """Student's grade"""
    number: int
    """Student's school number"""
    photo: bytes
    """Student's photo as jpeg bytes"""
    marks: Optional[MarkContainer] = None
    """Student's marks as MarkContainer object"""
    absenteeism: Optional[AbsenteeismContainer] = None
    """Student's absenteeism information as AbsenteeismContainer object"""
    lesson_schedule: Optional[LessonSchedule] = None
    """Student's lesson schedule as LessonSchedule object"""
    exam_schedule: Optional[ExamScheduleContainer] = None
    """Student's exam schedule as ExamScheduleContainer object"""
    class_exam_average: Optional[AvgMarkContainer] = None
    """Student's class' exam average as AvgMarkContainer object"""
    endterm_marks: Optional[EndtermMarkContainer] = None
    """Student's endterm marks as EndtermMarkContainer object"""
    transfer: Optional[Transfer] = None
    """Student's transfer information as Transfer object"""
    responsibility: Optional[Responsibility] = None
    """Student's responsibility information as Responsibility object"""
    documents: Optional[DocumentContainer] = None
    """Student's documents as DocumentContainer object"""
    additionalexams: Optional[AdditionalExam] = None
    """Student's additional exam data as AdditionalExam object"""

    def __eq__(self, __o: object) -> bool:
        if not isinstance(__o, EokulStudent):
            return False
        return self.tckn == __o.tckn
