from __future__ import annotations

import typing
from dataclasses import dataclass


@dataclass(init=False, repr=False)
class Assignment:
    parentCategory: Category
    objectSectionID: int
    parentObjectSectionID: None | typing.Any
    type: int
    personID: int
    taskID: int
    groupActivityID: int
    termIDs: list[int]
    assignmentName: str
    calendarID: int
    structureID: int
    sectionID: int
    dueDate: str
    assignedDate: str
    modifiedDate: str
    courseName: str
    active: bool
    scoringType: str
    score: str
    scorePoints: str
    scorePercentage: str
    totalPoints: int
    comments: None | typing.Any
    feedback: None | typing.Any
    late: bool
    missing: bool
    cheated: bool
    dropped: bool
    incomplete: bool
    turnedIn: bool
    wysiwygSubmission: bool
    upload: bool
    driveSubmission: bool
    multiplier: float
    hasStudentHTML: None | typing.Any
    hasTeacherHTML: None | typing.Any
    hasQuiz: None | typing.Any
    hasLTI: None | typing.Any
    hasLTIAcceptsScores: None | typing.Any
    hasFile: None | typing.Any
    hasExternalFile: None | typing.Any
    hasSubmission: None | typing.Any
    hasDiscussion: None | typing.Any
    hasRubric: None | typing.Any
    notGraded: bool
    isValidRubric: bool
    isValidMark: bool
    includeCampusLearning: bool

    def __init__(self, **kwargs) -> None:
        for kwarg in kwargs.keys():
            setattr(self, kwarg, kwargs[kwarg])

    def __getattr__(self, __name) -> None:
        return None

    def __repr__(self):
        return "{}: {}.".format(self.assignmentName, self.scorePercentage)


@dataclass(init=False, repr=False)
class Category:
    assignments: list[Assignment]
    categoryID: int
    sectionID: int
    name: str
    curveID: None | typing.Any
    weight: float
    seq: int
    hidePortal: None | typing.Any
    calcExclude: bool
    groupCourseID: None | typing.Any
    modifiedByID: int
    modifiedDate: str
    districtManaged: bool
    districtSourced: bool

    def __init__(self, **kwargs) -> None:
        for kwarg in kwargs.keys():
            setattr(self, kwarg, kwargs[kwarg])

    def __getattr__(self, __name) -> None:
        return None

    def __repr__(self):
        return f"{self.name} (weight: {self.weight})"
